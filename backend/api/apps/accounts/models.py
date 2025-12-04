"""
Custom User model for SAMS.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimestampedModel


class User(AbstractUser, TimestampedModel):
    """Custom User model for SAMS."""
    
    # Add custom fields here
    student_id = models.CharField(
        _('Student ID'),
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        _('Phone Number'),
        max_length=20,
        blank=True,
        null=True
    )
    
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="accounts_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="accounts_user_set",
        related_query_name="user",
    )
    
    class Meta:
        app_label = 'accounts'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return self.username


class UserDevice(TimestampedModel):
    """User devices for multi-device support."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='devices'
    )
    device_id = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(
        max_length=50,
        choices=(
            ('mobile', 'Mobile'),
            ('tablet', 'Tablet'),
            ('desktop', 'Desktop'),
        )
    )
    platform = models.CharField(max_length=50)
    fcm_token = models.TextField(blank=True, null=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'accounts'
        unique_together = ['user', 'device_id']
    
    def __str__(self):
        return f"{self.user.username} - {self.device_type}"


class PasswordResetToken(TimestampedModel):
    """Password reset tokens."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens'
    )
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'accounts'
    
    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    def is_valid(self):
        from django.utils.timezone import now
        return not self.is_used and now() < self.expires_at
