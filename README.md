# Journey — My Learning & Upskill Log

This folder is my personal learning journey. Each subfolder is one topic I'm actively studying, building, or practicing. Every topic owns its own knowledge base (concept docs + hands-on examples) and tracks how far along I am.

## Why this exists

- Force the things I learn into **writing**, so they stop being vibes and start being knowledge
- Make every topic something I can come back to in 6 months and still rebuild from scratch
- Track honestly how much of each topic I've actually internalized — not how much I've *touched*

## Progress tracker

The percentages below are computed automatically. Each topic folder has a `CLAUDE.md` with a `## Learning checklist` section listing what "100% learned" means for that topic. The percentage = `checked items / total items`. When the checklist changes (I tick a box, or new content is added), the table here is regenerated.

| Topic                                    | Progress      | %     | Status          |
|------------------------------------------|---------------|-------|-----------------|
| [code-quality-tools](./code-quality-tools/) | `██░░░░░░░░` | 17%   | In progress     |
| [workflow](./workflow/)                  | `░░░░░░░░░░`  |  0%   | Not started     |

> **How to read this:** the bar shows tens (each block = 10%). The % is the exact value from the topic's checklist. "Not started" means the topic stub exists but its checklist is still empty.

## Topics

### [code-quality-tools](./code-quality-tools/)

Formatter, linter, type checker, and git hooks system — for Python and JavaScript/TypeScript. Concepts plus runnable mock projects where one `git commit` fires the whole pipeline.

### [workflow](./workflow/)

_Stub — to be scoped._

## Adding a new topic

1. Create the folder: `journey/<new-topic>/`
2. Add a `CLAUDE.md` with a `## Learning checklist` section (see `code-quality-tools/CLAUDE.md` as the model)
3. Drop the topic's reference material (`reference.txt`, source notes, links) into the folder
4. The next time anything in this folder changes, the tracker above will pick up the new topic and compute its starting %

## Source of truth

Each topic's own folder is authoritative for that topic. This README is just the index.
