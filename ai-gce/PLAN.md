# AI-GCE — AI-Driven Governance & Compliance Engine

## Plan Document (Revised)

**Status:** In Progress — core-generator.md built, gap analysis complete
**Date:** 2026-06-04 (Revised: 2026-06-06)
**Author:** Maheri
**Revision:** 3 — Gap analysis against reference implementation; expanded from architecture-only to full project governance engine; added 3-tier model, hook debounce, .compliance-state.json, non-architectural rule categories (GOV-ROLE, GOV-TT, GOV-SESSION, GOV-SPRINT, GOV-PR, GOV-CICD, GOV-DEVOPS, GOV-STEER, GOV-LOG, CM-*)

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

---

## Critical Correction: How AI-GCE Gets Its Context

### ❌ WRONG (Original Plan)
```
AI-GCE is a static framework → user manually configures file patterns, tech stack, rules to enable
```

### ❌ ALSO WRONG (Revision 2 — incomplete)
```
AI-GCE READS the AI-DWG workspace → DERIVES everything from steering files only
Problem: If steering is silent on a governance topic → no rule exists → governance gap
```

### ✅ CORRECT (This Plan — Two-Source Model)
```
AI-GCE has TWO sources for rule generation:

SOURCE 1: STEERING FILES (project-specific, from AI-DWG workspace)
  • What technology? → reads .kiro/steering/tech-stack.md
  • What modules? → reads .kiro/steering/module-structure.md
  • What API conventions? → reads .kiro/steering/api-standards.md
  • What security rules? → reads .kiro/steering/security-rules.md
  • What team topology? → reads .kiro/steering/role-isolation.md + CODEOWNERS
  • What session methodology? → reads .kiro/steering/session-governance.md
  • What CI/CD? → reads .kiro/steering/git-workflow.md

SOURCE 2: BUILT-IN GOVERNANCE KNOWLEDGE (AI-DLC methodology baseline)
  • "Spec before code" → always enforced regardless of steering
  • "Never vibe code" → always enforced
  • "Author ≠ approver" → always enforced
  • "No direct push to main" → always enforced
  • "Tests pass before merge" → always enforced
  • "No hardcoded secrets" → always enforced
  • "Migration has rollback" → always enforced
  • "Compliance log is append-only" → always enforced

Resolution: Steering enriches baseline. Steering can override baseline.
            Silent steering = baseline-only (still get governance floor).
```

**Why two sources:**
- Architecture rules are 100% steering-derived (no api-standards.md = no API rules — correct)
- Governance rules have universal minimums ("author ≠ approver" is true for ALL projects)
- A team that didn't run the full chain still gets baseline governance value
- This matches the reference implementation (310+ rules, many are methodology constants)

---

## What AI-GCE Is

A **full project governance engine** (not just architecture compliance) that reads an AI-DWG workspace — which encodes architecture decisions, team topology, session methodology, role agreements, and operational governance from AI-ADLC — and produces a **tailored enforcement layer**: rules, hooks, agents, and logging specific to that project's technology, architecture, team structure, and process.

**Metaphor:** A project governance inspector. It reads everything posted on the walls — architecture blueprints, team agreements, role charts, process rules, and methodology commitments — and builds an automated compliance system calibrated to watch for violations of ALL of those commitments, not just the architectural ones.

---

## The Derivation Chain

```
AI-ADLC Architecture Package
         │
         │  Contains: principles, tech stack, C4 L3, API arch,
         │  security arch, data arch, multi-tenancy, infrastructure,
         │  team context, methodology, governance decisions
         │
         ▼
AI-DWG Workspace
         │
         │  Contains (as steering files + structure + operational docs):
         │
         │  ARCHITECTURAL:
         │  • tech-stack.md → exact technologies + versions
         │  • module-structure.md → module names + boundaries + ownership
         │  • api-standards.md → API conventions
         │  • security-rules.md → auth model + encryption
         │  • database-rules.md → schema patterns + migration rules
         │  • multi-tenancy.md → isolation model (if exists)
         │  • naming-conventions.md → file/folder/class patterns
         │  • architecture-principles.md → guiding principles
         │  • error-handling.md → error patterns + Result pattern
         │  • observability-logging.md → logging rules
         │  • observability-sensitive.md → data masking rules
         │  • domain-context.md → ubiquitous language, bounded contexts
         │
         │  NON-ARCHITECTURAL (team + methodology + governance):
         │  • role-isolation.md → roles, segregation of duties, approval chains
         │  • session-governance.md → AI-DLC session rules, never-vibe-code
         │  • project-governance.md → sprint cadence, phase gates, quality gates
         │  • git-workflow.md → branching, CI/CD, deployment strategy
         │  • testing-strategy.md → coverage targets, CI/CD thresholds
         │  • scope-and-risks.md → boundaries, risk-aware enforcement
         │  • TEAM_AGREEMENTS.md → PR process, commit conventions, ownership
         │  • CODEOWNERS → module-to-team mapping, review ownership
         │  • DEFINITION_OF_DONE.md → quality criteria per phase gate
         │  • Folder structure → actual module layout
         │
         ▼
AI-GCE Reads ALL Of The Above → GENERATES:
         │
         ├── rules/ → Compliance rules covering BOTH architecture AND governance
         │   ARCHITECTURAL:
         │   • Architecture compliance, API-first, security, data governance,
         │     module boundaries, naming, error handling, logging, domain context
         │   NON-ARCHITECTURAL:
         │   • Phase gates (PG-*), session methodology (GOV-SESSION),
         │     role isolation (GOV-ROLE), team topology (GOV-TT),
         │     sprint governance (GOV-SPRINT), PR governance (GOV-PR),
         │     CI/CD quality gates (GOV-CICD), DevOps (GOV-DEVOPS),
         │     steering quality (GOV-STEER), compliance log (GOV-LOG),
         │     change management (CM-*) — Tier 3
         │
         ├── hooks/ → Hook JSON files split by timing sensitivity:
         │   Tier A (fileEdited): security-critical (secrets, tenant, migration)
         │   Tier B (agentStop): advisory (DDD purity, cross-module, coverage)
         │   Other: promptSubmit (session-discipline), postTask (governance),
         │          userTriggered (audit, PR checklist)
         │
         ├── agents/ → Two agent specs:
         │   • compliance-audit-agent.md (9-step with scoring, dashboard, tiers)
         │   • project-init-agent.md (5 questions → full scaffold)
         │
         ├── .compliance-state.json → Tier tracking, readiness, score history
         │
         └── compliance-log/ → JSONL schema (CHECK/EXCEPTION/REMEDIATION/AUDIT)
```

---

## How AI-GCE Works (The Flow)

### Four Operating Modes

| Mode | When Used | Behavior |
|------|-----------|----------|
| **Full Generation** | First time — no compliance layer exists yet | Read workspace → generate full rules + hooks + agents (Tier 1 active) |
| **Re-Derivation** | Workspace steering files changed (after AI-DWG reconciliation) | Read changed files → regenerate ONLY affected rules + hooks |
| **Brownfield Adoption** | Workspace has `brownfield-patterns.md` | Baseline scan → incremental enforcement → new-code-only hooks |
| **Tier Activation** | Team ready for next compliance tier | Verify readiness → activate new rules + hooks → re-audit |

### Mode 1: Full Generation

The full generation flow has 12 steps. See `core-generator.md` STEP 1–12 for the authoritative detailed specification.

**Summary:**
1. Read workspace (all steering + operational docs + folder structure)
2. Determine applicable rule categories (two-source: baseline + steering-enriched)
3. Generate rules (architecture + governance, tier-tagged)
4. Generate hooks (debounce-tiered, phase-aware, compliance-logging in every prompt)
4b. Generate phase/role-aware steering (optional enrichment — fileMatch only)
5. Generate audit agent + project-init agent
6. Initialize `.compliance-state.json` (Tier 1)
7. Generate compliance logging infrastructure (JSONL schema)
8. Generate compliance dashboard template
9. Generate hook INSTALL-GUIDE (tier-based roadmap)
10. Generate COMPLIANCE_README
11. Validate (cross-check all output, context budget, phase-awareness)
12. Present summary with tier status

---

## What AI-GCE Produces (Per Project)

Generated INTO the development workspace:

```
{project-root}/
├── .kiro/
│   ├── steering/                         ← Already exists (from AI-DWG)
│   │   ├── [compliance-phase-context.md] ← GENERATED by AI-GCE (Step 4b, fileMatch)
│   │   ├── [compliance-code-rules.md]    ← GENERATED by AI-GCE (Step 4b, fileMatch)
│   │   ├── [compliance-test-conventions.md] ← IF team ≥ 3 (Step 4b, fileMatch)
│   │   └── [compliance-api-conventions.md]  ← IF team ≥ 3 (Step 4b, fileMatch)
│   │
│   └── hooks/                            ← GENERATED by AI-GCE
│       ├── INSTALL-GUIDE.md              ← Tier-based installation roadmap
│       │── — TIER A (fileEdited — security-critical) —
│       ├── security-gate-check.json      ← 🔴 Essential
│       ├── migration-safety.json         ← 🔴 Essential
│       ├── sensitive-data-check.json     ← 🔴 Essential (secrets + PII, sessionDedup)
│       ├── [tenant-isolation-check.json] ← 🔴 Essential (IF multi-tenancy)
│       │── — TIER B (agentStop — advisory) —
│       ├── domain-layer-purity.json      ← 🟠 High-value
│       ├── module-boundary-check.json    ← 🟠 High-value
│       ├── coverage-check.json           ← 🟠 High-value
│       ├── naming-check.json             ← 🟡 Advisory
│       ├── documentation-reminder.json   ← 🟡 Advisory
│       ├── steering-quality-check.json   ← 🟡 Advisory
│       │── — OTHER EVENT TYPES —
│       ├── session-discipline.json       ← promptSubmit (🟡 Advisory)
│       ├── pre-code-spec-check.json      ← preToolUse/write (🟠 High-value)
│       ├── post-task-governance.json     ← postTaskExecution (🟠 High-value)
│       ├── segregation-check.json        ← postTaskExecution (Tier 2+)
│       ├── api-contract-check.json       ← fileCreated (🟠 High-value)
│       ├── pre-pr-checklist.json         ← userTriggered (Tier 2+)
│       ├── periodic-audit.json           ← userTriggered (🟠 High-value)
│       └── [change-readiness-gate.json]  ← preTaskExecution (Tier 3)
│
├── .compliance-state.json                ← GENERATED by AI-GCE
│                                           Tier tracking, readiness criteria, score history
│
├── docs/
│   └── compliance-dashboard.md           ← GENERATED by audit agent (maintained ongoing)
│
└── .governance/                          ← GENERATED by AI-GCE
    ├── COMPLIANCE_README.md              ← How compliance works in THIS project
    │
    ├── rules/
    │   ├── — ARCHITECTURAL (always) —
    │   ├── architecture-compliance.md
    │   ├── api-first-compliance.md
    │   ├── security-compliance.md        ← Tier 1 baseline; Tier 3 enriched (SOX/GDPR)
    │   ├── data-governance.md
    │   ├── module-boundaries.md
    │   ├── naming-conventions.md         ← Tier 1
    │   ├── error-handling-compliance.md
    │   ├── logging-compliance.md
    │   ├── sensitive-data-protection.md
    │   ├── domain-context-enforcement.md
    │   ├── — NON-ARCHITECTURAL (tier-gated) —
    │   ├── phase-gates.md                ← Tier 1 basic → Tier 3 full
    │   ├── session-governance.md         ← Tier 1 basic / Tier 2 full
    │   ├── governance-checklist.md       ← Tier 2+
    │   ├── role-isolation.md             ← Tier 2+
    │   ├── team-topology.md              ← Tier 2+
    │   ├── sprint-governance.md          ← Tier 2+
    │   ├── pr-governance.md              ← Tier 2+
    │   ├── cicd-gates.md                 ← Tier 2+
    │   ├── devops-deployment.md          ← Tier 2+
    │   ├── steering-governance.md        ← Tier 2+
    │   ├── compliance-log-governance.md  ← Tier 2+
    │   ├── change-management.md          ← Tier 3
    │   ├── — CONDITIONAL —
    │   ├── [tenant-isolation.md]         ← IF multi-tenancy.md
    │   ├── [api-versioning-compliance.md] ← IF api-versioning.md
    │   ├── [resilience-compliance.md]    ← IF resilience-standards.md
    │   ├── [performance-compliance.md]   ← IF performance-standards.md
    │   ├── [frontend-compliance.md]      ← IF frontend-standards.md
    │   ├── [event-sourcing-compliance.md] ← IF event-sourcing.md
    │   ├── [feature-flag-compliance.md]  ← IF feature-flags.md
    │   └── [mcp-governance.md]           ← IF .kiro/settings/mcp.json configured
    │
    ├── agents/
    │   ├── compliance-audit-agent.md     ← 9-step with scoring, dashboard, tier awareness
    │   └── project-init-agent.md         ← 5-question scaffolding agent
    │
    ├── compliance-log/
    │   ├── compliance-log-schema.md      ← JSONL schema (CHECK/EXCEPTION/REMEDIATION/AUDIT/REDERIVATION)
    │   ├── exception-workflow.md         ← 5-step formal bypass process
    │   └── remediation-workflow.md       ← Violation resolution with SLAs
    │
    ├── [brownfield-baseline.md]          ← IF brownfield-patterns.md exists
    └── [incremental-adoption-plan.md]    ← IF brownfield-patterns.md exists
```

---

## Enforcement Layers (All Auto-Generated From Workspace)

```
┌─────────────────────────────────────────────────────────────────┐
│  FOUR ENFORCEMENT LAYERS                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  LAYER 1: PREVENTIVE (Steering — from AI-DWG)                    │
│  Already exists in .kiro/steering/                                │
│  AI-GCE READS these + MAY generate enforcement steering (4b)     │
│                                                                   │
│  LAYER 2: DETECTIVE (Hooks — generated by AI-GCE)                │
│  Fire on IDE events. Check against generated rules. Warn/block.  │
│  Tier A (fileEdited): security-critical, immediate               │
│  Tier B (agentStop): advisory, final-state-only                  │
│                                                                   │
│  LAYER 3: CORRECTIVE (Audit Agent — generated by AI-GCE)         │
│  On-demand full scan. Uses generated rules as checklist.          │
│  Scoring based on applicable rules for THIS project at THIS tier. │
│                                                                   │
│  LAYER 4: TRANSPARENT (Compliance Logging — always active)        │
│  Every hook writes to compliance-log/events/ after every fire.    │
│  Append-only JSONL. Git-committed as audit evidence.              │
│  Feeds: dashboard, exception tracking, MTTR metrics, auditors.   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Package File Structure (AI-GCE Framework)

The AI-GCE package itself contains the **generation logic** — not the final rules. It's the factory, not the product.

```
ai-gce/
├── README.md                               ← Overview, what it does, how to invoke
├── LICENSE                                 ← Apache 2.0 + Attribution
├── PLAN.md                                 ← This document (design rationale + summary)
│
├── ai-gce-rules/
│   └── core-generator.md                   ← Master generation logic (THE authoritative spec)
│
├── ai-gce-rule-details/
│   ├── common/ (5 files)                   ← Cross-cutting docs
│   ├── generators/ (23 files)              ← Derivation logic per rule category (11 architectural + 12 non-architectural)
│   ├── re-derivation/ (3 files)            ← Delta re-derivation logic
│   └── templates/
│       ├── hooks/ (15 files)               ← 14 parameterized JSON templates + INSTALL-GUIDE.md
│       ├── agents/ (3 files)               ← Audit agent + init agent + compliance readme
│       ├── compliance-log/ (6 files)       ← Schema + workflows + dashboard + brownfield templates
│       └── steering-templates/ (13 files)  ← Category templates for project-init-agent
│
└── kiro-setup/
    └── INSTALL.md
```

> **Note:** `core-generator.md` is the authoritative file inventory and orchestration spec (per Lesson 26).
> See the actual folder structure for the canonical list of filenames.
> Conditional hooks (tenant-isolation-check, documentation-reminder, steering-quality-check, etc.)
> are derived at runtime from generator logic — they do not have pre-built templates.

**Total actual files: ~73** (4 top-level + 1 core-generator + 5 common + 23 generators + 3 re-derivation + 15 hook templates + 3 agent templates + 6 compliance-log templates + 13 steering templates)

---

## Example: How a Rule Is Derived

### Input (from AI-DWG workspace)

`api-standards.md` contains:
```markdown
## API Documentation
| Aspect | Approach |
|--------|----------|
| Spec format | OpenAPI 3.1 |
| Generation | Auto-generated from NestJS decorators |
| Location | /api/docs |
```

`module-structure.md` contains:
```markdown
## Modules
| Module | Path |
|--------|------|
| Incident | src/modules/incident/ |
| Change | src/modules/change/ |
```

### AI-GCE Reads This → Generates:

**Rule (in `.governance/rules/api-first-compliance.md`):**
```markdown
### API-01: Contract Before Implementation

**Severity:** 🟠 High
**Derived From:** .kiro/steering/api-standards.md → "OpenAPI 3.1 spec"

**Rule:** Every API endpoint must have an OpenAPI specification BEFORE 
controller implementation code is written.

**Verification:**
- [ ] For each *.controller.ts in src/modules/*/presentation/ →
      a corresponding entry exists in the module's OpenAPI spec
- [ ] No controller file exists without matching spec

**File Patterns:** `src/modules/*/presentation/**/*.controller.ts`
```

**Hook (in `.kiro/hooks/api-contract-check.json`):**
```json
{
  "name": "API Contract Check",
  "version": "1.0.0",
  "when": {
    "type": "fileCreated",
    "patterns": ["src/modules/*/presentation/**/*.controller.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A controller file was created. Verify that an OpenAPI contract exists for this endpoint per rule API-01 in .governance/rules/api-first-compliance.md. Check if the corresponding spec defines this endpoint. If not, warn the developer to create the API contract first."
  }
}
```

**If the workspace were Django instead of NestJS:**
The same AI-GCE logic would read `tech-stack.md` (sees "Django") and `api-standards.md` (sees "OpenAPI") and generate:
- File pattern: `*/views.py` or `*/viewsets.py`
- Different hook pattern — same rule concept, different file globs

---

## Interaction Model

All four operating modes are fully specified in `core-generator.md`. Summary:

| Mode | Trigger | Steps | Key Output |
|------|---------|:-----:|-----------|
| **1: Full Generation** | "Generate compliance engine" / no .kiro/hooks/ | 12 | Full rules + hooks + agents + state file + dashboard |
| **2: Re-Derivation** | "Steering changed" / DWG signal | 6 | Updated rules + hooks (affected only) + REDERIVATION log event |
| **3: Brownfield** | brownfield-patterns.md exists | 8 | Baseline scan + incremental adoption plan + new-code-only hooks |
| **4: Tier Activation** | "Activate next tier" / readiness criteria met | 9 | New rules + hooks activated + re-audit + dashboard update |

### Re-Derivation Mapping (Which Steering Change Affects What)

| Steering File Changed | Affected Rules | Affected Hooks |
|----------------------|---------------|----------------|
| `tech-stack.md` | naming-conventions, devops-deployment | naming-check, coverage-check |
| `api-standards.md` | api-first-compliance | api-contract-check |
| `security-rules.md` | security-compliance | security-gate-check |
| `module-structure.md` | module-boundaries, team-topology | module-boundary-check |
| `multi-tenancy.md` | tenant-isolation | tenant-isolation-check |
| `database-rules.md` | data-governance | migration-safety |
| `testing-strategy.md` | cicd-gates, code-review-gates | coverage-check |
| `architecture-principles.md` | architecture-compliance | post-task-governance |
| `naming-conventions.md` | naming-conventions | naming-check |
| `git-workflow.md` | devops-deployment, pr-governance | pre-pr-checklist |
| `role-isolation.md` | role-isolation, team-topology | segregation-check |
| `session-governance.md` | session-governance | session-discipline |
| `project-governance.md` | phase-gates, sprint-governance | post-task-governance |
| `TEAM_AGREEMENTS.md` | pr-governance, role-isolation | pre-pr-checklist, segregation-check |
| `CODEOWNERS` | role-isolation, team-topology | module-boundary-check |
| `brownfield-patterns.md` (new) | → Triggers Mode 3 flow | |

---

## Conditional Generation

AI-GCE generates ONLY what the workspace justifies:

| Workspace Signal | Generated? | What's Generated |
|-----------------|:----------:|-----------------|
| `multi-tenancy.md` exists | ✅ | Tenant isolation rules + hook (fileEdited — Tier A) |
| `multi-tenancy.md` absent | ❌ | Skipped entirely |
| `api-versioning.md` exists | ✅ | Breaking-change prevention rules |
| `resilience-standards.md` exists | ✅ | Resilience pattern compliance rules |
| `observability-tracing.md` exists | ✅ | Distributed tracing compliance rules |
| `performance-standards.md` exists | ✅ | Performance budget enforcement rules |
| `workflow-engine.md` exists | ✅ | Workflow state-machine compliance |
| `frontend-standards.md` exists | ✅ | Frontend pattern + accessibility rules |
| `event-sourcing.md` exists | ✅ | Event store + CQRS boundary rules |
| `feature-flags.md` exists | ✅ | Flag lifecycle compliance |
| `brownfield-patterns.md` exists | ✅ | → Mode 3: baseline + incremental adoption |
| `.kiro/settings/mcp.json` configured | ✅ | MCP governance rules (MCP-001 through MCP-010) |
| Module count ≥ 3 | ✅ | Module boundary rules at full depth |
| Module count = 1 | ⚠️ | Basic boundary check (lightweight) |
| `.compliance-state.json` tier < 2 | — | Tier 2+ rules generated but NOT activated until tier upgrade |
| Team size ≥ 3 (from role-isolation.md) | ✅ | Phase/role-aware steering generated (Step 4b) |

---

## What AI-GCE Does NOT Do

- ❌ Require manual configuration (it READS the workspace — derives everything)
- ❌ Hardcode any technology (NestJS, Django, .NET — all derived from steering)
- ❌ Generate architecture/governance steering files (that's AI-DWG's job — it only READS them). Exception: AI-GCE MAY generate phase/role-aware ENFORCEMENT steering (Step 4b) — these are compliance-specific, fileMatch-only, and marked `<!-- generated by AI-GCE -->` to distinguish them from AI-DWG output.
- ❌ Make architecture decisions (those are in AI-ADLC)
- ❌ Generate application code
- ❌ Run as an interactive lifecycle with gates
- ❌ Activate all rules on Day 0 — uses 3-tier progressive adoption model
- ❌ Block day 1 on brownfield violations — baselines existing violations, enforces new code first
- ❌ Work without an AI-DWG workspace (it needs steering files to read)
- ❌ Require full regeneration for small changes (re-derivation handles incremental updates)
- ❌ Overwrite manually-customized rules during re-derivation (merge, don't replace)
- ❌ Fire advisory hooks on every intermediate save — security-critical on `fileEdited`, advisory on `agentStop`
- ❌ Only enforce architecture — covers team topology, role segregation, session methodology, sprint governance, DevOps, and change management too

---

## Prerequisite

**AI-GCE requires AI-DWG workspace output to exist.** It cannot operate on a bare repo. The steering files are its primary input — without them, it has only the built-in baseline (10 rules).

```
Required state BEFORE running AI-GCE:
  ✅ .kiro/steering/ populated (by AI-DWG) — primary derivation source
  ✅ Folder structure exists (by AI-DWG) — drives hook file patterns
  ✅ PROJECT_INSTRUCTIONS.md exists (by AI-DWG) — project identity

Enrichment sources (optional — enrich governance rules if present):
  ⚠️ TEAM_AGREEMENTS.md — enriches GOV-PR, GOV-ROLE rules
  ⚠️ CODEOWNERS — enriches GOV-ROLE, GOV-TT rules
  ⚠️ DEFINITION_OF_DONE.md — enriches phase gate rules
  ⚠️ docker-compose.yml — enriches migration + environment rules
```

**Without ANY steering files:** AI-GCE still produces the 10 built-in baseline rules (spec-before-code, never-vibe-code, author≠approver, etc.). This is the minimum viable governance floor.

---

## Estimated Effort

| Category | Files | Complexity |
|----------|:-----:|:----------:|
| Core generator | 1 | High (orchestration + workspace reading) |
| Common docs | 5 | Medium |
| Generators (architecture — 11 files) | 11 | High (derivation logic per architecture category) |
| Generators (governance — 12 files) | 12 | High (derivation logic per non-arch category) |
| Re-derivation logic (3 files) | 3 | High (change detection + incremental update) |
| Hook templates (15 files) | 15 | Medium (parameterized JSON + INSTALL-GUIDE) |
| Agent templates (3 files) | 3 | Medium-High (audit-agent + init-agent + readme) |
| Compliance log templates (6 files) | 6 | Medium (schema, exception, remediation, baseline, adoption-plan, dashboard) |
| Steering templates (13 files) | 13 | Medium (category template files for init-agent) |
| Documentation (README, LICENSE, PLAN, INSTALL) | 4 | Medium |
| **Total** | **~73** | |

---

## Implementation Order

1. `README.md` — overview and invocation guide
2. `core-generator.md` — master generation logic
3. `common/` — workspace reading guide, rule format, hook format, scoring
4. `generators/` — derivation logic per rule category
5. `hook-templates/` — parameterized hook JSONs
6. `agent-templates/` — audit agent spec + project-init-agent spec
7. `compliance-log-templates/` — logging infrastructure
8. `steering-templates/` — reusable steering templates for generated output
9. `accelerator/` — kickoff accelerator + tier activation plan

---

## Gap Analysis Summary

**Source:** Reference implementation at `_sample-project/__supportive inputs/_AI-DLC-compliance-engine/`
**Performed:** 2026-06-06 | **Session:** S10

### Status: Plan Updated — 11 Gaps Found, 3 Critical

| # | Gap | Severity | Action |
|---|-----|:--------:|--------|
| 1 | **3-Tier incremental adoption model missing** — plan treated adoption as single event; reference uses Day 0 / Sprint 2+ / Pre-Release tiers with readiness criteria and score targets | 🔴 Critical | Added to core-generator as fourth operating mode (Tier Activation); added to file structure |
| 2 | **`.compliance-state.json` missing** — reference tracks tier, phase, readiness criteria, artifacts, score history in a JSON state file read by audit agent | 🔴 Critical | Added to generated output; audit agent generates and maintains it |
| 3 | **Hook debounce strategy missing** — reference splits hooks: security-critical on `fileEdited`, advisory on `agentStop` (explicit decision record exists) | 🔴 Critical | Added to core-generator hook generation step; added to `generators/hooks-from-steering.md` scope |
| 4 | **Steering templates as GCE output** — reference has 16 template files (35 steering files) generated by the project-init-agent; distinct from AI-DWG steering files | 🟠 High | Added `steering-templates/` folder to file structure; scoped to init-agent path |
| 5 | **Project-init-agent absent** — reference has a full project scaffolding agent (5 questions → complete workspace in 2 min); GCE plan only had audit-agent | 🟠 High | Added `agent-templates/project-init-agent.md` to file structure and output |
| 6 | **Compliance dashboard missing** — reference has a full dashboard (`docs/compliance-dashboard.md`) with 30+ variables: tier progress, rules/hooks/steering inventory, score history, exceptions, remediations, MTTR | 🟠 High | Added `templates/compliance-log/compliance-dashboard-template.md` to file structure |
| 7 | **Knowledge map missing** — reference has full traceability matrix: rule → source → enforcement mechanism | 🟠 High | Added `common/knowledge-map-guide.md` to file structure; generated `docs/knowledge-map.md` in target workspace |
| 8 | **Compliance log JSONL format under-specified** — reference uses append-only JSONL with explicit event types (CHECK/EXCEPTION/REMEDIATION/AUDIT), dedup keys, SLAs | 🟡 Medium | Enriched compliance-log schema in core-generator and templates |
| 9 | **Rule taxonomy and tier tagging missing** — reference has 310+ rules in 8 categories, each tagged with tier and phase applicability | 🟡 Medium | Added tier-tagging requirement to rule generation step in core-generator |
| 10 | **Hook installation guide not generated in target workspace** — reference generates `.kiro/hooks/INSTALL-GUIDE.md` listing all hooks by tier | 🟡 Medium | Added to generated output list |
| 11 | **MCP governance dimension missing** — reference has `mcp-governance.md` rules and `mcp-audit-log.json` hook for MCP tool usage governance | 🟢 Low | Added as conditional rule category (IF project uses MCP servers) |

### Revised File Structure

The revised file structure is now the **main** file structure in the Package File Structure section above. The gap analysis additions were integrated directly into that canonical structure. Key changes from the original plan:

- `generators/` expanded from 11 → 23 files (added GOV-ROLE, GOV-TT, GOV-SESSION, GOV-SPRINT, GOV-PR, GOV-CICD, GOV-DEVOPS, GOV-STEER, GOV-LOG, CM-*, MCP-* generators)
- `templates/agents/` expanded: added `project-init-agent.md`
- `templates/compliance-log/` expanded: added `brownfield-baseline.md`, `incremental-adoption-plan.md`, `compliance-dashboard-template.md`
- `templates/steering-templates/` added: 13 category template files for project-init-agent
- `templates/hooks/` expanded: 15+ hooks + `INSTALL-GUIDE.md`
- `common/` expanded: added `scoring-model.md`, `knowledge-map-guide.md`

**Revised Total Estimated Files: ~67** (up from ~41 in original plan)

### What Doesn't Change

The fundamental design is sound:
- Zero manual configuration ✅
- Four operating modes (Full Generation, Re-Derivation, Brownfield, Tier Activation) ✅
- Two-source derivation (steering-enriched baseline) ✅
- Technology-specific hook derivation from steering files ✅
- Chain contract with AI-DWG ✅
- Conditional generation by steering file presence ✅

The gap analysis enriched the scope from architecture-compliance to full project governance, added the tier model, hook debounce, project-init-agent, compliance dashboard, and operational principles (silent-if-passing, phase-awareness, mandatory logging). It does not change the core derivation mechanism.
