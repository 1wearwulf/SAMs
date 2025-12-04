"""
API URL Configuration for SAMS.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps.accounts import views as accounts_views

router = DefaultRouter()
router.register(r'users', accounts_views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    # Add other URLs as they become available
]

print("Using minimal API URLs for now")
