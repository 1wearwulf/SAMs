"""
Serializers for the notifications app.
"""
from rest_framework import serializers
from .models import Notification, PushNotificationToken, NotificationLog, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    """
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    recipient_count = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'title', 'message', 'notification_type', 'sender', 'sender_name',
            'recipients', 'course', 'is_sent', 'sent_at', 'recipient_count',
            'is_read', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_sent', 'sent_at', 'created_at', 'updated_at']

    def get_recipient_count(self, obj):
        return obj.recipients.count()

    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return NotificationLog.objects.filter(
                notification=obj,
                recipient=request.user,
                status='read'
            ).exists()
        return False


class NotificationDetailSerializer(NotificationSerializer):
    """
    Detailed serializer for Notification with logs.
    """
    delivery_logs = serializers.SerializerMethodField()

    class Meta(NotificationSerializer.Meta):
        fields = NotificationSerializer.Meta.fields + ['delivery_logs']

    def get_delivery_logs(self, obj):
        logs = obj.logs.all()
        return NotificationLogSerializer(logs, many=True).data


class SendNotificationSerializer(serializers.Serializer):
    """
    Serializer for sending notifications.
    """
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    notification_type = serializers.ChoiceField(choices=[
        ('announcement', 'Announcement'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
        ('system', 'System'),
    ])
    recipient_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )
    course_id = serializers.IntegerField(required=False)

    def validate_recipient_ids(self, value):
        if len(value) > 1000:  # Limit bulk notifications
            raise serializers.ValidationError("Cannot send to more than 1000 recipients at once.")
        return value


class BulkNotificationSerializer(serializers.Serializer):
    """
    Serializer for sending bulk notifications to course students.
    """
    course_id = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    notification_type = serializers.ChoiceField(choices=[
        ('announcement', 'Announcement'),
        ('reminder', 'Reminder'),
        ('alert', 'Alert'),
    ])


class PushNotificationTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for PushNotificationToken model.
    """
    class Meta:
        model = PushNotificationToken
        fields = [
            'id', 'token', 'device_type', 'device_name',
            'is_active', 'last_used', 'created_at'
        ]
        read_only_fields = ['id', 'last_used', 'created_at']


class NotificationLogSerializer(serializers.ModelSerializer):
    """
    Serializer for NotificationLog model.
    """
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)

    class Meta:
        model = NotificationLog
        fields = [
            'id', 'notification', 'recipient', 'recipient_name',
            'delivery_method', 'status', 'sent_at', 'delivered_at',
            'read_at', 'error_message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for NotificationPreference model.
    """
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'push_course_announcements', 'push_attendance_reminders',
            'push_system_notifications', 'email_course_announcements',
            'email_attendance_reminders', 'email_system_notifications',
            'sms_urgent_notifications', 'sms_attendance_alerts', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
