# AI-ILC — AI-Driven Idea Life Cycle

**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**Version:** 1.0.0
**Package Type:** Interactive workflow (lifecycle)

---

## What It Does

AI-ILC takes a raw idea — from anyone, in any format — through a governed pipeline to a defensible go/no-go decision, then routes the approved idea to the right next step with zero context loss.

**Input:** A raw idea (verbal, one-liner, document, feature request)
**Output:** Approved Idea Brief / Change Request Brief / Feature Brief + Go/No-Go Decision Record

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
              ├──►  AI-DWG  ──►  AI-DLC (build) ¹              
    AI-POG ───┘     Prepare it       ▲                          
    Own it      └───────────────────┘  AI-POG ⇄ AI-DLC (back-and-forth)

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
| Project | **AI-POG** ³ | Interactive workflow (lifecycle) | PIP and/or AP | Product Backlog Package (PBP) |
| Project | **AI-DWG** | One-time generator | AP + PBP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POG) | Working Software |

> ¹ **AI-DLC** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ **AI-PPM**, **AI-FLO**, and **AI-POG** are **new and pending build**. AI-PPM (portfolio engine) and AI-FLO (router) are registered as ideas; AI-POG (product ownership lifecycle) is idea 006. Within the Project layer, **AI-ADLC and AI-POG run in parallel and both feed AI-DWG**; **AI-GCE and AI-TGE run alongside AI-DLC** as continuous quality engines; and **AI-POG ⇄ AI-DLC** exchange backlog/acceptance throughout delivery.

---

## Features

- **6-stage governed pipeline** — Capture → Shape → Evaluate → Scope → Approve → Route & Handoff
- **Gates at every stage** — human-in-the-loop; you decide, AI advises
- **Consistent evaluation** — 7-criterion scoring with configurable rubric (two-source model)
- **Value analysis** — articulates WHY an idea matters, not just whether it passes
- **Impact-driven routing** — determines whether an approved idea is a new project, a big change, or a small feature
- **Three brief types** — Approved Idea Brief (→ AI-PILC), Change Request Brief (→ AI-PILC change mgmt), Feature Brief (→ AI-DLC backlog)
- **Audit trail from day one** — Decision Log + Idea Register; every choice recorded with rationale
- **Adaptive depth** — Minimal / Standard / Comprehensive based on idea complexity
- **Dynamic stage-based personas** — each stage activates the right expert voice with specialist sub-roles
- **Session continuity** — state file enables resume after interruption
- **Standalone + chain** — delivers full value without the rest of the AI-* family

---

## Who Uses It

- **Anyone** can submit an idea (democratic intake)
- **Innovation / Product / Portfolio Manager** governs the pipeline (evaluation, go/no-go, routing)

---

## How It Routes

```
┌─────────────────────────────────────────────┐
│  Does a project exist for this idea?         │
├──── NO ─────────────────────────────────────▶ AI-PILC (new project)
├──── YES + BIG change ───────────────────────▶ AI-PILC change management
└──── YES + SMALL change ─────────────────────▶ AI-DLC backlog (feature)
```

"Big" = impacts scope, architecture, resources, or stakeholders beyond the team.
"Small" = bounded feature within existing project boundaries.

---

## Installation

### Kiro IDE (Recommended)

See `kiro-setup/INSTALL.md` for step-by-step instructions.

### Manual Setup

1. Copy `ai-ilc-rules/core-workflow.md` to your project's `.kiro/steering/ai-ilc-rules/` folder
2. Copy `ai-ilc-rule-details/` to your project's `.kiro/ai-ilc-rule-details/` folder (or adjacent to your steering)
3. Start a conversation with: "I have an idea"

### Standalone (No AI-* Family)

AI-ILC works independently. You don't need AI-PILC, AI-ADLC, or any other package installed. The briefs it produces are portable documents usable with any methodology.

---

## File Structure

```
ai-ilc/
├── README.md                           ← This file
├── LICENSE                             ← Apache 2.0 with Attribution
├── PLAN.md                             ← Design rationale + build summary
├── ai-ilc-rules/
│   └── core-workflow.md                ← Master orchestration (the heart)
├── ai-ilc-rule-details/
│   ├── common/
│   │   ├── process-overview.md         ← High-level workflow map
│   │   ├── session-continuity.md       ← State file spec + resume logic
│   │   ├── question-format-guide.md    ← How decisions are collected
│   │   ├── content-validation.md       ← Quality rules for outputs
│   │   └── welcome-message.md          ← First-time greeting
│   ├── idea-lifecycle/
│   │   ├── capture.md                  ← Stage 1: Log the idea fast
│   │   ├── shape.md                    ← Stage 2: Structure the problem
│   │   ├── evaluate.md                 ← Stage 3: Score + value analysis
│   │   ├── scope.md                    ← Stage 4: Define boundaries
│   │   ├── approve.md                  ← Stage 5: Go/no-go decision
│   │   └── route-handoff.md            ← Stage 6: Route + produce brief
│   ├── connectors/
│   │   └── portfolio-connector.md      ← Interface stub (v1.0 = single project)
│   └── templates/
│       ├── idea-register.md            ← Portfolio funnel register
│       ├── idea-entry.md               ← Structured idea statement
│       ├── decision-record.md          ← Decision log format
│       ├── approved-idea-brief.md      ← Brief for new projects
│       ├── change-request-brief.md     ← Brief for big changes
│       ├── feature-brief.md            ← Brief for small features
│       └── ilc-state.md                ← State file schema
└── kiro-setup/
    └── INSTALL.md                      ← Platform installation guide
```

---

## Tenets

1. **Every idea deserves a fair hearing.** The pipeline evaluates, not dismisses.
2. **Go/No-Go is always explicit.** No idea drifts into limbo — Approved, Parked, or Rejected.
3. **Context carries forward.** The brief carries everything learned — no cold starts for successors.
4. **The user decides, the AI advises.** Recommendations with rationale; the human makes the call.
5. **Audit trail from day one.** Every score, decision, and routing choice is logged.
6. **Standalone is first-class.** Full value without the AI-* family; chain integration is a bonus.
7. **Parked is not dead.** Parked ideas have a revisit date and re-enter when conditions change.

---

## What AI-ILC Does NOT Do

- Initiate projects (that's AI-PILC)
- Design architecture (that's AI-ADLC)
- Write code or tests
- Manage a multi-project portfolio (v1.0 = single project per workspace)
- Perform full feasibility studies (lightweight impact assessment only)

---

## Author

**Maheri** — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)

Builder of the AI-* family of injectable workflow packages. AI-ILC is the optional front door — governing the decision to start before the work begins.

---

*Version 1.0.0 | AI-ILC — AI-Driven Idea Life Cycle*
