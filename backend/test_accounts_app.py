import os
import sys
sys.path.insert(0, '.')

# Set up minimal Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')

print("1. Testing import...")
try:
    import api.apps.accounts
    print("   ✓ Imported api.apps.accounts")
except Exception as e:
    print(f"   ✗ Import failed: {e}")
    sys.exit(1)

print("\n2. Testing Django setup...")
import django
try:
    django.setup()
    print("   ✓ Django setup successful")
except Exception as e:
    print(f"   ✗ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. Checking app registration...")
from django.apps import apps
try:
    app_config = apps.get_app_config('accounts')
    print(f"   ✓ Found app: {app_config.name}")
except Exception as e:
    print(f"   ✗ App not found: {e}")
    
print("\n4. All apps:")
for app in apps.get_app_configs():
    print(f"   - {app.label}: {app.name}")
