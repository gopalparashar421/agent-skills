# caveman-compress scripts (optional)

**Not required** for the skill.

Primary path: agent apply rules in `../SKILL.md` (read → backup → compress prose → overwrite). No Claude CLI. No `python -m scripts`.

| Script | Role |
|--------|------|
| `validate.py` | Optional post-check: headings / fences / structure still intact |
| `detect.py` | Heuristic: is path a compressible natural-language file? |
| `compress.py` / `cli.py` | **Legacy** Claude-backed pipeline — do not use as default |
| `benchmark.py` | Historical compression measurements |

Example optional check after agent compress:

```bash
python -m scripts.validate path/to/file.md
```

(from this skill directory, or `python skills/caveman-compress/scripts/validate.py …` depending on cwd)
