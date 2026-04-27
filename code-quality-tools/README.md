# Code Quality Tools

A personal knowledge base for the four categories of code quality tools, covering **Python** and **JavaScript/TypeScript**. Each category is explained conceptually and demonstrated with a working mock project.

## The four categories

| Tool         | Question it answers                           |
| ------------ | --------------------------------------------- |
| Formatter    | "Does this look consistent?"                  |
| Linter       | "Is this suspicious or wrong?"                |
| Type Checker | "Are types used correctly?"                   |
| Git Hooks    | "Should this code even be allowed to commit?" |

## Tool choices

| Category     | Python      | JavaScript/TypeScript        |
|--------------|-------------|------------------------------|
| Formatter    | Black       | Prettier                     |
| Linter       | Ruff        | ESLint                       |
| Type checker | MyPy        | TypeScript (`tsc --noEmit`)  |
| Git hooks    | pre-commit  | Husky + lint-staged          |

## Folder map

```
code-quality-tools/
├── README.md                  ← you are here
├── CLAUDE.md                  ← rules to keep these docs fresh
├── reference.txt              ← canonical summary (don't edit)
│
├── formatter/                 ← concept docs
│   ├── python-formatter.md
│   └── javascript-formatter.md
├── linter/
│   ├── python-linter.md
│   └── javascript-linter.md
├── type-checker/
│   ├── python-type-checker.md
│   └── javascript-type-checker.md
├── git-hooks-system/
│   ├── python-git-hooks-system.md
│   └── javascript-git-hooks-system.md
│
└── set-up/                    ← runnable mock projects
    ├── python/                ← Black + Ruff + MyPy + pre-commit
    └── javascript/            ← Prettier + ESLint + TypeScript + Husky
```

## How to use this folder

**To understand a tool conceptually** → open `<tool>/<lang>-<tool>.md`.
Example: how does formatting work in Python? → `formatter/python-formatter.md`.

**To see a tool fire on a real commit** → go into `set-up/<lang>/` and follow its README.
You'll edit a deliberately messy file, run `git commit`, and watch the formatter, linter, and type checker all run via the git hook.

## Source of truth

The concept docs expand on `reference.txt`. If they ever disagree, `reference.txt` wins — fix the doc.
