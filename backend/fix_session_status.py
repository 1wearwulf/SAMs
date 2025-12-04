with open('api/apps/courses/models.py', 'r') as f:
    lines = f.readlines()

# Fix line 90: default=SESSION_STATUSES['SCHEDULED'] should be default="scheduled"
for i, line in enumerate(lines):
    if "default=SESSION_STATUSES[" in line:
        print(f"Found dict access on tuple at line {i+1}: {line.strip()}")
        # Extract the key from between the quotes
        import re
        match = re.search(r"default=SESSION_STATUSES\['([^']+)'\]", line)
        if match:
            key = match.group(1).lower()
            lines[i] = re.sub(r"default=SESSION_STATUSES\['[^']+'\]", f'default="{key}"', line)
            print(f"Changed to: {lines[i].strip()}")
        else:
            # Try with double quotes
            match = re.search(r'default=SESSION_STATUSES\["([^"]+)"\]', line)
            if match:
                key = match.group(1).lower()
                lines[i] = re.sub(r'default=SESSION_STATUSES\["[^"]+"\]', f'default="{key}"', line)
                print(f"Changed to: {lines[i].strip()}")

# Also check COURSE_STATUSES
for i, line in enumerate(lines):
    if "default=COURSE_STATUSES[" in line:
        print(f"Found COURSE_STATUSES dict access at line {i+1}: {line.strip()}")
        import re
        match = re.search(r"default=COURSE_STATUSES\['([^']+)'\]", line)
        if match:
            key = match.group(1).lower()
            lines[i] = re.sub(r"default=COURSE_STATUSES\['[^']+'\]", f'default="{key}"', line)
            print(f"Changed to: {lines[i].strip()}")
        else:
            match = re.search(r'default=COURSE_STATUSES\["([^"]+)"\]', line)
            if match:
                key = match.group(1).lower()
                lines[i] = re.sub(r'default=COURSE_STATUSES\["[^"]+"\]', f'default="{key}"', line)
                print(f"Changed to: {lines[i].strip()}")

with open('api/apps/courses/models.py', 'w') as f:
    f.writelines(lines)

print("Fixed tuple index errors")
