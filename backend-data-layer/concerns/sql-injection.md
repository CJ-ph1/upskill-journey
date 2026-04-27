<!--
PURPOSE: Explain SQL injection and why an ORM is not automatic protection.
LAYER:   concern
LAST REVIEWED: 2026-04-27
-->

# SQL Injection

## What it is

SQL injection happens when user input is treated as part of the SQL query *text* instead of as a *value*. The user types something that, when concatenated into the query string, changes what the query means.

```python
email = request.json["email"]  # attacker sends:  ' OR '1'='1
query = f"SELECT * FROM students WHERE email = '{email}'"
# becomes: SELECT * FROM students WHERE email = '' OR '1'='1'
# → returns every row in the table
```

Worse versions can drop tables, exfiltrate data, or escalate privileges.

## The fix: parameterized queries

Send the SQL and the values to the database as **separate things**. The database treats values as values, no matter what characters they contain.

```python
# ✅ Parameterized — the driver handles escaping
session.execute(
    text("SELECT * FROM students WHERE email = :email"),
    {"email": email},
)

# ✅ ORM API — same protection, plus you don't write SQL by hand
db.query(Student).filter(Student.email == email).first()
```

## Why ORM is NOT magic safety

A common assumption is "we use SQLAlchemy, so we're safe." That's only true when you let the ORM build the query. The moment you drop into raw SQL with `session.execute(...)` and string-format the input, the ORM has nothing to do with it — you've written a raw query, and the raw rules apply:

```python
# ❌ Unsafe — even though it's "in SQLAlchemy"
session.execute(f"SELECT * FROM students WHERE email = '{email}'")
```

The pattern to internalize: **never put user input into a SQL string with `+`, `%`, or `f"..."`**. If your fingers are typing those characters next to `SELECT`, stop.

## Defense in depth

ORM-correct queries are the main line of defense. Add:

- **Input validation** at the service layer: reject obviously malformed input early (not as security, but as good hygiene)
- **Least-privilege DB users**: the app's DB user should not have `DROP TABLE` if it never needs it
- **Code review / grep checks**: search for `f"SELECT`, `f"INSERT`, `f"DELETE` in the codebase periodically
- **Logging**: log slow or anomalous queries so injection attempts that hit a real query show up

## In this topic's stack

- All SQL goes through `mock/app/repositories.py`, and only via the SQLAlchemy ORM API (`db.query(...).filter(...)`).
- The grep test: `grep -rn "f\"SELECT\|f\"INSERT\|f\"UPDATE\|f\"DELETE" mock/` should return zero hits.
