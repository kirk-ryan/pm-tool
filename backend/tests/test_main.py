import pytest
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
