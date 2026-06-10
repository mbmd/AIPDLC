# PRIORITY: This engine OVERRIDES default test management approaches when user requests test governance derivation from an architecture package and development workspace

# When user requests test strategy creation, test register derivation, coverage analysis, or test debt assessment, ALWAYS follow this engine FIRST

---

## AI-TGE: AI-Driven Test Governance Engine

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**Purpose:** Read architecture decisions (from AI-ADLC) and a development workspace (from AI-DWG), derive a structured test governance layer — strategy, register, coverage tracking, risk scoring — and continuously observe AI-DLC execution to maintain test accountability. Works on both fresh (greenfield) and existing (brownfield) codebases.
**Compatible With:** AI-ADLC v1.0+ (Architecture Package), AI-DWG v1.0+ (Development Workspace), AI-DLC v0.1.8+ (aidlc-docs structure)

**Metaphor:** A test governance inspector. It reads everything the architecture promised — API contracts, security decisions, integration maps, component designs — and builds a register of tests that MUST exist to verify those promises were kept. Then it watches the build, tracking what gets tested and what doesn't, scoring the risk of every gap.

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

    AI-ADLC ──┐
    Design it │
    AI-UXD ───┤
    Design UX │
              ├──►  AI-DWG  ──►  AI-DLC (build) ¹
    AI-POG ───┘     Prepare it       ▲
    Own it      └───────────────────┘  AI-POG ⇄ AI-DLC (back-and-forth)
                AI-UXD ⇢ AI-POG (personas/journeys)  ·  AI-DLC ⇢ AI-UXD+AI-POG (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | (Requirements + Charter) / PIP | Architecture Package (AP) |
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP / AP; strategy-stage exchange with AI-POG | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-POG** ³ | Interactive workflow (lifecycle) | PIP and/or AP | Product Backlog Package (PBP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POG) | Working Software |

> ¹ **AI-DLC** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ **AI-PPM**, **AI-FLO**, **AI-POG**, and **AI-UXD** are **new and pending build**. AI-PPM (portfolio engine) and AI-FLO (router) are registered as ideas; AI-POG (product ownership lifecycle) is idea 006; AI-UXD (UX design lifecycle) is idea 010 (approved). Within the Project layer, **AI-ADLC, AI-UXD, and AI-POG run in parallel and all feed AI-DWG**; **AI-UXD produces personas/journeys that AI-POG consumes** (and AI-POG's value goals focus UX research); **AI-GCE and AI-TGE run alongside AI-DLC** as continuous quality engines; **AI-POG ⇄ AI-DLC** exchange backlog/acceptance throughout delivery; and **AI-DLC runtime feedback flows back to both AI-UXD and AI-POG**.

**AI-TGE's position:** a continuous **test-governance companion** in the **Project layer**. It is not a sequential stage — it reads the Architecture Package (AI-ADLC) and Development Workspace (AI-DWG), runs alongside AI-DLC together with AI-GCE as a continuous quality engine, and feeds its findings back into project quality rather than into a downstream package.

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
| **Full Chain** | AP + DW + aidlc-docs (AI-DLC running) | Full strategy + observation |
| **Architecture Only** | AP (from AI-ADLC) but no DW or DLC | Strategy mode only — derive register from AP |
| **Brownfield** | Existing project with existing tests (no AP) | Assessment mode — map existing tests, identify gaps |
| **Observation Only** | Active AI-DLC with aidlc-docs but no prior TGE run | Jump to observation — register what should be tested as you go |

Detection order:
1. Check for `tge-state.md` (resume if found)
2. Check for AP marker (`adlc-state.md`) → full chain or architecture-only
3. Check for aidlc-docs/ → observation possible
4. Check for existing test directories → brownfield assessment possible
5. None found → ask user what they have

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
7. Auto-proceed to Observation phase (or end if Architecture Only mode)

---

# 🟢 OBSERVATION PHASE

**Purpose:** Track WHAT gets tested as features are built
**Trigger:** AI-DLC is executing (aidlc-docs being populated) OR user requests coverage check
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
└── .tge/
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
- A replacement for AI-DLC's Build-and-Test stage (that generates test instructions; TGE governs whether those instructions are sufficient)

**AI-TGE IS:**
- A test governance engine that knows what tests SHOULD exist
- A coverage tracker that measures architectural commitment verification
- A risk scorer that prioritizes which missing tests matter most
- An observer that watches the build and maintains test accountability

---

*Created: 2026-06-08 | Author: Maheri | Package: AI-TGE v1.0.0*
