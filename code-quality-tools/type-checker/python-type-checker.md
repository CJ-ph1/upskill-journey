<!--
PURPOSE: Explain how a type checker works in Python and how to set up MyPy.
COVERS:  MyPy for Python.
PATTERNS: Annotate public APIs; turn on strict mode incrementally; treat type errors as build failures.
LAST REVIEWED: 2026-04-27
-->

# Python Type Checker — MyPy

## What a type checker does (Python)

A type checker analyzes **type annotations** in Python source and verifies that values flow through your functions in compatible types — without ever running the code.

Python is dynamically typed at runtime, but with type hints (`def f(x: int) -> str:`) a static checker can catch a large class of bugs early: passing a `str` where an `int` was expected, returning `None` from a function annotated `-> User`, accessing an attribute that doesn't exist on a class, etc.

## Tool used

**MyPy** — the original and most widely used Python type checker. (Pyright is a faster alternative used by Pylance/VS Code, but MyPy is the default choice for CI and matches Python's official typing PEPs closely.)

Why MyPy is the default choice:
- Mature, widely supported, well documented
- Strict mode catches the things that matter
- Per-module config — you can roll out strict typing gradually
- Plays well with `pyproject.toml`

## What it CAN do

- Catch wrong-type arguments at call sites
- Catch wrong return types
- Detect `None` flowing into a non-Optional value
- Verify generics (`list[int]`, `dict[str, User]`)
- Cross-module checking — type errors that span files
- Improve IDE autocomplete because the types are now machine-readable

## What it CANNOT do

- Check anything you didn't annotate (no annotations = no signal)
- Catch logical bugs — `def add(a: int, b: int) -> int: return a - b` is type-correct
- Run your code — it can't catch issues that depend on runtime values
- Help much in highly dynamic code (heavy `getattr`, `**kwargs`, metaprogramming)

## Before / after

**Before:**

```python
def add(a: int, b: int) -> int:
    return a + b

result = add("1", "2")           # passing strings to int params
print(result.upper())            # calling .upper() on declared int
```

**MyPy reports:**

```
error: Argument 1 to "add" has incompatible type "str"; expected "int"
error: Argument 2 to "add" has incompatible type "str"; expected "int"
error: "int" has no attribute "upper"
```

## How to set it up

### 1. Install

```bash
pip install mypy
```

Or pin in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["mypy>=1.10"]
```

### 2. Configure

Add to `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.11"
strict = true                     # enables a strong default rule set
warn_unused_ignores = true
warn_return_any = true
ignore_missing_imports = true     # for third-party libs without type stubs

# Loosen rules per package while you migrate (optional)
[[tool.mypy.overrides]]
module = "legacy.*"
strict = false
```

### 3. Run it

```bash
# Type-check the whole project
mypy .

# Just one package
mypy src/
```

`mypy` exits non-zero on errors, so it works in CI without extra flags.

### 4. IDE integration

VS Code's Python extension uses Pylance/Pyright for live feedback while typing. Use MyPy on commits and in CI as the source of truth — the tools sometimes disagree on edge cases.

### 5. Wire it into commits

See `git-hooks-system/python-git-hooks-system.md` — `pre-commit` runs MyPy on every commit and blocks if type errors are present.

## See it run

Open `set-up/python/` and commit `src/messy.py`. MyPy reports the wrong-type call and any missing annotations.
