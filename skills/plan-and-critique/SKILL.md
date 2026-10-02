---
name: plan-and-critique
description: >
  Combined Planner + Critic flow in one pass for medium-scope work. Saves tokens vs
  full plan then separate Critic round-trip. Use when user asks "plan and critique",
  "plan-and-critique", "draft plan with stress-test", or when scope is clear enough
  for one artifact but still needs a critique pass. Prefer `scope-intake` for fuzzy
  greenfield; keep separate Planner/Critic agents for large epics or formal handoffs.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Plan and Critique

## Purpose

One agent pass: write (or revise) plan **and** stress-test it. Additive entry point. Does **not** replace `planner` / `critic` agents — use those for big epics, formal handoffs, multi-revision critique threads.

## When

| Use this skill | Prefer separate agents / `scope-intake` |
|----------------|----------------------------------------|
| Medium feature, scope mostly clear | Fuzzy / greenfield → `scope-intake` first |
| User wants plan + critique in one shot | Large epic / many unknowns → Planner then Critic |
| Token budget tight; one doc round | Formal PM gate with dedicated Critic owner |

## Process

1. **Confirm scope.** If still fuzzy → stop and run `scope-intake` instead.
2. **Plan lens** (same constraints as Planner agent):
   - Value statement: As a … I want … so that …
   - In / out of scope, deps, risks, acceptance-level tasks
   - No impl code; no QA test cases (QA owns `agent-output/qa/`)
   - Write/update `agent-output/planning/NNN-….md` if chain ID exists; else draft in chat and ask before minting ID (`document-lifecycle`)
3. **Critique lens** (same spirit as Critic, lighter form):
   - Ambiguities that block Implementer
   - Over-scope, missing constraints, misalignment with roadmap/architecture if present
   - Go / Revise / Stop
4. **Emit both** in one response (and files when applicable):
   - Plan body (or path)
   - Short critique section or `agent-output/critiques/NNN-…-critique.md` when a numbered plan file exists
5. **If Revise:** fold critical fixes into the plan in the **same** pass when cheap; only split to Critic agent when findings need a dedicated thread.

## Output shape

```markdown
# Plan: <title>
Status: Draft | Ready for Implementer
…

## Critique (same pass)
Flags: …
Recommendation: Go | Revise | Stop
```

## Boundaries

- Still no source edits (planning/critique only)
- Still no writing QA docs
- Never touch `skills/caveman*`
- Large / contested plans → hand off to Critic agent after this pass
