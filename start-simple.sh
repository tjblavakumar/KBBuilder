#!/bin/bash

# KB Builder - Simple Start Script
# Run this AFTER activating your virtual environment

set -e

echo "========================================="
echo "KB Builder - Starting Services"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${RED}ERROR: Virtual environment not activated!${NC}"
    echo ""
    echo "Please run:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  cd .."
    echo "  ./start-simple.sh"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment detected${NC}"
echo "  $VIRTUAL_ENV"
echo ""

# Check if already running
if [ -f .kb-builder.pid ]; then
    echo -e "${YELLOW}Services may already be running${NC}"
    echo "Run ./stop.sh first if you want to restart"
    exit 1
fi

# Create PID file
touch .kb-builder.pid

# Start Backend
echo -e "${BLUE}[1/2] Starting Backend...${NC}"
cd backend
nohup python app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID >> ../.kb-builder.pid
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
cd ..

sleep 2

# Start Frontend
echo -e "${BLUE}[2/2] Starting Frontend...${NC}"
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID >> ../.kb-builder.pid
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
cd ..

sleep 3

# Check if running
if ps -p $BACKEND_PID > /dev/null && ps -p $FRONTEND_PID > /dev/null; then
    echo ""
    echo "========================================="
    echo -e "${GREEN}✓ All Services Started!${NC}"
    echo "========================================="
    echo ""
    echo "Backend:  http://localhost:8000"
    echo "Frontend: http://localhost:5173"
    echo ""
    echo "Logs:"
    echo "  tail -f backend.log"
    echo "  tail -f frontend.log"
    echo ""
    echo "To stop: ./stop.sh"
else
    echo ""
    echo -e "${RED}✗ Services failed to start${NC}"
    echo "Check logs:"
    echo "  cat backend.log"
    echo "  cat frontend.log"
    ./stop.sh
    exit 1
fi
