# 🚀 Free LLM Setup with Ollama

## Quick Setup for Free AI Recruitment System

### Step 1: Install Ollama
1. Go to https://ollama.ai/
2. Download and install Ollama for Windows
3. Run the installer

### Step 2: Pull a Free Model
Open Command Prompt or PowerShell and run:
```bash
ollama pull llama3.2:3b
```

### Step 3: Start Ollama Service
```bash
ollama serve
```

### Step 4: Run the AI Recruitment System
```bash
python -m streamlit run app.py
```

### Step 5: Configure the System
1. Open http://localhost:7860
2. In the sidebar, select **"Ollama"** as Model Provider
3. **No API key needed!** Leave it blank
4. Configure your Zoom and Email settings
5. Start using the system!

## Benefits of Ollama:
- ✅ **Completely FREE** - No API costs
- ✅ **Runs locally** - No internet dependency
- ✅ **Privacy** - Your data stays on your computer
- ✅ **Fast** - No API latency

## Alternative Free Models:
You can also try these models:
```bash
ollama pull llama3.2:1b    # Smaller, faster
ollama pull llama3.2:8b     # Larger, more capable
ollama pull mistral:7b       # Good balance
```

## Troubleshooting:
- If Ollama isn't found, restart your terminal after installation
- Make sure Ollama is running: `ollama serve`
- Check if model is downloaded: `ollama list`

**That's it! You now have a completely free AI recruitment system!** 🎉 