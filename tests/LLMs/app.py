from flask import Flask, render_template, request, jsonify
import os
from typing import List, Dict, Optional

# Simple pluggable LLM framework supporting offline (local) and online providers
# Offline: Ollama (via HTTP API running locally) and GGUF via llama-cpp-python if installed
# Online: OpenAI-compatible APIs (e.g., OpenAI, DeepSeek) via environment variables / keys

try:
    import requests
except Exception:
    requests = None

try:
    from llama_cpp import Llama
except Exception:
    Llama = None

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration and discovery
OFFLINE_MODE = os.environ.get('LLM_OFFLINE', '1') == '1'
OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://127.0.0.1:11434')
MODELS_DIR = os.environ.get('LLM_MODELS_DIR', os.path.expanduser('~'))

# Online providers config (OpenAI-compatible)
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
DEEPSEEK_BASE_URL = os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')

# Runtime state
_loaded_llama: Optional[Llama] = None
_loaded_model_id: Optional[str] = None
_loaded_provider: Optional[str] = None  # "ollama" | "llama-cpp" | "openai" | "deepseek"


def list_offline_models() -> List[Dict[str, str]]:
    models: List[Dict[str, str]] = []
    # Ollama models (if server is running)
    if requests is not None:
        try:
            r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=1.5)
            if r.ok:
                data = r.json()
                for m in data.get('models', []):
                    name = m.get('name')
                    if name:
                        models.append({"id": f"ollama:{name}", "name": f"Ollama - {name}"})
        except Exception:
            pass
    # llama-cpp GGUF files under MODELS_DIR
    if Llama is not None:
        for root, _, files in os.walk(MODELS_DIR):
            for f in files:
                if f.lower().endswith('.gguf'):
                    full = os.path.join(root, f)
                    models.append({"id": f"llama-cpp:{full}", "name": f"llama-cpp - {f}"})
    return models


def list_online_models() -> List[Dict[str, str]]:
    models: List[Dict[str, str]] = []
    # OpenAI-like providers; we don't fetch model list (requires auth), just provide common defaults
    if OPENAI_API_KEY:
        for name in ["gpt-4o-mini", "gpt-4o", "gpt-4.1", "gpt-3.5-turbo"]:
            models.append({"id": f"openai:{name}", "name": f"OpenAI - {name}"})
    if DEEPSEEK_API_KEY:
        for name in ["deepseek-reasoner", "deepseek-chat"]:
            models.append({"id": f"deepseek:{name}", "name": f"DeepSeek - {name}"})
    return models


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/models')
def api_models():
    models = list_offline_models() if OFFLINE_MODE else list_online_models()
    return jsonify({"offline": OFFLINE_MODE, "models": models})


def _ensure_unloaded():
    global _loaded_llama, _loaded_model_id, _loaded_provider
    _loaded_llama = None
    _loaded_model_id = None
    _loaded_provider = None


@app.route('/api/load', methods=['POST'])
def api_load():
    global _loaded_llama, _loaded_model_id, _loaded_provider
    data = request.get_json(force=True) or {}
    model_id = data.get('model')
    if not model_id:
        return jsonify({"error": "model id required"}), 400

    _ensure_unloaded()

    try:
        provider, ident = model_id.split(':', 1)
    except ValueError:
        return jsonify({"error": "invalid model id"}), 400

    if provider == 'ollama':
        # nothing to preload; we will stream from ollama generate API
        _loaded_provider = 'ollama'
        _loaded_model_id = ident
        return jsonify({"status": "ok", "provider": provider, "model": ident})

    if provider == 'llama-cpp':
        if Llama is None:
            return jsonify({"error": "llama_cpp not installed"}), 400
        if not os.path.exists(ident):
            return jsonify({"error": f"model file not found: {ident}"}), 404
        _loaded_llama = Llama(model_path=ident, n_ctx=4096)
        _loaded_provider = 'llama-cpp'
        _loaded_model_id = ident
        return jsonify({"status": "ok", "provider": provider, "model": os.path.basename(ident)})

    if provider in ('openai', 'deepseek'):
        _loaded_provider = provider
        _loaded_model_id = ident
        return jsonify({"status": "ok", "provider": provider, "model": ident})

    return jsonify({"error": f"unknown provider: {provider}"}), 400


@app.route('/api/ask', methods=['POST'])
def api_ask():
    global _loaded_llama, _loaded_model_id, _loaded_provider
    data = request.get_json(force=True) or {}
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400
    if not _loaded_provider:
        return jsonify({"error": "no model loaded"}), 400

    try:
        if _loaded_provider == 'ollama':
            if requests is None:
                return jsonify({"error": "requests not installed"}), 400
            r = requests.post(f"{OLLAMA_HOST}/api/generate", json={"model": _loaded_model_id, "prompt": prompt})
            if not r.ok:
                return jsonify({"error": r.text}), 500
            # Ollama /api/generate streams; but many builds also allow non-stream
            # Handle both: if first char is '{' per-line JSON, join text fields
            text = ''
            try:
                for line in r.text.splitlines():
                    if not line.strip():
                        continue
                    obj = None
                    try:
                        import json as _json
                        obj = _json.loads(line)
                    except Exception:
                        pass
                    if obj and 'response' in obj:
                        text += obj['response']
                    else:
                        text += line
            except Exception:
                text = r.text
            return jsonify({"answer": text})

        if _loaded_provider == 'llama-cpp':
            res = _loaded_llama(prompt, max_tokens=512, stop=["</s>"])
            text = res["choices"][0]["text"]
            return jsonify({"answer": text})

        if _loaded_provider in ('openai', 'deepseek'):
            # Use requests to call OpenAI-compatible chat completions
            if requests is None:
                return jsonify({"error": "requests not installed"}), 400
            base = OPENAI_BASE_URL if _loaded_provider == 'openai' else DEEPSEEK_BASE_URL
            key = OPENAI_API_KEY if _loaded_provider == 'openai' else DEEPSEEK_API_KEY
            headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            payload = {
                "model": _loaded_model_id,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            r = requests.post(f"{base}/chat/completions", headers=headers, json=payload, timeout=60)
            if not r.ok:
                return jsonify({"error": r.text}), 500
            data = r.json()
            text = data['choices'][0]['message']['content']
            return jsonify({"answer": text})

        return jsonify({"error": "unsupported provider"}), 400
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


if __name__ == '__main__':
    # Run with: python app.py
    # Environment:
    #  LLM_OFFLINE=1 to enable offline; 0 for online
    #  OLLAMA_HOST=http://127.0.0.1:11434
    #  LLM_MODELS_DIR=C:\\models (for GGUF discovery)
    #  OPENAI_API_KEY=... ; DEEPSEEK_API_KEY=...
    app.run(host='0.0.0.0', port=5055, debug=True)
