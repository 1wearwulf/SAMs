import sys
import os

# Add debug to imports
import builtins
_real_import = builtins.__import__

def debug_import(name, *args, **kwargs):
    if 'sams.settings' in name or 'settings' in name:
        print(f"Importing: {name}")
    result = _real_import(name, *args, **kwargs)
    if 'sams.settings' in name:
        print(f"  Imported module at: {result.__file__ if hasattr(result, '__file__') else 'No file'}")
    return result

builtins.__import__ = debug_import

# Now import Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'sams.settings'
import django
django.setup()

from django.conf import settings
print(f"\nFinal settings:")
print(f"  DEBUG: {settings.DEBUG}")
print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
