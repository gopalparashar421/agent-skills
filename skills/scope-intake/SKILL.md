---
name: scope-intake
description: >
  One-pass pre-plan intake that merges Planner scoping with Critic stress-tests early
  to save tokens. Use before writing a full plan, when user asks to scope a feature,
  "intake", "pre-plan critique", or when planning intent is clear but no plan exists yet.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Scope Intake

## Purpose

Single pass: understand scope + kill weak ideas early. Planner concerns + Critic concerns together. Save tokens vs full plan → full critique → revise loop when request still fuzzy.

## When

- New feature / epic / change request before `agent-output/planning/` draft
- User wants "scope this", "intake", "is this sane before we plan"
- Hook / session nudge when prompt looks like greenfield planning

**Not a replacement** for full Critic review on finished plans. This = early filter.

## One-pass checklist

Produce short intake note (chat or `agent-output/planning/NNN-intake.md` if ID chain started):

### Planner lens
- [ ] Value statement draft: As a … I want … so that …
- [ ] In / out of scope (3–7 bullets)
- [ ] Dependencies / unknowns needing Analyst
- [ ] Target release guess (if roadmap exists)
- [ ] Non-goals

### Critic lens (pre-plan)
- [ ] Ambiguities that would block Implementer
- [ ] Over-scope / gold-plating risks
- [ ] Missing constraints (security, data, compat)
- [ ] Alignment smell vs roadmap/architecture (if those docs exist)
- [ ] Go / reshape / stop recommendation

## Output shape

```markdown
# Intake: <title>
Status: Intake
Value: …
In scope: …
Out of scope: …
Risks / unknowns: …
Critic flags: …
Recommendation: Go | Reshape | Stop
Next: Planner full plan | Analyst research | drop
```

Keep terse. No impl code. No QA test plans.

## Token-saving combo

Intake (this skill) → only if **Go**: Planner full plan → Critic. Skip full plan when **Stop/Reshape** until scope fixed.
