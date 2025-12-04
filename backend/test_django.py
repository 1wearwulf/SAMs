import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings.development')

try:
    django.setup()
    print("✅ Django loaded successfully!")
    from django.conf import settings
    print(f"DEBUG mode: {settings.DEBUG}")
    print(f"Database: {settings.DATABASES['default']['ENGINE']}")
except Exception as e:
    print(f"❌ Django failed to load: {e}")
    import traceback
    traceback.print_exc()
