# AI-POLC Conceptual Map

> **What this file is:** A navigational guide to AI-POLC's internal structure. It answers "where does each product ownership concern live?" and helps you find the right file across 6 phases and 16 stages.

---

## How to Read This

AI-POLC is an **interactive lifecycle workflow** with 6 phases containing 16 stages, plus Tier 2 (story elaboration) and 7 opt-in extensions. This map organizes files by *concern domain* — so you can find what you need based on what you're trying to accomplish.

**Key principle:** AI-POLC turns business intent into a prioritized, value-justified product backlog. Everything traces from vision → goals → epics → stories.

---

## Concern → Location Map

### Vision & Identity (Phase 1: Foundation)

| Concern | File | Purpose |
|---------|------|---------|
| Product vision & goals | `foundation/product-vision.md` | Distill business intent into measurable goals |
| PO charter & authority | `foundation/po-charter.md` | Decision boundaries, RACI, stakeholder authority |
| Workspace setup | `foundation/workspace-detection.md` | State file, folder structure, predecessor detection |

### Strategy & Planning (Phase 2: Strategy)

| Concern | File | Purpose |
|---------|------|---------|
| Product discovery & roadmap | `strategy/product-discovery.md` | Now/Next/Later strategic planning |
| Epic decomposition | `strategy/epic-decomposition.md` | Goal→epic mapping with acceptance criteria |
| Value-based prioritization | `strategy/value-prioritization.md` | WSJF, MoSCoW, value-effort with rationale |
| Release & increment slicing | `strategy/release-slicing.md` | MVP/MMP scope + delivery groupings |

### Quality & Risk (Phase 3: Governance)

| Concern | File | Purpose |
|---------|------|---------|
| Definition of Ready / Done | `governance/definition-of-ready-done.md` | Quality bar flowing to AI-DWG and AI-GCE |
| Product risk & assumptions | `governance/product-risk.md` | Product-level risk register |
| Traceability | `governance/traceability.md` | Intent→epic→release linkage |

### Stakeholders (Phase 4)

| Concern | File | Purpose |
|---------|------|---------|
| Stakeholder management | `stakeholders/stakeholder-management.md` | Power/interest matrix + communication cadence |
| Product documentation | `stakeholders/product-documentation.md` | Release notes and changelog governance |

### Package Assembly (Phase 5)

| Concern | File | Purpose |
|---------|------|---------|
| PBP consolidation | `assembly/pbp-assembly.md` | Final package assembly + cross-check |

### Operations (Phase 6: Continuous)

| Concern | File | Purpose |
|---------|------|---------|
| Backlog operations | `operations/backlog-operations.md` | Refinement, splitting criteria, tech-debt trade-offs |
| Acceptance & feedback | `operations/acceptance-feedback.md` | Increment acceptance against DoD, DLC feedback loop |
| Value & metrics | `operations/value-metrics.md` | KPI tracking and benefits measurement |

### Story Elaboration (Tier 2 — User-Activated)

| Concern | File | Purpose |
|---------|------|---------|
| INVEST-compliant stories | `tier2/story-elaboration.md` | Given/When/Then acceptance criteria; off by default in chain mode |

### Extensions (Opt-In)

| Extension | Files | When Needed |
|-----------|-------|-------------|
| Advanced Discovery | `extensions/advanced-discovery.opt-in.md` + `.md` | OKRs, JTBD, opportunity scoring |
| Full Traceability | `extensions/full-traceability.opt-in.md` + `.md` | Audit-grade matrix, compliance evidence |
| Full Risk Register | `extensions/full-risk-register.opt-in.md` + `.md` | Scoring, owners, response plans |
| Full Product Docs | `extensions/full-product-docs.opt-in.md` + `.md` | PRD, feature briefs, wiki governance |
| Quality Review | `extensions/quality-review.opt-in.md` + `.md` | Automated backlog quality scanning |
| MVP/MMP Mature | `extensions/mvp-mmp-mature.opt-in.md` + `.md` | Next-version scoping |

---

## Cross-Cutting Mechanisms

| Mechanism | Where Defined | How It Works |
|-----------|--------------|--------------|
| **Adaptive depth** | `core-workflow.md` | Minimal/Standard/Comprehensive — scales to product complexity |
| **Tier activation** | `core-workflow.md` | Tier 1 always; Tier 2 user-activated (L35) |
| **Identity spine** | `core-workflow.md` | "What/why/order = in; how/when-built/compliance = out" (L36) |
| **AI-DLC v1 bidirectional exchange** | `operations/acceptance-feedback.md` | POLC ⇄ DLC backlog/acceptance throughout delivery |
| **AI-UXD consumer** | `core-workflow.md` Chain Contract | Consumes personas/journeys from AI-UXD |
| **Session continuity** | `common/session-continuity.md` | `polc-state.md` preserves progress |
| **Governance spine (L45)** | `templates/management-framework.md` | Appends POLC-* entries to shared spine |

---

## Common Questions

### "Where does prioritization happen?"
→ `strategy/value-prioritization.md` — WSJF/MoSCoW/value-effort with recorded rationale.

### "How does AI-POLC connect to AI-DLC v1?"
→ `operations/acceptance-feedback.md` — bidirectional exchange (backlog forward, feedback back). Also see Chain Contract in `core-workflow.md`.

### "When should I activate Tier 2 (stories)?"
→ Activate in standalone mode (no AI-DLC v1) or for PO-quality pre-elaboration. In chain mode it's off by default because AI-DLC v1 handles story creation.

### "What's the difference between core and extensions?"
→ Core = 80% common case (always active). Extensions = 20% specialized needs (opt-in, blocking when active). See `extensions/README.md`.

### "How does AI-POLC feed AI-DWG?"
→ Produces PBP (Product Backlog Package) with `polc-state.md` marker. AI-DWG reads DoR/DoD + prioritization model for workspace steering enrichment.

---

*Created: 2026-06-12 | Lesson 30 compliance*

---

## AI-DFE Data Interface (`ai-polc-rule-details/data-schema/`)

This package ships a machine-readable data interface consumed by **AI-DFE** (the family data fabric). AI-DFE reads these files to gather this package's output into `{family}-ws/data/polc-data.json`.

| File | Purpose |
|------|---------|
| `polc-data.schema.json` | JSON Schema — the shape AI-DFE produces for this package |
| `SOURCE_MAP.md` | Declares where this package's raw output lives + field extraction rules |
| `SCHEMA_README.md` | Human documentation of the schema, fields, and consumers |

> These files do not change this package's runtime behavior — they are a read-only contract for the data fabric. See AI-DFE for how the data surface is gathered, shaped, and distributed.
