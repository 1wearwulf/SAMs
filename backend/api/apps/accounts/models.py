"""
Custom User model for SAMS.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom User model for SAMS."""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name=_('Role')
    )
    student_id = models.CharField(
        _('Student ID'),
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )
    phone = models.CharField(
        _('Phone Number'),
        max_length=20,
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name=_('Profile Picture')
    )
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name=_('Email Verified')
    )
    
    # Fix related_name for groups and user_permissions to avoid clash
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
        app_label = 'accounts'  # EXPLICITLY SET APP LABEL
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'accounts_user'  # Optional: explicit table name
    
    def __str__(self):
        return self.username


class PasswordResetToken(models.Model):
    """Model for storing password reset tokens"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'accounts'
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        db_table = 'accounts_passwordresettoken'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['expires_at', 'is_used']),
        ]
    
    def __str__(self):
        return f"Password reset token for {self.user.email}"
    
    def is_valid(self):
        """Check if the token is still valid"""
        from django.utils import timezone
        return not self.is_used and self.expires_at > timezone.now()
    
    @property
    def is_expired(self):
        """Check if the token has expired"""
        from django.utils import timezone
        return self.expires_at <= timezone.now()
