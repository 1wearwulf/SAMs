import os
import sys

# Set environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'sams.settings'

# Import Django
import django
from django.conf import settings

try:
    # This should trigger settings loading
    print("1. Testing settings load...")
    
    # Monkey patch to see what's happening
    import sams.settings
    print(f"2. settings.DEBUG from module: {sams.settings.DEBUG}")
    print(f"3. settings.ALLOWED_HOSTS from module: {sams.settings.ALLOWED_HOSTS}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Now try the proper way
print("\n4. Trying django.setup()...")
try:
    django.setup()
    print(f"5. After setup - settings.DEBUG: {settings.DEBUG}")
    print(f"6. After setup - settings.ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # Check if it's really False
    if not settings.DEBUG:
        print("\n⚠️  DEBUG is still False! Checking why...")
        
        # Check the actual config
        from decouple import config
        print(f"   config('DEBUG'): {config('DEBUG', default='NOT FOUND')}")
        print(f"   config('ALLOWED_HOSTS'): {config('ALLOWED_HOSTS', default='NOT FOUND')}")
        
        # Check environment
        print(f"   os.environ['DEBUG']: {os.environ.get('DEBUG')}")
        
except Exception as e:
    print(f"Setup error: {e}")
    import traceback
    traceback.print_exc()
