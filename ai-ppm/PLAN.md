# AI-PPM — Package Build Plan

**Version:** 1.0.0
**Date:** 2026-06-11
**Author:** Maheri
**Status:** BUILT — Steps 1-10 complete. Awaiting dry test (Step 11) and family table registration (Step 12).
**Persona:** `#persona-pmo-project-manager` (primary) — Portfolio / Programme Management expert

---

## 1. Package Identity

| Field | Value |
|-------|-------|
| **Name** | AI-PPM *(challenged per Lesson 12; "PPM" = universal industry term for Project Portfolio Management — accurate, memorable, no product clash; alternative considered: AI-PGE "Portfolio Governance Engine" — rejected as less recognizable)* |
| **Full Title** | AI-Driven Project Portfolio Management |
| **Package Type** | Adaptive portfolio engine (continuous — not a one-pass lifecycle) |
| **Primary Input** | Multiple Project Initiation Packages (PIP) from AI-PILC + Approved Idea Briefs from AI-ILC + FLO-carried roll-up snapshots from Project layer |
| **Primary Output** | Portfolio Register + cross-project prioritization + portfolio governance decisions + dispatch authorizations + portfolio dashboards |
| **User Persona** | Portfolio / Programme Manager, PMO lead, Head of Delivery |
| **Family Position** | Top of the Portfolio layer: `AI-ILC ⇢ AI-PILC ⇢ AI-PPM`; feeds AI-FLO (downward dispatch) |
| **Marker File** | `ppm-state.md` |

---

## 2. The AI-* Family

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

    AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG ──► AI-DLC v1 (build) ¹
    Own it      Design UX   Design it   Prepare it       ▲
                                                         │
                        AI-POLC ⇄ AI-DLC v1 (back-and-forth)┘
                AI-DLC v1 ⇢ AI-UXD+AI-POLC (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC v1 (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC v1 = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-POLC** ³ | Interactive workflow (lifecycle) | PIP | Product Backlog Package (PBP) |
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP + PBP | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | PIP + PBP + UXP | Architecture Package (AP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC v1** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POLC) | Working Software |

> ¹ **AI-DLC v1** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC v1 consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ All packages in this table are **built**. AI-PPM (portfolio engine), AI-FLO (router), AI-POLC (product ownership lifecycle), and AI-UXD (UX design lifecycle) were the last four — completed June 2026. Within the Project layer, **AI-POLC, AI-UXD, and AI-ADLC run sequentially** (POLC→UXD→ADLC) — each feeds the next, culminating at AI-DWG which receives all three outputs (AP + PBP + UXP). **AI-GCE and AI-TGE run alongside AI-DLC v1** as continuous quality engines; **AI-POLC ⇄ AI-DLC v1** exchange backlog/acceptance throughout delivery; and **AI-DLC v1 runtime feedback flows back to both AI-UXD and AI-POLC**. Feedback loops (ADLC→POLC cost/risk, ADLC→UXD constraints) provide iterative refinement without changing the forward sequence.

---

## 3. Data Architecture — Layered Communication Model

### The Routing Rule

> **Cross-layer communication MUST go through AI-FLO. Same-layer communication is direct (marker-based).**

This is the family's fundamental communication law:
- Packages in the **same layer** talk directly via marker file detection (current design, unchanged)
- Packages in **different layers** communicate exclusively through AI-FLO (the layer-boundary courier)

AI-PPM does NOT duplicate per-project logic. It reads Portfolio-layer siblings directly (AI-PILC, AI-ILC) and receives Project-layer data exclusively via AI-FLO.

### Communication Map

```
╔════════════ PORTFOLIO LAYER ════════════════════════╗
║                                                      ║
║  AI-ILC ──direct──► AI-PILC ──direct──► AI-PPM      ║
║    │                                      │ ▲        ║
║    └──────────── direct ──────────────────┘ │        ║
║                                               │        ║
╚═══════════════════════════╤═══════════════════╝        ║
                            │ ▲                           
              (down via FLO)│ │(up via FLO)              
                            ▼ │                           
                         AI-FLO                           
                            │ ▲                           
              (down via FLO)│ │(up via FLO)              
                            ▼ │                           
╔════════════ PROJECT LAYER ════════════════════════════╗
║                                                        ║
║  ADLC ──direct──┐                                     ║
║  UXD  ──direct──┼──► DWG ──direct──► GCE + TGE       ║
║  POLC ──direct──┘         ──direct──► DLC             ║
║                                                        ║
║  POLC ⇄ DLC (direct bidirectional)                    ║
║  UXD → POLC (direct)                                  ║
║  DLC → UXD + POLC (direct feedback)                   ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

### What AI-PPM Reads — Two Channels

| Channel | Source | Mechanism | What PPM Gets |
|---|---|---|---|
| **Direct (same layer)** | AI-PILC | Read `pilc-state.md` marker | Project ID, charter summary, budget, timeline, risks, priority |
| **Direct (same layer)** | AI-ILC | Read `ilc-state.md` marker | Idea evaluation score, routing decision, effort estimate |
| **Via FLO (cross layer)** | Project Layer packages | FLO-carried roll-up payload | Health, progress, financials, risks, compliance, velocity |

### What AI-PPM Sends — Two Channels

| Channel | Target | Mechanism | What PPM Sends |
|---|---|---|---|
| **Direct (same layer)** | AI-ILC, AI-PILC | They read PPM's portfolio context if needed | Portfolio priority, capacity constraints |
| **Via FLO (cross layer)** | Project Layer | Dispatch Authorization carried by FLO | Project ID, priority, scope, constraints, required packages |

### FLO's Role (Cross-Layer Only)

AI-FLO operates EXCLUSIVELY on the edge between layers:

| Direction | What FLO Carries |
|---|---|
| **DOWN (Portfolio → Project)** | Dispatch authorization (PPM authorizes → FLO activates Project-layer packages) |
| **UP (Project → Portfolio)** | Roll-up payload per Project ID (health, progress, financials, compliance, velocity) |

FLO does NOT mediate:
- ILC → PILC (same layer — direct)
- PILC → PPM (same layer — direct)
- ADLC → DWG (same layer — direct)
- POLC ⇄ DLC (same layer — direct)

### Fallback Mode (No FLO Installed)

When AI-FLO is not installed:
- **Same-layer communication:** Unchanged (always direct)
- **Cross-layer downward:** User manually starts Project-layer packages pointing at the PIP (current behavior)
- **Cross-layer upward:** PPM prompts user for manual status updates per project (no automated roll-up)

### Dashboard Data Contract (What PPM Expects from FLO)

PPM consumes FLO-carried roll-up payloads to render portfolio dashboards. Each payload is keyed by `Project ID` and contains slices from every Project-layer package that has touched that project:

| Dashboard View | Source Slice | Source Package |
|---|---|---|
| Portfolio Health Summary | phase, progress_pct, rag_status | Project state files |
| Financial Summary | budget_planned, budget_actual, roi_estimate, npv | AI-PILC Business Case ¹ |
| Resource Heatmap | team_size, key_roles, allocation_pct | AI-PILC Resource Plan ¹ |
| Benefits Realization | benefits_realized_pct, kpi_actuals | AI-POLC Stage 16 |
| Risk Heat Map | top_risks[], exposure_score, risk_trend | AI-PILC ¹ + POLC + Spine |
| Progress Tracker | milestones[], completion_predicted | AI-DLC v1 / state files |
| Quality Posture | compliance_score, test_coverage_pct, violations | AI-GCE + AI-TGE |
| Demand Pipeline | ideas_in_funnel, approved_pending | AI-ILC ² |
| Backlog Health | backlog_size, stale_items, refinement_state | AI-POLC Stage 14 |
| Tech Health | adr_count, tech_debt_flags | AI-ADLC |
| Blockers & Escalation | open_issues, severity_distribution | Governance Spine |

> ¹ AI-PILC is Portfolio layer — PPM reads its PIP data **directly** at registration time. However, budget/resource ACTUALS (vs. planned) come from the Project layer via FLO as the project progresses.
> ² AI-ILC is Portfolio layer — PPM reads its pipeline stats **directly**.

---

## 4. Scope: Core Stages

| Phase | # | Stage | Key Output |
|-------|---|-------|------------|
| **INTAKE** | 1 | Portfolio Detection & Initialization | ppm-state.md established, Portfolio Register located/created |
| | 2 | Project Registration | New project entry in Portfolio Register (from PIP or Idea Brief) |
| **PRIORITIZATION & ALIGNMENT** | 3 | Strategic Alignment | Org strategy → investment categories mapped; each project aligned |
| | 4 | Cross-Project Prioritization | Project-vs-project ranking with explicit model + rationale |
| **AUTHORIZATION & DISPATCH** | 5 | Portfolio Governance Gate | Admit / Pause / Resume / Retire decision with audit trail |
| | 6 | Dispatch Authorization | Authorization token → AI-FLO for downward execution |
| **MONITORING & DASHBOARDS** | 7 | Roll-Up Ingestion | Read FLO-carried snapshots; refresh Portfolio Register data |
| | 8 | Portfolio Health & Dashboards | Aggregate cross-project view; surface patterns & alerts |
| **OPTIMIZATION** | 9 | Portfolio Rebalancing | Adjust priorities, investment allocation based on actuals |
| | 10 | Project Retirement & Closure | Formal exit: close, archive, capture lessons, release resources |

---

## 5. Scope: Extensions (Opt-In)

| # | Extension | Trigger | What It Adds |
|---|---|---|---|
| E1 | **Portfolio Balancing & Visualization** | "balance" / "portfolio mix" / >10 projects / Comprehensive depth | Bubble charts, horizon distribution, risk-spread analysis, balance guardrails |
| E2 | **What-If Scenario Modeling** | "what-if" / "scenario" / capacity constraints detected | Scenario comparison, trade-off analysis, impact prediction |
| E3 | **Cross-Project Dependency Mapping** | >5 projects / shared resources detected / "dependencies" | Full dependency graph, critical path across projects, blocked-by chains |
| E4 | **Portfolio-Level Capacity & Demand** | "capacity" / "resource contention" / >3 projects sharing teams | Resource supply vs. demand visualization, over-allocation alerts |
| E5 | **Investment Themes / Strategic Buckets** | "investment themes" / "strategic buckets" / formal budget categories | Budget allocation by category (growth/run/innovate/compliance), enforcement |
| E6 | **Financial Governance** | "budget" / "funding" / "financial governance" / enterprise context | Lean budgeting, funding guardrails, portfolio-level ROI tracking |
| E7 | **Benefits Realization Aggregation** | "benefits" / "value realized" / projects completing | Cross-project benefits tracking, portfolio value-delivered vs. promised |

---

## 6. Scope Exclusions — What We Don't Cover (and Why)

### 6.1 Features Descoped to Other Packages (Data Surfaced via FLO)

These capabilities **already exist** in downstream packages. AI-PPM descopes their logic but receives their data through FLO-carried roll-ups for dashboard presentation:

| Feature | Lives In | Why Not in PPM | PPM Still Gets |
|---|---|---|---|
| Per-project value/priority scoring | AI-POLC Stage 6 | POLC already does WSJF/MoSCoW per product | Score via FLO → Portfolio Prioritization Matrix |
| Per-project resource planning | AI-PILC Stage 12 | PILC plans one project's team/budget | Actuals via FLO → Resource Heatmap |
| Per-project ROI/financial analysis | AI-PILC Stage 8 | PILC Business Case covers this completely | NPV/ROI via FLO → Financial Summary |
| Per-project benefits tracking | AI-POLC Stage 16 (ext) | POLC tracks per-product KPIs | Benefits data via FLO → Benefits Realization |
| Per-project risk register | AI-PILC Stage 13 + POLC Stage 9 | Each package manages its own risks | Top risks via FLO → Risk Heat Map |
| Idea evaluation & scoring | AI-ILC Stages 2-3 | ILC is the demand triage engine | Pipeline stats via FLO → Demand Pipeline |
| Governance hooks/enforcement | AI-GCE | Runtime compliance is GCE's domain | Compliance score via FLO → Quality Posture |
| Per-project governance spine | MANAGEMENT_FRAMEWORK_CONTRACT | Spine is cross-package shared artifact | Issues/decisions via FLO → Blockers |

### 6.2 Patterns Deliberately Not Covered (with Rationale)

| # | Pattern | What It Is | Why Excluded | Risk of Not Covering | Future Path |
|---|---|---|---|---|---|
| 1 | **Programme/Program Grouping** | Cluster related projects into programmes sharing objectives/benefits | PPM treats projects as atomic units. Programme management is a distinct discipline with its own governance layer (MSP/MoP Programme level). Adding it conflates two levels of management. | Low — most users run flat portfolios. Those needing programme management typically use dedicated programme tools. | Future: AI-PPM extension ("Programme Mode") or separate package |
| 2 | **Monte Carlo / Probabilistic Forecasting** | Statistical simulation across portfolio schedule/budget for confidence intervals | Requires a computational engine — beyond what a markdown-based AI governance tool can meaningfully execute. The AI can't run 10,000 simulations. | No risk — this is tooling-dependent (Crystal Ball, @Risk, Planisware). PPM can recommend users run simulations externally. | Reference in user guide as "external tooling recommended for…" |
| 3 | **Portfolio Communication / Audience-Specific Views** | Different dashboard formats per audience (C-suite vs. PMO vs. team leads) | PPM produces one canonical dashboard format. Multi-audience rendering is a presentation concern, not a governance concern. | Low — users can manually extract relevant sections for different audiences. | Future: Extension E8 ("Audience Adaptation") — generate tailored report variants |
| 4 | **Organizational Change Impact Assessment** | How portfolio decisions cascade as organizational restructuring, role changes, culture shifts | This is change management discipline (Prosci/ADKAR), not portfolio governance. Different expertise domain, different deliverables, different lifecycle. | No risk — adjacent discipline. PPM identifies *what* changes; OCM handles *how* the organization adapts. | Outside AI-* family scope. Different problem space. |
| 5 | **Portfolio Maturity Model** | Progressive adoption: L1 (inventory) → L2 (prioritized) → L3 (optimized) → L4 (strategic) | AI-PPM *is* the tool. It doesn't assess organizational maturity in using PPM — it just operates at whatever level the user engages. Depth Levels (Minimal/Standard/Comprehensive) serve this purpose implicitly. | No risk — depth adaptation already handles "we're not ready for the advanced stuff." | Depth Levels cover this naturally |
| 6 | **Lean Funding Model (SAFe full)** | Replace project-based funding with value-stream-based persistent-team funding | AI-PPM uses project-as-unit model (matches AI-PILC PIP output). Lean funding requires fundamentally different structural assumptions (no projects — just value streams with persistent teams). Supporting both paradigms would double the package complexity. | Medium — SAFe shops expect this. Mitigated by Extension E6 (Financial Governance) which includes lean budget guardrails. | Extension E6 covers guardrails. Full value-stream funding is a paradigm choice that restructures the entire chain, not just PPM. |
| 7 | **Portfolio Kanban Board (Full SAFe)** | Visual board with WIP limits, Funnel→Reviewing→Analyzing→Backlog→Implementing→Done flow states | AI-PPM uses governance-gate model (admit/pause/resume/retire), not a continuous-flow kanban model. The state model in `ppm-state.md` uses portfolio lifecycle states that are functionally similar but governance-framed rather than flow-framed. | Medium — SAFe practitioners notice the vocabulary difference. Mitigated by the fact that our states map conceptually to kanban columns (Registered≈Funnel, Prioritized≈Reviewing, Authorized≈Implementing, Retired≈Done). | Could adopt kanban vocabulary as an alias layer in `ppm-state.md`. Extension possible. |
| 8 | **Epic Hypothesis / Lean Business Case (pre-project)** | Lightweight "hypothesis → MVP → measure → pivot/persist" before initiatives become full projects | AI-ILC's Shape+Evaluate covers lightweight evaluation. AI-PILC Business Case is the full version. The gap is specifically the *experiment step* between them — running a small bet to validate before committing. | Low — most orgs skip this or do it informally. Those who practice it have their own experimentation frameworks. | Future: AI-ILC extension ("Lean Validation") — add hypothesis → experiment → measure before routing to PILC |
| 9 | **Three Horizons Distribution Enforcement** | Actively enforce that portfolio maintains a specific ratio (e.g., 70/20/10 across H1/H2/H3) | Extension E1 (Portfolio Balancing) covers *visualization* of horizon distribution. Enforcement (reject projects that break the ratio) is a guardrail that could live in the governance gate. | Low — visualization is usually sufficient. Hard enforcement is controversial even in theory (do you reject a critical H1 project because H1 is "full"?). | Fold into Extension E1 as optional balance guardrail within Stage 5 (governance gate) |
| 10 | **Sensitivity Analysis** | "Which assumptions, if wrong, would flip the portfolio ranking?" | Related to what-if scenarios (E2) but specifically about identifying *fragile assumptions* across the prioritization model. | Low — sophisticated analysis. Extension E2 (What-If) covers the mechanics; sensitivity is a specific application of it. | Sub-step within Extension E2 |
| 11 | **Cross-Portfolio Management (Portfolio of Portfolios)** | Enterprise with multiple business units, each with their own portfolio — rolled up to enterprise level | AI-PPM manages ONE portfolio. Multi-portfolio enterprise governance is a layer above that serves CIOs/CEOs managing multiple PMOs. Extremely niche — most organizations have one portfolio. | Very low — only relevant for large enterprises with divisional PMOs. | Not planned. Would need "AI-EPM" (Enterprise Portfolio Management) or PPM nesting — if ever demanded. |
| 12 | **Transition Planning (Project → BAU)** | Governance of how a completed project transitions into business-as-usual operations | Stage 10 (Project Retirement) captures closure and resource release. But the detailed handover-to-operations process (training, support setup, warranty period, operational readiness) is service management, not portfolio governance. | Low — PPM records that a project closed. The mechanics of transitioning to operations is an ITIL/service-management concern. | Adjacent to Stage 10. Could be a sub-step there or left to ITIL tooling. |

### 6.3 Risk Summary

| Risk Level | Pattern Count | Mitigation |
|---|---|---|
| **No risk** | #2, #4, #5, #11, #12 (5 patterns) | Outside scope by nature — different discipline, external tooling, or edge case |
| **Low risk** | #1, #3, #8, #9, #10 (5 patterns) | Covered implicitly or by extensions; users won't miss them |
| **Medium risk** | #6, #7 (2 patterns) | SAFe practitioners may notice. Extension E6 + state-model vocabulary mitigates |

**Overall coverage estimate:** ~85-90% of established PPM patterns covered by core + extensions + FLO-carried dashboards. Remaining 10-15% is paradigm choices, external tooling, or adjacent disciplines.

---

## 7. Phase & Stage Structure

```
Phase 1: INTAKE (Project enters the portfolio)
  Stage 1: Portfolio Detection & Initialization
  Stage 2: Project Registration

Phase 2: PRIORITIZATION & ALIGNMENT (Rank and position)
  Stage 3: Strategic Alignment
  Stage 4: Cross-Project Prioritization

Phase 3: AUTHORIZATION & DISPATCH (Govern what proceeds)
  Stage 5: Portfolio Governance Gate
  Stage 6: Dispatch Authorization (→ AI-FLO)

Phase 4: MONITORING & DASHBOARDS (Ongoing portfolio health)
  Stage 7: Roll-Up Ingestion
  Stage 8: Portfolio Health & Dashboards

Phase 5: OPTIMIZATION (Rebalance and evolve)
  Stage 9: Portfolio Rebalancing
  Stage 10: Project Retirement & Closure
```

---

## 8. File Structure

```
ai-ppm/
├── README.md
├── LICENSE
├── PLAN.md                              ← This file
├── ai-ppm-rules/
│   └── core-engine.md                   ← Master orchestration
├── ai-ppm-rule-details/
│   ├── common/
│   │   ├── process-overview.md
│   │   ├── session-continuity.md
│   │   ├── question-format-guide.md
│   │   ├── content-validation.md
│   │   └── welcome-message.md
│   ├── intake/                          ← Phase 1
│   │   ├── portfolio-detection.md
│   │   └── project-registration.md
│   ├── prioritization/                  ← Phase 2
│   │   ├── strategic-alignment.md
│   │   └── cross-project-prioritization.md
│   ├── authorization/                   ← Phase 3
│   │   ├── governance-gate.md
│   │   └── dispatch-authorization.md
│   ├── monitoring/                      ← Phase 4
│   │   ├── rollup-ingestion.md
│   │   └── portfolio-dashboards.md
│   ├── optimization/                    ← Phase 5
│   │   ├── portfolio-rebalancing.md
│   │   └── project-retirement.md
│   ├── extensions/
│   │   ├── README.md
│   │   ├── portfolio-balancing/
│   │   │   ├── portfolio-balancing.opt-in.md
│   │   │   └── portfolio-balancing.md
│   │   ├── what-if-scenarios/
│   │   │   ├── what-if-scenarios.opt-in.md
│   │   │   └── what-if-scenarios.md
│   │   ├── dependency-mapping/
│   │   │   ├── dependency-mapping.opt-in.md
│   │   │   └── dependency-mapping.md
│   │   ├── capacity-demand/
│   │   │   ├── capacity-demand.opt-in.md
│   │   │   └── capacity-demand.md
│   │   ├── investment-themes/
│   │   │   ├── investment-themes.opt-in.md
│   │   │   └── investment-themes.md
│   │   ├── financial-governance/
│   │   │   ├── financial-governance.opt-in.md
│   │   │   └── financial-governance.md
│   │   └── benefits-aggregation/
│   │       ├── benefits-aggregation.opt-in.md
│   │       └── benefits-aggregation.md
│   ├── templates/
│   │   ├── portfolio-register.md
│   │   ├── project-intake-card.md
│   │   ├── strategic-alignment-map.md
│   │   ├── prioritization-scorecard.md
│   │   ├── governance-decision-record.md
│   │   ├── dispatch-authorization.md
│   │   ├── portfolio-health-dashboard.md
│   │   ├── rebalancing-proposal.md
│   │   └── retirement-record.md
│   └── templates/agents/
│       ├── portfolio-governance-agent.md
│       ├── portfolio-governance-shortcut.md
│       └── portfolio-governance-guide.md
└── setup/
    └── INSTALL.md
```

**Estimated file count:** ~42 files (5 common + 10 stages + 14 extensions + 9 templates + 3 agent + README/LICENSE/PLAN/INSTALL)

---

## 9. Input/Output Contract

### The Routing Rule

> **Cross-layer communication MUST go through AI-FLO. Same-layer communication is direct (marker-based).**

### I Read — Direct (Same Layer: Portfolio)

| Source | Marker | What I Read |
|---|---|---|
| AI-PILC output | `pilc-state.md` | PIP summary (Project ID, charter, budget, timeline, resources, risks) |
| AI-ILC output | `ilc-state.md` | Approved Idea Brief (evaluation score, routing decision, effort estimate) |
| Existing Portfolio Register | `portfolio-register.md` | Resume: current portfolio state |

These are same-layer reads. AI-PPM detects markers directly — no FLO routing needed.

### I Read — Via FLO (Cross Layer: Project → Portfolio)

| Source | What FLO Carries Up |
|---|---|
| Project-layer roll-up (per Project ID) | Health snapshot: progress, RAG, budget actuals, velocity, compliance, risks, backlog health |

AI-PPM NEVER reads Project-layer state files directly. All cross-layer data arrives via FLO.

**Fallback (no FLO):** PPM prompts user for manual status updates.

### I Produce — Direct (Same Layer: Portfolio)

| Artifact | Purpose |
|---|---|
| `ppm-state.md` | Engine state marker (resume, detection) |
| `portfolio-register.md` | Master portfolio view — all projects, states, priorities, health |
| `portfolio-decisions/` | Governance decision records (admit/pause/retire with rationale) |
| `portfolio-dashboards/` | Rendered dashboard views (health, financial, risk, progress) |

### I Produce — Via FLO (Cross Layer: Portfolio → Project)

| Artifact | Purpose |
|---|---|
| `dispatch-authorizations/` | Authorization for FLO to carry across layer boundary → activate Project-layer packages |

AI-PPM NEVER activates Project-layer packages directly. Dispatch authorizations are placed for FLO.

**Fallback (no FLO):** User manually starts Project-layer packages.

### My Same-Layer Neighbors

| Package | Relationship |
|---|---|
| AI-ILC | PPM reads its approved briefs for portfolio intake |
| AI-PILC | PPM reads its PIPs for portfolio registration |

### My Cross-Layer Courier

| Package | Role |
|---|---|
| AI-FLO | Carries dispatch DOWN to Project layer; carries roll-up UP from Project layer |

---

## 10. Key Design Decisions

| # | Decision | Choice | Rationale |
|---|---|---|---|
| 1 | Name | AI-PPM | Industry-standard acronym; Lesson 12 challenge passed |
| 2 | Package type | Adaptive engine (not lifecycle) | Portfolio management is continuous, not one-pass (Lesson 1) |
| 3 | Core stage count | 10 | Lean core; complexity handled by 7 extensions |
| 4 | Per-project metrics | Descoped | Already exist in PILC/POLC/GCE/TGE — data arrives via FLO |
| 5 | Dashboard data source | FLO-carried roll-up (cross-layer) + direct reads (same-layer PILC/ILC) | PPM reads, never computes per-project values |
| 6 | Communication rule | Cross-layer via FLO; same-layer direct | FLO is the layer-boundary courier, not a universal bus. Portfolio-layer packages talk directly to each other. |
| 6 | Governance model | Gate-based (not kanban) | Matches family's gate pattern; SAFe kanban vocabulary available as alias |
| 7 | Extension count | 7 | Cover the 20% advanced patterns (Lesson 9) |
| 8 | Financial deep-dive | Extension E6 | Not every portfolio needs lean funding / guardrails |
| 9 | Programme grouping | Excluded | Different discipline; portfolio manages atomic projects |
| 10 | State tracking | `ppm-state.md` + Portfolio Register | Standard family pattern |

---

## 11. Frameworks Studied

The following established frameworks informed the scope decisions:

| Framework | Key Contribution to AI-PPM |
|---|---|
| **PMI Standard for Portfolio Management (4th Ed.)** | Process groups: Defining, Aligning, Authorizing, Monitoring & Controlling → mapped to our 5 phases |
| **MoP (Management of Portfolios)** — AXELOS | Two cycles (Definition + Delivery); 12 practices → strategic alignment + balancing patterns |
| **SAFe Lean Portfolio Management** | Portfolio Kanban, WSJF, lean budget guardrails, strategic themes → extensions E1/E4/E5/E6 |
| **P3O (Portfolio, Programme & Project Offices)** | Office structures → governance cadence pattern |
| **Three Horizons Model** (McKinsey) | Balance innovation investment → extension E1 (balancing) |
| **Stage-Gate** (Cooper) | Gate-based pipeline management → core governance gate model |
| **Benefits Realization Management** | Track actual vs. predicted value → extension E7 |

---

## 12. Build Sequence (PLAYBOOK Steps)

1. ✅ **Step 1 — Problem space defined** (this plan §1-3)
2. ✅ **Step 2 — Research & pattern extraction** (§6, §11)
3. ✅ **Step 3 — Plan presented & approved** (this file)
4. ✅ **Step 4 — Build core-engine.md** (`ai-ppm-rules/core-engine.md`)
5. ✅ **Step 5 — Build common files** (5 files in `common/`)
6. ✅ **Step 6 — Build stage detail files** (10 files across 5 phase folders)
7. ✅ **Step 7 — Build templates** (9 files in `templates/`)
8. ✅ **Step 8 — Build extensions** (15 files: 7 × opt-in + detail + README)
9. ✅ **Step 9 — Build agent templates** (3 files in `templates/agents/`)
10. ✅ **Step 10 — Build README + LICENSE + INSTALL** (README, LICENSE, NOTICE, INSTALL.md, TEST_MODE_USER_GUIDE.md, CONCEPTUAL_MAP.md)
11. ⬜ **Step 11 — Verify (Dry Test)**
12. ⬜ **Step 12 — Register in FAMILY_TABLE_MAP.md**

---

*Created: 2026-06-11 | Author: Maheri | Source: Idea 007 + competitive research + family coverage analysis*
