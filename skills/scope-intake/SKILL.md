---
name: scope-intake
description: >
  Entrypoint skill for development work. Routes by clarity and size: interview-me when intent
  is fuzzy, optional idea-refine, then plan-and-critique or planner/critic/implementer.
  Use at session start for new work, "intake", "scope this", or before any plan.
license: MIT
metadata:
  author: groupzer0
  version: "2.0"
---

# Scope Intake (entrypoint)

## Purpose

Single entrypoint for new work. Decide **clarity** and **size**, run the right upstream skills, then hand off into the planning/impl chain. Uses `document-lifecycle` for any `agent-output/` artifacts.

## Flow (best of both worlds)

```
scope-intake                          ← START HERE
  ├─ underspecified intent?  → interview-me  → confirmed intent
  ├─ vague idea / many options? → suggest idea-refine (optional)
  └─ route by size (below)
        ├─ tiny        → edit + test (implementer optional)
        ├─ small       → planner → implementer → user review/commit
        ├─ medium      → [analysis-methodology if unknowns]
        │                → plan-and-critique → implementer → user review/commit
        └─ large       → roadmap → planner → critic → implementer
                         → qa / code-review-and-quality → user review/commit
```

After impl: `self-learning` (hook) + lifecycle status; never edit `skills/caveman*`.

## Step 0 — Clarity gate

Before scoping size, check intent:

| Signal | Action |
|--------|--------|
| Missing who / why / success / constraint | **Load `interview-me`** — stop this skill until confirmed intent exists |
| Confirmed intent already (or unambiguous ask) | Continue |
| Idea still mushy after intent ("I want X but don't know shape") | **Suggest `idea-refine`** — user can skip; do not force |
| Mechanical / typo / obvious one-liner | Skip intake; just change + test |

`interview-me` output (confirmed Outcome / User / Why now / Success / Constraint / Out of scope) is the **input** to later planning. Prefer that over the original vague ask.

If `idea-refine` ran, its one-pager / recommended direction feeds `plan-and-critique` or `planner`.

## Step 1 — Size route

| Signal | Load next |
|--------|-----------|
| Typo / one-liner / obvious fix | No plan skill; edit + test |
| Fuzzy / greenfield / many unknowns | Finish this intake note, then only on **Go** continue |
| Small + clear | `planner` → user ack → `implementer` |
| Medium + mostly clear | `plan-and-critique` (after optional analysis) |
| Large epic / multi-release / formal gates | `roadmap` → `planner` → `critic` → `implementer` |

**Not a replacement** for full `critic` on finished large plans. This skill = early filter + router.

## One-pass intake checklist

Produce short note (chat or `agent-output/planning/NNN-intake.md` if ID chain started — load `document-lifecycle`):

### Planner lens
- [ ] Value statement draft (or paste confirmed intent from `interview-me`)
- [ ] In / out of scope (3–7 bullets)
- [ ] Dependencies / unknowns → `analysis-methodology`?
- [ ] Target release guess (if roadmap exists)
- [ ] Non-goals

### Critic lens (pre-plan)
- [ ] Ambiguities that would block Implementer
- [ ] Over-scope / gold-plating
- [ ] Missing constraints (security, data, compat)
- [ ] Alignment vs roadmap/architecture if present
- [ ] Go / Reshape / Stop

## Output shape

```markdown
# Intake: <title>
Status: Intake
Intent source: interview-me | user | idea-refine
Value: …
In scope: …
Out of scope: …
Risks / unknowns: …
Critic flags: …
Recommendation: Go | Reshape | Stop
Next: plan-and-critique | planner | analysis-methodology | roadmap | drop
```

Keep terse. No impl code. No QA test plans.

## Token-saving rules

1. Interview before planning when confidence &lt; ~95% on intent.
2. Suggest `idea-refine` only when divergence/options help; skip when direction is already sharp.
3. Prefer `plan-and-critique` over planner↔critic ping-pong for medium work.
4. Reserve full `planner` → `critic` for large/contested epics.
5. Skip full plan on **Stop/Reshape** until scope fixed.
