# Quick Start: Using OpenAI with KB Builder

Get up and running with OpenAI in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Step 1: Update Backend

```bash
cd backend

# Activate virtual environment
# Windows:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install OpenAI package
pip install openai==1.54.0

# Run migration (if you have existing database)
python migrate_db.py
```

## Step 2: Start Backend

```bash
# Still in backend directory
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 3: Start Frontend

Open a new terminal:

```bash
cd frontend
npm run dev
```

You should see:
```
VITE ready in XXX ms
Local: http://localhost:5173/
```

## Step 4: Set Session API Key (Admin)

1. **Open browser**: Navigate to `http://localhost:5173`

2. Click **Admin** in the top navigation

3. Paste OpenAI API key: `sk-...`

4. Click **Save** and wait for validation success

5. Confirm top nav shows **OpenAI Ready**

## Step 5: Create Your First OpenAI Knowledge Base

1. **Click "+ New KB"**

2. **Step 1 - Discover PDFs**:
   - Enter a website URL with PDFs
   - Click "Scan"
   - Select the PDFs you want
   - Click "Next"

3. **Step 2 - Configure**:
   - Enter a name: "My OpenAI KB"
   - Select Provider: **OpenAI**
   - Use session key from Admin (no API key field required)
   - Select Model: **GPT-4o Mini** (recommended for cost)
   - Click "Build KB"

4. **Wait for processing** (may take 1-2 minutes)

5. **Start chatting!**

## Step 6: Test It Out

Try these questions:
- "What is this document about?"
- "Summarize the main points"
- "What does it say about [specific topic]?"

## Troubleshooting

### "OpenAI API key required for this session"
→ Open **Admin** and set your key again for this session

### "OpenAI API key is invalid"
→ Check your API key is valid and has credits

### "Failed to generate embedding"
→ Ensure your API key has access to embeddings API

### Backend won't start
→ Make sure you installed the openai package:
```bash
pip install openai==1.54.0
```

## Cost Estimate

For a typical knowledge base with 100 pages:

- **Embeddings**: ~$0.004
- **10 chat messages**: ~$0.01
- **Total**: Less than $0.02

Using GPT-4o Mini is very cost-effective!

## Switching Between Providers

You can have multiple knowledge bases with different providers:

- KB 1: AWS Bedrock (Claude 3.5 Sonnet)
- KB 2: OpenAI (GPT-4o Mini)
- KB 3: OpenAI (GPT-4o)

Each KB remembers its provider and settings.

## Next Steps

- Read [OPENAI_INTEGRATION.md](OPENAI_INTEGRATION.md) for detailed docs
- Check [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
- Explore different models and compare results

## Getting Help

- Check the main [README.md](README.md)
- Review error messages in browser console (F12)
- Check backend logs in terminal

## Security Reminder

🔒 OpenAI key is session-only in browser memory in this flow (not persisted by new requests). For production use:
- Use HTTPS/TLS
- Use server-side secret management if persistence is required
- Never commit API keys to git

---

Happy chatting! 🚀
