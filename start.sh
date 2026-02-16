#!/bin/bash

# KB Builder - Start Script
# Starts both backend and frontend services

set -e

echo "========================================="
echo "KB Builder - Starting Services"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if services are already running
if [ -f .kb-builder.pid ]; then
    echo -e "${RED}Services appear to be already running!${NC}"
    echo "If this is incorrect, run: ./stop.sh first"
    exit 1
fi

# Create PID file
touch .kb-builder.pid

# Start Backend
echo -e "${BLUE}[1/2] Starting Backend...${NC}"
cd backend

# Determine which Python command to use
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Using existing virtual environment: $VIRTUAL_ENV"
    PYTHON_CMD="python"
elif [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Warning: No virtual environment found, using system Python${NC}"
    PYTHON_CMD="python3"
else
    echo -e "${RED}Python not found!${NC}"
    echo "Please install Python 3.8+ or create a virtual environment"
    cd ..
    rm -f .kb-builder.pid
    exit 1
fi

# Start backend
nohup $PYTHON_CMD app.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID >> ../.kb-builder.pid
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo "  Log: backend.log"
echo "  URL: http://localhost:8000"
cd ..

# Wait a moment for backend to start
sleep 2

# Start Frontend
echo ""
echo -e "${BLUE}[2/2] Starting Frontend...${NC}"
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${RED}Node modules not found!${NC}"
    echo "Installing dependencies..."
    npm install --legacy-peer-deps
fi

# Start frontend
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID >> ../.kb-builder.pid
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo "  Log: frontend.log"
echo "  URL: http://localhost:5173"
cd ..

# Wait for services to be ready
echo ""
echo "Waiting for services to be ready..."
sleep 3

# Check if services are running
if ps -p $BACKEND_PID > /dev/null && ps -p $FRONTEND_PID > /dev/null; then
    echo ""
    echo "========================================="
    echo -e "${GREEN}✓ All Services Started Successfully!${NC}"
    echo "========================================="
    echo ""
    echo "Backend:  http://localhost:8000"
    echo "Frontend: http://localhost:5173"
    echo ""
    echo "Logs:"
    echo "  Backend:  tail -f backend.log"
    echo "  Frontend: tail -f frontend.log"
    echo ""
    echo "To stop: ./stop.sh"
    echo ""
else
    echo ""
    echo -e "${RED}✗ Failed to start services${NC}"
    echo "Check logs for errors:"
    echo "  Backend:  cat backend.log"
    echo "  Frontend: cat frontend.log"
    ./stop.sh
    exit 1
fi
