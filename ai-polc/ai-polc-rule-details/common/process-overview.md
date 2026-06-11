# AI-POLC — Process Overview

**Purpose:** Quick-reference map of the entire AI-POLC workflow. Use this to understand where you are, what comes next, and how the phases connect.

---

## The AI-* Family (AI-POLC Position)

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

    AI-ADLC ──┐
    Design it │
    AI-UXD ───┤
    Design UX │
              ├──►  AI-DWG  ──►  AI-DLC (build) ¹
    AI-POLC ──┘     Prepare it       ▲
    Own it      └───────────────────┘  AI-POLC ⇄ AI-DLC (back-and-forth)
                AI-UXD ⇢ AI-POLC (personas/journeys)  ·  AI-DLC ⇢ AI-UXD+AI-POLC (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | (Requirements + Charter) / PIP | Architecture Package (AP) |
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP / AP; strategy-stage exchange with AI-POLC | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-POLC** ³ | Interactive workflow (lifecycle) | PIP and/or AP | Product Backlog Package (PBP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POLC) | Working Software |

> ¹ **AI-DLC** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ **AI-PPM**, **AI-FLO**, **AI-POLC**, and **AI-UXD** are **new and pending build**. AI-PPM (portfolio engine) and AI-FLO (router) are registered as ideas; AI-POLC (product ownership lifecycle) is idea 006; AI-UXD (UX design lifecycle) is idea 010 (approved). Within the Project layer, **AI-ADLC, AI-UXD, and AI-POLC run in parallel and all feed AI-DWG**; **AI-UXD produces personas/journeys that AI-POLC consumes** (and AI-POLC's value goals focus UX research); **AI-GCE and AI-TGE run alongside AI-DLC** as continuous quality engines; **AI-POLC ⇄ AI-DLC** exchange backlog/acceptance throughout delivery; and **AI-DLC runtime feedback flows back to both AI-UXD and AI-POLC**.

---

## Workflow Map

```
PHASE 1: FOUNDATION                    PHASE 2: STRATEGY
┌────────────────────────┐            ┌─────────────────────────────────────┐
│ Stage 1: Detection     │            │ Stage 4: Discovery & Roadmap        │
│ Stage 2: Vision & Goals│───gate───► │ Stage 5: Epic Decomposition         │
│ Stage 3: PO Charter    │            │ Stage 6: Value Prioritization       │
└────────────────────────┘            │ Stage 7: Release Slicing            │
                                      └──────────────────┬──────────────────┘
                                                         │ gate
                                                         ▼
PHASE 4: STAKEHOLDERS                  PHASE 3: GOVERNANCE
┌────────────────────────┐            ┌─────────────────────────────────────┐
│ Stage 11: Stakeholders │◄───gate────│ Stage 8: DoR / DoD                  │
│ Stage 12: Product Docs │            │ Stage 9: Risk & Assumptions         │
└───────────┬────────────┘            │ Stage 10: Traceability              │
            │ gate                    └─────────────────────────────────────┘
            ▼
PHASE 5: ASSEMBLY                      PHASE 6: OPERATIONS (repeating)
┌────────────────────────┐            ┌─────────────────────────────────────┐
│ Stage 13: PBP Assembly │───gate───► │ Stage 14: Backlog Ops               │
│     & Handoff          │            │ Stage 15: Acceptance & Feedback     │
└────────────────────────┘            │ Stage 16: Value & Metrics (ext)     │
                                      └─────────────────────────────────────┘
```

---

## Stage Quick Reference

| # | Stage | What Happens | Key Output |
|---|-------|-------------|------------|
| 1 | Workspace Detection | Detect mode (chain/standalone), scan upstream changes, establish context factors | Mode + context factors established |
| 2 | Product Vision & Goals | Distill business intent into vision + measurable goals | Vision statement, OKRs/KPIs |
| 3 | PO Charter & Authority | Define PO's decision boundaries and accountability | PO Charter, RACI |
| 4 | Product Discovery & Roadmap | Map strategic themes into Now/Next/Later horizons | Roadmap, value proposition |
| 5 | Epic Decomposition | Break goals into epics with acceptance criteria | Epic definitions (one per file) |
| 6 | Value-Based Prioritization | Rank epics using explicit model (WSJF/MoSCoW/value-effort) | Prioritization register |
| 7 | Release & Increment Slicing | Group prioritized epics into deliverable releases; define MVP/MMP | Release plan |
| 8 | Definition of Ready / Done | Set the quality bar for entering and exiting development | DoR + DoD checklists |
| 9 | Product Risk & Assumptions | Identify product-level risks and validate assumptions | Risk register, assumption log |
| 10 | Traceability Spine | Link intent → epic → (story) → acceptance | Traceability matrix |
| 11 | Stakeholder Management | Map stakeholders, define communication cadence | Stakeholder map |
| 12 | Product Documentation | Establish release notes and changelog governance | Release notes framework |
| 13 | PBP Assembly | Bundle all outputs, finalize polc-state.md | PBP_README.md, status=ready |
| 14 | Backlog Operations | Refinement, splitting, tech-debt trade-offs, pruning | Updated backlog |
| 15 | Acceptance & Feedback | Accept/reject DLC output, process feedback, reprioritize | Acceptance decisions |
| 16 | Value & Metrics | Track KPIs, benefits realization, experiments | Metrics report (extension) |

---

## Input Modes (Lesson 4/6)

AI-POLC supports multiple intake modes:

| Mode | Input Available | Behavior |
|------|----------------|----------|
| **Chain (full)** | PIP + AP + UXP | Full context — auto-detect upstream, minimal user questions |
| **Chain (partial)** | PIP only, or AP only | Detect what's available, ask for missing context |
| **Standalone (structured)** | Product brief / vision document | User provides product-level intent directly |
| **Standalone (verbal)** | Conversation | AI interviews user to extract vision, goals, scope |
| **Brownfield** | Existing ungoverned backlog | Audit → gap analysis → progressive adoption |

---

## Key Concepts

### Product Backlog Package (PBP)

The complete output of AI-POLC. Contains: vision, charter, roadmap, epics, prioritization, release plan, DoR/DoD, risks, traceability, stakeholder map, and governance spine entries. This is what AI-DWG reads for workspace generation and what AI-DLC's user references for development.

### Tier Model

- **Tier 1 (always active):** Full PO governance — everything except story elaboration
- **Tier 2 (user-activated):** Story elaboration — INVEST stories + Given/When/Then AC. Off by default in chain mode (AI-DLC does this).

### Session-Based Operation

AI-POLC and AI-DLC never run simultaneously in one session. The user alternates:
1. POLC session → refine backlog, reprioritize, accept last increment
2. DLC session → build the next priority item
3. POLC session → review what DLC built, accept/reject, update plan

All state is persisted in files. No session memory dependency.

---

*Reference this file at any point during the workflow for orientation.*
