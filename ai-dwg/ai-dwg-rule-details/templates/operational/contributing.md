# Template: CONTRIBUTING.md

```markdown
<!-- AI-DWG generated | source: Infrastructure + Team Context | date: {generation-date} -->

# Contributing

## Workflow

1. Pick task from backlog
2. Create branch: `{type}/{ticket}-{description}`
3. Implement with tests
4. Open PR using template
5. Address review feedback
6. Merge after approval + CI pass

## Commit Messages

Format: `{type}({scope}): {subject}`

Types: feat, fix, refactor, docs, test, chore, perf, ci
Scope: module name (see module-structure.md)

Full convention: `.kiro/steering/git-workflow.md`

## Pull Requests

- Use PR template (auto-loaded)
- One concern per PR
- Max: {max-lines} lines
- Required: {n} approvals + CODEOWNER
- CI must pass

## Code Standards

Follow `.kiro/steering/` rules:
- Module boundaries (module-structure.md)
- Domain language (domain-context.md)
- Error patterns (error-handling.md)
- Logging (observability-logging.md)
- Testing (testing-strategy.md)

## Review Checklist

When reviewing:
- [ ] Module boundaries respected
- [ ] Domain terminology correct
- [ ] Tests for new behavior
- [ ] Error handling correct
- [ ] No sensitive data in logs
- [ ] Tenant scoping (if applicable)
- [ ] API standards followed (if API changes)
```

## Filling: Refer to `mapping/governance-derivation.md` (Target 2).
