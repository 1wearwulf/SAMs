"""
Device check middleware for validating device fingerprints.
"""

import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from utils.device_fingerprint import get_request_fingerprint
from django.core.cache import cache

logger = logging.getLogger(__name__)


class DeviceCheckMiddleware(MiddlewareMixin):
    """
    Middleware to check device consistency and prevent suspicious activity.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip device check for certain paths
        exempt_paths = [
            '/admin/',
            '/api/auth/',
            '/static/',
            '/media/',
        ]

        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)

        # Get current device fingerprint
        current_fingerprint = get_request_fingerprint(request)

        # Get user if authenticated
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            # Check device consistency for authenticated users
            device_check = self._check_user_device_consistency(user.id, current_fingerprint)

            if not device_check['is_valid']:
                logger.warning(
                    f'Device mismatch for user {user.username} (ID: {user.id}): {device_check["message"]}'
                )

                # For API requests, return error response
                if request.path.startswith('/api/'):
                    return JsonResponse({
                        'error': 'Device validation failed',
                        'message': device_check['message']
                    }, status=403)

                # For web requests, could redirect to verification page
                # For now, just log and continue

        # Store device fingerprint in request for later use
        request.device_fingerprint = current_fingerprint

        response = self.get_response(request)
        return response

    def _check_user_device_consistency(self, user_id: int, current_fingerprint: str) -> dict:
        """
        Check if current device fingerprint is consistent with user's device history.
        """
        # Get user's recent device fingerprints from cache
        cache_key = f"user_devices_{user_id}"
        recent_devices = cache.get(cache_key, [])

        if not recent_devices:
            # First device, consider valid and store it
            recent_devices.append(current_fingerprint)
            cache.set(cache_key, recent_devices, timeout=86400 * 30)  # 30 days
            return {'is_valid': True, 'message': 'First device registration'}

        # Check if current fingerprint matches recent ones
        if current_fingerprint in recent_devices:
            return {'is_valid': True, 'message': 'Device fingerprint matches history'}
        else:
            # Add to recent devices (limit to 5)
            recent_devices.append(current_fingerprint)
            recent_devices = recent_devices[-5:]
            cache.set(cache_key, recent_devices, timeout=86400 * 30)

            return {
                'is_valid': False,
                'message': f'Device fingerprint mismatch. Known devices: {len(recent_devices)}'
            }
