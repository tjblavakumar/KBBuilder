@echo off
echo Starting Cleanup Scheduler...
echo This will run daily at 2:00 AM to cleanup old chat history
echo Press Ctrl+C to stop
echo.

call venv\Scripts\activate.bat
python cleanup_scheduler.py
