import os
import re

# Constants that should be used directly
CONSTANTS = [
    'ATTENDANCE_STATUSES',
    'COURSE_STATUSES', 
    'SESSION_STATUSES',
    'COURSE_TYPES',
    'USER_ROLES',
    'ENROLLMENT_STATUSES',
    'NOTIFICATION_TYPES',
    'DEVICE_TYPES',
    'ACADEMIC_YEARS',
    'SEMESTERS'
]

def fix_file(filepath):
    print(f"\nFixing {filepath}")
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Fix pattern 1: choices=[(k, k.title()) for k in CONSTANT]
    for const in CONSTANTS:
        pattern = r'choices=\[\(([a-zA-Z]), \1\.title\(\)\) for \1 in ' + const + r'\]'
        replacement = f'choices={const}'
        content = re.sub(pattern, replacement, content)
    
    # Fix pattern 2: choices=[(k, v) for k, v in CONSTANT]
    for const in CONSTANTS:
        pattern = r'choices=\[\(k, v\) for k, v in ' + const + r'\]'
        replacement = f'choices={const}'
        content = re.sub(pattern, replacement, content)
    
    # Fix pattern 3: choices=[(k, k.title()) for k in CONSTANT.values()]
    for const in CONSTANTS:
        pattern = r'choices=\[\(([a-zA-Z]), \1\.title\(\)\) for \1 in ' + const + r'\.values\(\)\]'
        replacement = f'choices={const}'
        content = re.sub(pattern, replacement, content)
    
    # Write back
    with open(filepath, 'w') as f:
        f.write(content)
    
    # Check if file compiles
    try:
        compile(content, filepath, 'exec')
        print(f"✓ {filepath} syntax OK")
    except SyntaxError as e:
        print(f"✗ {filepath} still has syntax error: {e}")
        # Show problematic area
        lines = content.split('\n')
        error_line = e.lineno - 1 if e.lineno else 0
        start = max(0, error_line - 3)
        end = min(len(lines), error_line + 4)
        for i in range(start, end):
            prefix = '>>> ' if i == error_line else '    '
            print(f"{prefix}{i+1}: {lines[i]}")

# Find all models.py files
for root, dirs, files in os.walk('api/apps'):
    for file in files:
        if file == 'models.py':
            filepath = os.path.join(root, file)
            fix_file(filepath)
