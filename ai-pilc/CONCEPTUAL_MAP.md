# AI-PILC Conceptual Map

> **What this file is:** A navigational guide to AI-PILC's internal structure. It answers "where does each project initiation concern live?" and helps you find the right file without reading the entire core-workflow.

---

## How to Read This

AI-PILC is an **interactive lifecycle workflow** with 6 phases, each containing 1-5 stages. Every stage has a dedicated detail file that defines its logic, questions, deliverable, and gate. This map organizes those stages by *concern domain* — so you can find what governs a specific initiation activity.

**Key principle:** AI-PILC produces a Project Initiation Package (PIP) — the complete governance foundation for a project. Every stage contributes one deliverable to that package.

---

## Concern → Location Map

### Requirements & Scope

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Raw requirement ingestion | Inception | `inception/source-ingestion.md` | Structured requirement intake |
| Requirement structuring | Inception | `inception/requirement-structuring.md` | Categorized requirements |
| Requirements analysis & gaps | Assessment | `assessment/requirements-analysis.md` | Requirements analysis report |
| Scope definition & boundaries | Planning | `planning/scope-definition.md` | Scope statement |

### Feasibility & Assessment

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Clarification cycles (Q&A) | Assessment | `assessment/clarification-cycle.md` | Resolved ambiguities |
| Feasibility analysis | Assessment | `assessment/feasibility-assessment.md` | Feasibility assessment |
| Prioritization (MoSCoW, etc.) | Assessment | `assessment/prioritization.md` | Prioritized requirements |

### Business Justification

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Business case construction | Justification | `justification/business-case.md` | Business case document |

### Planning & Governance

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Stakeholder identification & RACI | Planning | `planning/stakeholder-management.md` | Stakeholder register + RACI |
| Risk identification & mitigation | Planning | `planning/risk-management.md` | Risk register |
| Resource & budget estimation | Planning | `planning/resource-budget.md` | Resource plan |
| Governance & communication plan | Planning | `planning/governance-communication.md` | Governance framework |

### Authorization

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Project charter creation | Authorization | `authorization/project-charter.md` | Project charter (formal approval) |

### Mobilization & Handoff

| Concern | Phase | Stage File | Deliverable |
|---------|-------|-----------|-------------|
| Kickoff preparation | Mobilization | `mobilization/kickoff-preparation.md` | Kickoff agenda + materials |
| Package assembly & handoff | Mobilization | `mobilization/package-assembly.md` | Complete PIP (assembled) |

### Workspace & Session Management

| Concern | Phase | Stage File | Purpose |
|---------|-------|-----------|---------|
| Workspace detection & setup | Inception | `inception/workspace-detection.md` | Detect/create output folder structure |
| Session continuity | Common | `common/session-continuity.md` | Resume logic, state management |
| Content validation | Common | `common/content-validation.md` | Quality rules for all deliverables |

---

## Cross-Cutting Mechanisms

### Phase Flow

```
Inception → Assessment → Justification → Planning → Authorization → Mobilization
    │            │             │              │            │              │
    │            │             │              │            │              └── Assemble & hand off
    │            │             │              │            └── Formal approval gate
    │            │             │              └── Plan the work
    │            │             └── Justify the investment
    │            └── Analyze & validate
    └── Capture & structure
```

### Adaptive Depth

| Depth Level | When Applied | Effect |
|-------------|-------------|--------|
| Minimal | Simple/clear input, small project | Fewer questions, shorter deliverables |
| Standard | Normal complexity | Full phase execution |
| Comprehensive | High complexity, many unknowns | Extended analysis, multiple iterations |

### Gate Model

Every stage ends with a gate — user must approve before proceeding. The gate presents:
1. Summary of what was produced
2. Explicit approval request
3. Option to revise or skip (where allowed)

### Templates (Deliverable Structures)

All 16 templates live in `templates/` — one per PIP deliverable. They define the exact structure of each output document (generic, `{placeholder}` based).

---

## Common Questions

### "Where do requirements get captured?"

→ `inception/source-ingestion.md` handles raw input. `inception/requirement-structuring.md` categorizes them. `assessment/requirements-analysis.md` analyzes gaps and conflicts.

### "Where is the business case built?"

→ `justification/business-case.md` — single stage, single deliverable. Uses data from Assessment phase (feasibility + prioritization) as input.

### "Where does formal approval happen?"

→ `authorization/project-charter.md` — the gate here is the formal project authorization. Everything before this is preparation; this is the decision point.

### "What's the final output?"

→ `mobilization/package-assembly.md` assembles all deliverables into the Project Initiation Package (PIP). This is what AI-ADLC receives as its input.

### "Where is session state managed?"

→ `common/session-continuity.md` defines the `pilc-state.md` file structure, resume flow, and edge cases for interrupted sessions.

### "How does Project ID work?"

→ Project ID is minted at Stage 1 (Workspace Detection) as `PRJ-{YYYYMMDD}-{NNN}` and written to `pilc-state.md` immediately. It's immutable — Stage 9 (Charter) references the existing ID rather than creating a new one. The correlation key threads through the entire chain: ADLC reads it, DWG embeds it, GCE logs it. (correlation-key threading — one immutable ID carried across every package)

### "What is the Route field in pilc-state.md?"

→ `pilc-state.md` carries a `Route: project` intent field (forward-compatible routing). This tells downstream packages what kind of output PILC produced and what follow-up action is appropriate. Today only one value exists, but the field is forward-declared so future routing logic (e.g., AI-FLO) can read it without requiring PILC changes.

### "Does AI-PILC install a governance agent?"

→ Yes. After PIP completion, AI-PILC **automatically** installs the `initiation-quality-agent` into `.kiro/agents/`. This agent validates PIP output quality (completeness, gate compliance, stakeholder coverage, register integrity, cross-references). Triggered by shortcut `IQA__`. The installation is self-sufficient — no dependency on AI-GCE being present (per AGENT_GOVERNANCE_CONTRACT §5). See `templates/agents/initiation-quality-agent.md` for the full check set, `templates/agents/shortcut-rules-block.md` for the workspace-rules injection, and `templates/agents/agent-guide.md` for the user-facing documentation section.

### "How does traceability work when AI-PILC receives an ILC brief (Mode E)?"

→ Per `TRACEABILITY_CONTRACT.md` §4-C, when AI-PILC ingests an Approved Idea Brief from AI-ILC (Mode E intake), the PIP output **MUST** carry `derivedFrom: {idea-brief-id}` in its front-matter. This is enforced in `inception/source-ingestion.md` (Mode E extraction step). The stamp creates a provenance edge from the idea that spawned the project — ensuring the PIP can always trace back to its ILC origin. This is REQUIRED (not optional) when ILC intake is detected.

---

## File Relationships

```
CONCEPTUAL_MAP.md  ← You are here (navigation)
README.md          ← What this package does (external audience)
WHITEPAPER.md      ← Theory and methodology (deep dive)
core-workflow.md   ← How it executes (runtime orchestration)
```

---

*Created: June 2026 | Package: AI-PILC v1.1*

---

## AI-DFE Data Interface (`ai-pilc-rule-details/data-schema/`)

This package ships a machine-readable data interface consumed by **AI-DFE** (the family data fabric). AI-DFE reads these files to gather this package's output into `{family}-ws/data/pilc-data.json`.

| File | Purpose |
|------|---------|
| `pilc-data.schema.json` | JSON Schema — the shape AI-DFE produces for this package |
| `SOURCE_MAP.md` | Declares where this package's raw output lives + field extraction rules |
| `SCHEMA_README.md` | Human documentation of the schema, fields, and consumers |

> These files do not change this package's runtime behavior — they are a read-only contract for the data fabric. See AI-DFE for how the data surface is gathered, shaped, and distributed.
