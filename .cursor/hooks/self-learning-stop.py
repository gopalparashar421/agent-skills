#!/usr/bin/env python3
"""stop: if implementation was edited this session, follow up with self-learning."""

from __future__ import annotations

import json
import sys
from pathlib import Path


MARKER = Path(".cursor") / "hooks" / "state" / "implementation-edited.marker"

FOLLOWUP = (
    "Implementation artifacts were edited this session. Run the `self-learning` skill now: "
    "capture only clear reusable lessons into AGENTS.md, README.md, and non-caveman skills "
    "(never modify skills/caveman*). Also apply `document-lifecycle` updates for the active "
    "impl chain (status/changelog/cross-refs) where Implementer completed. If nothing "
    "reusable, reply with an explicit no-op."
)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        json.dump({}, sys.stdout)
        sys.stdout.write("\n")
        return

    status = data.get("status")
    loop_count = int(data.get("loop_count") or 0)

    if status != "completed" or loop_count > 0 or not MARKER.is_file():
        json.dump({}, sys.stdout)
        sys.stdout.write("\n")
        return

    try:
        MARKER.unlink()
    except OSError:
        pass

    json.dump({"followup_message": FOLLOWUP}, sys.stdout)
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        json.dump({}, sys.stdout)
        sys.stdout.write("\n")
