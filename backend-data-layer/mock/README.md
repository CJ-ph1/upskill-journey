# mock — `students` resource sliced through all 5 layers

A tiny FastAPI + SQLAlchemy app whose only purpose is to make the layered architecture **visible**. One resource (`students`), one path through every layer.

## What's in here

```
app/
├── models.py        ← Model:      Student class ↔ students table
├── db.py            ← ORM:        engine, session, init_db
├── repositories.py  ← Repository: the only file that runs queries
├── services.py      ← Service:    validation + business rules
└── api.py           ← API:        FastAPI routes
```

The dependency direction is strict: `api → services → repositories → db/models`. Nothing imports upward.

## Run it

```bash
cd mock
pip install -e .
uvicorn app.api:app --reload
```

Then in another terminal:

```bash
# Happy path → 201 + the new student
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Ada Lovelace", "email": "ada@example.com", "age": 28}'

# Bad email → 400 from the service layer
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Bad", "email": "no-at-sign", "age": 20}'

# Negative age → 400
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Time Traveller", "email": "tt@example.com", "age": -1}'

# List
curl http://localhost:8000/students
```

The SQLite file `students.db` will appear in this folder after the first request.

## What to observe

1. **Trace one request top-to-bottom**: open all five files, send a `POST /students`, and follow the call chain `api.create_student` → `services.create_student` → `repositories.get_student_by_email` + `repositories.create_student`. Notice how each function only knows about its layer and the one directly below.
2. **Try to break the one-job rule**: open `app/api.py` and try to write `db.query(Student)...` directly in the route. It works! But now the API layer knows about SQL, the service layer is bypassed, and validation is gone. Revert. That's why the rule exists.
3. **Watch the SQL**: change `echo=False` to `echo=True` in `app/db.py`, restart, and send a request. You'll see the actual SQL SQLAlchemy emits — proof that the ORM is just a translator.
