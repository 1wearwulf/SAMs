"""
Serializers for the devices app.
"""
from rest_framework import serializers
from .models import (
    Device, DeviceFingerprint, DeviceLocation, DeviceSession,
    DeviceAlert, DeviceAnalytics, DevicePermission
)


class DeviceSerializer(serializers.ModelSerializer):
    """
    Serializer for Device model.
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    health_score = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = [
            'id', 'user', 'user_name', 'device_id', 'device_type', 'device_name',
            'os', 'os_version', 'app_version', 'model', 'manufacturer',
            'screen_resolution', 'ip_address', 'mac_address', 'imei',
            'is_trusted', 'status', 'last_seen', 'registered_at', 'health_score'
        ]
        read_only_fields = ['id', 'registered_at', 'health_score']

    def get_health_score(self, obj):
        from .services import DeviceService
        return DeviceService.get_device_health_score(obj.device_id)


class DeviceFingerprintSerializer(serializers.ModelSerializer):
    """
    Serializer for DeviceFingerprint model.
    """
    device_name = serializers.CharField(source='device.device_name', read_only=True)

    class Meta:
        model = DeviceFingerprint
        fields = [
            'id', 'device', 'device_name', 'fingerprint_hash',
            'fingerprint_data', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DeviceLocationSerializer(serializers.ModelSerializer):
    """
    Serializer for DeviceLocation model.
    """
    device_name = serializers.CharField(source='device.device_name', read_only=True)

    class Meta:
        model = DeviceLocation
        fields = [
            'id', 'device', 'device_name', 'latitude', 'longitude',
            'accuracy', 'altitude', 'speed', 'heading', 'timestamp',
            'source', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DeviceSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for DeviceSession model.
    """
    device_name = serializers.CharField(source='device.device_name', read_only=True)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = DeviceSession
        fields = [
            'id', 'device', 'device_name', 'session_id', 'ip_address',
            'user_agent', 'started_at', 'ended_at', 'is_active',
            'duration', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_duration(self, obj):
        if obj.ended_at and obj.started_at:
            duration = obj.ended_at - obj.started_at
            return duration.total_seconds()
        return None


class DeviceAlertSerializer(serializers.ModelSerializer):
    """
    Serializer for DeviceAlert model.
    """
    device_name = serializers.CharField(source='device.device_name', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.get_full_name', read_only=True)

    class Meta:
        model = DeviceAlert
        fields = [
            'id', 'device', 'device_name', 'alert_type', 'severity',
            'title', 'message', 'data', 'is_resolved', 'resolved_at',
            'resolved_by', 'resolved_by_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DeviceAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for device analytics data.
    """
    device_info = serializers.DictField()
    analytics = serializers.DictField()
    recent_locations = serializers.ListField()
    alerts_count = serializers.IntegerField()


class DeviceHealthSerializer(serializers.Serializer):
    """
    Serializer for device health data.
    """
    score = serializers.IntegerField()
    status = serializers.CharField()
    issues = serializers.ListField()


class DevicePermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for DevicePermission model.
    """
    device_name = serializers.CharField(source='device.device_name', read_only=True)

    class Meta:
        model = DevicePermission
        fields = [
            'id', 'device', 'device_name', 'location_tracking',
            'push_notifications', 'background_sync', 'data_collection',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RegisterDeviceSerializer(serializers.Serializer):
    """
    Serializer for device registration.
    """
    device_id = serializers.CharField(max_length=255)
    device_type = serializers.ChoiceField(choices=[
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('desktop', 'Desktop'),
        ('web', 'Web'),
    ])
    device_name = serializers.CharField(max_length=255, required=False)
    os = serializers.CharField(max_length=50, required=False)
    os_version = serializers.CharField(max_length=50, required=False)
    app_version = serializers.CharField(max_length=20, required=False)
    model = serializers.CharField(max_length=100, required=False)
    manufacturer = serializers.CharField(max_length=100, required=False)
    screen_resolution = serializers.CharField(max_length=20, required=False)
    mac_address = serializers.CharField(max_length=17, required=False)
    imei = serializers.CharField(max_length=15, required=False)


class UpdateLocationSerializer(serializers.Serializer):
    """
    Serializer for location updates.
    """
    device_id = serializers.CharField(max_length=255)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    accuracy = serializers.FloatField(required=False)
    altitude = serializers.FloatField(required=False)
    speed = serializers.FloatField(required=False)
    heading = serializers.FloatField(required=False)
    timestamp = serializers.DateTimeField(required=False)
    source = serializers.CharField(max_length=20, required=False)


class DeviceFingerprintValidationSerializer(serializers.Serializer):
    """
    Serializer for fingerprint validation.
    """
    device_id = serializers.CharField(max_length=255)
    fingerprint = serializers.DictField()


class DeviceSecurityCheckSerializer(serializers.Serializer):
    """
    Serializer for security checks.
    """
    device_id = serializers.CharField(max_length=255)
    security_data = serializers.DictField()
