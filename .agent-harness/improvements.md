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

### [IMPLEMENT] Rich f-string syntax error with dict access

**Found When**: Writing CLI with Rich formatting like `f"[bold {NORD['accent']}]"`
**Severity**: minor
**Description**: Python f-strings with dict access inside Rich style tags cause syntax errors

**Expected**: Should work or have clear error message
**Actual**: `SyntaxError: closing parenthesis '}' does not match opening parenthesis '['`

**Fix Needed**: Use constants instead of dict for colors: `NORD_ACCENT = "#a3be8c"`

---

### [IMPLEMENT] Typer can't use Python reserved words as commands

**Found When**: Creating `list` command with `def list_()` function
**Severity**: minor
**Description**: Typer doesn't automatically map `list_` to `list` command

**Expected**: Automatic mapping or clear error
**Actual**: `No such command 'list'` error

**Fix Needed**: Must use `@app.command(name="list")` explicitly

---

### [TEST] Temporary file storage needs empty file handling

**Found When**: Testing TodoStorage with NamedTemporaryFile
**Severity**: minor
**Description**: Empty temp files cause JSON decode error

**Expected**: Should handle empty files gracefully
**Actual**: `json.decoder.JSONDecodeError: Expecting value: line 1 column 1`

**Fix Needed**: Add empty file check in `_ensure_file()` and `_load()`

---

### [INIT] init-project.sh not called during initialization

**Found When**: User noticed `.claude/CLAUDE.md` was missing after INIT
**Severity**: major
**Description**: initialization skill instructions don't include init-project.sh step

**Expected**: INIT state → initializer skill → init-project.sh → .claude/CLAUDE.md created
**Actual**: INIT state → initializer skill → Manual setup → File missing

**Fix Needed**: Add `scripts/init-project.sh` to initialization/SKILL.md instructions list

**Root Cause**: The script exists and works correctly, but the skill's instructions don't tell agents to run it

---

### [INIT] Hooks installed but never triggered

**Found When**: Implementation completed without any hook enforcement
**Severity**: blocker
**Description**: 12 hooks installed (7 global + 5 project) but 0 fired during actions

**Expected**:
- Mark feature tested → Hook runs pytest → Blocks if fail
- Write to src/ → Hook checks dependencies → Blocks if missing

**Actual**: All actions succeeded without any hook verification

**Fix Needed**: Investigate why Claude Code doesn't trigger hooks - possibly:
1. Hooks need registration in settings.json
2. Hook event names don't match Claude Code expectations
3. Hook permissions incorrect
4. Claude Code version incompatibility

---

### [INIT] Session entry protocol not enforced

**Found When**: Started work without running session-entry.sh
**Severity**: major
**Description**: No mechanism ensuring session-entry.sh runs before other scripts

**Expected**: Hook or skill requirement blocks check-state.sh until session-entry.sh completes
**Actual**: Went straight to check-state.sh, skipped safety checks

**Fix Needed**: Add enforcement hook that blocks state operations until session-entry protocol complete

---

---

## Summary: DESIGN-v2 Compliance Analysis

**Test Session**: CLI Todo App Implementation
**Date**: 2025-12-30
**Overall Compliance**: ~50%

### What Worked ✅

| Area | Status |
|------|--------|
| State Machine | ✅ Followed transitions properly |
| Skills Loading | ✅ Progressive disclosure (on-demand) |
| Documentation Hierarchy | ✅ Created CLAUDE.md, project.json |
| Git Commits | ✅ Used proper feat-id format |
| Testing | ✅ Ran pytest, got 86% coverage |

### What Didn't Work ❌

| Area | Issue |
|------|--------|
| Session Entry Protocol | ❌ Never ran, skipped safety checks |
| Hooks Enforcement | ❌ 0/12 hooks fired during actions |
| Code Verification | ⚠️ Mixed - some tests, mostly judgment |
| Token Efficiency | ❌ No compression, full file reads |
| init-project.sh | ❌ Not called, .claude/CLAUDE.md missing |

### Priority Fixes

1. **Get hooks working** - Critical for enforcement
2. **Enforce session entry** - Safety/validation first
3. **Add init-project.sh to initializer** - Missing step
4. **Fix validate-transition.sh** - Syntax error (line 47)

### Files in .agent-harness/

- `DESIGN-v2.md` - Full specification (37KB)
- `improvements.md` - This file (all issues logged)

---
