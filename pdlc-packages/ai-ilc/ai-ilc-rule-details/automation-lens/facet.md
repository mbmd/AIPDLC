# Automation-LENS Facet — AI-ILC

> **Loaded by the lens seam** when `Lens_Status.md` Automation row = `Automated` (or when no mode exists yet — ILC is the first-touch capture point).
> **Integration points:** `idea-lifecycle/shape.md` (Stage 2) and `idea-lifecycle/evaluate.md` (Stage 3).
> **Persona:** Product Manager / Innovation Pipeline Lead (primary; no sub-role override).

---

## Purpose

Capture the Automation posture of an idea at the earliest possible point in the lifecycle. ILC is the first node in the chain; it records whether an idea involves automated processes before a project even exists. This posture travels forward to AI-PILC (where it becomes a formal Decision_Log row) and to AI-POLC (where individual automated features are identified and tagged).

---

## When This Facet Fires

1. **During shape (Stage 2):** after the idea is articulated and before it is evaluated, run the Resolution Protocol to capture Automation Posture on the Idea Brief.
2. **During evaluate (Stage 3):** note the high-level automation pattern signal and potential for the scoring model (light touch; deep suitability assessment is PILC's job).

---

## Step 1: Resolution Protocol (at Shape)

Run the Automation-LENS Resolution Protocol at shape stage:

1. **Read** the current automation-mode state:
   - At ILC level, there is no spine `Decision_Log` yet (ideas are pre-project). Check if an automation posture has already been set on this Idea Brief (resuming a prior session).
2. **If no posture recorded:**
   - Ask: "Does this idea involve automating a process or running actions without human intervention?"
   - Present the choice:
     ```
     Automation Posture for this idea:
       [ ] Manual — this idea does not involve automation
       [ ] Assisted — automation helps but a human still performs the task
       [ ] Attended — automation performs it but needs human trigger/approval
       [ ] Unattended — automation runs end-to-end without human involvement
     ```
   - Record the user's choice as the Automation Posture on the Idea Brief.
3. **If posture already set:**
   - Inform: "Automation Posture: {value}, set previously."
   - Offer: "Change it? (re-select above)"

### Recording the Posture

Add to the Idea Brief front-matter:

```yaml
---
automationPosture: manual | assisted | attended | unattended
automationPattern: {value from taxonomy, if automated}
automationFeatureId: AUTO-{NNN}
---
```

- `automationPosture` — the user's choice (maps directly to the sub-mode vocabulary; `manual` maps to the off state).
- `automationPattern` — set at evaluate (Step 2); left `null` at shape if not yet assessed.
- `automationFeatureId` — mint only if the idea IS about automation (posture != `manual`). This opens the thread that travels through the entire chain. Mint as `AUTO-{NNN}` (scan existing project/idea briefs for the highest, increment).

---

## Step 2: Pattern Signal (at Evaluate)

During the evaluation stage, when scoring the idea, add a lightweight automation assessment:

1. **If posture = `manual`:** skip entirely. No automation scoring dimension needed.
2. **If posture = assisted/attended/unattended:**
   - Identify the **primary automation pattern** this idea would follow (from the 13-entry taxonomy).
   - Record it as `automationPattern` on the Idea Brief front-matter.
   - Note it in one line for the scoring context: "Automation pattern signal: {pattern} — {one-sentence rationale}"
   - This is a **signal only** — not a suitability assessment (that's PILC's job). It informs the evaluator's judgment of implementation complexity and ROI potential.

### Pattern Taxonomy (quick reference)

| # | Pattern | Signal |
|---|---------|--------|
| 1 | `workflow-orchestration` | Multi-step process coordinating systems/actors |
| 2 | `task-automation` | Discrete, repetitive single-task automation |
| 3 | `data-pipeline` | Data movement and transformation (ETL/ELT/stream) |
| 4 | `integration` | System-to-system connection and exchange |
| 5 | `rules-decision` | Deterministic rules/policy engine decisioning |
| 6 | `routing-assignment` | Routing, assigning, or dispatching work items |
| 7 | `approval-workflow` | Multi-step approval, review, or escalation |
| 8 | `notification` | Automated alerts, reminders, messages |
| 9 | `document-generation` | Automated assembly of documents/reports |
| 10 | `intake-processing` | Capture and processing of inbound items |
| 11 | `reconciliation-matching` | Matching/reconciling records across sources |
| 12 | `remediation` | Corrective action in response to a condition |
| 13 | `state-transition` | Automated entity lifecycle/status progression |

---

## Step 3: Route-Handoff Signal (at Stage 6)

When the idea is approved and routed (to PILC/POLC/backlog):

- Include the Automation Posture in the handoff brief so the receiving package knows the automation state without re-asking.
- The receiving package (PILC) will promote this posture into a formal `Decision_Log` row on the project spine.
- If routed directly to POLC (skipping PILC), POLC's facet will read the posture from the Idea Brief and handle it at its own Resolution Protocol step.

---

## Co-Existence with AI-LENS

An idea may carry BOTH an AI Posture and an Automation Posture. They are independent questions:
- "Does this idea use AI?" → AI Posture
- "Does this idea automate a process?" → Automation Posture

Both are captured during shape; both travel forward independently. The seam loads both facets when both lenses are active.

---

## What This Facet Does NOT Do

- Does not assess process suitability, ROI, or control class (AI-PILC).
- Does not identify or tag individual automation features (AI-POLC).
- Does not make orchestration or infrastructure decisions.
- Does not create a `Decision_Log` row (that's PILC's job; ILC is pre-project and has no spine yet).

---

*Automation-LENS ILC Facet v1.0.0 | Integration: Stage 2 (shape) + Stage 3 (evaluate) + Stage 6 (route-handoff) | Author: Maheri*
