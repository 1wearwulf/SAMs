import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')

try:
    import django
    django.setup()
    print("✓ Django setup successful")
    
    # Check INSTALLED_APPS
    from django.conf import settings
    print(f"\nINSTALLED_APPS ({len(settings.INSTALLED_APPS)} apps):")
    
    attendance_found = False
    for app in settings.INSTALLED_APPS:
        if 'attendance' in app:
            attendance_found = True
            print(f"  ✓ {app}")
        else:
            print(f"    {app}")
    
    if not attendance_found:
        print("\n✗ Attendance app not found in INSTALLED_APPS")
        print("\nCurrent INSTALLED_APPS definition in base.py:")
        import re
        with open('sams/settings/base.py', 'r') as f:
            content = f.read()
            match = re.search(r'INSTALLED_APPS\s*=\s*\[.*?\]', content, re.DOTALL)
            if match:
                print(match.group(0))
    
    # Try to import attendance models
    print("\n" + "="*50)
    print("Testing attendance model import...")
    try:
        from api.apps.attendance.models import QRCode
        print("✓ Successfully imported QRCode")
    except Exception as e:
        print(f"✗ Error importing QRCode: {e}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
