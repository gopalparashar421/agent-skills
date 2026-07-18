# agent-skills

Installable **custom agents** and **Agent Skills** for Cursor, Claude Code, GitHub Copilot, and Windsurf.

Skills follow the [Agent Skills specification](https://agentskills.io/specification).

## Agents vs skills

| Layer | Role | UI |
|-------|------|----|
| `agents/` | Personas (Planner, Critic, Architect, …) with handoffs and tools | Cursor / Copilot agent dropdown and slash-select |
| `skills/` | Reusable knowledge modules (standards, checklists, caveman, …) | Auto-loaded when relevant; primary surface for Claude |

**Keep both agents and skills.** Agents alone are not enough: many agents instruct the model to load skills by name, and Claude Code is skills-first. Do not port personas into skills — that duplicates agents without giving Claude/Cursor the right UI behavior.

Per-skill docs under `skills/<name>/references/` install with the skill (e.g. `.cursor/skills/testing-patterns/references/`). Agents load those as `testing-patterns/references/...`.

## Install

Requires Python 3.9+.

```bash
git clone <this-repo-url>
cd agent-skills
python scripts/install.py
```

Interactive mode prompts for IDE tools and project vs global scope.

### Non-interactive examples

```bash
# Cursor + Claude into the current project
python scripts/install.py --tools cursor,claude --project -y

# Copilot into a specific repo
python scripts/install.py --tools copilot --project --path /path/to/your/repo -y

# Global Cursor install
python scripts/install.py --tools cursor --global -y

# Subset of skills and agents
python scripts/install.py --tools cursor --skills caveman,testing-patterns --agents planner,critic -y

# Overwrite existing installs
python scripts/install.py --tools all --project --force -y

# List catalog
python scripts/install.py --list
```

### Flags

| Flag | Meaning |
|------|---------|
| `--tools` | `cursor`, `claude`, `copilot`, `windsurf`, or `all` |
| `--project` | Install into the target repo (default) |
| `--global` | Install into user home directories |
| `--path` | Target project root (default: cwd) |
| `--skills` / `--agents` | Comma-separated names, or `all` |
| `--no-skills` / `--no-agents` | Skip a payload |
| `--force` | Overwrite existing files |
| `-y` | Skip confirmation |
| `--list` | Print catalog and exit |

### Where files go

**Skills**

| Tool | Project | Global |
|------|---------|--------|
| Cursor | `.cursor/skills/<name>/` | `~/.cursor/skills/<name>/` |
| Claude | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` |
| Copilot | `.github/skills/<name>/` | `~/.copilot/skills/<name>/` |
| Windsurf | `.windsurf/skills/<name>/` | `~/.codeium/windsurf/skills/<name>/` |

**Agents**

| Tool | Project | Global | Filename |
|------|---------|--------|----------|
| Copilot | `.github/agents/` | `~/.copilot/agents/` | `*.agent.md` |
| Cursor | `.cursor/agents/` | `~/.cursor/agents/` | `*.md` (`.agent` stripped) |
| Claude | `.claude/agents/` | `~/.claude/agents/` | `*.md` (best-effort) |
| Windsurf | — | — | Agents skipped |

## Catalog

### Agents

| Agent | Description |
|-------|-------------|
| `analyst` | Research and analysis specialist for code-level investigation |
| `architect` | Architectural coherence and technical debt review |
| `code-reviewer` | Code quality and maintainability review before QA |
| `critic` | Stress-tests planning documents |
| `devops` | Packaging, versioning, deployment readiness, releases |
| `implementer` | Implements approved plans |
| `pi` | Process improvement from retrospectives |
| `planner` | High-rigor planning for feature changes |
| `qa` | Test coverage and execution verification |
| `retrospective` | Lessons learned after implementation |
| `roadmap` | Outcome-focused product roadmap |
| `security` | Security audit across architecture, code, dependencies |
| `uat` | UAT against stated business value |

### Skills

| Skill | Description |
|-------|-------------|
| `analysis-methodology` | Confidence levels and gap tracking for investigations |
| `architecture-patterns` | ADRs, patterns, anti-pattern detection |
| `caveman` | Ultra-compressed communication mode |
| `caveman-commit` | Terse Conventional Commits messages |
| `caveman-compress` | Compress memory files to save tokens |
| `caveman-review` | One-line PR review comments |
| `code-review-checklist` | Pre/post-implementation review criteria |
| `code-review-standards` | Checklists, severity, review templates |
| `document-lifecycle` | Doc statuses, IDs, close procedures |
| `engineering-standards` | SOLID, DRY, YAGNI, KISS |
| `release-procedures` | Semver, release verification, deployment |
| `testing-patterns` | TDD, pyramid, coverage, anti-patterns |

## Layout

```
agent-skills/
├── agents/           # Custom agent personas (*.agent.md)
├── skills/           # Agent Skills (SKILL.md + optional scripts/references)
├── scripts/
│   └── install.py    # Cross-platform installer
└── README.md
```
