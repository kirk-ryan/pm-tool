import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "kanban.db"

SEED_DATA = {
    "columns": [
        {"id": "col-backlog",   "title": "Backlog",      "cardIds": ["card-1", "card-2"]},
        {"id": "col-discovery", "title": "Discovery",    "cardIds": ["card-3"]},
        {"id": "col-progress",  "title": "In Progress",  "cardIds": ["card-4", "card-5"]},
        {"id": "col-review",    "title": "Review",       "cardIds": ["card-6"]},
        {"id": "col-done",      "title": "Done",         "cardIds": ["card-7", "card-8"]},
    ],
    "cards": {
        "card-1": {"id": "card-1", "title": "Align roadmap themes",    "details": "Draft quarterly themes with impact statements and metrics."},
        "card-2": {"id": "card-2", "title": "Gather customer signals",  "details": "Review support tags, sales notes, and churn feedback."},
        "card-3": {"id": "card-3", "title": "Prototype analytics view", "details": "Sketch initial dashboard layout and key drill-downs."},
        "card-4": {"id": "card-4", "title": "Refine status language",   "details": "Standardize column labels and tone across the board."},
        "card-5": {"id": "card-5", "title": "Design card layout",       "details": "Add hierarchy and spacing for scanning dense lists."},
        "card-6": {"id": "card-6", "title": "QA micro-interactions",    "details": "Verify hover, focus, and loading states."},
        "card-7": {"id": "card-7", "title": "Ship marketing page",      "details": "Final copy approved and asset pack delivered."},
        "card-8": {"id": "card-8", "title": "Close onboarding sprint",  "details": "Document release notes and share internally."},
    },
}


def _resolve(path: Path | None) -> Path:
    """Return path if given, otherwise the current module-level DB_PATH."""
    return path if path is not None else DB_PATH


def get_connection(path: Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(_resolve(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(path: Path | None = None) -> None:
    """Create tables and seed the default user + board if they don't exist."""
    with get_connection(path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT    NOT NULL UNIQUE,
                created_at TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS boards (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                data       TEXT    NOT NULL,
                updated_at TEXT    NOT NULL DEFAULT (datetime('now'))
            );
        """)

        conn.execute(
            "INSERT OR IGNORE INTO users (username) VALUES (?)", ("user",)
        )

        row = conn.execute(
            "SELECT id FROM users WHERE username = ?", ("user",)
        ).fetchone()
        user_id = row["id"]

        existing = conn.execute(
            "SELECT id FROM boards WHERE user_id = ?", (user_id,)
        ).fetchone()

        if not existing:
            conn.execute(
                "INSERT INTO boards (user_id, data) VALUES (?, ?)",
                (user_id, json.dumps(SEED_DATA)),
            )


def get_board(username: str, path: Path | None = None) -> dict | None:
    """Return the board data dict for a user, or None if not found."""
    with get_connection(path) as conn:
        row = conn.execute(
            """
            SELECT b.data FROM boards b
            JOIN users u ON u.id = b.user_id
            WHERE u.username = ?
            ORDER BY b.id
            LIMIT 1
            """,
            (username,),
        ).fetchone()
    return json.loads(row["data"]) if row else None


def set_board(username: str, data: dict, path: Path | None = None) -> bool:
    """Overwrite the board data for a user. Returns True on success."""
    with get_connection(path) as conn:
        result = conn.execute(
            """
            UPDATE boards SET data = ?, updated_at = datetime('now')
            WHERE user_id = (SELECT id FROM users WHERE username = ?)
            """,
            (json.dumps(data), username),
        )
    return result.rowcount > 0
