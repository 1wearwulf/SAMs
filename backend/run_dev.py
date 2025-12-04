import os
import sys

# Use sams.settings but override it
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')

# Import and override settings
import django
from django.conf import settings

# Force settings before setup
settings.configure(
    DEBUG=True,
    ALLOWED_HOSTS=['*'],
    # Copy other settings from sams.settings
)

django.setup()

from django.core.management import execute_from_command_line
execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
