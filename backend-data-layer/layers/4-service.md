<!--
PURPOSE: Explain the Service layer — where business rules and validation live.
LAYER:   service
LAST REVIEWED: 2026-04-27
-->

# 4. Service Layer

## What this layer is

The service layer is where the *business* lives. Not the database, not the HTTP — the actual rules of your system: "a student must be at least 5 years old," "you can't register the same email twice," "after creating a student, send them a welcome email."

If the rule would still apply when you swap your database or your web framework, it belongs here.

## Single responsibility

Enforce business rules and orchestrate workflows. Decide whether an operation *should* happen, then ask the repository to do it.

## Minimal example

From `mock/app/services.py`:

```python
from sqlalchemy.orm import Session
from . import repositories
from .models import Student

class ValidationError(Exception):
    pass

def create_student(db: Session, name: str, email: str, age: int) -> Student:
    if not name.strip():
        raise ValidationError("name is required")
    if "@" not in email:
        raise ValidationError("email is not valid")
    if age < 0:
        raise ValidationError("age cannot be negative")
    if repositories.get_student_by_email(db, email) is not None:
        raise ValidationError("a student with that email already exists")

    return repositories.create_student(db, name=name, email=email, age=age)
```

The service is the only place that knows *all* the rules at once. The repository can't enforce uniqueness across business meaning ("same person, different capitalization in email") — it only knows what the DB tells it. The API can't enforce it either — it would need to import every rule.

## What does NOT belong here

- ❌ `db.query(...)` or any raw SQL → that's the repository's job
- ❌ `from fastapi import ...` → no HTTP awareness; the service must work the same if called from a CLI, a background job, or a test
- ❌ Defining the database schema → that's the model's job
- ❌ Translating exceptions to HTTP status codes → that's the API's job

The service raises *domain* exceptions (`ValidationError`, `NotFound`, `Forbidden`). The API layer translates those into HTTP.

## How it talks to neighbors

- **Imported by**: the API layer
- **Imports**: the repository layer (and sometimes other services)
- **Never imports**: FastAPI, request/response schemas, ORM session internals beyond accepting a `Session` as a parameter
- **Returns**: model instances or primitive types
- **Raises**: domain exceptions, not HTTP exceptions

The clean test for a service function: could you call it from a Jupyter notebook with a session and have it work? If yes, the boundary is clean.
