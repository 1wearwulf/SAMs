"""
Serializers for the attendance app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.constants import ATTENDANCE_STATUSES, DEFAULT_GEOFENCE_RADIUS_METERS, GRACE_PERIOD_MINUTES
from .models import Attendance, QRCode, AttendanceLog, AntiCheatFlag, BulkAttendanceImport
from api.apps.courses.models import ClassSession
from api.apps.accounts.models import User

User = get_user_model()


class QRCodeSerializer(serializers.ModelSerializer):
    session_details = serializers.SerializerMethodField()
    
    class Meta:
        model = QRCode
        fields = ['id', 'session', 'session_details', 'code', 'expires_at', 'is_active', 'created_at']
        read_only_fields = ['code', 'created_at']
    
    def get_session_details(self, obj):
        return {
            'title': obj.session.title,
            'course': obj.session.course.name,
            'start_time': obj.session.start_time,
            'end_time': obj.session.end_time
        }


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    session_details = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'student_name', 'session', 'session_details',
            'course_name', 'status', 'marked_at', 'latitude', 'longitude',
            'device_fingerprint', 'ip_address', 'qr_code_used', 'created_at'
        ]
        read_only_fields = ['marked_at', 'created_at']
    
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    
    def get_session_details(self, obj):
        return {
            'title': obj.session.title,
            'start_time': obj.session.start_time,
            'end_time': obj.session.end_time
        }
    
    def get_course_name(self, obj):
        return obj.session.course.name if obj.session.course else None


class StudentAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for student's attendance records."""
    session_title = serializers.CharField(source='session.title', read_only=True)
    course_name = serializers.CharField(source='session.course.name', read_only=True)
    session_date = serializers.DateField(source='session.start_time', read_only=True)
    session_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'session', 'session_title', 'course_name', 'session_date',
            'session_time', 'status', 'marked_at', 'created_at'
        ]
        read_only_fields = ['marked_at', 'created_at']
    
    def get_session_time(self, obj):
        return {
            'start': obj.session.start_time,
            'end': obj.session.end_time
        }


class SessionAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for attendance records of a specific session."""
    student_name = serializers.SerializerMethodField()
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    student_email = serializers.EmailField(source='student.email', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'student_id', 'student_name', 'student_email',
            'status', 'marked_at', 'latitude', 'longitude', 'device_fingerprint',
            'ip_address', 'created_at'
        ]
        read_only_fields = ['marked_at', 'created_at']
    
    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"


class MarkAttendanceSerializer(serializers.ModelSerializer):
    qr_code = serializers.CharField(write_only=True, required=False)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    
    class Meta:
        model = Attendance
        fields = ['session', 'qr_code', 'latitude', 'longitude', 'device_fingerprint', 'ip_address']
    
    def validate(self, attrs):
        qr_code = attrs.pop('qr_code', None)
        if qr_code:
            try:
                qr_obj = QRCode.objects.get(code=qr_code, is_active=True)
                attrs['qr_code_used'] = qr_obj
                attrs['session'] = qr_obj.session
            except QRCode.DoesNotExist:
                raise serializers.ValidationError({"qr_code": "Invalid or expired QR code."})
        
        return attrs


# Alias for backward compatibility
AttendanceCreateSerializer = MarkAttendanceSerializer


class AttendanceLogSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AttendanceLog
        fields = ['id', 'attendance', 'action', 'details', 'performed_by', 'performed_by_name', 'ip_address', 'created_at']
        read_only_fields = ['created_at']
    
    def get_performed_by_name(self, obj):
        if obj.performed_by:
            return f"{obj.performed_by.first_name} {obj.performed_by.last_name}"
        return None


class AntiCheatFlagSerializer(serializers.ModelSerializer):
    resolved_by_name = serializers.SerializerMethodField()
    attendance_details = serializers.SerializerMethodField()
    
    class Meta:
        model = AntiCheatFlag
        fields = [
            'id', 'attendance', 'attendance_details', 'flag_type', 'severity',
            'description', 'is_resolved', 'resolved_at', 'resolved_by',
            'resolved_by_name', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_resolved_by_name(self, obj):
        if obj.resolved_by:
            return f"{obj.resolved_by.first_name} {obj.resolved_by.last_name}"
        return None
    
    def get_attendance_details(self, obj):
        return {
            'student': f"{obj.attendance.student.first_name} {obj.attendance.student.last_name}",
            'session': obj.attendance.session.title,
            'marked_at': obj.attendance.marked_at
        }


class BulkAttendanceImportSerializer(serializers.ModelSerializer):
    imported_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = BulkAttendanceImport
        fields = [
            'id', 'session', 'imported_by', 'imported_by_name', 'file_name',
            'total_records', 'successful_imports', 'failed_imports',
            'errors', 'is_completed', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_imported_by_name(self, obj):
        return f"{obj.imported_by.first_name} {obj.imported_by.last_name}"


class AttendanceStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    present = serializers.IntegerField()
    absent = serializers.IntegerField()
    late = serializers.IntegerField()
    excused = serializers.IntegerField()
    date = serializers.DateField(required=False)


class AttendanceExportSerializer(serializers.Serializer):
    session = serializers.PrimaryKeyRelatedField(queryset=ClassSession.objects.all())
    format = serializers.ChoiceField(choices=[('csv', 'CSV'), ('excel', 'Excel'), ('pdf', 'PDF')])
