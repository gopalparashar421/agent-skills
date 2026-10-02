---
name: document-lifecycle
description: >
  Unified document lifecycle. Terminal statuses, numbering via .next-id, close procedures,
  orphan detection, and Implementer-completion status/changelog updates for agent-output/.
  Load at session start or when impl finishes / close procedure needed.
license: MIT
metadata:
  author: groupzer0
  version: "1.1"
---

# Document Lifecycle Skill

Manage doc state transitions, unified numbering, automated closure across all agent-output dirs.

---

## Core Principle

Every work chain shares one ID. Analyst creates analysis 080 → downstream plan, impl, QA, UAT, critique all use ID 080. Enables human traceability across lifecycle.

Docs in terminal status belong in `closed/` subfolders. Active work stays visible; completed work archived but accessible.

---

## Terminal Statuses

These statuses trigger closure (move to `closed/`):

| Status | Meaning | Closed By |
|--------|---------|-----------|
| `Committed` | Changes committed to git (awaiting release) | DevOps |
| `Released` | Successfully pushed/published | DevOps |
| `Abandoned` | Explicitly dropped, will not proceed | User (manual) |
| `Deferred` | Postponed indefinitely | User (manual) |
| `Superseded` | Replaced by a newer document | User (manual) |
| `Resolved` | All findings addressed (critiques only) | Critic |

---

## Unified Numbering Protocol

### The `.next-id` File

Location: `agent-output/.next-id`

Contents: Single integer (e.g., `081`)

**Rules:**
- Only **originating agents** (Analyst, Planner when no analysis) read + increment
- Downstream agents **inherit** ID from source doc
- Never skip numbers; always use next available

### Document Header Format

Every doc in `agent-output/` MUST include:

```yaml
---
ID: 080                    # Global sequence number
Origin: 080                # Chain origin (same as ID for originating docs)
UUID: a3f7c2b1             # 8-char random hex for collision-proofing
Status: Active             # Current lifecycle state
---
```

### ID Assignment Rules

| Scenario | Action |
|----------|--------|
| Analyst starts new investigation | Read `.next-id`, increment, use as ID, write back |
| Planner creates plan from analysis | Inherit ID/Origin from analysis doc |
| Planner creates plan from user request (no analysis) | Read `.next-id`, increment, use as ID, write back |
| Implementer/QA/UAT/Critic work on plan | Inherit ID/Origin from plan doc |
| Retrospective reviews plan | Inherit ID/Origin from plan doc |

---

## Implementer Completion (auto / hook)

When Implementer finishes a work package (code+tests per plan), update `agent-output/` **before** QA handoff:

1. **Impl doc** (`agent-output/implementation/NNN-*.md`): set Status to reflect done-for-impl (e.g. `Implemented` / `Ready for QA` — not a terminal close status). Add changelog row with paths touched + date.
2. **Plan doc** (same ID): changelog note that impl landed; Status stay non-terminal until DevOps commit/release close.
3. **Cross-refs**: ensure plan ↔ impl links valid; no broken relative paths.
4. **Do not** move to `closed/` on Implementer complete — closure still DevOps/`Committed`/`Released` (or user Abandoned/Deferred).
5. **Do not** edit `agent-output/qa/` (Implementer read-only there).
6. Hook path: edit under `agent-output/implementation/` → marker → `stop` follow-up runs `self-learning` + this checklist. Manual: "update document-lifecycle for impl NNN".

See also: `self-learning` skill (instruction/skills capture) vs this skill (status/paths/closure only).

---

## Close Procedure

When doc reaches terminal status:

1. **Update Status field** to terminal status
2. **Add changelog entry**: `| YYYY-MM-DD | [Agent] | Document closed | Status: [status] |`
3. **Create closed folder** if needed: `mkdir -p agent-output/<domain>/closed/`
4. **Move file**: `mv agent-output/<domain>/NNN-name.md agent-output/<domain>/closed/`
5. **Log action**: "Closed document NNN-name.md (Status: [status])"

### Cross-Reference Handling

When referencing closed doc from another doc, use relative paths:
- From active doc: `../closed/080-feature.md`
- From closed doc to closed doc: `./080-feature.md` (same folder)

---

## Orphan Detection

### Agent Self-Check (Every Session Start)

Before work, each agent MUST:

1. Scan exclusive domain (e.g., `agent-output/qa/`) excluding `closed/`
2. Identify any doc with terminal Status
3. Move orphaned docs to `closed/`
4. Log: "Found orphaned document [name] with Status [status], moved to closed/"

### Roadmap Periodic Sweep

Roadmap agent runs full sweep when reviewing roadmap:

1. Scan ALL `agent-output/*/` dirs (excluding `closed/`)
2. Flag docs with terminal Status not in `closed/`
3. Report to user
4. Move to respective `closed/` folders

---

## Agent Responsibilities

| Agent | Role | Closure Trigger |
|-------|------|-----------------|
| Analyst | Originate IDs | Planner closes when plan created |
| Planner | Originate or inherit | DevOps closes after commit |
| Implementer | Inherit | DevOps closes after commit |
| QA | Inherit | DevOps closes after commit |
| UAT | Inherit | DevOps closes after commit |
| Critic | Inherit | Self-closes when findings resolved |
| DevOps | N/A | Self-closes after release |
| Retrospective | Inherit | PI closes after processing |
| PI | N/A | Self-closes own analysis |
| Architect | N/A | Evergreen docs, no closure |
| Roadmap | N/A | Orphan sweep responsibility |
| Security | Inherit | Self-check only |

---

## Quick Reference

### Creating a New Document (Originating)

```bash
# Read current ID
NEXT_ID=$(cat agent-output/.next-id)
# Increment for next use
echo $((NEXT_ID + 1)) > agent-output/.next-id
# Use $NEXT_ID as your document ID
```

### Closing a Document

```bash
# Update Status in document header to terminal status
# Add changelog entry
mkdir -p agent-output/<domain>/closed/
mv agent-output/<domain>/NNN-name.md agent-output/<domain>/closed/
```

### Self-Check Pattern

```
Before starting work:
1. List agent-output/<my-domain>/*.md (excluding closed/)
2. For each file, check Status field
3. If Status in [Committed, Released, Abandoned, Deferred, Superseded, Resolved]:
   → Move to closed/
```
