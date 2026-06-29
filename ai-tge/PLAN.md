# AI-TGE — Package Build Plan

**Package:** AI-TGE (AI-Driven Test Governance Engine)
**Type:** Hybrid (Lifecycle + Engine)
**Status:** ✅ Complete — All 10 build steps done. Ready for dry test (TR-003 re-run).
**Idea Source:** Approved internal idea record (retained in the package-development environment)
**Build Persona:** `#persona-qa-test-engineer` + `#persona-process-designer`
**Created:** 2026-06-08

---

## Summary Report

| Field | Value |
|-------|-------|
| Status | ✅ COMPLETE — All 10 build steps done. Package structurally complete. Ready for dry test. |
| Sessions | S12 (2026-06-08): Plan + Core Engine | S13 (2026-06-09): Common files + persona alignment | S## (2026-06-13): Steps 6-10 (stage details + templates + INSTALL expansion + verification) |
| Scope | v1.0 — Governance Core (11 capabilities) |
| Build Estimate | Medium-Large (4-5 sessions) |
| Key Decisions Resolved | Two-source model (YES), taxonomy (ISTQB), risk scoring (multi-factor), output folder (.tge/), depth levels, conditional stages |
| Persona | `#persona-qa-test-engineer` (auto-loaded via `ai-tge-rules.md`) |

---

## Step 1: Problem Space Definition

### Package Identity

| Field | Value |
|-------|-------|
| **Name** | AI-TGE |
| **Full Title** | AI-Driven Test Governance Engine |
| **Package Type** | Hybrid (Lifecycle + Engine) |
| **Primary Input** | AI-ADLC output (AP) + AI-DWG output (DW) + AI-DLC v1 state (aidlc-docs/) |
| **Primary Output** | Test Strategy + Test Register + Coverage Reports + Defect Log + Debt Scorecard |
| **User Persona** | QA Lead / Test Engineer / Senior Developer |
| **Family Position** | Companion to AI-DLC v1 (parallel, not sequential) |

### Problem Statement

AI-DLC v1 builds software but has no structured test governance. It generates test instructions (build-and-test stage) and can enforce specific testing patterns (PBT extension), but provides no mechanism to:
- Derive test requirements from architecture decisions
- Track which tests must exist and whether they do
- Measure coverage against architectural commitments
- Prioritize test debt by architectural risk
- Adapt when architecture changes (reconciliation)
- Assess existing test coverage in brownfield projects

### Family Position (Companion Pattern)

```
   ── PROJECT LAYER ────────────────────────────────────►

    AI-ADLC ─┐
    AI-UXD  ─┼─►  AI-DWG  ─►  AI-DLC v1 (build) ¹
    AI-POLC  ─┘                    ▲
                                  │ observes
    AI-GCE  +  AI-TGE  ── alongside AI-DLC v1 (continuous quality) ──►
    Guard it   Test it
                   ▲
                   └─ AI-TGE reads AP (AI-ADLC) + DW (AI-DWG); observes AI-DLC v1
  ¹ AI-DLC v1 = Amazon's open-source build lifecycle (not ours; we feed it).
```

AI-TGE is a **companion package** — it does not sit in the linear flow but runs alongside it, in the Project layer, next to AI-GCE:
- Reads from multiple Project-layer predecessors (ADLC + DWG)
- Runs as a continuous quality companion alongside AI-DLC v1 (with AI-GCE)
- Observes a sibling package's execution (DLC)
- Output feeds back into project quality (not into another package)

### Dual-Mode Operation

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Strategy Mode** (Lifecycle) | Before/alongside AI-DLC v1 start | Creates test strategy, derives baseline register from AP, defines coverage goals |
| **Observation Mode** (Engine) | During AI-DLC v1 execution | Watches state, registers tests per completed feature, tracks coverage, reports gaps, scores debt |

### Input/Output Contract

**I Read:**
- `AI-ADLC output/` — Architecture Package (API contracts, component designs, ADRs, security decisions, integration maps)
- `AI-DWG output/` — Workspace (tech stack, testing frameworks configured, steering rules)
- `aidlc-docs/aidlc-state.md` — AI-DLC v1 progress (which units/stages are complete)
- `aidlc-docs/inception/user-stories/` — User stories with acceptance criteria
- `aidlc-docs/inception/requirements/` — NFR requirements
- `aidlc-docs/construction/*/` — Functional designs, NFR designs, build-and-test instructions
- Source code test directories — actual test files (existence check)

**I Produce:**
- `tge-state.md` — Marker file + state tracking (mode, progress, last observation)
- `test-strategy.md` — Test approach, types, coverage goals (derived from architecture)
- `test-register.md` — Master list: commitment → required test → status
- `coverage-report.md` — Gaps between architecture promises and actual tests
- `defect-log.md` — Structured defect tracking linked to stories/components
- `debt-scorecard.md` — Prioritized missing tests by architectural risk

**Marker File:** `tge-state.md`

---

## v1.0 Capabilities (11)

| # | Capability | Mode | QA Engineer Notes |
|---|-----------|------|-------------------|
| 1 | **Architecture → Test Requirements derivation** | Strategy | Maps: API contracts → contract tests, security decisions → penetration + auth tests, data models → data integrity tests, integrations → integration tests, NFRs → performance/load tests. Each mapping is typed (functional / non-functional / structural). |
| 2 | **Story → Acceptance Test derivation** | Strategy | Each acceptance criterion becomes a testable assertion. Stories with multiple scenarios generate one test per scenario, not one test per story. |
| 3 | **Test Register** | Both | NOT a flat list. Structured as: Commitment ID → Test Type → Test Name → Status → Risk Score → Linked Component → Linked Story. Supports filtering by type, status, risk, component. |
| 4 | **Test Strategy generation** | Strategy | Defines: test pyramid ratios (unit:integration:e2e), test environment requirements, test data strategy, automation approach, risk-based prioritization method, entry/exit criteria per test level. |
| 5 | **AI-DLC v1 state observation** | Observation | Detects: unit completion (Code Generation done), Build-and-Test stage reached, story approval. Each trigger event adds specific test registrations — not a generic "add tests." |
| 6 | **Coverage reporting (commitment-based)** | Observation | Multiple views: (a) by architectural commitment, (b) by component, (c) by test type, (d) by risk level. NOT just one flat percentage. |
| 7 | **Defect logging** | Observation | Structured: Defect ID → Severity (Critical/High/Medium/Low) → Category (Functional/Performance/Security/Data) → Linked Test → Linked Component → Root Cause → Status. |
| 8 | **Risk-Based Test Prioritization** | Observation | Scores each missing test by: (a) architectural risk if untested, (b) blast radius of the component, (c) complexity of the logic, (d) frequency of change. Produces ranked backlog. |
| 9 | **Architecture Reconciliation** | Observation | AP delta detection: new components → register new tests; removed components → deprecate tests; changed contracts → flag tests for review. Non-destructive — proposes changes, doesn't auto-apply. |
| 10 | **Brownfield Assessment** | Strategy | Scans existing test directories → maps found tests to architecture commitments → identifies: covered (has test), uncovered (no test), orphaned (test exists but no matching commitment). |
| 11 | **State tracking** | Both | `tge-state.md`: current mode, last observation timestamp, register stats (total/covered/missing/deprecated), assessment version, linked AP version. |

---

## v1.1 Deferred

| Capability | Rationale for Deferral |
|-----------|----------------------|
| Test Specifications (natural-language specs per registered test) | Guidance layer — v1.0 proves governance first |
| Test Templates (structural templates per test type) | Large surface area; needs v1.0 register format stable |
| PBT Compliance Tracking | Couples to specific AI-DLC v1 extension; add after core proven |
| Extension System | v1.0 must stabilize before enabling specialized extensions |

---

## Design Decisions (Resolved)

| # | Decision | Resolution | Implemented In |
|---|----------|-----------|----------------|
| 1 | Two-source model? (built-in baseline) | **YES** — 20-rule baseline catalog covering API, security, data, integration, business logic, workflow, error handling, configuration. AP-derived tests are additive on top. | `core-engine.md` + `common/two-source-model.md` |
| 2 | Output folder structure | **`.tge/`** — dotfolder under workspace root. TGE is a companion, not owned by AI-DLC v1. Artifacts survive independently. | `core-engine.md` (Output Directory Structure) |
| 3 | Observation trigger mechanism | **User-invoked with auto-detect** — user says "check coverage" or engine detects aidlc-state.md changes on session start. No continuous polling. | `core-engine.md` (Observation Phase) + `common/session-continuity.md` |
| 4 | Depth levels | **Three-tier:** Minimal (score 5-10): strategy + register only. Standard (score 11-18): + coverage reports + debt scoring + brownfield. Comprehensive (score 19-25): + full traceability + reconciliation + story mapping. | `core-engine.md` (Depth Calibration) + `common/process-overview.md` |
| 5 | Conditional capabilities | **Always:** 1, 3, 4, 5, 6, 8, 11. **Conditional:** 2 (stories exist), 7 (defects reported), 9 (AP changes), 10 (brownfield detected). | `core-engine.md` (Stage definitions) + `common/process-overview.md` |
| 6 | Test type taxonomy | **ISTQB standards-based:** Level (Unit/Integration/System/Acceptance) × Type (Functional/Non-Functional/Structural) × Technique (Architecture-Derived/Baseline/Story-Derived/Manual). Three-dimensional classification. | `core-engine.md` (Test Taxonomy) + `common/test-taxonomy.md` |
| 7 | Risk scoring formula | **Weighted multi-factor:** Architectural Risk × Blast Radius × Logic Complexity × Change Frequency. Each factor 1-5. Composite 1-625. Buckets: Critical (400-625), High (150-399), Medium (50-149), Low (1-49). | `core-engine.md` (Risk-Based Test Prioritization) + `common/test-taxonomy.md` |

---

## Build Sequence (Planned)

Following PLAYBOOK Steps 1-10:

| Step | Activity | Status |
|------|----------|--------|
| 1 | Define Problem Space | ✅ Done (this file) |
| 2 | Research & Extract | ✅ Done — studied internal test-management, AI-GCE two-source pattern, ISTQB taxonomy, AI-DLC v1 aidlc-docs structure |
| 3 | Present Plan for Approval | ✅ Done — phases, stages, file structure approved in idea file |
| 4 | Build Core File | ✅ Done — `ai-tge-rules/core-engine.md` (full 12-stage engine) |
| 5 | Build Common Files | ✅ Done — 7 files: process-overview, welcome-message, session-continuity, test-taxonomy, two-source-model, question-format-guide, content-validation |
| 6 | Build Stage Detail Files | ✅ Done — strategy/ (6 files) + observation/ (6 files). All 12 core-engine references resolve. |
| 7 | Build Templates | ✅ Done — 6 output templates: test-strategy, test-register, coverage-report, debt-scorecard, defect-log, tge-state |
| 8 | Build README + LICENSE + Setup | ✅ Done — LICENSE (Apache 2.0), README (Alpha Preview banner), INSTALL.md expanded to 6 platforms |
| 9 | Verify Completeness | ✅ Done — all 12 stage detail file references resolve; template set matches core-engine output structure |
| 10 | Compare Against Reference | ✅ Done — structural pattern mirrors AI-GCE (sibling engine); AI-PILC stage detail pattern followed |

---

## Applicable Lessons

From the package-development lessons log:

| Lesson | How It Applies |
|--------|---------------|
| L1 (Life Cycle naming) | Called "Engine" not "Life Cycle" — correct for hybrid |
| L3 (Reconciliation) | Architecture reconciliation included in v1.0 |
| L4 (Adaptive intake) | Multiple input modes: full chain / AP-only / brownfield |
| L5 (Downstream signaling) | Receives signals from ADLC; doesn't need to signal downstream |
| L7 (Conditional generation) | Not all capabilities needed for all projects |
| L8 (Gap analysis) | Compare against internal test-management + AI-DLC v1's build-and-test |
| L9 (Extensions) | Designed for v1.1; not in v1.0 |
| L10 (Adapt from predecessor) | Reads AP + DW automatically; never asks user to re-enter |
| L13 (Explicit contracts) | I Read / I Produce defined above |
| L14 (Marker files) | `tge-state.md` is the marker |
| L15 (Extension awareness) | Needs to detect ADLC extensions (e.g., microservices → more integration tests) |
| L23 (Brownfield) | Brownfield assessment included in v1.0 |
| L25 (Two-source model) | ✅ Resolved — 20-rule baseline catalog implemented in `common/two-source-model.md` |

---

## Risks (Carried from Idea File)

| Risk | Mitigation |
|------|-----------|
| AI-DLC v1 structure changes | Pin to v0.1.8 structure; add version detection |
| Companion pattern confuses users | Clear README + diagram |
| Hybrid model complex to explain | Auto-mode detection + strong welcome message |
| Overlap perception with AI-GCE | Explicit boundary statement in README |
| Scope creep into test writing | Hard boundary enforced in core file |
| Brownfield + Reconciliation adds complexity | Accepted — family consistency requires it |

---

*Filed: 2026-06-08 | Author: Maheri | Session: S12*
