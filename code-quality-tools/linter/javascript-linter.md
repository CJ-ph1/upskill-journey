<!--
PURPOSE: Explain how a linter works in JS/TS and how to set up ESLint.
COVERS:  ESLint for JavaScript and TypeScript (flat config).
PATTERNS: Lint on save / pre-commit via lint-staged; auto-fix safe issues; pair with Prettier via eslint-config-prettier.
LAST REVIEWED: 2026-04-27
-->

# JavaScript/TypeScript Linter — ESLint

## What a linter does (JS/TS)

A linter statically analyzes JS/TS source for **bad patterns, likely bugs, and risky code** without running it.

Typical findings in JS/TS: unused variables, undefined names, `==` instead of `===`, unreachable code, missing `await`, accidental `console.log`, unsafe `any` usage in TypeScript, React hook misuse, etc.

## Tool used

**ESLint** — the de facto JS/TS linter. With `typescript-eslint`, it understands TypeScript types and adds dozens of TS-specific rules.

Why ESLint is the default choice:
- Huge ecosystem of plugins (React, Next.js, import order, accessibility, security, etc.)
- Modern flat config (`eslint.config.js`) is straightforward
- Auto-fixes most stylistic and many code-quality issues
- Pairs cleanly with Prettier — `eslint-config-prettier` disables ESLint rules that fight Prettier so the two tools never argue

## What it CAN do

- Detect unused variables, undefined names, unreachable code
- Enforce strict equality (`===` over `==`)
- Flag React hook violations, missing dependency arrays, etc.
- Block use of `any`, non-null assertions, or other TS escape hatches (configurable)
- Auto-fix many issues with `--fix`
- Enforce import order, no relative `../../..` imports, banned modules, etc.

## What it CANNOT do

- Guarantee your code is correct — wrong logic still passes
- Replace the type checker — ESLint can flag *some* type-related smells, but `tsc --noEmit` is the real type checker
- Replace Prettier — formatting is Prettier's job; let it do that
- Replace tests — pattern matching, not behavior

## Before / after

**Before:**

```ts
import { foo } from "./x";        // unused
const bar = 42;                   // unused
function getUser(id) {            // implicit any (TS rule)
  if (id == null) return;         // should be ===
  console.log("debug", id);       // banned in some configs
  return fetchUser(id);
}
```

**ESLint reports:**

```
'foo' is defined but never used                           @typescript-eslint/no-unused-vars
'bar' is assigned a value but never used                  @typescript-eslint/no-unused-vars
Parameter 'id' implicitly has an 'any' type               @typescript-eslint/no-explicit-any
Expected '===' and instead saw '=='                       eqeqeq
Unexpected console statement                              no-console
```

## How to set it up

### 1. Install

```bash
npm install --save-dev eslint @eslint/js typescript-eslint eslint-config-prettier
```

### 2. Configure (flat config)

Create `eslint.config.js` at the project root:

```js
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import prettier from "eslint-config-prettier";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  prettier, // disables rules that conflict with Prettier — keep last
  {
    rules: {
      eqeqeq: "error",
      "no-console": "warn",
      "@typescript-eslint/no-unused-vars": "error",
    },
  },
  {
    ignores: ["node_modules", "dist", "build", "coverage"],
  },
];
```

### 3. Run it

Add to `package.json` scripts:

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix"
  }
}
```

Then:

```bash
npm run lint           # report issues
npm run lint:fix       # auto-fix what's safe
```

### 4. IDE integration

The ESLint VS Code extension highlights issues inline and can auto-fix on save when configured.

### 5. Wire it into commits

See `git-hooks-system/javascript-git-hooks-system.md` — Husky + lint-staged runs `eslint --fix` on staged files before each commit.

## See it run

Open `set-up/javascript/` and commit `src/messy.ts`. ESLint reports the unused import, the loose equality, and other issues in the file.
