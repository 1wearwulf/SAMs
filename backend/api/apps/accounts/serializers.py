"""
Serializers for the accounts app.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from api.apps.devices.models import UserDevice
from .models import User, PasswordResetToken
from core.constants import USER_ROLES, PASSWORD_RESET_TOKEN_EXPIRY_HOURS


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    password = serializers.CharField(write_only=True, required=False)
    full_name = serializers.CharField(read_only=True, source='get_full_name')

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'student_id', 'phone', 'profile_picture', 'is_email_verified',
            'date_joined', 'last_login', 'is_active', 'password'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'student_id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile updates.
    """
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'profile_picture'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'role', 'phone'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(_("Passwords don't match."))

        # Validate role
        if attrs.get('role') not in USER_ROLES.values():
            raise serializers.ValidationError(_("Invalid role specified."))

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    device_id = serializers.CharField(required=False)
    device_fingerprint = serializers.CharField(required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError(_("Invalid credentials."))
            if not user.is_active:
                raise serializers.ValidationError(_("User account is disabled."))
            attrs['user'] = user
        else:
            raise serializers.ValidationError(_("Must include username and password."))

        return attrs


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset request.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User with this email does not exist."))
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation.
    """
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(_("Passwords don't match."))

        try:
            reset_token = PasswordResetToken.objects.get(
                token=attrs['token'],
                is_used=False
            )
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError(_("Invalid or expired token."))

        if reset_token.is_expired:
            raise serializers.ValidationError(_("Token has expired."))

        attrs['reset_token'] = reset_token
        return attrs


class UserDeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for UserDevice model.
    """
    class Meta:
        model = UserDevice
        fields = [
            'id', 'device_id', 'device_type', 'device_name',
            'ip_address', 'is_active', 'last_used', 'created_at'
        ]
        read_only_fields = ['id', 'last_used', 'created_at']


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password.
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError(_("Old password is incorrect."))

        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(_("New passwords don't match."))

        return attrs
