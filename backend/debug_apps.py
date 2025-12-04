import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')

import django
django.setup()

from django.apps import apps

print("=== All installed apps ===")
for app in apps.get_app_configs():
    print(f"{app.label:20} -> {app.name}")

print("\n=== Looking for accounts ===")
accounts_found = False
for app in apps.get_app_configs():
    if 'account' in app.name:
        print(f"FOUND: {app.label} -> {app.name}")
        accounts_found = True
        
        # Try to get models
        print(f"  Models in this app: {list(app.models.keys())}")
        
if not accounts_found:
    print("No accounts app found in app registry!")

print("\n=== Trying to get app config ===")
for label in ['accounts', 'api_apps_accounts', 'api.apps.accounts']:
    try:
        app = apps.get_app_config(label)
        print(f"✓ get_app_config('{label}'): {app.name}")
    except Exception as e:
        print(f"✗ get_app_config('{label}'): {e}")

print("\n=== Checking INSTALLED_APPS ===")
from django.conf import settings
for app in settings.INSTALLED_APPS:
    if 'account' in app:
        print(f"  {app}")
