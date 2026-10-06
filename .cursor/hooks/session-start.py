#!/usr/bin/env python3
"""sessionStart: inject methodology context (fail-open)."""

from __future__ import annotations

import json
import sys


CONTEXT = """## agent-skills methodology (session)
- Entrypoint: `scope-intake` (clarity → size route)
- Clarity: underspecified → `interview-me`; wide solution space → suggest `idea-refine`
- Size: tiny → edit+test; small → `planner`→`implementer`; medium → `plan-and-critique`; large → `roadmap`→`planner`→`critic`→`implementer`
- Docs: `agent-output/` + `document-lifecycle` (IDs, status, closed/); user closes after commit
- Impl done: `self-learning` (hook may follow up) + lifecycle; never edit caveman* skills
- Hooks: `docs/hooks-methodology.md` | config `.cursor/hooks.json`
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
