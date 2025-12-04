"""
URL configuration for the notifications app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotificationViewSet, PushNotificationTokenViewSet,
    NotificationPreferenceViewSet, SendNotificationView, BulkNotificationView
)

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'push-tokens', PushNotificationTokenViewSet, basename='push-token')
router.register(r'preferences', NotificationPreferenceViewSet, basename='notification-preference')

urlpatterns = [
    path('', include(router.urls)),
    path('send/', SendNotificationView.as_view(), name='send-notification'),
    path('bulk-send/', BulkNotificationView.as_view(), name='bulk-notification'),
]
