"""
Services for the analytics app.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from django.core.cache import cache
from .models import (
    AttendanceAnalytics, StudentAnalytics, LecturerAnalytics,
    SystemAnalytics, AnalyticsCache
)

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for generating and managing analytics data.
    """

    @staticmethod
    def update_attendance_analytics(course_id: int, session_id: Optional[int] = None) -> None:
        """
        Update attendance analytics for a course or session.

        Args:
            course_id: Course ID
            session_id: Session ID (optional, if None updates all sessions for the course)
        """
        from courses.models import Course, ClassSession
        from attendance.models import Attendance

        try:
            course = Course.objects.get(id=course_id)

            if session_id:
                sessions = ClassSession.objects.filter(id=session_id, course=course)
            else:
                sessions = ClassSession.objects.filter(course=course)

            for session in sessions:
                # Get attendance data
                attendances = Attendance.objects.filter(session=session)
                total_students = course.enrolled_students.count()

                present_count = attendances.filter(status='present').count()
                absent_count = total_students - attendances.count()
                late_count = attendances.filter(status='late').count()

                attendance_rate = 0.0
                if total_students > 0:
                    attendance_rate = ((present_count + late_count) / total_students) * 100

                # Calculate average check-in time
                checkin_times = attendances.filter(
                    status__in=['present', 'late']
                ).values_list('marked_at__time', flat=True)

                average_checkin_time = None
                if checkin_times:
                    # Simple average calculation
                    total_seconds = sum(
                        t.hour * 3600 + t.minute * 60 + t.second
                        for t in checkin_times
                    )
                    avg_seconds = total_seconds / len(checkin_times)
                    hours = int(avg_seconds // 3600)
                    minutes = int((avg_seconds % 3600) // 60)
                    seconds = int(avg_seconds % 60)
                    average_checkin_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                # Update or create analytics record
                analytics, created = AttendanceAnalytics.objects.get_or_create(
                    course=course,
                    session=session,
                    date=session.scheduled_date,
                    defaults={
                        'total_students': total_students,
                        'present_count': present_count,
                        'absent_count': absent_count,
                        'late_count': late_count,
                        'attendance_rate': attendance_rate,
                        'average_checkin_time': average_checkin_time,
                    }
                )

                if not created:
                    analytics.total_students = total_students
                    analytics.present_count = present_count
                    analytics.absent_count = absent_count
                    analytics.late_count = late_count
                    analytics.attendance_rate = attendance_rate
                    analytics.average_checkin_time = average_checkin_time
                    analytics.save()

        except Exception as e:
            logger.error(f"Failed to update attendance analytics: {e}")

    @staticmethod
    def update_student_analytics(student_id: int, course_id: int) -> None:
        """
        Update analytics for a specific student in a course.

        Args:
            student_id: Student ID
            course_id: Course ID
        """
        from courses.models import Course, ClassSession
        from attendance.models import Attendance

        try:
            student = User.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)

            # Get all sessions for the course
            sessions = ClassSession.objects.filter(course=course)
            total_sessions = sessions.count()

            # Get student's attendance records
            attendances = Attendance.objects.filter(
                student=student,
                session__course=course
            )

            present_count = attendances.filter(status='present').count()
            absent_count = total_sessions - attendances.count()
            late_count = attendances.filter(status='late').count()
            excused_count = attendances.filter(status='excused').count()

            attendance_rate = 0.0
            if total_sessions > 0:
                attendance_rate = ((present_count + late_count + excused_count) / total_sessions) * 100

            # Calculate consecutive absences
            consecutive_absences = 0
            sessions_ordered = sessions.order_by('-scheduled_date')
            for session in sessions_ordered:
                attendance = attendances.filter(session=session).first()
                if not attendance or attendance.status == 'absent':
                    consecutive_absences += 1
                else:
                    break

            # Get last attendance date
            last_attendance = attendances.filter(
                status__in=['present', 'late', 'excused']
            ).order_by('-marked_at').first()

            last_attendance_date = last_attendance.marked_at.date() if last_attendance else None

            # Update or create analytics record
            analytics, created = StudentAnalytics.objects.get_or_create(
                student=student,
                course=course,
                defaults={
                    'total_sessions': total_sessions,
                    'present_count': present_count,
                    'absent_count': absent_count,
                    'late_count': late_count,
                    'excused_count': excused_count,
                    'attendance_rate': attendance_rate,
                    'consecutive_absences': consecutive_absences,
                    'last_attendance_date': last_attendance_date,
                }
            )

            if not created:
                analytics.total_sessions = total_sessions
                analytics.present_count = present_count
                analytics.absent_count = absent_count
                analytics.late_count = late_count
                analytics.excused_count = excused_count
                analytics.attendance_rate = attendance_rate
                analytics.consecutive_absences = consecutive_absences
                analytics.last_attendance_date = last_attendance_date
                analytics.save()

        except Exception as e:
            logger.error(f"Failed to update student analytics: {e}")

    @staticmethod
    def update_lecturer_analytics(lecturer_id: int, course_id: int) -> None:
        """
        Update analytics for a lecturer's course.

        Args:
            lecturer_id: Lecturer ID
            course_id: Course ID
        """
        from courses.models import Course, ClassSession

        try:
            lecturer = User.objects.get(id=lecturer_id)
            course = Course.objects.get(id=course_id)

            # Get session statistics
            sessions = ClassSession.objects.filter(course=course)
            total_sessions = sessions.count()
            completed_sessions = sessions.filter(status='completed').count()

            # Get attendance analytics
            attendance_analytics = AttendanceAnalytics.objects.filter(course=course)
            average_attendance_rate = attendance_analytics.aggregate(
                avg_rate=Avg('attendance_rate')
            )['avg_rate'] or 0.0

            # Get student statistics
            total_students = course.enrolled_students.count()
            active_students = StudentAnalytics.objects.filter(
                course=course,
                attendance_rate__gte=50.0  # Consider students with >50% attendance as active
            ).count()

            # Update or create analytics record
            analytics, created = LecturerAnalytics.objects.get_or_create(
                lecturer=lecturer,
                course=course,
                defaults={
                    'total_sessions': total_sessions,
                    'completed_sessions': completed_sessions,
                    'average_attendance_rate': average_attendance_rate,
                    'total_students': total_students,
                    'active_students': active_students,
                }
            )

            if not created:
                analytics.total_sessions = total_sessions
                analytics.completed_sessions = completed_sessions
                analytics.average_attendance_rate = average_attendance_rate
                analytics.total_students = total_students
                analytics.active_students = active_students
                analytics.save()

        except Exception as e:
            logger.error(f"Failed to update lecturer analytics: {e}")

    @staticmethod
    def update_system_analytics() -> None:
        """
        Update system-wide analytics for today.
        """
        from django.contrib.auth import get_user_model
        from courses.models import Course, ClassSession
        from attendance.models import Attendance
        from notifications.models import Notification

        User = get_user_model()
        today = timezone.now().date()

        try:
            # User statistics
            total_users = User.objects.count()
            active_users = User.objects.filter(
                last_login__date__gte=today - timedelta(days=30)
            ).count()

            # Course statistics
            total_courses = Course.objects.count()
            active_courses = Course.objects.filter(status='active').count()

            # Session statistics
            total_sessions = ClassSession.objects.count()
            completed_sessions = ClassSession.objects.filter(status='completed').count()

            # Attendance statistics
            total_attendances = Attendance.objects.count()
            recent_attendances = Attendance.objects.filter(
                created_at__date__gte=today - timedelta(days=30)
            )
            average_attendance_rate = recent_attendances.count() * 100 / max(total_sessions, 1)

            # Notification statistics
            total_notifications = Notification.objects.count()

            # System uptime (simplified - in real implementation, track actual uptime)
            system_uptime = 99.9  # Placeholder

            # Update or create system analytics
            analytics, created = SystemAnalytics.objects.get_or_create(
                date=today,
                defaults={
                    'total_users': total_users,
                    'active_users': active_users,
                    'total_courses': total_courses,
                    'active_courses': active_courses,
                    'total_sessions': total_sessions,
                    'completed_sessions': completed_sessions,
                    'total_attendances': total_attendances,
                    'average_attendance_rate': average_attendance_rate,
                    'total_notifications': total_notifications,
                    'system_uptime': system_uptime,
                }
            )

            if not created:
                analytics.total_users = total_users
                analytics.active_users = active_users
                analytics.total_courses = total_courses
                analytics.active_courses = active_courses
                analytics.total_sessions = total_sessions
                analytics.completed_sessions = completed_sessions
                analytics.total_attendances = total_attendances
                analytics.average_attendance_rate = average_attendance_rate
                analytics.total_notifications = total_notifications
                analytics.system_uptime = system_uptime
                analytics.save()

        except Exception as e:
            logger.error(f"Failed to update system analytics: {e}")

    @staticmethod
    def get_dashboard_data(user_id: int, user_role: str) -> Dict[str, Any]:
        """
        Get dashboard analytics data for a user.

        Args:
            user_id: User ID
            user_role: User role

        Returns:
            Dictionary with dashboard data
        """
        cache_key = f"dashboard_data_{user_id}_{user_role}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        data = {}

        if user_role == 'student':
            data = AnalyticsService._get_student_dashboard_data(user_id)
        elif user_role == 'lecturer':
            data = AnalyticsService._get_lecturer_dashboard_data(user_id)
        elif user_role == 'admin':
            data = AnalyticsService._get_admin_dashboard_data()

        # Cache for 1 hour
        cache.set(cache_key, data, timeout=3600)

        return data

    @staticmethod
    def _get_student_dashboard_data(student_id: int) -> Dict[str, Any]:
        """Get dashboard data for a student."""
        analytics = StudentAnalytics.objects.filter(student_id=student_id)

        return {
            'total_courses': analytics.count(),
            'average_attendance_rate': analytics.aggregate(avg=Avg('attendance_rate'))['avg'] or 0,
            'courses_at_risk': analytics.filter(attendance_rate__lt=75).count(),
            'recent_performance': list(analytics.values(
                'course__name', 'attendance_rate', 'consecutive_absences'
            )[:5])
        }

    @staticmethod
    def _get_lecturer_dashboard_data(lecturer_id: int) -> Dict[str, Any]:
        """Get dashboard data for a lecturer."""
        analytics = LecturerAnalytics.objects.filter(lecturer_id=lecturer_id)

        return {
            'total_courses': analytics.count(),
            'total_sessions': analytics.aggregate(total=Sum('total_sessions'))['total'] or 0,
            'average_class_attendance': analytics.aggregate(avg=Avg('average_attendance_rate'))['avg'] or 0,
            'total_students': analytics.aggregate(total=Sum('total_students'))['total'] or 0,
            'course_performance': list(analytics.values(
                'course__name', 'average_attendance_rate', 'active_students'
            )[:5])
        }

    @staticmethod
    def _get_admin_dashboard_data() -> Dict[str, Any]:
        """Get dashboard data for an admin."""
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        today_stats = SystemAnalytics.objects.filter(date=today).first()
        yesterday_stats = SystemAnalytics.objects.filter(date=yesterday).first()

        return {
            'total_users': today_stats.total_users if today_stats else 0,
            'active_users': today_stats.active_users if today_stats else 0,
            'total_courses': today_stats.total_courses if today_stats else 0,
            'average_attendance_rate': today_stats.average_attendance_rate if today_stats else 0,
            'user_growth': (today_stats.total_users - yesterday_stats.total_users) if today_stats and yesterday_stats else 0,
            'recent_trends': list(SystemAnalytics.objects.filter(
                date__gte=today - timedelta(days=7)
            ).values('date', 'total_users', 'average_attendance_rate').order_by('date'))
        }

    @staticmethod
    def generate_attendance_report(course_id: int, start_date: datetime.date, end_date: datetime.date) -> Dict[str, Any]:
        """
        Generate a detailed attendance report for a course.

        Args:
            course_id: Course ID
            start_date: Start date for the report
            end_date: End date for the report

        Returns:
            Dictionary with report data
        """
        from courses.models import Course, ClassSession
        from attendance.models import Attendance

        course = Course.objects.get(id=course_id)
        sessions = ClassSession.objects.filter(
            course=course,
            scheduled_date__range=[start_date, end_date]
        ).order_by('scheduled_date')

        report_data = {
            'course_name': course.name,
            'course_code': course.code,
            'period': f"{start_date} to {end_date}",
            'total_sessions': sessions.count(),
            'sessions': []
        }

        for session in sessions:
            attendances = Attendance.objects.filter(session=session)
            session_data = {
                'date': session.scheduled_date,
                'title': session.title,
                'total_enrolled': course.enrolled_students.count(),
                'present': attendances.filter(status='present').count(),
                'late': attendances.filter(status='late').count(),
                'absent': course.enrolled_students.count() - attendances.count(),
                'attendance_rate': 0
            }

            if session_data['total_enrolled'] > 0:
                session_data['attendance_rate'] = (
                    (session_data['present'] + session_data['late']) /
                    session_data['total_enrolled']
                ) * 100

            report_data['sessions'].append(session_data)

        return report_data

    @staticmethod
    def get_cached_analytics(cache_key: str, timeout: int = 3600) -> Optional[Dict[str, Any]]:
        """
        Get cached analytics data.

        Args:
            cache_key: Cache key
            timeout: Cache timeout in seconds

        Returns:
            Cached data or None
        """
        cached = AnalyticsCache.objects.filter(
            cache_key=cache_key,
            expires_at__gt=timezone.now()
        ).first()

        return cached.data if cached else None

    @staticmethod
    def set_cached_analytics(cache_key: str, data: Dict[str, Any], timeout: int = 3600) -> None:
        """
        Cache analytics data.

        Args:
            cache_key: Cache key
            data: Data to cache
            timeout: Cache timeout in seconds
        """
        expires_at = timezone.now() + timedelta(seconds=timeout)

        cache_obj, created = AnalyticsCache.objects.get_or_create(
            cache_key=cache_key,
            defaults={'data': data, 'expires_at': expires_at}
        )

        if not created:
            cache_obj.data = data
            cache_obj.expires_at = expires_at
            cache_obj.save()
