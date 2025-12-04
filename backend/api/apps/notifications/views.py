"""
Views for the notifications app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer
from api.permissions import IsOwnerOrLecturerOrAdmin


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrLecturerOrAdmin]
    
    def get_queryset(self):
        """Return notifications for the current user."""
        user = self.request.user
        return Notification.objects.filter(user=user).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read for the current user."""
        queryset = self.get_queryset().filter(is_read=False)
        updated = queryset.update(is_read=True)
        return Response({'marked_read': updated})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a specific notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})
