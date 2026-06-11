# AI-ILC — Process Overview

**Purpose:** High-level map of the entire AI-ILC workflow. Reference this to understand where you are, what comes next, and how the stages connect.

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

## Workflow at a Glance

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐
│ 1.CAPTURE│───▶│ 2. SHAPE │───▶│3.EVALUATE│───▶│ 4. SCOPE │───▶│5. APPROVE│───▶│6. ROUTE &    │
│          │    │          │    │          │    │          │    │          │    │   HANDOFF    │
│ Log idea │    │ Structure│    │ Score &  │    │ Boundary │    │ Go/No-Go │    │ Where does   │
│ fast     │    │ the      │    │ value    │    │ & effort │    │ decision │    │ it go?       │
│          │    │ problem  │    │ analysis │    │          │    │          │    │              │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────────┘
     │               │               │               │               │               │
     ▼               ▼               ▼               ▼               ▼               ▼
  Register        Idea            Score +        Scope          Decision         Brief +
  entry +         Statement       Value          definition     Record           Route
  state file                      Analysis                      (always)         (conditional)
```

---

## Stage Summary Table

| # | Stage | Always/Conditional | Gate | Output |
|---|-------|:------------------:|------|--------|
| 1 | **Capture** | Always | User confirms capture | Idea registered + state file created |
| 2 | **Shape** | Always | User approves structured statement | Idea Statement (working doc) |
| 3 | **Evaluate** | Always | User confirms Proceed / Park / Reject | Score + Value Analysis |
| 4 | **Scope** | Conditional (if Evaluate = Proceed) | User agrees on scope | Boundary + effort estimate |
| 5 | **Approve** | Conditional (if Scoped) | Explicit go/no-go | Go/No-Go Decision Record |
| 6 | **Route & Handoff** | Conditional (if Approved) | User confirms route | Approved Idea Brief / Change Request Brief / Feature Brief |

---

## Depth Model

AI-ILC adapts its depth to the idea's complexity:

| Level | When | Behavior |
|-------|------|----------|
| **Minimal** | Idea is clear, small scope, low risk | Fast pipeline: 3 shaping questions, quick score, lightweight scope, rapid handoff |
| **Standard** | Normal complexity, some ambiguity | Full pipeline: structured shaping, 7-criterion scoring + value analysis, full scope |
| **Comprehensive** | High stakes, ambiguous, multi-stakeholder | Deep pipeline: extensive shaping with prior art, competitive analysis, detailed value case, explicit trade-offs |

Depth is **recommended at Capture** (based on clarity + scale signals) and **confirmed by the user**. It can be adjusted at any stage gate.

---

## Routing Model (Stage 6)

After approval, an **impact-driven** routing determines the handoff destination:

```
┌─────────────────────────────────────────────────────────────┐
│                    ROUTING DECISION                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Q1: Does a project exist for this idea?                     │
│      ├── NO  → Route: NEW PROJECT (→ AI-PILC)               │
│      └── YES → Q2: Is the impact BIG?                        │
│                    (changes scope, criteria, or architecture) │
│                    ├── YES → Route: CHANGE REQUEST            │
│                    │         (→ AI-PILC change management)    │
│                    └── NO  → Route: FEATURE BACKLOG           │
│                              (→ AI-DLC backlog)               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

| Route | Brief Produced | Destination |
|-------|---------------|-------------|
| New Project | `Approved_Idea_Brief.md` | AI-PILC (initiates a new project) |
| Change Request | `Change_Request_Brief.md` | AI-PILC change management (on existing project) |
| Feature Backlog | `Feature_Brief.md` | AI-DLC backlog (small feature, direct to build queue) |

---

## Interaction Model

**Human-in-the-loop at every gate.** The AI advises; the user decides.

| Interaction Pattern | Description |
|-------------------|-------------|
| **Structured questions** | Formatted per `question-format-guide.md` — always with recommendation + rationale |
| **Stage gates** | User must approve before moving to next stage |
| **Depth adjustment** | User can increase or decrease depth at any gate |
| **Early exit** | User can Park or Reject at any Evaluate/Approve gate — clean close with audit trail |
| **Resume** | If interrupted, state file captures exactly where to continue (see `session-continuity.md`) |

---

## User Commands

At any point during the workflow, the user can say:

| Command | Effect |
|---------|--------|
| "Capture a new idea" | Start Stage 1 (new idea entry) |
| "Shape this idea" | Continue from Stage 2 if captured |
| "Evaluate" | Jump to scoring (if shaped) |
| "What's the status?" | Show current stage, pending decisions, depth level |
| "Park this" | Move idea to Parked status (with revisit date), close workflow cleanly |
| "Reject this" | Move idea to Rejected status (with rationale), close workflow cleanly |
| "Change depth to {level}" | Adjust depth level for remaining stages |
| "Resume" | Load state file and continue from last completed stage |
| "Show the register" | Display the Idea Register (all ideas, all statuses) |

---

## Dynamic Persona Model

No fixed persona for the whole workflow. Each stage activates the right expert voice with a specialist sub-role lens:

| Stage | Lead Primary | Sub-Role Layered | Why |
|-------|-------------|-----------------|-----|
| Capture | `#persona-product-manager` | — | Fast capture, no specialist needed |
| Shape | `#persona-product-manager` | `#persona-subrole-business-analyst` | Requirements decomposition, ambiguity detection |
| Evaluate | `#persona-product-manager` | `#persona-subrole-financial-analyst` | Value scoring, investment framing |
| Scope | `#persona-process-designer` | `#persona-subrole-resource-planner` | Boundary setting, effort estimation |
| Approve | `#persona-product-manager` | `#persona-subrole-risk-analyst` | Risk-aware go/no-go challenge |
| Route & Handoff | `#persona-product-manager` | `#persona-subrole-change-manager` | Impact assessment (big vs. small change) |

At the **Approve** and **Route** stages, the idea's subject domain may override the default sub-role with a domain-specific one (e.g., if the idea is about security, `#persona-subrole-security-architect` layers instead). Resolution: primary + one sub-role max per stage.

---

## Registers

| Register | Purpose | Created At |
|----------|---------|-----------|
| **Idea Register** | Portfolio funnel view — every idea's status, score, decision, dates | First Capture |
| **Decision Log** | Audit trail — every go/no-go, routing decision, park/reject rationale | First Approve |

---

## What AI-ILC Does NOT Do

- Does NOT initiate projects (that's AI-PILC)
- Does NOT design architecture (that's AI-ADLC)
- Does NOT write code or tests
- Does NOT manage a multi-project portfolio (v1.0 = single project per workspace)
- Does NOT perform full feasibility studies (lightweight impact assessment only — AI-PILC handles deep analysis)

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*
