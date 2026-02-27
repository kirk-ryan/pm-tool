# Backend

FastAPI backend for the Project Management MVP.

## Structure

- `main.py`: FastAPI app with all routes.
- `pyproject.toml`: Python project config, managed with uv.
- `tests/`: pytest unit tests for all routes.

## Routes

- `GET /`: Serves the built NextJS frontend static files (falls back to nothing if not built).
- `GET /api/test`: Returns JSON health check `{"message": "API is working", "status": "success"}`.
- `GET /api/board`: Returns the current user's Kanban board data (columns + cards).
- `PUT /api/board`: Replaces the current user's board data.
- `POST /api/ai/test`: Sends a prompt to OpenRouter (model: `openai/gpt-oss-120b`) and returns the response. Body: `{"prompt": "..."}` (defaults to `"2+2"`).

## AI (OpenRouter)

- `backend/ai.py`: OpenRouter client using the `openai` package with `base_url=https://openrouter.ai/api/v1`.
- Requires `OPENROUTER_API_KEY` environment variable (loaded from root `.env` for local dev).
- Model: `openai/gpt-oss-120b`.

## Running locally

From `backend/`:

```
uv run uvicorn main:app --reload
```

## Running tests

From `backend/`:

```
uv run pytest
```
