from .base import *

DEBUG = False

SECRET_KEY = 'test-secret-key-not-for-production'

# Test database (SQLite in memory)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable password hashing for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Email backend for tests
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable throttling in tests
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {}

# FCM settings for tests
FCM_DJANGO_SETTINGS["FCM_SERVER_KEY"] = 'test-fcm-key'

# Redis settings for tests (use in-memory if available, otherwise skip)
CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = 'memory://'
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Logging for tests
LOGGING['handlers']['console']['level'] = 'ERROR'
LOGGING['root']['level'] = 'ERROR'
LOGGING['loggers']['django']['level'] = 'ERROR'
