"""
URL configuration for the devices app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeviceViewSet, DeviceFingerprintViewSet, DeviceLocationViewSet,
    DeviceSessionViewSet, DeviceAlertViewSet, DeviceAnalyticsViewSet,
    DevicePermissionViewSet, RegisterDeviceView, UpdateLocationView,
    ValidateFingerprintView, DeviceHealthView, DeviceSecurityCheckView
)

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'fingerprints', DeviceFingerprintViewSet, basename='device-fingerprint')
router.register(r'locations', DeviceLocationViewSet, basename='device-location')
router.register(r'sessions', DeviceSessionViewSet, basename='device-session')
router.register(r'alerts', DeviceAlertViewSet, basename='device-alert')
router.register(r'device-analytics', DeviceAnalyticsViewSet, basename='device-analytics')
router.register(r'permissions', DevicePermissionViewSet, basename='device-permission')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterDeviceView.as_view(), name='register-device'),
    path('location/update/', UpdateLocationView.as_view(), name='update-location'),
    path('fingerprint/validate/', ValidateFingerprintView.as_view(), name='validate-fingerprint'),
    path('health/<str:device_id>/', DeviceHealthView.as_view(), name='device-health'),
    path('security/check/', DeviceSecurityCheckView.as_view(), name='device-security-check'),
]
