"""
URL configuration for the courses app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, ClassSessionViewSet, CourseMaterialViewSet,
    CourseAnnouncementViewSet, EnrollmentRequestViewSet,
    StudentCoursesView, LecturerCoursesView, CourseSearchView, UpcomingSessionsView
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'sessions', ClassSessionViewSet, basename='class-session')
router.register(r'materials', CourseMaterialViewSet, basename='course-material')
router.register(r'announcements', CourseAnnouncementViewSet, basename='course-announcement')
router.register(r'enrollment-requests', EnrollmentRequestViewSet, basename='enrollment-request')

urlpatterns = [
    path('', include(router.urls)),
    path('my-courses/', StudentCoursesView.as_view(), name='student-courses'),
    path('teaching-courses/', LecturerCoursesView.as_view(), name='lecturer-courses'),
    path('search/', CourseSearchView.as_view(), name='course-search'),
    path('upcoming-sessions/', UpcomingSessionsView.as_view(), name='upcoming-sessions'),
]
