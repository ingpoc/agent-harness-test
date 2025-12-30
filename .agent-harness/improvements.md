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

**Fix Applied**: (2025-12-30)
- Added `--non-interactive` / `-n` flag to skip all prompts
- Added `--yes` / `-y` flag to auto-confirm prompts
- Added `--config` / `-c` <path> flag to use existing config
- Added `CLAUDE_NON_INTERACTIVE` environment variable support
- Auto-detects existing config and skips prompts in non-interactive mode

**Usage**:
```bash
# Interactive
setup-project-hooks.sh

# Non-interactive (agent mode)
setup-project-hooks.sh --non-interactive
CLAUDE_NON_INTERACTIVE=1 setup-project-hooks.sh

# Use existing config
setup-project-hooks.sh --config /path/to/config.json
```

**Files Changed**:
- `~/.claude/skills/project-hook-setup/scripts/setup-project-hooks.sh`
- `~/.claude/skills/project-hook-setup/SKILL.md`

---

### [INIT] feature-commit.sh assumes git repo exists

**Found When**: Running `feature-commit.sh F-001` after implementing F-001
**Severity**: minor
**Description**: Script fails with "Not a git repository" on new projects

**Expected**: Script should auto-initialize git or provide clear error with fix
**Actual**: Script exits with error 1, agent must manually run `git init`

**Fix Applied**: (2025-12-30)
- Added git repo check before git operations
- Auto-initializes with `git init` if `.git` directory doesn't exist
- Provides clear message when auto-initializing

**Files Changed**:
- `~/.claude/hooks/feature-commit.sh`

---

### [INIT] terminal-ui-design skill not auto-discovered

**Found When**: Creating skill with `init_skill.py`, then trying to load via `Skill()` tool
**Severity**: minor
**Description**: Skill created at `~/.claude/skills/` but `Skill()` tool couldn't find it

**Expected**: Created skills should be immediately loadable
**Actual**: Had to apply design principles manually instead of via skill

**Fix Needed**: Skills may need registration step or index rebuild after creation

**Resolution**: (2025-12-30) - Not actually an issue. Skill was successfully executed in a later session. This may have been a temporary discovery issue that resolved itself.

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

**Fix Applied**: (2025-12-30)
- Added `init-project.sh` to initialization skill instructions as step 2
- Updated Scripts table to include init-project.sh
- Updated Exit Criteria to check for `.claude/CLAUDE.md`
- Validated skill with skill-creator's quick_validate.py (passed)

**Files Changed**:
- `~/.claude/skills/initialization/SKILL.md`

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

**Fix Applied**: (2025-12-30)
- **Root Cause**: `"hooks": {}` was empty in `~/.claude/settings.json`
- **Solution**: Added all 12 hooks to settings.json with correct format
- **Format**:
```json
"hooks": {
  "PreToolUse": [
    { "matcher": "Write", "hooks": [...] },
    { "matcher": "Edit", "hooks": [...] }
  ],
  "SessionStart": [{ "hooks": [...] }],
  "SessionEnd": [{ "hooks": [...] }]
}
```
- **Verification**: Hook script works correctly when tested directly (blocks invalid state transitions)
- **Note**: Hooks load on new Claude Code session; requires restart to take effect

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
**Issues Found**: 8 (removed 2 non-library issues)
**Issues Fixed**: 6 of 8 (75%)

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
| Hooks Enforcement | ✅ **FIXED** - Firing after settings.json + bug fix |
| init-project.sh | ✅ **FIXED** - Added to initializer skill |
| feature-commit.sh | ✅ **FIXED** - Auto git init |
| Interactive Setup Script | ✅ **FIXED** - Non-interactive flags added |
| Code Verification | ⚠️ Mixed - some tests, mostly judgment |
| Token Efficiency | ❌ No compression, full file reads |

### Priority Fixes

1. ~~**Get hooks working**~~ ✅ **FIXED** (2025-12-30) - Added to settings.json + Edit support
2. ~~**Add init-project.sh to initializer**~~ ✅ **FIXED** (2025-12-30) - Updated SKILL.md
3. ~~**Fix feature-commit.sh git assumption**~~ ✅ **FIXED** (2025-12-30) - Auto git init
4. ~~**Fix interactive setup script**~~ ✅ **FIXED** (2025-12-30) - Non-interactive flags
5. **Enforce session entry** - Safety/validation first

---

## Fix Log (2025-12-30)

### Hooks System Fixed

**Issue**: `[INIT] Hooks installed but never triggered` (blocker)

**Root Cause**: Hooks existed in `~/.claude/hooks/` and `.claude/hooks/` but `"hooks": {}` was empty in `~/.claude/settings.json`

**Solution**:
1. Added all 12 hooks to settings.json with correct JSON schema format
2. PreToolUse hooks use `matcher` to specify which tools (Write/Edit)
3. SessionStart/SessionEnd hooks don't use matcher
4. Each hook has `hooks` array with command objects

**Verification**:
- Direct test: `echo '{"tool_name":"Write",...}' | python3 ~/.claude/hooks/verify-state-transition.py`
- Result: Correctly blocked invalid state transition `COMPLETE → TEST`
- ✅ **Session restart confirmed**: Hooks now fire automatically on Write/Edit
- ✅ **State transition blocked**: `COMPLETE → TEST` blocked with error message
- ✅ **Git hygiene enforced**: Tested=true blocked with uncommitted changes

**Bug Fix Applied** (2025-12-30):
- Hooks only checked `content` (Write tool) but not `new_string` (Edit tool)
- Fixed 6 installed hooks: `require-commit-before-tested.py`, `require-outcome-update.py`, `link-feature-to-trace.py`, and 3 project hooks
- Fixed 7 skill templates in global-hook-setup and project-hook-setup skills
- Changed: `content = tool_input.get("content", "")` → `content = tool_input.get("content", "") or tool_input.get("new_string", "")`
- Both skills validated with skill-creator's quick_validate.py

---

### [INIT] Skill templates had same Edit tool bug

**Found When**: Analyzing hook setup skills after fixing installed hooks
**Severity**: major
**Description**: The skill templates (used to install hooks) had the same bug as installed hooks - only checking `content` not `new_string`

**Expected**: Skill templates should support both Write and Edit tools
**Actual**: Templates in both `global-hook-setup` and `project-hook-setup` only checked `content`

**Fix Applied**: (2025-12-30)
- Updated 7 Python hook templates across both skills
- Added Edit tool documentation to both SKILL.md files
- Validated both skills with skill-creator's validation scripts (passed)

**Files Fixed**:
- `~/.claude/skills/global-hook-setup/templates/verify-state-transition.py`
- `~/.claude/skills/global-hook-setup/templates/require-commit-before-tested.py`
- `~/.claude/skills/global-hook-setup/templates/require-outcome-update.py`
- `~/.claude/skills/global-hook-setup/templates/link-feature-to-trace.py`
- `~/.claude/skills/project-hook-setup/templates/verify-tests.py`
- `~/.claude/skills/project-hook-setup/templates/verify-files-exist.py`
- `~/.claude/skills/project-hook-setup/templates/verify-health.py`
- Both `SKILL.md` files (added Edit tool note)

**Impact**: New hook installations will have the fix from the start

### Files in .agent-harness/

- `DESIGN-v2.md` - Full specification (37KB)
- `improvements.md` - This file (all issues logged)

---
