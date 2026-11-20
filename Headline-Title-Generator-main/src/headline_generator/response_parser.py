import json
import re
from typing import Any


class ResponseParseError(ValueError):
    """Raised when an Ollama response does not contain parseable JSON."""


def parse_ollama_response(response_text: str) -> list[dict[str, Any]]:
    if not isinstance(response_text, str) or not response_text.strip():
        raise ResponseParseError("The AI response is empty.")

    text = response_text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        start = text.find("[")
        end = text.rfind("]")
        if start != -1 and end > start:
            try:
                parsed = json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                parsed = None
        else:
            parsed = None

        if parsed is None:
            raise ResponseParseError(
                "Ollama returned invalid JSON. Please try again."
            ) from exc

    if not isinstance(parsed, list):
        raise ResponseParseError("The AI response must be a JSON list.")
    if any(not isinstance(record, dict) for record in parsed):
        raise ResponseParseError(
            "Every item in the AI response must be a JSON object."
        )
    return parsed
