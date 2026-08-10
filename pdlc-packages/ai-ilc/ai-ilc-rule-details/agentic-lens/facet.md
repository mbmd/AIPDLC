# AGENTIC Facet — AI-ILC

> **Loaded by the lens seam as an INTERSECTION FACET** when BOTH lenses are active. At AI-ILC (pre-project — there is no governance spine or `Lens_Status.md` yet), activation is **derived from the two postures on the Idea Brief**: `aiPosture ∈ {augmented, native}` **AND** `automationPosture ∈ {attended, unattended}`. Agentic is **not a lens** — it is a facet composed from the AI Lens and the Automation Lens (`contracts/LENS_REGISTRY.md` → `intersection-facets`).
> **Runs after** the AI-LENS and Automation-LENS posture capture (Step 1 of each).
> **Integration points:** `idea-lifecycle/shape.md` (Stage 2) + `idea-lifecycle/evaluate.md` (Stage 3) + `idea-lifecycle/route-handoff.md` (Stage 6).
> **Persona:** Product Manager / Innovation Pipeline Lead (primary; no sub-role override).

---

## Purpose

Record the **agentic posture** of an idea at the earliest possible point — a derived note that this idea looks like an *autonomous agent* (it would both reason with a model and act autonomously without a human performing each step). This is a light, derived signal: no new prompt, no new id, no scoring of its own. It travels forward so AI-PILC can assess agent feasibility and AI-POLC can run its Agentic-Opportunity Scan without re-discovering the idea.

---

## When This Facet Fires

Only when both lens postures are at threshold (above). It fires at **shape** (derive the posture, after the two lens postures are captured), is carried at **evaluate** (a one-line signal), and rides in the **route-handoff** brief.

---

## Step 1: Derive the Agentic Posture (at Shape — NO new prompt)

After the AI-LENS facet and the Automation-LENS facet have captured their postures on the Idea Brief, derive the agentic posture — **do not ask the user a new question**:

- IF `aiPosture ∈ {augmented, native}` **AND** `automationPosture ∈ {attended, unattended}` → the idea is an **agent candidate**.
- ELSE → not agentic; add no marker.

Record on the Idea Brief front-matter (a derived shadow of the two postures — no new id):

```yaml
---
# aiPosture / automationPosture + their ids are already set by the two lens facets
agenticPosture: candidate     # DERIVED — both lens postures at threshold; dissolves if either drops below it
---
```

Inform in one line: "This idea looks **agentic** (reasons + acts autonomously) — noted; AI-PILC will assess agent feasibility."

If a prior session set `agenticPosture` and either lens posture has since dropped below threshold, **remove** the marker (it is a shadow, never independent).

---

## Step 2: Agentic Signal (at Evaluate)

When scoring the idea, add one line of context — a **signal only**, no separate score and no feasibility (that is AI-PILC's job):

> "Agentic signal: autonomous-agent candidate (native/augmented AI + attended/unattended automation) — expect higher build complexity and governance weight; AI-PILC will assess."

This informs the evaluator's judgment of technical risk and strategic fit; it does not add a scoring dimension.

---

## Step 3: Route-Handoff Signal (at Stage 6)

Include the agentic posture in the handoff brief so the receiving package does not re-discover it:
- To **AI-PILC** → PILC's agentic facet assesses agent feasibility + EU-AI-Act elevation + loop-cost.
- To **AI-POLC** (if PILC is skipped) → POLC's Agentic-Opportunity Scan confirms the profile per feature.

The two lens postures + their ids travel as they already do; `agenticPosture` rides alongside them.

---

## What This Facet Does NOT Do

- Does not ask a new question — it is derived from the two lens postures.
- Does not assess agent feasibility, loop-cost, or regulatory class (AI-PILC).
- Does not identify or confirm per-feature agents (AI-POLC's Agentic-Opportunity Scan).
- Does not mint an id or create a spine row (ILC is pre-project; the feature is threaded by the two lens ids).

---

*AGENTIC Facet — AI-ILC v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens) | Integration: Stage 2 (shape) + Stage 3 (evaluate) + Stage 6 (route-handoff) | Author: Maheri*
