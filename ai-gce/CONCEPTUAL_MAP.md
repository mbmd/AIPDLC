# AI-GCE Conceptual Map

> **What this file is:** A navigational guide to AI-GCE's internal structure. It answers "where does each governance concern live?" and helps you find the right file without reading all 23 generators.

---

## How to Read This

AI-GCE is an **adaptive governance engine** with 23 generator files, each responsible for deriving one category of compliance rules from a development workspace. This map organizes those generators by *concern domain* — so you can find what you need based on what you're trying to understand or enforce.

**Key principle:** Every generator reads specific steering files from the workspace and produces enforceable rules (MUST/NEVER, binary pass/fail). Nothing is advisory.

---

## Concern → Location Map

### Architecture Enforcement

| Concern | Generator File | Source Steering | Output Rules |
|---------|---------------|-----------------|--------------|
| Architecture patterns & decisions | `generators/architecture-compliance-gen.md` | `architecture-decisions.md`, ADRs | ARCH-* |
| Conditional architecture patterns | `generators/conditional-arch-generator.md` | Extension-specific steering (multi-tenancy, event sourcing, etc.) | Conditional ARCH-* |
| API contract compliance | `generators/api-compliance-generator.md` | `api-standards.md` | API-* |

### Decomposition & Module Boundaries

| Concern | Generator File | Source Steering | Output Rules |
|---------|---------------|-----------------|--------------|
| Module decomposition enforcement | `generators/module-boundary-generator.md` | `module-structure.md` | MOD-01 to MOD-04 |
| Domain layer purity | `generators/module-boundary-generator.md` | `module-structure.md` (layer rules) | MOD-02, DOM-005 |
| Domain language enforcement | `generators/domain-context-generator.md` | `domain-context.md` | DOM-* |

**Key insight:** Decomposition rules are 100% steering-derived. GCE reads `module-structure.md` and enforces that code matches the declared module layout — paths, layers, and allowed dependencies.

### Session & Methodology Discipline

| Concern | Generator File | Source Steering | Output Rules |
|---------|---------------|-----------------|--------------|
| AI-DLC v1 session methodology | `generators/session-governance-generator.md` | `session-governance.md` + built-in baseline | GOV-SESSION-* |
| Spec-before-code gate | `generators/session-governance-generator.md` | Built-in baseline | GOV-SESSION-BASELINE-01 |
| Correction escalation | `generators/session-governance-generator.md` | Built-in + steering | Escalation model (4 levels) |

**Key insight:** Session governance is HYBRID — it has a non-negotiable built-in baseline (4 rules that define AI-DLC v1 methodology) PLUS project-specific enrichment from `session-governance.md`. The baseline fires from Day 0; enriched rules activate at Tier 2.

### Steering Quality & Self-Governance

| Concern | Generator File | Source Steering | Output Rules |
|---------|---------------|-----------------|--------------|
| Steering file quality | `generators/steering-governance-gen.md` | Self-derived (analyzes steering files themselves) | GOV-STEER-* |
| Context budget (≤300 lines) | `generators/steering-governance-gen.md` | Line count analysis | GOV-STEER-001 |
| Five Qualities test | `generators/steering-governance-gen.md` | Language analysis | GOV-STEER-005 |
| Cross-file contradiction detection | `generators/steering-governance-gen.md` | Cross-file comparison | GOV-STEER-009 |

**Key insight:** This is the only SELF-DERIVED category. It doesn't read a specific upstream steering file — it analyzes the steering files *themselves* for quality, structure, and consistency. Also validated post-generation by V7 in `common/validation-rules.md`.

### Team & Role Isolation

| Concern | Generator File | Source Steering | Output Rules |
|---------|---------------|-----------------|--------------|
| Role segregation | `generators/role-isolation-generator.md` | `role-isolation.md` | GOV-ROLE-* |
| Team topology enforcement | `generators/team-topology-generator.md` | `team-topology.md` | GOV-TT-* |

### Sprint, PR & Change Management

| Concern | Generator File | Source Steering | Output Rules |
|---------|---------------|-----------------|--------------|
| Sprint governance | `generators/sprint-governance-generator.md` | `sprint-governance.md` | GOV-SPRINT-* |
| PR process enforcement | `generators/pr-governance-generator.md` | `pr-governance.md` | GOV-PR-* |
| Change management | `generators/change-management-gen.md` | `change-management.md` | CM-* |
| Phase gates (Definition of Done) | `generators/phase-gates-generator.md` | `DEFINITION_OF_DONE.md` | PG-* |

### Security & Data Protection

| Concern | Generator File | Source Steering | Output Rules |
|---------|---------------|-----------------|--------------|
| Security compliance | `generators/security-compliance-gen.md` | `security-standards.md` | SEC-* |
| Data governance | `generators/data-governance-generator.md` | `data-governance.md` | DG-* |
| Sensitive data protection | (hook-level, part of security) | `security-standards.md` | SEC (sensitive-data subset) |

### DevOps & CI/CD

| Concern | Generator File | Source Steering | Output Rules |
|---------|---------------|-----------------|--------------|
| CI/CD gate enforcement | `generators/cicd-gates-generator.md` | `cicd-standards.md` | GOV-CICD-* |
| DevOps deployment standards | `generators/devops-generator.md` | `devops-standards.md` | GOV-DEVOPS-* |
| MCP server governance | `generators/mcp-governance-gen.md` | `.kiro/settings/mcp.json` | GOV-MCP-* |

### Code Quality Standards

| Concern | Generator File | Source Steering | Output Rules |
|---------|---------------|-----------------|--------------|
| Naming conventions | `generators/naming-generator.md` | `naming-conventions.md` | NC-* |
| Error handling | `generators/error-handling-generator.md` | `error-handling.md` | ERR-* |
| Logging standards | `generators/logging-generator.md` | `logging-standards.md` | LOG-* |
| Compliance log governance | `generators/compliance-log-gov-gen.md` | Self-referential (GCE's own log integrity) | GOV-LOG-* |

---

## Cross-Cutting Mechanisms

These mechanisms span ALL generators — they're not a single concern but structural features of the engine:

### Hook Debounce Strategy

| Classification | Event Type | When to Use |
|---------------|-----------|-------------|
| **Tier A — Security-critical** | `fileEdited` | Immediate enforcement. Data leakage, secret exposure, destructive operations. |
| **Tier B — Advisory** | `agentStop` | Batch check after AI finishes. Boundaries, naming, coverage — intermediate states are misleading. |
| **Methodology** | `promptSubmit` | Every prompt. Session discipline. |
| **Gate** | `preToolUse (write)` | Before code is written. Spec-before-code check. |
| **Completion** | `postTaskExecution` | After task marked done. DoD verification. |
| **On-demand** | `userTriggered` | Manual full audit or PR readiness check. |

### Three-Tier Progressive Compliance

| Tier | Coverage | When Active | What's Included |
|------|----------|-------------|-----------------|
| **Tier 1 — Day 0** | 60-70% | Project setup | Naming, basic architecture, session baselines, security essentials |
| **Tier 2 — Sprint 2+** | 80-90% | After team stabilizes | Full session rules, module boundaries, team topology, PR governance |
| **Tier 3 — Pre-Release** | 92%+ | Go-live readiness | CI/CD gates, SOX/GDPR compliance, full change management |

### Phase-Awareness

Rules only fire when the project's current phase makes them relevant. A sprint-governance rule doesn't fire during initial setup. The `.compliance-state.json` file tracks `currentPhase`, and every hook checks it before enforcing.

### Validation Pipeline (Post-Generation)

After GCE generates output, 9 validation checks run (defined in `common/validation-rules.md`):

| Check | Question It Answers |
|-------|-------------------|
| V1: Completeness | Is everything generated that should be? |
| V2: Traceability | Can every rule trace to a steering source? |
| V3: Consistency | Do rules and hooks agree with each other? |
| V4: Conditional | Are conditional rules correctly included/excluded? |
| V5: Hook Integrity | Do hooks use real paths and correct event types? |
| V6: Enforceable | Are rules concrete (not aspirational)? |
| V7: Context Budget | Does output respect the ≤300-line always-inclusion limit? |
| V8: Phase-Awareness | Are rules correctly tagged with applicable phase? |
| V9: Logging | Does every hook end with the compliance logging block? |

---

## Common Questions

### "Where does decomposition get enforced?"

→ `generators/module-boundary-generator.md`. Reads `module-structure.md` from the workspace. Produces MOD-01 through MOD-04. Hooks: `module-boundary-check.json` and `domain-layer-purity.json` (both agentStop, Tier B).

### "Where are session contracts governed?"

→ `generators/session-governance-generator.md`. HYBRID category: 4 built-in baseline rules (always, Tier 1) + project-specific GOV-SESSION-001 through 012 (from `session-governance.md`, Tier 2). Hooks: `session-discipline.json` (promptSubmit), `pre-code-spec-check.json` (preToolUse/write), `post-task-governance.json` (postTaskExecution).

### "Where does steering quality get checked?"

→ `generators/steering-governance-gen.md`. Self-derived (analyzes steering files themselves). Checks line budget, prescriptive language, cross-file contradictions, freshness. Hook: `steering-quality-check.json` (agentStop, Tier B). Also validated post-generation by V7 in `common/validation-rules.md`.

### "What's the difference between built-in baseline and steering-derived rules?"

→ **Built-in baseline** = universal AI-DLC v1 methodology rules that apply to ANY project regardless of steering content. They exist because the methodology demands them. **Steering-derived** = project-specific rules extracted from YOUR workspace's steering files. Steering overrides baseline where they overlap; baseline stands where steering is silent.

### "How do I know which hooks fire immediately vs. batch?"

→ Check the debounce strategy. Security-critical (secrets, tenant isolation, destructive ops) = `fileEdited` (immediate). Advisory (naming, boundaries, coverage) = `agentStop` (batch after AI finishes). See the full classification in `common/validation-rules.md` → V5 → Debounce Strategy Verification table.

### "Why are some governance checks agents instead of hooks?"

→ Per Lesson 49: hooks are reserved for checks that MUST fire automatically (real-time security, code quality on save). Process governance checks — session discipline, sprint health, code review compliance, change management — are **milestone-based** and only the user knows when the milestone occurs. These are agents triggered by shortcut keywords (`SDC__`, `SGV__`, `CRV__`, `SQC__`, `CMG__`, `DOD__`). Benefits: no context waste on "nothing to do" fires, no recursive risk, full user visibility, state isolation. The user manual at `.governance/AGENT-GUIDE.md` documents when to call each, consequences of skipping, and recovery.

### "Where do I find the agent user manual?"

→ `.governance/AGENT-GUIDE.md` (generated by AI-GCE Step 5d). Contains: quick-reference table, process cadence map (every session / sprint / review / release / task completion), consequence severity matrix, escalation model, and recovery procedures. Also: `.governance/AGENT_REGISTRY.md` is the single-source lookup for all active agents.

### "What happens if I never call the process agents?"

→ The compliance audit agent (Layer 3 — safety net) catches drift that process agents (Layer 2) would have prevented at the milestone. But the audit can only DETECT violations after the fact — it can't PREVENT them. Accumulated skips degrade: audit score drops → dashboard flags "process adherence declining" → after 6+ misses, a REMEDIATION entry is created. See `AGENT_GOVERNANCE_CONTRACT.md` §10 for the full debt model.

### "What happens in brownfield mode?"

→ Mode 3 baselines existing violations as technical debt, marks them in a brownfield registry, and enforces rules ONLY against new/changed code from day 1. Existing violations get a remediation timeline but don't block development. Defined across generators — each has brownfield-specific behavior.

### "How does the Project ID flow into compliance logging?"

→ AI-GCE reads the `Project ID` from workspace metadata (embedded by AI-DWG in `workspace-rules.md`). Every compliance log JSONL entry includes a `projectId` field across all 5 event types (rule-check, hook-fire, tier-change, phase-advance, audit-run). This enables cross-project portfolio-level compliance queries when AI-PPM aggregates. (Lesson 39/43 — correlation key threading)

### "Can I use AI-GCE without AI-DWG (standalone)?"

→ Yes. AI-GCE works on **any workspace** with `.kiro/steering/` files — AI-DWG doesn't need to have generated them. You can create steering manually, use an existing project's steering setup, or run with no steering at all. The **built-in baseline** provides universal governance rules (author ≠ approver, no direct-push to main, spec before code, session discipline, etc.) that apply to any project regardless of steering content. Steering files enrich and specialize — their absence doesn't block (Lesson 6, OR-input: graceful degradation from full-enriched enforcement to baseline-only governance). See README.md → "Standalone Usage" section.

### "How do hooks avoid firing on package infrastructure files?"

→ Three-layer segregation strategy (defined in `common/hook-preamble.md` + `templates/package-territories.md`):

1. **Layer 1 — Pattern Scoping:** Hook `patterns` arrays use scoped paths (`src/**/*.ts`) instead of bare wildcards (`**/*.ts`). This structurally excludes `.kiro/`, `.governance/`, `compliance-log/`, etc. — ~90% of interference eliminated.
2. **Layer 2 — Prompt Preamble:** Every file-context hook (fileEdited, fileCreated, agentStop) starts with a "Package Territory Check" that evaluates the file path before running compliance logic. If the file is in an excluded zone → exit silently.
3. **Layer 3 — Territory Registry:** `.governance/PACKAGE_TERRITORIES.md` is the single source of truth for which paths are package infrastructure. Layer 2 references it. Teams can add custom exclusions in the `<!-- custom -->` section.

Validated by V10 in `common/validation-rules.md`. Non-file hooks (promptSubmit, preToolUse, postTaskExecution, userTriggered) do NOT get the preamble — they don't have file context.

---

## File Relationships

```
CONCEPTUAL_MAP.md  ← You are here (navigation)
README.md          ← What this package does (external audience)
PLAN.md            ← Why it was designed this way (decisions)
WHITEPAPER.md      ← Theory and methodology (deep dive)
core-generator.md  ← How it executes (runtime orchestration)
```

---

*Created: June 2026 | Package: AI-GCE v1.0*

---

## AI-DFE Data Interface (`ai-gce-rule-details/data-schema/`)

This package ships a machine-readable data interface consumed by **AI-DFE** (the family data fabric). AI-DFE reads these files to gather this package's output into `{family}-ws/data/gce-data.json`.

| File | Purpose |
|------|---------|
| `gce-data.schema.json` | JSON Schema — the shape AI-DFE produces for this package |
| `SOURCE_MAP.md` | Declares where this package's raw output lives + field extraction rules |
| `SCHEMA_README.md` | Human documentation of the schema, fields, and consumers |

> These files do not change this package's runtime behavior — they are a read-only contract for the data fabric. See AI-DFE for how the data surface is gathered, shaped, and distributed.
