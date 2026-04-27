<!--
PURPOSE: Walk through how each issue in src/messy.py gets fixed (or flagged) as pre-commit runs, stage by stage, with exact copy-paste blocks you can use to reproduce each stage.
COVERS:  Black, Ruff, MyPy on the Python mock project — what changes after each commit attempt.
PATTERNS: Track the file across the pipeline; auto-fixers run first, type checker last; manual fixes only where tools can't.
LAST REVIEWED: 2026-04-27
-->

# Fixing `messy.py` step by step (copy-paste guide)

This doc tracks `src/messy.py` as it moves through the pre-commit pipeline. For each stage you get:

- **Copy this** — paste the exact contents into `src/messy.py`
- **Run** — the exact commands to type
- **What you should see** — the expected output

Pipeline order:

1. **Black** — formatter (auto-rewrites)
2. **Ruff** — linter (auto-fixes what's safe, flags the rest)
3. **MyPy** — type checker (never rewrites; only reports)

A commit only succeeds when all three pass with the file unchanged.

> **Tip:** keep `src/messy.py` open in your editor. After each `git commit`, reload the file in the editor — the auto-fixers rewrite it on disk, and watching the file change is the whole point of this exercise.

---

## Stage 0 — Reset `src/messy.py` to the broken version

**Copy this** into `src/messy.py` (overwrite whatever's there):

```python
def add(a: int,b: int)->int:
    return a - b  # bad spacing + logic bug (subtraction in `add`)


def greet(name):  # missing annotations
    msg = "hello, " + name
    extra = 42  # unused variable
    return msg


def total(prices: list[float]) -> float:
    return sum(prices)


# Type error MyPy will catch
result: int = add("1", "2")
print(result)
```

Issues planted:

| # | Issue                                  | Tool that catches it | Auto-fixable? |
|---|----------------------------------------|----------------------|---------------|
| 1 | Bad spacing around `,` and `->`        | Black                | Yes           |
| 2 | Logic bug: `add` returns `a - b`       | None (humans only)   | No            |
| 3 | Missing annotations on `greet`         | MyPy (strict)        | No            |
| 4 | Unused local `extra = 42` (F841)       | Ruff                 | Yes           |
| 5 | `add("1", "2")` — `str` where `int`    | MyPy                 | No            |

**Run:**

```bash
git add src/messy.py
git commit -m "stage 0: messy"
```

---

## Stage 1 — Black rewrites the formatting

**What you should see:** Black modifies the file and pre-commit aborts with *"files were modified by this hook"*. Look at the bottom of the output for something like:

```
black....................................................................Failed
- hook id: black
- files were modified by this hook
reformatted src/messy.py
```

**Reload `src/messy.py` in your editor.** Black has rewritten it. The spacing around `,` and `->` is now normalized:

```python
def add(a: int, b: int) -> int:
    return a - b  # logic bug still here


def greet(name):
    msg = "hello, " + name
    extra = 42
    return msg


def total(prices: list[float]) -> float:
    return sum(prices)


result: int = add("1", "2")
print(result)
```

**Run** (re-stage the rewrite and try again):

```bash
git add src/messy.py
git commit -m "stage 1: after black"
```

---

## Stage 2 — Ruff flags the unused variable (but won't auto-fix it)

**What you should see:** Black is happy now. Ruff fires next, finds `extra = 42`, but **does not delete it** — it reports the error and exits non-zero. MyPy still runs and reports its own errors:

```
black....................................................................Passed
ruff.....................................................................Failed
- hook id: ruff
- exit code: 1

src/messy.py:7:5: F841 Local variable `extra` is assigned to but never used
Found 1 error.
No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).

mypy.....................................................................Failed
- hook id: mypy
src/messy.py:5: error: Function is missing a type annotation  [no-untyped-def]
src/messy.py:16: error: Argument 1 to "add" has incompatible type "str"; expected "int"
src/messy.py:16: error: Argument 2 to "add" has incompatible type "str"; expected "int"
Found 3 errors in 1 file (checked 1 source file)
```

**Why didn't Ruff auto-fix it?** Ruff splits fixes into **safe** and **unsafe**. Removing an assignment is unsafe — the right-hand side could in theory have a side effect (`extra = some_call()`), so Ruff refuses to delete it without you opting in via `--unsafe-fixes`. F841 falls in that bucket. The hint *"1 hidden fix can be enabled with the `--unsafe-fixes` option"* is Ruff telling you exactly that.

You have two options:

**Option A (recommended for this exercise) — fix it by hand.** Open `src/messy.py` and delete the `extra = 42` line so the file looks like this:

```python
def add(a: int, b: int) -> int:
    return a - b


def greet(name):
    msg = "hello, " + name
    return msg


def total(prices: list[float]) -> float:
    return sum(prices)


result: int = add("1", "2")
print(result)
```

**Option B — let Ruff auto-fix unsafe rules.** Edit `.pre-commit-config.yaml` and change the ruff `args` line to:

```yaml
      - id: ruff
        args: [--fix, --unsafe-fixes]
```

Then re-stage and re-commit; Ruff will delete the line for you.

**Run** (after either option):

```bash
git add src/messy.py
git commit -m "stage 2: after ruff"
```

---

## Stage 3 — MyPy is the only thing left failing

**What you should see:** Black and Ruff both pass now. MyPy still fails — it never rewrites the file, it just reports:

```
black....................................................................Passed
ruff.....................................................................Passed
mypy.....................................................................Failed
- hook id: mypy
src/messy.py:5: error: Function is missing a type annotation  [no-untyped-def]
src/messy.py:14: error: Argument 1 to "add" has incompatible type "str"; expected "int"  [arg-type]
src/messy.py:14: error: Argument 2 to "add" has incompatible type "str"; expected "int"  [arg-type]
Found 3 errors in 1 file (checked 1 source file)
```

> Note: MyPy already ran in Stage 2 (pre-commit runs every hook even when an earlier one fails) — you saw the same errors there. The only difference now is that MyPy is the *only* failure left.

These need to be fixed by hand. Move on to Stage 4.

---

## Stage 4 — Manually fix the type errors (and the logic bug)

**Copy this** into `src/messy.py` (this is the final, clean version):

```python
def add(a: int, b: int) -> int:
    return a + b


def greet(name: str) -> str:
    msg = "hello, " + name
    return msg


def total(prices: list[float]) -> float:
    return sum(prices)


result: int = add(1, 2)
print(result)
```

What changed vs. Stage 3:

- `a - b` → `a + b` (the logic bug — **no tool caught this**, you have to)
- `def greet(name):` → `def greet(name: str) -> str:` (annotations for MyPy)
- `add("1", "2")` → `add(1, 2)` (correct types at the call site)

**Run:**

```bash
git add src/messy.py
git commit -m "stage 4: clean"
```

**What you should see:**

```
black....................................................................Passed
ruff.....................................................................Passed
mypy.....................................................................Passed
[main abc1234] stage 4: clean
```

---

## Summary table

| Stage | Tool  | Issues fixed                    | Issues left after stage                          |
|-------|-------|---------------------------------|--------------------------------------------------|
| 1     | Black | Formatting                      | Unused var, missing annotations, str→int, logic  |
| 2     | Ruff  | Flags F841 (you delete it by hand, or enable `--unsafe-fixes`) | Missing annotations, str→int, logic |
| 3     | MyPy  | — (reports only)                | Logic bug in `add` (no tool catches this)        |
| 4     | Human | Annotations, call site, logic   | None                                             |

---

## What this exercise proves

- **Auto-fixers run first, type checker last.** Black and Ruff settle the file into a stable shape before MyPy reasons about it.
- **A single commit will be rejected several times** on a freshly-broken file: Black rewrites and aborts, then Ruff and MyPy report errors you have to address. That's normal — re-stage and continue.
- **Ruff distinguishes safe vs unsafe fixes.** With plain `--fix`, it only rewrites things that can't change behavior. Removing an unused assignment is "unsafe" because the right-hand side might have side effects, so by default Ruff flags F841 instead of deleting it. Add `--unsafe-fixes` if you want it auto-deleted.
- **Tools cover formatting, lint rules, and types. They do not cover *intent*.** The `a - b` bug in `add` is the reminder.

---

## Reset and replay

To run the whole thing again from scratch, just paste the **Stage 0** block back into `src/messy.py` and start over. Nothing else needs to be reset — the venv, pre-commit hook, and pyproject config all stay in place.
