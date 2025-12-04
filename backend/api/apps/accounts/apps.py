from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.apps.accounts'
    label = 'accounts'  # EXPLICITLY SET THIS
    
    def ready(self):
        # Import signals if you have any
        try:
            import api.apps.accounts.signals  # noqa: F401
        except ImportError:
            pass
