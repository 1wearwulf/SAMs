"""
Custom permissions for the SAMS API.
"""
from rest_framework import permissions


class IsLecturerOrAdmin(permissions.BasePermission):
    """
    Allows access only to lecturers or admin users.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role in ['lecturer', 'admin'] or request.user.is_staff)
        )


class IsStudentOrLecturerOrAdmin(permissions.BasePermission):
    """
    Allows access to students, lecturers, and admin users.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role in ['student', 'lecturer', 'admin'] or request.user.is_staff)
        )


class IsOwnerOrLecturerOrAdmin(permissions.BasePermission):
    """
    Allows access to object owner, lecturers, and admin users.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is owner of the object
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        
        # Check if user is owner (alternative attribute names)
        if hasattr(obj, 'student') and obj.student == request.user:
            return True
        
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        
        # Allow lecturers and admins
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role in ['lecturer', 'admin'] or request.user.is_staff)
        )


class IsStudent(permissions.BasePermission):
    """
    Allows access only to students.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'student'
        )


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_staff)
        )
