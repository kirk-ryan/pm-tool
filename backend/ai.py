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
