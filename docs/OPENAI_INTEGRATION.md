# OpenAI Integration Guide

This project now supports both AWS Bedrock and OpenAI as LLM providers!

## Features

- **Dual Provider Support**: Choose between AWS Bedrock or OpenAI when creating a knowledge base
- **Flexible Model Selection**: Access to GPT-4o, GPT-4 Turbo, GPT-3.5 Turbo, and more
- **Secure API Key Storage**: OpenAI API keys are stored per knowledge base
- **Unified Interface**: Same chat experience regardless of provider

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

The `openai` package is now included in requirements.txt.

### 2. Migrate Existing Database (if applicable)

If you have an existing database, run the migration script:

```bash
cd backend
python migrate_db.py
```

This adds the `provider` and `api_key` columns to existing knowledge bases.

### 3. Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

## Usage

### Creating a Knowledge Base with OpenAI

1. Navigate to "Create Knowledge Base"
2. Scan and select your PDFs
3. In Step 2:
   - Select **Provider**: Choose "OpenAI"
   - Enter your **OpenAI API Key**
   - Select a **Model** (e.g., GPT-4o Mini for cost-effective option)
4. Build your knowledge base

### Creating a Knowledge Base with AWS Bedrock

1. Follow the same steps as above
2. In Step 2:
   - Select **Provider**: Choose "AWS Bedrock"
   - Select a **Model** (e.g., Claude 3.5 Sonnet)
   - No API key needed (uses AWS SSO)

## Available Models

### OpenAI Models
- **GPT-4o** - Latest and most capable
- **GPT-4o Mini** - Cost-effective, fast
- **GPT-4 Turbo** - Previous generation flagship
- **GPT-3.5 Turbo** - Fast and economical

### AWS Bedrock Models
- **Claude 3.5 Sonnet** - Anthropic's latest
- **Claude 3 Opus** - Most capable Claude model
- **Claude 3 Sonnet** - Balanced performance
- And more...

## Embeddings

- **OpenAI**: Uses `text-embedding-3-small` (cost-effective)
- **AWS Bedrock**: Uses `amazon.titan-embed-text-v1`

Both providers generate high-quality embeddings for semantic search.

## Cost Considerations

### OpenAI Pricing (approximate)
- GPT-4o Mini: ~$0.15 per 1M input tokens
- GPT-4o: ~$2.50 per 1M input tokens
- Embeddings: ~$0.02 per 1M tokens

### AWS Bedrock Pricing
- Varies by model and region
- Check AWS Bedrock pricing page for details

## Security Notes

⚠️ **Important**: 
- API keys are stored in the database in plain text in this version
- For production use, implement encryption for API keys
- Never commit API keys to version control
- Consider using environment variables for shared keys

## API Endpoints

### Get OpenAI Models
```
GET /api/openai/models
```

### Get Bedrock Models
```
GET /api/bedrock/models
```

### Create Knowledge Base
```
POST /api/kb
{
  "name": "My KB",
  "provider": "openai",  // or "bedrock"
  "api_key": "sk-...",   // required for OpenAI
  "model_id": "gpt-4o-mini",
  "documents": [...]
}
```

## Troubleshooting

### "API key is required for OpenAI provider"
- Make sure you've entered a valid OpenAI API key
- Key should start with `sk-`

### "OpenAI invocation failed"
- Check your API key is valid
- Ensure you have credits in your OpenAI account
- Verify the model ID is correct

### "Failed to generate embedding"
- Check your API key has access to embeddings API
- Verify network connectivity

## Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Vue.js)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│Bedrock │ │ OpenAI   │
│Provider│ │ Provider │
└────────┘ └──────────┘
```

## Future Enhancements

- [ ] API key encryption
- [ ] Support for more providers (Anthropic Direct, Cohere, etc.)
- [ ] Model-specific parameter tuning
- [ ] Cost tracking per knowledge base
- [ ] Batch processing for embeddings

## Support

For issues or questions, please check the main README.md or create an issue in the repository.
