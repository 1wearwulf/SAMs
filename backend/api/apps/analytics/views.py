from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from courses.models import Course
from attendance.models import AttendanceRecord, AttendanceSession


class DashboardStatsView(APIView):
    """
    API view for dashboard statistics.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get total students
        total_students = User.objects.filter(role='student').count()

        # Get total courses
        total_courses = Course.objects.count()

        # Get today's attendance percentage
        today = timezone.now().date()
        today_sessions = AttendanceSession.objects.filter(
            date=today,
            status='completed'
        )

        if today_sessions.exists():
            total_records = AttendanceRecord.objects.filter(session__in=today_sessions).count()
            present_records = AttendanceRecord.objects.filter(
                session__in=today_sessions,
                status='present'
            ).count()

            today_attendance = round((present_records / total_records * 100) if total_records > 0 else 0, 1)
        else:
            today_attendance = 0

        # Get pending tasks (sessions without records or incomplete)
        pending_tasks = AttendanceSession.objects.filter(
            Q(status='active') | Q(status='scheduled')
        ).count()

        return Response({
            'totalStudents': total_students,
            'totalCourses': total_courses,
            'todayAttendance': today_attendance,
            'pendingTasks': pending_tasks,
        })


class AttendanceStatsView(APIView):
    """
    API view for attendance statistics.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get attendance trends for the last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)

        attendance_data = []
        current_date = start_date

        while current_date <= end_date:
            sessions = AttendanceSession.objects.filter(
                date=current_date,
                status='completed'
            )

            if sessions.exists():
                total_records = AttendanceRecord.objects.filter(session__in=sessions).count()
                present_records = AttendanceRecord.objects.filter(
                    session__in=sessions,
                    status='present'
                ).count()

                percentage = round((present_records / total_records * 100) if total_records > 0 else 0, 1)
            else:
                percentage = 0

            attendance_data.append({
                'date': current_date.isoformat(),
                'attendance': percentage,
                'total_sessions': sessions.count(),
            })

            current_date += timedelta(days=1)

        # Get overall statistics
        total_sessions = AttendanceSession.objects.filter(status='completed').count()
        total_records = AttendanceRecord.objects.filter(session__status='completed').count()
        present_records = AttendanceRecord.objects.filter(
            session__status='completed',
            status='present'
        ).count()

        overall_percentage = round((present_records / total_records * 100) if total_records > 0 else 0, 1)

        return Response({
            'trends': attendance_data,
            'summary': {
                'total_sessions': total_sessions,
                'total_records': total_records,
                'present_records': present_records,
                'overall_percentage': overall_percentage,
            }
        })


class CourseStatsView(APIView):
    """
    API view for course statistics.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.annotate(
            student_count=Count('enrollments'),
            session_count=Count('sessions'),
        ).values(
            'id', 'name', 'code', 'student_count', 'session_count'
        )

        course_stats = []
        for course in courses:
            # Calculate attendance rate for this course
            sessions = AttendanceSession.objects.filter(
                course_id=course['id'],
                status='completed'
            )

            if sessions.exists():
                total_records = AttendanceRecord.objects.filter(session__in=sessions).count()
                present_records = AttendanceRecord.objects.filter(
                    session__in=sessions,
                    status='present'
                ).count()

                attendance_rate = round((present_records / total_records * 100) if total_records > 0 else 0, 1)
            else:
                attendance_rate = 0

            course_stats.append({
                'id': course['id'],
                'name': course['name'],
                'code': course['code'],
                'students': course['student_count'],
                'sessions': course['session_count'],
                'attendance_rate': attendance_rate,
            })

        return Response(course_stats)


class StudentStatsView(APIView):
    """
    API view for student statistics.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = User.objects.filter(role='student').annotate(
            course_count=Count('enrollments'),
            attendance_count=Count('attendance_records', filter=Q(attendance_records__status='present')),
            total_sessions=Count('attendance_records'),
        ).values(
            'id', 'first_name', 'last_name', 'email', 'course_count',
            'attendance_count', 'total_sessions'
        )

        student_stats = []
        for student in students:
            attendance_rate = round(
                (student['attendance_count'] / student['total_sessions'] * 100)
                if student['total_sessions'] > 0 else 0, 1
            )

            student_stats.append({
                'id': student['id'],
                'name': f"{student['first_name']} {student['last_name']}",
                'email': student['email'],
                'courses': student['course_count'],
                'attendance_rate': attendance_rate,
                'total_sessions': student['total_sessions'],
                'present_sessions': student['attendance_count'],
            })

        return Response(student_stats)
