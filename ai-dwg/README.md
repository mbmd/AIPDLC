# AI-DWG — AI-Driven Workspace Generator

**Transform architecture into a ready-to-code development workspace.**

---

## What It Does

AI-DWG reads an Architecture Package (from AI-ADLC or equivalent) — optionally enriched by a Product Backlog Package (from AI-POG) and a UX Design Package (from AI-UXD) — and generates a complete development workspace including Kiro steering files, project instructions, repository structure, configuration files, and operational documents.

**Input:** Architecture Package (required) + optional Product Backlog Package (AI-POG) and UX Design Package (AI-UXD) — all structured markdown documents
**Output:** Ready-to-code workspace with governance, structure, and rules

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

- **Full Generation** — one-shot workspace creation from architecture docs
- **Delta Reconciliation** — incremental updates when architecture changes
- **Extension-Aware** — detects AI-ADLC v1.1 extensions (DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags)
- **Conditional Generation** — only produces steering files justified by the architecture
- **Provenance Tracking** — every generated rule traces to its AP source
- **Non-Destructive Updates** — reconciliation preserves team customizations
- **Technology-Adaptive** — generates stack-appropriate configs (Node, Python, .NET, Java, Generic)
- **Prescriptive Output** — steering files say "MUST/MUST NOT", not "should/consider"

---

## What It Generates

| Category | Files |
|----------|:-----:|
| Steering files (always) | 19 |
| Steering files (conditional) | Up to 8 |
| Operational documents | 6 |
| Planning templates | 3 |
| Config files | 5 |
| Source structure | Per C4 L3 modules |

---

## Installation

See [kiro-setup/INSTALL.md](./kiro-setup/INSTALL.md)

---

## Usage

```
# First time
Using #ai-dwg-rules, generate the development workspace from my architecture package.

# After architecture changes
Using #ai-dwg-rules, reconcile the workspace — {what changed}.
```

---

## File Structure

```
ai-dwg/
├── README.md                    ← You are here
├── LICENSE                      ← Apache 2.0 + Attribution
├── PLAN.md                      ← Design plan
├── ai-dwg-rules/
│   └── core-generator.md       ← Master generation logic
├── ai-dwg-rule-details/
│   ├── common/                  ← Process overview, AP reading guide, validation
│   ├── mapping/                 ← 23 transformation rule files
│   ├── reconciliation/          ← Diff, merge, provenance, signaling
│   └── templates/               ← Output file templates (48 files)
└── kiro-setup/
    └── INSTALL.md               ← Installation instructions
```

---

## Tenets

1. **AP is the source of truth** — every rule traces to architecture
2. **Prescriptive over descriptive** — "MUST" not "should"
3. **Day-1 productivity** — developers start contributing immediately
4. **Non-destructive reconciliation** — team work is never lost
5. **Conditional generation** — no bloat; only what architecture justifies
6. **Detection by marker** — works regardless of folder structure
7. **Standalone capable** — works with or without the full AI-* chain

---

## Compatibility

- AI-ADLC v1.0 (core workflow)
- AI-ADLC v1.1 (6 extensions)
- Standalone Architecture Package (any structured markdown)

---

## Author

**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)

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
