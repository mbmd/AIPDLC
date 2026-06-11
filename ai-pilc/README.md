# AI-PILC (AI-Driven Project Initiation Life Cycle)

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**License:** Apache 2.0 with Attribution Addendum — See `LICENSE` and `../ai-license/`

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

## What is AI-PILC?

AI-PILC is an injectable workflow that guides an AI assistant and a human user through the complete process of initiating a project — from receiving a raw requirement to delivering a professional, execution-ready **Project Initiation Package (PIP)**.

It is designed as a general-purpose, reusable framework with zero project-specific content. Drop it into any workspace, point it at a requirement, and it will walk you through 6 phases and 16 stages of structured project initiation — producing PMBOK/PRINCE2-aligned deliverables at every step.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Injectable** | Drop into any workspace and activate — no project-specific setup |
| **Interactive** | Human-in-the-loop at every gate; you decide, AI recommends |
| **Adaptive** | Depth adjusts to project complexity (Minimal / Standard / Comprehensive) |
| **Resumable** | State file tracks progress; resume across sessions seamlessly |
| **Platform-Agnostic** | Works with Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, GitHub Copilot |
| **Template-Based** | Consistent, professional deliverables via reusable templates |
| **Register-Driven** | Management registers (decisions, changes, risks, actions, assumptions, lessons) maintained automatically |
| **Source-Driven** | Never invents scope; always references the user's input document |

---

## What It Produces

A complete Project Initiation Package containing:

- Requirement Intake Form
- Requirements Analysis Report
- Clarification Questionnaire & Responses
- Feasibility Assessment & Prioritization
- Business Case
- Project Charter
- Stakeholder Register
- Scope Statement & WBS
- Resource & Budget Plan
- Risk Register
- RACI Matrix & Governance Plan
- Kickoff Agenda & Materials
- 6 Management Registers (Decision, Change, Issue, Action, Assumptions, Lessons)
- Package README (summary and handoff guide)

---

## The Six Phases

```
🔵 INCEPTION        →  Receive, validate, structure the requirement
🟠 ASSESSMENT       →  Analyze feasibility, resolve gaps, prioritize
🟡 JUSTIFICATION    →  Build the investment case
🟣 AUTHORIZATION    →  Formalize authority and boundaries
🟢 PLANNING         →  Plan scope, resources, risks, governance
🚀 MOBILIZATION     →  Prepare kickoff, assemble final package
```

---

## Installation

1. Download or clone this repository
2. The package contains two key directories:
   - `ai-pilc-rules/` — the core workflow (always loaded by the AI)
   - `ai-pilc-rule-details/` — phase details and templates (loaded on demand)
3. Follow the platform-specific instructions in [kiro-setup/INSTALL.md](./kiro-setup/INSTALL.md)

---

## Usage

1. Open your workspace in your IDE with the AI assistant active
2. Start a chat and say:

   ```
   Using AI-PILC, initiate a project from this requirement: [provide source]
   ```

3. The workflow activates and guides you from there
4. Answer structured questions when asked
5. Review and approve each deliverable at gates
6. All artifacts are generated in your configured output folder

---

## Adaptive Depth

AI-PILC automatically calibrates its depth based on your project's complexity:

| Depth | When Applied | Deliverable Detail |
|-------|-------------|-------------------|
| **Minimal** | Small scope, clear requirements, low risk | Streamlined; fewer interaction cycles |
| **Standard** | Normal complexity, some gaps to resolve | Full deliverable set; standard gates |
| **Comprehensive** | High complexity, many unknowns, large investment | Detailed analysis; multiple iterations |

You can override the depth at any time: "Change depth to Comprehensive"

---

## Session Continuity

AI-PILC supports multi-session workflows:

- Progress is saved in `pilc-state.md` after every stage
- On new session start, the workflow detects existing state and offers to resume
- You can safely close and return at any time
- All decisions and context are preserved

---

## File Structure

```
ai-pilc/
├── README.md                          ← This file
├── ai-pilc-rules/
│   └── core-workflow.md               ← Master orchestration (always loaded)
└── ai-pilc-rule-details/
    ├── common/
    │   ├── process-overview.md        ← High-level process map
    │   ├── session-continuity.md      ← Resume/state management rules
    │   ├── question-format-guide.md   ← Structured question formatting
    │   ├── content-validation.md      ← Deliverable quality checks
    │   └── welcome-message.md         ← One-time welcome display
    ├── inception/
    │   ├── workspace-detection.md     ← Stage 1: Setup
    │   ├── source-ingestion.md        ← Stage 2: Receive requirements
    │   └── requirement-structuring.md ← Stage 3: Structure into Intake Form
    ├── assessment/
    │   ├── requirements-analysis.md   ← Stage 4: Gap/ambiguity analysis
    │   ├── clarification-cycle.md     ← Stage 5: Structured Q&A
    │   ├── feasibility-assessment.md  ← Stage 6: 4-dimension scoring
    │   └── prioritization.md          ← Stage 7: Strategic alignment + MoSCoW
    ├── justification/
    │   └── business-case.md           ← Stage 8: Investment case
    ├── authorization/
    │   └── project-charter.md         ← Stage 9: Formal authority
    ├── planning/
    │   ├── stakeholder-management.md  ← Stage 10: Stakeholder register
    │   ├── scope-definition.md        ← Stage 11: WBS + boundaries
    │   ├── resource-budget.md         ← Stage 12: Team + costs
    │   ├── risk-management.md         ← Stage 13: Risk register
    │   └── governance-communication.md← Stage 14: RACI + comms
    ├── mobilization/
    │   ├── kickoff-preparation.md     ← Stage 15: Kickoff agenda
    │   └── package-assembly.md        ← Stage 16: Final consolidation
    └── templates/                     ← Reusable deliverable skeletons
        ├── requirement-intake-form.md
        ├── feasibility-assessment.md
        ├── business-case.md
        ├── project-charter.md
        ├── stakeholder-register.md
        ├── scope-statement.md
        ├── resource-plan.md
        ├── risk-register.md
        ├── raci-matrix.md
        ├── kickoff-agenda.md
        ├── decision-log.md
        ├── change-log.md
        ├── issue-log.md
        ├── action-items.md
        ├── assumptions-dependencies.md
        └── lessons-learned.md
```

---

## Tenets

1. **Human in the loop** — AI recommends; human decides. No autonomous progression past gates.
2. **Source-driven** — Never invent scope. Always reference the user's input.
3. **Adaptive** — Scale rigor to complexity. Don't over-process simple projects.
4. **Resumable** — Work across sessions without losing progress.
5. **Auditable** — Every decision logged with rationale. Full traceability.
6. **Agnostic** — No dependency on specific IDE, model, or vendor.
7. **Professional** — PMBOK/PRINCE2-aligned outputs. PMO-ready quality.

---

## Methodology Alignment

AI-PILC draws from:

- **PMBOK 7th Edition** — Principles, performance domains, and process groups
- **PRINCE2** — Business case-driven, stage-gated, governance-focused
- **ITIL** — Service management context where applicable
- **AIDLC** — Adaptive workflow structure and interaction patterns (inspired by [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows))

---

## Differences from AI-DLC

| Aspect | AI-DLC | AI-PILC |
|--------|--------|---------|
| **Domain** | Software development | Project initiation (pre-execution) |
| **Output** | Code + documentation | Project management deliverables |
| **Phases** | Inception → Construction → Operations | Inception → Assessment → Justification → Authorization → Planning → Mobilization |
| **End State** | Working software | Execution-ready Project Initiation Package |
| **Audience** | Developers | Project Managers, PMOs, Business Analysts, Sponsors |

---

## Contributing

Contributions welcome. When modifying:

- Core workflow changes affect all users — test thoroughly
- Phase detail files can be enhanced independently
- Templates can be customized per organization
- Always maintain zero project-specific content in the framework

---

## Author

Created by **Maheri** — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)

Conceptualized and designed based on real-world PPM/PMO practice, combining structured project governance methodology with AI-driven interactive workflows.

---

## License

**Apache License 2.0 with Attribution Addendum**

- **Free to use:** Personal, commercial, educational, and organizational use — all permitted
- **Modify and distribute:** Create derivative works, redistribute, sublicense — all permitted
- **Attribution required:** Any distributed product substantially based on this work must include:

> *"Built on AIFLC by Mohammad Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)"*

- **No warranty:** Provided "AS IS" without warranties of any kind

See `LICENSE` in this directory and the canonical licensing documents in `../ai-license/` for full terms and FAQ.

**Copyright:** © 2026 Mohammad Maheri

> **Note:** AI-DLC (Development Life Cycle) is NOT part of the AI-* Family — it is a separate AWS product ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) licensed under MIT-0.
