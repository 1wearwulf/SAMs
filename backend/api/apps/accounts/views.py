"""
Views for the accounts app.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import User, UserDevice, PasswordResetToken
from .serializers import (
    UserSerializer, UserProfileSerializer, RegisterSerializer,
    LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer,
    UserDeviceSerializer, ChangePasswordSerializer
)
from api.permissions import IsOwnerOrLecturerOrAdmin
from utils.device_fingerprint import generate_device_fingerprint, get_device_info
from core.constants import PASSWORD_RESET_TOKEN_EXPIRY_HOURS


class UserViewSet(ModelViewSet):
    """
    ViewSet for User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrLecturerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.all()
        elif user.role == 'lecturer':
            # Lecturers can see students in their courses
            return User.objects.filter(
                role__in=['student', 'lecturer']
            ).distinct()
        else:
            # Students can only see themselves
            return User.objects.filter(id=user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current user profile.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        Update current user profile.
        """
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegisterView(APIView):
    """
    View for user registration.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Log device information
        device_info = get_device_info(request)
        UserDevice.objects.create(
            user=user,
            device_id=device_info.get('device_id', 'unknown'),
            device_type=device_info.get('device_type', 'unknown'),
            device_name=f"{device_info.get('browser', 'Unknown')} on {device_info.get('os', 'Unknown')}",
            ip_address=device_info.get('ip_address'),
            is_active=True
        )

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': access_token,
            },
            'message': 'User registered successfully.'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    View for user login.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate device fingerprint
        device_fingerprint = generate_device_fingerprint(request)

        # Check device consistency for security
        user_devices = UserDevice.objects.filter(
            user=user,
            is_active=True
        ).order_by('-last_used')

        device_consistency_check = True
        if user_devices.exists():
            # Compare with most recent device fingerprint
            recent_device = user_devices.first()
            if recent_device.device_fingerprint and recent_device.device_fingerprint != device_fingerprint:
                # Log suspicious activity
                # In production, you might want to send alerts or require additional verification
                pass

        # Update or create device record
        device_id = request.data.get('device_id', f"web_{user.id}_{timezone.now().timestamp()}")
        device, created = UserDevice.objects.get_or_create(
            user=user,
            device_id=device_id,
            defaults={
                'device_type': 'web',
                'device_name': f"Web Browser - {request.META.get('HTTP_USER_AGENT', '')[:50]}",
                'ip_address': request.META.get('REMOTE_ADDR'),
                'device_fingerprint': device_fingerprint,
                'is_active': True
            }
        )

        if not created:
            device.last_used = timezone.now()
            device.ip_address = request.META.get('REMOTE_ADDR')
            device.device_fingerprint = device_fingerprint
            device.save()

        # Perform login
        login(request, user)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': access_token,
            },
            'message': 'Login successful.'
        })


class LogoutView(APIView):
    """
    View for user logout.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Blacklist refresh token if provided
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        logout(request)
        return Response({'message': 'Logout successful.'})


class PasswordResetView(APIView):
    """
    View for password reset request.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.get(email=email)

        # Create password reset token
        reset_token = PasswordResetToken.objects.create(user=user)

        # Send email
        subject = 'Password Reset Request'
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'token': reset_token.token,
            'expiry_hours': PASSWORD_RESET_TOKEN_EXPIRY_HOURS,
        })

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=message,
            )
        except Exception as e:
            # Log error but don't fail the request
            pass

        return Response({
            'message': 'Password reset email sent if account exists.'
        })


class PasswordResetConfirmView(APIView):
    """
    View for password reset confirmation.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_token = serializer.validated_data['reset_token']
        new_password = serializer.validated_data['password']

        # Update password
        user = reset_token.user
        user.set_password(new_password)
        user.save()

        # Mark token as used
        reset_token.is_used = True
        reset_token.save()

        return Response({
            'message': 'Password reset successfully.'
        })


class ChangePasswordView(APIView):
    """
    View for changing password.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'message': 'Password changed successfully.'
        })


class UserDeviceViewSet(ModelViewSet):
    """
    ViewSet for UserDevice model.
    """
    serializer_class = UserDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Deactivate a device.
        """
        device = self.get_object()
        device.is_active = False
        device.save()

        return Response({
            'message': 'Device deactivated successfully.'
        })
