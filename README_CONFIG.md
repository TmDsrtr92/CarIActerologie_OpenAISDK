# Configuration Setup Guide for CarIActerology

This guide helps you set up API keys and configuration for the CarIActerology application.

## Quick Setup

1. **Replace dummy API keys** in `.env` file with your actual keys
2. **Run the setup validator**: `python config_setup.py`
3. **Install required packages**: `pip install -r requirements.txt`

## Configuration Files Overview

### `.env` - Local Development
Contains environment variables for local development:
```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
MEM0_API_KEY=your-mem0-key-here
```

### `.streamlit/secrets.toml` - Streamlit Cloud
Contains secrets for Streamlit Cloud deployment:
```toml
[api_keys]
OPENAI_API_KEY = "sk-your-actual-openai-key-here"
```

### `modules/config.py` - Configuration Manager
Centralized configuration management that handles:
- API keys from multiple sources
- Model settings
- Application configuration
- Validation and error handling

## Required API Keys

### OpenAI API Key (REQUIRED)
- **Purpose**: Powers the AI knowledge base and embeddings
- **Get it**: https://platform.openai.com/api-keys
- **Usage**: Semantic search, character analysis, embeddings

### Mem0 API Key (OPTIONAL)
- **Purpose**: Enhanced memory management system
- **Get it**: https://mem0.ai (if using hosted version)
- **Usage**: User memory persistence, conversation context

## Setup Steps

### 1. Get Your OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-...`)

### 2. Configure for Local Development
Replace the dummy value in `.env`:
```env
# Replace this dummy value:
OPENAI_API_KEY=sk-dummy-openai-api-key-replace-with-your-actual-key-here

# With your actual key:
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Validate Configuration
```bash
python config_setup.py
```

You should see:
```
✅ All required configuration is valid!
✅ Configuration setup complete!
```

## Deployment Configuration

### Streamlit Cloud
1. Upload your code to GitHub (without API keys)
2. In Streamlit Cloud dashboard → App Settings → Secrets
3. Add your keys:
```toml
[api_keys]
OPENAI_API_KEY = "sk-your-actual-key-here"
```

### Docker Deployment
Use environment variables or `.env` file:
```bash
docker-compose up --build
```

## Security Best Practices

### ✅ Do:
- Keep API keys in `.env` or secrets files
- Add sensitive files to `.gitignore`
- Use different keys for development/production
- Rotate keys periodically

### ❌ Don't:
- Commit API keys to git
- Share keys in code or screenshots
- Use production keys for development
- Leave dummy values in production

## Configuration Priority

The system checks configuration in this order:
1. **Streamlit secrets** (when running in Streamlit)
2. **Environment variables**
3. **`.env` file**
4. **Default values**

## Troubleshooting

### "Configuration error: OPENAI_API_KEY is not configured"
- Check that you replaced the dummy value in `.env`
- Ensure the key starts with `sk-`
- Verify the file is in the project root

### "python-dotenv not installed"
```bash
pip install python-dotenv
```

### "No module named 'config'"
Run from the project root directory where `config_setup.py` is located.

### API Key Not Working
- Verify the key is correct and active
- Check OpenAI account billing status
- Ensure key has proper permissions

## Model Configuration

### Default Models
- **LLM**: `gpt-4o-mini` (cost-efficient)
- **Embeddings**: `text-embedding-3-small` (optimized for characterology)

### Custom Models
Modify in `.env`:
```env
DEFAULT_LLM_MODEL=gpt-4o
DEFAULT_EMBEDDING_MODEL=text-embedding-3-large
```

## Development vs Production

### Development Mode
```env
DEVELOPMENT_MODE=true
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

### Production Mode
```env
DEVELOPMENT_MODE=false
DEBUG_MODE=false
LOG_LEVEL=INFO
```

## Testing Your Setup

Run the configuration test:
```bash
python config_setup.py
```

Expected output for successful setup:
```
🎯 CarIActerology Configuration Setup
==================================================
📄 .env file: ✅ Found
🔑 API keys in .env: ✅ Looks configured

🧪 Testing Configuration Loading
------------------------------
=== CarIActerology Configuration Summary ===
Environment: Local
Development Mode: True
LLM Model: gpt-4o-mini
Embedding Model: text-embedding-3-small

API Keys Status:
  OPENAI_API_KEY: sk-1234567890...abcd ✓

✅ All required configuration is valid!
✅ Configuration setup complete!
```

## Support

If you encounter issues:
1. Run `python config_setup.py` for diagnostics
2. Check that API keys are properly formatted
3. Verify all required packages are installed
4. Ensure files are in correct locations

The application will not start without proper OpenAI API key configuration.