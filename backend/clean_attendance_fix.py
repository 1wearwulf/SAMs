with open('api/apps/attendance/models.py', 'r') as f:
    content = f.read()

# Find the Attendance class
import re

# Pattern to find the status field with various possible corruptions
# We need to find and fix the broken status field definition
print("Looking for status field patterns...")

# Check for multiple status field definitions
status_matches = list(re.finditer(r'status\s*=\s*models\.CharField', content))
print(f"Found {len(status_matches)} status field definitions")

if len(status_matches) > 1:
    print("Multiple status fields found - need to clean up")
    # Find the class definition first
    class_start = content.find('class Attendance')
    if class_start != -1:
        # Find the end of the class (next class or function definition)
        class_end_pattern = re.compile(r'\nclass |\ndef |\n\n')
        class_end_match = class_end_pattern.search(content, class_start + 1)
        if class_end_match:
            class_end = class_end_match.start()
        else:
            class_end = len(content)
        
        class_content = content[class_start:class_end]
        
        # Replace the entire broken status field with a clean one
        # Look for the pattern with parentheses
        cleaned_class = re.sub(
            r'status\s*=\s*models\.CharField\s*\(\s*\n?\s*max_length\s*=\s*20\s*,?\s*\n?\s*status\s*=\s*models\.CharField.*?\n?\s*default\s*=\s*[\'"][^\'"]*[\'"]\s*\n?\s*\)',
            '''    status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_STATUSES,
        default="present"
    )''',
            class_content,
            flags=re.DOTALL
        )
        
        # If that didn't work, try a simpler replacement
        if cleaned_class == class_content:
            cleaned_class = re.sub(
                r'status\s*=\s*models\.CharField.*?\n.*?\n.*?\n',
                '''    status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_STATUSES,
        default="present"
    )
''',
                class_content,
                flags=re.DOTALL
            )
        
        # Replace the class content in the full content
        content = content[:class_start] + cleaned_class + content[class_end:]
        
        with open('api/apps/attendance/models.py', 'w') as f:
            f.write(content)
        print("Fixed attendance models.py")
    else:
        print("Could not find Attendance class")
else:
    print("Only one status field found - checking syntax...")
    # Just fix the syntax if it's broken
    content = re.sub(
        r'status\s*=\s*models\.CharField\(\s*max_length\s*=\s*20\s*,\s*choices\s*=\s*ATTENDANCE_STATUSES\s*,\s*default\s*=\s*"present"\s*\)',
        'status = models.CharField(max_length=20, choices=ATTENDANCE_STATUSES, default="present")',
        content
    )
    with open('api/apps/attendance/models.py', 'w') as f:
        f.write(content)
    print("Fixed syntax")
