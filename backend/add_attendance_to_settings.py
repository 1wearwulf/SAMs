import re

with open('sams/settings/base.py', 'r') as f:
    lines = f.readlines()

# Find where to add attendance
for i, line in enumerate(lines):
    # Look for INSTALLED_APPS definition
    if 'INSTALLED_APPS' in line and '=' in line:
        # Find the opening bracket
        for j in range(i, len(lines)):
            if '[' in lines[j]:
                start_line = j
                # Find the closing bracket
                bracket_count = 1
                for k in range(j+1, len(lines)):
                    if '[' in lines[k]:
                        bracket_count += 1
                    if ']' in lines[k]:
                        bracket_count -= 1
                        if bracket_count == 0:
                            end_line = k
                            # Add attendance before the closing bracket
                            lines.insert(end_line, '    "api.apps.attendance.apps.AttendanceConfig",\n')
                            print(f"Added attendance at line {end_line}")
                            break
                break
        break

# Write back
with open('sams/settings/base.py', 'w') as f:
    f.writelines(lines)

print("Updated settings.py")
