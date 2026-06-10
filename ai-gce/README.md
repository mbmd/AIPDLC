# AI-GCE — AI-Driven Governance & Compliance Engine

**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**Version:** 1.0.0

---

## What Is AI-GCE?

A **full project governance engine** that reads an AI-DWG development workspace and derives a tailored compliance enforcement layer — rules, hooks, agents, and logging infrastructure specific to that project's architecture, technology, team structure, and methodology.

**Not just architecture compliance.** AI-GCE enforces team topology, role segregation, session discipline, sprint governance, PR process, CI/CD gates, DevOps standards, and change management — all derived automatically from the workspace.

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
    AI-POG ───┘     Prepare it       ▲                          
    Own it      └───────────────────┘  AI-POG ⇄ AI-DLC (back-and-forth)
                AI-UXD ⇢ AI-POG (personas/journeys)  ·  AI-DLC ⇢ AI-UXD+AI-POG (feedback)

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
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP / AP; strategy-stage exchange with AI-POG | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-POG** ³ | Interactive workflow (lifecycle) | PIP and/or AP | Product Backlog Package (PBP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POG) | Working Software |

> ¹ **AI-DLC** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ **AI-PPM**, **AI-FLO**, **AI-POG**, and **AI-UXD** are **new and pending build**. AI-PPM (portfolio engine) and AI-FLO (router) are registered as ideas; AI-POG (product ownership lifecycle) is idea 006; AI-UXD (UX design lifecycle) is idea 010 (approved). Within the Project layer, **AI-ADLC, AI-UXD, and AI-POG run in parallel and all feed AI-DWG**; **AI-UXD produces personas/journeys that AI-POG consumes** (and AI-POG's value goals focus UX research); **AI-GCE and AI-TGE run alongside AI-DLC** as continuous quality engines; **AI-POG ⇄ AI-DLC** exchange backlog/acceptance throughout delivery; and **AI-DLC runtime feedback flows back to both AI-UXD and AI-POG**.

---

## Key Features

- **Zero configuration** — reads the workspace; derives everything from steering files
- **Two-source derivation** — built-in methodology baseline + steering-enriched project specifics
- **Four operating modes** — Full Generation, Re-Derivation, Brownfield Adoption, Tier Activation
- **Three-tier progressive compliance** — Day 0 (60-70%) → Sprint 2+ (80-90%) → Pre-Release (92%+)
- **Hook debounce strategy** — security-critical on fileEdited; advisory on agentStop
- **Phase-aware enforcement** — rules only fire when applicable to current project phase
- **Silent when passing** — no output unless something is wrong
- **Technology-specific** — hooks use actual file patterns derived from tech-stack.md
- **Brownfield first-class** — baseline existing violations, enforce new code from day 1
- **Full audit trail** — every hook writes JSONL compliance events; Git-committed evidence

---

## How to Use

### Quick Start

In a workspace that has `.kiro/steering/` populated (by AI-DWG):

```
Using AI-GCE, generate the compliance engine for this workspace
```

AI-GCE asks 1-2 questions, then generates everything in one pass.

### Four Modes

| Say This | Mode Triggered |
|----------|:-------------:|
| "Generate compliance engine" | Mode 1: Full Generation |
| "Steering changed — re-derive" | Mode 2: Re-Derivation |
| "Brownfield adoption" / "Baseline scan" | Mode 3: Brownfield |
| "Activate next compliance tier" | Mode 4: Tier Activation |

---

## What It Produces

Installed into the development workspace:

```
.kiro/hooks/              ← 15 always-generated + up to 6 conditional enforcement hooks (JSON)
.kiro/hooks/INSTALL-GUIDE.md  ← Tier-based adoption roadmap
.compliance-state.json    ← Tier tracking + readiness criteria
docs/compliance-dashboard.md  ← Visual compliance overview
.governance/
├── COMPLIANCE_README.md  ← Developer-facing guide
├── rules/                ← 18+ always rules + conditionals
├── agents/               ← Audit agent + init agent specs
└── compliance-log/       ← JSONL schema + workflows
```

---

## Installation

See `kiro-setup/INSTALL.md` for platform-specific installation instructions.

---

## Package Structure

```
ai-gce/
├── README.md                          ← This file
├── LICENSE                            ← Apache 2.0 + Attribution
├── PLAN.md                            ← Design rationale + gap analysis
├── ai-gce-rules/
│   └── core-generator.md             ← Master derivation logic (4 modes)
├── ai-gce-rule-details/
│   ├── common/                        ← Cross-cutting docs (5 files)
│   ├── generators/                    ← Derivation logic per rule category (23 files)
│   ├── re-derivation/                 ← Incremental update logic (3 files)
│   └── templates/                     ← Hook, agent, and log templates
│       ├── hooks/                     ← 15 hook JSON templates + INSTALL-GUIDE
│       ├── agents/                    ← Audit agent + init agent + README template
│       └── compliance-log/            ← Schema + workflows + dashboard template
└── kiro-setup/
    └── INSTALL.md
```

---

## Tenets

1. **Derive, don't configure.** The workspace already has the answers — read them.
2. **Governance is broader than architecture.** Roles, sessions, sprints, PRs, DevOps — all enforced.
3. **Progressive, not big-bang.** Three tiers. Teams adopt at their pace.
4. **Silent when compliant.** Noise kills adoption. Only speak when wrong.
5. **Every action logged.** Audit trail is non-negotiable. Every hook writes.
6. **Brownfield is normal.** Most projects have existing code. Baseline and improve.
7. **Rules are enforceable.** MUST/NEVER, not "consider." Binary pass/fail.
8. **Customizations survive.** Team additions marked `<!-- custom -->` persist through re-derivation.

---

## Author

**Maheri** — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)

AI-GCE is part of the AI-* injectable package family. Inspired by [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0 license).

---

## License

**Apache License 2.0 with Attribution Addendum**

- **Free to use:** Personal, commercial, educational, and organizational use — all permitted
- **Modify and distribute:** Create derivative works, redistribute, sublicense — all permitted
- **Attribution required:** Any distributed product substantially based on this work must include:

> *"Built on AIFLC by Mohammad Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)"*

- **No warranty:** Provided "AS IS" without warranties of any kind

See [LICENSE](./LICENSE) in this directory and the canonical licensing documents in `../ai-license/` for full terms and FAQ.

**Copyright:** © 2026 Mohammad Maheri
