import requests


OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"
REQUEST_TIMEOUT = 180


class OllamaServiceError(Exception):
    """A user-readable error raised when Ollama cannot generate a response."""


def generate_headlines(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.4},
    }

    try:
        response = requests.post(
            OLLAMA_CHAT_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.Timeout as exc:
        raise OllamaServiceError(
            "Ollama took too long to respond. Check that the service is running "
            "and try again."
        ) from exc
    except requests.exceptions.ConnectionError as exc:
        raise OllamaServiceError(
            "Could not connect to Ollama. Start Ollama with `ollama serve`, "
            "then verify that it is available at http://localhost:11434."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise OllamaServiceError(f"Ollama request failed: {exc}") from exc

    if response.status_code == 404:
        raise OllamaServiceError(
            "The Ollama model could not be found. Install it with "
            "`ollama pull qwen2.5:3b`."
        )
    if not response.ok:
        message = ""
        try:
            message = response.json().get("error", "")
        except (requests.exceptions.JSONDecodeError, ValueError):
            message = response.text.strip()
        raise OllamaServiceError(
            f"Ollama returned an error (HTTP {response.status_code}). "
            f"{message or 'Please check the Ollama service and model.'}"
        )

    try:
        data = response.json()
    except (requests.exceptions.JSONDecodeError, ValueError) as exc:
        raise OllamaServiceError("Ollama returned an unreadable response.") from exc

    try:
        content = data["message"]["content"]
    except (KeyError, TypeError) as exc:
        raise OllamaServiceError(
            "Ollama returned a response without message content."
        ) from exc

    if not isinstance(content, str) or not content.strip():
        raise OllamaServiceError("Ollama returned an empty response.")
    return content
