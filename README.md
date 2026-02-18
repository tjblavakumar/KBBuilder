# KB Builder - AI-Powered Knowledge Base with RAG

Build intelligent knowledge bases from PDFs and chat with them using AI. Supports both AWS Bedrock and OpenAI.

## ✨ Features

- 🔍 **PDF Discovery** - Automatically scan websites for PDFs
- 📚 **Knowledge Base Creation** - Build searchable knowledge bases from PDFs
- 🤖 **Dual Provider Support** - Choose between AWS Bedrock or OpenAI
- 💬 **RAG-based Chat** - Ask questions and get contextual answers with source references
- 🗂️ **Multiple KBs** - Create and manage multiple knowledge bases
- 🔄 **Chat History** - Review past conversations (7-day retention)
- ⚡ **Fast Search** - FAISS-powered vector search for quick retrieval

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd KBBuilder
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

cd ..
```

### 3. Frontend Setup

```bash
cd frontend
npm install --legacy-peer-deps
cd ..
```

### 4. Start the Application

```bash
# Make sure you're in the project root with venv activated
./start.sh
```

The application will start:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173

Open your browser to http://localhost:5173

## 📖 Usage

### Creating a Knowledge Base

1. Click "Create New"
2. **Scan for PDFs**: Enter a website URL and click "Scan"
3. **Select PDFs**: Choose which PDFs to include
4. **Configure**:
   - Enter KB name
   - Provider: OpenAI (default) or AWS Bedrock
   - Select model (GPT-4o Mini recommended)
   - For OpenAI: Click `Admin` in the top bar, paste your API key, and save (validated immediately)
5. Click "Build KB" and wait for processing

### Chatting with Your KB

1. Click "Start Chat" on any knowledge base
2. Type your question
3. Get AI-powered answers with source references
4. View which documents and pages were used

## ⚙️ Configuration

### OpenAI Setup (Recommended)

1. **Get API Key**: https://platform.openai.com/api-keys
2. In the app, open **Admin** from the top navigation
3. Paste your API key and click **Save**
4. The key is validated immediately and used for this browser session only

### AWS Bedrock Setup (Optional)

1. Configure AWS SSO
2. Set up AWS credentials
3. Update config.yml:
   ```yaml
   bedrock:
     profile_name: "default"
     region: "us-east-1"
     default_model: "anthropic.claude-3-5-sonnet-20240620-v1:0"
   ```

## 🎮 Scripts

### Start Services
```bash
./start.sh
```

### Stop Services
```bash
./stop.sh
```

### Check Status
```bash
./status.sh
```

### Restart
```bash
./restart.sh
```

### View Logs
```bash
tail -f backend.log
tail -f frontend.log
```

## 🔧 Available Models

### OpenAI Models
- **GPT-4o** - Latest, most capable (~$2.50/1M tokens)
- **GPT-4o Mini** - Cost-effective, fast (~$0.15/1M tokens) ⭐ Recommended
- **GPT-4 Turbo** - Previous generation (~$10/1M tokens)
- **GPT-3.5 Turbo** - Fast and economical (~$0.50/1M tokens)

### AWS Bedrock Models
- **Claude 3.5 Sonnet** - Anthropic's latest
- **Claude 3 Opus** - Most capable
- **Claude 3 Sonnet** - Balanced performance

## 💰 Cost Comparison

### Typical Usage (100 pages, 10 chats/day)

| Provider | Model | Setup | Monthly | Total/Month |
|----------|-------|-------|---------|-------------|
| OpenAI | GPT-4o Mini | $0.002 | $0.10 | **$0.10** ⭐ |
| OpenAI | GPT-4o | $0.002 | $2.00 | $2.00 |
| Bedrock | Claude 3.5 | $0.01 | $0.30 | $0.31 |

## 🏗️ Architecture

```
Frontend (Vue.js) → Backend (FastAPI) → LLM Provider
                                        ├─ OpenAI
                                        └─ AWS Bedrock
```

- **Frontend**: Vue 3 + Vite
- **Backend**: FastAPI + SQLAlchemy
- **Vector DB**: FAISS
- **Text Processing**: LangChain
- **Embeddings**: OpenAI text-embedding-3-small or AWS Titan

## 🐛 Troubleshooting

### "API key is required"
- Open **Admin** in the top bar
- Paste your OpenAI API key and click **Save**

### "Incorrect API key provided"
- Verify your API key at https://platform.openai.com/api-keys
- Check you have credits in your account
- Make sure you copied the entire key

### Services won't start
```bash
./stop.sh
cd backend
pip install -r requirements.txt
cd ..
./start.sh
```

### Frontend errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
cd ..
./restart.sh
```

### Check logs for errors
```bash
cat backend.log
cat frontend.log
```

## 📚 Documentation

- [Architecture Details](docs/ARCHITECTURE_DIAGRAM.md)
- [Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)
- [Setup Checklist](docs/SETUP_CHECKLIST.md)
- [Troubleshooting Guide](docs/FIX_IMPORT_ERROR.md)

## 🔐 Security Notes

⚠️ **Important**:
- OpenAI API keys are session-only in memory (entered via **Admin**)
- New keys are not persisted to database or config by the app
- Session key is cleared when browser tab/app is refreshed or closed
- For production:
  - Add TLS/HTTPS between browser and backend
  - Use a secure server-side secrets manager if persistent credentials are needed
  - Use environment variables
  - Implement key rotation
  - Add audit logging

## 🤝 Contributing

Contributions welcome! The provider abstraction makes it easy to add new LLM providers.

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- AWS Bedrock for Claude models
- OpenAI for GPT models
- FastAPI for backend framework
- Vue.js for frontend framework
- FAISS for vector search
- LangChain for text processing

---

**Built with ❤️ for AI-powered knowledge management**
