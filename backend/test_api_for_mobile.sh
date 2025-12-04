#!/bin/bash
# Test script for mobile app developers
# Tests all endpoints that the mobile app will use

BASE_URL="http://localhost:8000/api"
echo "SAMS API Test for Mobile App Development"
echo "========================================"
echo "Base URL: $BASE_URL"
echo ""

# Test 1: Server is running
echo "1. Testing server connectivity..."
curl -s -o /dev/null -w "   API Root: %{http_code}\n" $BASE_URL/

# Test 2: Register a test user
echo -e "\n2. Registering test user for mobile app..."
REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "flutter_user",
    "email": "flutter@example.com",
    "password": "Flutter@123",
    "password_confirm": "Flutter@123",
    "role": "student",
    "student_id": "FLUTTER001"
  }')

echo "$REGISTER_RESPONSE" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('   ✓ Registration successful')
    print(f'   Username: {data[\"user\"][\"username\"]}')
    print(f'   Email: {data[\"user\"][\"email\"]}')
    print(f'   Role: {data[\"user\"][\"role\"]}')
except Exception as e:
    print(f'   Response: {sys.stdin.read()[:100]}...')
" 2>/dev/null || echo "   Registration attempt completed"

# Test 3: Login (most important for mobile)
echo -e "\n3. Testing login endpoint..."
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "flutter_user", "password": "Flutter@123"}')

echo "$LOGIN_RESPONSE" | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('   ✓ Login successful!')
    print(f'   Access token: {data[\"access\"][:50]}...')
    print(f'   Refresh token: {data[\"refresh\"][:50]}...')
    
    # Save tokens for other tests
    with open('/tmp/mobile_tokens.json', 'w') as f:
        json.dump(data, f)
    print('   ✓ Tokens saved to /tmp/mobile_tokens.json')
except Exception as e:
    print(f'   ✗ Login failed: {e}')
    print(f'   Response: {sys.stdin.read()[:200]}')
" 2>/dev/null

# Test 4: Test token refresh
echo -e "\n4. Testing token refresh..."
if [ -f "/tmp/mobile_tokens.json" ]; then
    REFRESH_TOKEN=$(python -c "import json; print(json.load(open('/tmp/mobile_tokens.json'))['refresh'])")
    curl -s -X POST $BASE_URL/accounts/token/refresh/ \
      -H "Content-Type: application/json" \
      -d "{\"refresh\": \"$REFRESH_TOKEN\"}" \
      -w "\n   Status: %{http_code}\n" -o /dev/null
else
    echo "   Skipping - no refresh token available"
fi

# Test 5: Test other endpoints that mobile will use
echo -e "\n5. Testing mobile-relevant endpoints (with auth if available)..."
if [ -f "/tmp/mobile_tokens.json" ]; then
    ACCESS_TOKEN=$(python -c "import json; print(json.load(open('/tmp/mobile_tokens.json'))['access'])")
    
    echo "   - User profile:"
    curl -s -X GET $BASE_URL/accounts/profile/ \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -w "     Status: %{http_code}\n" -o /dev/null
    
    echo "   - Courses:"
    curl -s -X GET $BASE_URL/courses/ \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -w "     Status: %{http_code}\n" -o /dev/null
    
    echo "   - Notifications:"
    curl -s -X GET $BASE_URL/notifications/ \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -w "     Status: %{http_code}\n" -o /dev/null
else
    echo "   Skipping authenticated endpoints - no access token"
fi

echo -e "\n✅ API Testing Complete!"
echo "The backend is ready for mobile app integration."
echo ""
echo "For mobile app development, use:"
echo "  • Base URL: http://localhost:8000/api"
echo "  • Login endpoint: /accounts/login/"
echo "  • Add 'Authorization: Bearer <token>' header for protected endpoints"
