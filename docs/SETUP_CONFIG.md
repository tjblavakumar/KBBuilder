# OpenAI Key Setup (Session-Only)

This app now uses a **session-only OpenAI key flow**.

- Enter the key in **Admin** (top navigation)
- The key is validated immediately
- The key is kept only in browser memory for the current session
- The app does not persist new keys to DB/config

## Steps

1. Start the app:
   ```bash
   ./start.sh
   ```
2. Open: `http://localhost:5173`
3. Click **Admin** in the top bar
4. Paste your OpenAI API key (`sk-...` or `sk-proj-...`)
5. Click **Save**
6. Wait for validation success toast (`OpenAI API key validated for this session`)

You should now see `OpenAI Ready` in the top nav.

## How It Works

- Frontend attaches `X-Session-OpenAI-Key` to API requests during the session
- Backend validates OpenAI calls using that key
- If missing/invalid, backend returns explicit 4xx errors

## Troubleshooting

### "OpenAI API key required for this session"
- Open **Admin** and set your key again
- Ensure you clicked **Save** and saw validation success

### "OpenAI API key is invalid"
- Check for copy/paste issues or trailing spaces
- Regenerate key at https://platform.openai.com/api-keys

### "OpenAI quota exceeded or billing issue"
- Check credits/billing in your OpenAI account

### "Unable to reach OpenAI API"
- Check internet/DNS from the backend machine

## Optional Legacy Cleanup

If you want to remove older keys that may have been stored previously:

```bash
cd backend
../venv/bin/python cleanup_api_keys.py
```

or call:

`POST /api/admin/cleanup-api-keys`
