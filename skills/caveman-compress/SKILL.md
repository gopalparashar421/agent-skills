---
name: caveman-compress
description: >
  Compress natural language memory files (CLAUDE.md, todos, preferences) into caveman format
  to save input tokens. Preserves all technical substance, code, URLs, and structure.
  Compressed version overwrites the original file. Human-readable backup saved as FILE.original.md.
  Trigger: /caveman:compress <filepath> or "compress memory file"
license: MIT
metadata:
  author: groupzer0
  version: "1.1"
---

# Caveman Compress

## Purpose

Compress natural language files (CLAUDE.md, todos, preferences) into caveman-speak to reduce input tokens. Agent apply compression rules DIRECTLY — no Claude CLI, no API call, no `python -m scripts`. Compressed version overwrite original. Human-readable backup saved as `<filename>.original.md`.

Intensity / voice reference: sibling skill `skills/caveman/SKILL.md` (full intensity default). Compression rule set below = standalone; caveman skill optional for tone examples only.

## Trigger

`/caveman:compress <filepath>` or when user asks to compress a memory file.

## Process

Agent do these steps INLINE (read file → transform → write). Do NOT call Claude CLI. Do NOT run `python -m scripts` for compression.

1. **Resolve path.** Absolute or workspace-relative filepath from user.
2. **Guardrails (abort, no write):**
   - File missing / not a file → report, stop
   - Name ends with `.original.md` → NEVER compress backups; report skip, stop
   - Extension not natural-language → skip (see Boundaries)
3. **Backup once:** If `FILE.original.md` does not exist, copy current file contents there. If backup already exists, leave it untouched (re-compress from current FILE, or user edits `.original.md` then copies back first).
4. **Compress prose in place** using Compression Rules below. Preserve code/inline/URLs/paths/headings/structure EXACTLY.
5. **Overwrite** original path with compressed result.
6. **Return** to user: compressed path, backup path, rough before/after size if easy.

## Compression Rules

### Remove
- Articles: a, an, the
- Filler: just, really, basically, actually, simply, essentially, generally
- Pleasantries: "sure", "certainly", "of course", "happy to", "I'd recommend"
- Hedging: "it might be worth", "you could consider", "it would be good to"
- Redundant phrasing: "in order to" → "to", "make sure to" → "ensure", "the reason is because" → "because"
- Connective fluff: "however", "furthermore", "additionally", "in addition"

### Preserve EXACTLY (never modify)
- Code blocks (fenced ``` and indented)
- Inline code (`backtick content`)
- URLs and links (full URLs, markdown links)
- File paths (`/src/components/...`, `./config.yaml`)
- Commands (`npm install`, `git commit`, `docker build`)
- Technical terms (library names, API names, protocols, algorithms)
- Proper nouns (project names, people, companies)
- Dates, version numbers, numeric values
- Environment variables (`$HOME`, `NODE_ENV`)

### Preserve Structure
- All markdown headings (keep exact heading text, compress body below)
- Bullet point hierarchy (keep nesting level)
- Numbered lists (keep numbering)
- Tables (compress cell text, keep structure)
- Frontmatter/YAML headers in markdown files

### Compress
- Use short synonyms: "big" not "extensive", "fix" not "implement a solution for", "use" not "utilize"
- Fragments OK: "Run tests before commit" not "You should always run tests before committing"
- Drop "you should", "make sure to", "remember to" — just state the action
- Merge redundant bullets that say the same thing differently
- Keep one example where multiple examples show the same pattern

CRITICAL RULE:
Anything inside ``` ... ``` must be copied EXACTLY.
Do not:
- remove comments
- remove spacing
- reorder lines
- shorten commands
- simplify anything

Inline code (`...`) must be preserved EXACTLY.
Do not modify anything inside backticks.

If file contains code blocks:
- Treat code blocks as read-only regions
- Only compress text outside them
- Do not merge sections around code

## Pattern

Original:
> You should always make sure to run the test suite before pushing any changes to the main branch. This is important because it helps catch bugs early and prevents broken builds from being deployed to production.

Compressed:
> Run tests before push to main. Catch bugs early, prevent broken prod deploys.

Original:
> The application uses a microservices architecture with the following components. The API gateway handles all incoming requests and routes them to the appropriate service. The authentication service is responsible for managing user sessions and JWT tokens.

Compressed:
> Microservices architecture. API gateway route all requests to services. Auth service manage user sessions + JWT tokens.

## Boundaries

- ONLY compress natural language files (.md, .txt, extensionless)
- NEVER modify: .py, .js, .ts, .json, .yaml, .yml, .toml, .env, .lock, .css, .html, .xml, .sql, .sh
- If file has mixed content (prose + code), compress ONLY the prose sections
- If unsure whether something is code or prose, leave it unchanged
- Original file is backed up as FILE.original.md before overwriting
- Never compress FILE.original.md (skip it)
- No network / no Claude CLI / no Anthropic API for this skill
