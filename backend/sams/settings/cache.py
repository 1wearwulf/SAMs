"""
Cache configuration for SAMS.
"""
from datetime import timedelta

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': -1,
        },
        'KEY_PREFIX': 'sams',
        'TIMEOUT': 60 * 60 * 24,  # 24 hours default
    },
    'sessions': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'sams_sessions',
    },
    'api': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/3',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'sams_api',
        'TIMEOUT': 60 * 5,  # 5 minutes for API caching
    }
}

# Session configuration with Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'sessions'
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Cache timeouts in seconds
CACHE_TIMEOUTS = {
    'SHORT': 60 * 5,        # 5 minutes
    'MEDIUM': 60 * 30,      # 30 minutes
    'LONG': 60 * 60 * 6,    # 6 hours
    'VERY_LONG': 60 * 60 * 24 * 7,  # 7 days
}

# Cache keys template
CACHE_KEYS = {
    'USER_PROFILE': 'user:{user_id}:profile',
    'COURSE_DETAILS': 'course:{course_id}:details',
    'ATTENDANCE_STATS': 'attendance:{session_id}:stats',
    'QR_CODE': 'qr:{session_id}:code',
    'API_RESPONSE': 'api:{endpoint}:{params}',
    'NOTIFICATIONS': 'notifications:{user_id}:unread',
}

# Celery configuration for background tasks
CELERY_BROKER_URL = 'redis://localhost:6379/4'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/4'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Celery Beat periodic tasks
CELERY_BEAT_SCHEDULE = {
    'cleanup-expired-qr-codes': {
        'task': 'api.apps.attendance.tasks.cleanup_expired_qr_codes',
        'schedule': timedelta(minutes=5),
    },
    'send-attendance-reminders': {
        'task': 'api.apps.notifications.tasks.send_attendance_reminders',
        'schedule': timedelta(hours=1),
    },
    'generate-daily-reports': {
        'task': 'api.apps.analytics.tasks.generate_daily_reports',
        'schedule': timedelta(days=1),
    },
}
