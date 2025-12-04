"""
Models for the notifications app.
"""
from django.db import models
from django.conf import settings
from core.models import TimestampedModel


class Notification(TimestampedModel):
    """System notifications for users."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=50,
        choices=(
            ('info', 'Information'),
            ('warning', 'Warning'),
            ('success', 'Success'),
            ('error', 'Error'),
        ),
        default='info'
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class PushNotificationToken(TimestampedModel):
    """FCM push notification tokens for mobile devices."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='push_tokens'
    )
    device_id = models.CharField(max_length=255, unique=True)
    fcm_token = models.TextField()
    platform = models.CharField(
        max_length=20,
        choices=(
            ('android', 'Android'),
            ('ios', 'iOS'),
            ('web', 'Web'),
        )
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'device_id']
    
    def __str__(self):
        return f"{self.user.username} - {self.platform}"


class NotificationLog(TimestampedModel):
    """Log of sent notifications."""
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    sent_via = models.CharField(
        max_length=50,
        choices=(
            ('push', 'Push Notification'),
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('in_app', 'In-App'),
        )
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('failed', 'Failed'),
            ('pending', 'Pending'),
        )
    )
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.notification.title} - {self.sent_via}"


class NotificationPreference(TimestampedModel):
    """User preferences for notifications."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    push_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    
    # Notification type preferences
    attendance_updates = models.BooleanField(default=True)
    course_updates = models.BooleanField(default=True)
    system_alerts = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Preferences - {self.user.username}"
