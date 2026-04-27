<!--
PURPOSE: Explain the API layer — the HTTP boundary that turns requests into service calls.
LAYER:   api
LAST REVIEWED: 2026-04-27
-->

# 5. API Layer

## What this layer is

The API layer is the **edge** of the application — the place where HTTP enters and leaves. It parses incoming JSON into Python types, hands them to a service, takes the result, and serializes it back to JSON with an appropriate status code.

That is its entire job. It is not where you write business rules, and it is not where you write SQL.

## Single responsibility

Translate between HTTP and the service layer. Nothing else.

## Minimal example

From `mock/app/api.py`:

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import services
from .db import get_session, init_db

app = FastAPI()
init_db()

class StudentIn(BaseModel):
    name: str
    email: str
    age: int

class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    age: int

    class Config:
        from_attributes = True

@app.post("/students", response_model=StudentOut, status_code=201)
def create_student(payload: StudentIn, db: Session = Depends(get_session)):
    try:
        return services.create_student(
            db, name=payload.name, email=payload.email, age=payload.age,
        )
    except services.ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

The route is five lines of real work: call the service, catch the domain exception, translate to HTTP. That's the whole pattern.

## What does NOT belong here

- ❌ `db.query(Student).filter(...)` → repository
- ❌ `if "@" not in payload.email: raise ...` → service (the API only enforces *shape*, via Pydantic; the service enforces *meaning*)
- ❌ Sending welcome emails inline in the route → service (or a background task triggered by it)
- ❌ Reaching across resources ("on student creation, also create a Course") → service

A good rule of thumb: a route function should be short enough to fit on one screen, and most of it should be I/O glue. If a route is doing real thinking, push that thinking down into the service.

## How it talks to neighbors

- **Imports**: services, Pydantic schemas, FastAPI, the session dependency
- **Never imports**: models directly (use Pydantic schemas at the boundary), repositories directly (always go through a service)
- **Catches**: domain exceptions from the service, maps them to HTTP status codes
- **Returns**: serialized response models

## The dependency direction

The whole point of the layered structure is that dependencies point *down*:

```
api  → service  → repository  → orm  → model
```

Nothing points back up. The model doesn't know there's an API. The service doesn't know there's a FastAPI route calling it. That's what makes each layer testable and replaceable in isolation.
