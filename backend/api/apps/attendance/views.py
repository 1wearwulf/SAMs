"""
Views for the attendance app.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from .models import QRCode, Attendance, AttendanceLog, AntiCheatFlag
from .serializers import (
    QRCodeSerializer, AttendanceSerializer, MarkAttendanceSerializer,
    AttendanceLogSerializer, AntiCheatFlagSerializer, AttendanceStatsSerializer,
    StudentAttendanceSerializer, SessionAttendanceSerializer
)
from api.permissions import IsLecturerOrAdmin, IsStudentOrLecturerOrAdmin
from utils.geolocation import is_within_geofence, calculate_distance
from utils.device_fingerprint import validate_device_consistency
from core.constants import (
    ATTENDANCE_STATUSES, QR_CODE_EXPIRY_SECONDS,
    DEFAULT_GEOFENCE_RADIUS_METERS, GRACE_PERIOD_MINUTES
)
from core.exceptions import InvalidQRCodeException, LocationOutOfRangeException


class QRCodeViewSet(ModelViewSet):
    """
    ViewSet for QRCode model.
    """
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsLecturerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return QRCode.objects.all()
        else:
            # Lecturers can only see QR codes for their sessions
            return QRCode.objects.filter(
                session__course__lecturer=user
            )


class AttendanceViewSet(ModelViewSet):
    """
    ViewSet for Attendance model.
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrLecturerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Attendance.objects.all()
        elif user.role == 'lecturer':
            # Lecturers can see attendance for their courses
            return Attendance.objects.filter(
                session__course__lecturer=user
            )
        else:
            # Students can only see their own attendance
            return Attendance.objects.filter(student=user)


class GenerateQRView(APIView):
    """
    View for generating QR codes for class sessions.
    """
    permission_classes = [permissions.IsAuthenticated, IsLecturerOrAdmin]

    def post(self, request):
        session_id = request.data.get('session_id')
        if not session_id:
            return Response(
                {'error': 'session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the session
        from courses.models import ClassSession
        try:
            session = ClassSession.objects.get(id=session_id)
        except ClassSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user can generate QR for this session
        if request.user.role != 'admin' and session.course.lecturer != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if session is active
        now = timezone.now()
        if not (session.scheduled_date <= now.date() and
                session.start_time <= now.time() <= session.end_time):
            return Response(
                {'error': 'Session is not currently active'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create or update QR code
        qr_code, created = QRCode.objects.get_or_create(
            session=session,
            defaults={
                'expires_at': now + timedelta(seconds=QR_CODE_EXPIRY_SECONDS),
                'is_active': True
            }
        )

        if not created:
            qr_code.expires_at = now + timedelta(seconds=QR_CODE_EXPIRY_SECONDS)
            qr_code.is_active = True
            qr_code.save()

        serializer = QRCodeSerializer(qr_code)
        return Response(serializer.data)


class ValidateQRView(APIView):
    """
    View for validating QR codes.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response(
                {'error': 'QR code is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            qr_code = QRCode.objects.get(
                code=code,
                is_active=True
            )
        except QRCode.DoesNotExist:
            return Response(
                {'error': 'Invalid QR code'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if qr_code.is_expired:
            return Response(
                {'error': 'QR code has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'valid': True,
            'session_id': qr_code.session.id,
            'session_title': qr_code.session.title,
            'expires_at': qr_code.expires_at
        })


class MarkAttendanceView(APIView):
    """
    View for marking attendance using QR codes.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = MarkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        qr_code = serializer.validated_data['qr_code']
        user = request.user

        # Check if user is a student
        if user.role != 'student':
            return Response(
                {'error': 'Only students can mark attendance'},
                status=status.HTTP_403_FORBIDDEN
            )

        session = qr_code.session

        # Check if attendance already exists
        existing_attendance = Attendance.objects.filter(
            student=user,
            session=session
        ).first()

        if existing_attendance:
            return Response(
                {'error': 'Attendance already marked for this session'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate location if provided
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')

        if latitude and longitude:
            # Check if within geofence
            session_lat = session.latitude
            session_lng = session.longitude

            if session_lat and session_lng:
                if not is_within_geofence(
                    (latitude, longitude),
                    (session_lat, session_lng),
                    session.geofence_radius or DEFAULT_GEOFENCE_RADIUS_METERS
                ):
                    raise LocationOutOfRangeException()

        # Determine attendance status
        now = timezone.now()
        session_start = timezone.datetime.combine(
            session.scheduled_date,
            session.start_time
        ).replace(tzinfo=now.tzinfo)

        grace_period_end = session_start + timedelta(minutes=GRACE_PERIOD_MINUTES)

        if now <= grace_period_end:
            attendance_status = ATTENDANCE_STATUSES['PRESENT']
        elif now <= session_start + timedelta(minutes=GRACE_PERIOD_MINUTES * 2):
            attendance_status = ATTENDANCE_STATUSES['LATE']
        else:
            attendance_status = ATTENDANCE_STATUSES['ABSENT']

        # Validate device consistency
        device_fingerprint = serializer.validated_data.get('device_fingerprint')
        if device_fingerprint:
            device_check = validate_device_consistency(
                user.id,
                device_fingerprint,
                user.devices.filter(is_active=True).first().device_fingerprint if user.devices.exists() else None
            )

            if not device_check['is_valid']:
                # Create anti-cheat flag
                AntiCheatFlag.objects.create(
                    attendance=None,  # Will be set after attendance creation
                    flag_type='device_mismatch',
                    severity='medium',
                    description=f'Device fingerprint mismatch detected: {device_check["message"]}'
                )

        # Create attendance record
        with transaction.atomic():
            attendance = Attendance.objects.create(
                student=user,
                session=session,
                status=attendance_status,
                latitude=latitude,
                longitude=longitude,
                device_fingerprint=device_fingerprint,
                ip_address=request.META.get('REMOTE_ADDR'),
                qr_code_used=qr_code
            )

            # Create attendance log
            AttendanceLog.objects.create(
                attendance=attendance,
                action='marked',
                details=f'Attendance marked via QR code. Status: {attendance_status}',
                performed_by=user,
                ip_address=request.META.get('REMOTE_ADDR')
            )

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AttendanceStatsView(APIView):
    """
    View for getting attendance statistics.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        course_id = request.query_params.get('course_id')
        session_id = request.query_params.get('session_id')

        queryset = Attendance.objects.all()

        if user.role == 'student':
            queryset = queryset.filter(student=user)
        elif user.role == 'lecturer':
            queryset = queryset.filter(session__course__lecturer=user)

        if course_id:
            queryset = queryset.filter(session__course_id=course_id)
        if session_id:
            queryset = queryset.filter(session_id=session_id)

        total_attendances = queryset.count()
        present_count = queryset.filter(status=ATTENDANCE_STATUSES['PRESENT']).count()
        absent_count = queryset.filter(status=ATTENDANCE_STATUSES['ABSENT']).count()
        late_count = queryset.filter(status=ATTENDANCE_STATUSES['LATE']).count()

        attendance_rate = 0
        if total_attendances > 0:
            attendance_rate = ((present_count + late_count) / total_attendances) * 100

        data = {
            'total_attendances': total_attendances,
            'present_count': present_count,
            'absent_count': absent_count,
            'late_count': late_count,
            'attendance_rate': round(attendance_rate, 2)
        }

        serializer = AttendanceStatsSerializer(data)
        return Response(serializer.data)


class StudentAttendanceHistoryView(APIView):
    """
    View for getting student's attendance history.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != 'student':
            return Response(
                {'error': 'Only students can view their attendance history'},
                status=status.HTTP_403_FORBIDDEN
            )

        attendances = Attendance.objects.filter(student=user).select_related(
            'session', 'session__course'
        )

        data = []
        for attendance in attendances:
            data.append({
                'session_id': attendance.session.id,
                'session_title': attendance.session.title,
                'course_name': attendance.session.course.name,
                'status': attendance.status,
                'marked_at': attendance.marked_at,
                'is_late': attendance.status == ATTENDANCE_STATUSES['LATE']
            })

        serializer = StudentAttendanceSerializer(data, many=True)
        return Response(serializer.data)


class SessionAttendanceView(APIView):
    """
    View for getting attendance for a specific session.
    """
    permission_classes = [permissions.IsAuthenticated, IsLecturerOrAdmin]

    def get(self, request, session_id):
        try:
            from courses.models import ClassSession
            session = ClassSession.objects.get(id=session_id)
        except ClassSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check permissions
        if request.user.role != 'admin' and session.course.lecturer != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        attendances = Attendance.objects.filter(session=session).select_related('student')

        data = []
        for attendance in attendances:
            data.append({
                'student_id': attendance.student.id,
                'student_name': attendance.student.get_full_name(),
                'status': attendance.status,
                'marked_at': attendance.marked_at,
                'latitude': attendance.latitude,
                'longitude': attendance.longitude
            })

        serializer = SessionAttendanceSerializer(data, many=True)
        return Response(serializer.data)
