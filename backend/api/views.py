"""
Main API views that import from app-specific views.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Import ViewSets from app views
from api.apps.accounts.views import UserViewSet, StudentViewSet
from api.apps.courses.views import CourseViewSet
from api.apps.attendance.views import AttendanceViewSet

# Import additional views from app views
from api.apps.accounts.views import RegisterView
from api.apps.attendance.views import MarkAttendanceView, ValidateQRView, AttendanceStatsView
from api.apps.courses.views import UpcomingSessionsView

# Device ViewSet - create a simple one since devices/views.py doesn't exist
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from api.apps.devices.models import UserDevice
from api.apps.devices.serializers import UserDeviceSerializer

class DeviceViewSet(ModelViewSet):
    """
    ViewSet for UserDevice model.
    """
    queryset = UserDevice.objects.all()
    serializer_class = UserDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Additional views
class VerifyAttendanceView(ValidateQRView):
    """
    Alias for ValidateQRView to match URL naming.
    """
    pass


class CourseSessionsView(UpcomingSessionsView):
    """
    Alias for UpcomingSessionsView to match URL naming.
    """
    pass


class AttendanceReportView(AttendanceStatsView):
    """
    Alias for AttendanceStatsView to match URL naming.
    """
    pass
