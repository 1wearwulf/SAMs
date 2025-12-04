#!/bin/bash
cd /home/riordan/Documents/blackb/sams-project/backend

echo "Fixing all choices fields..."

# Common constants that should be used directly
constants="ATTENDANCE_STATUSES COURSE_STATUSES SESSION_STATUSES COURSE_TYPES USER_ROLES ENROLLMENT_STATUSES NOTIFICATION_TYPES DEVICE_TYPES ACADEMIC_YEARS SEMESTERS"

for file in $(find api/apps/ -name "*.py" -type f); do
    echo "Processing $file"
    
    # Fix pattern: choices=[(k, k.title()) for k in CONSTANT]
    for const in $constants; do
        sed -i "s/choices=\[\((k\|v)\), \1\.title()\) for \(k\|v\) in ${const}\]/choices=${const}/g" "$file" 2>/dev/null || true
    done
    
    # Fix pattern: choices=[(k, v) for k, v in CONSTANT] (if CONSTANT is already tuple of tuples)
    for const in $constants; do
        sed -i "s/choices=\[\(k, v\) for k, v in ${const}\]/choices=${const}/g" "$file" 2>/dev/null || true
    done
done

echo "Testing..."
python manage.py check --database default
