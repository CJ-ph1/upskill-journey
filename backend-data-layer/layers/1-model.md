<!--
PURPOSE: Explain the Model layer — a Python class that mirrors a database table.
LAYER:   model
LAST REVIEWED: 2026-04-27
-->

# 1. Model Layer

## What this layer is

The Model layer is where OOP meets the database. A model is a Python class whose attributes describe the columns of a single table. When the ORM loads a row, it hands you back an instance of this class. When you set attributes on an instance and commit, the ORM writes a row.

The model is a **shape declaration**. It does not know how to query, validate, or talk to HTTP. It only knows what a `Student` *is*.

## Single responsibility

Describe the table's structure — column names, types, constraints, relationships. Nothing else.

## Minimal example

From `mock/app/models.py`:

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
```

That's the whole file. No methods, no validation, no queries.

## What does NOT belong here

- ❌ `def is_valid_email(self): ...` → that's a service-layer rule
- ❌ `@classmethod def get_by_email(cls, db, email): ...` → that's a repository function
- ❌ Calling `session.commit()` from inside the model → that's an ORM/repository concern
- ❌ Importing FastAPI, Pydantic request schemas, or HTTP types
- ❌ Default values that encode business policy (e.g. `is_active = True` "because new users start active") — that's a service decision

A model with methods on it slowly turns into a god-object. Resist.

## How it talks to neighbors

- **Imported by**: the ORM session, the repository layer, sometimes the service layer for type hints
- **Imports**: only SQLAlchemy primitives (`Column`, `String`, `Base`, `relationship`)
- **Never touches**: HTTP, validation libraries, business logic, the session itself

The model is the most "downstream" piece of code in the stack — it's just a shape. Everyone else looks at it; it looks at no one.
