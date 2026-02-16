# Fixes Applied

## Issue: Bedrock Error When Creating Knowledge Base

### Problem
When clicking "Create Knowledge Base", the app was trying to load AWS Bedrock models by default, causing errors for users without AWS credentials.

### Root Cause
The frontend `CreateKBView.vue` had `selectedProvider` defaulting to `'bedrock'`, which triggered a call to `/api/bedrock/models` on page load.

### Solution Applied

1. **Changed Default Provider to OpenAI**
   - File: `frontend/src/views/CreateKBView.vue`
   - Changed: `const selectedProvider = ref('openai')`
   - Now the app defaults to OpenAI (easier setup, no AWS required)

2. **Fixed Pydantic Warnings**
   - File: `backend/models.py`
   - Added `model_config = ConfigDict(protected_namespaces=())` to:
     - `BedrockModel`
     - `OpenAIModel`
     - `CreateKBRequest`
     - `KBDetail`
     - `KBListItem`
   - This suppresses the "model_" namespace warnings

3. **Fixed TypeScript Config Issues**
   - Files: `frontend/tsconfig.node.json`, `frontend/tsconfig.app.json`
   - Removed missing `extends` references
   - Added complete TypeScript compiler options

## How to Apply

```bash
# Stop services
./stop.sh

# Start services (with venv activated)
./start-simple.sh

# Or if not in venv:
cd backend
source venv/bin/activate
cd ..
./start-simple.sh
```

## What Changed for Users

### Before
- Page loaded → Tried to load Bedrock models → Error if no AWS
- User had to manually switch to OpenAI

### After
- Page loads → Loads OpenAI models by default
- User can still switch to Bedrock if they have AWS credentials
- Cleaner experience for users without AWS

## Testing

1. Open http://localhost:5173
2. Click "Create New"
3. Should see OpenAI selected by default
4. Models should load without errors
5. Can enter OpenAI API key and create KB

## Additional Notes

- AWS Bedrock is still fully supported
- Users can switch to Bedrock in the provider dropdown
- OpenAI is now the recommended default for easier setup
