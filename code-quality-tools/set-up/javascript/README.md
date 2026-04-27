<!--
PURPOSE: Runnable mock JS/TS project demonstrating Prettier + ESLint + TypeScript + Husky + lint-staged.
COVERS:  All four tool categories for JS/TS wired into one git pre-commit hook.
PATTERNS: One commit triggers formatter, linter, and type checker; commit blocks until clean.
LAST REVIEWED: 2026-04-27
-->

# JavaScript/TypeScript Mock Project — see all four tools fire on one commit

This is a real, runnable Node project. It contains one intentionally messy file (`src/messy.ts`) that has bad formatting, lint issues, and type errors all at once. Commit it and watch every tool fire.

## What's in this folder

| File                    | What it does                                                |
|-------------------------|-------------------------------------------------------------|
| `package.json`          | Dev deps + scripts (`format`, `lint`, `typecheck`) + lint-staged config |
| `.prettierrc.json`      | Prettier rules                                              |
| `eslint.config.js`      | ESLint flat config (uses `typescript-eslint` + Prettier compatibility) |
| `tsconfig.json`         | TypeScript strict config (`noEmit`, used as a type checker) |
| `.husky/pre-commit`     | Pre-commit hook: runs lint-staged then `tsc --noEmit`       |
| `.gitignore`            | Standard Node ignores                                       |
| `src/messy.ts`          | The deliberately broken file you'll commit                  |

## One-time setup

From inside `set-up/javascript/`:

```bash
# 1. Install deps. The `prepare` script automatically installs Husky's git hooks.
npm install

# 2. Initialize a git repo here (Husky needs a .git directory to install into).
git init

# 3. If git was init'd AFTER npm install, re-run prepare to install the hooks.
npm run prepare
```

## Run the demo

```bash
git add .
git commit -m "test"
```

Expected output (in this order):

1. **Husky** fires the pre-commit hook.
2. **lint-staged** runs on `src/messy.ts`:
   - **Prettier** rewrites the file (fixes spacing, semicolons, quotes). Modified files are re-staged automatically.
   - **ESLint** auto-fixes what it can (unused-imports, etc.) and reports remaining issues (`==` instead of `===`, unused variable, no-console warning).
3. **TypeScript** (`tsc --noEmit`) checks the whole project and reports type errors:
   - `greet(name)` — implicit `any` on `name`
   - `result.toUpperCase()` — `toUpperCase` does not exist on `number`
4. The commit stays blocked until you fix the errors. Edit `src/messy.ts`, re-stage, commit again.

When everything passes, the commit completes.

## Run individual tools manually

```bash
npm run format          # Prettier rewrite
npm run format:check    # Prettier CI mode
npm run lint            # ESLint report
npm run lint:fix        # ESLint auto-fix
npm run typecheck       # TypeScript (tsc --noEmit)
```

## Concept docs

For the "why" and deeper explanation of each tool:

- `formatter/javascript-formatter.md` — Prettier
- `linter/javascript-linter.md` — ESLint
- `type-checker/javascript-type-checker.md` — TypeScript
- `git-hooks-system/javascript-git-hooks-system.md` — Husky + lint-staged
