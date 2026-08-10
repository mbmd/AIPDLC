# AGENTIC Facet — AI-PILC

> **Loaded by the lens seam as an INTERSECTION FACET** when `management_framework/Lens_Status.md` shows BOTH `AI-LENS = AI-Powered` AND `Automation = Automated`. Agentic is **not a lens** — it is composed from the two (`contracts/LENS_REGISTRY.md` → `intersection-facets`); it promotes **no mode of its own** (the two lens facets already promoted theirs).
> **Runs after** the AI-LENS and Automation-LENS PILC facets — it adds the agent-specific **delta** to their feasibility / cost / risk work; it does not repeat them.
> **Integration points:** `assessment/` (Stage 4–7) + `justification/` (Stage 8).
> **Persona:** PMO Professional / Senior Project Manager (primary; sub-role `#persona-subrole-risk-analyst` for agent feasibility/risk, `#persona-subrole-financial-analyst` for loop-cost).

---

## Purpose

Assess the **agent dimension** at the project level — the part that is specific to a feature being an *autonomous agent* and is NOT already covered by the AI feasibility or automation suitability assessments the two lens facets perform. Three deltas only: **agent feasibility** (tool/action integration + loop realism), an **EU-AI-Act elevation** note (action-taking agents often sit a class higher than a passive AI feature), and **loop-cost realism** (multi-step amplification). Agentic is derived — no separate mode row, no new id.

---

## When This Facet Fires

Only when both lens modes are at threshold (`aiSubMode ∈ {augmented, native}` AND `automationMode ∈ {attended, unattended}`). It fires during **assessment** (agent feasibility + EU-AI-Act elevation) and **justification** (loop-cost), folding into the two lenses' existing PIP sections — never duplicating them.

---

## Step 1: Recognize the Agentic Profile (at Assessment)

The two lens facets promote their own modes into the spine + `Lens_Status.md`. This facet promotes **nothing** — it recognizes the derived agentic profile (both modes at threshold, or an `agenticPosture: candidate` carried from an ILC Idea Brief) and notes it so the deltas below are captured:

> "Agentic profile: this project has agent candidate(s) — model reasoning + attended/unattended action. Agent-specific feasibility, regulatory, and cost deltas assessed below."

No `Decision_Log` row of its own (the two lens rows already record the modes); no id.

---

## Step 2: Agent Feasibility Delta (at Assessment)

Add only the agent-specific dimensions the AI-feasibility + automation-suitability tables do **not** already cover:

| Dimension | Key question | Output |
|-----------|-------------|--------|
| **Tool / action integration** | Do the systems the agent must act on expose usable, permissioned interfaces? Is each action reversible and auditable? | Ready / Partial / Gap |
| **Loop realism** | Can the task be decomposed into a bounded reason-act loop that terminates (clear success + a step/cost ceiling)? Or is it open-ended? | Bounded / Needs-bounding / Open-ended-risk |
| **Autonomy vs. oversight fit** | Does the desired autonomy (attended vs. unattended) match the risk of the actions taken? | Aligned / Over-autonomous / Under-autonomous |
| **Failure containment** | Is there a safe stop / escalation / kill path when the agent goes wrong? | Present / Design-required |

Record under `## Agent Feasibility` in the PIP feasibility section. **Overall agent feasibility:** {Feasible / Feasible-with-conditions / Not-feasible}. If `Open-ended-risk` or `Design-required`, add it to the project risk register alongside the AI/automation risks.

---

## Step 3: EU-AI-Act Elevation (at Assessment)

An agent that *takes actions* (not just produces content) frequently sits a **class higher** than the same capability would as a passive AI feature — autonomous action in a real domain raises risk. This is an **annotation on the AI-LENS EU-AI-Act classification (its Step 5)**, never a second classification:

- If the agent acts **unattended** in a domain the AI-LENS facet rated `limited`, re-examine for `high` — autonomous action can cross the high-risk threshold that a suggestion-only feature would not.
- Record the elevation (or the reasoned decision not to elevate) as a one-line note next to the existing AI-LENS classification row.

> Single source of truth for the EU-AI-Act class stays with the AI-LENS facet; this facet only annotates it with the agentic elevation.

---

## Step 4: Loop-Cost Realism (at Justification)

The AI-LENS cost model captures per-inference cost. Agents change its **shape**: one agent task = many model calls (the reason-act loop iterates). Add one line to the AI Cost Analysis — do not build a second cost table:

> "**Agentic cost multiplier:** each agent task runs a multi-step loop, so model cost scales with *steps-per-task × tasks*, not calls. Budget an average and a worst-case step count per task; the AI-ADLC agent-cost design will impose a per-task step/cost ceiling."

This keeps the business case from being under-budgeted for autonomous loops.

---

## What This Facet Does NOT Do

- Does not repeat the AI feasibility / automation suitability / cost / risk assessments — the two lens facets own those; this adds only the agent delta.
- Does not identify individual agents in the backlog (AI-POLC's Agentic-Opportunity Scan).
- Does not design tool-calling, the reasoning loop, memory, or the step/cost ceiling (AI-ADLC).
- Does not create a mode row or mint an id (derived; the two lens rows + ids already exist).
- Does not enforce agent governance or run agent evals (AI-GCE / AI-TGE).

---

*AGENTIC Facet — AI-PILC v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens) | Integration: Assessment (agent feasibility + EU-AI-Act elevation) + Justification (loop-cost) | Author: Maheri*
