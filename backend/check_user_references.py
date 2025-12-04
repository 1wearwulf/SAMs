import os
import re
import sys

def check_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for problematic patterns
    patterns = [
        (r"models\.ForeignKey\s*\(\s*['\"]auth\.User['\"]", "Direct reference to auth.User"),
        (r"from django\.contrib\.auth\.models import User", "Importing default User"),
        (r"import.*User.*from django\.contrib\.auth", "Importing default User"),
    ]
    
    for pattern, message in patterns:
        if re.search(pattern, content):
            issues.append(f"  - {message}")
    
    return issues

print("Checking all Python files for User model references...")
all_issues = []

for root, dirs, files in os.walk('api/apps'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            issues = check_file(filepath)
            if issues:
                print(f"\n{filepath}:")
                all_issues.extend(issues)
                for issue in issues:
                    print(issue)

if all_issues:
    print(f"\n✗ Found {len(all_issues)} issues with User model references")
    print("\nYou need to fix these to use accounts.User consistently")
else:
    print("\n✓ All User model references look good!")

# Check settings
print("\n=== CHECKING SETTINGS ===")
try:
    with open('sams/settings/base.py', 'r') as f:
        content = f.read()
        if "AUTH_USER_MODEL = 'accounts.User'" in content:
            print("✓ AUTH_USER_MODEL is correctly set to 'accounts.User'")
        else:
            print("✗ AUTH_USER_MODEL is NOT set to 'accounts.User'")
except:
    print("Could not check settings file")
