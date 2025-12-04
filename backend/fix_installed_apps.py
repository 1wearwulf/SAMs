import re

with open('sams/settings/__init__.py', 'r') as f:
    content = f.read()

# Find and replace the entire INSTALLED_APPS
new_installed_apps = '''INSTALLED_APPS = [
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

    # Local apps - ALL apps must be here
    'api.apps.accounts',
    'api.apps.attendance',
    'api.apps.courses',
    'api.apps.notifications',
    'api.apps.analytics',
    'api.apps.devices',
    'core',
]'''

# Replace INSTALLED_APPS
content = re.sub(r'INSTALLED_APPS = \[.*?\n\]', new_installed_apps, content, flags=re.DOTALL)

# Update AUTH_USER_MODEL to match
content = re.sub(r"AUTH_USER_MODEL = '.*?\.User'", "AUTH_USER_MODEL = 'accounts.User'", content)

with open('sams/settings/__init__.py', 'w') as f:
    f.write(content)

print("Fixed INSTALLED_APPS and AUTH_USER_MODEL")
