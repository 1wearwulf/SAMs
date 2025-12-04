#!/bin/bash

echo "🚀 Starting SAMS (Student Attendance Management System)"
echo "=================================================="

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use. Please stop the service using that port first."
        return 1
    fi
    return 0
}

# Function to start backend
start_backend() {
    echo "📡 Starting Django Backend..."
    cd backend
    if [ ! -d ".venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver 8000 &
    BACKEND_PID=$!
    echo "✅ Backend started on http://localhost:8000 (PID: $BACKEND_PID)"
    cd ..
}

# Function to start web dashboard
start_web() {
    echo "🌐 Starting React Web Dashboard..."
    cd web-dashboard
    if [ ! -d "node_modules" ]; then
        echo "Installing dependencies..."
        npm install
    fi
    npm start &
    WEB_PID=$!
    echo "✅ Web Dashboard starting on http://localhost:3000 (PID: $WEB_PID)"
    cd ..
}

# Function to start mobile app (simulator)
start_mobile() {
    echo "📱 Starting Flutter Mobile App..."
    cd mobile-app
    flutter pub get
    flutter run &
    MOBILE_PID=$!
    echo "✅ Mobile App starting (PID: $MOBILE_PID)"
    cd ..
}

# Check ports
echo "🔍 Checking port availability..."
check_port 8000 || exit 1
check_port 3000 || exit 1

# Start services
start_backend
sleep 3
start_web
sleep 5
start_mobile

echo ""
echo "🎉 All services started!"
echo "📡 Backend API: http://localhost:8000"
echo "🌐 Web Dashboard: http://localhost:3000"
echo "📱 Mobile App: Running in simulator"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo '🛑 Stopping all services...'; kill $BACKEND_PID $WEB_PID $MOBILE_PID 2>/dev/null; exit" INT
wait
