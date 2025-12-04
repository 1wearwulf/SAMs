from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'attendance', views.AttendanceViewSet, basename='attendance')
# Fix: Use correct view name (AttendanceViewSet instead of AttendanceLogViewSet)
# router.register(r'attendance-logs', views.AttendanceViewSet, basename='attendance-log')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'attendance'
