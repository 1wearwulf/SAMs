import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'sams.settings'

import django
django.setup()

from django.conf import settings
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"SECRET_KEY exists: {'SECRET_KEY' in dir(settings)}")
