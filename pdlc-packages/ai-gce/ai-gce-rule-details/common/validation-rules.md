<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Validation Rules

## Purpose

This document defines the cross-check rules applied AFTER AI-GCE generates its compliance output (Step 11 of Full Generation, and after re-derivation). Every generated compliance layer must pass these validations before being presented to the user.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Apply systematic verification: every validation category (V1–V9) is a control objective — skip none
- Think adversarially: what could slip through? What inconsistency would break enforcement silently?
- Distinguish BLOCKING from WARNING — only block when integrity is at genuine risk
- Treat validation as a quality gate, not a formality — failures require remediation before delivery
- Cross-check artifacts against each other (hooks vs. rules vs. filesystem vs. state file)

### Anti-Patterns for This Activity
- Do NOT approve output with BLOCKING failures unresolved (no exceptions)
- Do NOT validate in isolation — consistency checks require comparing multiple artifacts together
- Do NOT accept aspirational language ("should", "consider") as enforceable rules

### Quality Check
A good output from this activity sounds like:
- "V1: PASS (5/5 Tier-1 hooks installed; tier-gated absent at Tier 1 = PASS, not a gap; 12/12 rules). V5: FAIL — naming-check.json references `src/modules/` but filesystem shows `src/Modules/` (case mismatch). Remediation: update pattern to match actual path." *(♻️ the count here counts **installed** hooks by active tier — matching the rewritten V1 completeness table below; it previously read `13/13 hooks`, the pre-item-2 template-count framing that made V1 block a correctly-generated workspace.)*
- "V6: 2 rules use weak language ('should consider'). Rewriting to MUST/NEVER form before marking complete."

---

## Pre-Gate Structural Lint

Before delivering generated Markdown artifacts (steering files, docs) to the user, run this mechanical 6-point check on each `.md` file and silently fix the auto-fixable issues. These are formatting/structure checks — they run alongside the validation categories below.

1. **Monotonic headings** — sections stay in order (no §5.6 after §7). *(flag)*
2. **Single footer** — exactly one closing footer; remove duplicates. *(auto-fix)*
3. **Status consistency** — status strings agree with the current state. *(auto-fix)*
4. **List blank-line** — every list has a blank line before its first item. *(auto-fix)*
5. **xychart axis range** — the y-axis spans the actual data values. *(auto-fix)*
6. **Heading-level sanity** — no level jumps (H2 → H4) and only one H1. *(flag)*

Record a one-line result — "Pre-gate lint: {N} passed, {M} auto-fixed, {K} flagged." — and flag the non-auto-fixable issues (checks 1, 6) with the artifact.

---

## Validation Categories

```
┌──────────────────────────────────────────────────────────────────┐
│  AI-GCE VALIDATION PIPELINE                                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  V1: COMPLETENESS    — Is everything generated that should be?     │
│  V2: TRACEABILITY    — Can every rule trace to a steering source   │
│                        OR built-in baseline?                        │
│  V3: CONSISTENCY     — Do rules + hooks agree with each other?     │
│  V4: CONDITIONAL     — Are conditional rules correctly included/   │
│                        excluded based on steering presence?         │
│  V5: HOOK INTEGRITY  — Do hooks use real paths, correct event      │
│                        types, and follow debounce strategy?         │
│  V6: ENFORCEABLE     — Are rules concrete (not aspirational)?      │
│  V7: CONTEXT BUDGET  — Does AI-GCE output respect the ≤300-line   │
│                        always-inclusion steering budget?            │
│  V8: PHASE-AWARENESS — Are rules correctly tagged with their       │
│                        applicable phase?                            │
│  V9: LOGGING         — Does every hook prompt end with the         │
│                        compliance logging block?                    │
│                                                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## V1: Completeness Validation

**Question:** "Is everything generated that should be?"

### Always-Generated Artifacts

Every AI-GCE run (Mode 1) MUST produce these. Missing = validation failure.

| Category | Artifacts | Check |
|----------|-----------|-------|
| Hooks (installed core set — Tier 1) | pre-code-spec-check, api-contract-check, security-gate-check, migration-safety, sensitive-data-check | Each .json file exists in `.governance/hooks/` |
| Hooks (installed — Tier 2, when activated) | post-task-governance, segregation-check, session-end-compliance | Each .json file exists in `.governance/hooks/` **when the tier is active** — absent at Tier 1 is a PASS, not a gap |
| Hooks (installed — Tier 3, when activated) | change-readiness-gate, exception-expiry-check | As above, at Tier 3 |
| Hooks (reference-only — MUST NOT be required) | module-boundary-check, domain-layer-purity, coverage-check, naming-check | Generated as reference documentation of rule logic. Their checks run inside `session-end-compliance.json`. ⚠️ **NEVER assert these are installed** |
| Hooks (ships disabled) | package-activation-guard | Exists with `"enabled": false`. Present-but-disabled is the PASS state |
| Hooks (retired to agents — MUST NOT be required) | ~~session-discipline~~, ~~pre-pr-checklist~~, ~~periodic-audit~~, ~~steering-quality-check~~ | ❌ **Not generated as hooks.** Verify the *agent* instead: `session-discipline-agent.md` (`SDC__`), `pre-pr-checklist-agent.md` (`PRC__`), `compliance-audit-agent.md` (`CAA__`), `steering-quality-agent.md` (`SQC__`) |
| Hooks (removed) | ~~documentation-reminder~~ | ❌ **Not generated.** No generator produces a rule family for it; its intent is covered by the session-end sweep |
| Hook enforcement guide | ENFORCEMENT-GUIDE.md | File exists in `.governance/hooks/` |
| Rules (always) | architecture-compliance, api-first-compliance, security-compliance, data-governance, module-boundaries, naming-conventions, error-handling-compliance, logging-compliance, sensitive-data-protection, domain-context-enforcement, phase-gates, session-governance | Each .md file exists in `.governance/rules/` |
| Rules (tier-gated) | governance-checklist, role-isolation, team-topology, sprint-governance, pr-governance, cicd-gates, devops-deployment, steering-governance, compliance-log-governance | Generated but activation controlled by tier |
| Agents (always) | compliance-audit-agent.md (`CAA__`), project-init-agent.md, pre-pr-checklist-agent.md (`PRC__`), session-discipline-agent.md (`SDC__`) | Each exists in `.governance/agents/` |
| Agents (Tier 2+) | sprint-governance-agent.md (`SGV__`), code-review-agent.md (`CRV__`), steering-quality-agent.md (`SQC__`), dod-gate-agent.md (`DOD__`) | Each exists when the tier is active |
| Agents (Tier 3) | change-management-agent.md (`CMG__`) | Exists when Tier 3 is active |
| Agents (drift — conditional) | drift-detect-agent.md (`DFT__`) | Exists when a DWG baseline is present |

| Compliance log | compliance-log-schema.md, exception-workflow.md, remediation-workflow.md | All exist in `.governance/compliance-log/` |
| COMPLIANCE_README | COMPLIANCE_README.md | Exists in `.governance/` |
| State file | .compliance-state.json | Exists at workspace root |
| Dashboard template | management_framework/dashboards/compliance-dashboard.md | Exists (skeleton — audit agent populates) |

> ### ⚠️ Why this table was rewritten — it blocked correct workspaces and ignored missing agents
>
> **The hook row over-required.** It named thirteen `.json` files and asked only *"does each exist?"* Three had been retired to agents and four are generated as reference documentation that is deliberately **not installed**, so a correctly-generated workspace held at most **6 of 13**. V1 reported `6/13 ❌`, V1 failures are classed **BLOCKING**, and the prescribed response is *"generate the missing artifact"* — so the check told the engine to recreate seven files the package had deliberately retired. **A validation rule that fails on correct output is worse than no rule: it manufactures work and trains the operator to override it.**
>
> **The agent row under-required, which is the more dangerous direction.** It listed **two** agents while the gate-out contract guarantees **nine** to downstream consumers. Seven guaranteed artifacts had no completeness check at all — a missing hook was loudly over-reported while a missing agent was silently unreported.
>
> **The fix is to make the expected set tier-relative and mechanism-aware.** *Installed*, *reference-only*, *ships-disabled*, *retired-to-agent* and *removed* are five different states, and only the first is a file that must be present and active. Collapsing them into "does the file exist" is what produced both errors.

### Completeness Check Format

```
V1: COMPLETENESS CHECK
  Hooks (Tier 1):    {n}/5 installed ✅|❌
  Hooks (tier-gated):{n}/{m} for the ACTIVE tier ✅|❌   (Tier 2 → 3, Tier 3 → +2)
  Hooks (reference): {n}/4 generated, 0 installed ✅|❌   (installed>0 is a FAIL)
  Hooks (disabled):  package-activation-guard present, enabled=false ✅|❌
  Conditional hooks: {n} generated (of {m} applicable) ✅|❌
  Rules (always):    {n}/12 ✅|❌
  Rules (tier-gated):{n}/9 ✅|❌
  Rules (conditional):{n} generated ✅|❌
  Agents (always):   {n}/4 ✅|❌
  Agents (tier-gated):{n}/{m} for the ACTIVE tier ✅|❌   (Tier 2 → 4, Tier 3 → +1)
  Agents (drift):    {n}/1 IF a DWG baseline exists ✅|❌
  Compliance log:    {n}/3 ✅|❌
  State file:        ✅|❌
  Dashboard:         ✅|❌
  ENFORCEMENT-GUIDE:     ✅|❌
  COMPLIANCE_README: ✅|❌
```

---

## V2: Traceability Validation

**Question:** "Can every rule trace to a steering file section OR the built-in baseline?"

### Rules

1. Every rule in `.governance/rules/*.md` MUST have one of:
   - `Derived From: rules/{file} → {section}` (steering-derived)
   - `Derived From: Built-in Baseline → {baseline rule name}` (methodology floor)
   - `Derived From: {operational doc} → {section}` (enrichment source)

2. No "orphan rules" — if a rule cannot trace to a source, it must be removed.

3. Built-in baseline rules are self-justifying — they exist because of AI-DLC methodology. Their source is "AI-DLC methodology: {principle}."

### Traceability Check

| Check | Pass Criteria |
|-------|--------------|
| Every rule has a `Derived From` field | No rule without stated source |
| Steering-derived rules reference existing files | Every `rules/{file}` reference exists |
| Built-in baseline rules match the 10 declared baselines | No baseline rule that isn't in the declared list |
| Tier tags are valid | Every rule has `Tier: 1|2|3` and it matches the expected category tier |

### Two-Source Traceability Example

```markdown
### GOV-ROLE-004: Session Owner ≠ Reviewer
Tier: 2
Derived From: Built-in Baseline → "Author ≠ Approver" + rules/role-isolation.md → "Segregation of Duties" table
```

This shows BOTH sources: baseline provides the universal principle; steering provides the project-specific detail.

---

## V3: Consistency Validation

**Question:** "Do all generated rules and hooks agree with each other?"

### Cross-Artifact Consistency Checks

| Check | Artifacts Involved | What to Verify |
|-------|-------------------|----------------|
| Hook rule references | `.governance/hooks/*.json` prompts vs. `.governance/rules/*.md` | Every rule ID cited in a hook prompt exists in a rule file |
| Hook file patterns vs. tech stack | `.governance/hooks/*.json` patterns vs. `tech-stack.md` | Patterns use correct extensions for the stated technology |
| Hook file patterns vs. real folders | `.governance/hooks/*.json` patterns vs. actual filesystem | Patterns reference paths that actually exist |
| Rule severity consistency | Rules with same severity across categories | 🔴 Critical used consistently (not inflated) |
| Tier assignments | Rules vs. tier model | GOV-ROLE rules all say Tier 2 (not mixed 1 and 2) |
| Phase gate rules vs. DoD | phase-gates.md criteria vs. DEFINITION_OF_DONE.md | No contradiction between what gates require and what DoD defines |
| COMPLIANCE_README vs. actual output | Description sections vs. generated artifacts | README describes what actually exists |
| ENFORCEMENT-GUIDE vs. actual hooks | Listed hooks vs. `.governance/hooks/` contents | All listed hooks exist; no unlisted hooks |
| State file schema | .compliance-state.json structure vs. audit agent expectations | State file has all fields the audit agent reads |

### Consistency Check Format

```
V3: CONSISTENCY CHECK
  Hook→Rule references:   ✅|❌ {n} rule IDs, all valid
  Hook→Path patterns:     ✅|❌ {n} patterns, all real
  Severity consistency:   ✅|❌
  Tier assignments:       ✅|❌
  Phase gates vs. DoD:    ✅|❌
  README vs. actual:      ✅|❌
  ENFORCEMENT-GUIDE vs. hooks:✅|❌
  State file schema:      ✅|❌
```

---

## V4: Conditional Generation Validation

**Question:** "Are conditional rules/hooks correctly included/excluded?"

### Validation Matrix

| Conditional Artifact | Trigger | Verification |
|---------------------|---------|--------------|
| Tenant isolation rules + hook | `multi-tenancy.md` exists in `rules/` | Check filesystem |
| API versioning rules | `api-versioning.md` exists | Check filesystem |
| Resilience rules | `resilience-standards.md` exists | Check filesystem |
| Tracing rules | `observability-tracing.md` exists | Check filesystem |
| Performance rules | `performance-standards.md` exists | Check filesystem |
| Workflow rules | `workflow-engine.md` exists | Check filesystem |
| Frontend rules | `frontend-standards.md` exists | Check filesystem |
| Event sourcing rules | `event-sourcing.md` exists | Check filesystem |
| Feature flag rules | `feature-flags.md` exists | Check filesystem |
| MCP governance | `.kiro/settings/mcp.json` exists with configured servers | Check filesystem + parse JSON |
| Brownfield artifacts | `brownfield-patterns.md` exists | Check filesystem |

### Rules

1. **Conditional file present → rules MUST be generated** (completeness)
2. **Conditional file absent → rules MUST NOT be generated** (no bloat)
3. **Generated conditionals are documented** in the output summary with justification
4. **Skipped conditionals are documented** with reason

---

## V5: Hook Integrity Validation

**Question:** "Do hooks use real paths, correct event types, and follow the design principles?"

### Hook-Level Checks (Per Hook)

| Check | Pass Criteria |
|-------|--------------|
| Event type is valid | One of: fileEdited, fileCreated, fileDeleted, preToolUse, postToolUse, promptSubmit, agentStop, postTaskExecution, preTaskExecution, userTriggered |
| File patterns use real paths | Patterns reference actual tech-stack extensions AND actual module paths |
| Debounce tier correct | Security-critical hooks → fileEdited; Advisory hooks → agentStop |
| Prompt references real rule IDs | Rule IDs in prompt exist in `.governance/rules/` |
| Prompt includes compliance logging block | Last section of prompt is the JSONL logging instruction |
| Prompt includes phase-awareness check | Prompt mentions checking `.compliance-state.json` → `currentPhase` |
| Prompt includes DX principle | Contains "If all rules pass, confirm compliance silently" or equivalent |
| Noise classification assigned | Hook is tagged 🔴 Essential / 🟠 High-value / 🟡 Advisory |

### Debounce Strategy Verification

**Installed hooks only.** A hook that is not generated has no event type to verify.

| Hook | Expected Event Type | Rationale |
|------|:-------------------:|-----------|
| sensitive-data-check | fileEdited | Secrets + PII risk (Tier A) |
| tenant-isolation-check | fileEdited | Data leakage risk (Tier A, conditional) |
| security-gate-check | fileEdited | Security-critical (Tier A) |
| migration-safety | fileEdited | Destructive ops (Tier A) |
| session-end-compliance | agentStop | Advisory (Tier B) — the consolidated sweep; intermediate states mislead, refs resolve after all writes |
| pre-code-spec-check | preToolUse (write) | Gate before code is written |
| post-task-governance | postTaskExecution | Check after task completion |
| segregation-check | postTaskExecution | Author ≠ approver, at a task boundary |
| change-readiness-gate | preTaskExecution | CM artifacts before Integration tasks (Tier 3) |
| exception-expiry-check | userTriggered | On-demand expired-bypass scan (Tier 3) |
| package-activation-guard | promptSubmit | Multi-package switch guard (ships disabled) |

> **`secret-detection` was never a real filename.** This table previously opened with it; the actual hook is **`sensitive-data-check.json`**. A validation table naming a file that does not exist cannot fail — it silently checks nothing, which is why the row survived.
>
> **Four `agentStop` rows collapsed into one.** `domain-layer-purity`, `module-boundary-check`, `coverage-check` and `naming-check` are reference-only; their checks fire inside `session-end-compliance.json`, so that is the hook whose event type matters. **Five rows removed** — `documentation-reminder` (no longer generated) and `steering-quality-check`, `session-discipline`, `periodic-audit`, `pre-pr-checklist` (all retired to agents, which have no event type because a human invokes them).

---

## V6: Enforceable Quality Validation

**Question:** "Are rules concrete enough to be checked by a hook or audit agent?"

### The Enforceability Test

Every rule must be binary — either followed or not. No subjective judgment.

| ❌ Aspirational (Fails V6) | ✅ Enforceable (Passes V6) |
|---------------------------|---------------------------|
| "Code should be well-structured" | "Every module MUST have domain/application/infrastructure/presentation layers" |
| "Security is important" | "Every endpoint MUST have `[Authorize]` or explicit `[AllowAnonymous]`" |
| "Tests should cover critical paths" | "Line coverage MUST be ≥ 80% at PR gate" |
| "Follow good naming practices" | "Controllers: `{Entity}Controller.{ext}`. Services: `{Entity}Service.{ext}`" |
| "Consider performance" | "GET single entity response MUST be < 50ms (p95)" |

### Language Check

Rules MUST use:

| Enforceable Language | NOT Acceptable |
|---------------------|----------------|
| MUST / MUST NOT | should / should not |
| NEVER / ALWAYS | avoid / try to |
| Required / Forbidden | preferred / discouraged |
| Exactly / At least / Maximum | approximately / around / about |

### V6 Check Format

```
V6: ENFORCEABLE CHECK
  Rules scanned:        {n}
  Weak language found:  {n} instances
  Non-binary rules:     {n} (cannot be checked yes/no)
  All rules enforceable: ✅|❌
```

---

## V7: Context Budget Validation

**Question:** "Does AI-GCE's output respect the ≤300-line always-inclusion steering budget?"

### The Rule

Total lines across ALL `inclusion: always` files in `rules/` MUST NOT exceed 300 lines. AI-GCE's Step 4b can generate additional steering files — these MUST be `fileMatch` only (not `always`).

### Checks

| Check | Pass Criteria |
|-------|--------------|
| AI-GCE generated steering uses fileMatch | Any `compliance-*.md` files in `rules/` have `inclusion: fileMatch` in front-matter |
| Total always-inclusion budget | Sum lines of all `inclusion: always` files ≤ 300 |
| No always-inclusion from AI-GCE | AI-GCE NEVER generates `inclusion: always` steering (those are AI-DWG's domain) |

### If Budget Exceeded

If pre-existing AI-DWG steering already uses 290 lines and AI-GCE adds Phase-aware steering:
1. AI-GCE's generated steering MUST use fileMatch (not always) — problem avoided
2. If somehow an always file was generated by AI-GCE → convert to fileMatch immediately
3. Report in validation: "⚠️ Context budget at {n}/300 lines — AI-GCE output uses fileMatch only"

---

## V8: Phase-Awareness Validation

**Question:** "Are rules correctly tagged with their applicable phase?"

### Phase Applicability Rules

| Rule Category | Applicable From Phase | Not Before |
|--------------|----------------------|------------|
| NC-* (Naming) | Setup | — (always relevant) |
| PG-SETUP-* | Setup | — |
| GOV-INIT-* | Setup | — |
| GOV-SESSION-* (basic) | Setup | — |
| PG-FOUND-* | Foundation | Setup |
| GOV-SESSION-* (full) | Foundation | Setup |
| SEC-* (baseline) | Foundation | Setup |
| PG-INCEP-* through PG-TEST-* | Construction | Foundation |
| GOV-PR-*, GOV-CICD-* | Construction | Foundation |
| GOV-ROLE-*, GOV-TT-* | Construction | Foundation |
| GOV-DEVOPS-* | Construction | Foundation |
| CM-* | Integration | Construction |
| PG-CONST-*, PG-INTEG-* | Integration | Construction |
| SEC-* (SOX/GDPR) | Go-Live | Integration |

### Checks

| Check | Pass Criteria |
|-------|--------------|
| Every rule has phase tag | Rule metadata includes applicable phase |
| Hooks reference phase check | Hook prompts mention checking currentPhase in state file |
| No Construction-phase rules in hook for Setup projects | Phase-check prevents premature firing |

---

## V9: Logging Validation

**Question:** "Does every hook prompt end with the compliance logging block?"

### The Non-Negotiable Rule

EVERY hook prompt MUST end with:

```
## Compliance Logging
After completing all checks above, append a JSON event to
`compliance-log/events/{today-date}.jsonl` (create the file if it doesn't exist).
Format:
{"timestamp": "{ISO-8601-UTC}", "type": "check", "id": "chk-{date}-{time}-{seq}",
 "hook": "{hook-name}", "trigger": "{event-type}", "ruleId": "{primary-rule-checked}",
 "ruleSeverity": "{severity}", "result": "{pass|fail|warn}",
 "message": "{one-line-finding}"}
Log ONE event per rule checked. If multiple rules are checked, log multiple events.
```

### Checks

| Check | Pass Criteria |
|-------|--------------|
| All hooks have logging block | Every `.json` file's prompt ends with "## Compliance Logging" section |
| Logging format matches schema | JSON structure matches compliance-log-schema.md |
| Tier A hooks include sessionDedup | fileEdited hooks add `"sessionDedup": true` field |
| Hook name in log matches filename | `"hook": "sensitive-data-check"` matches `sensitive-data-check.json` |
| `ruleId` resolves to a real rule | The logged `ruleId` is an actual generated rule ID, **not** an unsubstituted `{primary-rule-checked}` placeholder. ⚠️ An unresolved placeholder means the event is unattributable and V3's rule-reference check has nothing to verify — treat as a FAIL, not a warning |

---

## Full Validation Report Template

```
═══════════════════════════════════════════════════════════════
  AI-GCE VALIDATION REPORT
  Workspace: {name}
  Generated: {date}
  Mode: {1: Full Generation | 2: Re-Derivation | 3: Brownfield | 4: Tier Activation}
═══════════════════════════════════════════════════════════════

V1: COMPLETENESS        {PASS|FAIL}  — {n} hooks, {n} rules, {n} agents
V2: TRACEABILITY        {PASS|FAIL}  — {n} rules, all traced to source
V3: CONSISTENCY         {PASS|FAIL}  — {n} cross-checks, {n} passed
V4: CONDITIONAL         {PASS|FAIL}  — {n} generated, {n} skipped (all justified)
V5: HOOK INTEGRITY      {PASS|FAIL}  — {n} hooks, all valid patterns + debounce correct
V6: ENFORCEABLE         {PASS|FAIL}  — No weak language, all rules binary
V7: CONTEXT BUDGET      {PASS|FAIL}  — Always-inclusion ≤ 300 lines; GCE uses fileMatch only
V8: PHASE-AWARENESS     {PASS|FAIL}  — All rules phase-tagged; hooks check currentPhase
V9: LOGGING             {PASS|FAIL}  — All hook prompts have compliance logging block
V10: TERRITORY SEGREGATION {PASS|FAIL} — Hook patterns exclude infra; preamble present

───────────────────────────────────────────────────────────────
OVERALL:                {PASS|FAIL}

{If FAIL: list specific failures with remediation actions}
═══════════════════════════════════════════════════════════════
```

---

## V10: Package Territory Segregation Validation

**Question:** "Do hook patterns and prompts correctly exclude package infrastructure?"

### Checks

| Check | Pass Criteria |
|-------|---------------|
| No bare `**/*.ext` in Tier A hooks | Pattern is scoped to at least one directory level (e.g., `src/**/*.ts`) — except secrets hook which uses Layer 2 |
| Preamble present in file-context hooks | First section of prompt is "Package Territory Check" for fileEdited, fileCreated, and agentStop hooks |
| Preamble absent in non-file hooks | promptSubmit, preToolUse, postTaskExecution, and userTriggered hooks do NOT have the preamble |
| Registry file generated | `.governance/PACKAGE_TERRITORIES.md` exists after full generation |
| Registry covers all package outputs | All AI-* family output paths have an entry |
| Custom section has markers | `<!-- custom -->` tags present for re-derivation safety |
| Patterns do not match excluded zones | No hook pattern structurally matches `.kiro/`, `.governance/`, `compliance-log/`, `project-initiation/`, `architecture/`, `management_framework/`, or `templates/` |

### V10 Check Format

```
V10: TERRITORY SEGREGATION CHECK
  Bare wildcards in Tier A:   {n} found (expected: 0, except secrets with justification)
  Preamble in file hooks:     {n}/{m} ✅|❌
  Preamble absent non-file:   {n}/{m} ✅|❌
  Registry generated:         ✅|❌
  Registry covers all paths:  ✅|❌
  Custom markers present:     ✅|❌
  Pattern-zone conflicts:     {n} found ✅|❌
```

---

## V11: Sensor-Wiring Verification (aidlc only)

**Question:** "Was every emitted v2 sensor manifest actually bound to a stage?"

Runs **only under `buildProfile: aidlc`** (no other build method emits v2 sensor manifests). Under `aidlc`, AI-DWG emits the sensor manifests + `.governance/AIDLC_SENSOR_WIRING.md` but does **not** edit v2's stage files — so a manifest no stage imports **never fires, silently**. AI-GCE reads `seeded.sensors` in `.governance/aidlc-bootstrap.yaml` and reports any emitted-but-unwired manifest as a finding (`manifests-only` = present-but-not-firing; `wired` = confirmed live). Full procedure + report format in `common/sensor-wiring-verification.md` (merged item 26). An unwired manifest is a **reportable finding (WARNING)**, never a silent pass; AI-GCE reports it but does not apply the binding (v2 / the human applies from the wiring file).

## When to Run Validation

| Scenario | Validation Scope |
|----------|-----------------|
| After Full Generation (Mode 1) | ALL checks (V1–V10); **+ V11 when `buildProfile: aidlc`** |
| After Re-Derivation (Mode 2) | V2, V3, V4, V5, V6, V9, V10 on affected artifacts only |
| After Brownfield Adoption (Mode 3) | ALL checks (V1–V10) + brownfield-specific: baseline exists, adoption plan exists |
| After Tier Activation (Mode 4) | V1 (new artifacts complete), V3 (consistency with new tier), V5 (new hooks valid), V10 (new hooks segregated) |
| User requests "validate compliance" | ALL checks (V1–V10) |

---

## Validation Failures — Response

| Failure Type | Severity | Response |
|-------------|----------|----------|
| Missing required artifact (V1) | BLOCKING | Generate the missing artifact before completing |
| Untraceable rule (V2) | BLOCKING | Add source reference or remove the rule |
| Cross-artifact inconsistency (V3) | BLOCKING | Resolve before presenting to user |
| Wrong conditional (V4) | BLOCKING | Add missing or remove unjustified artifact |
| Hook uses non-existent path (V5) | BLOCKING | Fix pattern to match actual filesystem |
| Hook has wrong event type (V5) | BLOCKING | Correct per debounce strategy table |
| Aspirational rule language (V6) | WARNING | Rewrite to enforceable form |
| Context budget exceeded (V7) | BLOCKING | Convert AI-GCE steering to fileMatch |
| Missing phase tag (V8) | WARNING | Add phase applicability to rule |
| Missing logging block (V9) | BLOCKING | Add compliance logging to hook prompt |
| Bare wildcard in Tier A hook (V10) | BLOCKING | Scope pattern to application paths or justify Layer 2 reliance |
| Missing preamble in file-context hook (V10) | BLOCKING | Prepend Package Territory Check preamble |
| Registry missing or incomplete (V10) | WARNING | Generate or update PACKAGE_TERRITORIES.md |

**BLOCKING** = must fix before output is complete.
**WARNING** = flag to user but can proceed.

---

## Checkpoint Enforcement

Beyond the V1–V10 validation pipeline above, AI-GCE enforces these completion checkpoints before declaring any generation pass complete. A checkpoint failure halts or degrades the pass per its failure action.

| Checkpoint | Requirement | Failure Action |
|------------|-------------|---------------|
| Workspace marker found | `rules/workspace-rules.md` exists | Stop; ask user for workspace path |
| Technology identified | `tech-stack.md` readable and has technology entry | Warn; use generic file patterns as fallback |
| Module paths confirmed | `module-structure.md` readable and has module paths | Warn; scan actual folder structure as fallback |
| Hooks use real paths | All hook file patterns match actual workspace structure | Fix before completing |
| Rules have sources | Every rule references a specific steering file | Flag untraced rules; request confirmation |
| No contradictions | Rules in one category don't contradict rules in another | Resolve or flag to user |
| COMPLIANCE_README generated | `.governance/COMPLIANCE_README.md` exists and is populated | Do not complete without this |
| Brownfield baseline present | If `brownfield-patterns.md` exists, `.governance/brownfield-baseline.md` must also exist | Trigger Mode 3 if missing |

---

## Artifact Content Rules (IMP-001–005, 015, 016, 019)

> Added 2026-08-15 from user-workspace field validation. These are **BLOCKING** rules — an artifact fails validation without compliance.

### IMP-001: Self-Explanatory Quantitative Artifacts

Every artifact containing quantitative analysis (scores, rankings, matrices, assessments) MUST include a **"What This Analysis Means"** section placed AFTER the document title/introductory blockquote but BEFORE the first numbered section (`## 1. ...`).

The section MUST include:
1. **Plain-language summary** — what the numbers mean in business terms
2. **Concrete example** — one specific finding from the analysis explained simply
3. **Business implications** — what action or decision the analysis supports

**Blocking:** Artifact fails validation if quantitative analysis is present but no interpretation section exists at the top.

---

### IMP-002: Completeness & Downstream Resolution

Every artifact MUST include a **"Completeness & Downstream Resolution"** section (placed after the main content, before Glossary/Sources) that answers three questions:

1. **What's complete here?** — which aspects are fully covered in this document
2. **What's partial and why?** — what is shown as representative samples vs exhaustive, and the rationale
3. **Where/when does each gap get resolved?** — downstream package/stage that fills each gap (with package code + stage reference)

**Blocking:** Artifact fails validation without this section.

---

### IMP-003: Back-Propagate "Gap Filled" Status

After each stage writes its artifact, scan all earlier-stage artifacts in the same package for "Completeness & Downstream Resolution" sections that reference the just-completed stage. Update those references:
- FROM: "Where gaps get filled → {Package} Stage N"
- TO: "✅ Completed — see `{artifact-path}`"

Stale "where gaps get filled" references pointing to already-completed stages are a **validation failure**.

**Post-gate check:** After each gate approval, verify no earlier artifact references the just-completed stage as "pending."

---

### IMP-004: Human-Readable Package Key Expansion

First mention of any package code in an artifact MUST include a parenthetical plain-language description.

**Pattern:** `AI-{XXX} ({Human-Readable Purpose})`

**Examples:**
- `AI-AAG (Governance & Handoff)` — not just `AI-AAG`
- `AI-INT (Integration Architecture)` — not just `AI-INT`
- `TALC (Technology Architecture Life Cycle)` — not just `TALC`

Subsequent mentions in the same document may use the bare code after first-use expansion.

**Blocking:** First-use bare codes without expansion are a validation failure.

---

### IMP-005: Mandatory Glossary Section

Every artifact MUST include a **"Glossary"** section at the bottom of the document (before Sources Used or doc signature/footer). The glossary MUST:

1. Appear as the last major section before Sources/footer
2. Contain a table with **Term** and **Meaning** columns
3. Cover ALL abbreviations (e.g., K8s, mTLS, GPU, RAG, SWOT) and domain-specific technical terms used in the document
4. Be tailored to each document's actual content — not a generic copy-paste

**Blocking:** Artifact fails validation without a document-specific glossary.

---

### IMP-015: Rank-Score Consistency

In any table with both a **Rank** column and a numeric **Score/Significance** column:

1. Rank MUST be in **descending score order** (highest score = rank 1)
2. If a dependency or business override changes the rank, an explicit **override column or footnote** MUST explain WHY (e.g., "GATE-ZERO prerequisite", "Blocked by #1")
3. **Equal scores** MUST use tied ranks (e.g., 1, 1, 1, 4 — not 1, 2, 3, 4)

**Blocking:** Rank/score mismatch without documented justification is a validation failure.

---

### IMP-016: Key-Reference Traceability (CRITICAL)

Every reference to a key (`OBJ-01`, `CAP-05`, `REQ-D-03`, `THEME-02`, `SD-001`, `GAP-04`, etc.) in any artifact MUST be a markdown link pointing to the source document where that key is formally defined.

**Pattern:** `[KEY-ID](relative-path-to-source#anchor)`

**Rules:**
1. Every register/definition document MUST define anchors for every key (`<a id="key-id"></a>`)
2. Every reference to a key in any other artifact MUST be a markdown link to the source anchor
3. **Bare key codes without links are NOT acceptable** in final artifacts — only in draft state
4. Each stage's post-write checklist must include a "Link Validation" step verifying all keys are linked

**Key prefixes requiring anchors and links:** `OBJ-`, `THEME-`, `SD-`, `CAP-`, `REQ-`, `REQ-D-`, `REQ-T-`, `CC`, `CON-`, `GAP-`, `DEBT-`, `RDR-`, `ST-`, `SO-`, `WO-`, `WT-`, `INFRA-`, `SEC-`, `RES-`, `GPU-`

**Blocking (CRITICAL):** Bare key references without links are a validation failure.

---

### IMP-019: Column Legend for Register-Style Tables

Every **register-style table** (4+ columns with an ID/identifier column or technical register structure) MUST be followed immediately by a blockquote column legend.

The legend MUST:
1. Be inside a `>` blockquote
2. Start with `**Column Legend:**`
3. Contain a two-column table (Column / Description)
4. Describe ALL columns including value-set meanings (e.g., "Priority: Critical = must resolve before deployment, High = must resolve before production")

**Excluded:** Simple key-value tables (Field/Value format) and prose checklists.

**Blocking:** Register-style tables without a column legend are a validation failure.
