#!/bin/bash

# Fix attendance/models.py
cat > /tmp/fix_attendance.py << 'PYEOF'
with open('api/apps/attendance/models.py', 'r') as f:
    lines = f.readlines()

# Find and fix the problematic line(s)
for i, line in enumerate(lines):
    if 'choices=[' in line and 'for' in line and 'in' in line:
        # Extract the constant name
        import re
        match = re.search(r'choices=\[.*for.*in\s+([A-Z_]+)', line)
        if match:
            const_name = match.group(1)
            # Replace the entire choices expression with just the constant
            new_line = re.sub(r'choices=\[.*for.*in\s+[A-Z_]+\]', f'choices={const_name}', line)
            lines[i] = new_line
            print(f"Fixed line {i+1}: {new_line.strip()}")

with open('api/apps/attendance/models.py', 'w') as f:
    f.writelines(lines)
PYEOF

python /tmp/fix_attendance.py
rm /tmp/fix_attendance.py

# Also fix courses/models.py
for file in api/apps/courses/models.py; do
    sed -i 's/choices=\[.*for k in COURSE_STATUSES\]/choices=COURSE_STATUSES/g' "$file"
    sed -i 's/choices=\[.*for k in SESSION_STATUSES\]/choices=SESSION_STATUSES/g' "$file"
done
