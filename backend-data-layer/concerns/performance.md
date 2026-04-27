<!--
PURPOSE: Explain the most common backend data-layer performance traps — N+1 and over-fetching.
LAYER:   concern
LAST REVIEWED: 2026-04-27
-->

# Performance

A correct backend can still be slow. Most of the slowness comes from a few well-known patterns. Two of them are worth memorizing because you will hit both within your first month of building anything real.

## The N+1 query problem

You fetch a list of N parents, then loop over them to fetch each one's children. That's `1` query for the parents and `N` queries for the children — `N+1` total. With 1,000 students, that's 1,001 round trips to the database.

```python
# ❌ N+1
students = db.query(Student).all()                  # 1 query
for s in students:
    print(s.name, [c.title for c in s.courses])     # N queries (one per student)
```

The fix is to tell the ORM to fetch the children in the same trip:

```python
# ✅ One query (or two, batched), via a JOIN or IN
from sqlalchemy.orm import joinedload

students = (
    db.query(Student)
      .options(joinedload(Student.courses))
      .all()
)
```

The names differ by ORM (`joinedload`, `selectinload`, `prefetch_related`, `include`), but the concept is universal: **if you're about to loop over a list and access a relationship, load that relationship eagerly first.**

How to spot N+1: enable SQL echo (`create_engine(..., echo=True)`) and watch the log when you hit the endpoint. A burst of identical queries with different IDs is the giveaway.

## Over-fetching

Asking for more data than you'll use. Two flavors:

**Too many columns:**
```python
# Returns every column on Student even if the page only shows name + email
students = db.query(Student).all()
```
Use column projection when the table has heavy columns (text blobs, JSON, binary):
```python
db.query(Student.id, Student.name, Student.email).all()
```

**Too many rows:**
```python
# Fetches all 50,000 students to render page 1
students = db.query(Student).all()
```
Always paginate at the DB:
```python
db.query(Student).order_by(Student.id).limit(20).offset(page * 20).all()
```

## The other usual suspects

- **Missing indexes** on columns you filter or join on. The query plan (`EXPLAIN`) tells you. Add an index on any column that appears regularly in `WHERE` or `JOIN`.
- **Doing work in Python that the DB can do in SQL** — sorting, filtering, aggregating in a loop after `db.query(...).all()` instead of in the query itself.
- **Open transactions held too long** — fetch, do slow work (HTTP call, big computation), then commit. Other writers wait. Move the slow work outside the transaction.

## The mindset

Performance work is mostly about **counting database round trips**. If a single API request fires more than a handful of queries, ask why. The ORM hides this from you on purpose — your job is to not be fooled.
