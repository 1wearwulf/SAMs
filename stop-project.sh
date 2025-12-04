#!/bin/bash

# SAMS Project Stop Script

echo "========================================="
echo "   Stopping SAMS Project                "
echo "========================================="

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

for service in backend frontend mobile; do
    if [ -f "$service.pid" ]; then
        PID=$(cat "$service.pid")
        if kill -0 $PID 2>/dev/null; then
            echo -e "${YELLOW}Stopping $service (PID: $PID)...${NC}"
            kill $PID
            wait $PID 2>/dev/null || true
            echo -e "${GREEN}$service stopped${NC}"
        else
            echo -e "${YELLOW}$service process not found (PID: $PID)${NC}"
        fi
        rm -f "$service.pid" "$service.log"
    else
        echo -e "${YELLOW}No PID file found for $service${NC}"
    fi
done

echo ""
echo -e "${GREEN}All services stopped${NC}"
