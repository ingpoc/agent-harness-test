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

### [INIT] feature-commit.sh assumes git repo exists

**Found When**: Running `feature-commit.sh F-001` after implementing F-001
**Severity**: minor
**Description**: Script fails with "Not a git repository" on new projects

**Expected**: Script should auto-initialize git or provide clear error with fix
**Actual**: Script exits with error 1, agent must manually run `git init`

**Fix Needed**: Check for `.git` and run `git init` if missing, or include in init state setup

---

### [INIT] terminal-ui-design skill not auto-discovered

**Found When**: Creating skill with `init_skill.py`, then trying to load via `Skill()` tool
**Severity**: minor
**Description**: Skill created at `~/.claude/skills/` but `Skill()` tool couldn't find it

**Expected**: Created skills should be immediately loadable
**Actual**: Had to apply design principles manually instead of via skill

**Fix Needed**: Skills may need registration step or index rebuild after creation

---
