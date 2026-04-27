# CLAUDE.md — journey

This folder is my learning journey. The top-level `README.md` is an auto-maintained index whose progress tracker is computed from per-topic checklists. When working in this folder, follow the rules below.

## What this folder is

- Each immediate subfolder = one learning topic (e.g. `code-quality-tools/`, `workflow/`)
- Each topic owns its own `CLAUDE.md`, concept docs, and (where applicable) hands-on examples
- This file governs the **journey-level** rules; topic-level rules live inside each topic's own `CLAUDE.md`

## The progress tracker rule (most important)

The progress table in `journey/README.md` is **derived data**. Don't hand-edit it. Whenever any topic's content changes — new files, edited docs, ticked checkbox — recompute the tracker.

### How to compute a topic's percentage

1. Open `<topic>/CLAUDE.md`
2. Find the section heading `## Learning checklist`
3. Read every line under that heading that starts with `- [ ]` or `- [x]` (until the next `##` heading or end of file)
4. `percentage = round(100 * checked / total)`
5. If `total == 0`, the topic is **0%** with status "Not started"

### How to render a row

```
| [<topic>](./<topic>/) | <bar> | <pct>% | <status> |
```

- `<bar>` is 10 block-characters: `n = round(pct / 10)` filled with `█`, the rest with `░`. Example: `47%` → `█████░░░░░`.
- `<status>` rules:
  - `0%` and checklist is empty → `Not started`
  - `0%` and checklist has items → `Just started`
  - `1–99%` → `In progress`
  - `100%` → `Done`

### When to recompute

Recompute and rewrite the table any time you:
- Tick or untick a box in any topic's `## Learning checklist`
- Add or remove items from any checklist
- Add a new topic folder
- Rename or remove a topic folder

The user does not need to ask. If you've just edited a checklist, regenerate the tracker in the same change.

## Adding a new topic

When the user creates a new topic folder, you must:

1. Create `<new-topic>/CLAUDE.md` with at minimum:
   - A short purpose paragraph
   - A `## Learning checklist` section (initially empty or with the user's seed items)
2. Add a row to the progress tracker in `journey/README.md`
3. Add a one-paragraph entry under "## Topics" in `journey/README.md`

## Topic-level rules

Each topic's own `CLAUDE.md` may add stricter rules. Honor them. The journey-level rules in this file are the floor, not the ceiling.

## Out of scope

- Don't merge content across topics. Each topic stays self-contained so it can be lifted out or rebuilt independently.
- Don't auto-tick checkboxes the user hasn't earned. New documentation does not equal learned material — only check items the user has explicitly read, practiced, or completed. When unsure, leave the box unticked.
- Don't add topics the user hasn't asked for, even if a folder appears empty.
