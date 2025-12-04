from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.apps.attendance'
    verbose_name = 'Attendance Management'
    
    def ready(self):
        # Import signals or other initialization code here
        try:
            import api.apps.attendance.signals  # noqa: F401
        except ImportError:
            pass
