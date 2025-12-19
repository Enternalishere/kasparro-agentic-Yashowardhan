import os
import json
import time
from typing import Dict, Any, Optional
import requests


class ConfigurationError(RuntimeError):
    pass


class LocalLLMProvider:
    def __init__(self):
        kind = os.getenv("LOCAL_LLM_KIND", "").strip().lower()
        base = os.getenv("LOCAL_LLM_URL", "").strip()
        model = os.getenv("LOCAL_LLM_MODEL", "").strip()
        if not kind or not base or not model:
            raise ConfigurationError("LOCAL_LLM_KIND, LOCAL_LLM_URL, LOCAL_LLM_MODEL must be set")
        self.kind = kind
        self.base = base.rstrip("/")
        self.model = model

    def ping(self) -> None:
        try:
            if self.kind == "ollama":
                r = requests.get(f"{self.base}/api/tags", timeout=3)
                if r.status_code != 200:
                    raise ConfigurationError(f"Ollama not available: {r.status_code}")
            elif self.kind in ("lmstudio", "openai-compatible", "llamacpp"):
                r = requests.get(f"{self.base}/v1/models", timeout=3)
                if r.status_code != 200:
                    raise ConfigurationError(f"OpenAI-compatible server not available: {r.status_code}")
            else:
                raise ConfigurationError(f"Unsupported LOCAL_LLM_KIND: {self.kind}")
        except Exception as e:
            raise ConfigurationError(f"Local LLM unavailable: {e}")

    def chat_json(self, prompt: str) -> str:
        if self.kind == "ollama":
            payload = {"model": self.model, "prompt": prompt, "stream": False}
            r = requests.post(f"{self.base}/api/generate", json=payload, timeout=60)
            if r.status_code != 200:
                raise RuntimeError(f"Ollama chat error: {r.text}")
            data = r.json()
            return data.get("response", "")
        else:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
            }
            r = requests.post(f"{self.base}/v1/chat/completions", json=payload, timeout=60)
            if r.status_code != 200:
                raise RuntimeError(f"Chat error: {r.text}")
            data = r.json()
            return data["choices"][0]["message"]["content"]

    def ensure_json(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except Exception:
            start = text.find("{")
            end = text.rfind("}") + 1
            return json.loads(text[start:end])


def is_local_llm_available() -> bool:
    try:
        LocalLLMProvider().ping()
        return True
    except Exception:
        return False
