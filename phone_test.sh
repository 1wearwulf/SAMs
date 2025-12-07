#!/bin/bash
echo "📱 Phone Testing Setup..."

# 1. Update API URL in mobile
cd ~/Documents/blackb/sams-project/mobile
API_FILE=$(find app/ -name "*.ts" -o -name "*.tsx" -o -name "*.js" | xargs grep -l "localhost:8000" | head -1)
if [ -n "$API_FILE" ]; then
    sed -i "s/localhost:8000/10.1.34.219:8000/g" "$API_FILE"
    echo "✅ Updated API in: $API_FILE"
fi

# 2. Check backend
echo "🌐 Backend URL: http://10.1.34.219:8000"
curl -s --connect-timeout 5 http://10.1.34.219:8000 > /dev/null && echo "✅ Backend accessible" || echo "❌ Backend not reachable"

# 3. Show connection info
echo ""
echo "========================================="
echo "   PHONE TESTING INSTRUCTIONS           "
echo "========================================="
echo ""
echo "📱 On your phone:"
echo "1. Connect to same WiFi (10.1.34.x)"
echo "2. Install 'Expo Go' app"
echo "3. Scan QR code from mobile terminal"
echo ""
echo "🔗 Or enter manually in Expo Go:"
echo "   exp://10.1.34.219:8081"
echo ""
echo "🔧 If connection fails:"
echo "1. Check phone WiFi IP: Should be 10.1.34.x"
echo "2. On phone browser, visit: http://10.1.34.219:8000"
echo "3. Should see Django page"
echo ""
echo "🔄 Restart mobile after API URL change:"
echo "   cd ~/Documents/blackb/sams-project"
echo "   ./stop-project.sh"
echo "   ./start-project.sh"
