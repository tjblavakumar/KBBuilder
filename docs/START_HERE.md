# 🚀 Quick Start - KB Builder

## One-Command Start

```bash
./start.sh
```

That's it! Both backend and frontend will start automatically.

## Access the Application

Open your browser: **http://localhost:5173**

## Stop Everything

```bash
./stop.sh
```

## Check Status

```bash
./status.sh
```

## First Time Setup

If this is your first time:

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

# 3. Start!
./start.sh
```

## Available Commands

| Command | What it does |
|---------|--------------|
| `./start.sh` | Start both services |
| `./stop.sh` | Stop both services |
| `./restart.sh` | Restart both services |
| `./status.sh` | Check if running |

## View Logs

```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log
```

## Troubleshooting

**Services won't start?**
```bash
./stop.sh
./start.sh
```

**Check what's wrong:**
```bash
./status.sh
cat backend.log
cat frontend.log
```

## More Info

- Full guide: [SCRIPTS_GUIDE.md](SCRIPTS_GUIDE.md)
- OpenAI setup: [QUICKSTART_OPENAI.md](QUICKSTART_OPENAI.md)
- Main README: [README.md](README.md)

---

**Happy building!** 🎉
