import re

def fix_corrupted_field(content, field_name, constant_name, default_value):
    """Fix a corrupted CharField with choices."""
    # Pattern for corrupted field: field_name = models.CharField( ... field_name = models.CharField( ... )
    pattern = rf'{field_name}\s*=\s*models\.CharField\s*\(\s*\n\s*max_length\s*=\s*\d+\s*,\s*\n\s*{field_name}\s*=\s*models\.CharField.*?\n\s*default\s*=\s*[^)]+'
    
    # Try to find and replace
    matches = list(re.finditer(pattern, content, re.DOTALL))
    if matches:
        print(f"Found {len(matches)} corrupted {field_name} fields")
        for match in matches:
            print(f"  At position {match.start()}")
    
    # Simpler: replace the specific corrupted pattern
    corrupted_pattern = rf'({field_name}\s*=\s*models\.CharField\(\s*\n\s*max_length\s*=\s*\d+\s*,\s*\n\s*){field_name}\s*=\s*models\.CharField\([^)]+\)(\s*\n\s*default\s*=\s*[^)]+\s*\n\s*\))'
    
    replacement = rf'\1choices={constant_name},\2'
    new_content = re.sub(corrupted_pattern, replacement, content, flags=re.DOTALL)
    
    if new_content != content:
        print(f"Fixed {field_name} field")
        return new_content
    
    return content

# Read the file
with open('api/apps/courses/models.py', 'r') as f:
    content = f.read()

# Fix status field with COURSE_STATUSES
content = fix_corrupted_field(content, 'status', 'COURSE_STATUSES', '"active"')

# Also look for any other similar patterns
# Fix pattern: field = models.CharField( ... field = models.CharField( ... )
general_pattern = r'(\w+)\s*=\s*models\.CharField\(\s*\n\s*max_length\s*=\s*\d+\s*,\s*\n\s*\1\s*=\s*models\.CharField'
matches = re.findall(general_pattern, content, re.DOTALL)
if matches:
    print(f"\nFound other potentially corrupted fields: {matches}")
    for field in matches:
        content = re.sub(
            rf'({field}\s*=\s*models\.CharField\(\s*\n\s*max_length\s*=\s*\d+\s*,\s*\n\s*){field}\s*=\s*models\.CharField\([^)]+\)(\s*\n\s*default\s*=\s*[^)]+\s*\n\s*\))',
            rf'\1choices=CONSTANT,\2',  # Generic fix
            content,
            flags=re.DOTALL
        )

# Write back
with open('api/apps/courses/models.py', 'w') as f:
    f.write(content)

print("\nApplied comprehensive fixes")
