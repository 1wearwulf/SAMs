#!/bin/bash

echo "🔍 Testing SAMS Setup..."
echo "========================"

# Check Redis
echo "1. Checking Redis..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo "   ✅ Redis is running"
    else
        echo "   ⚠️  Redis installed but not running"
        echo "   Run: redis-server --daemonize yes"
    fi
else
    echo "   ❌ Redis not installed"
    echo "   Install: sudo apt-get install redis-server"
fi

# Check Python/Django
echo -e "\n2. Checking Backend..."
cd backend 2>/dev/null
if [ $? -eq 0 ]; then
    if [ -d "venv" ]; then
        echo "   ✅ Python virtual environment exists"
    else
        echo "   ⚠️  Python venv not found"
        echo "   Run: python -m venv venv"
    fi
    
    if [ -f "requirements.txt" ]; then
        echo "   ✅ requirements.txt exists"
    else
        echo "   ❌ requirements.txt missing"
    fi
    
    if [ -f "manage.py" ]; then
        echo "   ✅ Django manage.py exists"
    else
        echo "   ❌ manage.py missing"
    fi
    cd ..
else
    echo "   ❌ Backend directory not found"
fi

# Check React
echo -e "\n3. Checking Frontend..."
cd frontend 2>/dev/null
if [ $? -eq 0 ]; then
    if [ -f "package.json" ]; then
        echo "   ✅ package.json exists"
        
        if [ -d "node_modules" ]; then
            echo "   ✅ node_modules exists"
        else
            echo "   ⚠️  node_modules not found"
            echo "   Run: npm install"
        fi
    else
        echo "   ❌ package.json missing"
    fi
    cd ..
else
    echo "   ❌ Frontend directory not found"
fi

echo -e "\n📋 Summary:"
echo "=========="
echo "Run these commands if anything is missing:"
echo ""
echo "1. Install Redis: sudo apt-get install redis-server"
echo "2. Start Redis: redis-server --daemonize yes"
echo "3. Backend setup:"
echo "   cd backend"
echo "   python -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo "   python manage.py migrate"
echo "4. Frontend setup:"
echo "   cd frontend"
echo "   npm install"
echo "5. Start development:"
echo "   Backend: python manage.py runserver"
echo "   Frontend: npm start"
