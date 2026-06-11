---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: workspace-rules.md

## Template Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Architecture Vision | date: {generation-date} -->

# Workspace Rules

## Architecture Identity

{vision-statement}

**System:** {system-name}
**Architecture style:** {monolith | modular-monolith | microservices | hybrid}
**Primary technology:** {language + framework}
**Deployment model:** {on-premises | cloud | hybrid}

## Guiding Principles

<!-- begin: AP-sourced -->

| # | Principle | Statement | Implication for Development |
|---|-----------|-----------|---------------------------|
| P1 | {principle-name} | {principle-statement} | {development-implication} |
| P2 | {principle-name} | {principle-statement} | {development-implication} |
| ... | ... | ... | ... |

<!-- end: AP-sourced -->

## Constraints (Non-Negotiable)

<!-- begin: AP-sourced -->

These constraints are ABSOLUTE. They cannot be violated regardless of convenience or preference.

| Constraint | Rule | Source |
|-----------|------|--------|
| {constraint-name} | {MUST NOT / NEVER / DO NOT statement} | {source} |
| ... | ... | ... |

<!-- end: AP-sourced -->

## Quality Priorities

Development decisions MUST prioritize quality attributes in this order:

<!-- begin: AP-sourced -->

1. **{critical-attribute}** — {practical-meaning}
2. **{critical-attribute}** — {practical-meaning}
3. **{high-attribute}** — {practical-meaning}
4. ...

<!-- end: AP-sourced -->

When two quality attributes conflict, the higher-priority attribute wins.

## Golden Rules

<!-- begin: AP-sourced -->

1. {rule-derived-from-principle — prescriptive, actionable}
2. {rule-derived-from-principle}
3. {rule-derived-from-constraint}
4. ...
(8-12 total)

<!-- end: AP-sourced -->

## Scope Awareness

This system includes: {module-list-brief}
This system does NOT include: {out-of-scope-items}

## References

- Architecture Principles (full detail): `.kiro/steering/architecture-principles.md`
- Technology Stack: `.kiro/steering/tech-stack.md`
- Module Structure: `.kiro/steering/module-structure.md`
```

## Filling Instructions

Refer to `mapping/vision-to-workspace-rules.md` for complete transformation rules.
