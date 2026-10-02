# Hooks methodology

Cursor hooks wire this repo multi-agent flow. Caveman prose. Skills hold deep process; hooks nudge / gate / follow up.

Inspiration layout patterns: [addyosmani/agent-skills docs](https://github.com/addyosmani/agent-skills/tree/main/docs).

## Implemented now

| Hook event | Script | What fire | Why |
|------------|--------|-----------|-----|
| `sessionStart` | `.cursor/hooks/session-start.py` | Inject methodology blurb (lifecycle, scope-intake, self-learning) | Cheap shared context; cut "forgot the process" tokens |
| `afterFileEdit` | `.cursor/hooks/mark-implementation-edit.py` | If path under `agent-output/implementation/` → write marker | Best proxy for "Implementer touched docs" |
| `stop` | `.cursor/hooks/self-learning-stop.py` (`loop_limit: 1`) | On completed + marker → `followup_message` run `self-learning` + lifecycle touch | Auto learn without perfect "impl done" event |
| `beforeShellExecution` | `.cursor/hooks/tdd-gate-reminder.py` | Soft `agent_message` on commit/publish-ish commands | TDD reminder; fail-open allow |

Config: `.cursor/hooks.json`.

### Manual fallbacks

- Self-learning: `/self-learning` or "run self-learning skill"
- Lifecycle close: load `document-lifecycle` / `references/close-procedure.md`
- Scope intake: load `scope-intake` before full plan

**Limit:** Cursor no exact "Implementer agent finished" event. Marker + stop = best available. False positives possible if someone edits impl notes mid-spike — skill must stay conservative (no-op OK).

## Proposed (skill-level or future hooks)

| Idea | Level | Event / trigger | Notes |
|------|-------|-----------------|-------|
| Scope intake (Planner+Critic early) | **Skill** `scope-intake` + session blurb | User / Planner start | Token saver; not block-prompt |
| Doc lifecycle on Implementer complete | **Skill** + stop follow-up text | Same stop as self-learning | Status/changelog/cross-refs |
| Orphan sweep | Prompt / Roadmap / `sessionStart` remind | Session / roadmap review | Move terminal-status docs → `closed/` |
| Security gate | `beforeShellExecution` or pre-PR skill | `gh pr create`, deploy | Ask on risky; pair `security` agent |
| QA handoff | `subagentStop` / handoff text | Implementer → QA | Ensure QA doc exists; Implementer never edit `qa/` |
| Close after DevOps commit | `afterShellExecution` on `git commit` + devops | DevOps | Run close-procedure for chain ID |
| Critic after plan write | `afterFileEdit` on `agent-output/planning/` | Marker + stop | Optional; easy to annoy — prefer handoff |
| Pre-compact memory | `preCompact` | Context full | Reminder: compress memory via caveman-compress |

## Token-saving combinations

1. **Intake → Plan → Critic** — `scope-intake` first; skip full plan if Stop/Reshape.
2. **Self-learning on stop (once)** — `loop_limit: 1`; no-op if no reusable lesson.
3. **Session blurb not full skills** — hooks inject pointers; agent loads skill only when needed.
4. **Lifecycle + learning same follow-up** — one stop message, two checklists, one pass.

## Add a hook

Follow Cursor create-hook skill:

1. Pick narrow event
2. Edit `.cursor/hooks.json`
3. Add script under `.cursor/hooks/`
4. Prefer Python here (Windows-friendly): `python .cursor/hooks/….py`
5. Fail open unless safety-critical (`failClosed: true`)
6. Check Hooks tab / output channel

## Skills tied to hooks

- `self-learning` — post-impl capture
- `document-lifecycle` — status / close / orphans
- `scope-intake` — early Planner+Critic merge
- `testing-patterns` — TDD gate content
- `caveman-compress` — optional preCompact / memory hygiene (agent-applied; no Claude CLI)
