<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Hooks From Steering — Derivation Logic

## Purpose

This file defines HOW to derive hook JSON files from steering content. It covers: which steering files produce which hooks, how to populate file patterns, debounce tier assignment, noise classification, compliance logging injection, and phase-awareness injection.

> **Since merged item 23 — this is the *hook render* of the neutral intermediate, not the origin of hook JSON.** Generators emit a **format-neutral intermediate** (rule + check logic + glob — see `rendering/neutral-intermediate.md`); the **mechanism** axis (`buildProfile` → hook vs v2 sensor, via `common/build-method-resolution.md`) decides whether that intermediate becomes a hook at all. When the mechanism is `hook`, this file renders it; when the mechanism is `sensor` (under `aidlc`, for the sensor-convertible set), the sensor render (merged item 25) takes the same intermediate instead. The `checkLogic` + `glob` are identical either way — this file never re-derives a check, it renders the hook form of one. The secrets/PII check renders here as a hook under **every** build method (the one genuine hook⇄sensor pair).

> **Secrets/PII has two hook variants (merged item 24c) — advisory and blocking.** `templates/hooks/sensitive-data-check.json` is the advisory (`askAgent`, `fileEdited`) form; `templates/hooks/sensitive-data-check-blocking.json` is the blocking (`PreToolUse`, exit-2-on-violation) form. Which one is emitted is decided by the recorded enforcement strength via `common/strength-to-mechanism.md` — `block` (where the platform supports pre-write blocking) → the blocking variant; `warn`, or a platform that cannot block pre-write → the advisory variant (with the limitation disclosed in `PLATFORM_NOTES.md`). Both carry **identical check logic**; only the action type and trigger differ. This is the one check where blocking must be a hook — a secret on disk is irreversibly exposed before any gate fires (a gate-fired sensor is too late).

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in event-driven automation: each hook is a trigger → condition → action pipeline that must fire at exactly the right moment
- Apply the debounce decision tree rigorously: security-critical = fileEdited (Tier A), advisory = agentStop (Tier B)
- Derive file patterns from tech-stack + module-structure + actual filesystem — generic globs are engineering failures
- Ensure every hook prompt follows the 4-part structure: phase check → rule checks → DX principle → compliance logging
- Classify noise honestly: 🔴 Essential (auditor cares), 🟠 High-value (drift if removed), 🟡 Advisory (team convenience)

### Anti-Patterns for This Activity
- Do NOT use generic `**/*.ts` patterns — always derive module-specific, layer-specific paths
- Do NOT skip the compliance logging block on any hook (it's the audit trail, non-negotiable)
- Do NOT assign Tier A to advisory hooks (it creates noise fatigue that undermines genuine security alerts)

### Quality Check
A good output from this activity sounds like:
- "security-gate-check.json: event=fileEdited, debounce=Tier A, noise=🔴 Essential. Pattern: `src/modules/*/presentation/**/*.controller.ts`. Prompt cites SEC-01/02/03 + SEC-BASELINE-02, includes phase-check, DX silence rule, and compliance logging suffix."
- "ENFORCEMENT-GUIDE.md organizes 10 installed hooks + 1 ships-disabled + 4 reference-only + 6 conditional by activation tier. Removal guidance: `session-end-compliance.json` first (advisory batch), NEVER remove security-gate-check."

### MANDATORY: Cite rule IDs from the OWNING generator, never from a hook table

Every rule ID in this file is **cited**, not produced. The generator that emits a rule alongside its statement is the owner, and the owner wins on every disagreement.

| Rule | Why |
|---|---|
| **Read the owning generator's produced-rules table** — not another hook mapping, not this file's own history | Copying from a consuming table is what produced the eight wrong rows this inventory previously carried |
| **Then reconcile that generator against itself** | Reading the owner is necessary but **not sufficient** — three generators cite IDs in their *hook-mapping* section that their own *produced-rules* table never emits. A rule ID is real only if some table states it **with a rule statement attached** |
| **Match the family's padding exactly** | **Code-level families take two digits** — `SEC-01`, `DATA-02`, `MOD-01`, `DOM-05`, `NC-01`, `ERR-01`, `ARCH-01`. **Process/governance families take three** — `GOV-*`, `CM-001`, instantiated `PG-INCEP-001`. Baseline rules are always `{FAMILY}-BASELINE-{NN}`, two-digit |
| **Never invent a family** | `NAME-*`, `TEAM-*`, `SPRINT-*`, `PR-*` and `GOV-DDD-*` **do not exist**. The real families are `NC-*`, `GOV-TT-*`, `GOV-SPRINT-*`, `GOV-PR-*`, and domain purity is `DOM-05` + `MOD-02` |

⚠️ **Two error types, and only the first is caught by an existence check.** An ID that exists **nowhere** (`SEC-006`, `DATA-012`) fails immediately. An ID that **exists but belongs to another hook or another family** passes existence and is still wrong — `DATA-012/013/014` was a digit-perfect transposition of `GOV-DEVOPS-012/013/014` from a different generator's mapping for the *same* hook. Verify the **relationship**, not just the identifier.

---

## Hook Derivation Pipeline

```
For EACH hook to generate:
1. IDENTIFY source steering file(s) → what rules this hook enforces
2. DETERMINE event type → when should this hook fire?
3. DERIVE file patterns → from tech-stack.md + module-structure.md + folder scan
4. ASSIGN debounce tier → Tier A (fileEdited) or Tier B (agentStop) or Other
5. APPLY PATTERN SCOPING (Layer 1 — Package Territory Segregation):
   • Read.governance/PACKAGE_TERRITORIES.md for excluded zones
   • Ensure derived file patterns do NOT structurally match any excluded zone
   • If hook needs broad coverage (e.g., secrets) → keep broad pattern BUT rely on Layer 2
   • Prefer: {module-root}/**/*.{ext} over **/*.{ext}
   • NEVER use a bare **/*.{ext} that would match.kiro/,.governance/, compliance-log/,
     project-initiation/, architecture/, docs/, management_framework/, or templates/
6. PREPEND PACKAGE TERRITORY PREAMBLE (Layer 2 — Runtime Filter):
   • Load common/hook-preamble.md
   • For hooks with file context (fileEdited, fileCreated, agentStop): prepend preamble
   • For non-file hooks (promptSubmit, preToolUse, postTaskExecution, userTriggered): skip
   • Preamble goes BEFORE the phase check — absolute first evaluation
7. ASSIGN noise classification → 🔴 Essential / 🟠 High-value / 🟡 Advisory
8. WRITE prompt → cite rule IDs, include phase-check, include DX principle
9. APPEND compliance logging block → non-negotiable suffix
10. VALIDATE → patterns exist on filesystem, rule IDs exist in generated rules,
    patterns do NOT structurally match excluded zones (unless justified by Layer 2)
```

---

## Hook Inventory (What Gets Generated)

> **Counts, stated once so they cannot drift.** **10 installed hooks** (5 at Tier 1, 3 at Tier 2, 2 at Tier 3) · **1 ships disabled** · **4 reference-only templates that are deliberately NOT installed** · **6 conditional** · **4 retired to agents** · **1 removed entirely**. **Twenty-one `.json` template files now exist — one for every hook this inventory declares** (the Tier 1–3 installed set, the ships-disabled optional, the four reference-only, and the six conditional). ♻️ *This read "Thirteen `.json` template files exist … the Tier 3 pair plus the six conditional hooks are generated without a reference template"; the eight that lacked one were authored 2026-09-01 (merged item 3) so every declared hook has documentation parity.* **A template is a worked example of the output, not a prerequisite** — every element of one is produced by the ten-step pipeline above, and the territory preamble is loaded from `common/hook-preamble.md` at step 6. **Having a template does NOT change a hook's disposition:** the four reference-only templates are still NOT installed (their checks run in `session-end-compliance.json`), the six conditional templates are still emitted only when their steering file exists, and the ships-disabled optional still ships `"enabled": false`. What changed is documentation coverage, not the install set.

### Tier 1 — Always Installed (Day 0)

| Hook File | Event Type | Debounce | Noise | Source Steering | Rules Enforced (owning generator) |
|-----------|:----------:|:--------:|:-----:|----------------|----------------|
| `pre-code-spec-check.json` | preToolUse (write) | — | 🟠 | session-governance.md + project-governance.md | `GOV-SESSION-001/003` · `PG-INCEP-001/002` *(session-governance-generator · phase-gates-generator)* |
| `api-contract-check.json` | fileCreated | — | 🟠 | api-standards.md | `GOV-API-001` *(api-compliance-generator)* |
| `security-gate-check.json` | fileEdited | Tier A | 🔴 | security-rules.md | `SEC-01/02/03` · `SEC-BASELINE-02` *(security-compliance-gen)* |
| `migration-safety.json` | fileEdited | Tier A | 🔴 | database-rules.md + infrastructure decisions | `DATA-BASELINE-01/02` · `DATA-02/03` *(data-governance-generator)* · `GOV-DEVOPS-012/013/014` · `GOV-DEVOPS-BASELINE-02` *(devops-generator)* |
| `sensitive-data-check.json` | fileEdited | Tier A | 🔴 | observability-sensitive.md | `SEC-BASELINE-01` · `SEC-20/21/22` *(security-compliance-gen)* · `SEC-PII-01/02/03` *(logging-generator)* ⚠️ see the duplicate-family note below |

### Tier 2 — Installed at Sprint 2+ (when readiness met)

| Hook File | Event Type | Debounce | Noise | Source Steering | Rules Enforced (owning generator) |
|-----------|:----------:|:--------:|:-----:|----------------|----------------|
| `post-task-governance.json` | postTaskExecution | — | 🟠 | project-governance.md + DEFINITION_OF_DONE.md | `PG-*` for the current phase *(phase-gates-generator)* · `GOV-SESSION-003/012` *(session-governance-generator)* · `ARCH-01` *(architecture-compliance-gen)* · `GOV-ROLE-BASELINE-01` *(role-isolation-generator)* · `GOV-DEVOPS-005` *(devops-generator)* · `ERR-01` *(error-handling-generator)* |
| `segregation-check.json` | postTaskExecution | — | 🟠 | role-isolation.md + CODEOWNERS | `GOV-ROLE-004` *(role-isolation-generator)* |
| `session-end-compliance.json` | agentStop | Tier B | 🟠 | consolidated — see below | `MOD-01/02/03` *(module-boundary-generator)* · `DOM-05` *(domain-context-generator)* · `GOV-CICD-002/003` *(cicd-gates-generator)* · `NC-01`…`NC-08` *(naming-generator)* |

> **`session-end-compliance.json` is the consolidated `agentStop` sweep.** It replaces four individual `agentStop` hooks with one pass and one report — cutting firings from four to one and prompt cost from four to one. The four individual templates are **retained as reference and NOT installed**; see the reference-only table below.

### Tier 3 — Installed Pre-Release (when readiness met)

| Hook File | Event Type | Debounce | Noise | Source Steering | Rules Enforced (owning generator) |
|-----------|:----------:|:--------:|:-----:|----------------|----------------|
| `change-readiness-gate.json` | preTaskExecution | — | 🟠 | project-governance.md | `CM-001/002/004/005/006/010` *(change-management-gen — **owner**)* · `PG-CONST-*` · `PG-INTEG-*` *(phase-gates-generator — references, does not re-declare)* |
| `exception-expiry-check.json` | userTriggered | — | 🟠 | compliance-log-governance | `GOV-LOG-004/005/006` *(compliance-log-gov-gen)* |

> **`change-readiness-gate` enforces the union of two families, and `change-management-gen.md` owns the declaration.** Two generators previously claimed this hook at the same event and tier with **disjoint** rule sets, and no file stated the union — so whichever generator a builder happened to read produced a hook enforcing half the intended set. Both families are genuinely produced, so this was a missing union rather than a wrong ID. `phase-gates-generator.md` now references this row instead of re-declaring it (single source of truth per family-hook pairing).

### Optional — Family-Wide (opt-in, ships DISABLED)

| Hook File | Event Type | Debounce | Noise | Source | Rules Enforced |
|-----------|:----------:|:--------:|:-----:|--------|----------------|
| `package-activation-guard.json` | promptSubmit | — | 🟡 | `TRIGGER_KEYS_REFERENCE.md` + each package core's Activation section | **None** — governs trigger-key switching, which sits outside the rule model |

> Ships `"enabled": false`. Useful only where several AI-* packages share one workspace. `promptSubmit` is the noisiest event surface there is, so this is opt-in by design rather than by omission.

### Reference-Only Templates — retained, NOT installed as hooks

These four `.json` files are generated because they **document the rule logic**, and their checks are performed by `session-end-compliance.json` instead. **A validation check MUST NOT require them to be installed.**

| Template File | Documents | Its checks run in |
|-----------|-----------|-------------------|
| `module-boundary-check.json` | `MOD-01/02/03` *(module-boundary-generator)* · `GOV-TT-002` *(team-topology-generator)* | `session-end-compliance.json` |
| `domain-layer-purity.json` | `DOM-05` *(domain-context-generator)* · `MOD-02` *(module-boundary-generator)* | `session-end-compliance.json` |
| `coverage-check.json` | `GOV-CICD-002/003` *(cicd-gates-generator)* | `session-end-compliance.json` |
| `naming-check.json` | `NC-01`…`NC-08` *(naming-generator)* | `session-end-compliance.json` |

### Retired to Process Agents — NOT generated as hooks

Each conversion is recorded in the agent template that performed it. **These names must not reappear in any hook inventory, runtime tree, or completeness check.**

| Former Hook | Now | Agent Template | Why an agent |
|---|---|---|---|
| `session-discipline.json` | `SDC__` | `session-discipline-agent.md` | Fired on **every** prompt — the highest-noise surface in the package |
| `pre-pr-checklist.json` | `PRC__` | `pre-pr-checklist-agent.md` | A process milestone a human invokes, not an event |
| `periodic-audit.json` | `CAA__` | `compliance-audit-agent.md` | On-demand full scan — inherently user-triggered |
| `steering-quality-check.json` | `SQC__` | `steering-quality-agent.md` | Advisory quality review at a milestone |

> **The timing that is given up, and where it went.** Retiring `session-discipline.json` kept the checks and lost the **interception** — an agent runs when invoked, so a violating prompt proceeds and is reviewed afterwards. That timing is recoverable via an opt-in `promptSubmit` hook shipping `"enabled": false`, on the `package-activation-guard` precedent.

### Removed Entirely

| Former Hook | Disposition |
|---|---|
| `documentation-reminder.json` | ❌ **Removed.** **No generator produces any rule family for it** — there is no `DOC-*`, `DOCS-*` or `GOV-DOC-*` family in the package, so it had consumers but no producer and could never cite a real rule ID. Its intent (docs updated after a feature) is carried by the `session-end-compliance` sweep. |

> **Why an orphan hook is worse than a missing one.** It was declared, tier-assigned, debounce-classified, listed in a runtime tree as always-present, **and** separately declared retired — so every count that included it was wrong and every attempt to generate it would have produced a hook with no rule to cite.

### ⚠️ Duplicate PII family — flagged, not resolved here

`security-compliance-gen.md` produces **`SEC-20/21/22`** from `observability-sensitive.md`, and `logging-generator.md` produces **`SEC-PII-01/02/03`** for the same concern. Both are genuinely produced, so both are cited above rather than one being silently dropped. **Choosing a single family is a design change, not a citation fix**, and it is out of scope for this inventory pass — a hook citing one family while the other still generates rules would leave those rules unenforced and unrecorded.

### ⚠️ Rules whose enforcement assignment is still open

`SEC-10` (DTO validation), `SEC-11` (injection prevention) and `SEC-12` (CORS origins) are produced by `security-compliance-gen.md` and **assigned to no hook**. `security-gate-check.json`'s prompt substantively checks the first two — input validation and string-concatenation in queries — **without citing their IDs**, so those checks run and produce no attributable compliance event. They are deliberately **not** claimed in the table above: assigning them here would record enforcement that has not been designed, and all three are deterministically checkable and belong on a gate-fired surface. Leave them visible and unassigned until that surface exists.

### Conditional Hooks (only if steering file exists)

| Hook File | Condition | Event Type | Debounce | Source |
|-----------|-----------|:----------:|:--------:|--------|
| `tenant-isolation-check.json` | multi-tenancy.md exists | fileEdited | Tier A 🔴 | multi-tenancy.md |
| `resilience-gate.json` | resilience-standards.md exists | agentStop | Tier B | resilience-standards.md |
| `tracing-check.json` | observability-tracing.md exists | agentStop | Tier B | observability-tracing.md |
| `event-sourcing-check.json` | event-sourcing.md exists | agentStop | Tier B | event-sourcing.md |
| `frontend-a11y-check.json` | frontend-standards.md exists | agentStop | Tier B | frontend-standards.md |
| `mcp-audit-log.json` |.kiro/settings/mcp.json configured | postToolUse (`^mcp_.*`) | — | MCP governance |

---

## File Pattern Derivation

### The Rule

Hook `patterns` fields MUST use technology-specific, module-specific paths. NEVER use generic globs like `**/*.ts`.

### Pattern Assembly Formula

```
Pattern = {module-path-prefix}/{layer-pattern}/{technology-file-pattern}

Where:
  module-path-prefix = from module-structure.md (e.g., "src/modules/*" or "src/Modules/*")
  layer-pattern = from module-structure.md layer rules (e.g., "presentation" or "Presentation")
  technology-file-pattern = from tech-stack.md (see mapping table below)
```

### Technology → File Pattern Mapping

| tech-stack.md Says | Controllers | Services | Entities | Migrations | Tests |
|-------------------|-------------|----------|----------|------------|-------|
| NestJS / TypeScript | `*.controller.ts` | `*.service.ts` | `*.entity.ts` | `src/migrations/*.ts` | `*.spec.ts` |
| Django / Python | `views.py`, `viewsets.py` | `services.py` | `models.py` | `*/migrations/*.py` | `test_*.py` |
| ASP.NET Core / C# | `*Controller.cs` | `*Service.cs` | `*.Entity.cs` | `Migrations/*.cs` | `*Tests.cs` |
| Spring Boot / Java | `*Controller.java` | `*Service.java` | `*Entity.java` | `db/migration/*.sql` | `*Test.java` |
| Go | `*_handler.go` | `*_service.go` | `*_model.go` | `migrations/*.sql` | `*_test.go` |

### Pattern Examples (Assembled)

For a NestJS project with module-structure.md showing `src/modules/{module}/`:

| Hook | Pattern |
|------|---------|
| api-contract-check | `src/modules/*/presentation/**/*.controller.ts` |
| domain-layer-purity | `src/modules/*/domain/**/*.ts` |
| migration-safety | `src/migrations/**/*.ts` |
| naming-check | `src/modules/**/*.ts` |
| security-gate-check | `src/modules/*/presentation/**/*.controller.ts` |
| tenant-isolation-check | `src/modules/*/domain/entities/**/*.ts` |

For an ASP.NET project with module-structure.md showing `src/Modules/{Module}/`:

| Hook | Pattern |
|------|---------|
| api-contract-check | `src/Modules/*/Presentation/**/*Controller.cs` |
| domain-layer-purity | `src/Modules/*/Domain/**/*.cs` |
| migration-safety | `**/Migrations/**/*.cs` |
| security-gate-check | `src/Modules/*/Presentation/**/*Controller.cs` |
| tenant-isolation-check | `src/Modules/*/Domain/Entities/**/*.cs` |

---

## Pattern Scoping — Package Territory Segregation (Layer 1)

### The Mandatory Rule

Hook `patterns` MUST be scoped to application code paths. They MUST NOT structurally match package infrastructure directories. This is Layer 1 of the three-layer segregation strategy.

### Pattern Scoping Decision Tree

```
Is this hook's pattern a bare wildcard (e.g., **/*.ts, **/*.json)?
├── YES → Can it be scoped to a module/src root?
│         ├── YES → Scope it (e.g., src/**/*.ts, src/modules/**/*.ts)
│         └── NO  → Does this hook GENUINELY need workspace-wide coverage?
│                   ├── YES (e.g., secrets in any file) → Keep broad, rely on Layer 2 preamble
│                   └── NO  → Scope it to at least one directory level
└── NO  → Already scoped (e.g., src/modules/*/presentation/**/*.controller.ts)
          → Verify it doesn't accidentally include excluded zones → PASS
```

### Scoping Examples by Hook

| Hook | ❌ NEVER Use | ✅ Use Instead | Why |
|------|-------------|---------------|-----|
| sensitive-data-check | `**/*.cs, **/*.ts, **/*.json` | `src/**/*.{ext}, *.env, appsettings*.json` | Excludes.kiro/,.governance/, compliance-log/ structurally |
| security-gate-check | `**/*Controller.cs` | `src/modules/*/presentation/**/*Controller.cs` | Already scoped — OK |
| naming-check | (agentStop — no pattern) | N/A | Preamble filters infra files from scan |
| domain-layer-purity | (agentStop — no pattern) | N/A | Preamble filters infra files from scan |

### Exception: Secrets Detection

The `sensitive-data-check` hook legitimately needs to scan root config files (`.env`, `appsettings.json`, etc.) because secrets can appear there. For this hook:
- Keep application-scoped patterns PLUS specific root config patterns
- Use Layer 2 preamble to filter `.kiro/**` and `.governance/**` at runtime
- Pattern template: `src/**/*.{ext}, *.env, appsettings*.json, {config-roots}`

### Technology-Specific Safe Patterns

| Stack | Application Code Pattern | What's Excluded Structurally |
|-------|-------------------------|------------------------------|
| NestJS | `src/**/*.ts`, `src/**/*.json` | `.kiro/`, `.governance/`, `compliance-log/`, root `*.json` |
| Django | `{app}/**/*.py`, `{app}/**/migrations/*.py` | `.kiro/`, `.governance/`, `compliance-log/`, `docs/` |
|.NET | `src/**/*.cs`, `src/**/*.json` | `.kiro/`, `.governance/`, `compliance-log/` |
| Spring Boot | `src/**/*.java`, `src/main/resources/**` | `.kiro/`, `.governance/`, `compliance-log/` |
| Generic | `src/**/*` | Everything outside `src/` |

---

## Debounce Strategy Assignment

### Decision Tree

```
Is this hook checking for something that is DANGEROUS even in intermediate state?
├── YES → Does a single frame of violation pose security/data risk?
│         ├── YES → Tier A: fileEdited (fire every save, sessionDedup in log)
│         └── NO  → agentStop is sufficient
└── NO  → Does this hook care about FINAL state only?
          ├── YES → Tier B: agentStop (fire once at session end)
          └── NO  → Use appropriate non-file event type (postTask, promptSubmit, userTriggered)
```

### Tier A Criteria (fileEdited — immediate fire)

ALL of these conditions must be true:
- Violation creates security risk, data leakage, or financial error
- Waiting until session end means the damage already happened
- False positives on intermediate state are acceptable (security > noise)

### Tier B Criteria (agentStop — final state only)

ANY of these conditions make a hook Tier B:
- The check is about code STRUCTURE (using statements, imports, references)
- The check cares about COMPLETENESS (all tests, all docs, all coverage)
- Intermediate states regularly produce false positives (e.g., adding import before writing code)

### Session Deduplication (Tier A only)

For Tier A hooks, add to the compliance logging section:

```
"sessionDedup": true
```

This tells the compliance log to keep only the LAST event per hook + file path within a session. Earlier check results for the same file are overwritten — only the final state matters for audit.

---

## Prompt Construction Template

Every hook prompt follows this structure:

```
{PHASE CHECK}
{RULE CHECKS — numbered, specific}
{DX PRINCIPLE — silent if passing}
{COMPLIANCE LOGGING BLOCK}
```

### Phase Check (First Line)

```
Check.compliance-state.json → currentPhase. Only enforce rules applicable to {applicable phases}.
If this is a {earlier phase} project, skip silently.
```

### Rule Checks (Core)

```
Check the following rules against the current context:
1. {RULE-ID}: {what to check} — {how to verify}
2. {RULE-ID}: {what to check} — {how to verify}
...

If any rule is violated, warn with:
- Rule ID
- What was expected
- What was found
- Remediation suggestion
```

### DX Principle (Before Logging)

```
If all rules pass, confirm compliance silently. Do NOT produce output when nothing is wrong.
```

### Compliance Logging Block (Mandatory Suffix)

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

For Tier A hooks, add after the format block:
```
If a previous log entry exists for the same hook + file path within this session,
OVERWRITE it (keep only the latest result). Add "sessionDedup": true to the event.
```

---

## Noise Classification Guide

| Classification | Criteria | Hook Removal Impact |
|:-:|-----------|---------------------|
| 🔴 Essential | Security risk, data integrity, compliance evidence | Removing = audit trail gap, security hole, or data leak risk |
| 🟠 High-value | Architecture enforcement, governance checks, methodology discipline | Removing = drift accumulates silently; caught only at periodic audit |
| 🟡 Advisory | Quality suggestions, documentation reminders, style checks | Removing = minor quality decline; team can self-manage |

**Rule for classification:**
- Would an external auditor care if this hook was removed? → 🔴 Essential
- Would architecture/governance drift if this hook was removed? → 🟠 High-value
- Is this primarily about team convenience/quality? → 🟡 Advisory

---

## ENFORCEMENT-GUIDE Generation

When generating `.governance/hooks/ENFORCEMENT-GUIDE.md`, **render `templates/hooks/ENFORCEMENT-GUIDE.md`** — do not compose the tier tables here.

**Why this file no longer carries a draft.** It used to embed a full copy of the guide, which made **three** places in the package assert a hook inventory: this file's own tables above, the embedded draft, and the canonical template. All three drifted, and the draft was the least visible of them — it still listed `session-discipline`, `periodic-audit`, `pre-pr-checklist`, `steering-quality-check` and `documentation-reminder` as live hooks long after four became agents and one was removed, and it named a removal order whose first two entries no longer exist. **A third copy of a list is a third thing to keep true.**

The division of authority:

| Question | Authoritative source |
|---|---|
| Hook **or** agent — which mechanism does a check use? | **** + `generators/agents-from-steering.md` + the per-conversion record in each agent template |
| Which hooks are **installed, and at which tier**? | **`templates/hooks/ENFORCEMENT-GUIDE.md`** |
| Which **rule IDs** does a hook enforce? | The **owning generator** for each rule family — see the inventory tables above |
| What gets **generated** and with what patterns? | This file (the derivation pipeline) |

**When the inventory changes, both this file's tables and the canonical template change together.** They answer different questions about the same set, so they cannot be allowed to disagree — and the guide's own generation step is the natural place to catch it.
