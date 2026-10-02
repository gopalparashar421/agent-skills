---
name: analysis-methodology
description: Systematic approach to converting unknowns to knowns through structured investigation with confidence levels and gap tracking. Use when analyzing bugs, investigating systems, or reducing uncertainty in technical findings.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Analysis Methodology

Convert unknowns → knowns via structured investigation.

## Core Principle

**Objective**: Every analysis session reduce uncertainty. Unknown unresolvable → document *why* + *what needed* to close.

---

## Confidence Levels

Classify every finding by evidence strength:

| Level | Label | Meaning | Example |
|---|---|---|---|
| 1 | **Proven** | Verified by code execution, POC, or reproducible test. | "Running `npm test -- --filter=X` confirms the error." |
| 2 | **Observed** | Seen in logs, monitoring, or direct inspection — not isolated. | "The error appears in production logs at 3am." |
| 3 | **Inferred** | Derived from docs, patterns, or logical deduction. | "The API docs suggest this should return 404." |

**Rule**: Level 3 (Inferred) → flag upgrade to Level 1 (Proven) before decisions.

---

## Gap Tracking Template

Surface remaining unknowns:

```markdown
## Remaining Gaps

| # | Unknown | Blocker | Required Action | Owner |
|---|---------|---------|-----------------|-------|
| 1 | Why does X fail under load? | Cannot reproduce locally. | Need staging access or load test harness. | [TBD] |
| 2 | Does API Y support pagination? | Docs unclear. | Contact vendor or run POC against sandbox. | [TBD] |
```

**Behaviors**:
- Populate table during investigation, not only at end.
- Surface table to user in chat before handoff.
- Mark "Resolved" (w/ link to finding) or "Deferred" (w/ rationale).

---

## Investigation Techniques

Move unknowns → knowns:

### Log Tracing
- Add targeted logging to isolate behavior.
- Compare expected vs actual log sequences.

### Component Isolation
- Reproduce w/ minimal dependencies.
- Mocks/stubs eliminate variables.

### Binary Search Debugging
- Narrow failure window: bisect commits, config, or code paths.
- Halve search space each step.

### POC Execution
- Minimal runnable code prove/disprove behavior.
- POCs reproducible by others (check in or share).

### Upstream Tracing
- Follow data/control flow backward → root cause.
- Ask: "Where did this value *come from*?"

---

## Analysis Document Structure

Recommended sections:

1. **Changelog** — Date, handoff context, outcome summary.
2. **Value Statement & Objective** — Why analysis matters.
3. **Context** — Background, scope, constraints.
4. **Methodology** — Techniques used (ref above).
5. **Findings** — Factual results by Confidence Level.
6. **Gap Tracking Table** — (see template above).
7. **Analysis Recommendations** — Next steps *to deepen inquiry* (not solutions).
8. **Open Questions** — Unresolved items needing user/agent input.

---

## Handoff Protocol

Before handoff to agent or user:

1. **List resolved unknowns** — What determined + confidence level.
2. **List remaining gaps** — Use Gap Tracking Table.
3. **State blockers explicitly** — What blocks further progress.
4. **Communicate in chat** — Don't rely on document alone; surface gaps directly.
