#!/usr/bin/env python3
"""sessionStart: inject methodology context (fail-open)."""

from __future__ import annotations

import json
import sys


CONTEXT = """## agent-skills methodology (session)
- Docs: `agent-output/` + `document-lifecycle` (IDs, status, closed/)
- Scope route: tiny fix → skip full plan; fuzzy/greenfield → `scope-intake`; medium clear → `plan-and-critique`; large epic → Planner then Critic agents
- Impl done: `self-learning` (hook may follow up) + lifecycle status/changelog; never edit caveman* skills
- Hooks: `docs/hooks-methodology.md` | config `.cursor/hooks.json`
- Orphan sweep: terminal-status docs not in `closed/` → move per document-lifecycle
"""


def main() -> None:
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    json.dump({"additional_context": CONTEXT}, sys.stdout)
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # fail open
        json.dump({}, sys.stdout)
        sys.stdout.write("\n")
