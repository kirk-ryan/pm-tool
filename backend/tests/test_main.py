import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


# ── helpers ──────────────────────────────────────────────────────────────────

def make_client(tmp_db):
    """Return a TestClient whose app uses tmp_db for all DB calls."""
    import db as db_module
    import importlib
    import main as main_module

    # Point the db module at the temp file and seed it.
    db_module.DB_PATH = tmp_db
    db_module.init_db(tmp_db)

    # Reload main so its imports and startup handler use the patched DB_PATH.
    importlib.reload(main_module)

    return TestClient(main_module.app, raise_server_exceptions=True)


# ── /api/test ─────────────────────────────────────────────────────────────────

def test_api_test_returns_json(tmp_path):
    client = make_client(tmp_path / "test.db")
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"message": "API is working", "status": "success"}


# ── GET /api/board ────────────────────────────────────────────────────────────

def test_get_board_returns_seed_data(tmp_path):
    client = make_client(tmp_path / "test.db")
    response = client.get("/api/board")
    assert response.status_code == 200
    data = response.json()
    assert "columns" in data
    assert "cards" in data
    assert len(data["columns"]) == 5
    assert len(data["cards"]) == 8


def test_get_board_columns_have_required_fields(tmp_path):
    client = make_client(tmp_path / "test.db")
    data = client.get("/api/board").json()
    for col in data["columns"]:
        assert "id" in col
        assert "title" in col
        assert "cardIds" in col


def test_get_board_cards_have_required_fields(tmp_path):
    client = make_client(tmp_path / "test.db")
    data = client.get("/api/board").json()
    for card in data["cards"].values():
        assert "id" in card
        assert "title" in card
        assert "details" in card


# ── PUT /api/board ────────────────────────────────────────────────────────────

def test_put_board_persists_changes(tmp_path):
    client = make_client(tmp_path / "test.db")

    updated = {
        "columns": [{"id": "col-1", "title": "Todo", "cardIds": ["c-1"]}],
        "cards": {"c-1": {"id": "c-1", "title": "My card", "details": "details"}},
    }
    put_response = client.put("/api/board", json=updated)
    assert put_response.status_code == 204

    get_response = client.get("/api/board")
    assert get_response.status_code == 200
    saved = get_response.json()
    assert saved["columns"][0]["title"] == "Todo"
    assert saved["cards"]["c-1"]["title"] == "My card"


def test_put_board_accepts_empty_board(tmp_path):
    client = make_client(tmp_path / "test.db")
    empty = {"columns": [], "cards": {}}
    response = client.put("/api/board", json=empty)
    assert response.status_code == 204
    assert client.get("/api/board").json() == empty


def test_put_board_rejects_invalid_body(tmp_path):
    client = make_client(tmp_path / "test.db")
    response = client.put("/api/board", json={"bad": "payload"})
    assert response.status_code == 422


def test_put_board_preserves_card_order(tmp_path):
    client = make_client(tmp_path / "test.db")
    ordered = {
        "columns": [{"id": "col-1", "title": "Col", "cardIds": ["c-3", "c-1", "c-2"]}],
        "cards": {
            "c-1": {"id": "c-1", "title": "A", "details": ""},
            "c-2": {"id": "c-2", "title": "B", "details": ""},
            "c-3": {"id": "c-3", "title": "C", "details": ""},
        },
    }
    client.put("/api/board", json=ordered)
    saved = client.get("/api/board").json()
    assert saved["columns"][0]["cardIds"] == ["c-3", "c-1", "c-2"]


# ── db module unit tests ──────────────────────────────────────────────────────

def test_init_db_is_idempotent(tmp_path):
    from db import init_db, get_board
    path = tmp_path / "idempotent.db"
    init_db(path)
    init_db(path)
    data = get_board("user", path)
    assert data is not None
    assert len(data["columns"]) == 5


def test_get_board_returns_none_for_unknown_user(tmp_path):
    from db import init_db, get_board
    path = tmp_path / "test.db"
    init_db(path)
    assert get_board("nobody", path) is None


def test_set_board_returns_false_for_unknown_user(tmp_path):
    from db import init_db, set_board
    path = tmp_path / "test.db"
    init_db(path)
    ok = set_board("nobody", {"columns": [], "cards": {}}, path)
    assert ok is False


def test_set_and_get_board_roundtrip(tmp_path):
    from db import init_db, get_board, set_board
    path = tmp_path / "test.db"
    init_db(path)
    payload = {"columns": [{"id": "x", "title": "X", "cardIds": []}], "cards": {}}
    set_board("user", payload, path)
    assert get_board("user", path) == payload


# ── POST /api/ai/test ─────────────────────────────────────────────────────────

def test_ai_test_returns_response(tmp_path):
    client = make_client(tmp_path / "test.db")
    with patch("main.ai_query", return_value="4") as mock_query:
        response = client.post("/api/ai/test", json={"prompt": "2+2"})
    assert response.status_code == 200
    assert response.json() == {"response": "4"}
    mock_query.assert_called_once_with("2+2")


def test_ai_test_uses_default_prompt(tmp_path):
    client = make_client(tmp_path / "test.db")
    with patch("main.ai_query", return_value="4"):
        response = client.post("/api/ai/test", json={})
    assert response.status_code == 200
    assert "response" in response.json()


def test_ai_test_missing_api_key_returns_500(tmp_path):
    client = make_client(tmp_path / "test.db")
    with patch("main.ai_query", side_effect=ValueError("OPENROUTER_API_KEY environment variable is not set")):
        response = client.post("/api/ai/test", json={"prompt": "hello"})
    assert response.status_code == 500
    assert "OPENROUTER_API_KEY" in response.json()["detail"]


def test_ai_test_network_error_returns_502(tmp_path):
    client = make_client(tmp_path / "test.db")
    with patch("main.ai_query", side_effect=RuntimeError("connection refused")):
        response = client.post("/api/ai/test", json={"prompt": "hello"})
    assert response.status_code == 502
    assert response.json()["detail"] == "AI service unavailable"


# ── ai module unit tests ──────────────────────────────────────────────────────

def test_ai_query_calls_openai_client(monkeypatch):
    import ai as ai_module

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "4"

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch.object(ai_module, "get_client", return_value=mock_client):
        result = ai_module.ai_query("2+2")

    assert result == "4"
    mock_client.chat.completions.create.assert_called_once_with(
        model=ai_module.MODEL,
        messages=[{"role": "user", "content": "2+2"}],
    )


def test_get_client_raises_without_api_key(monkeypatch):
    import ai as ai_module
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        ai_module.get_client()


def test_get_client_uses_openrouter_base_url(monkeypatch):
    import ai as ai_module
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    client = ai_module.get_client()
    assert "openrouter.ai" in str(client.base_url)
