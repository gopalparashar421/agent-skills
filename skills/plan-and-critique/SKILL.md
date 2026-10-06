---
name: plan-and-critique
description: >
  Combined planner + critic flow in one pass for medium-scope work. Use after scope-intake
  (and interview-me / idea-refine when used), or when user asks "plan and critique".
  Prefer scope-intake for fuzzy greenfield; separate planner then critic skills for large epics.
license: MIT
metadata:
  author: groupzer0
  version: "2.0"
---

# Plan and Critique

## Purpose

One pass: write (or revise) plan **and** stress-test it. Token saver vs full `planner` → `critic` round-trip. Does **not** replace those skills for large epics or multi-revision critique threads.

**Common skills:** `document-lifecycle` (when minting/updating `agent-output/` docs), `engineering-standards`.

## Skill hooks

| When | Next |
|------|------|
| Entrypoint / fuzzy | `scope-intake` first |
| Underspecified intent | `interview-me` — confirmed intent is **required input** |
| Idea still broad after intent | **Suggest `idea-refine`** before this skill; continue only if user declines or refine done |
| Unknowns | `analysis-methodology` before or mid-pass |
| Go | `implementer` |
| Contested / large findings | hand off to dedicated `critic` |
| Architecture risk | `architect` |

## When

| Use this skill | Prefer instead |
|----------------|----------------|
| Medium feature, scope mostly clear | Fuzzy → `scope-intake` (+ maybe `interview-me`) |
| User wants plan + critique in one shot | Large epic → `roadmap` → `planner` → `critic` |
| Token budget tight | Formal gate needing dedicated critique owner → `critic` |

## Process

1. **Confirm inputs.**  
   - No clear intent → stop; run `interview-me`.  
   - Intent clear but solution space wide → suggest `idea-refine`; wait for user choice.  
   - Still fuzzy on boundaries → stop; run `scope-intake`.
2. **Plan lens** (same constraints as `planner`):
   - Value statement from confirmed intent
   - In/out of scope, deps, risks, acceptance-level tasks
   - No impl code; no QA test cases (`qa` owns those)
   - Write/update `agent-output/planning/NNN-….md` per `document-lifecycle`
3. **Critique lens** (same spirit as `critic`, lighter):
   - Ambiguities that block Implementer
   - Over-scope, missing constraints, misalignment with roadmap/architecture
   - Unresolved `OPEN QUESTION` → surface; do not silent-approve
   - Go / Revise / Stop
4. **Emit both** in one response (and files when applicable).
5. **If Revise:** fold critical fixes into the plan in the **same** pass when cheap; split to `critic` only when findings need a dedicated thread.

## Output shape

```markdown
# Plan: <title>
Status: Draft | Ready for Implementer
Intent: [from interview-me / user]
…

## Critique (same pass)
Flags: …
Recommendation: Go | Revise | Stop
Next: implementer | critic | planner | analysis-methodology
```

## Boundaries

- No source edits (planning/critique only)
- No writing QA docs
- Never touch `skills/caveman*`
- Large / contested plans → `critic` after this pass
