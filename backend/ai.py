import json
import os

from openai import OpenAI

MODEL = "openai/gpt-oss-120b"
BASE_URL = "https://openrouter.ai/api/v1"


def get_client() -> OpenAI:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    return OpenAI(base_url=BASE_URL, api_key=api_key)


def ai_query(prompt: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


_SYSTEM_PROMPT = """\
You are a Kanban board assistant. Help the user understand and manage their board.

Always reply with valid JSON — no markdown, no code fences — in exactly this shape:
{"response": "<plain-text reply>", "board": null}

If the user asks you to change the board, include the complete updated board:
{"response": "<plain-text explanation>", "board": {"columns": [...], "cards": {...}}}

Rules:
- "response" is short, friendly plain text (no markdown).
- "board" is null unless you are making changes.
- When modifying, always return the COMPLETE board (every column and card, including unchanged ones).
- Column shape: {"id": "...", "title": "...", "cardIds": [...]}
- Card shape:   {"id": "...", "title": "...", "details": "..."}
- Reuse existing IDs for existing items; create new IDs for new items (e.g. "card-abc123").
"""


def ai_chat(board: dict, message: str, history: list[dict]) -> dict:
    client = get_client()

    board_context = (
        f"Current board:\n{json.dumps(board, indent=2)}"
    )
    system = _SYSTEM_PROMPT + f"\n\n{board_context}"

    messages: list[dict] = [{"role": "system", "content": system}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content
    result = json.loads(raw)
    return {
        "response": result.get("response", ""),
        "board": result.get("board"),
    }
