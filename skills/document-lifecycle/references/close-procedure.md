# Close Procedure Reference

Step-by-step: close doc when it reaches terminal status.

---

## Prerequisites

- Doc reached terminal status:
  - `Committed` - Changes committed to git
  - `Released` - Successfully pushed/published
  - `Abandoned` - Explicitly dropped
  - `Deferred` - Postponed indefinitely
  - `Superseded` - Replaced by newer document
  - `Resolved` - All findings addressed (critiques)

---

## Procedure

### Step 1: Update Status Field

In doc YAML frontmatter, update Status:

```yaml
---
ID: 080
Origin: 080
UUID: a3f7c2b1
Status: Committed    # ← Updated to terminal status
---
```

### Step 2: Add Changelog Entry

Add closure entry to doc changelog table:

```markdown
| YYYY-MM-DD | [Skill or user] | Document closed | Status: Committed |
```

### Step 3: Create Closed Folder (If Needed)

```bash
mkdir -p agent-output/<domain>/closed/
```

Replace `<domain>` with appropriate folder:
- `planning`, `implementation`, `qa`, `uat`, `critiques`
- `analysis`, `retrospectives`, `process-improvement`
- `deployment`, `security`, `architecture`

### Step 4: Move the File

```bash
mv agent-output/<domain>/NNN-name.md agent-output/<domain>/closed/
```

### Step 5: Log the Action

Report in response:

> Closed document `080-feature-name.md` (Status: Committed) → moved to `agent-output/planning/closed/`

---

## Bulk closure (after user commit)

When the user commits a plan's changes, close all related docs for that chain ID:

```bash
# For each document type in the chain
for domain in planning implementation qa critiques; do
  mkdir -p agent-output/$domain/closed/
  # Update Status to "Committed" in each doc, then move
  mv agent-output/$domain/080-*.md agent-output/$domain/closed/ 2>/dev/null || true
done
```

Report:
> Closed documents for Plan 080: planning, implementation, qa, critiques → moved to respective `closed/` folders.

---

## Cross-Reference Updates

If other active docs reference now-closed doc, update path:

**Before:**
```markdown
See [plan](../planning/080-feature.md)
```

**After:**
```markdown
See [plan](../planning/closed/080-feature.md)
```

Note: Optional for docs closed together (all land in `closed/`).
