# AI-ADLC Conceptual Map

> **What this file is:** A navigational guide to AI-ADLC's internal structure. It answers "where does each architecture concern live?" and helps you find the right file without reading the entire core-workflow.

---

## How to Read This

AI-ADLC is an **interactive lifecycle workflow** with 5 phases, each containing 1-4 stages. It produces an Architecture Package (AP) — the complete technical design foundation for a project. Every stage contributes one or more architecture artifacts to that package.

**Key principle:** AI-ADLC uses C4 model progressive decomposition (Context → Container → Component) combined with ADR-driven decisions. Extensions add specialized patterns when the architecture demands them.

---

## Concern → Location Map

### Requirements & Vision (Foundation Phase)

| Concern | Phase | Stage File | Output |
|---------|-------|-----------|--------|
| PIP/requirements ingestion | Foundation | `foundation/requirements-ingestion.md` | Structured requirements for architecture |
| Architecture vision & goals | Foundation | `foundation/architecture-vision.md` | Vision statement, quality attributes, constraints |
| Workspace detection & setup | Foundation | `foundation/workspace-detection.md` | Output folder structure |

### Architecture Decisions (Decisions Phase)

| Concern | Phase | Stage File | Output |
|---------|-------|-----------|--------|
| Technology stack selection | Decisions | `decisions/technology-stack.md` | ADR: technology choices |
| Security & identity model | Decisions | `decisions/security-identity.md` | ADR: auth strategy, identity provider |
| Multi-tenancy strategy | Decisions | `decisions/multi-tenancy.md` | ADR: tenancy model (if applicable) |

### System Decomposition (Decomposition Phase)

| Concern | Phase | Stage File | Output |
|---------|-------|-----------|--------|
| System context (C4 Level 1) | Decomposition | `decomposition/system-context.md` | Context diagram, external actors, boundaries |
| Container design (C4 Level 2) | Decomposition | `decomposition/container-design.md` | Container diagram, technology assignments, communication |

### Detailed Design (Design Phase)

| Concern | Phase | Stage File | Output |
|---------|-------|-----------|--------|
| Component design (C4 Level 3) | Design | `design/component-design.md` | Component diagrams, module structure |
| API architecture | Design | `design/api-architecture.md` | API contracts, versioning, standards |
| Data architecture | Design | `design/data-architecture.md` | Data models, storage strategy, migration approach |
| Integration & infrastructure | Design | `design/integration-infrastructure.md` | Integration patterns, infra requirements, deployment |

### Package Assembly (Assembly Phase)

| Concern | Phase | Stage File | Output |
|---------|-------|-----------|--------|
| Architecture Package assembly | Assembly | `assembly/package-assembly.md` | Complete AP (assembled, validated, handed off) |

---

## Extensions (Optional Advanced Patterns)

Extensions activate when the architecture demands specialized patterns. Each extension has two files:
- `{name}.opt-in.md` — always scanned, defines activation conditions
- `{name}.md` — loaded only when activated, adds stage rules

| Extension | Folder | When It Activates |
|-----------|--------|-------------------|
| BFF Pattern | `extensions/bff-pattern/` | Multiple frontend channels needing different API shapes |
| DDD Tactical | `extensions/ddd-tactical/` | Complex domain with aggregates, entities, value objects |
| Event Sourcing + CQRS | `extensions/event-sourcing-cqrs/` | Event-driven architecture with CQRS read/write separation |
| Feature Flags | `extensions/feature-flags/` | Progressive delivery, trunk-based development |
| Microservices | `extensions/microservices/` | Distributed system with independently deployable services |
| Resilience Patterns | `extensions/resilience-patterns/` | Distributed calls needing circuit breakers, retries, bulkheads |

**Key insight:** Extensions are blocking when active — not optional suggestions. They add mandatory stages/checks to the workflow. Multiple extensions can compose without conflict.

---

## Cross-Cutting Mechanisms

### Phase Flow

```
Foundation → Decisions → Decomposition → Design → Assembly
     │            │            │             │          │
     │            │            │             │          └── Package & hand off to AI-DWG
     │            │            │             └── Detail the internals (C4 L3 + APIs + data)
     │            │            └── Decompose the system (C4 L1 + L2)
     │            └── Make key technology & strategy choices (ADRs)
     └── Establish vision, constraints, quality attributes
```

### C4 Progressive Decomposition

| Level | Stage | What It Produces |
|-------|-------|-----------------|
| C4 Level 1 (Context) | `decomposition/system-context.md` | System boundary, external actors, trust zones |
| C4 Level 2 (Container) | `decomposition/container-design.md` | Deployable units, technology mapping, communication |
| C4 Level 3 (Component) | `design/component-design.md` | Internal module structure, responsibilities, interfaces |

### ADR-Driven Decisions

Architecture Decision Records are created during the Decisions phase and referenced throughout. Each ADR captures:
- Context (why this decision is needed)
- Decision (what was chosen)
- Consequences (trade-offs accepted)
- Status (proposed → accepted → superseded)

### Gate Model

Every stage ends with a gate — user must approve before proceeding. Extensions add additional gates when activated.

### Adaptive Depth

| Depth Level | When Applied | Effect |
|-------------|-------------|--------|
| Minimal | Simple architecture, few components | Fewer questions, condensed documents |
| Standard | Normal complexity | Full C4 treatment, all design artifacts |
| Comprehensive | Distributed systems, many integrations | Extended analysis, multiple extension activations |

---

## Common Questions

### "Where does the system boundary get defined?"

→ `decomposition/system-context.md` — C4 Level 1. Defines what's inside vs. outside the system, identifies external actors and integration points.

### "Where are technology choices made?"

→ `decisions/technology-stack.md` — produces the ADR for technology selection. This feeds into container design (which tech goes where) and downstream to AI-DWG (which generates tech-specific configs).

### "Where is the API design?"

→ `design/api-architecture.md` — defines API contracts, versioning strategy, standards. Works at C4 Level 3 granularity. References component design for endpoint grouping.

### "Where does multi-tenancy get decided?"

→ `decisions/multi-tenancy.md` — but only if the project needs it. This is a conditional stage. The decision here propagates to data architecture, security, and downstream packages (AI-DWG generates tenancy steering, AI-GCE generates tenant isolation hooks).

### "What's the final output?"

→ `assembly/package-assembly.md` assembles all artifacts into the Architecture Package (AP). This is what AI-DWG receives as its input.

### "How do extensions work?"

→ Each extension's `.opt-in.md` file is always scanned. If activation conditions are met (detected during decisions or decomposition), the full extension file loads and adds mandatory stages/rules. See `extensions/README.md` for the full registry.

---

## File Relationships

```
CONCEPTUAL_MAP.md  ← You are here (navigation)
README.md          ← What this package does (external audience)
WHITEPAPER.md      ← Theory and methodology (deep dive)
ROADMAP.md         ← Future development plans
core-workflow.md   ← How it executes (runtime orchestration)
```

---

*Created: June 2026 | Package: AI-ADLC v1.1*
