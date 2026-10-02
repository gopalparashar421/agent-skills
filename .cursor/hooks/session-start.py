#!/usr/bin/env python3
"""sessionStart: inject methodology context (fail-open)."""

from __future__ import annotations

import json
import sys


CONTEXT = """## agent-skills methodology (session)
- Docs: `agent-output/` + `document-lifecycle` skill (IDs, status, closed/)
- New / fuzzy scope: load `scope-intake` before full Planner pass
- Impl done: `self-learning` skill (hook may auto-follow up); never edit caveman* skills
- Hooks plan: `docs/hooks-methodology.md`
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
