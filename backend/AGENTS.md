# Backend

FastAPI backend for the Project Management MVP.

## Structure

- `main.py`: FastAPI app with all routes.
- `pyproject.toml`: Python project config, managed with uv.
- `tests/`: pytest unit tests for all routes.

## Routes

- `GET /`: Returns static HTML (Hello World placeholder; will serve the built NextJS frontend in Part 3).
- `GET /api/test`: Returns JSON health check `{"message": "API is working", "status": "success"}`.

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
