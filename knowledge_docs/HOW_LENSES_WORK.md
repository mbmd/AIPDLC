# How Lenses Work (AI Lens, Automation Lens, and the Agentic Facet)

**Purpose:** Explains the two cross-cutting **lenses** — the AI Lens and the Automation Lens — that make every design-chain package design a domain-specific facet of your product, plus the **Agentic facet** that emerges where both are active. Covers how they switch on, how features are tagged, and how they are governed and tested across the AI-* PDLC Family.

---

## What a Lens Is

A **lens** is a cross-cutting mode. When it is on, every design-chain package applies a domain-specific **facet** as it designs its slice of the product — one switch, a different facet per package. Lenses are **orthogonal**: a single feature can carry several lens tags at once, and each lens designs its own slice independently.

The design-chain packages that apply lens facets are the ones that produce design artifacts — AI-Driven Idea Life Cycle (AI-ILC), AI-Driven Project Initiation Life Cycle (AI-PILC), AI-Driven Product Ownership Life Cycle (AI-POLC), AI-Driven UX Design (AI-UXD), AI-Driven Architecture Design Life Cycle (AI-ADLC), and AI-Driven Workspace Generator (AI-DWG). The engine cores (AI-Driven Governance & Compliance Engine (AI-GCE), AI-Driven Test Governance Engine (AI-TGE), AI-Driven Data Fabric Engine (AI-DFE)) carry no facet seam — their lens work is delivered as **manually-triggered agents**.

---

## The Two Lenses

| Lens | OFF value | ON value | Sub-modes | Feature tag |
|------|-----------|----------|-----------|-------------|
| **AI Lens** | `No-AI` | `AI-Powered` | Opportunity / Augmented / Native | `aiFeature` (id prefix `AIF`) |
| **Automation Lens** | `Manual` | `Automated` | Assisted / Attended / Unattended | `automationFeature` (id prefix `AUTO`) |

- The **AI Lens** designs AI features across the chain — model-serving / RAG architecture, human-in-the-loop AI UX, and AI governance and testing — including EU AI Act obligations.
- The **Automation Lens** designs automated features — workflow automation, and the approval / monitoring / override UX that a Manual, Assisted, Attended, or Unattended automation needs.

Each lens's current mode is the single source of truth in `management_framework/Lens_Status.md`.

---

## Switching a Lens On or Off

Two triggers report and toggle the lenses, and they work regardless of which package is active (no package switch needed):

| Trigger | Does |
|---------|------|
| `_AILENS_` | Prints the current AI-Lens mode (`No-AI` / `AI-Powered` + active palette) from `Lens_Status.md`, and offers a one-line change |
| `_AUTOLENS_` | Prints the current Automation-Lens mode (`Manual` / `Automated` + active palette) from `Lens_Status.md`, and offers a one-line change |

On a confirmed change, the toggle performs a **dual write** — it appends a history row to the `Decision_Log` and upserts the mode row in `Lens_Status.md` (the live single source of truth). Adding a new lens is a registry-only change: the machinery reads the lens registry rather than hard-coding any one lens.

---

## How Features Get Tagged

Once a lens is on, features are tagged as they flow down the chain:

- **AI-PILC** records the active modes in the governance spine (`Lens_Status.md`).
- **AI-POLC** tags features — `aiFeature` and/or `automationFeature` — and derives the `agenticProfile` where both apply.
- **AI-UXD** and **AI-ADLC** design the tagged facets (AI UX / AI architecture; automation UX / automation architecture).
- **AI-DWG** provisions the scaffolding, and seeds the lens governance/quality agents into the generated workspace.

---

## The Agentic Facet — an Intersection, Not a Third Lens

The **Agentic facet** is a distinct kind: it is **composed** from the two lenses rather than being a lens of its own. It activates only where the AI Lens is `AI-Powered` **and** the Automation Lens is `Automated`, and only above a sub-mode threshold — the AI sub-mode is `augmented` or `native` **and** the automation sub-mode is `attended` or `unattended`.

Where it holds, a derived **`agenticProfile`** marker appears on the feature — a shadow of the two underlying lens tags. It gives guidance on tool-use, memory, and reasoning-loop design; tool-permission and kill-switch governance; and trajectory / step-cap testing. Because it is derived, it carries **no feature id of its own and no register** — it is threaded by the two underlying tags (`aiFeatureId`, `automationFeatureId`), and it **dissolves automatically** if either lens drops below the threshold.

---

## Governing and Testing the Lens Facets

When a lens is active, AI-GCE and AI-TGE provide manually-triggered Layer-3 agents seeded by AI-DWG:

| Trigger | Agent | Owner | Does |
|---------|-------|-------|------|
| `AIG__` | AI Governance | AI-GCE | AI governance checks — EU AI Act obligations, responsible-AI, PII boundary, model pinning, prompt review, cost controls. Writes to `.governance/ai-lens/` |
| `AIQ__` | AI Quality & Drift | AI-TGE | AI quality + drift — golden-set eval, acceptance-criteria validation, hallucination/bias/injection testing, drift monitoring |
| `ATG__` | Automation Governance | AI-GCE | Automation governance — audit-trail completeness, kill-switch / loop-guard presence, segregation of duties, least-privilege identity. Writes to `.governance/automation-lens/` |
| `ATQ__` | Automation Quality | AI-TGE | Automation verification — idempotency, exception-path coverage, retry/compensation, rollback, and the loop test (fire the trigger; assert the causal chain terminates within the hop budget) |

The AI-LENS agents are available when the AI Lens is `AI-Powered`; the Automation-Lens agents when the Automation Lens is `Automated`.

---

## What Stays the Same

- With both lenses OFF (`No-AI` + `Manual`), the chain behaves exactly as a non-lens project — zero facet load, no lens agents.
- Lenses are orthogonal and additive — turning one on never changes how the other behaves.
- Adding a future lens is a registry-only change; the packages do not hard-code any single lens.

---

## Related Documents

| Document | Location |
|----------|----------|
| Reference Map — Triggers | `knowledge_docs/REFERENCE_MAP_TRIGGERS.md` |
| How to Design Architecture | `knowledge_docs/HOW_TO_DESIGN_ARCHITECTURE.md` |
| How to Design User Experience | `knowledge_docs/HOW_TO_DESIGN_USER_EXPERIENCE.md` |
| How to Manage Product Backlog | `knowledge_docs/HOW_TO_MANAGE_PRODUCT_BACKLOG.md` |
| How GCE Compliance Audit Works | `knowledge_docs/HOW_GCE_COMPLIANCE_AUDIT_WORKS.md` |
| How TGE Test Governance Works | `knowledge_docs/HOW_TGE_TEST_GOVERNANCE_WORKS.md` |

*Knowledge Document | Created: 2026-09-05 | Updated: 2026-09-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
