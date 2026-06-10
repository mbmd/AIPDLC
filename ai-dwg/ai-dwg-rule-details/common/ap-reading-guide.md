# Architecture Package Reading Guide

## Purpose

This document defines HOW AI-DWG reads, locates, and parses an Architecture Package (AP) produced by AI-ADLC. It covers detection strategy, file identification, content extraction patterns, and error handling when the AP is incomplete or uses a non-standard structure.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS activity, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Read the AP with stakeholder empathy — understand WHY decisions were made, not just WHAT was decided
- Validate completeness from a requirements perspective — are there gaps between stated goals and documented architecture?
- Extract implicit business rules that the architect may have embedded in technical constraints
- Map quality attributes back to business outcomes (e.g., "99.9% uptime" = "customer SLA commitment")
- Question assumptions — if an artifact seems incomplete, frame clarification questions in business terms

### Anti-Patterns for This Activity
- Do NOT invent architecture decisions when the AP is silent — flag as missing, never assume
- Do NOT interpret ambiguous AP content optimistically — ambiguity means "ask the user"
- Do NOT skip validation steps because the AP "looks complete" — verify structure AND content

### Quality Check
A good output from this activity sounds like:
- "AP scan complete — 10/10 required artifacts found. Multi-tenancy document present (conditional generation triggered). Extension `ddd-tactical` active — enrichment mappings will apply."
- "Architecture Vision contains 6 principles but no explicit constraints table — flagging for user: should I proceed with principles-only or do constraints exist elsewhere?"

---

## Step 1: Locate the Architecture Package

### Detection Strategy (Ordered)

```
1. User provides path explicitly
   → Use that path directly
   
2. Scan for marker file (adlc-state.md) in common locations:
   → ./architecture/
   → ./docs/architecture/
   → ../
   → ./ (current directory)
   → Any sibling folder of the workspace root
   
3. Marker not found
   → Ask user: "Where is your Architecture Package located?"
   → User points to folder
   
4. No adlc-state.md exists anywhere (standalone/manual mode)
   → Ask user to identify which documents map to which AP artifact
   → Proceed without extension detection (no state file to read)
```

### Marker File: `adlc-state.md`

This is the anchor. Once found, ALL other AP files are located relative to its directory.

**Critical fields to extract from `adlc-state.md`:**

| Field | Used For |
|-------|----------|
| `Output Structure` | Determines naming pattern: `numbered` (01_*.md) or `phase-folder` (foundation/, design/, etc.) |
| `Enabled Extensions` | Triggers extension-enrichment mappings (DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags) |
| `Completed Stages` | Confirms AP completeness — flags if stages are missing |
| `ADR Register` | Inventory of all architecture decisions for cross-referencing |
| `System Name` | Used as default project display name if user doesn't override |

---

## Step 1b: Locate Parallel Inputs (PBP / UXP)

In the reshaped Project layer, **AI-ADLC, AI-POG, and AI-UXD run in parallel and all feed AI-DWG**. After locating the AP, also look for two optional sibling inputs. Neither blocks generation — they enrich it.

### Detection Strategy (per input)

```
For PBP (AI-POG output):
1. User provides path explicitly → use it
2. Scan for marker pog-state.md in: ./backlog/, ./product/, ../, ./ , sibling folders
3. Not found → proceed AP-only (PBP enrichment skipped — do NOT block)

For UXP (AI-UXD output):
1. User provides path explicitly → use it
2. Scan for marker uxd-state.md in: ./design/, ./ux/, ../, ./ , sibling folders
3. Not found → proceed without design-system / accessibility enrichment (do NOT block)
```

### Marker Files

| Input | Marker | Producer | What it anchors |
|-------|--------|----------|-----------------|
| **PBP** — Product Backlog Package | `pog-state.md` | AI-POG | DoR/DoD, release/increment slices, acceptance-criteria standard, prioritization model |
| **UXP** — UX Design Package | `uxd-state.md` | AI-UXD | Design system + tokens, component/pattern inventory, accessibility baseline (WCAG) |

### Graceful Degradation (Lesson 6 — OR-input)

The AP is the generation core. PBP and UXP are *additive enrichment*: when present they sharpen specific outputs (`DEFINITION_OF_DONE.md`, planning templates, `frontend-standards.md`, and a future `design-system.md`); when absent the generator proceeds AP-only with no loss of core function. **Never invent backlog or design content the PBP/UXP doesn't provide** — same rule as the AP (Key Rule 1).

> **Forward-declaration note:** AI-POG (idea 006) and AI-UXD (idea 010) are pending build. This step defines the *detection contract* AI-DWG honors once these producers exist. The detailed PBP→DW and UXP→DW extraction guides are authored at their integration builds (Phase 4), not here.

---

## Step 2: Identify AP Files

### Two Naming Patterns

AI-ADLC lets users choose between numbered documents and phase folders. AI-DWG must handle both.

**Pattern A: Numbered Documents (Default)**

| # | File Name Pattern | Maps To |
|---|------------------|---------|
| 01 | `*Architecture_Vision*` | Architecture Vision & Principles |
| 02 | `*System_Context*` or `*C4L1*` | System Context (C4 Level 1) |
| 03 | `*Container*` or `*C4L2*` | Container Diagram (C4 Level 2) |
| 04 | `*Technology_Stack*` | Technology Stack |
| 05 | `*MultiTenancy*` or `*Multi_Tenancy*` | Multi-Tenancy Architecture (conditional) |
| 06 | `*Security*Identity*` or `*Security*` | Security & Identity Architecture |
| 07 | `*Data_Architecture*` | Data Architecture |
| 08 | `*API_Architecture*` | API Architecture |
| 09 | `*Integration*` | Integration Architecture |
| 10 | `*Infrastructure*` or `*Deployment*` | Infrastructure & Deployment |
| 11 | `*Component*` or `*C4L3*` | Component Design (C4 Level 3) |
| — | `Architecture_Workbook*` | Architecture Workbook |
| — | `*PACKAGE_README*` or `*README*` | Package README |
| — | `ADR/` folder | Architecture Decision Records |

**Pattern B: Phase Folders**

| Folder | Contains |
|--------|----------|
| `foundation/` | Architecture Vision, (may include requirements summary) |
| `decomposition/` | System Context (C4 L1), Container Diagram (C4 L2) |
| `decisions/` | Technology Stack, Multi-Tenancy, Security Architecture |
| `design/` | Data Architecture, API Architecture, Integration, Infrastructure, Component Design |
| `ADR/` | Architecture Decision Records |

**Detection logic:**
1. Read `adlc-state.md` → `Output Structure` field
2. If `numbered` → scan for numbered files using Pattern A
3. If `phase-folder` → scan for folders using Pattern B
4. If field missing → try Pattern A first (default), fall back to Pattern B

---

## Step 3: Validate AP Completeness

Before generating, verify all required artifacts exist:

### Required Artifacts (Generation fails without these)

| Artifact | How to Verify | If Missing |
|----------|--------------|-----------|
| Architecture Vision | File exists + contains "Principles" section | BLOCK — ask user |
| System Context (C4 L1) | File exists + contains external actors/systems | BLOCK — ask user |
| Container Diagram (C4 L2) | File exists + contains container list | BLOCK — ask user |
| Technology Stack | File exists + contains technology selections table | BLOCK — ask user |
| Security Architecture | File exists + contains authentication/authorization sections | BLOCK — ask user |
| Data Architecture | File exists + contains entity/schema information | BLOCK — ask user |
| API Architecture | File exists + contains REST conventions/standards | BLOCK — ask user |
| Integration Architecture | File exists + contains external system patterns | BLOCK — ask user |
| Infrastructure & Deployment | File exists + contains deployment topology | BLOCK — ask user |
| Component Design (C4 L3) | File exists + contains module decomposition | BLOCK — ask user |
| ADR folder | Folder exists + contains at least 1 ADR | WARN — generate without cross-refs |

### Optional Artifacts (Enrich generation if present)

| Artifact | If Present | If Absent |
|----------|-----------|----------|
| Multi-Tenancy Architecture | Generate `multi-tenancy.md` steering file | Skip — single-tenant assumed |
| Architecture Workbook | Extract open items for `scope-and-risks.md` | Generate scope from other sources |
| Package README | Use as summary reference | Derive summary from individual docs |

### Completeness Report

After scanning, present to user:

```
📋 Architecture Package Scan Results

Location: {path}
Structure: {numbered | phase-folder}
Extensions active: {list or "none"}

Required artifacts:
  ✅ Architecture Vision — found
  ✅ System Context (C4 L1) — found
  ✅ Container Diagram (C4 L2) — found
  ✅ Technology Stack — found
  ✅ Security Architecture — found
  ✅ Data Architecture — found
  ✅ API Architecture — found
  ✅ Integration Architecture — found
  ✅ Infrastructure & Deployment — found
  ✅ Component Design (C4 L3) — found
  ✅ ADR folder — found ({n} ADRs)

Optional artifacts:
  {✅|❌} Multi-Tenancy Architecture
  {✅|❌} Architecture Workbook
  {✅|❌} Package README

Status: {READY TO GENERATE | MISSING REQUIRED: {list}}
```

---

## Step 4: Extract Content from AP Artifacts

### What to Extract Per Artifact

For each AP document, extract these specific elements that drive workspace generation:

#### From Architecture Vision

| Extract | Used In |
|---------|---------|
| Vision statement (1-2 sentences) | `workspace-rules.md` header |
| Guiding Principles (P1-Pn) | `workspace-rules.md` rules, `architecture-principles.md` |
| Architectural Constraints table | `workspace-rules.md` DON'T rules |
| Quality Attributes with priorities | `testing-strategy.md`, `DEFINITION_OF_DONE.md` |

#### From Technology Stack

| Extract | Used In |
|---------|---------|
| Language/runtime per container | `tech-stack.md`, `.gitignore`, `docker-compose.yml` |
| Framework selections | `coding-standards.md`, `naming-conventions.md` |
| Database technology | `database-rules.md`, `docker-compose.yml` |
| Caching layer | `tech-stack.md` |
| Message queue | `tech-stack.md`, `docker-compose.yml` |
| Monitoring/observability stack | `observability-*.md` |
| UI framework (if any) | `frontend-standards.md` |

#### From System Context (C4 L1)

| Extract | Used In |
|---------|---------|
| System boundary definition | `scope-and-risks.md` |
| External actors list | `scope-and-risks.md`, `security-rules.md` |
| External systems list | `scope-and-risks.md`, integration context |
| Communication protocols | `api-standards.md` |

#### From Container Diagram (C4 L2)

| Extract | Used In |
|---------|---------|
| Container list (deployable units) | Top-level folder structure |
| Container technologies | `docker-compose.yml` |
| Data stores | `database-rules.md`, `docker-compose.yml` |
| Inter-container communication | `api-standards.md`, `resilience-standards.md` |
| UI containers (if any) | Triggers `frontend-standards.md` |

#### From Component Design (C4 L3)

| Extract | Used In |
|---------|---------|
| Module list per container | Folder structure (src-level) |
| Module responsibilities | `module-structure.md` |
| Module dependencies/rules | `module-structure.md` |
| Bounded contexts | `domain-context.md` |
| Core entities per context | `domain-context.md`, `naming-conventions.md` |
| Cross-cutting concerns | `error-handling.md`, `observability-logging.md` |
| Component ownership | `CODEOWNERS` |

#### From Security Architecture

| Extract | Used In |
|---------|---------|
| Authentication methods | `security-rules.md` |
| Token strategy | `security-rules.md` |
| RBAC model | `security-rules.md` |
| Encryption approach | `security-rules.md`, `observability-sensitive.md` |
| Audit logging strategy | `observability-logging.md` |
| OWASP mitigations | `security-rules.md` |
| Sensitive data categories | `observability-sensitive.md` |

#### From API Architecture

| Extract | Used In |
|---------|---------|
| REST conventions | `api-standards.md` |
| URL patterns | `api-standards.md`, `naming-conventions.md` |
| Error response format | `api-standards.md`, `error-handling.md` |
| Versioning strategy | `api-versioning.md` (conditional) |
| Pagination approach | `api-standards.md` |
| Rate limiting | `api-standards.md` |

#### From Data Architecture

| Extract | Used In |
|---------|---------|
| Data model strategy (DDD/ERD) | `database-rules.md` |
| Schema management approach | `database-rules.md` |
| Multi-tenant scoping method | `database-rules.md`, `multi-tenancy.md` |
| Caching strategy | `database-rules.md` |
| Search index approach | `database-rules.md` |

#### From Integration Architecture

| Extract | Used In |
|---------|---------|
| Integration patterns per external system | `resilience-standards.md` |
| Failure handling (retry, circuit breaker) | `resilience-standards.md` |
| Event-driven patterns | `module-structure.md` |
| Integration count (triggers conditional) | Conditional: `resilience-standards.md` |

#### From Infrastructure & Deployment

| Extract | Used In |
|---------|---------|
| Container/orchestration strategy | `docker-compose.yml` |
| Observability stack (metrics, logging, tracing) | `observability-*.md` |
| Branching/CI strategy | `git-workflow.md` |
| Scaling approach | `performance-standards.md` |
| HA/DR approach | `scope-and-risks.md` |

#### From ADRs

| Extract | Used In |
|---------|---------|
| ADR titles and decisions | Cross-referenced in relevant steering files |
| Technology choices with rationale | `tech-stack.md` rationale sections |
| Pattern decisions | Relevant steering files (e.g., ADR about event-driven → module-structure) |

---

## Step 5: Detect Active Extensions (AI-ADLC v1.1+)

### Reading Extension State

From `adlc-state.md`, locate the `Enabled Extensions` field:

```markdown
## Enabled Extensions
- ddd-tactical (activated at Stage 12)
- microservices (activated at Stage 5)
- resilience-patterns (activated at Stage 11)
```

### Extension Impact on Reading

When an extension is active, the AP contains ADDITIONAL content that normal (non-extension) APs don't have:

| Extension Active | Look For (additional AP content) |
|-----------------|----------------------------------|
| **DDD Tactical** | Aggregate boundary definitions in C4 L3; Domain Events catalog; ACL specifications; Value Object identification |
| **Microservices** | Service mesh configuration in Infrastructure; Distributed tracing design; Saga/choreography patterns in Integration; Schema registry in API |
| **BFF Pattern** | BFF container in C4 L2; Aggregation rules; Client-specific shaping rules |
| **Event Sourcing/CQRS** | Event store design in Data Architecture; Projection definitions; Read model specifications; Snapshot strategy |
| **Resilience Patterns** | Extended failure handling in Integration (bulkhead, graceful degradation); Circuit breaker configuration per integration |
| **Feature Flags** | Flag architecture in Component Design or Technology Stack; Rollout strategy; Flag lifecycle rules |

### What to Do with Extension Content

1. Extract the extension-specific content from the AP documents where it appears
2. Load the corresponding extension-enrichment mapping file (`mapping/extension-{name}-enrichment.md`)
3. Follow enrichment rules to add extension-specific content to relevant steering files
4. Override conditional triggers where the extension demands it (e.g., Microservices → always generate `resilience-standards.md`)

---

## Step 6: Build the Generation Context

After reading all artifacts, compile a **generation context** — a mental model of the system:

```
GENERATION CONTEXT:
├── System Identity
│   ├── Name: {from adlc-state or user config}
│   ├── Vision: {1-2 sentence architecture vision}
│   └── Type: {monolith | modular-monolith | microservices | hybrid}
│
├── Technology Profile
│   ├── Primary language: {e.g., TypeScript}
│   ├── Framework: {e.g., NestJS}
│   ├── Database: {e.g., PostgreSQL}
│   ├── Cache: {e.g., Redis}
│   ├── Queue: {e.g., BullMQ}
│   └── Frontend: {e.g., React / none}
│
├── Complexity Indicators
│   ├── Module count: {n}
│   ├── Integration count: {n}
│   ├── Multi-tenant: {yes/no}
│   ├── Extensions active: {list}
│   └── Depth level: {minimal / standard / comprehensive}
│
├── Principles (Rules to Encode)
│   ├── P1: {name} — {statement}
│   ├── P2: {name} — {statement}
│   └── ...
│
├── Constraints (DON'T Rules)
│   ├── C1: {constraint} — source: {where it came from}
│   └── ...
│
├── Modules (Folder Structure)
│   ├── {module-1}: {responsibility}
│   ├── {module-2}: {responsibility}
│   └── ...
│
└── Conditional Triggers
    ├── multi-tenancy.md: {yes/no — reason}
    ├── resilience-standards.md: {yes/no — reason}
    ├── observability-tracing.md: {yes/no — reason}
    ├── performance-standards.md: {yes/no — reason}
    ├── workflow-engine.md: {yes/no — reason}
    ├── frontend-standards.md: {yes/no — reason}
    ├── api-versioning.md: {yes/no — reason}
    ├── event-sourcing.md: {yes/no — reason}
    └── feature-flags.md: {yes/no — reason}
```

This context drives ALL subsequent mapping and generation. It's the "compiled understanding" of the architecture.

---

## Error Handling

| Situation | Response |
|-----------|----------|
| `adlc-state.md` not found | Ask user for AP location. If still not found → manual mode (user maps docs) |
| Required artifact missing | Present completeness report. Ask: "Generate with assumptions?" or "Wait for artifact?" |
| Artifact exists but has unexpected format | Attempt to extract what's available. Mark sections with `<!-- partial: could not extract {what} -->` |
| `adlc-state.md` shows incomplete stages | Warn user: "AP appears incomplete (stages {list} not completed). Generate anyway?" |
| Conflicting information between AP docs | Flag conflict to user: "Technology Stack says X but Infrastructure says Y. Which is correct?" |
| Unknown technology (not in template library) | Generate generic patterns. Mark with `<!-- customize: {technology}-specific rules needed -->` |
| Extension listed in state but no extension content in AP | Warn: "Extension {name} was active but its expected content wasn't found in AP. Generating without enrichment." |

---

## Key Rules

1. **NEVER invent architecture decisions.** If the AP doesn't state something, don't assume it. Ask or skip.
2. **Extract VERBATIM where possible.** Principle statements, constraint definitions, and technology names should be copied exactly — not paraphrased.
3. **Trace every extraction.** Know which AP document + section provided which piece of generated content (for provenance tracking).
4. **Respect conditional triggers.** Don't generate files the AP doesn't justify. Don't skip files the AP demands.
5. **Extension content is authoritative.** If an extension was active, its additional AP content takes precedence over normal conditional logic.
