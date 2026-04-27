# backend-data-layer

How a backend system moves data — safely, cleanly, and one layer at a time — from an HTTP request down to a database row, and back. Stack: **Python + SQLAlchemy + FastAPI + SQLite**.

## The mental model

```
HTTP request
   ↓
API           ← FastAPI route, talks HTTP only
   ↓
Service       ← business rules, validation
   ↓
Repository    ← the only place that touches the DB
   ↓
ORM (SQLAlchemy)  ← Python objects ↔ SQL
   ↓
Model         ← class that mirrors a table
   ↓
Database
```

Every layer has exactly one job. Mixing jobs across layers is the bug this topic exists to prevent.

## What's in here

- **`reference.txt`** — the canonical one-page summary of the whole topic (source of truth).
- **`layers/`** — one doc per layer (model, ORM, repository, service, API). Each follows the same five-section shape so they're easy to compare.
- **`concerns/`** — cross-cutting issues that don't live in any single layer: SQL injection, performance (N+1, over-fetching), consistency (transactions, race conditions).
- **`mock/`** — a runnable mini-app: a `students` resource sliced through all five layers. This is where you actually see the architecture work.
- **`CLAUDE.md`** — the rules for editing this folder + the learning checklist that drives the progress %.

## Quick start

```bash
cd mock
pip install -e .
uvicorn app.api:app --reload
# in another terminal:
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Ada Lovelace", "email": "ada@example.com", "age": 28}'
```

You should see a `201` back, and a new row in `mock/students.db`.

## Suggested reading order

1. `reference.txt` — get the big picture
2. `layers/1-model.md` → `layers/5-api.md` — bottom-up, one layer at a time
3. Run `mock/` and trace one request through the code while it runs
4. `concerns/*.md` — once the layers feel natural, learn what still goes wrong across them
