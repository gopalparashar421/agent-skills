---
name: document-lifecycle
description: >
  Unified document lifecycle. Terminal statuses, numbering via .next-id, close procedures,
  orphan detection, and Implementer-completion status/changelog updates for agent-output/.
  Load at session start or when impl finishes / close procedure needed. Used by all persona skills.
license: MIT
metadata:
  author: groupzer0
  version: "2.0"
---

# Document Lifecycle

Manage doc state transitions, unified numbering, closure across all `agent-output/` dirs.

**All persona skills** (`planner`, `critic`, `implementer`, `qa`, `architect`, `roadmap`, plus `plan-and-critique` / `scope-intake` when writing files) load this skill. Addyosmani-style skills (`interview-me`, `idea-refine`, `code-review-and-quality`, …) use it whenever they touch `agent-output/`.

---

## Core principle

Every work chain shares one ID. Originating skill mints analysis/plan `080` → downstream plan, critique, impl, QA all use ID `080`.

Docs in terminal status belong in `closed/` subfolders.

---

## Terminal statuses

| Status | Meaning | Closed by |
|--------|---------|-----------|
| `Committed` | Changes committed to git (awaiting release) | User (manual review/commit) |
| `Released` | Successfully pushed/published | User |
| `Abandoned` | Explicitly dropped | User |
| `Deferred` | Postponed indefinitely | User |
| `Superseded` | Replaced by a newer document | User |
| `Resolved` | All findings addressed (critiques only) | `critic` skill |

---

## Unified numbering

Location: `agent-output/.next-id` — single integer.

**Rules:**
- Only **originating** skills (`analysis-methodology` when writing analysis, or `planner` / `plan-and-critique` when no analysis) read + increment
- Downstream skills **inherit** ID from source doc
- Never skip numbers

### Document header

```yaml
---
ID: 080
Origin: 080
UUID: a3f7c2b1
Status: Active
---
```

### ID assignment

| Scenario | Action |
|----------|--------|
| Analysis starts new investigation | Read `.next-id`, increment, use as ID |
| Planner / plan-and-critique from analysis | Inherit; close analysis → `Planned` |
| Planner / plan-and-critique from user request | Read `.next-id`, increment |
| Implementer / QA / Critic on plan | Inherit from plan |
| Intake note with chain ID | Inherit or originate per above |

---

## Implementer completion (auto / hook)

When `implementer` finishes a work package (code+tests per plan), update `agent-output/` **before** QA/review:

1. **Impl doc:** Status e.g. `Implemented` / `Ready for QA` (not terminal). Changelog with paths + date.
2. **Plan doc:** changelog note; Status stays non-terminal until user commit/release close.
3. **Cross-refs:** plan ↔ impl links valid.
4. **Do not** move to `closed/` on impl complete — closure on `Committed`/`Released` (or Abandoned/Deferred).
5. **Do not** edit `agent-output/qa/` (implementer read-only).
6. Hook: edit under `agent-output/implementation/` → marker → `stop` follow-up runs `self-learning` + this checklist.

See also: `self-learning` (instruction/skills capture) vs this skill (status/paths/closure only).

---

## Close procedure

See [references/close-procedure.md](references/close-procedure.md).

When doc reaches terminal status:

1. Update Status field
2. Add changelog entry
3. `mkdir` domain `closed/` if needed
4. Move file into `closed/`
5. Log action

**Bulk close after user commit:** close planning + implementation + qa (+ critiques if resolved) for the chain ID.

---

## Orphan detection

### Self-check (every skill start)

Scan exclusive domain excluding `closed/`; move terminal-status orphans.

### Roadmap sweep

`roadmap` skill runs full sweep across all `agent-output/*/`.

---

## Skill responsibilities

| Skill | Role | Closure trigger |
|-------|------|-----------------|
| `analysis-methodology` | May originate IDs (analysis docs) | Planner closes when plan created |
| `planner` / `plan-and-critique` | Originate or inherit | User closes after commit |
| `implementer` | Inherit | User closes after commit |
| `qa` | Inherit | User closes after commit |
| `critic` | Inherit | Self-closes when findings resolved |
| `architect` | Evergreen master; findings inherit | Findings follow standard close |
| `roadmap` | Evergreen + orphan sweep | N/A |
| `code-review-and-quality` | Optional review notes | User closes after commit |
| User (manual) | Commit / release | Sets `Committed` / `Released` + bulk close |

---

## Quick reference

```bash
NEXT_ID=$(cat agent-output/.next-id)
echo $((NEXT_ID + 1)) > agent-output/.next-id
# use $NEXT_ID

mkdir -p agent-output/<domain>/closed/
mv agent-output/<domain>/NNN-name.md agent-output/<domain>/closed/
```
