#!/usr/bin/env python3
"""afterFileEdit: mark when agent-output/implementation files change."""

from __future__ import annotations

import json
import sys
from pathlib import Path


MARKER = Path(".cursor") / "hooks" / "state" / "implementation-edited.marker"


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    path = str(data.get("file_path") or "").replace("\\", "/").lower()
    if "agent-output/implementation" not in path:
        return
    if path.endswith(".marker"):
        return

    MARKER.parent.mkdir(parents=True, exist_ok=True)
    MARKER.write_text(path + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    # afterFileEdit: no required output fields
