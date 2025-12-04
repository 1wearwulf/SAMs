from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import User, PasswordResetToken
from api.apps.devices.models import UserDevice
from .serializers import (
    UserSerializer, UserProfileSerializer, RegisterSerializer,
    LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer,
    UserDeviceSerializer, ChangePasswordSerializer
)
from api.permissions import IsOwnerOrLecturerOrAdmin

# ===== AUTH VIEWS =====
class RegisterView(generics.CreateAPIView):
    """View for user registration"""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """View for user login"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': 'Account is disabled'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LogoutView(APIView):
    """View for user logout"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception:
            # Even if token blacklisting fails, logout should succeed
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)


# ===== PROFILE VIEWS =====
class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrLecturerOrAdmin]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """View for changing password"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': ['Wrong password.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password updated successfully'})


# ===== PASSWORD RESET VIEWS =====
class PasswordResetView(APIView):
    """View for requesting password reset"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # For security, don't reveal if user exists
            return Response(
                {'message': 'If your email exists in our system, you will receive a password reset link.'},
                status=status.HTTP_200_OK
            )
        
        # Generate token
        token = get_random_string(50)
        expires_at = timezone.now() + timezone.timedelta(hours=24)
        
        # Create reset token
        PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)
        PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # TODO: Send email
        return Response({
            'message': 'If your email exists in our system, you will receive a password reset link.',
        })


class PasswordResetConfirmView(APIView):
    """View for confirming password reset"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reset_token = serializer.validated_data['reset_token']
        user = reset_token.user
        new_password = serializer.validated_data['password']
        
        # Update password
        user.set_password(new_password)
        user.save()
        
        # Mark token as used
        reset_token.is_used = True
        reset_token.save()
        
        return Response({'message': 'Password has been reset successfully'})


# ===== DEVICE VIEWS =====
class UserDeviceView(generics.ListCreateAPIView):
    """View for managing user devices"""
    serializer_class = UserDeviceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ===== VIEWSETS =====
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user instances.
    ReadOnlyModelViewSet provides 'list' and 'retrieve' actions.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return users based on the requesting user's role"""
        user = self.request.user
        
        if user.role == 'admin':
            # Admins can see all users
            return User.objects.all()
        elif user.role == 'lecturer':
            # Lecturers can see students and other lecturers
            return User.objects.filter(role__in=['student', 'lecturer'])
        else:
            # Students can only see themselves
            return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
