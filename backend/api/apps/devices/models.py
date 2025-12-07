"""
Models for the devices app.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


class Device(models.Model):
    """
    Model for storing device information.
    """
    DEVICE_TYPES = [
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('desktop', 'Desktop'),
        ('web', 'Web'),
    ]

    DEVICE_STATUSES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
        ('suspended', 'Suspended'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    device_name = models.CharField(max_length=255, blank=True)
    os = models.CharField(max_length=50, blank=True)
    os_version = models.CharField(max_length=50, blank=True)
    app_version = models.CharField(max_length=20, blank=True)
    model = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    screen_resolution = models.CharField(max_length=20, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    mac_address = models.CharField(max_length=17, blank=True)
    imei = models.CharField(max_length=15, blank=True)
    is_trusted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=DEVICE_STATUSES, default='active')
    last_seen = models.DateTimeField(auto_now=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_seen']
        unique_together = ['user', 'device_id']

    def __str__(self):
        return f"{self.user.username} - {self.device_name or self.device_id}"


class DeviceFingerprint(models.Model):
    """
    Model for storing device fingerprints.
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='fingerprints')
    fingerprint_hash = models.CharField(max_length=128, unique=True)
    fingerprint_data = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.device.device_name} - {self.fingerprint_hash[:16]}"


class DeviceLocation(models.Model):
    """
    Model for storing device location data.
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    accuracy = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    heading = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=20, default='gps')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.device.device_name} - {self.latitude},{self.longitude}"


class DeviceSession(models.Model):
    """
    Model for storing device sessions.
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='sessions')
    session_id = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.device.device_name} - {self.session_id}"

    def end_session(self):
        """End the session."""
        self.ended_at = timezone.now()
        self.is_active = False
        self.save()


class DeviceAlert(models.Model):
    """
    Model for storing device alerts.
    """
    ALERT_TYPES = [
        ('security', 'Security'),
        ('location', 'Location'),
        ('performance', 'Performance'),
        ('connectivity', 'Connectivity'),
        ('battery', 'Battery'),
    ]

    SEVERITIES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITIES, default='medium')
    title = models.CharField(max_length=255)
    message = models.TextField()
    data = models.JSONField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.device.device_name} - {self.title}"

    def resolve(self, resolved_by=None):
        """Resolve the alert."""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        if resolved_by:
            self.resolved_by = resolved_by
        self.save()


class DeviceAnalytics(models.Model):
    """
    Model for storing device analytics data.
    """
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='analytics')
    total_sessions = models.PositiveIntegerField(default=0)
    total_locations = models.PositiveIntegerField(default=0)
    total_alerts = models.PositiveIntegerField(default=0)
    average_session_duration = models.FloatField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.device_name} Analytics"


class DevicePermission(models.Model):
    """
    Model for storing device permissions.
    """
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='permissions')
    location_tracking = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    background_sync = models.BooleanField(default=True)
    data_collection = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device.device_name} Permissions"


class UserDevice(models.Model):
    """Model to store user devices for FCM push notifications"""
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='user_devices')
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
