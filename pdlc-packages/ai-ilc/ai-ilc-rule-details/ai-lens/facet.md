# AI-LENS Facet — AI-ILC

> **Loaded by the lens seam** when `Lens_Status.md` AI-LENS row = `AI-Powered` (or when no mode exists yet — ILC is the first-touch capture point).
> **Integration points:** `idea-lifecycle/shape.md` (Stage 2) and `idea-lifecycle/evaluate.md` (Stage 3).
> **Persona:** Product Manager / Innovation Pipeline Lead (primary; no sub-role override).

---

## Purpose

Capture the AI posture of an idea at the earliest possible point in the lifecycle. ILC is the first node in the chain; it records whether an idea has AI potential before a project even exists. This posture travels forward to AI-PILC (where it becomes a formal Decision_Log row) and to AI-POLC (where individual features are identified and tagged).

---

## When This Facet Fires

1. **During shape (Stage 2):** after the idea is articulated and before it is evaluated, run the Resolution Protocol to capture AI Posture on the Idea Brief.
2. **During evaluate (Stage 3):** note the high-level AI capability signal and potential for the scoring model (light touch; deep feasibility is PILC's job).

---

## Step 1: Resolution Protocol (at Shape)

Run the AI-LENS Resolution Protocol at shape stage:

1. **Read** the current AI-mode state:
   - At ILC level, there is no spine `Decision_Log` yet (ideas are pre-project). Check if an AI posture has already been set on this Idea Brief (resuming a prior session).
2. **If no posture recorded:**
   - Ask: "Does this idea involve or benefit from AI/ML capabilities?"
   - Present the choice:
     ```
     AI Posture for this idea:
       [ ] No-AI — this idea does not involve AI
       [ ] Opportunity — AI could add value as an enhancement
       [ ] Augmented — the idea is deliberately about AI enhancement
       [ ] Native — the idea fundamentally requires AI to exist
     ```
   - Record the user's choice as the AI Posture on the Idea Brief.
3. **If posture already set:**
   - Inform: "AI Posture: {value}, set previously."
   - Offer: "Change it? (re-select above)"

### Recording the Posture

Add to the Idea Brief front-matter:

```yaml
---
aiPosture: no-ai | opportunity | augmented | native
aiCapability: {value from taxonomy, if AI}
aiFeatureId: AIF-{NNN}
---
```

- `aiPosture` — the user's choice (maps directly to the sub-mode vocabulary; `no-ai` maps to the off state).
- `aiCapability` — set at evaluate (Step 2); left `null` at shape if not yet assessed.
- `aiFeatureId` — mint only if the idea IS an AI feature (posture != `no-ai`). This opens the thread that travels through the entire chain. Mint as `AIF-{NNN}` (scan existing project/idea briefs for the highest, increment).

---

## Step 2: Capability Signal (at Evaluate)

During the evaluation stage, when scoring the idea, add a lightweight AI assessment:

1. **If posture = `no-ai`:** skip entirely. No AI scoring dimension needed.
2. **If posture = opportunity/augmented/native:**
   - Identify the **primary AI capability** this idea would leverage (from the 21-entry taxonomy).
   - Record it as `aiCapability` on the Idea Brief front-matter.
   - Note it in one line for the scoring context: "AI capability signal: {capability} — {one-sentence rationale}"
   - This is a **signal only** — not a feasibility assessment (that's PILC's job). It informs the evaluator's judgment of technical risk and strategic fit.

### Capability Taxonomy (quick reference)

| # | Capability | Signal |
|---|------------|--------|
| 1 | `classification` | Categorizing inputs into predefined labels |
| 2 | `prediction` | Forecasting future values/outcomes |
| 3 | `recommendation` | Suggesting items/actions/content |
| 4 | `generation` | Producing text/images/code/artifacts |
| 5 | `summarization` | Condensing content |
| 6 | `semantic-search` | Meaning-based retrieval (incl. RAG) |
| 7 | `personalization` | Adapting to individual context |
| 8 | `anomaly-detection` | Identifying outliers/unusual patterns |
| 9 | `extraction` | Structured data from unstructured sources |
| 10 | `conversational` | Interactive dialogue/agentic behavior |
| 11 | `optimization` | Optimal solutions/ranking |
| 12 | `clustering` | Grouping similar items (unsupervised) |
| 13 | `translation` | Language conversion |
| 14 | `transcription` | Speech/audio to text |
| 15 | `planning` | Goal decomposition into steps |
| 16 | `moderation` | Policy/harm detection |
| 17 | `causal-inference` | Cause-effect relationships |
| 18 | `simulation` | What-if scenario modeling |
| 19 | `verification` | Correctness checking against ground truth |
| 20 | `entity-resolution` | Identity matching across records |
| 21 | `speech-synthesis` | Text to spoken audio |

---

## Step 3: Route-Handoff Signal (at Stage 6)

When the idea is approved and routed (to PILC/POLC/backlog):

- Include the AI Posture in the handoff brief so the receiving package knows the AI state without re-asking.
- The receiving package (PILC) will promote this posture into a formal `Decision_Log` row on the project spine.
- If routed directly to POLC (skipping PILC), POLC's facet will read the posture from the Idea Brief and handle it at its own Resolution Protocol step.

---

## What This Facet Does NOT Do

- Does not assess feasibility, cost, or regulatory risk (AI-PILC).
- Does not identify or tag individual AI features (AI-POLC).
- Does not make architecture or implementation decisions.
- Does not create a `Decision_Log` row (that's PILC's job; ILC is pre-project and has no spine yet).

---

*AI-LENS ILC Facet v1.0.0 | Integration: Stage 2 (shape) + Stage 3 (evaluate) + Stage 6 (route-handoff) | Author: Maheri*
