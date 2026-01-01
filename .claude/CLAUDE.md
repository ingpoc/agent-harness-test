---
name: project
description: CLAUDE.md for project configuration
---

## Quick Reference

## Project Purpose

This is a **test project** for validating the Agent Harness system. Build a real app while logging issues/improvements found.

**Goal**: Test Agent Design-v2 in production by building a functional CLI todo app.

> **"Break the system to make it robust"** - Find issues, document improvements, validate autonomous behavior.

Full orchestrator instructions are in `~/.claude/prompts/orchestrator.md`

## Agent Harness System

Uses single orchestrator + skills library (NOT multi-agent).

**Your skills are in**: `~/.claude/skills/`

**State machine**:
```
START → INIT → IMPLEMENT → TEST → COMPLETE
```

## What to Build

Built: CLI Todo App with Terminal UI (completed, 9 features, 24 tests passing)

## Common Commands

```bash
# Check current state
~/.claude/skills/orchestrator/scripts/check-state.sh

# Run tests (reads test_command from .claude/config/project.json)
~/.claude/skills/testing/scripts/run-unit-tests.sh

# Health check (reads health_check from config)
~/.claude/skills/implementation/scripts/health-check.sh

# Browser smoke test (reads dev_server_port from config)
~/.claude/skills/browser-testing/scripts/smoke-test.sh

# Log an issue
echo "## [Category] Title" >> .agent-harness/improvements.md
```

## Session Entry

Run: `~/.claude/skills/orchestrator/scripts/session-entry.sh`

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `.claude/` | Agent Harness configuration and progress |
| `.agent-harness/` | Test findings, design spec, and improvements log |
| `src/` | Todo app source code |
| `tests/` | Test files (24 tests, 66% coverage) |

## State → Skill Mapping

| State | Skill |
|-------|-------|
| INIT | initialization/ |
| IMPLEMENT | implementation/ |
| TEST | testing/ |
| COMPLETE | context-graph/ |

## MCP Servers (Token Efficiency & Learning)

This project has two MCP servers configured in `.mcp.json`:

### token-efficient MCP
**Use for**: Large data processing (CSV, logs), code execution in sandbox

| Situation | Tool | Benefit |
|-----------|------|---------|
| File >50 lines | `process_logs` with pattern | 98% token savings |
| CSV files | `process_csv` with filter | Returns summary, not raw data |
| Multiple files | `batch_process_csv` | Batch processing |
| Execute code | `execute_code` | Sandbox execution |

### context-graph MCP
**Use for**: Storing decisions, querying precedents, learning from history

| Situation | Tool | Benefit |
|----------|------|---------|
| Made technical decision | `context_store_trace` | Build institutional memory |
| Facing similar problem | `context_query_traces` | Find past decisions by meaning |
| Session complete | `context_list_categories` | Extract patterns |
| Repeating error | `context_query_traces` | Find how it was fixed |

**Priority Rule**: Think before reading/executing - Can I use MCP servers instead?

## Config Files

- `.claude/config/project.json` - Project settings (auto-detected)
- `.claude/progress/state.json` - Current state
- `.claude/progress/feature-list.json` - Features
- `.mcp.json` - MCP server configuration

## Critical: Track Issues

**Log ALL issues found to**: `.agent-harness/improvements.md`

```markdown
## [Category] Issue Title

**Found When**: [What you were doing]
**Severity**: blocker|major|minor|enhancement
**Description**: What happened

**Expected**:
**Actual**:

**Fix Needed**:
```

**Categories**:
- `INIT` - Setup, feature breakdown, hooks
- `IMPLEMENT` - Coding patterns, skills workflow
- `TEST` - Verification, evidence collection
- `COMPLETE` - Summary, learning loops
- `GENERAL` - Cross-cutting concerns

## Success Criteria

1. ✅ App is working (deployable, tested)
2. ✅ `.agent-harness/improvements.md` has detailed findings
3. ✅ At least 3 issues documented (even if minor)
4. ✅ Each issue has: severity, description, fix suggestion

> **Note**: `.agent-harness/` contains only 2 files: `DESIGN-v2.md` (spec) and `improvements.md` (all issues logged).

**Remember**: The app you're building is secondary. The **primary goal** is testing the Agent Harness system itself. Log everything that doesn't work smoothly.
