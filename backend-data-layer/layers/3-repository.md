<!--
PURPOSE: Explain the Repository layer — the only place in the codebase that talks to the database.
LAYER:   repository
LAST REVIEWED: 2026-04-27
-->

# 3. Repository Layer

## What this layer is

The repository is a thin wall around the database. Every read, write, update, or delete that hits the DB goes through a function in this file. Nothing else in the codebase is allowed to touch a session or write a query.

That sounds like overkill until the first time you need to swap SQLite for Postgres, add caching, add a read replica, or audit every place a `students` row is read. Then it pays for itself.

## Single responsibility

Database access. That's it. Take a session and some plain inputs, return model objects (or `None`, or lists). No business decisions about whether the operation *should* happen.

## Minimal example

From `mock/app/repositories.py`:

```python
from sqlalchemy.orm import Session
from .models import Student

def get_student_by_email(db: Session, email: str) -> Student | None:
    return db.query(Student).filter(Student.email == email).first()

def list_students(db: Session) -> list[Student]:
    return db.query(Student).all()

def create_student(db: Session, name: str, email: str, age: int) -> Student:
    student = Student(name=name, email=email, age=age)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
```

Notice what's missing: no email-format checks, no "is the user allowed to do this," no HTTP status codes. Just the database operation.

## What does NOT belong here

- ❌ `if not email_is_valid(email): raise ...` → service layer
- ❌ `raise HTTPException(404, ...)` → API layer
- ❌ Sending welcome emails after creation → service layer (or a dedicated notifications layer)
- ❌ Computing derived state ("is this student senior or junior") → service layer

The repository is the *only* layer where a `db.query(...)` or `db.execute(...)` call is allowed to appear. If you grep the codebase for `db.query` and find a hit outside this file, that's a bug.

## How it talks to neighbors

- **Imported by**: the service layer
- **Imports**: models, SQLAlchemy session types
- **Returns**: model instances or primitive types — never HTTP responses, never raises HTTP errors
- **Receives**: a session (passed in by the caller — the repository never creates sessions itself)

The session-in / models-out pattern is what makes the repository easy to test. You hand it a test session, you get back model objects, no FastAPI required.
