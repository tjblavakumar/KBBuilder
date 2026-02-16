# Architecture Diagram - OpenAI Integration

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│                     http://localhost:5173                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST API
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      FRONTEND (Vue.js)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  HomeView    │  │ CreateKBView │  │  ChatView    │         │
│  │              │  │              │  │              │         │
│  │ - List KBs   │  │ - Provider   │  │ - Chat UI    │         │
│  │ - Show       │  │   Selection  │  │ - Sources    │         │
│  │   Provider   │  │ - API Key    │  │ - History    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                  │                  │
│         └─────────────────┼──────────────────┘                  │
│                           │                                     │
│                  ┌────────▼────────┐                           │
│                  │   API Service   │                           │
│                  │   (api.js)      │                           │
│                  └────────┬────────┘                           │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            │ HTTP/REST
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│                  http://localhost:8000                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                        │  │
│  │                                                         │  │
│  │  GET  /api/bedrock/models                              │  │
│  │  GET  /api/openai/models        ← NEW                  │  │
│  │  POST /api/kb                   (provider, api_key)    │  │
│  │  POST /api/kb/{id}/chat         (uses provider)        │  │
│  │  GET  /api/kb                   (shows provider)       │  │
│  └────────────────────┬────────────────────────────────────┘  │
│                       │                                        │
│  ┌────────────────────▼────────────────────────────────────┐  │
│  │                  Service Layer                          │  │
│  │                                                         │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐  │  │
│  │  │ ChatService  │  │ Embeddings   │  │ PDF         │  │  │
│  │  │              │  │ Service      │  │ Processor   │  │  │
│  │  │ - Uses       │  │ - Uses       │  │             │  │  │
│  │  │   Provider   │  │   Provider   │  │             │  │  │
│  │  └──────┬───────┘  └──────┬───────┘  └─────────────┘  │  │
│  │         │                 │                            │  │
│  │         └────────┬────────┘                            │  │
│  │                  │                                     │  │
│  │         ┌────────▼────────┐                           │  │
│  │         │  LLMProvider    │  ← NEW (Abstraction)      │  │
│  │         │  (Interface)    │                           │  │
│  │         └────────┬────────┘                           │  │
│  │                  │                                     │  │
│  │         ┌────────┴────────┐                           │  │
│  │         │                 │                           │  │
│  │  ┌──────▼──────┐   ┌──────▼──────┐                   │  │
│  │  │  Bedrock    │   │   OpenAI    │  ← NEW            │  │
│  │  │  Provider   │   │   Provider  │                   │  │
│  │  │             │   │             │                   │  │
│  │  │ - Chat      │   │ - Chat      │                   │  │
│  │  │ - Embeddings│   │ - Embeddings│                   │  │
│  │  └──────┬──────┘   └──────┬──────┘                   │  │
│  └─────────┼─────────────────┼──────────────────────────┘  │
│            │                 │                              │
│  ┌─────────▼─────────────────▼──────────────────────────┐  │
│  │              Database (SQLite)                       │  │
│  │                                                      │  │
│  │  KnowledgeBase:                                     │  │
│  │    - id                                             │  │
│  │    - name                                           │  │
│  │    - model_id                                       │  │
│  │    - provider      ← NEW                           │  │
│  │    - api_key       ← NEW                           │  │
│  │    - created_at                                     │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
┌───────▼────────┐                 ┌────────▼────────┐
│  AWS Bedrock   │                 │     OpenAI      │
│                │                 │                 │
│ - Claude 3.5   │                 │ - GPT-4o        │
│ - Claude 3     │                 │ - GPT-4o Mini   │
│ - Titan Embed  │                 │ - GPT-4 Turbo   │
│                │                 │ - text-embed-3  │
└────────────────┘                 └─────────────────┘
```

## Data Flow: Creating a Knowledge Base

```
1. User Input
   ↓
   [Frontend: CreateKBView]
   - Select Provider (Bedrock/OpenAI)
   - Enter API Key (if OpenAI)
   - Select Model
   - Choose Documents
   ↓
2. API Request
   ↓
   POST /api/kb
   {
     "name": "My KB",
     "provider": "openai",
     "api_key": "sk-...",
     "model_id": "gpt-4o-mini",
     "documents": [...]
   }
   ↓
3. Backend Processing
   ↓
   [app.py]
   - Validate provider & API key
   - Create KB record in database
   ↓
   [PDFProcessor]
   - Download PDFs
   - Extract text
   ↓
   [EmbeddingsService]
   - Get provider (OpenAI/Bedrock)
   - Chunk text
   - Generate embeddings via provider
   - Store in FAISS
   ↓
4. Response
   ↓
   {
     "id": 1,
     "status": "success",
     "message": "KB created"
   }
```

## Data Flow: Chatting with Knowledge Base

```
1. User Message
   ↓
   [Frontend: ChatView]
   - User types question
   ↓
2. API Request
   ↓
   POST /api/kb/{id}/chat
   {
     "message": "What is...?"
   }
   ↓
3. Backend Processing
   ↓
   [app.py]
   - Get KB from database
   - Extract provider & api_key
   ↓
   [ChatService]
   - Initialize with provider
   ↓
   [EmbeddingsService]
   - Generate query embedding
   - Search FAISS for relevant chunks
   ↓
   [LLMProvider]
   - Build prompt with context
   - Call appropriate provider
     ├─ BedrockProvider → AWS Bedrock
     └─ OpenAIProvider → OpenAI API
   ↓
   [ChatService]
   - Extract sources
   - Format response
   ↓
4. Response
   ↓
   {
     "response": "Based on the context...",
     "sources": [...]
   }
   ↓
5. Display
   ↓
   [Frontend: ChatView]
   - Show response
   - Show sources
   - Add to history
```

## Provider Abstraction Layer

```
┌─────────────────────────────────────────┐
│         LLMProvider (Abstract)          │
│                                         │
│  + generate_chat_response(prompt)      │
│  + generate_embedding(text)            │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐   ┌──────▼────────┐
│   Bedrock    │   │    OpenAI     │
│   Provider   │   │    Provider   │
├──────────────┤   ├───────────────┤
│              │   │               │
│ __init__:    │   │ __init__:     │
│  - boto3     │   │  - OpenAI()   │
│  - session   │   │  - api_key    │
│              │   │               │
│ chat:        │   │ chat:         │
│  - Claude    │   │  - GPT models │
│    format    │   │    format     │
│  - invoke_   │   │  - client.    │
│    model()   │   │    chat.      │
│              │   │    create()   │
│              │   │               │
│ embedding:   │   │ embedding:    │
│  - Titan     │   │  - text-      │
│    Embed     │   │    embedding  │
│              │   │    -3-small   │
└──────────────┘   └───────────────┘
```

## Database Schema

```
┌─────────────────────────────────────┐
│        KnowledgeBase Table          │
├─────────────────────────────────────┤
│ id              INTEGER PRIMARY KEY │
│ name            VARCHAR(255)        │
│ model_id        VARCHAR(255)        │
│ provider        VARCHAR(50)  ← NEW  │
│ api_key         VARCHAR(500) ← NEW  │
│ created_at      DATETIME            │
│ updated_at      DATETIME            │
└─────────────────┬───────────────────┘
                  │
                  │ 1:N
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌───────▼────────┐
│   Documents    │  │  ChatHistory   │
├────────────────┤  ├────────────────┤
│ id             │  │ id             │
│ kb_id          │  │ kb_id          │
│ filename       │  │ user_message   │
│ url            │  │ bot_response   │
│ page_count     │  │ timestamp      │
│ status         │  └────────────────┘
└────────────────┘
```

## File Structure

```
project/
├── backend/
│   ├── services/
│   │   ├── llm_provider.py      ← NEW (Abstraction)
│   │   ├── openai_client.py     ← NEW (OpenAI models)
│   │   ├── bedrock_client.py    (Existing)
│   │   ├── chat.py              (Modified)
│   │   ├── embeddings.py        (Modified)
│   │   ├── pdf_processor.py     (Unchanged)
│   │   └── scraper.py           (Unchanged)
│   ├── app.py                   (Modified)
│   ├── database.py              (Modified)
│   ├── models.py                (Modified)
│   ├── migrate_db.py            ← NEW
│   ├── test_openai.py           ← NEW
│   └── requirements.txt         (Modified)
│
├── frontend/
│   └── src/
│       ├── views/
│       │   ├── CreateKBView.vue (Modified)
│       │   ├── HomeView.vue     (Modified)
│       │   └── ChatView.vue     (Unchanged)
│       └── services/
│           └── api.js           (Modified)
│
└── docs/
    ├── OPENAI_INTEGRATION.md
    ├── QUICKSTART_OPENAI.md
    ├── PROVIDER_COMPARISON.md
    ├── IMPLEMENTATION_SUMMARY.md
    ├── SETUP_CHECKLIST.md
    └── ARCHITECTURE_DIAGRAM.md  (This file)
```

## Component Interaction Sequence

```
User Action: Create KB with OpenAI
│
├─► Frontend: CreateKBView
│   ├─► Select Provider: "OpenAI"
│   ├─► Enter API Key
│   ├─► Select Model: "gpt-4o-mini"
│   └─► Click "Build KB"
│
├─► API: POST /api/kb
│   └─► Validate: provider + api_key
│
├─► Database: Insert KB record
│   └─► Store: provider="openai", api_key="sk-..."
│
├─► PDFProcessor: Download & Extract
│   └─► Return: pages_data[]
│
├─► EmbeddingsService
│   ├─► Get Provider: OpenAILLMProvider
│   ├─► Chunk Text: RecursiveTextSplitter
│   ├─► For each chunk:
│   │   └─► provider.generate_embedding()
│   │       └─► OpenAI API: text-embedding-3-small
│   └─► Store: FAISS index + metadata
│
└─► Response: Success
    └─► Frontend: Show success, redirect to chat
```

## Security Flow

```
┌──────────────┐
│ User enters  │
│ API key      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Frontend     │
│ (Plain text) │
└──────┬───────┘
       │ HTTPS
       ▼
┌──────────────┐
│ Backend API  │
│ (Receives)   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Database     │
│ (Plain text) │ ⚠️ Not encrypted
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Provider     │
│ (Uses key)   │
└──────────────┘

⚠️ Production: Add encryption layer before database
```

## Extension Points

```
To add a new provider (e.g., Anthropic Direct):

1. Create new provider class:
   backend/services/anthropic_provider.py
   
2. Implement LLMProvider interface:
   class AnthropicLLMProvider(LLMProvider):
       def generate_chat_response(...)
       def generate_embedding(...)

3. Update factory function:
   backend/services/llm_provider.py
   def get_llm_provider(...):
       if provider == 'anthropic':
           return AnthropicLLMProvider(...)

4. Add client for model listing:
   backend/services/anthropic_client.py

5. Add API endpoint:
   backend/app.py
   @app.get("/api/anthropic/models")

6. Update frontend:
   frontend/src/views/CreateKBView.vue
   Add "Anthropic" to provider dropdown

Done! No changes to core logic needed.
```

---

This architecture provides:
- ✅ Clean separation of concerns
- ✅ Easy to extend with new providers
- ✅ Testable components
- ✅ Backward compatible
- ✅ Scalable design
