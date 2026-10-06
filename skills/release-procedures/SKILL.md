---
name: release-procedures
description: Version management, release verification, and deployment procedures for software releases. Includes semver guidance, version consistency checks, and platform-specific constraints.
license: MIT
metadata:
  author: groupzer0
  version: "1.0"
---

# Release Procedures

Version + release guidance for persona skills. Use when:
- `implementer` updates version files during plan milestones
- `planner` / `plan-and-critique` specify version bumps
- User prepares a release after manual review/commit
- `roadmap` tracks release→plan mappings

## Release workflow (user-driven)

```
STAGE 1: Per-plan
  1. QA Complete (qa skill) and/or code-review-and-quality
  2. User manual review
  3. User commits locally (optionally no push yet)
  4. document-lifecycle → Status Committed + close chain docs
  5. roadmap: update Active Release Tracker

STAGE 2: Per-release (once plans for version are committed)
  1. User approves release
  2. Git tag, push, publish
  3. document-lifecycle → Status Released on included plans
  4. roadmap: mark release done; bump working release
```

---

## Semantic Versioning (SemVer)

### Version Format: MAJOR.MINOR.PATCH

| Bump | When | Examples |
|------|------|----------|
| **MAJOR** | Breaking changes | API signature change, removed feature |
| **MINOR** | New features (backward compatible) | New command, added option |
| **PATCH** | Bug fixes (backward compatible) | Fixed crash, corrected behavior |

### Pre-Release Versions

```
1.2.3-alpha.1    # Early development
1.2.3-beta.1     # Feature complete, testing
1.2.3-rc.1       # Release candidate
```

### When to Bump

| Change Type | Version | Rationale |
|-------------|---------|-----------|
| Fix typo in docs | PATCH | No code change |
| Fix bug | PATCH | Backward compatible |
| Add new feature | MINOR | New capability |
| Deprecate feature | MINOR | Still works |
| Remove deprecated | MAJOR | Breaking |
| Change API contract | MAJOR | Breaking |

---

## Version Consistency Checklist

All version refs must match before release:

| File | Field | Example |
|------|-------|---------|
| `package.json` | `version` | `"version": "1.2.3"` |
| `CHANGELOG.md` | Latest heading | `## [1.2.3] - 2024-12-19` |
| `README.md` | Badge/install (if versioned) | May be "latest" |
| Platform config | Varies | See platform-specific |

### Verification Command

```bash
# Extract and compare versions
PACKAGE_VERSION=$(jq -r .version package.json)
CHANGELOG_VERSION=$(grep -oP '## \[\K[0-9]+\.[0-9]+\.[0-9]+' CHANGELOG.md | head -1)

if [ "$PACKAGE_VERSION" != "$CHANGELOG_VERSION" ]; then
  echo "VERSION MISMATCH: package.json=$PACKAGE_VERSION, CHANGELOG=$CHANGELOG_VERSION"
  exit 1
fi
```

---

## Platform-Specific Constraints

### VS Code Extensions

| Constraint | Requirement |
|------------|-------------|
| Version format | 3-part semver only (X.Y.Z) |
| Pre-release | Use odd minor version (e.g., 1.1.0) |
| Engine | Specify minimum VS Code version |

```json
{
  "version": "1.2.3",
  "engines": { "vscode": "^1.80.0" }
}
```

### npm Packages

| Constraint | Requirement |
|------------|-------------|
| Version | Standard semver |
| Pre-release | `-alpha.1`, `-beta.1` allowed |
| Deprecation | Use `npm deprecate` |

### Python Packages (PyPI)

| Constraint | Requirement |
|------------|-------------|
| Version | PEP 440 compliant |
| Pre-release | `a1`, `b1`, `rc1` suffixes |
| Location | `setup.py`, `pyproject.toml`, or `__version__` |

---

## CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.2.3] - 2024-12-19

### Added
- New feature description

### Changed
- Modified behavior description

### Fixed
- Bug fix description

### Deprecated
- Feature to be removed

### Removed
- Removed feature

### Security
- Security fix description
```

### Categories Order

1. Added (new features)
2. Changed (changes to existing)
3. Deprecated (soon to be removed)
4. Removed (now removed)
5. Fixed (bug fixes)
6. Security (vulnerability fixes)

---

## Pre-Release Verification

### Mandatory Checks

| Check | Command/Action | Fail Response |
|-------|----------------|---------------|
| User review | Explicit user ack to ship | STOP |
| QA Status | Read `agent-output/qa/` when present | STOP if `QA Failed` |
| Code review | `code-review-and-quality` when used | STOP if REJECTED |
| Version Match | Compare all version files | STOP and fix |
| Tests Pass | Run test suite | STOP and fix |
| Clean Workspace | `git status` | Commit or stash |
| No Debug | Check for debug flags | Remove before release |

### Pre-Commit Cleanup

```bash
# Ensure no debug artifacts
grep -r "console.log" src/ --include="*.ts" && exit 1
grep -r "debugger" src/ --include="*.ts" && exit 1
grep -r "TODO: remove" src/ && exit 1
```

---

## Release Execution

### Git Tagging

```bash
# Create annotated tag
git tag -a v1.2.3 -m "Release v1.2.3"

# Push tag
git push origin v1.2.3
```

### Publication Commands

| Platform | Command |
|----------|---------|
| VS Code | `vsce publish` |
| npm | `npm publish` |
| PyPI | `twine upload dist/*` |
| GitHub | `gh release create v1.2.3` |

### Post-Publication Verification

| Check | Method |
|-------|--------|
| Version visible | Check marketplace/registry |
| Installable | Fresh install test |
| Changelog visible | Check release notes |
| No errors | Check for publish warnings |

---

## Skill responsibilities

### User (manual review / commit / release)
- Review + commit per plan; push/tag/publish only with explicit release intent
- Trigger `document-lifecycle` close (`Committed` / `Released`)
- Never push a release without conscious approval

### `implementer`
- Update version files + CHANGELOG during plan milestones
- Follow plan's specified version bump

### `planner` / `plan-and-critique`
- Specify target release version in plan header
- Multiple plans may share same target release
- Coordinate with `roadmap` for assignments
- Include version update in final milestone

### `roadmap`
- Maintain Active Release Tracker
- Track current working release + plan→release mappings
- Notify when all plans for a release are committed

---

## Rollback Procedure

If release fails:

1. **Unpublish** (if platform allows)
   - npm: `npm unpublish package@version` (within 72h)
   - VS Code: Unpublish via dashboard

2. **Delete tag** (if needed)
   ```bash
   git tag -d v1.2.3
   git push origin :refs/tags/v1.2.3
   ```

3. **Document** in deployment log
4. **Notify** stakeholders of rollback

See [references/release-templates.md](references/release-templates.md) for deployment document templates.
