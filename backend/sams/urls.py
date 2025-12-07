"""SAMS URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Simple test view
def test_api(request):
    return HttpResponse('SAMS Backend is running!')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/test/', test_api, name='test-api'),
]
