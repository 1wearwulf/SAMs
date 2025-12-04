#!/bin/bash

echo "🚀 Starting SAMS Development Environment..."
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a service is running
check_service() {
    if pgrep -f "$1" > /dev/null; then
        echo -e "${GREEN}✓${NC} $2 is running"
        return 0
    else
        echo -e "${RED}✗${NC} $2 is not running"
        return 1
    fi
}

# Function to start service in background
start_service() {
    echo -e "${BLUE}▶${NC} Starting $2..."
    $1 &
    sleep 2
    check_service "$3" "$2"
}

# Kill any existing services
echo -e "\n${YELLOW}Stopping existing services...${NC}"
pkill -f "redis-server" 2>/dev/null || true
pkill -f "python manage.py runserver" 2>/dev/null || true
pkill -f "npm start" 2>/dev/null || true

# Start Redis
echo -e "\n${YELLOW}Starting services...${NC}"
if ! check_service "redis-server" "Redis"; then
    echo -e "${BLUE}▶${NC} Starting Redis..."
    redis-server --daemonize yes
    sleep 1
    check_service "redis-server" "Redis"
fi

# Start Django backend
cd backend
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')" >> .env
fi

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run migrations
echo -e "\n${YELLOW}Running database migrations...${NC}"
python manage.py migrate

# Create superuser if not exists
echo -e "\n${YELLOW}Checking superuser...${NC}"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Created admin user: admin@example.com / admin123')
else:
    print('Admin user already exists')
"

# Create test users
echo -e "\n${YELLOW}Creating test users...${NC}"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

# Create test student
if not User.objects.filter(email='student@test.com').exists():
    User.objects.create_user(
        email='student@test.com',
        password='password123',
        first_name='John',
        last_name='Doe',
        role='student'
    )
    print('Created student: student@test.com / password123')

# Create test lecturer
if not User.objects.filter(email='lecturer@test.com').exists():
    User.objects.create_user(
        email='lecturer@test.com',
        password='password123',
        first_name='Jane',
        last_name='Smith',
        role='lecturer'
    )
    print('Created lecturer: lecturer@test.com / password123')
"

# Start Django server
echo -e "\n${YELLOW}Starting Django backend...${NC}"
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!
sleep 3
check_service "manage.py runserver" "Django Backend"

# Start React frontend
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo -e "\n${YELLOW}Installing React dependencies...${NC}"
    npm install
fi

echo -e "\n${YELLOW}Starting React frontend...${NC}"
npm start &
REACT_PID=$!
sleep 5
check_service "npm start" "React Frontend"

# Show summary
echo -e "\n${GREEN}==========================================${NC}"
echo -e "${GREEN}🚀 SAMS Development Environment Ready!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo -e "\n${BLUE}Access Points:${NC}"
echo -e "  Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "  Backend API: ${GREEN}http://localhost:8000/api/${NC}"
echo -e "  Admin Panel: ${GREEN}http://localhost:8000/admin/${NC}"
echo -e "\n${BLUE}Test Credentials:${NC}"
echo -e "  Admin: ${YELLOW}admin@example.com / admin123${NC}"
echo -e "  Student: ${YELLOW}student@test.com / password123${NC}"
echo -e "  Lecturer: ${YELLOW}lecturer@test.com / password123${NC}"
echo -e "\n${BLUE}Redis Status:${NC}"
redis-cli ping
echo -e "\n${YELLOW}Press Ctrl+C to stop all services${NC}"

# Wait for Ctrl+C
trap "echo -e '\n${YELLOW}Stopping services...${NC}'; kill $DJANGO_PID $REACT_PID 2>/dev/null; pkill -f redis-server 2>/dev/null; echo -e '${GREEN}Services stopped.${NC}'; exit" INT
wait
