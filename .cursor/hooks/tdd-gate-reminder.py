#!/usr/bin/env python3
"""beforeShellExecution: soft TDD reminder for impl-like commands (ask, never blind-deny)."""

from __future__ import annotations

import json
import re
import sys


# Commands that often mean "writing production code without tests in the same breath"
IMPL_HINT = re.compile(
    r"(^|[;&|]\s*)((git\s+commit)|npm\s+publish|pip\s+install\s+-e)",
    re.IGNORECASE,
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        json.dump({"permission": "allow"}, sys.stdout)
        sys.stdout.write("\n")
        return

    command = str(data.get("command") or "")
    if IMPL_HINT.search(command):
        json.dump(
            {
                "permission": "allow",
                "agent_message": (
                    "TDD gate reminder: new feature code needs failing test before impl "
                    "(testing-patterns skill). Confirm tests exist for this change."
                ),
            },
            sys.stdout,
        )
        sys.stdout.write("\n")
        return

    json.dump({"permission": "allow"}, sys.stdout)
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        json.dump({"permission": "allow"}, sys.stdout)
        sys.stdout.write("\n")
