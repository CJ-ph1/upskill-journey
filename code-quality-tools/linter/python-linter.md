<!--
PURPOSE: Explain how a linter works in Python and how to set up Ruff.
COVERS:  Ruff for Python.
PATTERNS: Lint on save / pre-commit; auto-fix safe issues; treat warnings as errors in CI.
LAST REVIEWED: 2026-04-27
-->

# Python Linter — Ruff

## What a linter does (Python)

A linter statically analyzes Python source for **suspicious code, bad patterns, and likely bugs** without running it. It's a tireless code reviewer.

Typical findings: unused imports, unused variables, undefined names, shadowed builtins, mutable default arguments, comparison to `None` with `==`, broad `except`, etc.

## Tool used

**Ruff** — an extremely fast Python linter (and formatter, but here we use it just as a linter). It is a near-drop-in replacement for the older Flake8/pylint/isort/pyupgrade ecosystem, packaged as a single binary written in Rust.

Why Ruff is the default choice:
- 10–100× faster than the older Python linters — fast enough to run on every save with no friction
- Bundles dozens of rule sets (pyflakes, pycodestyle, isort, pyupgrade, bugbear, etc.) into one tool
- Auto-fixes most safe issues
- One config block in `pyproject.toml` instead of many separate tool configs

## What it CAN do

- Detect unused imports and unused variables
- Catch undefined names, shadowed builtins, redefined imports
- Sort imports (replaces isort)
- Flag legacy syntax that has a modern equivalent (replaces pyupgrade)
- Warn about likely bugs (mutable default args, comparing to `True`/`None` with `==`, etc.)
- Auto-fix many issues with `--fix`

## What it CANNOT do

- Guarantee your code is correct — `def divide(a, b): return a + b` looks fine to Ruff
- Understand whole-program behavior across modules
- Check types (that's MyPy)
- Replace tests — a linter sees patterns, not behavior

## Before / after

**Before:**

```python
import os                              # unused import
import sys
from typing import List

def get_users(ids: List[int]):
    result = []                        # unused variable
    return [u for u in fetch(ids)]     # could be: list(fetch(ids))
```

**Ruff reports:**

```
F401 [*] `os` imported but unused
F841 [*] Local variable `result` is assigned to but never used
C416 [*] Unnecessary list comprehension (rewrite using `list()`)
```

The `[*]` means Ruff can auto-fix it.

## How to set it up

### 1. Install

```bash
pip install ruff
```

Or pin in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["ruff>=0.5"]
```

### 2. Configure

Add to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
# E, F = pyflakes/pycodestyle (defaults)
# I    = isort (import sorting)
# B    = bugbear (likely bugs)
# UP   = pyupgrade (modernize syntax)
select = ["E", "F", "I", "B", "UP"]
ignore = []

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]   # allow re-export imports
```

### 3. Run it

```bash
# Report issues
ruff check .

# Auto-fix what's safe to fix
ruff check . --fix

# CI mode — exit non-zero if anything is found
ruff check .
```

### 4. IDE integration

The Ruff VS Code / PyCharm plugins highlight issues inline and can auto-fix on save.

### 5. Wire it into commits

See `git-hooks-system/python-git-hooks-system.md` — `pre-commit` runs Ruff on every commit and can auto-fix before letting the commit through.

## See it run

Open `set-up/python/` and commit `src/messy.py`. Ruff reports the unused import, the unused variable, and other issues in the file.
