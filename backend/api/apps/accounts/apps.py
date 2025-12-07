from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.apps.accounts'  # Python import path
    label = 'accounts'  # Short name for AUTH_USER_MODEL
    verbose_name = 'Accounts'
