---
name: self-learning
description: >
  After an implementation completes, capture reusable lessons into AGENTS.md, README.md,
  and non-caveman skills — conservative surgical edits only. Excludes all caveman* skills.
  Use when implementation finishes, Implementer marks work done, user says "capture learnings",
  "/self-learning", or when the post-implementation stop hook fires.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Self-Learning

## Purpose

After impl done: distill clear, reusable guidance into project instruction files + non-caveman skills. No spam. No invent. Preserve technical accuracy.

## Triggers

| Trigger | When |
|---------|------|
| Hook `stop` follow-up | Marker set after edits under `agent-output/implementation/` then agent completes |
| Manual | User: `/self-learning`, "capture learnings", "update skills from impl" |
| Skill handoff | `implementer` / parent after successful impl before QA/review |

**Best available auto signal:** Cursor cannot perfectly detect "Implementer done". Repo uses: `afterFileEdit` on `agent-output/implementation/**` → write marker → `stop` hook (status completed, loop_count 0) → follow-up message that runs this skill. Manual fallback always valid.

## Inputs

Read when present (prefer current work chain ID):

- `agent-output/implementation/*.md` (active, not only `closed/`)
- Matching plan: `agent-output/planning/`
- Critique / QA notes if they record durable process lessons
- Diff / files touched this session (git status / recent edits)
- Existing `AGENTS.md`, root `README.md`, relevant `skills/*/SKILL.md`

## Outputs (WHERE APPLICABLE)

| Target | Update when |
|--------|-------------|
| `AGENTS.md` | Repo-wide durable convention agents must follow next time |
| Root `README.md` | Install/catalog/user-facing workflow change |
| `skills/<name>/SKILL.md` + references | Domain skill gap or wrong guidance exposed by impl |
| `docs/` (optional) | Methodology note that does not belong in a skill yet |

**Never auto-modify:** any `skills/caveman*` path (caveman, caveman-commit, caveman-compress, caveman-review, …).

## Constraints

- Conservative: only clear, reusable guidance. Skip one-off bugs, transient paths, secrets.
- Small surgical edits. Prefer bullet add / one paragraph over rewrites.
- Do not invent process the team did not practice.
- Do not expand scope into new features or refactors.
- Preserve accuracy; if unsure → skip or ask user one question.
- No commit unless user asked.
- Caveman* skills = hard exclude.

## Process

1. Confirm impl actually completed (impl doc status / user statement / substantial code+test change). If unclear → ask or stop.
2. List candidate lessons (max ~5). Drop anything not reusable.
3. Map each lesson → best target file (AGENTS / README / specific non-caveman skill).
4. Apply minimal edits. Mirror style of target file (if target already caveman-compressed, keep that intensity).
5. Optionally note in impl doc changelog: `Self-learning: updated X, Y`.
6. Report to user: files touched + one-line why. If nothing worth writing → say so (success = no spam).

## Checklist

```
Self-learning:
- [ ] Impl complete signal confirmed
- [ ] Lessons listed; one-offs discarded
- [ ] No caveman* paths in edit set
- [ ] AGENTS.md / README / skills updated only where applicable
- [ ] Edits surgical; technical claims verified against what was built
- [ ] User summary of changes (or explicit no-op)
```

## Hook wiring

Project hooks (see `.cursor/hooks.json` + `docs/hooks-methodology.md`):

1. `.cursor/hooks/mark-implementation-edit.py` — `afterFileEdit` when path matches `agent-output/implementation`
2. `.cursor/hooks/self-learning-stop.py` — `stop` reads marker; if set and `status=completed` and `loop_count=0`, emit `followup_message` to run this skill + clear marker
3. `loop_limit: 1` on stop hook — avoid follow-up storms

Manual fallback:

```
/self-learning
```

or: "Run self-learning skill on the work just completed."
