# Agent Harness Issues Found

_This file logs all issues, gaps, and improvements discovered while testing the Agent Harness system._

---

## Template for New Issues

```markdown
## [Category] Issue Title

**Found When**: [What you were doing]
**Severity**: blocker|major|minor|enhancement
**Description**: What happened

**Expected**:
**Actual**:

**Fix Needed**:
```

---

## Issues Found

### [INIT] Interactive setup-script requires user input

**Found When**: Running `setup-project-hooks.sh` during initialization
**Severity**: major
**Description**: The setup script prompts for interactive input, blocking autonomous agent execution

**Expected**: Script should accept config via CLI flags or environment variables
**Actual**: Script hangs waiting for user input, requires manual intervention

**Fix Needed**: Add `--config` flag or auto-detect from existing `.claude/config/project.json`

---
