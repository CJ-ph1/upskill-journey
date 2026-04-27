# CLAUDE.md — backend-data-layer

This folder is a personal knowledge base about how a backend system moves data safely from an HTTP request all the way down to a database row — and back. When working in this folder, follow the rules below.

## Source of truth

`reference.txt` is the canonical summary of the layered architecture (Model → ORM → Repository → Service → API) and the cross-cutting concerns. Everything in `layers/` and `concerns/` expands on it but **must not contradict it**. If a contradiction shows up, fix the doc — not `reference.txt`.

## Scope

Stack is intentionally pinned to **Python + SQLAlchemy + FastAPI + SQLite**. Other stacks (Django ORM, Prisma, Node, Go) are out of scope unless the user explicitly asks. The point of the topic is to learn the *shape* of a layered data pipeline — the language is just a vehicle.

## The one-job rule

Every layer has exactly one responsibility. This is the property the topic exists to teach, and the property the `mock/` exists to demonstrate. Concretely:

| Layer        | Owns                          | Must NOT contain                       |
|--------------|-------------------------------|----------------------------------------|
| `models.py`  | table schema, column types    | validation, queries, business rules    |
| ORM session  | Python ↔ SQL translation      | (no logic — it's a tool, not a layer)  |
| `repositories.py` | DB read/write functions  | validation, HTTP, business decisions   |
| `services.py`| business rules, validation    | raw SQL, FastAPI imports               |
| `api.py`     | HTTP routes, request/response | SQL, business rules                    |

If you catch yourself putting SQL in `api.py` or validation in `models.py`, that's a bug worth flagging — not a shortcut.

## Module headers required

Every `.md` file in this folder — except top-level `README.md` and `reference.txt` — must start with this header block:

```
<!--
PURPOSE: one sentence on what this doc is for
LAYER:   model | orm | repository | service | api | concern
LAST REVIEWED: YYYY-MM-DD
-->
```

When editing a doc, update `LAST REVIEWED` to today's date.

## Layer-doc shape

The five files in `layers/` should each follow the same five-section shape so they're easy to scan side by side:

1. **What this layer is** — one paragraph
2. **Single responsibility** — one sentence, plain English
3. **Minimal example** — code lifted from `mock/` (don't invent toy examples — keep the doc and the mock in sync)
4. **What does NOT belong here** — explicit anti-patterns
5. **How it talks to neighbors** — what it imports, what it returns, what it never touches

## Mock project

`mock/` is a runnable mini-app (a `students` resource) sliced cleanly through all five layers. Its value is that you can `POST /students`, watch the request flow API → Service → Repository → ORM → DB, and inspect the result. Do not break this property:

- Each file in `mock/app/` stays inside its layer
- `mock/README.md` explains how to run it and what to observe
- The mock is the source of all code examples in `layers/*.md`

## Learning checklist

This checklist defines what "100% learned" means for this topic. The percentage shown in `../README.md` is computed as `checked / total`. Update boxes as you actually read, run, or apply each item — not just because the file exists.

**Concepts (8 items)**
- [ ] Read `layers/1-model.md` — understand OOP-to-table mapping
- [ ] Read `layers/2-orm.md` — understand what SQLAlchemy does and doesn't do
- [ ] Read `layers/3-repository.md` — understand the DB-access boundary
- [ ] Read `layers/4-service.md` — understand where business rules live
- [ ] Read `layers/5-api.md` — understand the HTTP boundary
- [ ] Read `concerns/sql-injection.md` — explain why ORM is not magic safety
- [ ] Read `concerns/performance.md` — explain N+1 and over-fetching
- [ ] Read `concerns/consistency.md` — explain transactions and race conditions

**Hands-on (4 items)**
- [ ] Run `mock/` end-to-end: `POST /students` → row appears in the SQLite file
- [ ] Break the one-job rule on purpose (e.g. drop SQL into `api.py`), then revert — feel why it's bad
- [ ] Add a second resource (e.g. `courses`) sliced through all 5 layers
- [ ] Apply the layered structure to one real project at work

> The journey-level scanner reads only `- [ ]` and `- [x]` lines under "## Learning checklist" to compute the percentage. Don't rename this heading.
