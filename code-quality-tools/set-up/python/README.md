<!--
PURPOSE: Runnable mock Python project demonstrating Black + Ruff + MyPy + pre-commit.
COVERS:  All four tool categories for Python wired into one git pre-commit hook.
PATTERNS: One commit triggers formatter, linter, and type checker; commit blocks until clean.
LAST REVIEWED: 2026-04-27
-->

# Python Mock Project

A real, runnable Python project. Inside `src/messy.py` is one file with bad formatting, lint issues, and type errors all at once. Commit it and watch every tool fire.

---

## Files in this folder

| File                      | What it does                                          |
|---------------------------|-------------------------------------------------------|
| `pyproject.toml`          | Configures Black, Ruff, and MyPy in one file          |
| `.pre-commit-config.yaml` | Wires Black, Ruff, MyPy into the git pre-commit hook  |
| `.gitignore`              | Standard Python ignores                               |
| `src/messy.py`            | The deliberately broken file you'll commit            |

---

## One-time setup

Run from inside `set-up/python/`. Each step has the command first, then a short explanation of *what it does* and *why*.

### Step 1 — Create the virtual env

```bash
python -m venv .venv
```

**What it does:** creates a `.venv/` folder containing an isolated Python installation just for this project.

**Why:** any package you `pip install` after activating it lands inside `.venv/` instead of polluting your system Python. You can delete `.venv/` and start fresh anytime — it doesn't affect anything outside this folder.

---

### Step 2 — Activate the venv

```bash
.venv\Scripts\Activate.ps1          # PowerShell
```

**What it does:** flips your terminal so `python` and `pip` point inside `.venv/`. Your prompt should now start with `(.venv)`.

**Other shells:**

| Shell           | Command                              |
|-----------------|--------------------------------------|
| PowerShell      | `.venv\Scripts\Activate.ps1`         |
| CMD             | `.venv\Scripts\activate.bat`         |
| Git Bash / WSL  | `source .venv/Scripts/activate`      |
| macOS / Linux   | `source .venv/bin/activate`          |

**If PowerShell rejects it** with *"running scripts is disabled on this system"*, run this **once** (per user, persistent), then retry:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Step 3 — Install the project + its dev tools

```bash
pip install -e ".[dev]"
```

**What it does:** installs Black, Ruff, MyPy, and pre-commit into the venv at the versions pinned in `pyproject.toml`. The `pre-commit` *command* now exists in your terminal — but no hook is wired up yet.

**Why this exact form (not just `pip install`)?** The command is three pieces stacked:

| Part          | Meaning                                                                                          |
|---------------|--------------------------------------------------------------------------------------------------|
| `pip install` | The normal install command                                                                       |
| `-e`          | **Editable mode** — installs *this folder as a package*; source changes take effect immediately  |
| `.`           | The package = the project in the current directory (reads `pyproject.toml`)                      |
| `[dev]`       | Install the **optional extras group** named `dev` on top of the base deps                        |

The quotes around `".[dev]"` just stop the shell from interpreting the brackets.

Inside `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = ["black>=24.0", "ruff>=0.5", "mypy>=1.10", "pre-commit>=3.7"]
```

So this one command installs all four tools at the *exact* versions pinned in the file. The next person who clones gets the same versions — no guessing.

> **Equivalent shortcut** (works, but loses version pinning): `pip install black ruff mypy pre-commit`
>
> For a published library elsewhere (e.g. `pip install requests`), plain `pip install` is still correct. The `-e ".[dev]"` form is specifically for **installing the project you're working on** with its declared dev tooling.

---

### Step 4 — Wire pre-commit into the git repo

```bash
pre-commit install
```

**What it does:** writes a script into `.git/hooks/pre-commit` so every future `git commit` runs Black + Ruff + MyPy automatically.

**Why this is a separate step** (the most common confusion):

The word "install" is overloaded. Two different things happened, in two different places:

| Command                                | Installs                     | Where it lives                 | Effect                                         |
|----------------------------------------|------------------------------|--------------------------------|------------------------------------------------|
| `pip install pre-commit` (Step 3)      | The **`pre-commit` program** | `.venv/Scripts/pre-commit.exe` | Makes the *command* available in your terminal |
| `pre-commit install` (this step)       | A **git hook script**        | `.git/hooks/pre-commit`        | Tells git "run pre-commit before every commit" |

The first is **a tool**. The second is **a hook that calls the tool**.

**Printer analogy:**
- `pip install pre-commit` = unboxing the printer and plugging it in. It exists, ready to use.
- `pre-commit install` = telling Word "print to *this* printer when I press Ctrl+P". Without this step, nothing prints.

**Under the hood,** `pre-commit install` writes a small script into `.git/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
exec pre-commit run --hook-stage pre-commit
```

Git looks for this exact file path on every `git commit`. No file → nothing runs.

**Prove it yourself** — after Step 3 but before Step 4:

```bash
pre-commit --version          # → "pre-commit 3.x.x" (the tool exists)
ls .git/hooks/pre-commit      # → missing (or only the .sample file)
# A `git commit` here runs NOTHING — Black/Ruff/MyPy stay silent.
```

Run `pre-commit install` and check again — the file appears, and `git commit` triggers the pipeline.

> **About `git init`:** `pre-commit install` needs a git repo above it.
> - You're inside `journey/` (already a git repo) → skip `git init`.
> - You copied this mock somewhere new that isn't a git repo yet → run `git init` first, then `pre-commit install`.
> - Don't run `git init` inside an already-tracked subfolder — it creates a nested repo and causes confusing behavior.

---

## Run the demo

```bash
git add .
git commit -m "test"
```

Expected sequence:

1. **Black** rewrites `src/messy.py` (spacing, quotes, indentation). The commit is rejected with *"files were modified by this hook"*.
2. Re-stage and try again:
   ```bash
   git add src/messy.py
   git commit -m "test"
   ```
3. **Black** passes.
4. **Ruff** auto-fixes unused imports and the unused variable, then reports what it can't fix. If anything was rewritten, re-stage and commit again.
5. **MyPy** reports type errors:
   - missing annotations on `greet`
   - `add("1", "2")` — `str` passed where `int` expected
6. The commit stays blocked until you fix the type errors by hand.

When everything passes, the commit completes.

---

## Run individual tools manually

```bash
black .                       # format
ruff check . --fix            # lint (auto-fix safe issues)
mypy .                        # type-check
pre-commit run --all-files    # run every hook on every file
```

---

## Concept docs

For the "what" and "why" of each tool:

- `formatter/python-formatter.md` — Black
- `linter/python-linter.md` — Ruff
- `type-checker/python-type-checker.md` — MyPy
- `git-hooks-system/python-git-hooks-system.md` — pre-commit
