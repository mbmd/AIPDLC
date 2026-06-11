# AI-DWG Process Overview

## What is AI-DWG?

AI-DWG (AI-Driven Workspace Generator) is a **one-time generator** that transforms an Architecture Package (produced by AI-ADLC) into a complete, ready-to-code development workspace. It produces Kiro steering files, project instructions, repository structure, configuration files, planning templates, and operational documents — everything a team needs to start building on day one.

Unlike AI-PILC and AI-ADLC (interactive lifecycles with stages and gates), AI-DWG is a **transformation engine**: Architecture Package in → Development Workspace out.

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
    AI-POLC ──┘     Prepare it       ▲                          
    Own it      └───────────────────┘  AI-POLC ⇄ AI-DLC (back-and-forth)
                AI-UXD ⇢ AI-POLC (personas/journeys)  ·  AI-DLC ⇢ AI-UXD+AI-POLC (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC = Amazon's open-source build lifecycle (not ours; we feed it).
```

AI-DWG sits between **architecture** and **construction**. It takes the "how" from AI-ADLC and transforms it into the operational environment that AI-DLC builds within and AI-GCE enforces against.

---

## Three Operating Modes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI-DWG OPERATING MODES                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MODE 1: FULL GENERATION                                                     │
│  ─────────────────────────                                                   │
│  When: Workspace doesn't exist yet (first time)                              │
│  Flow: READ AP → MAP → GENERATE → VALIDATE → OUTPUT                         │
│  Result: Complete development workspace, ready for git init + team start     │
│                                                                              │
│  MODE 2: DELTA RECONCILIATION                                                │
│  ─────────────────────────────                                               │
│  When: Architecture changed after initial generation                         │
│  Flow: READ CHANGES → DIFF → PROPOSE → MERGE → SIGNAL DOWNSTREAM            │
│  Result: Workspace updated incrementally, team customizations preserved      │
│                                                                              │
│  MODE 3: BROWNFIELD OVERLAY                                                  │
│  ──────────────────────────                                                  │
│  When: Existing codebase without AI-DWG governance                           │
│  Flow: DETECT EXISTING → READ AP → GENERATE MISSING → MERGE CONFIGS         │
│  Result: Steering + governance layered onto existing project, code untouched │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Mode Detection (Automatic)

| Condition | Mode Selected |
|-----------|:-------------:|
| Target workspace does NOT exist OR has no `.kiro/steering/` folder | Mode 1: Full Generation |
| User explicitly says "generate workspace" / "full generation" | Mode 1: Full Generation |
| Workspace EXISTS and `.kiro/steering/` has content | Mode 2: Delta Reconciliation |
| User says "architecture changed" / "reconcile" / points to updated ADR | Mode 2: Delta Reconciliation |
| Workspace EXISTS with code but NO `.kiro/steering/` (or partial) | Mode 3: Brownfield Overlay |
| User says "add governance" / "overlay" / "retrofit steering" / "brownfield" | Mode 3: Brownfield Overlay |

---

## Full Generation Pipeline (Mode 1)

```
┌──────────┐     ┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│  READ    │ ──► │   MAP    │ ──► │   GENERATE   │ ──► │   VALIDATE   │ ──► │  OUTPUT  │
│  (AP)    │     │(Transform)│    │  (Produce)   │     │ (Cross-check)│     │(Summary) │
└──────────┘     └──────────┘     └──────────────┘     └──────────────┘     └──────────┘
     │                │                   │                    │                    │
     ▼                ▼                   ▼                    ▼                    ▼
Load all AP      AP artifact →       Files with real     AP↔Workspace         Present to
artifacts +      workspace           content (not        consistency          user; signal
detect           artifact(s)         placeholders)       verified             AI-GCE
extensions       mapping rules
```

### Step Details

| Step | What Happens | Guided By |
|------|-------------|-----------|
| **READ** | Load all AP artifacts (vision, tech stack, C4 L1-L3, security, API, data, infra, multi-tenancy). Detect active AI-ADLC extensions via `adlc-state.md`. | `common/ap-reading-guide.md` |
| **MAP** | Transform each AP artifact into workspace artifact(s) using mapping rules. Extension-enrichment mappings loaded if extensions were active. | `mapping/*.md` files |
| **GENERATE** | Produce all steering files, operational docs, configs, folder structure. Content is populated from AP decisions — NOT placeholders. | `templates/*.md` files |
| **VALIDATE** | Cross-check: all principles encoded? All constraints reflected? No contradictions? Folder structure matches C4 L3? | `common/validation-rules.md` |
| **OUTPUT** | Present summary (file count, conditional files generated/skipped, next steps). Signal AI-GCE if applicable. | Core generator |

---

## Delta Reconciliation Pipeline (Mode 2)

```
┌─────────────┐   ┌─────────────┐   ┌──────────┐   ┌─────────┐   ┌──────────┐   ┌──────────┐
│ READ STATE  │►  │ READ CHANGE │►  │   DIFF   │►  │ PROPOSE │►  │  MERGE   │►  │  SIGNAL  │
│ (workspace) │   │  (updated   │   │(identify │   │(changes │   │(preserve │   │(AI-GCE)  │
│             │   │   AP art.)  │   │ affected)│   │ to user)│   │ customs) │   │          │
└─────────────┘   └─────────────┘   └──────────┘   └─────────┘   └──────────┘   └──────────┘
```

### Reconciliation Principles

| Principle | Description |
|-----------|-------------|
| **Never overwrite blindly** | Always diff → propose → user approves |
| **Preserve team customizations** | Only update AP-sourced sections; leave team additions untouched |
| **Additive preferred** | Adding content is safe; removing/changing requires confirmation |
| **Track provenance** | Sections marked `<!-- source: AP -->` vs. team additions |
| **Don't delete modules** | Flag module removals; don't auto-delete (may have code) |
| **Signal downstream** | After update, notify AI-GCE to re-derive affected rules |

---

## Brownfield Overlay Pipeline (Mode 3)

```
┌─────────────┐   ┌──────────┐   ┌──────────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│   DETECT    │►  │   READ   │►  │   GENERATE   │►  │  MERGE   │►  │ VALIDATE │►  │  OUTPUT  │
│  EXISTING   │   │   (AP)   │   │   MISSING    │   │ CONFIGS  │   │          │   │          │
│ (workspace) │   │          │   │(steering+docs)│  │(additive)│   │          │   │          │
└─────────────┘   └──────────┘   └──────────────┘   └──────────┘   └──────────┘   └──────────┘
```

### Key Differences from Mode 1

| Aspect | Mode 1 (Greenfield) | Mode 3 (Brownfield Overlay) |
|--------|---------------------|----------------------------|
| Source folders | Created from C4 L3 | NEVER created (code exists) |
| Steering files | Generated fresh | Generated fresh (safe — .kiro/ is new) |
| Config files | Generated fresh | MERGED (additive only) |
| Operational docs | Generated fresh | Only if missing (skip existing) |
| README.md | Generated | NEVER overwritten |
| brownfield-patterns.md | Not generated (greenfield) | Generated if AP has brownfield context |

### Brownfield Overlay Principles

| Principle | Description |
|-----------|-------------|
| **Never modify source code** | Mode 3 touches ONLY .kiro/, configs, and docs — never source files |
| **Steering is always safe** | .kiro/steering/ is a new directory — no conflict with existing code |
| **Config merges are additive** | Only ADD entries to .gitignore, CODEOWNERS — never remove |
| **Respect existing docs** | If README.md, CONTRIBUTING.md exist, they belong to the team |
| **Ask about conventions** | Before generating, detect what the team already does |

---

## What Gets Generated (Output Inventory)

### Steering Files (19 always + up to 10 conditional)

| Category | Files | Always/Conditional |
|----------|:-----:|:------------------:|
| Core Rules | `workspace-rules.md`, `architecture-principles.md` | Always |
| Technology | `tech-stack.md`, `coding-standards.md`, `naming-conventions.md` | Always |
| Governance | `project-governance.md`, `session-governance.md`, `role-isolation.md`, `scope-and-risks.md` | Always |
| Domain | `domain-context.md`, `module-structure.md` | Always |
| API | `api-standards.md` | Always |
| API (extended) | `api-versioning.md` | Conditional |
| Security | `security-rules.md` | Always |
| Data | `database-rules.md` | Always |
| Quality | `testing-strategy.md` | Always |
| Error Handling | `error-handling.md` | Always |
| Observability | `observability-logging.md`, `observability-sensitive.md` | Always |
| Observability (extended) | `observability-tracing.md` | Conditional |
| Infrastructure | `git-workflow.md` | Always |
| Multi-tenancy | `multi-tenancy.md` | Conditional |
| Resilience | `resilience-standards.md` | Conditional |
| Performance | `performance-standards.md` | Conditional |
| Workflow | `workflow-engine.md` | Conditional |
| Frontend | `frontend-standards.md` | Conditional |
| Event Sourcing | `event-sourcing.md` | Conditional (ADLC extension) |
| Feature Flags | `feature-flags.md` | Conditional (ADLC extension) |
| Brownfield | `brownfield-patterns.md` | Conditional (ADLC brownfield mode) |

### Operational Documents (7 files)

| Document | Purpose |
|----------|---------|
| `PROJECT_INSTRUCTIONS.md` | Master developer guide — single entry point |
| `DEFINITION_OF_DONE.md` | Quality criteria for completion |
| `CONTRIBUTING.md` | Commit strategy, PR process, branching model |
| `CICD_GUIDE.md` | CI/CD pipeline setup, quality gates, deployment, rollback |
| `TEAM_AGREEMENTS.md` | Operating rules, ownership, review standards |
| `ONBOARDING.md` | New developer checklist |
| `.github/pull_request_template.md` | PR checklist template |

### Planning Templates (3 files)

| Template | Purpose |
|----------|---------|
| `templates/session-planning.md` | AI-DLC session planning |
| `templates/sprint-planning.md` | Sprint structure and capacity |
| `templates/estimation-guide.md` | Size estimation (S/M/L/XL) with multipliers |

### Configuration Files

| File | Derived From |
|------|-------------|
| `.gitignore` | Technology Stack |
| `.editorconfig` | Technology Stack + coding standards |
| `docker-compose.yml` | Infrastructure & Deployment |
| `CODEOWNERS` | Component Design (C4 L3) ownership |
| `README.md` | Project skeleton |

### Source Structure

Folder layout derived from C4 Level 3 component design — modules, bounded contexts, and layer separation reflected in directory hierarchy.

---

## Extension-Aware Generation (AI-ADLC v1.1+)

When AI-ADLC extensions were active during architecture design, AI-DWG detects them and enriches output:

```
┌─────────────────────────────────────────────────────────────────┐
│  EXTENSION DETECTION FLOW                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. Read adlc-state.md → check "Enabled Extensions" section      │
│                                                                   │
│  2. For each active extension:                                    │
│     • Load extension-enrichment mapping file                      │
│     • Override conditional triggers (force-generate if needed)    │
│     • Enrich relevant steering files with pattern-specific rules  │
│                                                                   │
│  3. Extension enrichments are ADDITIVE — they add rules,          │
│     they don't replace core generation logic                      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

| Extension | Enriches | Forces Generation Of |
|-----------|----------|---------------------|
| DDD Tactical | `domain-context.md`, `module-structure.md`, `naming-conventions.md` | — |
| Microservices | `module-structure.md` | `resilience-standards.md`, `observability-tracing.md` |
| BFF Pattern | `api-standards.md` | `frontend-standards.md` |
| Event Sourcing/CQRS | `database-rules.md` | `event-sourcing.md` |
| Resilience Patterns | — | `resilience-standards.md` (full catalog) |
| Feature Flags | — | `feature-flags.md` |

---

## Adaptive Depth Model

AI-DWG adapts output scope and detail based on AP complexity:

| Depth Level | AP Indicators | Generation Behavior |
|-------------|--------------|---------------------|
| **Minimal** | ≤5 components, single-stack, no multi-tenancy, ≤2 integrations | 19 core steering files, basic operational docs, standard folder layout |
| **Standard** | 5-15 components, moderate integrations, typical security | Full steering set (19 + applicable conditional), complete operational docs, detailed folder layout |
| **Comprehensive** | >15 components, polyglot, multi-tenant, >5 integrations, compliance-heavy | All steering files, extended operational docs, granular folder layout with sub-module structure |

**Depth is determined automatically** from the AP content — not from user configuration. The AP already encodes complexity through its component count, integration points, and constraint density.

---

## Interaction Model

### Mode 1: Initial Generation

```
User: "Generate the development workspace from my architecture package"
  │
  ▼
AI asks 2-4 config questions:
  • Workspace root path? (default: ./)
  • Project display name? (default: from AP system name)
  • Team size? (affects operational doc depth)
  • Target Kiro autonomy mode? (affects session-governance)
  │
  ▼
AI generates all files in one pass
  │
  ▼
AI presents summary:
  "✅ Generated {n} steering files, {m} config files, repo structure with {p} modules"
  │
  ▼
Done. User verifies and starts working.
```

### Mode 2: Delta Reconciliation

```
User: "Architecture changed — reconcile the workspace"
  │
  ▼
AI reads updated AP artifact(s) + current workspace state
  │
  ▼
AI presents proposed changes:
  "Affected workspace files:
   • {file 1} — {what changes}
   • {file 2} — {what changes}
   Apply? (a) All (b) Review each (c) Skip"
  │
  ├── User picks (a) → Apply all; signal AI-GCE
  ├── User picks (b) → Show each change; user approves/rejects per file
  └── User picks (c) → Skip; no changes applied
```

### User Commands (Available at Any Time)

| Command | Effect |
|---------|--------|
| "Generate workspace" / "Full generation" | Trigger Mode 1 |
| "Architecture changed" / "Reconcile" | Trigger Mode 2 |
| "What extensions were active?" | Show detected AI-ADLC extensions |
| "Why was {file} generated?" | Show provenance (which AP artifact triggered it) |
| "Why was {file} skipped?" | Show conditional trigger that wasn't met |
| "Show conditional files" | List which conditional files were generated/skipped and why |
| "Regenerate {file}" | Re-derive a single steering file from current AP |
| "Add governance" / "Overlay" / "Brownfield" | Trigger Mode 3 |

---

## Mapping Logic (How AP → Workspace)

Each AP artifact maps to specific workspace artifacts:

| AP Artifact | Produces (Workspace) | Mapping File |
|-------------|---------------------|--------------|
| Architecture Vision & Principles | `workspace-rules.md`, `architecture-principles.md` | `mapping/vision-to-workspace-rules.md` |
| Technology Stack + ADRs | `tech-stack.md`, `.gitignore`, `docker-compose.yml`, `.editorconfig` | `mapping/techstack-to-config.md` |
| Component Design (C4 L3) | Folder structure, `module-structure.md`, `CODEOWNERS` | `mapping/components-to-structure.md` |
| C4 L3 Bounded Contexts | `domain-context.md` | `mapping/components-to-domain-context.md` |
| Security Architecture | `security-rules.md` | `mapping/security-to-steering.md` |
| API Architecture | `api-standards.md`, `api-versioning.md` | `mapping/api-to-steering.md` |
| Data Architecture | `database-rules.md` | `mapping/data-to-steering.md` |
| Multi-Tenancy Architecture | `multi-tenancy.md` | `mapping/tenancy-to-steering.md` |
| Infrastructure & Deployment | `git-workflow.md`, `docker-compose.yml` | `mapping/infra-to-config.md` |
| Infrastructure (CI/CD) | `CICD_GUIDE.md` | `mapping/infra-to-cicd.md` |
| Infrastructure (observability) | `observability-*.md` | `mapping/infra-to-observability.md` |
| Component Design (errors) | `error-handling.md` | `mapping/components-to-error-handling.md` |
| Integration Architecture | `resilience-standards.md` | `mapping/integration-to-resilience.md` |
| Quality Attributes (latency) | `performance-standards.md` | `mapping/quality-to-performance.md` |
| Container Design (UI) | `frontend-standards.md` | `mapping/containers-to-frontend.md` |
| Quality Attributes (all) | `DEFINITION_OF_DONE.md` | `mapping/quality-to-dod.md` |
| Team Context + Methodology | `TEAM_AGREEMENTS.md`, `role-isolation.md`, templates/ | `mapping/team-to-agreements.md` |
| Governance context | `CONTRIBUTING.md`, `ONBOARDING.md`, `PROJECT_INSTRUCTIONS.md`, PR template | `mapping/governance-derivation.md` |
| Brownfield context (conditional) | `brownfield-patterns.md` | `mapping/brownfield-to-steering.md` |

---

## What AI-DWG Does NOT Do

- ❌ Generate application code (AI-DLC's job)
- ❌ Set up CI/CD pipelines fully (produces skeleton; team configures)
- ❌ Install dependencies (produces dependency file skeleton; team runs install)
- ❌ Make architecture decisions (already made in AI-ADLC)
- ❌ Create governance enforcement hooks (AI-GCE's job)
- ❌ Overwrite team customizations during reconciliation
- ❌ Delete modules/folders during reconciliation
- ❌ Require full regeneration for small architecture changes
- ❌ Ask questions the Architecture Package already answers
- ❌ Generate steering for patterns the AP doesn't use

---

## Key Principle: Prescriptive Over Descriptive

Generated steering files are **rules**, not documentation:

| ❌ Descriptive (Avoid) | ✅ Prescriptive (Do This) |
|------------------------|--------------------------|
| "We use PostgreSQL for data storage" | "ALL persistent data MUST use PostgreSQL. Do NOT introduce alternative databases without an ADR." |
| "The project follows REST conventions" | "All endpoints MUST use kebab-case URLs, return JSON envelope format, and use standard HTTP status codes. See api-standards.md for the complete contract." |
| "Tenants are isolated" | "Every database query MUST include `tenant_id` in WHERE clause. NEVER query across tenants. Tenant context is propagated via middleware — do NOT access it directly from request." |

This makes steering files **enforceable** by AI-GCE and **unambiguous** for developers.
