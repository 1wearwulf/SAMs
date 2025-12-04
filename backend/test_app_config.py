import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
django.setup()

# Check if attendance app is in INSTALLED_APPS
print("INSTALLED_APPS containing attendance:")
for app in settings.INSTALLED_APPS:
    if 'attendance' in app:
        print(f"  ✓ {app}")

# Try to import attendance models
try:
    from api.apps.attendance.models import QRCode
    print("✓ Successfully imported QRCode model")
except Exception as e:
    print(f"✗ Error importing QRCode: {e}")

# Check if there are any other apps missing
print("\nChecking all app imports:")
apps_to_check = [
    'api.apps.accounts',
    'api.apps.attendance', 
    'api.apps.courses',
    'api.apps.notifications',
]

for app in apps_to_check:
    try:
        __import__(app)
        print(f"✓ {app}")
    except ImportError as e:
        print(f"✗ {app}: {e}")
