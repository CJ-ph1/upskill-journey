<!--
PURPOSE: Explain transactions, race conditions, and how to keep data consistent under concurrency.
LAYER:   concern
LAST REVIEWED: 2026-04-27
-->

# Consistency

A backend that's correct for one user at a time can still corrupt data when two users hit it at the same instant. This concern is about the rules that keep things sane when more than one thing is happening.

## Transactions: all-or-nothing

A transaction groups multiple database operations into a single unit. Either *all* of them happen, or *none* of them do. There is no in-between.

```python
# ✅ Both happen, or neither does
def transfer(db, from_id, to_id, amount):
    sender = db.query(Account).get(from_id)
    receiver = db.query(Account).get(to_id)
    sender.balance -= amount
    receiver.balance += amount
    db.commit()    # commit point — both updates land together
```

If the process crashes between the two updates, the transaction rolls back and neither change is applied. Without a transaction, you'd lose money (sender debited, receiver never credited) — a class of bug that is genuinely hard to recover from.

Rule of thumb: any operation that mutates **more than one row** belongs in a transaction. SQLAlchemy's session is already a transactional unit of work — your job is to commit at the right boundary (usually once per service-layer call) and not in the middle.

## Race conditions

Two requests read the same row, both modify it based on what they read, both write it back. The second write silently overwrites the first.

The classic example is the "check-then-act" race:

```python
# ❌ Race condition
existing = repositories.get_student_by_email(db, email)
if existing is None:
    repositories.create_student(db, name, email, age)
```

Two requests with the same email arrive at the same moment. Both check, both see `None`, both insert. Now you have two students with the same email — even though your service logic says you can't.

### Three ways to fix it

1. **Database constraints** (best when possible). Put a `UNIQUE` constraint on `email`. The DB will refuse the second insert and raise an error you can translate to a clean 409 Conflict. The DB enforces invariants better than your app ever will.

2. **Locking the row you're about to update**:
   ```python
   row = db.query(Student).filter(...).with_for_update().first()
   ```
   Other writers wait. Use sparingly — it serializes access.

3. **Optimistic concurrency**: include a `version` column. On update, `WHERE id = ? AND version = ?`. If the version moved, your update affects 0 rows and you know to retry. Good for low-contention writes.

## Isolation levels (one-line version)

Databases offer different "isolation levels" that trade consistency for throughput. Defaults vary (Postgres: `READ COMMITTED`; SQLite: serialized in practice). For most CRUD apps the default is fine; the moment you start computing balances, inventory, or anything where two readers must not see partial updates, look up `REPEATABLE READ` and `SERIALIZABLE` properly.

## In this topic's stack

- The mock uses SQLite, which serializes writes for us — so race conditions are hard to demonstrate live. The pattern still matters because production almost certainly won't be SQLite.
- The right place to handle the race in `services.create_student` is to add a `UNIQUE` constraint on `Student.email` (already in the model) and catch `IntegrityError` from the repository, then translate to `ValidationError`.
