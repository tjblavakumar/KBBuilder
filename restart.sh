#!/bin/bash

# KB Builder - Restart Script
# Restarts both backend and frontend services

echo "========================================="
echo "KB Builder - Restarting Services"
echo "========================================="
echo ""

# Stop services
./stop.sh

# Wait a moment
sleep 2

# Start services
./start.sh
