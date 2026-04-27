<!--
PURPOSE: Runnable mock Python project demonstrating Black + Ruff + MyPy + pre-commit.
COVERS:  All four tool categories for Python wired into one git pre-commit hook.
PATTERNS: One commit triggers formatter, linter, and type checker; commit blocks until clean.
LAST REVIEWED: 2026-04-27
-->

# Python Mock Project — see all four tools fire on one commit

This is a real, runnable Python project. It contains one intentionally messy file (`src/messy.py`) that has bad formatting, lint issues, and type errors all at once. Commit it and watch every tool fire.

## What's in this folder

| File                      | What it does                                            |
|---------------------------|---------------------------------------------------------|
| `pyproject.toml`          | Configures Black, Ruff, and MyPy in one file            |
| `.pre-commit-config.yaml` | Wires Black, Ruff, MyPy into the git pre-commit hook    |
| `.gitignore`              | Standard Python ignores                                 |
| `src/messy.py`            | The deliberately broken file you'll commit              |

## One-time setup

From inside `set-up/python/`:

```bash
# 1. Create and activate a virtual env (Windows PowerShell shown; use bash on macOS/Linux)
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Install the four tools
pip install -e ".[dev]"

# 3. Initialize a git repo here so hooks have somewhere to live
git init

# 4. Install the pre-commit hooks into .git/hooks/
pre-commit install
```

## Run the demo

```bash
git add .
git commit -m "test"
```

Expected output (in this order):

1. **Black** rewrites `src/messy.py` (fixes spacing, indentation, quotes). The commit is rejected with "files were modified by this hook".
2. You re-stage the changes:
   ```bash
   git add src/messy.py
   git commit -m "test"
   ```
3. **Black** now passes.
4. **Ruff** auto-fixes the unused imports and unused variable, then reports anything it can't fix. If anything was rewritten, re-stage and commit again.
5. **MyPy** reports type errors:
   - missing annotations on `greet`
   - `add("1", "2")` — `str` passed where `int` expected
6. The commit stays blocked until you fix the type errors by hand. Edit `src/messy.py`, re-stage, commit again.

When everything passes, the commit completes.

## Run individual tools manually

```bash
# Format
black .

# Lint (and auto-fix what's safe)
ruff check . --fix

# Type-check
mypy .

# Run all hooks across all files (not just staged)
pre-commit run --all-files
```

## Concept docs

For the "why" and deeper explanation of each tool:

- `formatter/python-formatter.md` — Black
- `linter/python-linter.md` — Ruff
- `type-checker/python-type-checker.md` — MyPy
- `git-hooks-system/python-git-hooks-system.md` — pre-commit
