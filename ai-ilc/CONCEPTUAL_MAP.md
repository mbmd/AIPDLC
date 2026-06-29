# AI-ILC Conceptual Map

> **What this file is:** A navigational guide to AI-ILC's internal structure. It answers "where does each idea-lifecycle concern live?" and helps you find the right file without reading all stage details.

---

## How to Read This

AI-ILC is an **interactive lifecycle workflow** with 6 stages, each handling a distinct phase of idea evaluation. This map organizes files by *concern domain* — so you can find what you need based on what you're trying to understand or accomplish.

**Key principle:** Ideas enter raw, exit as governed briefs routed to the right destination. Every decision is logged, every score is rationale-backed.

---

## Concern → Location Map

### Idea Capture & Shaping

| Concern | File | Purpose |
|---------|------|---------|
| Initial idea intake | `idea-lifecycle/capture.md` | Capture raw idea, create register entry, mint Idea ID |
| Ambiguity resolution | `idea-lifecycle/shape.md` | Decompose, detect gaps, build problem/solution clarity |
| Question formatting | `common/question-format-guide.md` | How to structure questions at any stage |

### Evaluation & Scoring

| Concern | File | Purpose |
|---------|------|---------|
| Multi-dimension scoring | `idea-lifecycle/evaluate.md` | Strategic alignment, feasibility, value, urgency scoring |
| Scoping & boundaries | `idea-lifecycle/scope.md` | WBS-like boundary setting, effort estimation, dependencies |
| Content quality checks | `common/content-validation.md` | Validation rules for all output artifacts |

### Decision & Approval

| Concern | File | Purpose |
|---------|------|---------|
| Go/No-Go gate | `idea-lifecycle/approve.md` | Formal approval, park, or reject with rationale |
| Decision record template | `templates/decision-record.md` | Template for the formal decision artifact |

### Routing & Handoff

| Concern | File | Purpose |
|---------|------|---------|
| Route determination | `idea-lifecycle/route-handoff.md` | Impact-driven routing to PILC/POLC/DLC + brief assembly |
| Forward-compatible routing | `core-workflow.md` → Chain Contract | Intent-based routing (L47) with preferred/fallback resolution |
| Portfolio connector | `connectors/portfolio-connector.md` | Integration with AI-PPM portfolio funnel |

### Output Templates (what gets produced)

| Concern | Template | When Produced |
|---------|----------|---------------|
| New project approved | `templates/approved-idea-brief.md` | Route = `new-project` |
| Feature for backlog | `templates/feature-brief.md` | Route = `feature` |
| Change to existing project | `templates/change-request-brief.md` | Route = `change-request` |
| Idea register entry | `templates/idea-entry.md` | Always (every idea) |
| Portfolio-level register | `templates/idea-register.md` | Always (funnel view) |
| State/marker file | `templates/ilc-state.md` | Always |
| Governance spine | `templates/management-framework.md` | Always (L45 compliant) |

### Governance & Quality

| Concern | File | Purpose |
|---------|------|---------|
| Quality validation agent | `templates/agents/idea-quality-agent.md` | IQC__ — 13 checks across 4 categories |
| Agent shortcut injection | `templates/agents/shortcut-rules-block.md` | Workspace-rules append block |
| Agent user guide | `templates/agents/agent-guide.md` | AGENT-GUIDE.md section |

---

## Cross-Cutting Mechanisms

| Mechanism | Where Defined | How It Works |
|-----------|--------------|--------------|
| **Adaptive depth** | `core-workflow.md` | Minimal/Standard/Comprehensive — scales to idea complexity |
| **Dynamic persona selection** | `core-workflow.md` → Stage→Persona Map | Different expert leads each stage; domain detection adds sub-roles |
| **Session continuity** | `common/session-continuity.md` | `ilc-state.md` preserves progress across sessions |
| **OR-input (L6)** | `core-workflow.md` → Chain Contract | Works standalone or after AI-PPM/portfolio context |
| **Per-idea output folders** | `core-workflow.md` → Output Folder Structure | Per-idea artifacts under `{NNN}-{slug}/` (keyed by stable Register ID); shared state/register/spine stay flat; status in metadata + Register, never in folder names (Lesson 40) |
| **Intent-based routing (L47)** | `core-workflow.md` → Chain Contract | Route field carries semantic intent, not hardcoded targets |
| **Governance spine (L45)** | `templates/management-framework.md` | Appends ILC-* entries to shared spine if present |

---

## Common Questions

### "Where does idea scoring happen?"
→ `idea-lifecycle/evaluate.md` — multi-dimension scoring with rationale per dimension.

### "How does AI-ILC decide where to route an idea?"
→ `idea-lifecycle/route-handoff.md` — impact-driven routing logic (big change = project, small = feature, existing system change = change-request).

### "What if the target package doesn't exist yet (e.g., AI-POLC)?"
→ `core-workflow.md` Chain Contract — intent-based routing with fallback resolution. Route writes intent; resolution happens on the consuming side (L47).

### "Does AI-ILC install a governance agent?"
→ Yes. `templates/agents/idea-quality-agent.md` (IQC__) validates brief completeness, scoring integrity, routing quality, and governance records. Installed during first workflow run.

### "How does AI-ILC relate to AI-PPM?"
→ `connectors/portfolio-connector.md` — AI-PPM reads Approved Idea Briefs directly (same Portfolio layer). AI-ILC is the funnel; AI-PPM is the portfolio governor.

---

*Created: 2026-06-12 | Lesson 30 compliance*

---

## AI-DFE Data Interface (`ai-ilc-rule-details/data-schema/`)

This package ships a machine-readable data interface consumed by **AI-DFE** (the family data fabric). AI-DFE reads these files to gather this package's output into `{family}-ws/data/ilc-data.json`.

| File | Purpose |
|------|---------|
| `ilc-data.schema.json` | JSON Schema — the shape AI-DFE produces for this package |
| `SOURCE_MAP.md` | Declares where this package's raw output lives + field extraction rules |
| `SCHEMA_README.md` | Human documentation of the schema, fields, and consumers |

> These files do not change this package's runtime behavior — they are a read-only contract for the data fabric. See AI-DFE for how the data surface is gathered, shaped, and distributed.
