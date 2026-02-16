#!/bin/bash

# KB Builder - Status Script
# Check status of backend and frontend services

echo "========================================="
echo "KB Builder - Service Status"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if PID file exists
if [ ! -f .kb-builder.pid ]; then
    echo -e "${YELLOW}PID file not found${NC}"
    echo ""
fi

# Check Backend
echo "Backend (Python):"
BACKEND_PIDS=$(ps aux | grep "[p]ython.*app.py" | awk '{print $2}')
if [ -n "$BACKEND_PIDS" ]; then
    echo -e "  Status: ${GREEN}RUNNING${NC}"
    echo "  PID(s): $BACKEND_PIDS"
    echo "  URL: http://localhost:8000"
    
    # Check if port is listening
    if command -v netstat &> /dev/null; then
        if netstat -tuln | grep -q ":8000 "; then
            echo -e "  Port 8000: ${GREEN}LISTENING${NC}"
        else
            echo -e "  Port 8000: ${RED}NOT LISTENING${NC}"
        fi
    fi
else
    echo -e "  Status: ${RED}NOT RUNNING${NC}"
fi

echo ""

# Check Frontend
echo "Frontend (Node/Vite):"
FRONTEND_PIDS=$(ps aux | grep "[v]ite" | awk '{print $2}')
if [ -n "$FRONTEND_PIDS" ]; then
    echo -e "  Status: ${GREEN}RUNNING${NC}"
    echo "  PID(s): $FRONTEND_PIDS"
    echo "  URL: http://localhost:5173"
    
    # Check if port is listening
    if command -v netstat &> /dev/null; then
        if netstat -tuln | grep -q ":5173 "; then
            echo -e "  Port 5173: ${GREEN}LISTENING${NC}"
        else
            echo -e "  Port 5173: ${RED}NOT LISTENING${NC}"
        fi
    fi
else
    echo -e "  Status: ${RED}NOT RUNNING${NC}"
fi

echo ""

# Check logs
echo "Recent Logs:"
if [ -f backend.log ]; then
    echo "  Backend (last 3 lines):"
    tail -n 3 backend.log | sed 's/^/    /'
else
    echo "  Backend: No log file"
fi

echo ""

if [ -f frontend.log ]; then
    echo "  Frontend (last 3 lines):"
    tail -n 3 frontend.log | sed 's/^/    /'
else
    echo "  Frontend: No log file"
fi

echo ""
echo "========================================="

# Overall status
if [ -n "$BACKEND_PIDS" ] && [ -n "$FRONTEND_PIDS" ]; then
    echo -e "${GREEN}✓ All services are running${NC}"
    echo ""
    echo "Access the application at: http://localhost:5173"
elif [ -n "$BACKEND_PIDS" ] || [ -n "$FRONTEND_PIDS" ]; then
    echo -e "${YELLOW}⚠ Some services are running${NC}"
    echo ""
    echo "Run './start.sh' to start all services"
else
    echo -e "${RED}✗ No services are running${NC}"
    echo ""
    echo "Run './start.sh' to start services"
fi

echo ""
