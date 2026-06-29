---
inclusion: manual
---
<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# PRIORITY: This engine OVERRIDES default test management approaches when activated by key `_TGE_` or when the user requests test governance derivation from an architecture package and development workspace

# Activate via the explicit key `_TGE_`, OR when the user requests test strategy creation, test register derivation, coverage analysis, or test debt assessment — then ALWAYS follow this engine FIRST. See "Activation & Multi-Package Isolation" below before asserting priority in a shared workspace.

---

## AI-TGE: AI-Driven Test Governance Engine

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**Purpose:** Read architecture decisions (from AI-ADLC) and a development workspace (from AI-DWG), derive a structured test governance layer — strategy, register, coverage tracking, risk scoring — and continuously observe AI-DLC v1 execution to maintain test accountability. Works on both fresh (greenfield) and existing (brownfield) codebases.
**Compatible With:** AI-ADLC v1.0+ (Architecture Package), AI-DWG v1.0+ (Development Workspace), AI-DLC v1 (v0.1.8+ aidlc-docs structure)

**Metaphor:** A test governance inspector. It reads everything the architecture promised — API contracts, security decisions, integration maps, component designs — and builds a register of tests that MUST exist to verify those promises were kept. Then it watches the build, tracking what gets tested and what doesn't, scoring the risk of every gap.

---

## MANDATORY: Obtaining the Current Timestamp

When you need the current date/time to stamp generated output (e.g. a dashboard's "Last refreshed", a coverage report, or a state-file `Last Updated`), **always source it from a shell command via the normal command-execution tool. NEVER use an internal, hosted, or "server-side" time/code-execution tool to compute the time** — doing so emits an unsupported content block and aborts the run.

Get the current UTC instant with one command, then reuse it for the whole pass:

```powershell
[DateTimeOffset]::UtcNow.ToString('o')
```

On a non-Windows shell: `date -u +%Y-%m-%dT%H:%M:%SZ`.

Capture the time **once at the start of a pass** and reuse it, so every file written in one pass shares a consistent stamp.

---

## The AI-* Family

The family is organized into two **layers** joined by a **router on the edge**: the
Portfolio layer reasons across MANY projects; the Project layer executes ONE project.

```
╔════════════════ PORTFOLIO LAYER · scope = MANY projects ════════════════╗

   (optional)
    AI-ILC  ⇢  AI-PILC  ⇢  AI-PPM
    Decide it   Initiate it   Govern it (portfolio of N projects)

╚═════════════════════════════════╤═══════════════════════════════════════╝
                                   │
                                AI-FLO   Route it — package-to-package
                                   │     flow on the edge between layers
╔════════════════ PROJECT LAYER · scope = ONE project ════════════════════╗

    AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG ──► AI-DLC v1 (build) ¹
    Own it      Design UX   Design it   Prepare it       ▲
                                                         │
                        AI-POLC ⇄ AI-DLC v1 (back-and-forth)┘
                AI-DLC v1 ⇢ AI-UXD+AI-POLC (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC v1 (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC v1 = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-POLC** ³ | Interactive workflow (lifecycle) | PIP | Product Backlog Package (PBP) |
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP + PBP | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | PIP + PBP + UXP | Architecture Package (AP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC v1** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POLC) | Working Software |

> ¹ **AI-DLC v1** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC v1 consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ All packages in this table are **built**. AI-PPM (portfolio engine), AI-FLO (router), AI-POLC (product ownership lifecycle), and AI-UXD (UX design lifecycle) were the last four — completed June 2026. Within the Project layer, **AI-POLC, AI-UXD, and AI-ADLC run sequentially** (POLC→UXD→ADLC) — each feeds the next, culminating at AI-DWG which receives all three outputs (AP + PBP + UXP). **AI-GCE and AI-TGE run alongside AI-DLC v1** as continuous quality engines; **AI-POLC ⇄ AI-DLC v1** exchange backlog/acceptance throughout delivery; and **AI-DLC v1 runtime feedback flows back to both AI-UXD and AI-POLC**. Feedback loops (ADLC→POLC cost/risk, ADLC→UXD constraints) provide iterative refinement without changing the forward sequence.

**AI-TGE's position:** a continuous **test-governance companion** in the **Project layer**. It is not a sequential stage — it reads the Architecture Package (AI-ADLC) and Development Workspace (AI-DWG), runs alongside AI-DLC v1 together with AI-GCE as a continuous quality engine, and feeds its findings back into project quality rather than into a downstream package.

---

## Activation & Multi-Package Isolation

**Explicit activation key:** `_TGE_`
Type `_TGE_` in any prompt to activate this engine. An explicit key is treated as a **direct user order to switch** — it wins over keyword matching and every sibling package immediately.

**Active-package status key:** `_ACTIVE_`
Type `_ACTIVE_` at any time and the assistant reports which AI-* package is currently active (and its state-marker status). This is a read-only check — it changes nothing and never triggers a switch.

**Keyword activation (fallback):** This engine also activates when the user requests **test governance** specifically — test strategy, register derivation, coverage analysis, test-debt assessment. It does NOT claim generic "compliance governance", "architecture / UX design", "backlog", or "workspace" requests — those belong to sibling packages (notably AI-GCE for compliance governance).

**Switching rule — NON-NEGOTIABLE: a package switch NEVER happens without a direct user order or explicit confirmation.**
1. **Direct order:** the user types an explicit activation key (`_TGE_`, or a sibling `_XXX_` key). Treat this as the order — switch immediately, no confirmation needed.
2. **Otherwise, check for an active sibling:** scan for any sibling `*-state.md` (e.g. `adlc-state.md`, `polc-state.md`) or `.compliance-state.json` whose status is not "complete". If one exists, that package is active — do NOT take over. Ask first: "AI-GCE is active — switch to AI-TGE? (yes / no)" and proceed only on explicit confirmation.
3. **Ambiguity:** if a request could match more than one installed package by keyword, ask which to run rather than guessing.
4. **Announce every switch:** on any switch (via key or confirmation), the **FIRST line of that response MUST name the now-active package** — e.g. `Active package: AI-TGE`.
5. This engine's own marker is `tge-state.md`; sibling packages extend it the same courtesy when it is active.

---

## MANDATORY: Role Adoption

When executing this engine, adopt the role defined in:

> `#persona-qa-test-engineer` (see `.kiro/steering/persona-qa-test-engineer.md`)

**Primary:** Senior QA Engineer / Test Architect
- Think in terms of: test coverage, risk exposure, traceability, verification completeness
- Prioritize: what could go wrong if untested, blast radius of gaps, architectural risk

**Secondary:** Process Designer
- Think in terms of: repeatability, systematic derivation, structured governance
- Prioritize: consistency, auditability, non-intrusive tracking

**Sub-roles per stage:** See `.kiro/steering/ai-tge-rules.md` for the complete stage → sub-role mapping.

**Communication style:** Precise, evidence-based, risk-aware. Never vague about what's missing — always specific about which commitment lacks which test type and why it matters.

---

## Adaptive Engine Principle

AI-TGE adapts to what exists. It does NOT require the full chain to have run.

**Input modes (detect automatically):**

| Mode | What Exists | Behavior |
|------|------------|----------|
| **Full Chain** | AP + DW + aidlc-docs (AI-DLC v1 running) | Full strategy + observation |
| **Architecture Only** | AP (from AI-ADLC) but no DW or DLC | Strategy mode only — derive register from AP |
| **Brownfield** | Existing project with existing tests (no AP) | Assessment mode — map existing tests, identify gaps |
| **Observation Only** | Active AI-DLC v1 with aidlc-docs but no prior TGE run | Jump to observation — register what should be tested as you go |

Detection order:
1. Check for `tge-state.md` (resume if found)
2. Check for AP marker (`adlc-state.md`) → full chain or architecture-only
3. Check for aidlc-docs/ → observation possible
4. Check for existing test directories → brownfield assessment possible
5. None found → ask user what they have

**Graceful degradation (OR-input):** AI-TGE never blocks on a missing predecessor. AP alone produces architecture-derived strategy. Existing tests alone produce brownfield assessment. Running AI-DLC v1 alone produces observation-only tracking. Each input is additive enrichment — its absence reduces scope but never halts the engine.

---

## Two-Source Derivation Model

AI-TGE derives test requirements from TWO sources:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SOURCE 1: ARCHITECTURE PACKAGE (project-specific, from AI-ADLC)         │
│  ────────────────────────────────────────────────────────────────────────│
│  What: API contracts, component designs, ADRs, security decisions,       │
│        integration maps, data models, NFR commitments                    │
│  Result: Tailored test requirements linked to specific commitments       │
│  If absent: No architecture-specific tests (only baseline)               │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  SOURCE 2: BUILT-IN TEST GOVERNANCE BASELINE (universal minimums)        │
│  ────────────────────────────────────────────────────────────────────────│
│  What: Universal test expectations that apply to ANY project              │
│  Result: Tests that should exist regardless of what the AP says          │
│  If AP silent on topic: Baseline provides minimum coverage               │
│  If AP provides more: Baseline is enriched (both apply)                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Built-In Baseline Test Requirements (Always Applied)

| Component Type | Required Test | Rationale |
|---------------|--------------|-----------|
| Any API endpoint | Contract test (request/response schema) | API promises must be verifiable |
| Any auth flow | Security test (authn + authz verification) | Security is never optional |
| Any data mutation | Data integrity test (write → read → verify) | Data corruption is catastrophic |
| Any external integration | Integration test (connectivity + error handling) | External dependencies fail |
| Any business rule | Unit test (rule logic isolation) | Business logic is core value |
| Any user-facing workflow | Acceptance test (end-to-end happy path) | User experience must work |
| Any error handler | Negative test (error path verification) | Failure modes must be handled |
| Any configuration | Config validation test (valid + invalid inputs) | Bad config causes outages |

### Resolution Rule

```
IF AP explicitly defines a commitment for this component:
   → Derive specific test requirements (type, scope, assertions)
   → Baseline ALSO applies (additive, not replaced)

IF AP is silent on this component:
   → Baseline provides minimum test expectation
   → Flag as "baseline-only coverage" in register

IF component doesn't fit any baseline category:
   → No auto-derived requirement (but can be manually registered)
```

---

## MANDATORY: Rule Details Loading

When performing any stage, read relevant detail files from:
- `ai-tge-rule-details/common/` — cross-cutting docs
- `ai-tge-rule-details/strategy/` — Phase 1 stage details
- `ai-tge-rule-details/observation/` — Phase 2 stage details

Load `common/process-overview.md` and `common/test-taxonomy.md` at engine start.

---

## MANDATORY: Welcome Message

On first activation, load and display `common/welcome-message.md`. Display ONCE only.

---

## State Management

### State File: `.tge/tge-state.md`

```markdown
# AI-TGE State

## Engine Status
- **Mode:** {Full Chain / Architecture Only / Brownfield / Observation Only}
- **Project ID:** {immutable correlation key — read from the DW `workspace-rules.md` / carried-forward spine; persisted in every defect/coverage record — }
- **Current Phase:** {Strategy / Observation / Complete}
- **Last Stage Completed:** {1-12}
- **Last Updated:** {ISO timestamp}

## Input Sources
- **AP Location:** {path or "not available"}
- **DW Location:** {path or "not available"}
- **aidlc-docs Location:** {path or "not available"}
- **Existing Tests Location:** {path or "not detected"}

## Register Stats
- **Total Commitments Tracked:** {N}
- **Tests Required:** {N}
- **Tests Existing:** {N}
- **Tests Missing:** {N}
- **Tests Deprecated:** {N}
- **Coverage:** {N}%

## Depth Level
- **Level:** {Minimal / Standard / Comprehensive}
- **Factors:** {scoring rationale}

## AP Version
- **Last Read:** {ISO timestamp}
- **Reconciliation Needed:** {Yes / No}
```

> **Multi-project context (`OUTPUT_AND_STATE_CONTRACT.md` §11–§12):** AI-TGE operates **inside the AI-DWG-generated dev workspace**, opened as its **own Kiro IDE root** (default layout: `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/{slug}-workspace/`). All TGE paths (`.tge/`, DW location) are relative to that root and are unaffected by the multi-project restructure — the DW location resolves to the workspace root itself. Because the opened folder is one project, AI-TGE sees exactly one project **incidentally** (one folder), not via a lock (D8). **Project ID continuity (4.2):** read the immutable `Project ID` from the DW `workspace-rules.md` and the carried-forward spine `{slug}-workspace/management_framework/`; persist it in `tge-state.md` and in every coverage/defect record.

---

## Depth Calibration

| Factor | Score 1 (Low) | Score 3 (Medium) | Score 5 (High) |
|--------|--------------|-----------------|----------------|
| Component count | ≤5 components | 6-15 components | >15 components |
| Integration count | ≤2 external | 3-7 external | >7 external |
| Security surface | Basic auth only | Multi-role, API keys | OAuth, multi-tenant, PII |
| Data complexity | Simple CRUD | Multiple schemas, migrations | Event sourcing, CQRS, distributed |
| Team size | Solo / pair | 3-8 developers | >8, multiple teams |

**Thresholds:**
- Score 5-10: **Minimal** — strategy + register only
- Score 11-18: **Standard** — + coverage reports + debt scoring
- Score 19-25: **Comprehensive** — + brownfield + full traceability + reconciliation

---

## Test Taxonomy (ISTQB-Based)

### By Level

| Level | What It Verifies | Scope |
|-------|-----------------|-------|
| **Unit** | Individual function/method logic | Single component |
| **Integration** | Interaction between components/services | 2+ components |
| **System** | End-to-end behavior of complete system | Full stack |
| **Acceptance** | Business requirements met from user perspective | User workflow |

### By Type

| Type | Focus | Examples |
|------|-------|---------|
| **Functional** | Correct behavior | Business logic, workflows, calculations |
| **Non-Functional** | Quality attributes | Performance, security, accessibility, reliability |
| **Structural** | Internal code quality | Coverage, complexity, architecture conformance |

### Derived Test Mapping

| AP Artifact | Test Level | Test Type | Register Entry |
|-------------|-----------|-----------|---------------|
| API contract | Integration | Functional | Contract test per endpoint |
| Security decision (ADR) | System | Non-Functional | Security test per auth flow |
| Component design | Unit | Functional | Unit tests per business rule |
| Integration map | Integration | Functional | Integration test per external |
| NFR commitment (performance) | System | Non-Functional | Performance test per SLA |
| Data model | Unit + Integration | Functional | Data integrity test per entity |
| User story | Acceptance | Functional | Acceptance test per criterion |

---

## Risk-Based Test Prioritization

### Scoring Formula

Each missing test is scored on 4 factors (1-5 each):

| Factor | What It Measures | Score 1 | Score 5 |
|--------|-----------------|---------|---------|
| **Architectural Risk** | Impact if this goes untested | Low impact, easily caught manually | Critical path, catastrophic if broken |
| **Blast Radius** | How many things break if this fails | Isolated, single component | Cross-system, affects all users |
| **Logic Complexity** | How likely a bug exists here | Simple CRUD, trivial logic | Complex algorithms, state machines |
| **Change Frequency** | How often this code changes | Stable, rarely touched | Active development, frequent changes |

**Composite Score:** Risk × Blast × Complexity × Frequency = 1-625

**Buckets:**
- **Critical (400-625):** Test immediately — high risk of production failure
- **High (150-399):** Test within current sprint — significant exposure
- **Medium (50-149):** Test within next 2 sprints — manageable risk
- **Low (1-49):** Test when convenient — minimal exposure

---

# 🔵 STRATEGY PHASE

**Purpose:** Determine WHAT must be tested and WHY
**Trigger:** User invokes AI-TGE (first time or strategy refresh)
**Output:** Test Strategy + Test Register (baseline) + Debt Scorecard

## Stage 1: Workspace Detection (ALWAYS EXECUTE)

1. Load `strategy/workspace-detection.md`
2. Detect input mode (Full Chain / Architecture Only / Brownfield / Observation Only)
3. Locate AP, DW, aidlc-docs, existing tests
4. Initialize `.tge/tge-state.md`
5. Determine depth level (score 5 factors)
6. Present findings and mode selection to user
7. Auto-proceed to Stage 2

## Stage 2: Architecture Reading (ALWAYS EXECUTE)

1. Load `strategy/architecture-reading.md`
2. Read AP (if available): API contracts, component designs, ADRs, security decisions, integration maps, data models, NFR commitments
3. Read DW (if available): tech stack, testing frameworks, steering rules
4. Read aidlc-docs (if available): user stories, requirements, functional designs
5. Produce: **Architecture Commitment Inventory** — every testable promise the architecture makes
6. Present inventory for review
7. Wait for approval: "Is this what was designed?"

## Stage 3: Test Requirement Derivation (ALWAYS EXECUTE)

1. Load `strategy/test-requirement-derivation.md`
2. Load `common/two-source-model.md`
3. Apply two-source derivation:
   - For each AP commitment → derive specific test requirement(s) using Derived Test Mapping
   - For each component type → apply Built-In Baseline
4. Produce: **Test Register (baseline)** — every required test linked to its source commitment
5. Each register entry includes: Commitment ID, Test Level, Test Type, Test Name, Source (AP/Baseline), Risk Score (preliminary), Status (Required)
6. Present register for review
7. Wait for approval: "Are these the right tests?"

## Stage 4: Brownfield Assessment (CONDITIONAL — if existing tests detected)

**Execute IF:** Existing test directories found in workspace
**Skip IF:** Greenfield project with no existing tests

1. Load `strategy/brownfield-assessment.md`
2. Scan test directories for existing test files
3. Map found tests to register entries (pattern matching: test names, file paths, imports)
4. Classify each register entry:
   - **Covered:** Matching test exists
   - **Uncovered:** No matching test found
   - **Orphaned:** Test exists but no matching commitment in register
5. Produce: **Brownfield Gap Map**
6. Present findings for review
7. Wait for approval: "Does this match reality?"

## Stage 5: Test Strategy Generation (ALWAYS EXECUTE)

1. Load `strategy/test-strategy-generation.md`
2. Using register + tech stack + depth level, produce **Test Strategy** document:
   - Test pyramid ratios (recommended unit:integration:system:acceptance split)
   - Test types needed for this project (which apply, which don't)
   - Testing tools/frameworks (from DW tech stack)
   - Coverage goals per level and type
   - Test data strategy
   - Automation approach
   - Entry/exit criteria per test level
3. Present strategy for review
4. Wait for approval: "Approve strategy?"

## Stage 6: Risk Scoring (ALWAYS EXECUTE)

1. Load `strategy/risk-scoring.md`
2. For each MISSING test in the register (Status = Required, not Covered):
   - Score 4 risk factors (1-5 each)
   - Calculate composite score
   - Assign bucket (Critical/High/Medium/Low)
3. Produce: **Debt Scorecard** — prioritized list of missing tests by risk
4. Save all outputs to `.tge/`
5. Update `tge-state.md` (Phase = Strategy Complete)
6. Present scorecard summary
7. Present next-step guidance:

```
━━━━ AI-TGE Strategy Phase Complete ━━━━

📊 Test Register: {n} test requirements derived
   • Architecture-derived: {n}
   • Baseline (universal): {n}
📊 Debt Scorecard: {n} Critical, {n} High, {n} Medium, {n} Low

🔀 Chain Navigation:
   • Dashboard data: type `DAT__ pdlc/tge` to update the family dashboard

⚠️ WHAT HAPPENS NEXT — Observation Phase:
   AI-TGE's Observation phase activates when AI-DLC v1 is running.
   AI-DLC v1 runs in the GENERATED workspace, not this planning session.

   To proceed:
   1. Close this planning session
   2. Open the generated workspace folder as ROOT in a fresh Kiro
      instance (or Cursor / Windsurf / Claude Code)
   3. Install AI-DLC v1 (github.com/awslabs/aidlc-workflows) — it is
      a separate product; install it yourself
   4. Install AI-TGE in that same workspace (for Observation phase)
   5. As AI-DLC v1 builds, invoke TGV__ or CVR__ to track coverage

   The test strategy, register, and debt scorecard are already saved
   in.tge/ — they'll be picked up when TGE resumes in Observation mode.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

8. If mode = Architecture Only → END (no Observation possible without AI-DLC v1)
   If mode = Full Chain and aidlc-docs already present → auto-proceed to Observation

---

# 🟢 OBSERVATION PHASE

**Purpose:** Track WHAT gets tested as features are built
**Trigger:** AI-DLC v1 is executing (aidlc-docs being populated) OR user requests coverage check
**Output:** Updated Register + Coverage Reports + Defect Log

## Stage 7: State Observation (ALWAYS EXECUTE in Observation Phase)

1. Load `observation/state-observation.md`
2. Read `aidlc-docs/aidlc-state.md` — identify completed units and stages
3. For each newly completed unit:
   - Check if unit's required tests now exist in source code
   - Update register entry status: Required → Exists / Still Missing
4. Update `.tge/tge-state.md` with observation results
5. No gate — continuous operation

## Stage 8: Story Acceptance Mapping (CONDITIONAL — if user stories exist)

**Execute IF:** `aidlc-docs/inception/user-stories/` contains story files
**Skip IF:** No user stories in aidlc-docs

1. Load `observation/story-acceptance-mapping.md`
2. Read user stories and extract acceptance criteria
3. For each acceptance criterion → register as Acceptance Test requirement
4. Link to existing register entries where overlap exists (don't duplicate)
5. Update register with new story-derived entries
6. No gate — continuous operation

## Stage 9: Coverage Reporting (ALWAYS EXECUTE in Observation Phase)

1. Load `observation/coverage-reporting.md`
2. Generate coverage report with multiple views:
   - **By Commitment:** Which AP commitments have all required tests?
   - **By Component:** Which components are fully tested?
   - **By Test Type:** What's the unit/integration/system/acceptance distribution?
   - **By Risk Level:** Are Critical-risk gaps being addressed first?
3. Calculate overall coverage percentage (tests existing / tests required)
4. Produce: **Coverage Report** (saved to `.tge/coverage-report.md`)
5. Present summary to user
6. Wait for review: "Coverage acceptable?"

## Stage 10: Architecture Reconciliation (CONDITIONAL — if AP changed)

**Execute IF:** AP has been modified since last `tge-state.md` read (timestamp comparison)
**Skip IF:** AP unchanged since last strategy run

1. Load `observation/architecture-reconciliation.md`
2. Detect AP delta (new components, removed components, changed contracts)
3. For each change:
   - New commitment → register NEW required tests
   - Removed commitment → mark tests as DEPRECATED (don't delete)
   - Changed contract → flag existing tests for REVIEW
4. Produce delta summary: additions, deprecations, reviews needed
5. Present for approval (non-destructive — proposes, doesn't auto-apply)
6. Wait for approval: "Accept register changes?"

## Stage 11: Defect Logging (CONDITIONAL — when defects are reported)

**Execute IF:** User reports a defect or test failure is detected
**Skip IF:** No defects reported

1. Load `observation/defect-logging.md`
2. Capture defect details:
   - Defect ID (auto-generated: DEF-NNN)
   - Severity (Critical / High / Medium / Low)
   - Category (Functional / Performance / Security / Data / Integration)
   - Linked Test (which test caught it, or "manual discovery")
   - Linked Component (which architectural component)
   - Linked Story (which user story, if applicable)
   - Root Cause (once determined)
   - Status (Open / Investigating / Fixed / Verified / Closed)
3. Update defect log (`.tge/defect-log.md`)
4. No gate — continuous operation

## Stage 12: Debt Reassessment (ALWAYS EXECUTE after coverage report or reconciliation)

1. Load `observation/debt-reassessment.md`
2. Re-score all missing tests (factors may have changed since initial scoring)
3. Update debt scorecard with current priorities
4. Highlight changes: "Test X moved from Medium → Critical because component is now in active development"
5. Update `.tge/debt-scorecard.md`
6. No gate — auto-update

---

## Key Principles

- **Govern, don't write.** AI-TGE identifies what tests must exist and tracks coverage. It does NOT write test code.
- **Architecture-driven.** Test requirements are derived from architectural commitments, not invented ad-hoc.
- **Risk-aware.** Not all missing tests are equal — prioritize by architectural risk and blast radius.
- **Non-destructive.** Reconciliation proposes changes; brownfield assessment maps without modifying. Never delete.
- **Two-source coverage.** Even if the AP is thin, universal baselines ensure minimum test governance.
- **Observable state.** Everything is tracked in `.tge/` — progress, coverage, debt, defects. Fully auditable.
- **Silent when complete.** If all required tests exist and pass, AI-TGE has nothing to report. Only speak when gaps exist.

---

## Output Directory Structure

```
<workspace-root>/
└──.tge/
    ├── tge-state.md              ← Engine state + progress tracking (MARKER FILE)
    ├── test-strategy.md          ← Test approach, pyramid, tools, goals
    ├── test-register.md          ← Master list: commitment → test → status
    ├── coverage-report.md        ← Multi-view coverage analysis
    ├── debt-scorecard.md         ← Prioritized missing tests by risk
    └── defect-log.md             ← Structured defect tracking
```

---

## Boundary Statement

**AI-TGE is NOT:**
- A test runner (doesn't execute tests)
- A test writer (doesn't generate test code)
- A CI/CD tool (doesn't connect to pipelines)
- A replacement for AI-GCE (GCE governs code compliance; TGE governs test completeness)
- A replacement for AI-DLC v1's Build-and-Test stage (that generates test instructions; TGE governs whether those instructions are sufficient)

**AI-TGE IS:**
- A test governance engine that knows what tests SHOULD exist
- A coverage tracker that measures architectural commitment verification
- A risk scorer that prioritizes which missing tests matter most
- An observer that watches the build and maintains test accountability

---

## Post-Workflow: Agent Installation (ALWAYS EXECUTE)

After the Strategy phase completes (or at any point during AI-TGE execution), install the AI-TGE governance agents into the destination workspace. This step is **automatic** — no user interaction required.

### What Gets Installed

| Artifact | Destination | Action |
|----------|-------------|--------|
| `test-governance-agent.md` | `.kiro/agents/` | Copy from `templates/agents/` |
| `coverage-review-agent.md` | `.kiro/agents/` | Copy from `templates/agents/` (if Observation phase active) |
| Shortcut rules block | `.kiro/steering/workspace-rules.md` | Append `<!-- BEGIN AI-TGE AGENT SHORTCUTS -->` block (or replace if exists) |
| Agent registry entries | `.governance/AGENT_REGISTRY.md` | Create file if absent; append AI-TGE entries if exists |
| Agent guide section | `.governance/AGENT-GUIDE.md` | Create file if absent; append AI-TGE section if exists |

### Installation Logic

1. **Agent files:** Copy `templates/agents/test-governance-agent.md` to `.kiro/agents/test-governance-agent.md`. If Observation phase is active, also copy a `coverage-review-agent.md` (derived from the test-governance-agent template with coverage-specific checks). Populate `{version}` with current AI-TGE version and `{ISO-date}` with today's date.

2. **Shortcut block:** Check `.kiro/steering/workspace-rules.md` for `<!-- BEGIN AI-TGE AGENT SHORTCUTS -->` marker:
   - If found → replace the block (between BEGIN and END markers)
   - If not found → append the block from `templates/agents/shortcut-rules-block.md`

3. **Agent registry:** Check for `.governance/AGENT_REGISTRY.md`:
   - If absent → create with header + AI-TGE entries (TGE-AG-01, TGE-AG-02)
   - If exists → append AI-TGE entries using `TGE-AG-{NN}` IDs
   - Entries: `| TGE-AG-01 | test-governance-agent | Process | TGV__ | 1 | AI-TGE | Active | {date} |`
   - `| TGE-AG-02 | coverage-review-agent | Process | CVR__ | 1 | AI-TGE | Active | {date} |`

4. **Agent guide:** Check for `.governance/AGENT-GUIDE.md`:
   - If absent → create with header + AI-TGE section from `templates/agents/agent-guide.md`
   - If exists → append AI-TGE section (between `<!-- BEGIN AI-TGE AGENT GUIDE SECTION -->` markers)

### Self-Sufficiency Rule (AGENT_GOVERNANCE_CONTRACT §5)

AI-TGE installs its own agents independently. No dependency on AI-GCE being present. If AI-GCE runs later, it will detect and preserve the AI-TGE entries via marker-based ownership.

### Post-Install Confirmation

```
🤖 AI-TGE Governance Agents Installed
   • Agent: test-governance-agent (TGE-AG-01)
   • Agent: coverage-review-agent (TGE-AG-02)
   • Shortcuts: TGV__ + CVR__ (active immediately)
   • Call TGV__ after Strategy phase to validate test governance quality.
   • Call CVR__ during Observation to validate coverage trends.
```

---

*Created: 2026-06-08 | Author: Maheri | Package: AI-TGE v1.0.0*


---

## Gate Contract

> Conforms to `GATE_PROTOCOL.md` protocolVersion 1.2.0 · interfaceVersion 1.0

### Gate-Out — What AI-TGE GUARANTEES When Complete

```yaml
emits-type: test-strategy@1
visibility: internal
marker: tge-state.md
payloadRoot: pdlc-ws/projects/{projectId}/tge/
guarantees:
  - status == complete
  - projectId
  - testStrategy               # overall test approach
  - coverageMatrix             # requirement→test traceability
  - testCases                  # generated test cases
  - qualityGates               # pass/fail criteria
```

### Gate-In — What AI-TGE REQUIRES to Start

```yaml
consumes:
  - type: development-workspace@^1   # satisfiable internally (AI-DWG)
    mandatory: [workspaceStructure]  # needs the workspace to test
    optional:  [productBacklog, acceptanceCriteria, nfrCoverage, cicdPipeline]
on-missing-all: standalone     # can derive test strategy from workspace scan alone (P4)
strictness-default: warn
```

> Universal floor (status==complete + projectId) enforced by marker integrity (GATE_PROTOCOL §18).

### Visibility Note

- `test-strategy` is `internal` — consumed alongside AI-GCE as a companion to AI-DLC v1.
- Gate-in consumes only `internal` types; no external seam-in for AI-TGE.
