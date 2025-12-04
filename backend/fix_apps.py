import sys
import re

with open('sams/settings/__init__.py', 'r') as f:
    content = f.read()

# Remove any existing INSTALLED_APPS
content = re.sub(r"INSTALLED_APPS = \[.*?\n\]", "", content, flags=re.DOTALL)

# Add correct INSTALLED_APPS
correct_apps = '''INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',
    'fcm_django',
    'django_celery_beat',
    'drf_yasg',

    # Local apps - USE CORRECT PATHS
    'api.apps.accounts',
    'api.apps.attendance',
    'api.apps.courses',
    'api.apps.notifications',
    'api.apps.analytics',
    'api.apps.devices',
    'core',
]'''

# Insert after imports but before MIDDLEWARE
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'MIDDLEWARE = [' in line:
        lines.insert(i, correct_apps)
        break

with open('sams/settings/__init__.py', 'w') as f:
    f.write('\n'.join(lines))

print("Fixed INSTALLED_APPS")
