# Agent Behavioral Guidelines

## Core Principles

1. **Plan First, Execute Second**
   - Always create a detailed development plan before starting any implementation
   - Break down tasks into manageable checkpoints
   - Review the plan with user before proceeding
   - Mark progress as checkpoints are completed

2. **Test-Driven Module Development**
   - Develop in module units with incremental testing
   - Each module must have corresponding test coverage
   - Run tests after completing each module
   - Fix all test failures before moving to next module

3. **Complete Before Declare Done**
   - Development is COMPLETE only when ALL feature tests pass
   - No feature can be marked complete without test verification
   - Run full test suite before final delivery
   - Document any known issues or limitations

4. **Atomic Commits per Module**
   - Each completed module gets its own commit with proper message
   - Commit message style: `<type>: <description>` (feat, fix, test, docs, chore, refactor)
   - Push commits after each module completion
   - Ensure commit history is clear and traceable

## Development Workflow

```
Receive Request
    ↓
Create Plan (todo list with detailed steps)
    ↓
User Approval → (if major changes)
    ↓
For Each Module:
    1. Mark todo as in_progress
    2. Implement module
    3. Write/integrate tests
    4. Run tests (pytest -v)
    5. Fix any failures
    6. Mark todo as completed
    7. Create commit
    8. Push to remote
    ↓
All Tests Pass (pytest -v)
    ↓
Development Complete
```

## Code Quality Standards

- **Type Safety**: No `as any`, `@ts-ignore`, or type suppression
- **Error Handling**: Never leave empty catch blocks
- **LSP Diagnostics**: Verify clean diagnostics on all changed files
- **Build Verification**: Ensure build passes before marking complete
- **Test Coverage**: Every feature must have test coverage

## Git Commit Convention

```
feat: add news collection for company tickers
test: add unit tests for finnhub collector
fix: resolve duplicate article insertion bug
docs: update README with API documentation
chore: add app/__init__.py for package initialization
refactor: consolidate database connection logic
```

## Required Steps for Any Task

### Before Implementation
1. Understand requirements and scope
2. Create detailed todo list
3. Identify modules and dependencies
4. Review existing code patterns

### During Implementation
1. One module at a time (mark `in_progress`)
2. Follow existing codebase patterns
3. Write tests alongside implementation
4. Run `lsp_diagnostics` on changed files

### After Implementation
1. All todos marked `completed`
2. Full test suite passes (`pytest -v`)
3. Build succeeds
4. No LSP errors/warnings on changed files
5. Commit and push atomic changes

## Verification Checklist

Before declaring any task complete:

- [ ] All planned items in todo list are completed
- [ ] LSP diagnostics clean on all changed files
- [ ] Test suite passes (`pytest -v`)
- [ ] Build command succeeds (if applicable)
- [ ] Commit message follows convention
- [ ] Changes pushed to remote
- [ ] User's original request fully addressed

## Failure Recovery Protocol

1. **Stop** immediately after 3 consecutive failures
2. **Revert** to last known working state
3. **Document** what was attempted and failed
4. **Consult** senior agent or user before proceeding
5. Never leave code in broken state

---

*This document serves as the behavioral contract for all AI agents working on this project.*
