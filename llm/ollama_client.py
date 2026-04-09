"""
ollama_client.py

This module provides a simple Python client for calling
a local Ollama LLM (Gemma 2B) via HTTP.

No API key is required.
"""

import requests
import json
from typing import Optional

# Ollama local server URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Model name (Gemma 1B)
MODEL_NAME = "gemma3:1b"


def call_llm(prompt: str, temperature: float = 0.0) -> str:
    """
    Send a prompt to the local Ollama LLM and return the response text.

    Args:
        prompt (str): Input prompt for the LLM
        temperature (float): Sampling temperature

    Returns:
        str: Generated response from the LLM
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "temperature": temperature,
        "stream": False
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=1000
        )
        response.raise_for_status()

        result = response.json()
        return result.get("response", "").strip()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Failed to call Ollama LLM at {OLLAMA_URL}. "
            f"Is Ollama running?\nError: {e}"
        )