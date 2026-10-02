<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/rock_1faa8.png" width="80" />
</p>

<h1 align="center">caveman-compress</h1>

<p align="center">
  <strong>shrink memory file. save token every session.</strong>
</p>

---

Skill compress project memory files (`CLAUDE.md`, todos, preferences) into caveman format — fewer tokens each session load.

Agent apply compression rules from `SKILL.md` directly. No Claude CLI. No API key. No required Python pipeline.

## What It Do

```
/caveman:compress CLAUDE.md
```

```
CLAUDE.md          ← compressed (agent reads this — fewer tokens every session)
CLAUDE.original.md ← human-readable backup (you edit this)
```

Original never lost. Edit `.original.md` when needed. Re-run skill to re-compress after edits.

## Benchmarks

Historical results (when Claude-backed pipeline existed) on real project files:

| File | Original | Compressed | Saved |
|------|----------:|----------:|------:|
| `claude-md-preferences.md` | 706 | 285 | **59.6%** |
| `project-notes.md` | 1145 | 535 | **53.3%** |
| `claude-md-project.md` | 1122 | 636 | **43.3%** |
| `todo-list.md` | 627 | 388 | **38.1%** |
| `mixed-with-code.md` | 888 | 560 | **36.9%** |
| **Average** | **898** | **481** | **46%** |

Target still: headings, code blocks, URLs, file paths preserved exactly.

## Before / After

<table>
<tr>
<td width="50%">

### Original (706 tokens)

> "I strongly prefer TypeScript with strict mode enabled for all new code. Please don't use `any` type unless there's genuinely no way around it, and if you do, leave a comment explaining the reasoning. I find that taking the time to properly type things catches a lot of bugs before they ever make it to runtime."

</td>
<td width="50%">

### Caveman (285 tokens)

> "Prefer TypeScript strict mode always. No `any` unless unavoidable — comment why if used. Proper types catch bugs early."

</td>
</tr>
</table>

**Same instructions. ~60% fewer tokens. Every session.**

## Security

Primary path = agent edits one user-named file in-process. No subprocess, no network. See [SECURITY.md](./SECURITY.md).

Legacy `scripts/` (optional validators / old Claude pipeline) may still trip static-analysis false positives if scanned — unused by default skill flow.

## Install

Part of this agent-skills repo. After install, invoke `/caveman:compress` or ask agent to compress a memory file.

## Usage

```
/caveman:compress <filepath>
```

Examples:
```
/caveman:compress CLAUDE.md
/caveman:compress docs/preferences.md
/caveman:compress todos.md
```

### What files work

| Type | Compress? |
|------|-----------|
| `.md`, `.txt`, `.rst` | Yes |
| Extensionless natural language | Yes |
| `.py`, `.js`, `.ts`, `.json`, `.yaml` | Skip (code/config) |
| `*.original.md` | Skip (backup files) |

## How It Work

```
/caveman:compress CLAUDE.md
        ↓
guard: type + never *.original.md
        ↓
backup → CLAUDE.original.md (if missing)
        ↓
agent compress prose per SKILL.md rules
  (code/inline/URLs/paths/headings untouched)
        ↓
overwrite CLAUDE.md
```

Optional: run legacy `scripts/` validators afterward for preservation checks. Not required.

## What Is Preserved

Caveman compress natural language. Never touch:

- Code blocks (fenced or indented)
- Inline code (`` `backtick content` ``)
- URLs and links
- File paths (`/src/components/...`)
- Commands (`npm install`, `git commit`)
- Technical terms, library names, API names
- Headings (exact text preserved)
- Tables (structure preserved, cell text compressed)
- Dates, version numbers, numeric values

## Why This Matter

Memory files load every session. Big file → repeated token tax. Caveman cut ~46% average historically. Same instructions. Less waste.

## Part of Caveman

- **caveman** — speak like caveman (cut response tokens)
- **caveman-compress** — read less (cut context tokens)
