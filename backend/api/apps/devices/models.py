from django.db import models

class UserDevice(models.Model):
    """Model to store user devices for FCM push notifications"""
    # Try different variations if 'accounts.User' doesn't work
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=255, unique=True)
    fcm_token = models.TextField(blank=True, null=True)
    device_type = models.CharField(max_length=50, choices=[
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('web', 'Web')
    ], default='android')
    is_active = models.BooleanField(default=True)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Device'
        verbose_name_plural = 'User Devices'
        unique_together = ('user', 'device_id')
    
    def __str__(self):
        return f"{self.user_id} - {self.device_type}"
