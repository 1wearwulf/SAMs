from django.http import HttpResponse
import sys
import os

# Add to Django's URL patterns
def test_view(request):
    return HttpResponse('SAMS Backend is running!')

# Manual URL test
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
    import django
    django.setup()
    
    from django.test import RequestFactory
    from django.http import HttpResponse
    
    print("✅ Django setup complete")
    print("🌐 Test URL: http://10.1.34.219:8000")
