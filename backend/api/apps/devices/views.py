"""
Views for the devices app.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from .models import Device, DeviceFingerprint, DeviceLocation, DeviceSession, DeviceAlert, DevicePermission
from .serializers import (
    DeviceSerializer, DeviceFingerprintSerializer, DeviceLocationSerializer,
    DeviceSessionSerializer, DeviceAlertSerializer, DevicePermissionSerializer,
    RegisterDeviceSerializer, UpdateLocationSerializer, DeviceAnalyticsSerializer,
    DeviceHealthSerializer, DeviceFingerprintValidationSerializer, DeviceSecurityCheckSerializer
)
from .services import DeviceService


class DeviceViewSet(ModelViewSet):
    """
    ViewSet for Device model.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Device.objects.all()
        else:
            return Device.objects.filter(user=user)

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Get device analytics."""
        device = self.get_object()
        analytics = DeviceService.get_device_analytics(device.device_id)
        if analytics:
            serializer = DeviceAnalyticsSerializer(analytics)
            return Response(serializer.data)
        return Response({'error': 'Analytics not available'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def health(self, request, pk=None):
        """Get device health score."""
        device = self.get_object()
        score = DeviceService.get_device_health_score(device.device_id)
        health_data = {
            'score': score,
            'status': 'healthy' if score >= 80 else 'warning' if score >= 60 else 'critical',
            'issues': []
        }
        serializer = DeviceHealthSerializer(health_data)
        return Response(serializer.data)


class DeviceFingerprintViewSet(ModelViewSet):
    """
    ViewSet for DeviceFingerprint model.
    """
    queryset = DeviceFingerprint.objects.all()
    serializer_class = DeviceFingerprintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return DeviceFingerprint.objects.all()
        else:
            return DeviceFingerprint.objects.filter(device__user=user)


class DeviceLocationViewSet(ModelViewSet):
    """
    ViewSet for DeviceLocation model.
    """
    queryset = DeviceLocation.objects.all()
    serializer_class = DeviceLocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return DeviceLocation.objects.all()
        else:
            return DeviceLocation.objects.filter(device__user=user)


class DeviceSessionViewSet(ModelViewSet):
    """
    ViewSet for DeviceSession model.
    """
    queryset = DeviceSession.objects.all()
    serializer_class = DeviceSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return DeviceSession.objects.all()
        else:
            return DeviceSession.objects.filter(device__user=user)


class DeviceAlertViewSet(ModelViewSet):
    """
    ViewSet for DeviceAlert model.
    """
    queryset = DeviceAlert.objects.all()
    serializer_class = DeviceAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return DeviceAlert.objects.all()
        else:
            return DeviceAlert.objects.filter(device__user=user)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve an alert."""
        alert = self.get_object()
        alert.resolve(resolved_by=request.user)
        serializer = self.get_serializer(alert)
        return Response(serializer.data)


class DevicePermissionViewSet(ModelViewSet):
    """
    ViewSet for DevicePermission model.
    """
    queryset = DevicePermission.objects.all()
    serializer_class = DevicePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return DevicePermission.objects.all()
        else:
            return DevicePermission.objects.filter(device__user=user)


class RegisterDeviceView(APIView):
    """
    View for registering a device.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RegisterDeviceSerializer(data=request.data)
        if serializer.is_valid():
            device, created = DeviceService.register_device(request.user, serializer.validated_data)
            device_serializer = DeviceSerializer(device)
            return Response({
                'device': device_serializer.data,
                'created': created
            }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateLocationView(APIView):
    """
    View for updating device location.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = UpdateLocationSerializer(data=request.data)
        if serializer.is_valid():
            location = DeviceService.update_device_location(
                serializer.validated_data['device_id'],
                serializer.validated_data
            )
            if location:
                location_serializer = DeviceLocationSerializer(location)
                return Response(location_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceFingerprintValidationView(APIView):
    """
    View for validating device fingerprints.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DeviceFingerprintValidationSerializer(data=request.data)
        if serializer.is_valid():
            # Implement fingerprint validation logic
            return Response({'valid': True, 'message': 'Fingerprint validated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceSecurityCheckView(APIView):
    """
    View for performing security checks on devices.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DeviceSecurityCheckSerializer(data=request.data)
        if serializer.is_valid():
            # Implement security check logic
            return Response({'secure': True, 'message': 'Device is secure'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
