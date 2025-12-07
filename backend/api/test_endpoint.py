from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_api(request):
    return JsonResponse({
        'status': 'online',
        'service': 'SAMS Backend',
        'version': '1.0.0',
        'endpoints': {
            'test': '/api/test/',
            'auth': '/api/auth/login/'
        }
    })
