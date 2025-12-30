# CLAUDE.md

This is a **test project** for validating the Agent Harness system. Build a real app while logging issues/improvements found.

## Project Purpose

Test Agent Design-v2 in production. Build a functional app to uncover edge cases, gaps, and improvements needed.

## Goal

> **"Break the system to make it robust"** - Find issues, document improvements, validate autonomous behavior.

## What to Build

Choose any simple app (examples):
- URL shortener service
- Todo API with auth
- Markdown preview tool
- Weather dashboard
- File conversion service

**Requirements**: Must have frontend + backend, tests, and be deployable.

## Agent Harness System

Uses single orchestrator + skills library (NOT multi-agent).

**Your skills are in**: `~/.claude/skills/` (installed via `install-skills.sh`)

**State machine**:
```
START → INIT → IMPLEMENT → TEST → COMPLETE
```

## Critical: Track Issues

**Log ALL issues found to**: `.agent-harness/improvements.md`

```markdown
# Agent Harness Issues Found

## [Category] Issue Title

**Found When**: [What you were doing]
**Severity**: blocker|major|minor|enhancement
**Description**: What happened

**Expected**:
**Actual**:

**Fix Needed**:

---

## Next Issue...
```

**Categories**:
- `INIT` - Setup, feature breakdown, hooks
- `IMPLEMENT` - Coding patterns, skills workflow
- `TEST` - Verification, evidence collection
- `COMPLETE` - Summary, learning loops
- `GENERAL` - Cross-cutting concerns

## What to Test

| Area | What to Validate |
|------|-----------------|
| **INIT state** | Feature breakdown quality, hook setup |
| **IMPLEMENT state** | Skill loading, code quality, progress tracking |
| **TEST state** | Evidence collection, verification scripts |
| **Hooks** | Enforcement actually blocks, error messages clear |
| **Context compression** | Works at 80% threshold |
| **Session resumption** | Can continue from summary |

## Success Criteria

1. ✅ App is working (deployable, tested)
2. ✅ `.agent-harness/improvements.md` has detailed findings
3. ✅ At least 3 issues documented (even if minor)
4. ✅ Each issue has: severity, description, fix suggestion

## Quick Reference

```bash
# Check current state
~/.claude/skills/orchestrator/scripts/check-state.sh

# Run tests
~/.claude/skills/testing/scripts/run-unit-tests.sh

# Health check
~/.claude/skills/implementation/scripts/health-check.sh

# Log an issue
echo "## [Category] Title" >> .agent-harness/improvements.md
```

## Config Files

- `.claude/config/project.json` - Project settings (auto-detected)
- `.claude/progress/state.json` - Current state
- `.claude/progress/feature-list.json` - Features

---

**Remember**: The app you're building is secondary. The **primary goal** is testing the Agent Harness system itself. Log everything that doesn't work smoothly.
