import re

# Read the settings file
with open('sams/settings/base.py', 'r') as f:
    content = f.read()

# Check if 'api.apps.attendance' is in INSTALLED_APPS
if "'api.apps.attendance'" not in content and '"api.apps.attendance"' not in content:
    print("Attendance app not found in INSTALLED_APPS, adding it...")
    
    # Find INSTALLED_APPS pattern and add attendance
    # Try to find LOCAL_APPS first
    if 'LOCAL_APPS' in content:
        # Add to LOCAL_APPS
        content = re.sub(
            r'(LOCAL_APPS\s*=\s*\[)',
            r'\1\n    "api.apps.attendance",',
            content
        )
        print("Added to LOCAL_APPS")
    else:
        # Find INSTALLED_APPS and add it
        content = re.sub(
            r'(INSTALLED_APPS\s*=\s*\[)',
            r'\1\n    "api.apps.attendance",',
            content
        )
        print("Added to INSTALLED_APPS directly")
    
    # Write back
    with open('sams/settings/base.py', 'w') as f:
        f.write(content)
else:
    print("Attendance app already in INSTALLED_APPS")

# Also check if we need to add the AppConfig version
with open('sams/settings/base.py', 'r') as f:
    content = f.read()

# Try adding as AppConfig if not already there
if 'api.apps.attendance.apps.AttendanceConfig' not in content:
    print("Adding AttendanceConfig to INSTALLED_APPS...")
    # Replace simple reference with AppConfig
    content = content.replace(
        '"api.apps.attendance",',
        '"api.apps.attendance.apps.AttendanceConfig",'
    ).replace(
        "'api.apps.attendance',",
        "'api.apps.attendance.apps.AttendanceConfig',"
    )
    
    with open('sams/settings/base.py', 'w') as f:
        f.write(content)
    print("Updated to use AttendanceConfig")
