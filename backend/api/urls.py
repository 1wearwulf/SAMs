from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'attendance', views.AttendanceViewSet, basename='attendance')
router.register(r'devices', views.DeviceViewSet, basename='userdevice')

accounts_router = DefaultRouter()
accounts_router.register(r'students', views.StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/', include(accounts_router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('attendance/mark/', views.MarkAttendanceView.as_view(), name='mark-attendance'),
    path('attendance/verify/', views.VerifyAttendanceView.as_view(), name='verify-attendance'),
    path('courses/<int:pk>/sessions/', views.CourseSessionsView.as_view(), name='course-sessions'),
    path('reports/attendance/', views.AttendanceReportView.as_view(), name='attendance-report'),
    path('analytics/', include('api.apps.analytics.urls')),
]
