import os
import sys

# Set up environment
os.environ['DEBUG'] = 'True'
os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,0.0.0.0,*'
os.environ['DATABASE_URL'] = 'sqlite:///db.sqlite3'
os.environ['DJANGO_SETTINGS_MODULE'] = 'sams.settings'

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import django
    django.setup()
    print("✓ Django setup successful")
    
    from django.core.management import execute_from_command_line
    print("✓ Starting server...")
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
