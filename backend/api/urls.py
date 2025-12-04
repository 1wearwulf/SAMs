from django.urls import path, include
from . import views

urlpatterns = [
    # API root
    path('', views.api_root, name='api-root'),
    
    # All authentication goes through accounts app
    path('accounts/', include('api.apps.accounts.urls')),
    
    # Other API endpoints (commented out until fixed)
    # path('attendance/', include('api.apps.attendance.urls')),
    # path('courses/', include('api.apps.courses.urls')),
    # path('notifications/', include('api.apps.notifications.urls')),
    # path('analytics/', include('api.apps.analytics.urls')),
    # path('devices/', include('api.apps.devices.urls')),
]

app_name = 'api'
