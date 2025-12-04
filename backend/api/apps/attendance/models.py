"""
Models for the attendance app.
"""
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from core.models import TimestampedModel
from core.constants import ATTENDANCE_STATUSES, QR_CODE_EXPIRY_SECONDS
from utils.security import generate_secure_token
import uuid


class QRCode(TimestampedModel):
    """
    Model for storing QR codes for attendance sessions.
    """
    session = models.OneToOneField(
        'courses.ClassSession',
        on_delete=models.CASCADE,
        related_name='qr_code'
    )
    code = models.CharField(max_length=100, unique=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"QR Code for {self.session} - Expires: {self.expires_at}"

    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_secure_token(32)
        super().save(*args, **kwargs)


class Attendance(TimestampedModel):
    """
    Model for storing attendance records.
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendances',
        limit_choices_to={'role': 'student'}
    )
    session = models.ForeignKey(
        'courses.ClassSession',
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_STATUSES,
        default="present"
    )
    marked_at = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    device_fingerprint = models.CharField(max_length=128, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    qr_code_used = models.ForeignKey(
        QRCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendances'
    )

    class Meta:
        ordering = ['-marked_at']
        unique_together = ['student', 'session']

    def __str__(self):
        return f"{self.student} - {self.session} - {self.status}"

    def clean(self):
        # Validate coordinates if provided
        if (self.latitude is not None and self.longitude is None) or \
           (self.latitude is None and self.longitude is not None):
            raise ValidationError("Both latitude and longitude must be provided together.")

        # Validate coordinate ranges
        if self.latitude is not None and not (-90 <= self.latitude <= 90):
            raise ValidationError("Latitude must be between -90 and 90.")
        if self.longitude is not None and not (-180 <= self.longitude <= 180):
            raise ValidationError("Longitude must be between -180 and 180.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class AttendanceLog(TimestampedModel):
    """
    Model for logging attendance-related activities for audit purposes.
    """
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    action = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action} - {self.attendance} - {self.created_at}"


class AntiCheatFlag(TimestampedModel):
    """
    Model for flagging suspicious attendance activities.
    """
    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE,
        related_name='cheat_flags'
    )
    flag_type = models.CharField(max_length=50)
    severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        default='low'
    )
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_flags'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.flag_type} - {self.attendance} - {self.severity}"


class BulkAttendanceImport(TimestampedModel):
    """
    Model for tracking bulk attendance imports.
    """
    session = models.ForeignKey(
        'courses.ClassSession',
        on_delete=models.CASCADE,
        related_name='bulk_imports'
    )
    imported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bulk_imports'
    )
    file_name = models.CharField(max_length=255)
    total_records = models.PositiveIntegerField(default=0)
    successful_imports = models.PositiveIntegerField(default=0)
    failed_imports = models.PositiveIntegerField(default=0)
    errors = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Bulk import for {self.session} by {self.imported_by}"


