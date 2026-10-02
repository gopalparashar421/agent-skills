# Security

## Primary path (current skill)

`caveman-compress` instructs the agent to compress one user-named natural-language file in-process:

- Read path user gave
- Backup to `FILE.original.md` if missing
- Rewrite prose only; preserve code / inline / URLs / paths / structure
- Never touch `*.original.md` or non-prose types

**Does not:**

- Call Claude CLI or Anthropic API
- Spawn subprocesses as part of the skill flow
- Reach network
- Execute file content as code
- Read/write outside the user-specified path (+ sibling `.original.md` backup)

## Legacy scripts/ (optional)

Folder `scripts/` holds an older Claude-backed CLI and local validators. Skill.md does **not** require them.

If you run legacy scripts yourself:

1. **subprocess**: older compress path may call `claude` CLI when `ANTHROPIC_API_KEY` unset — fixed argv list, content via stdin, no `shell=True`
2. **File I/O**: only the filepath you pass (+ `.original.md` backup)
3. **Size guard**: files >500KB rejected before any API use

Static analyzers (e.g. Snyk) may flag subprocess + file I/O in `scripts/` as high risk. For default agent-applied compression, those code paths stay unused.

## Reporting a vulnerability

Open a GitHub issue with label `security`.
