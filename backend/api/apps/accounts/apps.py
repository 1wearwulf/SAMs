from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.apps.accounts'
    verbose_name = 'Accounts'
    
    def ready(self):
        # Import signals here if needed
        pass
