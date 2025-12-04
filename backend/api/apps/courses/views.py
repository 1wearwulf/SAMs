"""
Views for the courses app.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Course, ClassSession, CourseMaterial, CourseAnnouncement, EnrollmentRequest
from .serializers import (
    CourseSerializer, CourseDetailSerializer, ClassSessionSerializer,
    ClassSessionDetailSerializer, CourseMaterialSerializer,
    CourseAnnouncementSerializer, EnrollmentRequestSerializer,
    CreateEnrollmentRequestSerializer, EnrollmentActionSerializer
)
from api.permissions import IsLecturerOrAdmin, IsStudentOrLecturerOrAdmin


class CourseViewSet(ModelViewSet):
    """
    ViewSet for Course model.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrLecturerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Course.objects.all()
        elif user.role == 'lecturer':
            return Course.objects.filter(lecturer=user)
        else:
            # Students see courses they're enrolled in
            return Course.objects.filter(enrolled_students=user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(lecturer=self.request.user)

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """
        Enroll in a course (for students).
        """
        course = self.get_object()
        user = request.user

        if user.role != 'student':
            return Response(
                {'error': 'Only students can enroll in courses'},
                status=status.HTTP_403_FORBIDDEN
            )

        if course.enrolled_students.filter(id=user.id).exists():
            return Response(
                {'error': 'Already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if course.available_slots <= 0:
            return Response(
                {'error': 'No available slots in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course.enrolled_students.add(user)
        return Response({'message': 'Successfully enrolled in course'})

    @action(detail=True, methods=['post'])
    def unenroll(self, request, pk=None):
        """
        Unenroll from a course (for students).
        """
        course = self.get_object()
        user = request.user

        if user.role != 'student':
            return Response(
                {'error': 'Only students can unenroll from courses'},
                status=status.HTTP_403_FORBIDDEN
            )

        if not course.enrolled_students.filter(id=user.id).exists():
            return Response(
                {'error': 'Not enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course.enrolled_students.remove(user)
        return Response({'message': 'Successfully unenrolled from course'})

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """
        Get enrolled students for a course.
        """
        course = self.get_object()
        user = request.user

        # Only lecturer or admin can view enrolled students
        if user.role not in ['lecturer', 'admin'] and course.lecturer != user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        students = course.enrolled_students.all()
        data = [{
            'id': student.id,
            'name': student.get_full_name(),
            'username': student.username,
            'email': student.email
        } for student in students]

        return Response(data)


class ClassSessionViewSet(ModelViewSet):
    """
    ViewSet for ClassSession model.
    """
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrLecturerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return ClassSession.objects.all()
        elif user.role == 'lecturer':
            return ClassSession.objects.filter(course__lecturer=user)
        else:
            # Students see sessions for courses they're enrolled in
            return ClassSession.objects.filter(course__enrolled_students=user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClassSessionDetailSerializer
        return ClassSessionSerializer

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        # Check if user can create sessions for this course
        if self.request.user.role != 'admin' and course.lecturer != self.request.user:
            raise permissions.PermissionDenied("Can only create sessions for your own courses")
        serializer.save()

    @action(detail=True, methods=['post'])
    def start_session(self, request, pk=None):
        """
        Mark session as active.
        """
        session = self.get_object()
        user = request.user

        if user.role != 'admin' and session.course.lecturer != user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        session.status = 'active'
        session.save()

        return Response({'message': 'Session started successfully'})

    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """
        Mark session as completed.
        """
        session = self.get_object()
        user = request.user

        if user.role != 'admin' and session.course.lecturer != user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        session.status = 'completed'
        session.save()

        return Response({'message': 'Session ended successfully'})

    @action(detail=True, methods=['get'])
    def attendance_summary(self, request, pk=None):
        """
        Get attendance summary for a session.
        """
        session = self.get_object()
        user = request.user

        if user.role not in ['lecturer', 'admin'] and session.course.lecturer != user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        attendances = session.attendances.all()
        total_enrolled = session.course.enrolled_students.count()

        present = attendances.filter(status='present').count()
        absent = total_enrolled - attendances.count()
        late = attendances.filter(status='late').count()

        return Response({
            'total_enrolled': total_enrolled,
            'present': present,
            'absent': absent,
            'late': late,
            'attendance_rate': (present + late) / total_enrolled * 100 if total_enrolled > 0 else 0
        })


class CourseMaterialViewSet(ModelViewSet):
    """
    ViewSet for CourseMaterial model.
    """
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrLecturerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return CourseMaterial.objects.all()
        elif user.role == 'lecturer':
            return CourseMaterial.objects.filter(course__lecturer=user)
        else:
            # Students see materials for courses they're enrolled in
            return CourseMaterial.objects.filter(course__enrolled_students=user)

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        # Check if user can add materials to this course
        if self.request.user.role != 'admin' and course.lecturer != self.request.user:
            raise permissions.PermissionDenied("Can only add materials to your own courses")
        serializer.save()


class CourseAnnouncementViewSet(ModelViewSet):
    """
    ViewSet for CourseAnnouncement model.
    """
    queryset = CourseAnnouncement.objects.all()
    serializer_class = CourseAnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrLecturerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return CourseAnnouncement.objects.all()
        elif user.role == 'lecturer':
            return CourseAnnouncement.objects.filter(course__lecturer=user)
        else:
            # Students see announcements for courses they're enrolled in
            return CourseAnnouncement.objects.filter(course__enrolled_students=user)

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        # Check if user can create announcements for this course
        if self.request.user.role != 'admin' and course.lecturer != self.request.user:
            raise permissions.PermissionDenied("Can only create announcements for your own courses")
        serializer.save(author=self.request.user)


class EnrollmentRequestViewSet(ModelViewSet):
    """
    ViewSet for EnrollmentRequest model.
    """
    queryset = EnrollmentRequest.objects.all()
    serializer_class = EnrollmentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return EnrollmentRequest.objects.all()
        elif user.role == 'lecturer':
            return EnrollmentRequest.objects.filter(course__lecturer=user)
        else:
            # Students see only their own requests
            return EnrollmentRequest.objects.filter(student=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateEnrollmentRequestSerializer
        return EnrollmentRequestSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """
        Review an enrollment request (approve/reject).
        """
        enrollment_request = self.get_object()
        user = request.user

        # Check permissions
        if user.role != 'admin' and enrollment_request.course.lecturer != user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EnrollmentActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data['action']
        response_message = serializer.validated_data.get('response_message', '')

        if action == 'approve':
            enrollment_request.approve(user)
            message = 'Enrollment request approved'
        else:
            enrollment_request.reject(user, response_message)
            message = 'Enrollment request rejected'

        return Response({'message': message})


class StudentCoursesView(generics.ListAPIView):
    """
    View for getting courses a student is enrolled in.
    """
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'student':
            return Course.objects.none()
        return Course.objects.filter(enrolled_students=user)


class LecturerCoursesView(generics.ListAPIView):
    """
    View for getting courses taught by a lecturer.
    """
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'lecturer':
            return Course.objects.none()
        return Course.objects.filter(lecturer=user)


class CourseSearchView(generics.ListAPIView):
    """
    View for searching courses.
    """
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Course.objects.filter(status='active')
        search_query = self.request.query_params.get('q', '')

        if search_query:
            queryset = queryset.filter(
                Q(code__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset


class UpcomingSessionsView(generics.ListAPIView):
    """
    View for getting upcoming class sessions.
    """
    serializer_class = ClassSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()

        if user.role == 'admin':
            return ClassSession.objects.filter(
                scheduled_date__gte=today,
                status__in=['scheduled', 'active']
            ).order_by('scheduled_date', 'start_time')[:20]

        elif user.role == 'lecturer':
            return ClassSession.objects.filter(
                course__lecturer=user,
                scheduled_date__gte=today,
                status__in=['scheduled', 'active']
            ).order_by('scheduled_date', 'start_time')[:20]

        else:
            # Students
            return ClassSession.objects.filter(
                course__enrolled_students=user,
                scheduled_date__gte=today,
                status__in=['scheduled', 'active']
            ).order_by('scheduled_date', 'start_time')[:20]
