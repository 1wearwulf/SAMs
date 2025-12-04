from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'SAMS API is running!',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/swagger/',
            'redoc': '/redoc/',
            'accounts': {
                'login': '/api/accounts/login/',
                'register': '/api/accounts/register/',
                'logout': '/api/accounts/logout/',
                'password_reset': '/api/accounts/password/reset/',
                'password_change': '/api/accounts/password/change/',
                'profile': '/api/accounts/profile/',
            }
        }
    })
