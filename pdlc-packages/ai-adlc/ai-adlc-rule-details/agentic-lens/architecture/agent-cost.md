# Agentic Architecture — Agent Cost

> **Sub-module of** `agentic-lens/facet.md` (light delta). Loaded on demand when designing an agent's cost model and budget controls.
> **Sub-role:** `#persona-subrole-ai-engineer`
> **Reuses from (do not re-document):** token/inference budgets, cost attribution, usage monitoring, and cost-control mechanisms (rate limiting, caching, cheaper-model fallback) from `ai-lens/architecture/cost.md`. This file is a **thin delta** — it corrects the unit of cost for a multi-step agent.

---

## What is new here

`ai-lens/architecture/cost.md` budgets **per request** — the right unit for a single model call. An agent makes **many** model calls and tool calls per task: one task = N loop steps, each with its own inference (and possibly tool) cost. A per-request budget that looks fine can multiply into a per-task cost that does not. Agent cost re-frames the budget around the **task and its loop**, then reuses every control mechanism from the parent sub-module.

---

## Decision Framework

### 1. Loop-Amplified Cost Model

Model cost at the **task** unit, not the request unit:

```
cost(task) ≈ steps(task) × [ inference_cost(step) + tool_cost(step) ]
```

| Driver | Effect on cost |
|--------|----------------|
| **Steps per task** | Linear multiplier — the dominant agentic cost factor |
| **Reflection / re-planning** | Adds steps (and therefore cost) — account for the pattern chosen in `reasoning-loop.md` |
| **Context growth** | Later steps carry more context (history + memory), so per-step token cost tends to *rise* across a task |
| **Tool costs** | External-call tools may carry their own per-invocation price |

**Design rule:** estimate cost at **expected** and **worst-case (step-cap)** step counts. The worst case is bounded by the termination contract — which is exactly why that contract is also a cost control.

### 2. Per-Task Step Budget

The step cap from `reasoning-loop.md` **is** the primary cost ceiling — express it in cost terms here.

- Set the step budget from the expected task shape plus a safety margin — not an arbitrary large number.
- Translate the step budget into a **worst-case task cost** and check it against the per-feature budget from `ai-lens/architecture/cost.md`.
- If worst-case task cost × expected task volume exceeds the feature budget, the design is not viable at scale — flag it as a risk (as `ai-lens/architecture/cost.md` §5 does for scale tiers).

### 3. Cost-Ceiling Termination

Add **cost** as a termination limit in the loop's termination contract (`reasoning-loop.md` §2):

- Track accumulated spend per task; when it reaches the ceiling, terminate and escalate (same exhaustion path as any other limit).
- The cost ceiling is a **hard stop**, not a warning — a warning does not prevent overspend on a runaway task.
- Record cost-ceiling terminations distinctly — a rising rate of them signals under-budgeted tasks or a loop-efficiency regression.

### 4. Reused Controls (reference only)

Apply — without re-documenting — the mechanisms from `ai-lens/architecture/cost.md`: rate limiting (cap tasks/window), caching (reuse identical sub-results across steps/tasks), cheaper-model fallback (route routine steps to a smaller model), and the usage dashboard/alerting (now surfaced **per task and per step**, not only per request).

---

## ADR Triggers

- The per-task step budget and its worst-case cost translation
- Adding cost-ceiling termination to the loop
- A task whose worst-case cost is prohibitive at expected volume (risk escalation)

---

## Handoff to Layer 3

AI-DWG provisions the **cost-ceiling hook** into the loop runner (alongside the step/wall-clock limits from `reasoning-loop.md`) and extends the usage dashboard from `ai-lens/architecture/cost.md` with per-task/per-step granularity.

`AIQ__`/`ATQ__` (AI-TGE) assert the loop terminates within its step **and cost** budget; `AIG__` (AI-GCE) verifies the cost ceiling is enforced, not advisory.

---

## Anti-Patterns

- **Per-request budgeting for an agent** — ignores the step multiplier; the real cost is per task.
- **A cost warning with no hard ceiling** — a runaway task overspends before anyone reacts.
- **Estimating at expected steps only** — the worst case (step cap) is the number that protects the budget.
- **Ignoring context growth** — assuming flat per-step cost underestimates long tasks.
- **No per-task cost visibility** — request-level dashboards hide the amplified agentic cost.

---

*Agentic Architecture Sub-Module — Agent Cost (light) | v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens) | References `ai-lens/architecture/cost.md`*
