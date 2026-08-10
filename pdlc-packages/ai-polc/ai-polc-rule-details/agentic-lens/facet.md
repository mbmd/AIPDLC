# AGENTIC Facet — AI-POLC

> **Loaded by the lens seam as an INTERSECTION FACET** when `management_framework/Lens_Status.md` shows **BOTH** `ai-lens = AI-Powered` **AND** `automation-lens = Automated`. Agentic is **not a lens** — it is a facet *composed* from the AI Lens and the Automation Lens (registered under `intersection-facets` in `contracts/LENS_REGISTRY.md`).
> **Runs after** the AI-LENS and Automation-LENS Step-1 scans on the same batch (it reads their results for convergence).
> **Integration points:** `strategy/epic-decomposition.md` (Stage 5, Step 5.7+) and `tier2/story-elaboration.md`.
> **Persona:** Product Manager / Product Ownership Lead (primary; no sub-role override).

---

## Purpose

Proactively identify which epics/stories are **agents** — features that BOTH *reason with a model* (AI Lens) AND *act autonomously across multiple steps without a human performing each step* (Automation Lens). This is the **origin point** where agent candidates are surfaced to the user: the AI Lens tells you what could be intelligent, the Automation Lens what could run unattended; this facet tells you where those meet — a candidate autonomous agent.

Agentic is **derived**: a confirmed agent carries both lens tags plus a `agenticProfile: true` marker. There is **no** `agenticFeatureId` and **no** agentic register — the feature is threaded by its existing `aiFeatureId` + `automationFeatureId`.

---

## Guardrail

This facet operates strictly within the Product Manager's lane:
- Identify **what** is an agent candidate and **why** (product value, autonomy need).
- Define **what good looks like** for an agent from the user's perspective (autonomy scope, task-completion, escalation).
- DO NOT design **how** the agent is built — tool/function-calling, the reasoning loop, memory, multi-agent orchestration are all **AI-ADLC's** lane (the agentic architecture facet).
- DO NOT design the agent's interaction/transparency UX (**AI-UXD**).
- DO NOT mint a new id or register — agentic is a derived shadow of the two lens tags.

---

## When This Facet Fires

Only when **both** lenses are active at the product level (`ai-lens = AI-Powered` AND `automation-lens = Automated` in `Lens_Status.md`). If either is OFF, this facet does not load — a feature cannot be agentic without both intelligence and autonomy.

1. **During epic decomposition (Stage 5):** after the AI-LENS scan and the Automation-LENS scan have run on the batch, run the Agentic-Opportunity Scan (below).
2. **During story elaboration (Tier 2, if active):** when elaborating stories under an agentic-profiled epic, carry the two ids forward and refine story-level agentic acceptance criteria.

---

## Step 1: Agentic-Opportunity Scan

For each epic (or story, in Tier 2), detect agent candidates two ways:

### Detection mode A — Convergence

The feature was tagged by **both** the AI-LENS scan (an `aiFeature` with sub-mode `augmented` or `native`) **and** the Automation-LENS scan (an `automationFeature` with mode `attended` or `unattended`). Convergence at these thresholds is the strongest agent signal: the product wants something that reasons *and* acts unsupervised.

- Below-threshold combinations (`opportunity` × `assisted`, or either lens absent) are **not** auto-proposed as agentic — but see Detection mode B, and the user may always opt in.

### Detection mode B — Dedicated agentic signals

Scan the epic/story text for agentic intent even where only one lens (or neither) tagged it:

| Signal category | Examples |
|-----------------|----------|
| **Goal-directed autonomy** | "autonomously resolve/investigate/handle…", "end-to-end without a human", "own the outcome, not just a step" |
| **Multi-step reason-then-act** | "plan then execute", "figure out how to…", "iterate until done", "decide the next action based on the result" |
| **Tool / system use to accomplish a goal** | "use {the tools/systems} to complete…", "take actions across {systems} to achieve…", "call whatever it needs to finish the task" |

If mode B fires but the two lens tags are not both present at threshold, the scan will propose setting them (Step 2) — it is surfacing an agent the single-lens scans under-classified.

### Scan behavior

- Read the epic/story description, acceptance criteria, and the results of the two lens scans on this batch.
- If neither convergence nor a dedicated agentic signal is present → this is not an agent; skip and move on.
- If either fires → proceed to Step 2.

---

## Step 2: Propose Classification

For each detected agent candidate, present:

```
Agentic Candidate Detected:
  Epic/Story:  {epic-id} — {title}
  Signal:      "{quoted text or paraphrase}"
  Why agentic: reasons with a model AND acts autonomously ({convergence | agentic-signal})
  Proposed:    aiFeature = {augmented | native}
               automationFeature = {attended | unattended}
               agenticProfile = true
  Rationale:   {one sentence — why this is an agent, not just an AI feature or just an automation}

Confirm? (yes / AI-only / automation-only / not agentic)
```

Wait for user confirmation. The user may:
- **yes** → it is an agent; apply the profile (Step 3).
- **AI-only** → intelligent but not autonomous; only the AI Lens tags it (no profile). The AI-LENS facet owns it.
- **automation-only** → autonomous but not model-driven; only the Automation Lens tags it (no profile). The Automation-LENS facet owns it.
- **not agentic** → drop; no tags added by this scan.

The scan **proposes; the user confirms** — never auto-apply.

---

## Step 3: Apply the Agentic Profile

On **yes**, ensure the feature carries **both** lens tags (set any that the single-lens scans did not already apply, at the confirmed sub-mode/mode), then stamp the derived marker in the epic/story front-matter:

```yaml
---
aiFeature: true
aiSubMode: augmented | native          # must be augmented or native for agentic
aiCapability: {from the AI taxonomy — often conversational or planning}
aiFeatureId: AIF-{NNN}
automationFeature: true
automationMode: attended | unattended  # must be attended or unattended for agentic
automationPattern: {from the automation taxonomy}
automationTrigger: {scheduled | event | manual | continuous}
automationFeatureId: AUTO-{NNN}
agenticProfile: true                   # DERIVED — a shadow of the two tags above
---
```

**Rules:**
- **No `agenticFeatureId`** is minted — the feature threads by `aiFeatureId` + `automationFeatureId` (both required whenever `agenticProfile: true`).
- The profile is a **shadow**: if a later edit removes either lens tag, or drops `aiSubMode` below `augmented`/`native` or `automationMode` below `attended`/`unattended`, the `agenticProfile` marker **must be removed** — it cannot outlive the combination that defines it.
- The two lens facets still run and write their own acceptance criteria for the feature; this facet **adds** the agentic layer on top.

---

## Step 4: Write Agentic Acceptance Criteria

For each confirmed agent, write **product-level** acceptance criteria — what a good agent looks like from the user's perspective. These bound the autonomy and define success; they do NOT prescribe architecture (that is AI-ADLC).

| Category | What it defines | Example |
|----------|-----------------|---------|
| **Autonomy scope** | What the agent may do end-to-end vs. what always requires a human | "The agent may triage, research, and draft a resolution autonomously; issuing a refund always requires human approval." |
| **Tool inventory (intent-level)** | The kinds of tools/systems the agent may use to accomplish the goal — named at intent level, never as APIs | "May read the ticket system, search the knowledge base, and query order history; may NOT modify billing." |
| **Task-completion definition** | What "done" means for one agent task — the success signal | "A task is complete when a resolution is drafted and either sent (within autonomy scope) or queued for human approval." |
| **Escalation path** | What the agent does when it cannot complete, hits its budget, or is low-confidence | "On low confidence, ambiguity, or after N steps, the agent stops and hands off to a human with its reasoning summary." |

### Writing rules

- Write from the **user's / process-owner's perspective** (what they need), not the system's (how it's built).
- Make each criterion **testable** — AI-TGE will later derive trajectory / task-completion evals from these.
- Do NOT name model frameworks, agent libraries, tool-calling mechanisms, or loop patterns (that's ADLC's job).
- Place under a `## Agentic Acceptance Criteria` heading in the epic/story body (or an `agenticAcceptanceCriteria` array in front-matter for machine extraction).

### Format

```markdown
## Agentic Acceptance Criteria

- **Autonomy scope:** {what it may do unattended vs. what needs a human}
- **Tool inventory (intent):** {kinds of tools/systems it may use}
- **Task-completion:** {what "done" means for one task}
- **Escalation:** {what it does when it can't complete / low confidence / budget hit}
```

Minimum: all four categories for a `native × unattended` agent; autonomy scope + escalation are mandatory for any agent.

---

## Step 5: Prioritization & Inform Downstream

- **Prioritization signal:** agents are typically high-value and high-governance (an unattended agent that acts on real systems carries the combined weight of both lenses). Surface this to the user for the Stage 5/6 prioritization model; do not auto-override scores.
- **Summary line:** "Agentic: {N} agent candidates confirmed across {M} epics — {list of AIF-{NNN}+AUTO-{NNN} pairs}."
- **Downstream:** the two ids + `agenticProfile` are exposed via POLC's `data-schema/` (the `agenticProfile.agenticFeatures[]` field) for AI-DFE threading. The confirmed agents flow to:
  - **AI-UXD** — agent-interaction transparency (reasoning/tool-use visibility, working states, interruptibility);
  - **AI-ADLC** — the agent architecture (tool-use, reasoning-loop, memory, agent-eval, agent-cost) + the action-surface coherence check;
  - **AI-DWG** — agent-framework provisioning + Layer-3 courier;
  - **AI-GCE / AI-TGE** — extended agentic governance + quality checks (via the existing `AIG__/ATG__/AIQ__/ATQ__`).

---

## Tier 2 Behavior (Story Elaboration)

When Tier 2 is active and stories are elaborated under an agentic-profiled epic:
- Each story inherits the epic's `aiFeatureId` + `automationFeatureId` (via `derivedFrom`); a story carries `agenticProfile: true` only if it is itself a distinct agent unit.
- Refine story-level agentic acceptance criteria where they differ from the epic level (e.g. one story owns the escalation path; another owns a specific autonomous action).
- Stories that are not agents within an agentic epic do NOT get the profile (e.g. a settings screen under an autonomous-triage epic).

---

## Relationship to the Two Lens Facets

This facet does **not** replace or duplicate the AI-LENS and Automation-LENS POLC facets — they still run, tag, classify, and write their own acceptance criteria for the feature. Agentic **composes** them: it recognizes the intersection, stamps the derived profile, and adds the agentic acceptance layer (autonomy scope, tool inventory, task-completion, escalation) that neither lens writes alone. Read the two sibling facets (`ai-lens/facet.md`, `automation-lens/facet.md`) for their own scan + tag behavior.

---

## What This Facet Does NOT Do

- Does not design tool/function-calling, the reasoning loop, agent memory, or multi-agent orchestration (AI-ADLC agentic architecture facet).
- Does not design agent-interaction transparency or controls UX (AI-UXD).
- Does not provision the agent framework or courier context (AI-DWG).
- Does not run trajectory eval, step-cap tests, or excessive-agency governance (AI-TGE `AIQ__`/`ATQ__` + AI-GCE `AIG__`/`ATG__`).
- Does not mint an `agenticFeatureId` or maintain an agentic register (derived-only; threaded by the two lens ids).
- Does not re-classify or re-tag what the two lens scans already own — it only adds the agentic layer.

---

*AGENTIC Facet — AI-POLC v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens) | Integration: Stage 5 (epic-decomposition) + Tier 2 (story-elaboration) | Author: Maheri*
