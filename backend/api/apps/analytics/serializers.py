"""
Serializers for the analytics app.
"""
from rest_framework import serializers
from .models import (
    AttendanceAnalytics, StudentAnalytics, LecturerAnalytics,
    SystemAnalytics
)


class AttendanceAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for AttendanceAnalytics model.
    """
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    session_title = serializers.CharField(source='session.title', read_only=True)

    class Meta:
        model = AttendanceAnalytics
        fields = [
            'id', 'course', 'course_name', 'course_code', 'session',
            'session_title', 'date', 'total_students', 'present_count',
            'absent_count', 'late_count', 'attendance_rate',
            'average_checkin_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentAnalytics model.
    """
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)

    class Meta:
        model = StudentAnalytics
        fields = [
            'id', 'student', 'student_name', 'student_username', 'course',
            'course_name', 'course_code', 'total_sessions', 'present_count',
            'absent_count', 'late_count', 'excused_count', 'attendance_rate',
            'consecutive_absences', 'last_attendance_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LecturerAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for LecturerAnalytics model.
    """
    lecturer_name = serializers.CharField(source='lecturer.get_full_name', read_only=True)
    lecturer_username = serializers.CharField(source='lecturer.username', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)

    class Meta:
        model = LecturerAnalytics
        fields = [
            'id', 'lecturer', 'lecturer_name', 'lecturer_username', 'course',
            'course_name', 'course_code', 'total_sessions', 'completed_sessions',
            'average_attendance_rate', 'total_students', 'active_students',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SystemAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for SystemAnalytics model.
    """
    class Meta:
        model = SystemAnalytics
        fields = [
            'id', 'date', 'total_users', 'active_users', 'total_courses',
            'active_courses', 'total_sessions', 'completed_sessions',
            'total_attendances', 'average_attendance_rate', 'total_notifications',
            'system_uptime', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardSerializer(serializers.Serializer):
    """
    Serializer for dashboard data.
    """
    total_courses = serializers.IntegerField()
    average_attendance_rate = serializers.FloatField()
    courses_at_risk = serializers.IntegerField(required=False)
    recent_performance = serializers.ListField(required=False)
    total_sessions = serializers.IntegerField(required=False)
    average_class_attendance = serializers.FloatField(required=False)
    total_students = serializers.IntegerField(required=False)
    course_performance = serializers.ListField(required=False)
    active_users = serializers.IntegerField(required=False)
    user_growth = serializers.IntegerField(required=False)
    recent_trends = serializers.ListField(required=False)


class AttendanceReportSerializer(serializers.Serializer):
    """
    Serializer for attendance reports.
    """
    course_name = serializers.CharField()
    course_code = serializers.CharField()
    period = serializers.CharField()
    total_sessions = serializers.IntegerField()
    sessions = serializers.ListField()


class CourseAnalyticsSerializer(serializers.Serializer):
    """
    Serializer for course analytics data.
    """
    course_info = serializers.DictField()
    attendance_summary = serializers.DictField()
    student_performance = serializers.ListField()
    session_details = serializers.ListField()


class StudentPerformanceSerializer(serializers.Serializer):
    """
    Serializer for student performance data.
    """
    student_info = serializers.DictField()
    overall_performance = serializers.DictField()
    course_details = serializers.ListField()
