# Hooks methodology

Cursor hooks wire this repo skills flow. Skills hold deep process; hooks nudge / gate / follow up.

Inspiration: [addyosmani/agent-skills docs](https://github.com/addyosmani/agent-skills/tree/main/docs).

## Implemented now

| Hook event | Script | What fire | Why |
|------------|--------|-----------|-----|
| `sessionStart` | `.cursor/hooks/session-start.py` | Inject methodology blurb (entrypoint, lifecycle, self-learning) | Cheap shared context |
| `afterFileEdit` | `.cursor/hooks/mark-implementation-edit.py` | If path under `agent-output/implementation/` → write marker | Proxy for "implementer touched docs" |
| `stop` | `.cursor/hooks/self-learning-stop.py` (`loop_limit: 1`) | On completed + marker → run `self-learning` + lifecycle touch | Auto learn without perfect "impl done" event |
| `beforeShellExecution` | `.cursor/hooks/tdd-gate-reminder.py` | Soft reminder on commit/publish-ish commands | TDD nudge; fail-open |

Config: `.cursor/hooks.json`.

### Manual fallbacks

- Self-learning: `/self-learning` or "run self-learning skill"
- Lifecycle close: load `document-lifecycle` / `references/close-procedure.md`
- Entrypoint: load `scope-intake` before planning

**Limit:** Cursor has no exact "implementer finished" event. Marker + stop = best available. Skills stay conservative (no-op OK).

## Token-saving combinations

1. **Entrypoint route** (`scope-intake` + session blurb):
   - Tiny fix → skip plan skills; edit + test
   - Underspecified → `interview-me` → confirmed intent
   - Wide idea → suggest `idea-refine`
   - Medium + clear → `plan-and-critique`
   - Large epic → `roadmap` → `planner` → `critic`
2. **Intake → plan** — skip full plan if Stop/Reshape.
3. **Self-learning on stop (once)** — `loop_limit: 1`.
4. **Session blurb not full skills** — hooks inject pointers; agent loads skill when needed.
5. **Lifecycle + learning same follow-up** — one stop message, two checklists.

## Skills tied to hooks

- `scope-intake` — entrypoint router
- `self-learning` — post-impl capture
- `document-lifecycle` — status / close / orphans + Implementer Completion
- `plan-and-critique` — medium clear scope
- `testing-patterns` — TDD gate content
- `caveman-compress` — optional preCompact / memory hygiene

## Add a hook

1. Pick narrow event
2. Edit `.cursor/hooks.json`
3. Add script under `.cursor/hooks/`
4. Prefer Python (Windows-friendly)
5. Fail open unless safety-critical
6. Check Hooks tab / output channel
