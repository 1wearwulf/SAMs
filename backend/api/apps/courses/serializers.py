"""
Serializers for the courses app.
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Course, ClassSession, CourseMaterial, CourseAnnouncement, EnrollmentRequest


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """
    lecturer_name = serializers.CharField(source='lecturer.get_full_name', read_only=True)
    enrolled_count = serializers.ReadOnlyField()
    available_slots = serializers.ReadOnlyField()
    total_sessions = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'description', 'lecturer', 'lecturer_name',
            'semester', 'academic_year', 'status', 'max_students', 'enrolled_count',
            'available_slots', 'total_sessions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'enrolled_count', 'available_slots']

    def get_total_sessions(self, obj):
        return obj.sessions.count()


class CourseDetailSerializer(CourseSerializer):
    """
    Detailed serializer for Course with related data.
    """
    enrolled_students = serializers.SerializerMethodField()
    recent_sessions = serializers.SerializerMethodField()
    recent_announcements = serializers.SerializerMethodField()

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + [
            'enrolled_students', 'recent_sessions', 'recent_announcements'
        ]

    def get_enrolled_students(self, obj):
        students = obj.enrolled_students.all()[:10]  # Limit to 10 for performance
        return [{
            'id': student.id,
            'name': student.get_full_name(),
            'username': student.username
        } for student in students]

    def get_recent_sessions(self, obj):
        sessions = obj.sessions.filter(scheduled_date__gte=timezone.now().date())[:5]
        return ClassSessionSerializer(sessions, many=True).data

    def get_recent_announcements(self, obj):
        announcements = obj.announcements.all()[:3]
        return CourseAnnouncementSerializer(announcements, many=True).data


class ClassSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for ClassSession model.
    """
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    duration_hours = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    attendance_count = serializers.ReadOnlyField()
    attendance_rate = serializers.ReadOnlyField()

    class Meta:
        model = ClassSession
        fields = [
            'id', 'course', 'course_name', 'course_code', 'title', 'description',
            'scheduled_date', 'start_time', 'end_time', 'location', 'latitude',
            'longitude', 'geofence_radius', 'status', 'is_mandatory',
            'duration_hours', 'is_active', 'attendance_count', 'attendance_rate',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'duration_hours', 'is_active',
                          'attendance_count', 'attendance_rate']


class ClassSessionDetailSerializer(ClassSessionSerializer):
    """
    Detailed serializer for ClassSession with attendance data.
    """
    attendances = serializers.SerializerMethodField()

    class Meta(ClassSessionSerializer.Meta):
        fields = ClassSessionSerializer.Meta.fields + ['attendances']

    def get_attendances(self, obj):
        attendances = obj.attendances.all().select_related('student')
        return [{
            'id': attendance.id,
            'student_name': attendance.student.get_full_name(),
            'status': attendance.status,
            'marked_at': attendance.marked_at,
            'latitude': attendance.latitude,
            'longitude': attendance.longitude
        } for attendance in attendances]


class CourseMaterialSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseMaterial model.
    """
    uploaded_by = serializers.CharField(source='course.lecturer.get_full_name', read_only=True)
    download_url = serializers.ReadOnlyField()

    class Meta:
        model = CourseMaterial
        fields = [
            'id', 'course', 'title', 'description', 'file', 'file_url',
            'material_type', 'is_required', 'order', 'download_url',
            'uploaded_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'download_url', 'uploaded_by']


class CourseAnnouncementSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseAnnouncement model.
    """
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)

    class Meta:
        model = CourseAnnouncement
        fields = [
            'id', 'course', 'title', 'content', 'author', 'author_name',
            'is_pinned', 'is_urgent', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author', 'author_name']


class EnrollmentRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for EnrollmentRequest model.
    """
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', read_only=True)

    class Meta:
        model = EnrollmentRequest
        fields = [
            'id', 'student', 'student_name', 'course', 'course_name', 'course_code',
            'status', 'request_message', 'response_message', 'reviewed_by',
            'reviewed_by_name', 'reviewed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'reviewed_by',
                          'reviewed_by_name', 'reviewed_at']


class CreateEnrollmentRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for creating enrollment requests.
    """
    class Meta:
        model = EnrollmentRequest
        fields = ['course', 'request_message']

    def validate_course(self, value):
        user = self.context['request'].user

        # Check if user is already enrolled
        if value.enrolled_students.filter(id=user.id).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")

        # Check if there's already a pending request
        if EnrollmentRequest.objects.filter(
            student=user,
            course=value,
            status='pending'
        ).exists():
            raise serializers.ValidationError("You already have a pending enrollment request for this course.")

        # Check if course has available slots
        if value.available_slots <= 0:
            raise serializers.ValidationError("This course has no available slots.")

        return value


class EnrollmentActionSerializer(serializers.Serializer):
    """
    Serializer for enrollment request actions (approve/reject).
    """
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    response_message = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs['action'] == 'reject' and not attrs.get('response_message', '').strip():
            raise serializers.ValidationError("Response message is required when rejecting a request.")
        return attrs
