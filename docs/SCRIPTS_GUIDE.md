# KB Builder - Scripts Guide

Quick reference for managing the KB Builder application.

## 🚀 Available Scripts

### Start Services
```bash
./start.sh
```
Starts both backend and frontend services in the background.

**What it does:**
- Activates Python virtual environment
- Starts backend on http://localhost:8000
- Starts frontend on http://localhost:5173
- Creates log files (backend.log, frontend.log)
- Saves process IDs to .kb-builder.pid

**Output:**
```
=========================================
KB Builder - Starting Services
=========================================

[1/2] Starting Backend...
✓ Backend started (PID: 12345)
  Log: backend.log
  URL: http://localhost:8000

[2/2] Starting Frontend...
✓ Frontend started (PID: 12346)
  Log: frontend.log
  URL: http://localhost:5173

=========================================
✓ All Services Started Successfully!
=========================================

Backend:  http://localhost:8000
Frontend: http://localhost:5173

To stop: ./stop.sh
```

---

### Stop Services
```bash
./stop.sh
```
Stops both backend and frontend services.

**What it does:**
- Reads PIDs from .kb-builder.pid
- Gracefully stops each process
- Force kills if needed
- Cleans up child processes (vite, etc.)
- Removes PID file

**Output:**
```
=========================================
KB Builder - Stopping Services
=========================================

Stopping process 12345...
✓ Process 12345 stopped
Stopping process 12346...
✓ Process 12346 stopped

Cleaning up child processes...
  Stopped vite processes

=========================================
✓ All Services Stopped
=========================================
```

---

### Restart Services
```bash
./restart.sh
```
Stops and then starts both services.

**What it does:**
- Runs ./stop.sh
- Waits 2 seconds
- Runs ./start.sh

---

### Check Status
```bash
./status.sh
```
Shows the current status of all services.

**What it does:**
- Checks if processes are running
- Shows PIDs
- Checks if ports are listening
- Shows recent log entries

**Output:**
```
=========================================
KB Builder - Service Status
=========================================

Backend (Python):
  Status: RUNNING
  PID(s): 12345
  URL: http://localhost:8000
  Port 8000: LISTENING

Frontend (Node/Vite):
  Status: RUNNING
  PID(s): 12346
  URL: http://localhost:5173
  Port 5173: LISTENING

Recent Logs:
  Backend (last 3 lines):
    INFO:     Started server process [12345]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.

  Frontend (last 3 lines):
    VITE v5.4.0  ready in 234 ms
    ➜  Local:   http://localhost:5173/
    ➜  press h + enter to show help

=========================================
✓ All services are running
=========================================

Access the application at: http://localhost:5173
```

---

## 📋 Common Usage

### First Time Setup
```bash
# 1. Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# 2. Setup frontend
cd frontend
npm install --legacy-peer-deps
cd ..

# 3. Start everything
./start.sh
```

### Daily Usage
```bash
# Start
./start.sh

# Check if running
./status.sh

# Stop when done
./stop.sh
```

### Development
```bash
# Start services
./start.sh

# Make changes to code...

# Restart to apply changes
./restart.sh

# Check logs
tail -f backend.log
tail -f frontend.log
```

---

## 📁 Generated Files

### .kb-builder.pid
Contains process IDs of running services.
- Created by: start.sh
- Removed by: stop.sh
- Don't edit manually

### backend.log
Backend (Python/FastAPI) logs.
- View: `cat backend.log`
- Follow: `tail -f backend.log`
- Clear: `> backend.log`

### frontend.log
Frontend (Node/Vite) logs.
- View: `cat frontend.log`
- Follow: `tail -f frontend.log`
- Clear: `> frontend.log`

---

## 🔧 Troubleshooting

### "Services appear to be already running"
```bash
./stop.sh
./start.sh
```

### Services won't start
```bash
# Check logs
cat backend.log
cat frontend.log

# Check status
./status.sh

# Try manual start
cd backend && source venv/bin/activate && python app.py
```

### Port already in use
```bash
# Find what's using the port
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :5173

# Kill the process
kill <PID>

# Or use stop script
./stop.sh
```

### Clean restart
```bash
./stop.sh
rm -f backend.log frontend.log .kb-builder.pid
./start.sh
```

---

## 🎯 Quick Commands

| Command | Description |
|---------|-------------|
| `./start.sh` | Start all services |
| `./stop.sh` | Stop all services |
| `./restart.sh` | Restart all services |
| `./status.sh` | Check service status |
| `tail -f backend.log` | Watch backend logs |
| `tail -f frontend.log` | Watch frontend logs |
| `./stop.sh && ./start.sh` | Clean restart |

---

## 🌐 URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 💡 Tips

1. **Always check status first**
   ```bash
   ./status.sh
   ```

2. **Watch logs during development**
   ```bash
   # Terminal 1
   tail -f backend.log
   
   # Terminal 2
   tail -f frontend.log
   ```

3. **Clean logs periodically**
   ```bash
   > backend.log
   > frontend.log
   ```

4. **Use restart for code changes**
   ```bash
   ./restart.sh
   ```

5. **Stop services when not in use**
   ```bash
   ./stop.sh
   ```

---

## 🚨 Emergency Stop

If scripts don't work:

```bash
# Kill all Python processes running app.py
pkill -f "python.*app.py"

# Kill all vite processes
pkill -f "vite"

# Remove PID file
rm -f .kb-builder.pid
```

---

## 📝 Notes

- Scripts run services in background (daemon mode)
- Logs are written to backend.log and frontend.log
- Services auto-restart on code changes (hot reload)
- Use Ctrl+C in log tail to stop watching logs
- PID file prevents duplicate starts

---

Enjoy using KB Builder! 🎉
