#!/usr/bin/env python3
"""Install agents and skills into a target project or user home."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Iterable

CATALOG_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = CATALOG_ROOT / "skills"
AGENTS_DIR = CATALOG_ROOT / "agents"

TOOL_IDS = ("cursor", "claude", "copilot", "windsurf")

# agent_mode: "agent.md" keep *.agent.md | "md" strip .agent -> name.md | None skip agents
TOOL_CONFIG = {
    "cursor": {
        "project_skills": Path(".cursor") / "skills",
        "global_skills": lambda home: home / ".cursor" / "skills",
        "project_agents": Path(".cursor") / "agents",
        "global_agents": lambda home: home / ".cursor" / "agents",
        "agent_mode": "md",
        "supports_agents": True,
    },
    "claude": {
        "project_skills": Path(".claude") / "skills",
        "global_skills": lambda home: home / ".claude" / "skills",
        "project_agents": Path(".claude") / "agents",
        "global_agents": lambda home: home / ".claude" / "agents",
        "agent_mode": "md",
        "supports_agents": True,
    },
    "copilot": {
        "project_skills": Path(".github") / "skills",
        "global_skills": lambda home: home / ".copilot" / "skills",
        "project_agents": Path(".github") / "agents",
        "global_agents": lambda home: home / ".copilot" / "agents",
        "agent_mode": "agent.md",
        "supports_agents": True,
    },
    "windsurf": {
        "project_skills": Path(".windsurf") / "skills",
        "global_skills": lambda home: home / ".codeium" / "windsurf" / "skills",
        "project_agents": None,
        "global_agents": None,
        "agent_mode": None,
        "supports_agents": False,
    },
}


def home_dir() -> Path:
    return Path.home()


def discover_skills() -> list[Path]:
    if not SKILLS_DIR.is_dir():
        return []
    skills = []
    for path in sorted(SKILLS_DIR.iterdir()):
        if path.is_dir() and (path / "SKILL.md").is_file():
            skills.append(path)
    return skills


def discover_agents() -> list[Path]:
    if not AGENTS_DIR.is_dir():
        return []
    return sorted(AGENTS_DIR.glob("*.agent.md"))


def parse_frontmatter_field(skill_md: Path, field: str) -> str:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    block = text[3:end]
    pattern = rf"^{re.escape(field)}:\s*(?:>\s*)?(.*?)(?=\n[a-zA-Z0-9_-]+:|\Z)"
    match = re.search(pattern, block, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    raw = match.group(1).strip()
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    return " ".join(lines)


def skill_description(skill_dir: Path) -> str:
    return parse_frontmatter_field(skill_dir / "SKILL.md", "description") or "(no description)"


def agent_stem(path: Path) -> str:
    name = path.name
    if name.endswith(".agent.md"):
        return name[: -len(".agent.md")]
    return path.stem


def agent_dest_name(source: Path, mode: str) -> str:
    stem = agent_stem(source)
    if mode == "agent.md":
        return f"{stem}.agent.md"
    if mode == "md":
        return f"{stem}.md"
    raise ValueError(f"Unknown agent filename mode: {mode}")


def parse_csv_list(value: str | None, allowed: Iterable[str] | None = None) -> list[str] | None:
    if value is None:
        return None
    if value.strip().lower() == "all":
        return list(allowed) if allowed is not None else ["all"]
    items = [part.strip() for part in value.split(",") if part.strip()]
    if allowed is not None:
        allowed_set = set(allowed)
        bad = [i for i in items if i not in allowed_set]
        if bad:
            raise SystemExit(f"Unknown value(s): {', '.join(bad)}. Allowed: {', '.join(allowed)}")
    return items


def prompt_yes_no(question: str, default: bool = True) -> bool:
    suffix = " [Y/n] " if default else " [y/N] "
    try:
        answer = input(question + suffix).strip().lower()
    except EOFError:
        return default
    if not answer:
        return default
    return answer in ("y", "yes")


def prompt_multi_select(title: str, options: list[tuple[str, str]], default_all: bool = True) -> list[str]:
    print(f"\n{title}")
    for i, (key, label) in enumerate(options, 1):
        print(f"  {i}. {label} ({key})")
    print("  Enter numbers separated by commas, or 'all'.")
    default_hint = "all" if default_all else "1"
    try:
        raw = input(f"Choice [{default_hint}]: ").strip().lower()
    except EOFError:
        raw = default_hint
    if not raw:
        raw = default_hint
    if raw == "all":
        return [key for key, _ in options]
    chosen: list[str] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            idx = int(part)
        except ValueError:
            raise SystemExit(f"Invalid selection: {part}")
        if idx < 1 or idx > len(options):
            raise SystemExit(f"Selection out of range: {idx}")
        chosen.append(options[idx - 1][0])
    if not chosen:
        raise SystemExit("No tools selected.")
    return chosen


def prompt_scope() -> bool:
    """Return True for global, False for project."""
    print("\nInstall scope:")
    print("  1. Project (into the target repository) [default]")
    print("  2. Global (user home directories)")
    try:
        raw = input("Choice [1]: ").strip()
    except EOFError:
        raw = "1"
    if not raw:
        raw = "1"
    if raw == "2":
        return True
    if raw == "1":
        return False
    raise SystemExit(f"Invalid scope choice: {raw}")


def _same_path(a: Path, b: Path) -> bool:
    try:
        return a.resolve() == b.resolve()
    except OSError:
        return False


def copy_tree(src: Path, dest: Path, force: bool) -> str:
    if _same_path(src, dest):
        return "already present (catalog path)"
    if dest.exists():
        if not force:
            return "skipped (exists; use --force)"
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)
    return "installed"


def copy_file(src: Path, dest: Path, force: bool) -> str:
    if _same_path(src, dest):
        return "already present (catalog path)"
    if dest.exists() and not force:
        return "skipped (exists; use --force)"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return "installed"


def list_catalog() -> None:
    print("Skills:")
    for skill in discover_skills():
        desc = skill_description(skill)
        if len(desc) > 90:
            desc = desc[:87] + "..."
        print(f"  - {skill.name}: {desc}")
    print("\nAgents:")
    for agent in discover_agents():
        print(f"  - {agent_stem(agent)}")


def install(
    tools: list[str],
    target: Path,
    is_global: bool,
    skill_names: list[str] | None,
    agent_names: list[str] | None,
    do_skills: bool,
    do_agents: bool,
    force: bool,
) -> None:
    skills = discover_skills()
    agents = discover_agents()

    if skill_names is not None and "all" not in skill_names:
        available = {s.name for s in skills}
        missing = set(skill_names) - available
        if missing:
            raise SystemExit(f"Unknown skill(s): {', '.join(sorted(missing))}")
        skills = [s for s in skills if s.name in skill_names]

    if agent_names is not None and "all" not in agent_names:
        available = {agent_stem(a) for a in agents}
        missing = set(agent_names) - available
        if missing:
            raise SystemExit(f"Unknown agent(s): {', '.join(sorted(missing))}")
        agents = [a for a in agents if agent_stem(a) in agent_names]

    home = home_dir()
    results: list[str] = []

    for tool in tools:
        cfg = TOOL_CONFIG[tool]
        print(f"\n=== {tool} ===")

        if do_skills:
            if is_global:
                skills_root = cfg["global_skills"](home)
            else:
                skills_root = target / cfg["project_skills"]
            for skill in skills:
                dest = skills_root / skill.name
                status = copy_tree(skill, dest, force)
                line = f"  skill {skill.name} -> {dest} [{status}]"
                print(line)
                results.append(line)

        if do_agents:
            if not cfg["supports_agents"]:
                msg = f"  agents: skipped (not supported for {tool})"
                print(msg)
                results.append(msg)
            else:
                if is_global:
                    agents_root = cfg["global_agents"](home)
                else:
                    agents_root = target / cfg["project_agents"]
                mode = cfg["agent_mode"]
                for agent in agents:
                    dest = agents_root / agent_dest_name(agent, mode)
                    status = copy_file(agent, dest, force)
                    line = f"  agent {agent_stem(agent)} -> {dest} [{status}]"
                    print(line)
                    results.append(line)

    print("\nDone.")
    installed = sum(1 for r in results if "installed" in r and "already present" not in r)
    skipped = sum(1 for r in results if "skipped" in r)
    present = sum(1 for r in results if "already present" in r)
    print(f"Summary: {installed} installed, {skipped} skipped, {present} already present.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install agents and skills for Cursor, Claude, Copilot, or Windsurf.",
    )
    parser.add_argument(
        "--tools",
        help="Comma-separated tools: cursor,claude,copilot,windsurf, or all",
    )
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument(
        "--project",
        action="store_true",
        help="Install into the target project (default)",
    )
    scope.add_argument(
        "--global",
        dest="global_install",
        action="store_true",
        help="Install into user home directories",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=None,
        help="Target project root (default: current working directory)",
    )
    parser.add_argument(
        "--skills",
        help="Comma-separated skill names, or all (default: all)",
    )
    parser.add_argument(
        "--agents",
        help="Comma-separated agent names (without .agent.md), or all (default: all)",
    )
    parser.add_argument("--no-skills", action="store_true", help="Skip skills")
    parser.add_argument("--no-agents", action="store_true", help="Skip agents")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompts")
    parser.add_argument("--list", action="store_true", help="List catalog and exit")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        list_catalog()
        return 0

    available_skills = [s.name for s in discover_skills()]
    available_agents = [agent_stem(a) for a in discover_agents()]

    if args.tools:
        tools = parse_csv_list(args.tools, TOOL_IDS)
        assert tools is not None
        if args.tools.strip().lower() == "all":
            tools = list(TOOL_IDS)
    else:
        tools = prompt_multi_select(
            "Select IDE / agent tools to configure:",
            [
                ("cursor", "Cursor"),
                ("claude", "Claude Code"),
                ("copilot", "GitHub Copilot"),
                ("windsurf", "Windsurf"),
            ],
            default_all=True,
        )

    if args.global_install:
        is_global = True
    elif args.project:
        is_global = False
    elif args.yes:
        is_global = False
    else:
        is_global = prompt_scope()

    target = (args.path or Path.cwd()).resolve()
    if not is_global and not target.is_dir():
        raise SystemExit(f"Target path is not a directory: {target}")

    skill_names = parse_csv_list(args.skills, available_skills) if args.skills else None
    agent_names = parse_csv_list(args.agents, available_agents) if args.agents else None

    do_skills = not args.no_skills
    do_agents = not args.no_agents

    print(f"\nCatalog: {CATALOG_ROOT}")
    print(f"Target:  {'global (home)' if is_global else target}")
    print(f"Tools:   {', '.join(tools)}")
    print(
        f"Payload: "
        f"skills={'yes' if do_skills else 'no'}, "
        f"agents={'yes' if do_agents else 'no'}"
    )

    if not args.yes:
        if not prompt_yes_no("Proceed with installation?", default=True):
            print("Aborted.")
            return 1

    install(
        tools=tools,
        target=target,
        is_global=is_global,
        skill_names=skill_names,
        agent_names=agent_names,
        do_skills=do_skills,
        do_agents=do_agents,
        force=args.force,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
