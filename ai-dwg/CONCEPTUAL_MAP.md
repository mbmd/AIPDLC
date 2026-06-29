# AI-DWG Conceptual Map

> **What this file is:** A navigational guide to AI-DWG's internal structure. It answers "where does each workspace generation concern live?" and helps you find the right mapping or template file without reading the entire core-generator.

---

## How to Read This

AI-DWG is a **convergence-point generator** with 36 mapping files, each defining a transformation contract: "given this peer input, produce this workspace output cluster." This map organizes those mappings by *concern domain* — so you can find the right transformation rule for any workspace artifact.

**Key principles:**
- **Peer inputs, no master.** AI-DWG accepts any non-empty subset of {ADLC, POLC, UXD}. None is privileged. Each input unlocks its own output cluster.
- **One input → one output cluster.** Every generated file traces back to exactly one peer input. If that input is absent, the cluster is skipped (with quality-impact disclosure to the user).
- **The mapping IS the API** — input → output, explicitly defined.

### Peer Input → Output Cluster

| Peer Input | Producer | Marker | Output Cluster |
|-----------|----------|--------|----------------|
| **AP** — Architecture Package | AI-ADLC | `adlc-state.md` | Tech steering (13+), `technical-environment.md`, src structure, configs |
| **PBP** — Product Backlog Package | AI-POLC | `polc-state.md` | `vision.md`, `DEFINITION_OF_DONE.md`, planning templates, scope-and-risks, `traceability-matrix.md`, `value-metrics.md`, `epics-and-backlog.md`, `user-stories.md` |
| **UXP** — UX Design Package | AI-UXD | `uxd-state.md` | `design-system.md`, `frontend-standards.md`, `ui-implementation-spec.md`, a11y relay, `navigation-structure.md`, `design-qa.md`, `content-guidelines.md`, `theming.md`, `i18n-standards.md` |

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

### Peer Cluster Assembly (POLC & UXD clusters + AI-DLC v1 input documents)

| Concern | Mapping File | Source Input | Generated Output |
|---------|-------------|-------------|-----------------|
| Design system governance | `mapping/uxd-to-design-system.md` | UXP design tokens + component inventory | `design-system.md` steering |
| Vision Document (AI-DLC v1 input) | `mapping/polc-uxd-to-vision-document.md` | PBP product vision + UXP personas/journeys | `vision.md` |
| Technical Environment Document (AI-DLC v1 input) | `mapping/ap-uxp-to-tech-environment.md` | AP tech stack + UXP frontend patterns | `technical-environment.md` |
| Extension rules bundle (AI-DLC v1 input) | `mapping/extension-rules-assembly.md` | AP security + UXP a11y + TGE/DWG testing | `aidlc-rules/extensions/` |
| Frontend standards (UXD-enriched) | `mapping/containers-to-frontend.md` | C4 L2 UI containers + UXP design system | `frontend-standards.md` steering |

### POLC Cluster — Backlog, Traceability & Value (extended)

| Concern | Mapping File | Source Input | Generated Output |
|---------|-------------|-------------|-----------------|
| Traceability matrix | `mapping/polc-to-traceability.md` | PBP `governance/traceability.md` | `traceability-matrix.md` |
| Value & KPI metrics | `mapping/polc-to-value-metrics.md` | PBP `operations/value-metrics.md` | `value-metrics.md` (+ observability relay) |
| Epic/backlog scaffold | `mapping/polc-to-epics-backlog.md` | PBP `strategy/epic-decomposition.md` | `epics-and-backlog.md` + `backlog/EPIC-*.md` |
| INVEST user stories (Tier 2) | `mapping/polc-to-user-stories.md` | PBP `tier2/story-elaboration.md` | `user-stories.md` + `examples/acceptance/*.feature.md` |

### UXD Cluster — IA, Content, Theming & i18n (extended)

| Concern | Mapping File | Source Input | Generated Output |
|---------|-------------|-------------|-----------------|
| Information architecture | `mapping/uxd-to-information-architecture.md` | UXP `define/information-architecture.md` | `navigation-structure.md` steering |
| Design QA / fidelity | `mapping/uxd-to-design-qa.md` | UXP `validate/design-qa-framework.md` | `design-qa.md` steering (+ GCE relay) |
| Voice & tone / microcopy | `mapping/uxd-to-voice-tone.md` | UXP voice & tone guidelines | `content-guidelines.md` steering |
| Multi-brand + dark-mode theming | `mapping/uxd-to-theming.md` | UXP `design/multi-brand-theming.md` | `theming.md` steering |
| i18n / RTL / localization | `mapping/uxd-to-i18n.md` | UXP i18n/RTL tokens | `i18n-standards.md` steering |

### New Templates (non-mapping outputs)

| Concern | Template File | Source Input | Generated Output |
|---------|--------------|-------------|-----------------|
| UI implementation spec (AI-DLC v1 input) | `templates/operational/ui-implementation-spec.md` | UXP wireframes + components + flows | `ui-implementation-spec.md` |
| Design system steering | `templates/steering/design-system.md` | UXP (via uxd-to-design-system mapping) | `design-system.md` |
| Code pattern examples | `templates/examples/README.md` | AP tech patterns + UXP UI patterns | `examples/` directory |

---

## Cross-Cutting Mechanisms

### Generation Modes

| Mode | When Used | Behavior |
|------|-----------|----------|
| **Full Generation** | First run (no existing workspace) | Detect present peer inputs, disclose quality impact, generate all present clusters |
| **Delta Reconciliation** | A peer input updated after initial generation | Detect changes, update only affected files, preserve customizations |
| **Brownfield Overlay** | Existing codebase without AI-DWG governance | Layer steering + non-conflicting docs onto existing project; never touch source code |

### Pre-Mode Gate

Before any mode executes, AI-DWG runs a two-phase gate:
- **Phase A — Peer-input selection:** scan markers, disclose quality impact if <3 inputs, get user approval
- **Phase B — Conflict surfacing:** if 2+ inputs present, detect contradictions, surface with root-cause analysis (hard gate — does not proceed until resolved)

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

→ `reconciliation/downstream-signaling.md`. When DWG generates or re-generates, it creates/updates the marker file (`.kiro/steering/workspace-rules.md`). AI-GCE detects this and knows the workspace changed. The signal includes a `Route: workspace-ready` intent field that tells the next package the generation is complete and what follow-up action is appropriate (Lesson 47 — forward-compatible routing).

### "How does DWG handle the Project ID?"

→ DWG reads the `Project ID` from `adlc-state.md` (or `pilc-state.md` if ADLC was skipped) and embeds it in the generated `workspace-rules.md` metadata. This makes the correlation key discoverable by AI-GCE without requiring it to read upstream state files directly (Lesson 39/43 — correlation key threading).

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

*Created: June 2026 | Package: AI-DWG v1.0 | Updated 2026-06-15: peer-input model (OI-049 convergence execution)*

---

## AI-DFE Data Interface (`ai-dwg-rule-details/data-schema/`)

This package ships a machine-readable data interface consumed by **AI-DFE** (the family data fabric). AI-DFE reads these files to gather this package's output into `{family}-ws/data/dwg-data.json`.

| File | Purpose |
|------|---------|
| `dwg-data.schema.json` | JSON Schema — the shape AI-DFE produces for this package |
| `SOURCE_MAP.md` | Declares where this package's raw output lives + field extraction rules |
| `SCHEMA_README.md` | Human documentation of the schema, fields, and consumers |

> These files do not change this package's runtime behavior — they are a read-only contract for the data fabric. See AI-DFE for how the data surface is gathered, shaped, and distributed.
