<!--
PURPOSE: Explain how a formatter works in JS/TS and how to set up Prettier.
COVERS:  Prettier for JavaScript and TypeScript.
PATTERNS: Format on save / pre-commit via lint-staged; let Prettier decide.
LAST REVIEWED: 2026-04-27
-->

# JavaScript/TypeScript Formatter — Prettier

## What a formatter does (JS/TS)

A formatter rewrites JS/TS source so it always looks the same: indentation, quote style, semicolons, trailing commas, line length, JSX layout. It only changes **how the code looks**, never **what it does**.

For JS/TS that includes: consistent quotes (`"` vs `'`), semicolons on/off, 2- vs 4-space indent, trailing commas in multi-line literals, line wrapping for long expressions, JSX attribute layout.

## Tool used

**Prettier** — the de facto formatter for the JS/TS ecosystem. Like Black, it is opinionated by design: very few config knobs.

Why Prettier is the default choice:
- Zero-config defaults that match the wider ecosystem
- Handles JS, TS, JSX, TSX, JSON, CSS, Markdown, YAML, and more in one tool
- Idempotent and deterministic
- Pairs cleanly with ESLint via `eslint-config-prettier` (Prettier formats; ESLint lints; no overlap)

## What it CAN do

- Rewrite quotes, semicolons, indentation, and trailing commas
- Wrap long lines and indent JSX attributes consistently
- Format `.json`, `.md`, `.css`, `.yaml` too
- Run on save (IDE) or before commit (Husky + lint-staged)

## What it CANNOT do

- Detect bugs — wrong logic is none of Prettier's business
- Catch unused imports/variables (that's ESLint)
- Check types (that's TypeScript)
- Enforce code-quality rules (no `console.log`, no `any`, etc. — that's ESLint)

## Before / after

**Before:**

```ts
import {foo,bar}   from "./x"
const greet=(name:string)=>{return "hi "+name }
const user={ name:'cj',age :30}
```

**After Prettier runs:**

```ts
import { foo, bar } from "./x";
const greet = (name: string) => {
  return "hi " + name;
};
const user = { name: "cj", age: 30 };
```

## How to set it up

### 1. Install

```bash
npm install --save-dev prettier
```

### 2. Configure

Create `.prettierrc.json` in the project root:

```json
{
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
```

Optionally a `.prettierignore`:

```
node_modules
dist
build
coverage
```

### 3. Run it

Add to `package.json` scripts:

```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

Then:

```bash
npm run format          # rewrite files
npm run format:check    # CI mode — fail if anything would change
```

### 4. IDE integration

The VS Code Prettier extension formats on save when you enable "Editor: Format On Save" and set Prettier as the default formatter.

### 5. Wire it into commits

See `git-hooks-system/javascript-git-hooks-system.md` for using **Husky + lint-staged** to run Prettier on staged files before every commit.

## See it run

Open `set-up/javascript/`, follow the README, and commit `src/messy.ts`. Prettier rewrites the file in place before the commit completes.
