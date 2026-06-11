# AI-POLC — AI-Driven Product Ownership Life Cycle

**Version:** 1.0.0
**Author:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**License:** Apache 2.0 with Attribution

---

## What Is AI-POLC?

AI-POLC is an injectable workflow package that guides an AI assistant and a human Product Owner through establishing and operating disciplined product ownership — from business intent to a governed, prioritized Product Backlog Package (PBP) ready for development consumption.

**Identity:** AI-POLC turns business intent into a prioritized, value-justified product backlog, and is the single source of truth for *what gets built, in what order, and why*.

---

## The AI-* Family

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

## Features

### Core (Tier 1 — Always Active)

- **Product Vision & Goals** — distill business intent into measurable goals
- **PO Charter & Authority** — define decision boundaries and RACI
- **Product Discovery & Roadmap** — Now/Next/Later strategic planning
- **Epic Decomposition** — goal→epic mapping with acceptance criteria
- **Value-Based Prioritization** — WSJF, MoSCoW, or value-effort with recorded rationale
- **Release & Increment Slicing** — MVP/MMP scope + delivery groupings
- **Definition of Ready / Done** — quality bar flowing to AI-DWG and AI-GCE
- **Product Risk & Assumptions** — product-level risk register
- **Traceability** — intent→epic→release linkage
- **Stakeholder Management** — power/interest matrix + communication cadence
- **Product Documentation** — release notes and changelog governance
- **Backlog Operations** — refinement, splitting criteria, tech-debt trade-offs
- **Acceptance & Feedback** — increment acceptance against DoD, DLC feedback loop

### Story Elaboration (Tier 2 — User-Activated)

- **INVEST-compliant stories** with Given/When/Then acceptance criteria
- Off by default in chain mode (AI-DLC handles story creation)
- Activate for standalone use or PO-quality pre-elaboration

### Extensions (Opt-In)

- Advanced Discovery (OKRs, JTBD, opportunity scoring)
- Full Traceability (audit-grade matrix, compliance evidence)
- Full Risk Register (scoring, owners, response plans, trend tracking)
- Value & Metrics Engine (KPIs, benefits realization, experiments)
- Full Product Docs (PRD, feature briefs, wiki governance)
- Quality Review AI-Assist (automated backlog quality scanning)
- MVP/MMP for Mature Products (next-version scoping)

---

## Installation

See `kiro-setup/INSTALL.md` for platform-specific installation instructions.

---

## File Structure

```
ai-polc/
├── README.md                           ← This file
├── LICENSE
├── PLAN.md                             ← Build plan and design rationale
├── ai-polc-rules/
│   └── core-workflow.md                ← Master orchestration (always loaded)
├── ai-polc-rule-details/
│   ├── common/                         ← Cross-cutting rules (5 files)
│   ├── foundation/                     ← Phase 1: Stages 1-3
│   ├── strategy/                       ← Phase 2: Stages 4-7
│   ├── governance/                     ← Phase 3: Stages 8-10
│   ├── stakeholders/                   ← Phase 4: Stages 11-12
│   ├── assembly/                       ← Phase 5: Stage 13
│   ├── operations/                     ← Phase 6: Stages 14-16
│   ├── tier2/                          ← Tier 2: Story elaboration
│   ├── extensions/                     ← 7 opt-in extensions (14 files)
│   └── templates/                      ← 12 output templates
└── kiro-setup/
    └── INSTALL.md
```

---

## Tenets

1. **Value-justified** — nothing enters the backlog without answering "why does this serve the product vision?"
2. **Traceable** — every item links upward to a goal and downward to an acceptance bar
3. **Governed** — decisions are logged, priorities have rationale, changes are tracked
4. **Adaptive** — depth adapts to product complexity; context factors shape behavior
5. **Workspace-mediated** — rules reach AI-DLC through steering files, not direct integration
6. **Source-driven** — derive from user input; never fabricate scope

---

## Quick Start

```
You take the role of a high-skilled professional process designer/engineer.

Using the AI-POLC package, I want to establish product ownership governance
for my product.

Context:
- Product: {your product name}
- Input: {PIP available / Architecture Package / standalone vision}
- Mode: {chain with AI-DLC / standalone}

Please start the AI-POLC workflow.
```

---

*Created: 2026-06-11 | Author: Maheri*
