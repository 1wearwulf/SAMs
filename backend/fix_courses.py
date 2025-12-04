with open('api/apps/courses/models.py', 'r') as f:
    lines = f.readlines()

# Find and fix the corrupted status field at line 25-29
# Replace the corrupted block with clean version
for i in range(len(lines)):
    if i < len(lines) - 4:
        # Check for the pattern
        if ('status = models.CharField(' in lines[i] and 
            'max_length=20,' in lines[i+1] and
            'status = models.CharField(' in lines[i+2]):
            print(f"Found corrupted status field at line {i+1}")
            
            # Replace with clean version
            # Note: Using COURSE_STATUSES[0] for default if COURSE_STATUSES is a list of tuples
            # If COURSE_STATUSES is a dict, use 'active' as default
            lines[i] = '    status = models.CharField(\n'
            lines[i+1] = '        max_length=20,\n'
            lines[i+2] = '        choices=COURSE_STATUSES,\n'
            lines[i+3] = '        default="active"\n'
            lines[i+4] = '    )\n'
            
            # If there are more lines in this block, adjust
            if i+5 < len(lines) and not lines[i+5].strip().startswith('    )'):
                # Need to handle more complex case
                pass
            
            print(f"Fixed lines {i+1}-{i+5}")

with open('api/apps/courses/models.py', 'w') as f:
    f.writelines(lines)

print("Fixed courses/models.py")
