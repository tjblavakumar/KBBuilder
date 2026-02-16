# Setting Up Your API Key

You have two options to provide your OpenAI API key:

## Option 1: Config File (Recommended)

1. **Copy the example config:**
   ```bash
   cd backend
   cp config.example.yml config.yml
   ```

2. **Edit config.yml:**
   ```bash
   nano config.yml
   # or
   vim config.yml
   ```

3. **Add your API key:**
   ```yaml
   openai:
     api_key: "sk-proj-your-actual-key-here"
     default_model: "gpt-4o-mini"
   ```

4. **Save and restart:**
   ```bash
   cd ..
   ./stop.sh
   pip install pyyaml==6.0.1
   ./start-simple.sh
   ```

5. **Create KB without entering key:**
   - The app will automatically use the key from config.yml
   - You can leave the API key field empty in the UI

## Option 2: Enter Manually (Each Time)

1. When creating a KB, enter your API key in the form
2. The key will be stored with that specific KB
3. You'll need to enter it again for new KBs

## Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...` or `sk-...`)
5. Save it securely!

## Troubleshooting

### "Incorrect API key provided"
- Make sure you copied the entire key
- Check for extra spaces
- Verify the key is active in your OpenAI dashboard
- Make sure you have credits in your account

### Config file not working
- Make sure the file is named `config.yml` (not `config.example.yml`)
- Check the YAML syntax (indentation matters!)
- Restart the backend after editing config

### Still having issues?
- Check backend.log for detailed errors
- Make sure pyyaml is installed: `pip install pyyaml==6.0.1`
