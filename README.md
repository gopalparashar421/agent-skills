# agent-skills

Installable **custom agents** + **Agent Skills** for Cursor, Claude Code, GitHub Copilot, Windsurf.

Repo: [gopalparashar421/agent-skills](https://github.com/gopalparashar421/agent-skills). Skills follow [Agent Skills spec](https://agentskills.io/specification).

Docs / layout patterns inspired by [addyosmani/agent-skills docs](https://github.com/addyosmani/agent-skills/tree/main/docs).

## Agents vs skills

| Layer | Role | UI |
|-------|------|----|
| `agents/` | Personas (Planner, Critic, Implementer, …) + handoffs | Cursor / Copilot agent picker |
| `skills/` | Reusable workflows (standards, caveman, lifecycle, …) | Auto / slash when description matches |

Keep both. Agents load skills by name. Claude Code = skills-first. Do not duplicate personas into skills.

## Install

### Fast path — `npx skills` (any agent)

```bash
npx skills add gopalparashar421/agent-skills --list
npx skills add gopalparashar421/agent-skills
npx skills add gopalparashar421/agent-skills --skill caveman-compress
npx skills add gopalparashar421/agent-skills --skill self-learning --skill document-lifecycle
```

CLI: [vercel-labs/skills](https://github.com/vercel-labs/skills). Discovers `skills/*/SKILL.md`. Use `--skill <name>` for one skill; omit for interactive/all.

### Python installer (agents + skills, multi-tool)

Requires Python 3.9+.

```bash
git clone https://github.com/gopalparashar421/agent-skills.git
cd agent-skills
python scripts/install.py
```

```bash
python scripts/install.py --tools cursor,claude --project -y
python scripts/install.py --tools cursor --skills caveman,testing-patterns --agents planner,critic -y
python scripts/install.py --list
```

| Flag | Meaning |
|------|---------|
| `--tools` | `cursor`, `claude`, `copilot`, `windsurf`, or `all` |
| `--project` / `--global` | Install scope |
| `--skills` / `--agents` | Names or `all` |
| `--force` / `-y` | Overwrite / skip confirm |

**Skills land in:** Cursor `.cursor/skills/`, Claude `.claude/skills/`, Copilot `.github/skills/`, Windsurf `.windsurf/skills/` (project or `~/…` global).

**Agents:** Copilot keeps `*.agent.md`; Cursor/Claude strip to `*.md`.

### Project hooks (Cursor)

This repo ships `.cursor/hooks.json` + scripts. After clone/open in Cursor, hooks load for **this** project. Copy `.cursor/hooks*` into your app repo if you want the same self-learning / lifecycle follow-ups there.

See [docs/hooks-methodology.md](docs/hooks-methodology.md).

## Catalog

### Agents

| Agent | Role |
|-------|------|
| `analyst` | Code-level research |
| `architect` | Architecture / debt |
| `code-reviewer` | Pre-QA quality review |
| `critic` | Stress-test plans |
| `devops` | Release / deploy readiness |
| `implementer` | Execute approved plans |
| `pi` | Process improvement |
| `planner` | Feature planning |
| `qa` | Test verification |
| `retrospective` | Lessons after impl |
| `roadmap` | Outcome roadmap |
| `security` | Security audit |
| `uat` | Business-value UAT |

### Skills

| Skill | Role |
|-------|------|
| `analysis-methodology` | Confidence + gap tracking |
| `architecture-patterns` | ADRs / patterns |
| `caveman` | Terse talk (~75% fewer response tokens) |
| `caveman-commit` | Terse Conventional Commits |
| `caveman-compress` | Compress memory files (agent-applied; no Claude CLI) |
| `caveman-review` | One-line PR comments |
| `code-review-checklist` | Pre/post impl review |
| `code-review-standards` | Severity + templates |
| `document-lifecycle` | IDs, status, close, impl-complete updates |
| `engineering-standards` | SOLID / DRY / YAGNI / KISS |
| `plan-and-critique` | One-pass plan + stress-test (medium scope) |
| `release-procedures` | Semver / ship checks |
| `scope-intake` | Pre-plan Planner+Critic filter |
| `self-learning` | Post-impl → AGENTS/README/skills (never caveman*) |
| `testing-patterns` | TDD / pyramid / anti-patterns |

## Layout

```
agent-skills/
├── agents/              # *.agent.md personas
├── skills/              # SKILL.md modules (+ optional scripts/references)
├── scripts/install.py   # Multi-tool installer
├── .cursor/hooks.json   # Cursor hooks (self-learning, TDD nudge, …)
├── docs/hooks-methodology.md
├── plugin.json          # Claude plugin metadata
└── .claude-plugin/      # Marketplace metadata
```

## Hooks methodology (short)

- `sessionStart` → scope-route blurb
- `afterFileEdit` on `agent-output/implementation/**` → marker
- `stop` → `self-learning` + lifecycle touch (`loop_limit: 1`)
- `beforeShellExecution` → soft TDD reminder

Token savers: `scope-intake` / `plan-and-critique` / keep full Planner↔Critic for big epics only.

## Caveman note

`caveman-compress`: agent compresses in-process. Backup `FILE.original.md` once. Never compress backups. Optional `skills/caveman-compress/scripts/` = validators / legacy only.
