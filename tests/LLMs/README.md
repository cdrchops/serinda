Pluggable LLMs (Offline/Online)
================================

This mini app provides a simple, pluggable framework to run different LLM providers in either offline or online mode.

Location
- tests\LLMs\app.py — Flask server
- tests\LLMs\templates\index.html — Simple UI

Quick Start
1) Create and activate a Python environment (Python 3.9+ recommended).
2) Install dependencies:
   - Required: Flask, requests
   - Optional (for local GGUF): llama-cpp-python

   pip install Flask requests
   # Optional for local GGUF support
   pip install llama-cpp-python

3) Choose mode via environment:
   - Offline (default): LLM_OFFLINE=1
     - Supports:
       - Ollama (local server: http://127.0.0.1:11434)
       - llama-cpp GGUF files (scanned under LLM_MODELS_DIR)
   - Online: LLM_OFFLINE=0
     - Supports OpenAI-compatible APIs:
       - OpenAI: requires OPENAI_API_KEY
       - DeepSeek: requires DEEPSEEK_API_KEY and uses https://api.deepseek.com/v1 by default

4) Run the server from this folder:

   python app.py
   # App will start on http://127.0.0.1:5055

Environment Variables
- LLM_OFFLINE: "1" for offline mode (default), "0" for online mode.
- OLLAMA_HOST: Base URL for Ollama (default: http://127.0.0.1:11434). Requires Ollama server running locally with pulled models.
- LLM_MODELS_DIR: Directory to scan recursively for .gguf files when using llama-cpp (default: user home directory).
- OPENAI_API_KEY: API key for OpenAI (online mode).
- OPENAI_BASE_URL: Base URL for OpenAI-compatible endpoint (default: https://api.openai.com/v1).
- DEEPSEEK_API_KEY: API key for DeepSeek (online mode).
- DEEPSEEK_BASE_URL: Base URL for DeepSeek (default: https://api.deepseek.com/v1).

Using the UI
- The page shows whether you are in Offline mode (checkbox is informational).
- The dropdown lists available models for the current mode:
  - Offline: Ollama models (if Ollama is running) and any GGUF models found in LLM_MODELS_DIR.
  - Online: Common model names for the provider(s) with keys present (OpenAI, DeepSeek).
- After selecting a model, click "Load" to make it active.
- Enter your question in the textarea and click "Ask". The response appears below.

Providers
- Ollama (offline): Lists models via /api/tags and queries via /api/generate on your local Ollama server.
- llama-cpp (offline): Loads a specified GGUF file directly in-process (requires llama-cpp-python; large models need sufficient RAM/VRAM depending on build).
- OpenAI (online): Calls the Chat Completions API using your OPENAI_API_KEY.
- DeepSeek (online): Calls DeepSeek’s Chat Completions API using your DEEPSEEK_API_KEY.

Notes
- If no models are listed in offline mode:
  - Ensure Ollama is running and has models pulled (e.g., `ollama pull llama3`), or
  - Set LLM_MODELS_DIR to a directory containing .gguf files.
- If using llama-cpp-python on Windows, pre-built wheels are available for CPU; for GPU you may need a compatible build.
- Timeouts and error messages are returned in the UI if providers are not reachable or keys are missing.
