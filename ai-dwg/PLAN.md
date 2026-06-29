# AI-DWG — AI-Driven Workspace Generator

## Plan Document

**Status:** Complete
**Date:** 2026-06-04 (Updated: 2026-06-06)
**Author:** Maheri
**Compatible With:** AI-ADLC v1.0 (core) + v1.1 (extensions)

---

## The AI-* Family

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

---

## What AI-DWG Is

A **one-time generator** (not a lifecycle) that reads an Architecture Package produced by AI-ADLC and transforms it into a complete, ready-to-code development workspace — including Kiro steering files, project instructions, repository structure, configuration files, and development setup.

**Compatible with AI-ADLC v1.1 extensions:** When AI-ADLC extensions (DDD Tactical, Microservices, BFF, Event Sourcing/CQRS, Resilience Patterns, Feature Flags) were active during architecture design, AI-DWG detects them via `adlc-state.md` and enriches the generated workspace accordingly — producing additional conditional steering files and deeper pattern-specific rules.

**Metaphor:** Architecture-to-Workspace compiler. Blueprint → Construction site.

---

## What AI-DWG Produces

```
{project-root}/
├── .kiro/
│   └── steering/
│       ├── workspace-rules.md              ← Core rules (from AP principles)
│       ├── architecture-principles.md      ← From AP vision
│       ├── tech-stack.md                   ← From AP technology decisions
│       ├── coding-standards.md             ← Derived from tech + principles
│       ├── project-governance.md           ← Sprint cadence, DoD, gates
│       ├── scope-and-risks.md              ← From PIP scope + AP constraints
│       ├── session-governance.md           ← AI-DLC v1 session rules
│       ├── role-isolation.md               ← Who does what in AI-DLC v1 workflow
│       ├── domain-context.md              ← Ubiquitous language, bounded contexts, domain rules
│       ├── multi-tenancy.md                ← From AP multi-tenancy (conditional)
│       ├── api-standards.md                ← From AP API architecture
│       ├── api-versioning.md              ← Version lifecycle, breaking changes (conditional)
│       ├── security-rules.md               ← From AP security architecture
│       ├── module-structure.md             ← From AP component design
│       ├── testing-strategy.md             ← Derived from quality attributes
│       ├── database-rules.md              ← From AP data architecture
│       ├── naming-conventions.md           ← Derived from tech + patterns
│       ├── git-workflow.md                 ← From AP infrastructure/deployment
│       ├── error-handling.md              ← Error patterns, result pattern, API errors
│       ├── resilience-standards.md        ← Retry, circuit breaker, timeout (conditional)
│       ├── observability-logging.md       ← Log levels, format, required points
│       ├── observability-tracing.md       ← Span naming, instrumentation (conditional)
│       ├── observability-sensitive.md     ← What NEVER to log; masking rules
│       ├── performance-standards.md       ← Response budgets, measurement (conditional)
│       ├── workflow-engine.md             ← Workflow patterns (conditional)
│       ├── frontend-standards.md          ← Component patterns, accessibility (conditional)
│       ├── event-sourcing.md             ← Event store, projections, CQRS (conditional — ADLC extension)
│       └── feature-flags.md              ← Flag architecture, rollout strategies (conditional — ADLC extension)
│
├── PROJECT_INSTRUCTIONS.md                 ← Master developer guide
├── DEFINITION_OF_DONE.md                   ← Quality criteria for "done"
├── CONTRIBUTING.md                         ← Commit strategy, PR process, branching
├── CICD_GUIDE.md                           ← CI/CD pipeline setup, quality gates, deployment
├── TEAM_AGREEMENTS.md                      ← Operating rules (autonomy modes, ownership, review standards)
├── ONBOARDING.md                           ← New developer onboarding checklist
├── .github/
│   └── pull_request_template.md            ← PR template with checklist (or platform equivalent)
│
├── templates/                              ← Planning templates for team use
│   ├── session-planning.md                 ← AI-DLC v1 session planning template
│   ├── sprint-planning.md                  ← Sprint structure and capacity template
│   └── estimation-guide.md                 ← Size estimation (S/M/L/XL) with multipliers
│
├── .gitignore                              ← Tech-stack appropriate
├── .editorconfig                           ← Code style enforcement
├── docker-compose.yml                      ← Skeleton (from AP infrastructure)
├── CODEOWNERS                              ← From AP component ownership
├── README.md                               ← Project README skeleton
├── management_framework/                   ← Development phase governance registers
│   ├── Decision_Log.md                     ← Implementation decisions (below ADR threshold)
│   ├── Change_Log.md                       ← Scope/approach changes during build
│   ├── Issue_Log.md                        ← Blockers and problems
│   └── Lessons_Learned.md                  ← Sprint/session insights
└── {src-structure}/                        ← Folder layout per AP component design
```

### Conditional Steering Files

Not every project gets every steering file. AI-DWG generates ONLY what the Architecture Package justifies:

| Steering File | Generated IF (AP contains) |
|--------------|---------------------------|
| `multi-tenancy.md` | Multi-Tenancy Architecture document exists |
| `api-versioning.md` | API Architecture specifies multi-version strategy |
| `resilience-standards.md` | Microservices / >3 external integrations / distributed system / **Microservices or Resilience extension active** |
| `observability-tracing.md` | Infrastructure doc specifies distributed tracing tool / **Microservices extension active** |
| `performance-standards.md` | Quality Attributes include specific latency targets (p95/p99) |
| `workflow-engine.md` | Component Design includes workflow/state-machine component |
| `frontend-standards.md` | Container Design includes SPA/UI containers / **BFF extension active** |
| `event-sourcing.md` | **Event Sourcing/CQRS extension active** in AI-ADLC |
| `feature-flags.md` | **Feature Flags extension active** in AI-ADLC |
| All others (19 files) | ALWAYS generated — core to any project |

### Extension-Aware Generation (AI-ADLC v1.1+)

When AI-ADLC extensions were active during architecture design, AI-DWG enriches its output:

| Extension (if active) | Impact on Generation |
|-----------------------|---------------------|
| **DDD Tactical** | `domain-context.md` enriched with aggregate boundaries, value objects, ACL definitions; `module-structure.md` aligned to aggregates; `naming-conventions.md` includes DDD naming |
| **Microservices** | `resilience-standards.md` always generated (full detail); `observability-tracing.md` always generated; `module-structure.md` reflects service boundaries |
| **BFF Pattern** | `frontend-standards.md` always generated; `api-standards.md` includes BFF-specific endpoint conventions |
| **Event Sourcing / CQRS** | `event-sourcing.md` generated; `database-rules.md` enriched with event store patterns and projection rules |
| **Resilience Patterns** | `resilience-standards.md` always generated with extended catalog (circuit breaker, bulkhead, timeout, graceful degradation) |
| **Feature Flags** | `feature-flags.md` generated with flag architecture, rollout strategies, and lifecycle rules |

**Detection mechanism:** Read `adlc-state.md` → check `Enabled Extensions` section → load corresponding extension-enrichment mapping files.

---

## How It Works (Transformation, Not Lifecycle)

### Two Operating Modes

| Mode | When Used | Behavior |
|------|-----------|----------|
| **Full Generation** | First time — workspace doesn't exist | Generate everything from Architecture Package |
| **Delta Reconciliation** | Architecture changed during development | Read updated AP → diff against current workspace → propose changes only |

### Mode 1: Full Generation

```
┌─────────────────────────────────────────────────────────────────┐
│  AI-DWG FULL GENERATION FLOW                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  STEP 1: READ                                                     │
│  ─────────────                                                    │
│  Load Architecture Package from AI-ADLC output                    │
│  • Architecture Vision & Principles                               │
│  • Technology Stack + ADRs                                        │
│  • Container & Component Design (C4 L2 + L3)                     │
│  • API Architecture                                               │
│  • Security Architecture                                          │
│  • Data Architecture                                              │
│  • Multi-Tenancy (if applicable)                                  │
│  • Infrastructure & Deployment                                    │
│  • adlc-state.md (detect active extensions from v1.1)             │
│  • Extension-specific ADRs and design artifacts (if extensions    │
│    were active: DDD, Microservices, BFF, Event Sourcing,          │
│    Resilience, Feature Flags)                                     │
│                                                                   │
│  STEP 2: MAP                                                      │
│  ────────────                                                     │
│  Transform each AP artifact → workspace artifact(s)               │
│  • Principles → workspace-rules.md                                │
│  • Tech Stack → tech-stack.md + .gitignore + docker-compose       │
│  • C4 L3 → folder structure + module-structure.md + CODEOWNERS    │
│  • C4 L3 Bounded Contexts → domain-context.md (ubiquitous language)│
│  • API Arch → api-standards.md                                    │
│  • Security → security-rules.md                                   │
│  • Data Arch → database-rules.md                                  │
│  • Multi-Tenancy → multi-tenancy.md                               │
│  • Infrastructure → git-workflow.md + deployment configs           │
│  • Quality Attributes → testing-strategy.md + DEFINITION_OF_DONE  │
│  • Team Context → role-isolation.md + TEAM_AGREEMENTS             │
│  • Methodology → session-governance.md + templates/               │
│  • Governance → CONTRIBUTING.md + PR template + ONBOARDING        │
│  • Infrastructure (observability) → observability-*.md            │
│  • Component Design (error handling) → error-handling.md          │
│  • Integration Arch (resilience) → resilience-standards.md        │
│  • Quality Attrs (performance) → performance-standards.md         │
│  • Container Design (frontend) → frontend-standards.md            │
│  • Extension: DDD → enriched domain-context.md + module-structure │
│  • Extension: Microservices → resilience + tracing (force-gen)    │
│  • Extension: BFF → frontend-standards (force-gen) + api enriched │
│  • Extension: Event Sourcing → event-sourcing.md + database enrich│
│  • Extension: Resilience → resilience-standards (full catalog)    │
│  • Extension: Feature Flags → feature-flags.md                    │
│                                                                   │
│  STEP 3: GENERATE                                                 │
│  ────────────────                                                 │
│  Produce all files with actual content (not placeholders)         │
│  • Steering files populated from AP decisions                     │
│  • Repo structure created per C4 L3 modules                       │
│  • Config files generated per technology selections               │
│  • PROJECT_INSTRUCTIONS.md compiled as master guide               │
│                                                                   │
│  STEP 4: VALIDATE                                                 │
│  ───────────────                                                  │
│  Cross-check generated workspace against AP                       │
│  • All principles encoded in steering?                            │
│  • All constraints reflected in rules?                            │
│  • Folder structure matches C4 L3?                                │
│  • Technology labels consistent?                                  │
│  • No contradictions between generated files?                     │
│                                                                   │
│  STEP 5: OUTPUT                                                   │
│  ────────────                                                     │
│  Complete workspace ready for:                                    │
│  • git init                                                       │
│  • AI-DLC v1 workflow start                                          │
│  • Team onboarding                                                │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Mode 2: Delta Reconciliation

Triggered when architecture changes during AI-DLC v1 execution (new ADRs, principle amendments, module additions, technology changes).

```
┌─────────────────────────────────────────────────────────────────┐
│  AI-DWG DELTA RECONCILIATION FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  TRIGGER: User says "Architecture changed" or points to          │
│           updated ADR / modified AP artifact                      │
│                                                                   │
│  STEP 1: READ CURRENT STATE                                       │
│  ──────────────────────────                                       │
│  Load existing workspace:                                         │
│  • Current .kiro/steering/ files (with team's customizations)     │
│  • Current folder structure                                       │
│  • Current configs (docker-compose, .gitignore, etc.)             │
│                                                                   │
│  STEP 2: READ UPDATED ARCHITECTURE                                │
│  ─────────────────────────────────                                │
│  Load the changed artifact(s):                                    │
│  • New or updated ADR(s)                                          │
│  • Modified architecture document(s)                              │
│  • Or: full AP re-read if multiple changes                        │
│                                                                   │
│  STEP 3: DIFF — Identify What Changed                             │
│  ────────────────────────────────────                             │
│  Compare AP state vs. workspace state:                            │
│  • New principle added? → workspace-rules.md needs update         │
│  • Technology changed? → tech-stack.md + docker + .gitignore      │
│  • Module added/split? → new folder + module-structure.md         │
│  • Module removed? → flag (don't delete — team confirms)          │
│  • API convention changed? → api-standards.md                     │
│  • Security model changed? → security-rules.md                   │
│  • New integration? → may need new steering section               │
│                                                                   │
│  STEP 4: PROPOSE CHANGES (Don't auto-apply)                       │
│  ───────────────────────────────────────────                      │
│  Present to user:                                                 │
│  "Architecture change detected: {what changed}                    │
│                                                                   │
│   Affected workspace files:                                       │
│   • {file 1} — {what changes}                                     │
│   • {file 2} — {what changes}                                     │
│   • {file 3} — {what changes}                                     │
│                                                                   │
│   Apply these changes?                                            │
│   (a) Apply all                                                   │
│   (b) Review each change individually                             │
│   (c) Skip — I'll handle manually"                                │
│                                                                   │
│  STEP 5: MERGE (Preserve Customizations)                          │
│  ────────────────────────────────────────                         │
│  For each affected file:                                          │
│  • Identify architecture-sourced sections vs. team-added content  │
│  • Update ONLY architecture-sourced sections                      │
│  • Preserve team's additions, comments, and customizations        │
│  • If conflict: present both versions; user picks                 │
│                                                                   │
│  STEP 6: UPDATE TRACKING                                          │
│  ────────────────────────                                         │
│  • Log what changed and why (in a reconciliation log)             │
│  • Note which ADR triggered the update                            │
│  • Mark workspace as "reconciled with AP as of {date}"            │
│                                                                   │
│  STEP 7: SIGNAL AI-GCE (If compliance engine exists)              │
│  ────────────────────────────────────────────────────             │
│  "Steering files updated. Affected files: {list}.                 │
│   AI-GCE should re-derive rules/hooks for changed files."         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Reconciliation Rules

| Rule | Description |
|------|-------------|
| **Never overwrite blindly** | Always diff first; propose changes; user approves |
| **Preserve team customizations** | Steering files may have team-added content not from AP — don't remove it |
| **Additive preferred** | Adding new content is safe; removing/changing existing content requires confirmation |
| **Track provenance** | Each section in a steering file should be traceable: "from AP" vs. "team addition" |
| **Log all reconciliations** | Maintain a reconciliation history (what changed, when, from which ADR) |
| **Don't delete modules** | If AP removes a module, flag it; don't delete folder (may have code in development) |
| **Signal downstream** | After workspace update, AI-GCE needs to re-derive affected rules |

---

## Package File Structure

> **Per Lesson 26:** The plan is summary; the core file is spec. See `ai-dwg-rules/core-generator.md` for the authoritative generation logic, output inventory, and step-by-step flows.

```
ai-dwg/
├── README.md                               ← Overview, family table, features, tenets
├── LICENSE                                 ← Apache 2.0 + Attribution
├── PLAN.md                                 ← This document (design rationale)
├── ai-dwg-rules/
│   └── core-generator.md                   ← Master generation logic (THE spec)
├── ai-dwg-rule-details/
│   ├── common/                             ← 3 files (process overview, AP reading, validation)
│   ├── mapping/                            ← 36 transformation rule files (AP → DW)
│   ├── reconciliation/                     ← 4 files (diff, merge, provenance, signaling)
│   └── templates/                          ← 48 output file templates
│       ├── steering/                       ← 29 files (19 always + 10 conditional)
│       ├── operational/                    ← 8 files
│       ├── planning/                       ← 3 files
│       ├── config/                         ← 3 files
│       └── docker-compose/                 ← 5 files (per tech stack)
└── setup/
    └── INSTALL.md                          ← Multi-platform installation guide
```

**Total package files: ~80**

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Input format | Reads AP as markdown files in a folder | AP from AI-ADLC is already structured markdown |
| Output scope | Full workspace (steering + operations + repo structure + configs + planning templates) | Developers should be able to start immediately — including knowing how to work, not just what to build |
| Technology-awareness | Templates per common tech stack (Node/Python/.NET/Java/Generic) | Different stacks need different .gitignore, docker configs, folder conventions |
| Steering file inclusion model | Follows Kiro conventions (always/fileMatch/manual) | Native integration with Kiro IDE |
| Conditional generation | Multi-tenancy, workflow engine, etc. only generated if AP includes them | Don't generate steering files for patterns the architecture doesn't use |
| Extension-awareness (v1.1) | Detect active AI-ADLC extensions via `adlc-state.md`; enrich generation accordingly | Extensions produce richer AP — workspace must reflect that richness; no manual reconfiguration needed |
| PROJECT_INSTRUCTIONS as master guide | Single entry-point document for all developers | Provides a single entry-point consolidating essential information for immediate productivity |
| Operational docs included | DoD, CONTRIBUTING, CICD_GUIDE, TEAM_AGREEMENTS, ONBOARDING, PR template | Developers need process clarity from day one — not just architecture rules |
| Planning templates included | Session planning, sprint planning, estimation guide | Team needs to plan AI-DLC v1 work immediately; templates accelerate this |
| Domain context steering | Ubiquitous language + bounded context + domain rules from C4 L3 | Prevents AI from inventing synonyms or violating domain boundaries |
| Role isolation steering | Who does what in AI-DLC v1 (Architect, Developer, QA, Security, PM) | Prevents role confusion; supports segregation of duties |
| Reconciliation mode | Non-destructive delta updates when architecture changes | Projects evolve; workspace must evolve with them without data loss |

---

## What AI-DWG Does NOT Do

- ❌ Generate application code (that's AI-DLC v1's job)
- ❌ Set up CI/CD pipelines fully (produces skeleton; team configures)
- ❌ Install dependencies (produces package.json skeleton; team runs install)
- ❌ Make architecture decisions (those are already made in AI-ADLC)
- ❌ Create governance enforcement (that's AI-GCE's job)
- ❌ Overwrite team customizations during reconciliation (merge, don't replace)
- ❌ Delete modules/folders during reconciliation (flag for user; don't auto-delete)
- ❌ Require full regeneration for small architecture changes (delta mode handles incremental updates)

---

## Interaction Model

Unlike AI-PILC/AI-ADLC (interactive lifecycles with gates), AI-DWG has two invocation modes:

### Mode 1: Initial Generation
1. **User invokes:** "Using AI-DWG, generate the development workspace from my architecture package"
2. **AI reads** the Architecture Package
3. **AI asks** 2-3 configuration questions (project name, preferred folder structure, team size)
4. **AI generates** all files in one pass
5. **AI presents** summary: "Generated {n} steering files, {m} config files, repo structure with {p} modules"
6. **Done.** User verifies and starts working.

### Mode 2: Delta Reconciliation
1. **User invokes:** "Architecture changed — reconcile the workspace" (or points to updated ADR)
2. **AI reads** updated architecture artifact(s) + current workspace state
3. **AI diffs** — identifies what changed and which workspace files are affected
4. **AI proposes** specific changes (not a full regeneration)
5. **User approves** (all, per-file, or skips)
6. **AI applies** changes preserving team customizations
7. **AI signals** AI-GCE to re-derive affected rules (if compliance engine exists)
8. **Done.** Workspace reconciled with updated architecture.

---

## Estimated Effort

| Category | Files | Complexity |
|----------|:-----:|:----------:|
| Core generator | 1 | High (orchestration logic) |
| Common docs | 3 | Medium |
| Mapping rules (core) | 17 | High (transformation logic) |
| Mapping rules (extension-enrichment) | 4 | Medium-High (enrichment logic for ADLC v1.1 extensions) |
| Reconciliation | 4 | High (diff + merge logic) |
| Steering templates | 27 | Medium (generic patterns — 19 always + 8–10 conditional) |
| Operational doc templates | 6 | Medium |
| Planning templates | 3 | Low-Medium |
| Config templates | 8 | Low-Medium |
| README + LICENSE + setup | 3 | Low |
| **Total** | **~76** | |
