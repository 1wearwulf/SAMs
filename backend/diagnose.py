import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')

try:
    import django
    django.setup()
    
    from django.conf import settings
    from django.apps import apps
    
    print("🔍 DIAGNOSTIC:")
    print("="*50)
    
    # 1. Check AUTH_USER_MODEL
    print(f"1. AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
    
    # 2. Check accounts app
    try:
        accounts_config = apps.get_app_config('accounts')
        print(f"2. Accounts app: ✅ Found")
        print(f"   - label: {accounts_config.label}")
        print(f"   - name: {accounts_config.name}")
        print(f"   - models module: {accounts_config.models_module}")
    except:
        print(f"2. Accounts app: ❌ Not found")
    
    # 3. Try to get User model
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        print(f"3. User model: ✅ {User}")
        print(f"   - module: {User.__module__}")
    except Exception as e:
        print(f"3. User model: ❌ Error: {e}")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
