#!/bin/bash

# KB Builder - Stop Script
# Stops both backend and frontend services

echo "========================================="
echo "KB Builder - Stopping Services"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if PID file exists
if [ ! -f .kb-builder.pid ]; then
    echo -e "${YELLOW}No running services found (PID file missing)${NC}"
    echo ""
    echo "Checking for any running processes..."
    
    # Try to find and kill any running processes
    BACKEND_PIDS=$(ps aux | grep "[p]ython.*app.py" | awk '{print $2}')
    FRONTEND_PIDS=$(ps aux | grep "[n]pm run dev" | awk '{print $2}')
    VITE_PIDS=$(ps aux | grep "[v]ite" | awk '{print $2}')
    
    if [ -n "$BACKEND_PIDS" ] || [ -n "$FRONTEND_PIDS" ] || [ -n "$VITE_PIDS" ]; then
        echo "Found running processes, stopping them..."
        [ -n "$BACKEND_PIDS" ] && kill $BACKEND_PIDS 2>/dev/null && echo "  Stopped backend processes"
        [ -n "$FRONTEND_PIDS" ] && kill $FRONTEND_PIDS 2>/dev/null && echo "  Stopped frontend processes"
        [ -n "$VITE_PIDS" ] && kill $VITE_PIDS 2>/dev/null && echo "  Stopped vite processes"
        echo -e "${GREEN}✓ Cleanup complete${NC}"
    else
        echo "No running processes found"
    fi
    exit 0
fi

# Read PIDs from file
PIDS=$(cat .kb-builder.pid)

# Stop each process
for PID in $PIDS; do
    if ps -p $PID > /dev/null 2>&1; then
        echo "Stopping process $PID..."
        kill $PID 2>/dev/null
        
        # Wait for process to stop (max 5 seconds)
        for i in {1..5}; do
            if ! ps -p $PID > /dev/null 2>&1; then
                echo -e "${GREEN}✓ Process $PID stopped${NC}"
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "${YELLOW}Force killing process $PID...${NC}"
            kill -9 $PID 2>/dev/null
        fi
    else
        echo -e "${YELLOW}Process $PID not running${NC}"
    fi
done

# Also kill any child processes (vite, etc.)
echo ""
echo "Cleaning up child processes..."
pkill -f "vite" 2>/dev/null && echo "  Stopped vite processes"
pkill -f "node.*vite" 2>/dev/null

# Remove PID file
rm -f .kb-builder.pid

echo ""
echo "========================================="
echo -e "${GREEN}✓ All Services Stopped${NC}"
echo "========================================="
echo ""
