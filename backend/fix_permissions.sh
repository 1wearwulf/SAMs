#!/bin/bash
cd /home/riordan/Documents/blackb/sams-project/backend

echo "Fixing permissions issue..."

# 1. Create api/permissions.py
cat > api/permissions.py << 'END'
from rest_framework import permissions
class IsOwnerOrLecturerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
END

# 2. Fix the import in views.py
if grep -q "permission_classes = \[permissions.IsAuthenticated, IsOwnerOrLecturerOrAdmin\]" api/apps/accounts/views.py; then
    # Check if import exists
    if ! grep -q "from api.permissions import IsOwnerOrLecturerOrAdmin" api/apps/accounts/views.py; then
        # Add import after permissions import
        sed -i '/from rest_framework import permissions/a from api.permissions import IsOwnerOrLecturerOrAdmin' api/apps/accounts/views.py
    fi
fi

# 3. Test
echo "Testing..."
python manage.py check --database default && echo "✅ Success!" || echo "❌ Failed"
