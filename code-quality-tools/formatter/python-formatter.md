<!--
PURPOSE: Explain how a formatter works in Python and how to set up Black.
COVERS:  Black for Python.
PATTERNS: Format on save / pre-commit; never argue about style; let Black decide.
LAST REVIEWED: 2026-04-27
-->

# Python Formatter — Black

## What a formatter does (Python)

A formatter rewrites Python source so it always looks the same: spacing, indentation, quote style, line length, trailing commas. It only touches **how the code looks**, never **what it does**.

In Python that means: 4-space indentation, double quotes, one statement per line, line wrapped at a max length, blank lines between top-level definitions, etc.

## Tool used

**Black** — the de facto Python formatter. It is opinionated on purpose: almost no config, almost no decisions to make. Pick Black, run it, move on.

Why Black is the default choice:
- Zero-config: you accept its style and stop arguing about it
- Idempotent: running Black twice produces the same output as running it once
- Wide adoption: works the same in every Python project, every IDE

## What it CAN do

- Rewrite spacing, indentation, and quote style automatically
- Wrap long lines and arrange function arguments
- Insert/remove blank lines around `def` and `class`
- Make every Python file in your repo look like every other file
- Run automatically on save (IDE) or before commit (pre-commit hook)

## What it CANNOT do

- Detect bugs — `return a - b` when you meant `return a + b` is fine to Black
- Catch unused imports or unused variables (that's the linter's job)
- Check types (that's the type checker's job)
- Refactor logic, rename things, or improve readability beyond layout

## Before / after

**Before:**

```python
import   os
def add( a,b ):return a+b
class   User: pass
```

**After Black runs:**

```python
import os


def add(a, b):
    return a + b


class User:
    pass
```

## How to set it up

### 1. Install

```bash
pip install black
```

Or pin it as a dev dependency in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["black>=24.0"]
```

### 2. Configure (optional)

Black takes very little config. The most common knob is line length. Add to `pyproject.toml`:

```toml
[tool.black]
line-length = 100
target-version = ["py311"]
```

### 3. Run it

```bash
# Format every Python file in the project
black .

# Check only — exit non-zero if anything would change (CI mode)
black --check .

# Show what would change without writing
black --diff .
```

### 4. IDE integration

VS Code, PyCharm, and others have a "format on save" option that calls Black for you. Turn it on once and you never think about formatting again.

### 5. Wire it into commits

See `git-hooks-system/python-git-hooks-system.md` for using `pre-commit` to run Black automatically before every commit.

## See it run

Open `set-up/python/`, follow the README, and commit `src/messy.py`. Black rewrites the file in place before the commit completes.
