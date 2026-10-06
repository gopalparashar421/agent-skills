# agent-skills

Installable **Agent Skills** for Cursor, Claude Code, GitHub Copilot, Windsurf, and any client that supports the [Agent Skills spec](https://agentskills.io/specification).

Repo: [gopalparashar421/agent-skills](https://github.com/gopalparashar421/agent-skills).

Merges two methodologies:

1. **Personal lifecycle skills** — planner / critic / implementer / roadmap / qa / architect + `document-lifecycle`
2. **addyosmani-style skills** — `interview-me`, `idea-refine`, `code-review-and-quality`, `code-simplification`, `context-engineering`, `performance-optimization`

Personas used to live under `agents/` (Cursor/Copilot agent picker only). They are now **skills** so `npx skills add` installs the full workflow.

## Entrypoint

**Start with `scope-intake`.** It routes by clarity and size:

```
scope-intake
  ├─ underspecified?     → interview-me → confirmed intent
  ├─ wide solution space? → suggest idea-refine (optional)
  └─ size route
        tiny    → edit + test
        small   → planner → implementer → user review/commit
        medium  → [analysis-methodology if unknowns]
                  → plan-and-critique → implementer → user review/commit
        large   → roadmap → planner → critic → implementer
                  → qa / code-review-and-quality → user review/commit
```

After impl: `self-learning` (Cursor stop hook may auto-run) + `document-lifecycle` status updates. User owns review/commit and doc closure. Never auto-edit `skills/caveman*`.

### Scope cheatsheet (personal habits + addyosmani)

| Scope | Flow |
|-------|------|
| Smaller | `planner` → `implementer` → manual review/commit |
| Medium | `analysis-methodology` (if needed) → `plan-and-critique` → `implementer` → manual review/commit |
| Larger | `roadmap` → `planner` → `critic` → `implementer` → manual review/commit |

Upstream of all three when needed: `interview-me` → (optional `idea-refine`) → planning skill. Confirmed intent from `interview-me` is the input to `plan-and-critique` / `planner`.

## Install

```bash
npx skills add gopalparashar421/agent-skills --list
npx skills add gopalparashar421/agent-skills
npx skills add gopalparashar421/agent-skills --skill scope-intake
npx skills add gopalparashar421/agent-skills --skill self-learning --skill document-lifecycle
```

CLI: [vercel-labs/skills](https://github.com/vercel-labs/skills). Discovers `skills/*/SKILL.md`.

### Project hooks (Cursor)

This repo ships `.cursor/hooks.json` + scripts. After clone/open in Cursor, hooks load for **this** project. Copy `.cursor/hooks*` into an app repo to reuse self-learning / lifecycle follow-ups.

See [docs/hooks-methodology.md](docs/hooks-methodology.md).

## Catalog

### Entrypoint & orchestration

| Skill | Role |
|-------|------|
| `scope-intake` | **Entrypoint** — clarity gate + size router |
| `interview-me` | One-question-at-a-time intent extraction |
| `idea-refine` | Divergent/convergent ideation before planning |
| `plan-and-critique` | One-pass plan + stress-test (medium) |
| `document-lifecycle` | IDs, status, close, impl-complete updates |
| `self-learning` | Post-impl → AGENTS/README/skills (never caveman*) |

### Persona skills (ex-agents/)

| Skill | Role |
|-------|------|
| `roadmap` | Outcome roadmap + release tracker + orphan sweep |
| `planner` | Impl-ready plans in `agent-output/planning/` |
| `critic` | Pre-impl plan stress-test → `agent-output/critiques/` |
| `implementer` | TDD-first execution → `agent-output/implementation/` |
| `qa` | Test strategy + execution → `agent-output/qa/` |
| `architect` | System architecture / ADRs / debt |

### Shared engineering

| Skill | Role |
|-------|------|
| `analysis-methodology` | Confidence + gap tracking (medium unknowns) |
| `architecture-patterns` | ADRs / anti-patterns / diagrams |
| `engineering-standards` | SOLID / DRY / YAGNI / KISS |
| `testing-patterns` | TDD / pyramid / anti-patterns |
| `release-procedures` | Semver + version consistency (user-driven release) |
| `code-review-and-quality` | Post-impl multi-axis review (replaces code-reviewer agent) |
| `code-simplification` | Clarity refactors without behavior change |
| `context-engineering` | Session/context setup |
| `performance-optimization` | FE/BE/query performance |

### Caveman (token savers)

| Skill | Role |
|-------|------|
| `caveman` | Terse talk (~75% fewer response tokens) |
| `caveman-commit` | Terse Conventional Commits |
| `caveman-compress` | Compress memory files (agent-applied; no Claude CLI) |
| `caveman-review` | One-line PR comments |

## Consolidation notes

| Removed / merged | Why |
|------------------|-----|
| `agents/` personas | Converted to persona skills above (`npx skills` compatible) |
| `code-review-standards` | Orphaned with deleted code-reviewer; covered by `code-review-and-quality` |
| `code-review-checklist` | Pre-impl checklist merged into `critic`; post-impl covered by `code-review-and-quality` |
| analyst / devops / uat / security / pi / retrospective agents | Deleted earlier; unused. Analysis → `analysis-methodology`; release/close → user + `release-procedures` / `document-lifecycle`; review → `code-review-and-quality` |

Common skills (`document-lifecycle`, `engineering-standards`, `testing-patterns`, …) stay shared — persona skills load them instead of duplicating.

## Layout

```
agent-skills/
├── skills/                 # SKILL.md modules (+ optional scripts/references)
├── .cursor/hooks.json      # Cursor hooks (self-learning, TDD nudge, …)
├── docs/hooks-methodology.md
├── plugin.json             # Claude plugin metadata
└── .claude-plugin/         # Marketplace metadata
```

## Hooks methodology (short)

- `sessionStart` → entrypoint / scope-route blurb
- `afterFileEdit` on `agent-output/implementation/**` → marker
- `stop` → `self-learning` + lifecycle touch (`loop_limit: 1`)
- `beforeShellExecution` → soft TDD reminder

Token savers: `scope-intake` / `plan-and-critique` / keep full `planner`→`critic` for big epics only.

## Caveman note

`caveman-compress`: agent compresses in-process. Backup `FILE.original.md` once. Never compress backups. Optional `skills/caveman-compress/scripts/` = validators / legacy only.
