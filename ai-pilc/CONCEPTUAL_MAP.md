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
