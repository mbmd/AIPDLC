# AI-PPM Conceptual Map

> **What this file is:** A navigational guide to AI-PPM's internal structure. It answers "where does each portfolio governance concern live?" and helps you find the right file across 5 phases and 10 stages.

---

## How to Read This

AI-PPM is an **adaptive portfolio engine** with 5 phases containing 10 stages, plus 7 opt-in extensions. Unlike lifecycle packages that complete, AI-PPM operates continuously — projects enter and exit over time. This map organizes files by *concern domain*.

**Key principle:** AI-PPM governs the SET of projects — never one project in isolation. Every decision is comparative, every view is aggregate.

---

## Concern → Location Map

### Portfolio Intake (Phase 1: Stages 1–2)

| Concern | File | Purpose |
|---------|------|---------|
| Portfolio detection & setup | `intake/portfolio-detection.md` | Detect existing portfolio state, resolve markers, initialize register |
| Project registration | `intake/project-registration.md` | Register a new project into the portfolio from PIP/Idea Brief |

### Strategic Alignment & Prioritization (Phase 2: Stages 3–4)

| Concern | File | Purpose |
|---------|------|---------|
| Strategic alignment scoring | `prioritization/strategic-alignment.md` | Map objectives × projects, score alignment |
| Cross-project prioritization | `prioritization/cross-project-prioritization.md` | Project-vs-project ranking, resource contention surfacing |

### Authorization & Dispatch (Phase 3: Stages 5–6)

| Concern | File | Purpose |
|---------|------|---------|
| Governance gate decisions | `authorization/governance-gate.md` | Admit/pause/retire decisions with rationale |
| Dispatch authorization | `authorization/dispatch-authorization.md` | Send authorization to Project layer via AI-FLO |

### Monitoring & Health (Phase 4: Stages 7–8)

| Concern | File | Purpose |
|---------|------|---------|
| Portfolio dashboards & views | `monitoring/portfolio-dashboards.md` | Aggregate health views, RAG status, trends |
| Roll-up telemetry ingestion | `monitoring/rollup-ingestion.md` | Read project-layer state via AI-FLO telemetry |

### Optimization (Phase 5: Stages 9–10)

| Concern | File | Purpose |
|---------|------|---------|
| Portfolio rebalancing | `optimization/portfolio-rebalancing.md` | Proposals when reality changes (budget shift, new priority) |
| Project retirement | `optimization/project-retirement.md` | Formal closure with lessons, benefit capture |

### Extensions (Opt-In)

| Extension | Folder | When Needed |
|-----------|--------|-------------|
| Portfolio Balancing & Visualization | `extensions/portfolio-balancing/` | >10 projects, visual portfolio views |
| What-If Scenario Modeling | `extensions/what-if-scenarios/` | Capacity constraints, scenario comparison |
| Cross-Project Dependency Mapping | `extensions/dependency-mapping/` | >5 projects, shared components |
| Capacity & Demand | `extensions/capacity-demand/` | Shared teams, resource contention |
| Investment Themes / Strategic Buckets | `extensions/investment-themes/` | Formal investment categories |
| Financial Governance | `extensions/financial-governance/` | Enterprise, budget tracking |
| Benefits Realization Aggregation | `extensions/benefits-aggregation/` | Projects completing, ROI tracking |

### Output Templates

| Template | Purpose |
|----------|---------|
| `templates/portfolio-register.md` | Master list of all projects |
| `templates/strategic-alignment-map.md` | Objectives × projects scoring |
| `templates/prioritization-scorecard.md` | Comparative ranking |
| `templates/governance-decision-record.md` | Admit/pause/retire decisions |
| `templates/dispatch-authorization.md` | FLO-carried authorization |
| `templates/portfolio-health-dashboard.md` | Aggregate health view |
| `templates/project-intake-card.md` | Per-project registration card |
| `templates/rebalancing-proposal.md` | Change proposal + impact |
| `templates/retirement-record.md` | Formal project closure |

---

## Cross-Cutting Mechanisms

| Mechanism | Where Defined | How It Works |
|-----------|--------------|--------------|
| **Layered communication (L53)** | `core-engine.md` | Cross-layer = via FLO; same-layer = direct marker read |
| **Continuous engine** | `core-engine.md` | No "workflow complete" — episodes: register, review, rebalance, retire |
| **Adaptive depth** | `core-engine.md` | Scales to portfolio size (≤3 / 4-10 / 10+) |
| **Correlation key** | `core-engine.md` | Project ID threads from PILC through chain — PPM uses it for addressable roll-up |
| **No duplication** | `core-engine.md` | PPM aggregates downstream data, never recomputes it |
| **Session continuity** | `common/session-continuity.md` | `ppm-state.md` preserves portfolio state |
| **Governance spine** | N/A (PPM excluded) | PPM has its own portfolio-scope registers — NOT the per-project spine (L45) |

---

## Common Questions

### "How does AI-PPM get project status?"
→ `monitoring/rollup-ingestion.md` — reads telemetry carried up by AI-FLO from project-layer state files. In manual/fallback mode, prompts user for status updates.

### "Does AI-PPM write to the per-project management_framework?"
→ No. AI-PPM is portfolio-scope — it has its own registers. The per-project spine (L45) is for project-touching packages only. PPM is explicitly excluded (see `MANAGEMENT_FRAMEWORK_CONTRACT.md` §5).

### "How does AI-PPM talk to AI-ADLC or AI-POLC?"
→ It doesn't — directly. Cross-layer communication ALWAYS goes through AI-FLO (L53). PPM dispatches authorization down via FLO; project packages send telemetry up via FLO.

### "What if AI-FLO doesn't exist yet?"
→ Fallback: user manually starts project-layer packages. PPM prompts user for manual status updates. Same-layer reads (PPM reads pilc-state.md, ilc-state.md) work regardless — they're direct marker reads.

### "When does PPM use extensions?"
→ Extensions activate based on portfolio complexity: >10 projects, capacity constraints, formal investment governance, etc. Each has an opt-in trigger documented in `extensions/README.md`.

---

*Created: 2026-06-12 | Lesson 30 compliance*

---

## AI-DFE Data Interface (`ai-ppm-rule-details/data-schema/`)

This package ships a machine-readable data interface consumed by **AI-DFE** (the family data fabric). AI-DFE reads these files to gather this package's output into `{family}-ws/data/ppm-data.json`.

| File | Purpose |
|------|---------|
| `ppm-data.schema.json` | JSON Schema — the shape AI-DFE produces for this package |
| `SOURCE_MAP.md` | Declares where this package's raw output lives + field extraction rules |
| `SCHEMA_README.md` | Human documentation of the schema, fields, and consumers |

> These files do not change this package's runtime behavior — they are a read-only contract for the data fabric. See AI-DFE for how the data surface is gathered, shaped, and distributed.
