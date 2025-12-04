#!/bin/bash
cd /home/riordan/Documents/blackb/sams-project/backend

echo "=== Finding all Python files and checking imports ==="

# Create a temporary Python script to test imports
cat > /tmp/test_import.py << 'PYEOF'
import os
import sys
import importlib
import traceback

def test_file_imports(filepath):
    """Test if a Python file can be imported."""
    # Convert filepath to module path
    rel_path = os.path.relpath(filepath, '.')
    if not rel_path.endswith('.py'):
        return True
    
    # Convert to module name
    module_name = rel_path.replace('/', '.').replace('.py', '')
    
    try:
        # Try to import the module
        module = importlib.import_module(module_name)
        return True
    except ImportError as e:
        # Check if it's a Django app that needs to be loaded differently
        if 'api.apps' in module_name:
            # Try to import specific components
            parts = module_name.split('.')
            try:
                # Try to import the models module
                models_module = '.'.join(parts[:-1] + ['models'])
                importlib.import_module(models_module)
                return True
            except:
                pass
        
        print(f"✗ Cannot import {module_name}: {e}")
        return False
    except Exception as e:
        # Other errors (syntax, etc.)
        print(f"✗ Error in {module_name}: {e}")
        return False

# Walk through all Python files
for root, dirs, files in os.walk('.'):
    # Skip virtual environment directories
    if '.venv' in root or '__pycache__' in root or '.git' in root:
        continue
    
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            test_file_imports(filepath)
PYEOF

python /tmp/test_import.py

# Now let's run Django check with more debugging
echo -e "\n=== Running Django check with debug ==="
python -c "
import os
import sys
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sams.settings')
    django.setup()

# Now try to import attendance views
try:
    from api.apps.attendance import views
    print('✓ attendance.views imports successfully')
    
    # Try to import specific components
    from api.apps.attendance.serializers import (
        AttendanceSerializer, MarkAttendanceSerializer,
        StudentAttendanceSerializer, SessionAttendanceSerializer
    )
    print('✓ attendance.serializers imports successfully')
    
    from api.permissions import IsLecturerOrAdmin, IsStudentOrLecturerOrAdmin
    print('✓ permissions imports successfully')
    
    from utils.geolocation import is_within_geofence, calculate_distance
    print('✓ geolocation imports successfully')
    
    from utils.device_fingerprint import validate_device_consistency
    print('✓ device_fingerprint imports successfully')
    
    from core.exceptions import InvalidQRCodeException, LocationOutOfRangeException
    print('✓ core.exceptions imports successfully')
    
    print('\n✓ All critical imports are working!')
    
except ImportError as e:
    print(f'✗ Import error: {e}')
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f'✗ Other error: {e}')
    import traceback
    traceback.print_exc()
"

# Finally, run the Django check
echo -e "\n=== Final Django check ==="
python manage.py check --database default
