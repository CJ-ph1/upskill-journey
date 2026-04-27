# CLAUDE.md — code-quality-tools

This folder is a personal knowledge base. Its value depends on staying accurate. When working in this folder, follow the rules below.

## Source of truth

`reference.txt` is the canonical summary of the four tool categories. Concept docs expand on it but **must not contradict it**. If a contradiction appears, fix the doc — not `reference.txt`.

## Scope

Coverage is intentionally limited to **Python** and **JavaScript/TypeScript**. Do not add other languages without an explicit request.

## Freshness rules

### 1. Update on change

When any tool version, install command, or config snippet is changed in this folder, update **both layers** in the same change:

- The matching concept doc (`<tool>/<lang>-<tool>.md`)
- The matching file inside `set-up/<lang>/`

The two layers must always agree. Drift between them is a bug.

### 2. Module headers required

Every `.md` file in this folder — except top-level `README.md` and `reference.txt` — must start with this header block:

```
<!--
PURPOSE: one sentence on what this doc is for
COVERS:  what tool(s) and language(s) it covers
PATTERNS: the key conventions or patterns it teaches
LAST REVIEWED: YYYY-MM-DD
-->
```

When editing a doc, update `LAST REVIEWED` to today's date.

### 3. Coverage checklist

Each of the four tool categories must have:

- A `python-<tool>.md` AND a `javascript-<tool>.md` in the tool folder
- A working configuration in **both** `set-up/python/` and `set-up/javascript/`

If a category is missing one side, flag it and offer to fill the gap.

### 4. Last-reviewed stamp

If the `LAST REVIEWED` date on a doc is older than 6 months at the time of an edit, refresh the doc before unrelated edits:

- Verify tool versions are still current
- Verify install commands still work
- Verify config syntax matches the current tool version
- Update the date stamp

## Mock projects

`set-up/python/` and `set-up/javascript/` are runnable projects. Their value is that one `git commit` triggers the full pipeline (formatter → linter → type checker). Do not break this property:

- All four tools must remain wired into the git hook
- `src/messy.<py|ts>` must contain at least one bad-formatting issue, one lint issue, and one type error so every tool has visible work to do
- The mock README must explain what to expect when committing
