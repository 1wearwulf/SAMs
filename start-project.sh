#!/bin/bash

# SAMS Project Start Script
# Starts all services: Backend, Frontend, and Mobile

set -e  # Exit on error

echo "========================================="
echo "   Starting SAMS Project                "
echo "   Student Attendance Management System "
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if required commands are available
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}Error: $1 is not installed${NC}"
        exit 1
    fi
}

echo -e "${BLUE}Checking dependencies...${NC}"
check_command node
check_command npm
check_command python3

# Function to start a service
start_service() {
    local service_name=$1
    local service_dir=$2
    local start_command=$3
    
    echo -e "${YELLOW}Starting $service_name...${NC}"
    
    if [ ! -d "$service_dir" ]; then
        echo -e "${RED}Error: $service_name directory not found: $service_dir${NC}"
        return 1
    fi
    
    cd "$service_dir"
    
    # Check if node_modules exists, install if not
    if [ -f "package.json" ] && [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}Installing $service_name dependencies...${NC}"
        npm install
    fi
    
    # Start the service in background
    if [ "$start_command" = "npm run dev" ]; then
        # For React apps, we need to run in background and capture PID
        $start_command > "$service_name.log" 2>&1 &
        PID=$!
        echo $PID > "$service_name.pid"
        echo -e "${GREEN}$service_name started (PID: $PID)${NC}"
        echo -e "${BLUE}Logs: $service_dir/$service_name.log${NC}"
    else
        # For Python backend
        $start_command &
        PID=$!
        echo $PID > "$service_name.pid"
        echo -e "${GREEN}$service_name started (PID: $PID)${NC}"
    fi
    
    cd - > /dev/null
}

# Kill any existing processes
echo -e "${BLUE}Cleaning up old processes...${NC}"
for service in backend frontend mobile; do
    if [ -f "$service.pid" ]; then
        PID=$(cat "$service.pid")
        if kill -0 $PID 2>/dev/null; then
            echo -e "${YELLOW}Stopping existing $service process (PID: $PID)...${NC}"
            kill $PID
        fi
        rm -f "$service.pid" "$service.log"
    fi
done

# Start services in order
echo ""
echo -e "${BLUE}Starting services...${NC}"

# 1. Start Backend (FastAPI)
if [ -d "backend" ]; then
    start_service "backend" "backend" "python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
else
    echo -e "${YELLOW}Backend directory not found, skipping...${NC}"
fi

# 2. Start Web Frontend (React)
if [ -d "frontend" ]; then
    start_service "frontend" "frontend" "npm run dev"
else
    echo -e "${YELLOW}Frontend directory not found, skipping...${NC}"
fi

# 3. Start Mobile (React Native/Expo)
if [ -d "mobile" ]; then
    start_service "mobile" "mobile" "npm start"
else
    echo -e "${YELLOW}Mobile directory not found, skipping...${NC}"
fi

# Function to stop all services
stop_services() {
    echo ""
    echo -e "${RED}Stopping all services...${NC}"
    for service in backend frontend mobile; do
        if [ -f "$service.pid" ]; then
            PID=$(cat "$service.pid")
            if kill -0 $PID 2>/dev/null; then
                echo -e "${YELLOW}Stopping $service (PID: $PID)...${NC}"
                kill $PID
                wait $PID 2>/dev/null || true
            fi
            rm -f "$service.pid" "$service.log"
        fi
    done
    echo -e "${GREEN}All services stopped${NC}"
    exit 0
}

# Trap Ctrl+C to stop services
trap stop_services INT

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}All services started successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${BLUE}Access URLs:${NC}"
echo -e "Backend API:    ${GREEN}http://localhost:8000${NC}"
echo -e "Backend Docs:   ${GREEN}http://localhost:8000/docs${NC}"
echo -e "Frontend:       ${GREEN}http://localhost:3000${NC}"
echo -e "Mobile Expo:    ${GREEN}http://localhost:8081${NC}"
echo -e "Mobile QR Code: ${YELLOW}Check terminal where mobile service started${NC}"
echo ""
echo -e "${BLUE}To stop all services:${NC}"
echo -e "1. Press ${RED}Ctrl+C${NC} in this terminal"
echo -e "2. Or run: ${YELLOW}./stop-project.sh${NC}"
echo ""
echo -e "${BLUE}Log files:${NC}"
echo -e "Backend logs:  ${YELLOW}tail -f backend/backend.log${NC}"
echo -e "Frontend logs: ${YELLOW}tail -f frontend/frontend.log${NC}"
echo -e "Mobile logs:   ${YELLOW}tail -f mobile/mobile.log${NC}"
echo ""

# Keep script running
echo -e "${BLUE}Monitoring services... (Press Ctrl+C to stop)${NC}"
wait
