<!--
PURPOSE: Explain how git hooks work in Python projects and how to set up pre-commit.
COVERS:  pre-commit framework wiring Black, Ruff, and MyPy on commit.
PATTERNS: Run on staged files; auto-fix safe issues; block commit on type errors.
LAST REVIEWED: 2026-04-27
-->

# Python Git Hooks — pre-commit

## What a git hooks system does (Python)

Git itself supports hooks (scripts in `.git/hooks/`) that fire before/after git events. The problem with raw git hooks: they're per-clone, not version-controlled, and not consistent across team members.

A **git hooks system** solves this by storing hook configuration in a tracked file (`.pre-commit-config.yaml`) and installing the actual hook scripts into `.git/hooks/` for you. Now every clone of the repo gets the same checks.

For Python, the standard tool is **`pre-commit`** (the framework named `pre-commit`, run by the command `pre-commit`). It runs your formatter, linter, and type checker on staged files before each commit.

## Tool used

**`pre-commit`** — a Python-based hook runner that works for any language but is the default in Python projects.

Why pre-commit is the default choice:
- Config is in one tracked YAML file — every clone gets the same hooks
- Built-in support for Black, Ruff, MyPy, and dozens of other tools
- Each hook runs in an isolated environment (no polluting your project's deps)
- Caches tool installs so commits stay fast

## What it CAN do

- Run Black, Ruff, MyPy automatically on `git commit`
- Auto-fix safe issues (Black rewrites; Ruff `--fix`)
- Block the commit if any check fails
- Run only on staged files for speed
- Run all hooks across the whole repo on demand (`pre-commit run --all-files`)
- Update hook versions in one command (`pre-commit autoupdate`)

## What it CANNOT do

- Improve your code itself — it just runs other tools
- Detect new categories of error
- Run anywhere outside git events (use CI for that)
- Stop a determined commit — anyone can bypass with `git commit --no-verify`

## How it works on a commit

```
git add src/file.py
git commit -m "..."
  → pre-commit fires
    → Black runs on staged files (rewrites them if needed)
    → Ruff runs (auto-fixes; reports remaining issues)
    → MyPy runs (reports type errors; cannot auto-fix)
  → if all pass: commit succeeds
  → if any fail: commit blocked, fix and retry
```

If a hook **modified files** (e.g., Black reformatted), the commit is rejected with a "files were modified by this hook" message — `git add` the changes and commit again.

## How to set it up

### 1. Install

```bash
pip install pre-commit
```

### 2. Configure

Create `.pre-commit-config.yaml` at the project root:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: []   # add your typed runtime deps here
```

### 3. Install the hooks into `.git/hooks/`

```bash
pre-commit install
```

This is a one-time per-clone step. After this, every `git commit` in this repo runs the hooks.

### 4. Run on demand

```bash
# Run on all files (e.g., after first introducing pre-commit to a repo)
pre-commit run --all-files

# Update hook versions to latest
pre-commit autoupdate
```

### 5. Bypass (rarely)

```bash
git commit --no-verify -m "emergency fix"
```

Avoid making this a habit. If a hook is wrong, fix the hook config — don't normalize bypassing.

## See it run

Open `set-up/python/`, follow the README to install dependencies and run `pre-commit install`, then commit `src/messy.py`. You'll see Black reformat, Ruff fix what it can, and MyPy block the commit on type errors. Fix the type errors, re-stage, and commit again.
