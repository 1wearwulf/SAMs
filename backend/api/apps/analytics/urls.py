"""
URL configuration for the analytics app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AttendanceAnalyticsViewSet, StudentAnalyticsViewSet, LecturerAnalyticsViewSet,
    SystemAnalyticsViewSet, DashboardView, ReportsView
)

router = DefaultRouter()
router.register(r'attendance-analytics', AttendanceAnalyticsViewSet, basename='attendance-analytics')
router.register(r'student-analytics', StudentAnalyticsViewSet, basename='student-analytics')
router.register(r'lecturer-analytics', LecturerAnalyticsViewSet, basename='lecturer-analytics')
router.register(r'system-analytics', SystemAnalyticsViewSet, basename='system-analytics')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='analytics-dashboard'),
    path('reports/', ReportsView.as_view(), name='analytics-reports'),
]
