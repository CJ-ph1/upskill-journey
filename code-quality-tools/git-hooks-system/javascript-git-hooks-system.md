<!--
PURPOSE: Explain how git hooks work in JS/TS projects and how to set up Husky + lint-staged.
COVERS:  Husky for hook management, lint-staged for running tools on staged files.
PATTERNS: Husky installs hooks; lint-staged runs Prettier + ESLint on staged files; tsc --noEmit on whole project.
LAST REVIEWED: 2026-04-27
-->

# JavaScript/TypeScript Git Hooks — Husky + lint-staged

## What a git hooks system does (JS/TS)

Git's native hooks live in `.git/hooks/` and are not version-controlled. To get every team member running the same checks on every commit, you need a tool that stores hook configuration in tracked files and installs the hooks for you.

In the JS/TS ecosystem this is two tools working together:

- **Husky** — manages `.git/hooks/` from a tracked `.husky/` directory in the repo
- **lint-staged** — runs commands only on **files staged for commit** (so a commit that touches one file doesn't lint the whole repo)

## Tools used

- **Husky** — installs git hook scripts from a tracked `.husky/` folder, set up via `prepare` script in `package.json`
- **lint-staged** — runs configured commands on staged files, then re-stages them if they were modified

Why this pair is the default choice:
- Husky is by far the most common hook installer in the JS/TS ecosystem
- lint-staged keeps commits fast by checking only changed files
- Together they wire Prettier + ESLint + tsc into one commit pipeline cleanly

## What it CAN do

- Run Prettier, ESLint, and `tsc --noEmit` automatically on `git commit`
- Auto-fix safe issues (Prettier rewrites; `eslint --fix`)
- Block the commit if any check fails
- Run only on staged files for speed (Prettier + ESLint)
- Run a whole-project check (TypeScript) when the file-by-file model doesn't fit

## What it CANNOT do

- Improve your code itself — it just runs other tools
- Detect new categories of error
- Run anywhere outside git events (use CI for that)
- Stop a determined commit — `git commit --no-verify` bypasses hooks

## How it works on a commit

```
git add src/file.ts
git commit -m "..."
  → Husky's pre-commit hook fires
    → lint-staged runs on staged files
      → prettier --write    (rewrites + re-stages)
      → eslint --fix        (auto-fixes + re-stages; fails on remaining issues)
    → tsc --noEmit on the whole project (fails on type errors)
  → if all pass: commit succeeds
  → if any fail: commit blocked, fix and retry
```

Note: TypeScript is run on the whole project (not staged files only) because `tsc` needs full module graph context to check types correctly.

## How to set it up

### 1. Install

```bash
npm install --save-dev husky lint-staged
```

### 2. Initialize Husky

```bash
# Sets up the .husky/ directory and adds a "prepare" script to package.json
npx husky init
```

This creates `.husky/pre-commit` containing a default command — replace it with the one below.

### 3. Configure the pre-commit hook

Edit `.husky/pre-commit`:

```sh
npx lint-staged
npm run typecheck
```

### 4. Configure lint-staged

In `package.json`:

```json
{
  "scripts": {
    "prepare": "husky",
    "format": "prettier --write .",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "typecheck": "tsc --noEmit"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "prettier --write",
      "eslint --fix"
    ],
    "*.{json,md,css}": [
      "prettier --write"
    ]
  }
}
```

### 5. Other team members

The first time anyone clones the repo, `npm install` triggers the `prepare` script automatically, which installs Husky's git hooks. No manual step required.

### 6. Bypass (rarely)

```bash
git commit --no-verify -m "emergency fix"
```

Avoid making this a habit. Fix the hook or fix the code instead.

## See it run

Open `set-up/javascript/`, follow the README to `npm install` (which sets up Husky), then commit `src/messy.ts`. You'll see Prettier reformat, ESLint fix what it can, and `tsc --noEmit` block on type errors. Fix the type errors and commit again.
