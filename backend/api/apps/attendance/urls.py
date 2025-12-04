"""
URLs for the attendance app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'attendance', views.AttendanceViewSet, basename='attendance')
router.register(r'qr-codes', views.QRCodeViewSet, basename='qr-code')
router.register(r'attendance-logs', views.AttendanceLogViewSet, basename='attendance-log')
router.register(r'anti-cheat-flags', views.AntiCheatFlagViewSet, basename='anti-cheat-flag')
router.register(r'bulk-imports', views.BulkAttendanceImportViewSet, basename='bulk-import')

urlpatterns = [
    path('', include(router.urls)),
    path('mark-attendance/', views.MarkAttendanceAPIView.as_view(), name='mark-attendance'),
    path('generate-qr/<int:session_id>/', views.GenerateQRCodeAPIView.as_view(), name='generate-qr'),
    path('validate-qr/', views.ValidateQRCodeAPIView.as_view(), name='validate-qr'),
    path('stats/', views.AttendanceStatsAPIView.as_view(), name='attendance-stats'),
    path('export/', views.AttendanceExportAPIView.as_view(), name='attendance-export'),
]
