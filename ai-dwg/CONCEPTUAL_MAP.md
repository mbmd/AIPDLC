# AI-DWG Conceptual Map

> **What this file is:** A navigational guide to AI-DWG's internal structure. It answers "where does each workspace generation concern live?" and helps you find the right mapping or template file without reading the entire core-generator.

---

## How to Read This

AI-DWG is a **one-time generator** with 23 mapping files, each defining a transformation contract: "given this Architecture Package input, produce this workspace output." This map organizes those mappings by *concern domain* — so you can find the right transformation rule for any workspace artifact.

**Key principle:** Every generated file traces back to a specific AP document. If the AP doesn't contain it, DWG doesn't generate it (conditional generation). The mapping IS the API — input → output, explicitly defined.

---

## Concern → Location Map

### Core Workspace Setup

| Concern | Mapping File | AP Source | Generated Output |
|---------|-------------|-----------|-----------------|
| Workspace-level rules & identity | `mapping/vision-to-workspace-rules.md` | Architecture vision, project identity | `.kiro/steering/workspace-rules.md` |
| Tech stack configuration | `mapping/techstack-to-config.md` | Technology stack ADR | Project configs, linting, formatters |
| Project folder structure | `mapping/components-to-structure.md` | Component design (C4 L3) | Directory layout, module boundaries |

### Steering Files (Domain & Standards)

| Concern | Mapping File | AP Source | Generated Output |
|---------|-------------|-----------|-----------------|
| Domain language & context | `mapping/components-to-domain-context.md` | Component design, domain model | `domain-context.md` steering |
| API standards | `mapping/api-to-steering.md` | API architecture | `api-standards.md` steering |
| Security standards | `mapping/security-to-steering.md` | Security & identity ADR | `security-standards.md` steering |
| Data governance | `mapping/data-to-steering.md` | Data architecture | `data-governance.md` steering |
| Error handling patterns | `mapping/components-to-error-handling.md` | Component design | `error-handling.md` steering |
| Multi-tenancy rules | `mapping/tenancy-to-steering.md` | Multi-tenancy ADR (conditional) | `multi-tenancy.md` steering |

### Infrastructure & Operations

| Concern | Mapping File | AP Source | Generated Output |
|---------|-------------|-----------|-----------------|
| CI/CD pipeline config | `mapping/infra-to-cicd.md` | Integration & infrastructure | CI/CD config files |
| Environment configuration | `mapping/infra-to-config.md` | Integration & infrastructure | Environment configs |
| Observability & tracing | `mapping/infra-to-observability.md` | Integration & infrastructure | Observability steering |
| Resilience patterns | `mapping/integration-to-resilience.md` | Integration patterns | `resilience-standards.md` steering |
| Performance standards | `mapping/quality-to-performance.md` | Quality attributes | `performance-standards.md` steering |

### Governance & Team

| Concern | Mapping File | AP Source | Generated Output |
|---------|-------------|-----------|-----------------|
| Team agreements & topology | `mapping/team-to-agreements.md` | Team structure (from PIP) | Team topology, role steering |
| Session governance rules | `mapping/governance-derivation.md` | Governance framework | `session-governance.md` steering |
| Definition of Done | `mapping/quality-to-dod.md` | Quality attributes | `DEFINITION_OF_DONE.md` |
| Frontend standards | `mapping/containers-to-frontend.md` | Container design (UI containers) | `frontend-standards.md` steering |

### Brownfield Handling

| Concern | Mapping File | AP Source | Generated Output |
|---------|-------------|-----------|-----------------|
| Existing codebase overlay | `mapping/brownfield-to-steering.md` | Brownfield assessment (if exists) | Brownfield-aware steering additions |

### Extension Enrichments (from AI-ADLC Extensions)

| Concern | Mapping File | Triggered By | Generated Output |
|---------|-------------|-------------|-----------------|
| DDD tactical patterns | `mapping/extension-ddd-enrichment.md` | DDD extension active in AP | DDD-specific steering & structure |
| Event sourcing patterns | `mapping/extension-eventsourcing-enrichment.md` | Event sourcing extension in AP | CQRS/ES steering & structure |
| Feature flag patterns | `mapping/extension-featureflags-enrichment.md` | Feature flags extension in AP | Feature flag steering & config |
| Microservices patterns | `mapping/extension-microservices-enrichment.md` | Microservices extension in AP | Service boundaries, inter-service steering |

---

## Cross-Cutting Mechanisms

### Generation Modes

| Mode | When Used | Behavior |
|------|-----------|----------|
| **Full Generation** | First run (no existing workspace) | Generate everything from AP |
| **Delta Reconciliation** | AP updated after initial generation | Detect changes, update only affected files, preserve customizations |

### Reconciliation (Delta Updates)

Handled by 4 files in `reconciliation/`:

| File | Purpose |
|------|---------|
| `diff-strategy.md` | How to detect what changed in AP since last generation |
| `merge-strategy.md` | How to merge updates without overwriting team customizations (`<!-- custom -->` markers) |
| `provenance-tracking.md` | How to maintain AP-source comments in every generated file |
| `downstream-signaling.md` | How to notify AI-GCE that the workspace changed (triggers re-derivation) |

### Conditional Generation

Every mapping file has explicit trigger conditions. If the AP doesn't contain the relevant architecture content, the corresponding workspace file is NOT generated. No bloat.

| Condition | Example |
|-----------|---------|
| AP has multi-tenancy ADR | → Generate `multi-tenancy.md` steering |
| AP has no multi-tenancy | → Skip entirely |
| AP has event sourcing extension | → Generate ES-specific enrichment |
| AP has no extensions | → Skip all extension mappings |

### Provenance Tracking

Every generated file includes a metadata comment identifying which AP document justified its creation:

```markdown
<!-- Generated by AI-DWG | Source: api-architecture.md → "API Versioning Strategy" -->
```

This enables traceability audits and targeted reconciliation.

### Technology-Adaptive Output

Mappings produce different output based on the tech stack:

| Stack | Config Format | Linting | Test Framework | Package Manager |
|-------|--------------|---------|----------------|-----------------|
| Node.js | `.json` / `.yaml` | ESLint | Jest/Vitest | npm/yarn/pnpm |
| Python | `pyproject.toml` | Ruff/Pylint | pytest | pip/poetry |
| .NET | `.csproj` / `.json` | Roslyn analyzers | xUnit/NUnit | NuGet |
| Java | `pom.xml` / `build.gradle` | Checkstyle/SpotBugs | JUnit | Maven/Gradle |
| Generic | `.yaml` | — | — | — |

---

## Common Questions

### "Where does the folder structure come from?"

→ `mapping/components-to-structure.md`. Reads the C4 Level 3 component design and translates it into a directory layout with module boundaries.

### "Where do steering files get generated?"

→ Multiple mapping files, each producing one steering file. The mapping file name follows the pattern `{ap-source}-to-{output}.md`. For example, `api-to-steering.md` reads `api-architecture.md` and produces `api-standards.md`.

### "What if I customized a steering file and AP changes?"

→ `reconciliation/merge-strategy.md` defines the preservation logic. Sections marked `<!-- custom -->` survive re-generation. Everything else updates to match the new AP.

### "How does DWG signal downstream packages?"

→ `reconciliation/downstream-signaling.md`. When DWG generates or re-generates, it creates/updates the marker file (`.kiro/steering/workspace-rules.md`). AI-GCE detects this and knows the workspace changed.

### "How are AI-ADLC extensions handled?"

→ Four dedicated enrichment mapping files (`extension-*.md`). Each checks whether its corresponding extension was activated in the AP. If yes, it generates additional steering files and structure. If no, it's skipped entirely.

### "What does the AP reading guide do?"

→ `common/ap-reading-guide.md` teaches the generator how to parse and interpret AP documents — what to look for, section naming conventions, how to handle missing sections gracefully.

---

## File Relationships

```
CONCEPTUAL_MAP.md  ← You are here (navigation)
README.md          ← What this package does (external audience)
PLAN.md            ← Why it was designed this way (decisions)
WHITEPAPER.md      ← Theory and methodology (deep dive)
core-generator.md  ← How it executes (runtime orchestration)
```

---

*Created: June 2026 | Package: AI-DWG v1.0*
