import sys
sys.path.insert(0, '.')

# Read base.py
with open('sams/settings/base.py', 'r') as f:
    lines = f.readlines()

# Find and replace DEBUG and ALLOWED_HOSTS
new_lines = []
for line in lines:
    if line.strip().startswith('DEBUG ='):
        new_lines.append('DEBUG = True\n')
    elif line.strip().startswith('ALLOWED_HOSTS ='):
        new_lines.append("ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '*']\n")
    else:
        new_lines.append(line)

# Write back
with open('sams/settings/base.py', 'w') as f:
    f.writelines(new_lines)

print("Fixed base.py")
