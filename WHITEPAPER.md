# AI-* Family — Whitepaper

**From Raw Requirement to Governed Code: An AI-Driven Software Delivery Chain**

**Version:** 1.0.0
**Author:** Maheri
**Date:** 2026-06-07

---

## The Problem

Enterprise software projects fail the same way, over and over:

1. **Chaotic initiation** — Requirements arrive as emails, verbal descriptions, or 50-page RFPs. Teams skip governance and jump straight to building. Six months later, scope is undefined and budgets are blown.

2. **Architecture that dies on paper** — Even when architecture is properly designed, it lives in documents that developers never read. Decisions made in week one are violated by week six.

3. **The "ready to code" gap** — Between an approved architecture and a developer's first commit lies an enormous translation problem. Who converts ADR decisions into coding standards? Who enforces API contracts across 12 microservices?

4. **Governance through willpower** — Standards exist in wikis nobody reads. Conventions exist in someone's head. Enforcement happens in code reviews that are already too late.

5. **AI without structure** — Teams adopt AI assistants for code generation, but without constraints those assistants produce confident work that violates the team's own architecture. The problem isn't AI capability — it's AI direction.

---

## The Solution

The AI-* Family is a chain of four packages that solve these problems sequentially. Each package trains an AI assistant to perform one discipline of software delivery — with human oversight at every decision point.

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

## How It Works

### The Chain Model

Each package's output becomes the next package's input. Decisions flow forward — never lost, never repeated, never re-asked.

A requirement captured in AI-PILC becomes a constraint in AI-ADLC. A technology decision in AI-ADLC becomes a steering rule in AI-DWG. A steering rule in AI-DWG becomes an enforcement hook in AI-GCE. By the time a developer opens their IDE, every constraint is alive — enforced by AI, traceable to its origin.

### Human-in-the-Loop at Every Stage

No package auto-progresses. Every stage has a gate. The human makes decisions; the AI produces structured output from those decisions. This is not autonomous AI — it's AI as a disciplined collaborator.

### Standalone or Chained

Each package works independently:
- Have requirements but no charter? Start with AI-PILC.
- Already have architecture docs from another process? Feed them to AI-DWG directly.
- Already have a workspace with steering files? Run AI-GCE to add compliance.

The chain is the optimal path. But each link stands alone.

---

## Key Differentiators

### 1. Methodology, Not Magic

Each package embeds proven methodology — PMBOK/PRINCE2 for initiation, C4/ADR for architecture, prescriptive governance for compliance. The AI doesn't invent process; it executes established process consistently.

### 2. Injectable

These are not SaaS products or IDE plugins. They are markdown files — steering rules and templates — that inject into any AI-capable IDE. Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, GitHub Copilot. The package doesn't own your toolchain; it augments it.

### 3. Traceable

Every output traces to its source. Every steering rule traces to an architecture decision. Every compliance hook traces to a steering rule. The chain provides full lineage from requirement to enforcement.

### 4. Progressive

Nothing is big-bang. AI-PILC has adaptive depth (Minimal/Standard/Comprehensive). AI-GCE has three compliance tiers (Day 0 → Sprint 2+ → Pre-Release). Teams adopt at their own pace.

### 5. Brownfield-Aware

Every package handles "what if something exists already?" — not as an afterthought, but as a first-class operating mode. Real enterprises extend existing systems; the chain respects that.

### 6. Non-Destructive

Reconciliation modes (AI-DWG, AI-GCE) detect and preserve team customizations. Re-derivation after architecture changes updates only what's affected. Human additions are never overwritten.

---

## Who It's For

| Role | Value |
|------|-------|
| **CTO / VP Engineering** | Consistent architectural governance across all projects without manual policing |
| **PMO / Project Manager** | Structured initiation that produces governance-board-ready documents in hours, not weeks |
| **Solution Architect** | Architecture decisions that flow into enforceable rules — not documents that get ignored |
| **Platform Engineer** | Ready-to-code workspaces generated from architecture, not hand-crafted per project |
| **Tech Lead / Staff Engineer** | Team compliance that's automated and traceable, not dependent on code review heroics |
| **Compliance Officer** | Audit trails, evidence collection, and progressive enforcement without blocking delivery |

---

## The Economics

Traditional approach:
- 2-4 weeks: Project initiation and governance setup
- 2-6 weeks: Architecture documentation
- 1-2 weeks: Workspace setup, coding standards, CI/CD config
- Ongoing: Manual compliance reviews, code review enforcement, wiki maintenance

With the AI-* Family:
- 1-3 days: AI-PILC produces a complete Project Initiation Package
- 2-5 days: AI-ADLC produces a comprehensive Architecture Package
- Minutes: AI-DWG generates the entire workspace
- Minutes: AI-GCE derives the entire compliance layer

The saving isn't just time. It's consistency, traceability, and zero drift between what was decided and what gets enforced.

---

## Getting Started

Each package is available independently. Pick the one that matches your starting point:

| Starting Point | Package to Use |
|----------------|----------------|
| "I have a vague requirement" | [AI-PILC](./ai-pilc/) |
| "I have requirements, need architecture" | [AI-ADLC](./ai-adlc/) |
| "I have architecture, need a workspace" | [AI-DWG](./ai-dwg/) |
| "I have a workspace, need compliance" | [AI-GCE](./ai-gce/) |

Each package includes platform-specific installation instructions for Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, and GitHub Copilot.

---

## License

Apache 2.0 with Attribution Addendum. See `ai-license/` for full details.

---

*Created by Maheri — because enterprise software deserves better than chaos.*
