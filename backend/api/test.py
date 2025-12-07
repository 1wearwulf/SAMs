from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def test_api(request):
    return Response({
        'status': 'online',
        'message': 'SAMS Backend is running!',
        'mobile_ready': True,
        'endpoints': {
            'auth': '/api/auth/',
            'courses': '/api/courses/',
            'attendance': '/api/attendance/'
        }
    })
