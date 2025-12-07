#!/bin/bash
echo "🔧 COMPLETE BACKEND IMPROVEMENTS"
echo "================================"

cd backend

# 1. CREATE MISSING API ENDPOINTS
echo "📡 Creating essential API endpoints..."

# Create test endpoint
cat > api/views/test.py << 'TESTPY'
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def test_api(request):
    return Response({
        'status': 'online',
        'service': 'SAMS Backend',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth/',
            'courses': '/api/courses/',
            'attendance': '/api/attendance/',
            'users': '/api/users/'
        }
    })
TESTPY

# Create auth endpoints
cat > api/views/auth.py << 'AUTHPY'
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
AUTHPY

# 2. UPDATE URLS
echo "🔗 Updating URLs..."
cat > api/urls.py << 'URLSPY'
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import test, auth

urlpatterns = [
    path('test/', test.test_api, name='test-api'),
    path('auth/login/', auth.login, name='login'),
]
URLSPY

# 3. CREATE TEST USER
echo "👤 Creating test user..."
python3 manage.py shell << 'DJANGO'
from django.contrib.auth import get_user_model
User = get_user_model()

# Create test user if not exists
if not User.objects.filter(username='test').exists():
    User.objects.create_user(
        username='test',
        email='test@sams.com',
        password='test123',
        first_name='Test',
        last_name='User'
    )
    print('✅ Test user created: test/test123')
else:
    print('✅ Test user already exists')

# Create admin user if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@sams.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('✅ Admin user created: admin/admin123')
DJANGO

# 4. UPDATE SETTINGS
echo "⚙️  Updating settings..."
# Update CORS
sed -i "s|CORS_ALLOWED_ORIGINS=.*|CORS_ALLOWED_ORIGINS=http://localhost:3000,exp://10.1.34.219:8081,http://10.1.34.219:8081|g" .env

# 5. RUN MIGRATIONS
echo "🔄 Running migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# 6. START BACKEND
echo "🚀 Starting backend..."
python3 manage.py runserver 10.1.34.219:8000 &

echo ""
echo "✅ BACKEND COMPLETED!"
echo "�� API URL: http://10.1.34.219:8000"
echo "🔑 Test login: test/test123"
echo "👑 Admin: admin/admin123"
echo "📱 Ready for mobile app"
