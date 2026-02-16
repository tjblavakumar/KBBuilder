# OpenAI Integration - Setup Checklist

Use this checklist to ensure everything is set up correctly.

## Pre-Installation

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Git installed (optional)
- [ ] OpenAI account created
- [ ] OpenAI API key obtained

## Backend Setup

- [ ] Navigate to `backend` directory
- [ ] Virtual environment activated
- [ ] Run `pip install -r requirements.txt`
- [ ] Verify `openai==1.54.0` installed
- [ ] Run `python migrate_db.py` (if existing database)
- [ ] No errors in migration output
- [ ] Backend starts with `python app.py`
- [ ] See "Uvicorn running on http://0.0.0.0:8000"

## Frontend Setup

- [ ] Navigate to `frontend` directory
- [ ] Run `npm install` (if first time)
- [ ] Frontend starts with `npm run dev`
- [ ] See "Local: http://localhost:5173/"
- [ ] Browser opens automatically or manually navigate

## Verification Tests

### Test 1: OpenAI Models Endpoint
- [ ] Open browser to http://localhost:8000/api/openai/models
- [ ] See JSON response with models list
- [ ] Default model is "gpt-4o-mini"

### Test 2: Bedrock Models Endpoint (if AWS configured)
- [ ] Open browser to http://localhost:8000/api/bedrock/models
- [ ] See JSON response with models list
- [ ] Default model is Claude

### Test 3: Frontend Loads
- [ ] Navigate to http://localhost:5173
- [ ] See "Knowledge Bases" page
- [ ] "Create New" button visible
- [ ] No console errors (F12)

### Test 4: Provider Selection
- [ ] Click "Create New"
- [ ] Enter a test URL and scan (or skip)
- [ ] Go to Step 2
- [ ] See "Select Provider" dropdown
- [ ] Options: "AWS Bedrock" and "OpenAI"
- [ ] Select "OpenAI"
- [ ] API key field appears
- [ ] Model dropdown updates with OpenAI models

### Test 5: Create OpenAI KB (Optional - requires API key)
- [ ] Complete Step 1 with test PDFs
- [ ] In Step 2, select "OpenAI"
- [ ] Enter valid API key
- [ ] Select "GPT-4o Mini"
- [ ] Click "Build KB"
- [ ] Wait for processing
- [ ] Success message appears
- [ ] KB appears in home page

### Test 6: Chat with OpenAI KB (Optional)
- [ ] Click "Start Chat" on OpenAI KB
- [ ] Enter a test question
- [ ] Receive response
- [ ] Sources displayed
- [ ] No errors in console

## Troubleshooting Checks

### If Backend Won't Start
- [ ] Check Python version: `python --version`
- [ ] Check virtual environment is activated
- [ ] Check all dependencies installed: `pip list | grep openai`
- [ ] Check port 8000 is not in use: `netstat -an | grep 8000`
- [ ] Check for error messages in terminal

### If Frontend Won't Start
- [ ] Check Node version: `node --version`
- [ ] Check npm version: `npm --version`
- [ ] Run `npm install` again
- [ ] Check port 5173 is not in use
- [ ] Check for error messages in terminal

### If OpenAI Models Don't Load
- [ ] Check backend is running
- [ ] Check network tab in browser (F12)
- [ ] Verify endpoint returns data: http://localhost:8000/api/openai/models
- [ ] Check console for errors

### If API Key Validation Fails
- [ ] Verify API key starts with "sk-"
- [ ] Check API key is active in OpenAI dashboard
- [ ] Verify account has credits
- [ ] Check for typos in API key

### If KB Creation Fails
- [ ] Check backend logs for errors
- [ ] Verify PDFs are accessible
- [ ] Check API key is valid
- [ ] Verify sufficient OpenAI credits
- [ ] Check network connectivity

## File Verification

### New Backend Files
- [ ] `backend/services/openai_client.py` exists
- [ ] `backend/services/llm_provider.py` exists
- [ ] `backend/migrate_db.py` exists
- [ ] `backend/test_openai.py` exists
- [ ] `backend/setup_openai.bat` exists (Windows)

### Modified Backend Files
- [ ] `backend/database.py` has provider and api_key columns
- [ ] `backend/models.py` has OpenAI models
- [ ] `backend/app.py` has /api/openai/models endpoint
- [ ] `backend/services/chat.py` uses provider abstraction
- [ ] `backend/services/embeddings.py` uses provider abstraction
- [ ] `backend/requirements.txt` includes openai==1.54.0

### Modified Frontend Files
- [ ] `frontend/src/views/CreateKBView.vue` has provider selection
- [ ] `frontend/src/views/HomeView.vue` displays provider
- [ ] `frontend/src/services/api.js` has getModels(provider)

### Documentation Files
- [ ] `OPENAI_INTEGRATION.md` exists
- [ ] `IMPLEMENTATION_SUMMARY.md` exists
- [ ] `QUICKSTART_OPENAI.md` exists
- [ ] `PROVIDER_COMPARISON.md` exists
- [ ] `SETUP_CHECKLIST.md` exists (this file)

## Database Verification

### If Existing Database
- [ ] Backup created before migration
- [ ] Migration script ran successfully
- [ ] `provider` column exists in knowledgebases table
- [ ] `api_key` column exists in knowledgebases table
- [ ] Existing KBs have provider='bedrock'

### Check Database Schema
```bash
cd backend
python -c "from database import engine; import sqlite3; conn = sqlite3.connect('kb_builder.db'); cursor = conn.cursor(); cursor.execute('PRAGMA table_info(knowledgebases)'); print([col[1] for col in cursor.fetchall()])"
```
- [ ] Output includes 'provider' and 'api_key'

## Security Checks

- [ ] API keys not committed to git
- [ ] `.gitignore` includes `*.db` and `*.env`
- [ ] API keys stored securely
- [ ] No API keys in console logs
- [ ] No API keys in error messages

## Performance Checks

- [ ] Backend responds within 1 second
- [ ] Frontend loads within 2 seconds
- [ ] Model list loads quickly
- [ ] No memory leaks in browser
- [ ] No excessive API calls

## Final Verification

- [ ] Can create KB with Bedrock (if AWS configured)
- [ ] Can create KB with OpenAI (if API key available)
- [ ] Can chat with both types of KBs
- [ ] Can switch between KBs
- [ ] Can delete KBs
- [ ] All features work as expected

## Documentation Review

- [ ] Read OPENAI_INTEGRATION.md
- [ ] Read QUICKSTART_OPENAI.md
- [ ] Read PROVIDER_COMPARISON.md
- [ ] Understand security considerations
- [ ] Know how to get support

## Optional: Run Test Suite

```bash
cd backend
python test_openai.py
```

- [ ] OpenAI Client test passes
- [ ] OpenAI Provider test passes (if API key provided)
- [ ] All tests show ✓ PASSED

## Completion

✅ **All checks passed!** You're ready to use OpenAI with KB Builder.

⚠️ **Some checks failed?** Review the troubleshooting section or check the documentation.

## Next Steps

1. Create your first OpenAI knowledge base
2. Compare results with Bedrock (if available)
3. Explore different models
4. Read the provider comparison guide
5. Share feedback!

## Getting Help

If you encounter issues:

1. Check error messages carefully
2. Review relevant documentation
3. Check browser console (F12)
4. Check backend logs
5. Verify API keys and credentials
6. Try the test suite

## Rollback (if needed)

If something goes wrong:

```bash
# Stop backend and frontend
# Restore database backup
cp backend/kb_builder.db.backup backend/kb_builder.db
# Restart services
```

---

**Setup Date:** _____________

**Completed By:** _____________

**Notes:** _____________________________________________
