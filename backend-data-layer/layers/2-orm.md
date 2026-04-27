<!--
PURPOSE: Explain the ORM layer — SQLAlchemy translates Python objects to SQL and back.
LAYER:   orm
LAST REVIEWED: 2026-04-27
-->

# 2. ORM Layer (SQLAlchemy)

## What this layer is

The ORM (Object-Relational Mapper) is the translator between two worlds: Python objects and SQL rows. You write `session.query(Student).all()` and SQLAlchemy emits `SELECT * FROM students`, runs it, and hands you back a list of `Student` instances.

Strictly speaking, the ORM isn't really a "layer" you build — it's a tool the repository layer uses. But it's worth treating as its own concept because misunderstanding it leaks bugs everywhere.

## Single responsibility

Convert Python ↔ SQL. Manage the connection, the session, and the unit of work.

## Minimal example

From `mock/app/db.py`:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

engine = create_engine("sqlite:///./students.db", echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

That's the entire ORM setup. The repository layer pulls a session from `get_session()` and uses it.

## Why this exists

Without an ORM, you write SQL strings by hand:

```python
cursor.execute(f"SELECT * FROM students WHERE email = '{email}'")  # 💥 SQL injection
```

With an ORM:

```python
db.query(Student).filter(Student.email == email).first()  # safe, parameterized
```

You get:
- Parameterized queries by default (huge security win)
- A consistent Python API across SQLite, Postgres, MySQL
- Automatic mapping from rows back into objects
- Transactions and a session-scoped unit of work

## What does NOT belong here

- ❌ Business rules ("only adults can be added") — that's the service layer
- ❌ HTTP-aware error handling — that's the API layer
- ❌ Specific query functions like `get_student_by_email` — those live in the repository

The ORM is *infrastructure*. It should feel boring.

## ⚠️ ORM is NOT magic safety

This is the most common misconception. The ORM is safe **only when used correctly**. The moment you drop into raw SQL via `session.execute(...)` and string-format user input into it, you're back to SQL injection territory:

```python
# ❌ Unsafe — user input is concatenated into the SQL string
session.execute(f"SELECT * FROM students WHERE email = '{email}'")

# ✅ Safe — parameterized
session.execute(
    text("SELECT * FROM students WHERE email = :email"),
    {"email": email},
)

# ✅ Safer still — use the ORM API, not raw SQL
db.query(Student).filter(Student.email == email).first()
```

See `concerns/sql-injection.md` for more.

## How it talks to neighbors

- **Imported by**: the repository layer (which uses the session)
- **Imports**: the model classes (so it knows what tables exist)
- **Never touches**: HTTP, services, validation
