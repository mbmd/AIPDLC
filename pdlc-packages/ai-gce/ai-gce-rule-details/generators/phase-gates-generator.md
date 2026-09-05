<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Phase Gates — Derivation Logic

## Purpose

Derives phase gate rules (PG-*) from `project-governance.md` and `DEFINITION_OF_DONE.md`. Gates define what MUST exist before transitioning between project phases.

---

## MANDATORY: Stage Sub-Role — Audit & Compliance Specialist

During THIS activity, ALSO adopt the mindset of an **Audit & Compliance Specialist**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in control gates: phase transitions are the highest-stakes governance moments — missing a gate criterion risks delivering incomplete work
- Ensure gate criteria are evidence-based: "charter exists" is verifiable, "team is ready" is not
- Recognize that phase gates are the ONLY rules that can BLOCK transitions — all other rules warn
- Map gate criteria to specific artifacts (files, test results, sign-offs) that prove readiness
- Tier-gate appropriately: setup gates are Tier 1 (day 0), per-module gates are Tier 2, go-live gates are Tier 3

### Anti-Patterns for This Activity
- Do NOT create subjective gate criteria ("code is clean enough") — gates must be binary pass/fail
- Do NOT apply go-live gates during construction phase (phase-awareness is critical)
- Do NOT conflate Definition of Done (per-task) with phase gates (per-transition) — they're related but distinct

### Quality Check
A good output from this activity sounds like:
- "PG-FOUND-003: CI/CD pipeline operational with Build → Test → Security stages before Construction begins. Tier 2, Foundation phase. Enforced by post-task-governance.json."
- "Phase Gate Status: Can transition to Construction? ✅ Yes — all 6 Critical PG-SETUP rules pass. 1 Warning (documentation incomplete, non-blocking)."

---

## Source Files

| File | What to Extract |
|------|----------------|
| `project-governance.md` | Phase model, quality gates table, gate criteria per transition |
| `DEFINITION_OF_DONE.md` | Per-task completion criteria (feeds per-module gates) |

---

## Built-in Baseline

| Rule ID | Statement |
|---------|-----------|
| PG-BASELINE-01 | SOMETHING must exist (spec, design, or requirements) before implementation code is written |

---

## Gate Structure (From project-governance.md Phase Model)

The phase model in project-governance.md defines which transitions exist. For EACH transition, extract gate criteria:

| Transition | Rule Prefix | What Must Exist |
|-----------|:-----------:|-----------------|
| Setup → Foundation | PG-SETUP-* | Charter, RACI, steering files, team agreements, ADRs |
| Foundation → Construction | PG-FOUND-* | CI/CD working, auth framework, reference module, shared kernel |
| Per-module: Inception → Domain | PG-INCEP-* | Requirements spec, API contract, domain model documented |
| Per-module: Domain → Application | PG-DOM-* | Aggregates implemented, value objects immutable, no infra deps |
| Per-module: Application → Infra | PG-APP-* | Use cases implemented, DTOs defined, validation rules |
| Per-module: Infra → Presentation | PG-INFRA-* | Repositories implemented, migrations created |
| Per-module: Presentation → Tests | PG-PRES-* | Controllers match contract, auth on all endpoints |
| Per-module: Tests → Merge | PG-TEST-* | Unit tests, integration tests, contract tests, all pass, reviewed |
| Construction → Integration | PG-CONST-* | All modules tested individually, cross-module events flowing |
| Integration → Go-Live | PG-INTEG-* | E2E tests, security audit, UAT sign-off, rollback plan |

---

## Tier Progression

| Tier | Gates Active |
|:----:|-------------|
| 1 | PG-SETUP-* only (basic: Setup → Foundation) |
| 2 | + PG-FOUND-*, PG-INCEP-* through PG-TEST-* (per-module gates) |
| 3 | + PG-CONST-*, PG-INTEG-* (cross-module + go-live gates) |

---

## Hook Mapping

| Hook | Event | Rules Enforced |
|------|-------|----------------|
| `pre-code-spec-check.json` | preToolUse (write) | PG-INCEP-001/002 (spec + contract exist) |
| `post-task-governance.json` | postTaskExecution | All PG-* for current phase |
| `change-readiness-gate.json` | preTaskExecution | PG-CONST-*, PG-INTEG-* (Tier 3) |

---

## Phase-Vocabulary Mapping — `PG-*` families → AI-DLC v2 phase-rule files

**When the build method is `aidlc`, phase gates are delivered as v2 *phase rules* (destination D2), one file per v2 phase.** v2 exposes exactly four phase-rule files, and their filenames are **fixed** (per the frozen output contract §18) — a phase rule attaches to a stage by filename, so a differently-named file attaches to nothing. AI-GCE has **five** phase groupings and v2 has **four** files; the mapping below is derivable, not a judgement call (both sets are fixed facts). This mapping is authoritative and is consumed by the phase-file emission step (merged item 16); it MUST be authored before any `PG-*` rule is routed to a v2 phase file.

| AI-GCE phase | Its gate families | → v2 phase file | Reasoning |
|---|---|:---:|---|
| **Setup** | `PG-SETUP-*` (charter, RACI, steering, team agreements, ADRs) | ⛔ **No phase file** | Satisfied **before v2's first stage runs** — workspace preparation (AI-DWG's job), not a phase obligation v2 evaluates |
| **Foundation** | `PG-FOUND-*` (CI/CD operational, auth framework, reference module, shared kernel) | ⛔ **No phase file** | Same — all precede v2's run |
| **Construction (inception half)** ⭐ | `PG-INCEP-*` (requirements spec, API contract, domain model documented) | → **`inception.md`** | ⭐ **The split.** AI-GCE's "Construction" bundles the per-module *inception* gate with the per-module *build* gates; v2 separates them |
| **Construction (build half)** ⭐ | `PG-DOM-*`, `PG-APP-*`, `PG-PRES-*`, `PG-TEST-*` (aggregates, use cases, DTOs, controllers, tests pass) | → **`construction.md`** | The build half of the same AI-GCE phase |
| **Integration** | `PG-CONST-*` (all modules tested individually, cross-module events flowing) | → **`construction.md`** | Cross-module integration is still **build** work — v2 has no separate integration phase; promoting it to `operation` would gate a running system on something that must be true *before* it runs |
| **Go-Live** | `PG-INTEG-*` (E2E, security audit, UAT sign-off, rollback plan) **+ `CM-*`** | → **`operation.md`** | The only families that concern a system **in service** |
| *(nothing from AI-GCE)* | — | **`ideation.md`** | Correct, not a gap — see trap 1 below |

**Net: five AI-GCE phases → four v2 files, with two AI-GCE phases (Setup, Foundation) unmatched-by-design and one (Construction) splitting across `inception.md` + `construction.md`.**

### Three traps the emission step (item 16) must not fall into

1. **`ideation.md` is legitimately empty of AI-GCE rules — and MUST NOT ship silently blank.** Ideation is idea-shaping, upstream of governance; AI-GCE has no gate there, and inventing one would be fabricating a rule to fill a file. But §18 fixes all four filenames, so the file **is** emitted — **with a stated reason** (e.g. "No AI-GCE phase gates apply at ideation; this phase precedes governance"), never zero-byte. A blank rule file is indistinguishable from a failed generation (the same defect class as AI-TGE's silent degradation). Verified by TR-830 negative assertion (1).

2. **Setup's and Foundation's rules are NOT dropped — they change form.** They become **already-satisfied preconditions in the bootstrap record** (`aidlc-bootstrap.yaml`) plus **behavioural rules in `memory/team.md`** where they describe ongoing obligations rather than one-time gates. This is what keeps §0.1 principle 4 (no capability removed) intact — the mechanism changes, the capability does not. Reading "no phase file" as "delete these rules" is a ledger breach. Verified by TR-830 negative assertion (2); ledger row A36.

3. **`construction.md` receives rules from TWO AI-GCE phases** — the build half of Construction *and* all of Integration. They MUST be **grouped and labelled by originating AI-GCE phase** inside the file, or a later reader cannot tell why a cross-module event-flow gate sits beside a DTO-validation gate, and the next re-derivation will assume one is misfiled. Verified by TR-830 negative assertion (3).

> **Ledger + test cross-reference:** this mapping is summarised in `CAPABILITY_PRESERVATION_LEDGER.md` row A36 and verified structurally + by acceptance in **TR-830** (phase-mapping fidelity). Item 16 (`P6`) emits the four files from this mapping and depends on it.

---

## Key Rule

Phase gate rules are the ONLY rules that can BLOCK phase transitions. All other rules warn but don't block. When the `CAA__` compliance-audit agent runs a full scan, it reports:

```
Phase Gate Status: Can transition to {next phase}? 
  ✅ Yes — all Critical PG-* rules pass
  ❌ No — {n} Critical items blocking: {list}
```
