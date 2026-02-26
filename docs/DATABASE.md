# Database Design

## Technology

SQLite — single-file, zero-config, ships inside the Docker container. No separate database process needed.

## Schema

```sql
CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT    NOT NULL UNIQUE,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE boards (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    data        TEXT    NOT NULL,   -- JSON blob: BoardData { columns, cards }
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

## Design decisions

### JSON blob for board data

The entire board (`columns` array + `cards` record) is stored as a single JSON string in `boards.data`. This mirrors the frontend `BoardData` type exactly:

```json
{
  "columns": [
    { "id": "col-backlog", "title": "Backlog", "cardIds": ["card-1", "card-2"] }
  ],
  "cards": {
    "card-1": { "id": "card-1", "title": "Align roadmap themes", "details": "..." }
  }
}
```

**Why not fully normalized tables (columns/cards as separate rows)?**
- The frontend reads and writes the whole board at once — a JSON blob maps directly with no translation
- Column ordering is intrinsic to the `columns` array; a separate table needs an explicit position column
- Card-to-column membership is encoded in `column.cardIds` order — a junction table loses that ordering naturally
- A JSON blob is trivially serializable/deserializable in both Python and TypeScript

This can be normalized in a future part if query-level filtering of cards is needed.

### One board per user

Each user gets exactly one board. The `boards` table supports multiple rows per user (via `user_id`) to allow for future multi-board support without a schema change.

### Passwords not stored

Authentication is hardcoded in the frontend (Part 4). The `users` table exists only to key board data to a username. Password storage will be addressed if real auth is added later.

## Seed data

```sql
INSERT INTO users (username) VALUES ('user');

INSERT INTO boards (user_id, data) VALUES (
    1,
    '{
        "columns": [
            {"id": "col-backlog",   "title": "Backlog",     "cardIds": ["card-1","card-2"]},
            {"id": "col-discovery", "title": "Discovery",   "cardIds": ["card-3"]},
            {"id": "col-progress",  "title": "In Progress", "cardIds": ["card-4","card-5"]},
            {"id": "col-review",    "title": "Review",      "cardIds": ["card-6"]},
            {"id": "col-done",      "title": "Done",        "cardIds": ["card-7","card-8"]}
        ],
        "cards": {
            "card-1": {"id":"card-1","title":"Align roadmap themes",    "details":"Draft quarterly themes with impact statements and metrics."},
            "card-2": {"id":"card-2","title":"Gather customer signals",  "details":"Review support tags, sales notes, and churn feedback."},
            "card-3": {"id":"card-3","title":"Prototype analytics view", "details":"Sketch initial dashboard layout and key drill-downs."},
            "card-4": {"id":"card-4","title":"Refine status language",   "details":"Standardize column labels and tone across the board."},
            "card-5": {"id":"card-5","title":"Design card layout",       "details":"Add hierarchy and spacing for scanning dense lists."},
            "card-6": {"id":"card-6","title":"QA micro-interactions",    "details":"Verify hover, focus, and loading states."},
            "card-7": {"id":"card-7","title":"Ship marketing page",      "details":"Final copy approved and asset pack delivered."},
            "card-8": {"id":"card-8","title":"Close onboarding sprint",  "details":"Document release notes and share internally."}
        }
    }'
);
```

## File location

The database file will be created at `backend/kanban.db` on first startup. It is excluded from version control via `.gitignore`.
