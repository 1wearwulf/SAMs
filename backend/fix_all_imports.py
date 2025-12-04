import os
import sys

print("=== Fixing all import issues ===")

# 1. Fix utils/constants.py
constants_py = "utils/constants.py"
if not os.path.exists(constants_py):
    os.makedirs(os.path.dirname(constants_py), exist_ok=True)
    with open(constants_py, 'w') as f:
        f.write('''"""
Constants for utility modules.
"""

# Geocoding timeout in seconds
GEOCODING_TIMEOUT_SECONDS = 10

# API timeouts
REQUEST_TIMEOUT_SECONDS = 30

# Cache timeouts
CACHE_TIMEOUT_HOURS = 24

# File upload limits (in MB)
MAX_FILE_SIZE_MB = 10

# Image dimensions
MAX_IMAGE_WIDTH = 1920
MAX_IMAGE_HEIGHT = 1080

# Security constants
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_TIME_MINUTES = 15

# Default pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
''')
    print(f"✓ Created {constants_py}")

# 2. Update utils/geolocation.py to not import missing constants
geolocation_py = "utils/geolocation.py"
if os.path.exists(geolocation_py):
    with open(geolocation_py, 'r') as f:
        content = f.read()
    
    # Replace the import line
    new_content = content.replace(
        "from .constants import GEOCODING_TIMEOUT_SECONDS, DEFAULT_GEOFENCE_RADIUS_METERS",
        "from core.constants import DEFAULT_GEOFENCE_RADIUS_METERS"
    )
    
    with open(geolocation_py, 'w') as f:
        f.write(new_content)
    print(f"✓ Updated {geolocation_py}")

# 3. Check and fix all other potential missing imports
# Check what core.constants is missing
core_constants_py = "core/constants.py"
if os.path.exists(core_constants_py):
    with open(core_constants_py, 'r') as f:
        core_content = f.read()
    
    # Add any missing commonly used constants
    missing_constants = []
    
    if 'OTP_EXPIRY_SECONDS' not in core_content:
        missing_constants.append('\n# OTP expiry (5 minutes = 300 seconds)\nOTP_EXPIRY_SECONDS = 300')
    
    if 'EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS' not in core_content:
        missing_constants.append('\n# Email verification token expiry (24 hours)\nEMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS = 24')
    
    if 'JWT_TOKEN_EXPIRY_HOURS' not in core_content:
        missing_constants.append('\n# JWT token expiry (24 hours)\nJWT_TOKEN_EXPIRY_HOURS = 24')
    
    if 'REFRESH_TOKEN_EXPIRY_DAYS' not in core_content:
        missing_constants.append('\n# Refresh token expiry (7 days)\nREFRESH_TOKEN_EXPIRY_DAYS = 7')
    
    if missing_constants:
        with open(core_constants_py, 'a') as f:
            f.write('\n' + '\n'.join(missing_constants))
        print(f"✓ Added missing constants to {core_constants_py}")

# 4. Check for missing __init__.py files
init_files_to_check = [
    "utils/__init__.py",
    "core/__init__.py",
    "api/__init__.py",
    "api/apps/__init__.py",
    "api/apps/accounts/__init__.py",
    "api/apps/attendance/__init__.py",
    "api/apps/courses/__init__.py",
    "api/apps/notifications/__init__.py",
]

for init_file in init_files_to_check:
    if not os.path.exists(init_file):
        os.makedirs(os.path.dirname(init_file), exist_ok=True)
        with open(init_file, 'w') as f:
            f.write('')
        print(f"✓ Created {init_file}")

# 5. Create a simple test to check all imports
print("\n=== Testing imports ===")
test_code = '''
try:
    # Test core imports
    from core.constants import *
    from core.exceptions import *
    from core.models import TimestampedModel
    
    # Test utils imports
    from utils.geolocation import calculate_distance, is_within_geofence
    from utils.device_fingerprint import validate_device_consistency, get_request_fingerprint
    from utils.security import generate_secure_token
    
    # Test api imports
    from api.permissions import IsLecturerOrAdmin, IsStudentOrLecturerOrAdmin
    from api.apps.accounts.models import User
    from api.apps.attendance.models import Attendance, QRCode
    from api.apps.courses.models import Course, ClassSession
    from api.apps.attendance.serializers import (
        AttendanceSerializer, MarkAttendanceSerializer,
        StudentAttendanceSerializer, SessionAttendanceSerializer
    )
    
    print("✓ All imports successful!")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
'''

# Write and run test
test_file = "test_imports.py"
with open(test_file, 'w') as f:
    f.write(test_code)

try:
    exec(open(test_file).read())
except Exception as e:
    print(f"Test failed: {e}")

# Clean up
if os.path.exists(test_file):
    os.remove(test_file)

print("\n=== Import fix completed ===")
