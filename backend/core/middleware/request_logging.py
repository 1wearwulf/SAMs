"""
Middleware for logging HTTP requests.
"""

import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log incoming HTTP requests and responses.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        start_time = time.time()

        # Get user info if authenticated
        user_info = 'Anonymous'
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_info = f'User: {request.user.username} (ID: {request.user.id})'

        # Log request
        logger.info(
            f'[{request.method}] {request.path} - {user_info} - '
            f'IP: {self._get_client_ip(request)} - '
            f'User-Agent: {request.META.get("HTTP_USER_AGENT", "Unknown")}'
        )

        # Process request
        response = self.get_response(request)

        # Calculate response time
        duration = time.time() - start_time

        # Log response
        logger.info(
            f'[{request.method}] {request.path} - Status: {response.status_code} - '
            f'Duration: {duration:.2f}s'
        )

        return response

    def _get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
