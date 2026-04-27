<!--
PURPOSE: Explain how a type checker works in JS/TS and how to set up TypeScript (tsc --noEmit).
COVERS:  TypeScript as a type checker for JS and TS source.
PATTERNS: strict mode on; tsc --noEmit in CI; never silence with `any` or `@ts-ignore` casually.
LAST REVIEWED: 2026-04-27
-->

# JavaScript/TypeScript Type Checker — TypeScript

## What a type checker does (JS/TS)

TypeScript is two things: a **language** (TS source compiled to JS) and a **type checker** for JS/TS source. Even on plain `.js` files you can use TypeScript as a checker via `// @ts-check` and JSDoc annotations, or by including `.js` in `tsconfig.json` with `allowJs`.

The type checker verifies that values flow through your code in compatible types: argument types match parameter types, return types match declarations, properties exist on the objects you access, generics are used consistently.

## Tool used

**TypeScript (`tsc --noEmit`)** — run the compiler purely as a checker, producing no output files. This is the standard way to type-check a TS project in CI and in pre-commit hooks.

Why this is the default choice:
- TypeScript is the type system for JS/TS — there is no real alternative
- `--noEmit` makes it a pure check (no build artifacts)
- Strict mode (`"strict": true`) catches the bugs that matter
- IDE integration is excellent everywhere

## What it CAN do

- Catch wrong-type arguments at call sites
- Catch wrong return types
- Catch property access on the wrong type (`user.nmae` typo)
- Enforce that `null` / `undefined` are handled (`strictNullChecks`)
- Verify generics, discriminated unions, and conditional types
- Cross-file checking across the whole project

## What it CANNOT do

- Catch logical bugs — `(a: number, b: number) => a - b` named `add` is type-correct
- Check what isn't typed — `any`, untyped imports, and `@ts-ignore` blind it
- Run your code — runtime issues that depend on values are out of scope
- Replace tests — types prove shape, not behavior

## Before / after

**Before:**

```ts
function add(a: number, b: number): number {
  return a + b;
}

const result = add("1", "2");        // strings into number params
console.log(result.toUpperCase());   // calling string method on number
```

**TypeScript reports:**

```
Argument of type 'string' is not assignable to parameter of type 'number'.
Argument of type 'string' is not assignable to parameter of type 'number'.
Property 'toUpperCase' does not exist on type 'number'.
```

## How to set it up

### 1. Install

```bash
npm install --save-dev typescript
```

### 2. Configure

Generate a starter config:

```bash
npx tsc --init
```

Then edit `tsconfig.json` to a sensible strict baseline:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "noEmit": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "build"]
}
```

`"strict": true` is the single most important setting. It enables `strictNullChecks`, `noImplicitAny`, and several other strong defaults.

### 3. Run it

Add to `package.json` scripts:

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit"
  }
}
```

Then:

```bash
npm run typecheck
```

`tsc` exits non-zero on type errors.

### 4. IDE integration

VS Code uses TypeScript's language server out of the box for any file in a `tsconfig.json` project. Errors appear inline as you type.

### 5. Wire it into commits

See `git-hooks-system/javascript-git-hooks-system.md` — Husky runs `npm run typecheck` (or a faster project-aware alternative) before each commit.

## See it run

Open `set-up/javascript/` and commit `src/messy.ts`. TypeScript reports wrong-type calls and any missing/wrong type annotations.
