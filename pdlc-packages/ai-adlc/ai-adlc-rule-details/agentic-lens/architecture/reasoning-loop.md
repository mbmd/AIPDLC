# Agentic Architecture — Reasoning Loop

> **Sub-module of** `agentic-lens/facet.md`. Loaded on demand when designing the agent's deliberate reason-then-act loop.
> **Sub-role:** `#persona-subrole-ai-engineer` (termination/runaway concerns reuse the resilience-authored guards below)
> **Reuses from (do not re-document):** runaway protection (`causedBy`, hop-budget/TTL, circuit-breaker, kill-switch) from `automation-lens/architecture/loop-guards.md`; the audit sink from `automation-lens/architecture/audit-observability.md`. This file designs the **deliberate internal loop**, which is a different thing from the accidental event cycle those guards address.

---

## Two different loops — do not conflate them

| | Accidental event cycle (loop guards) | Deliberate reasoning loop (this file) |
|---|---|---|
| **Nature** | A design defect: feature A's effect re-triggers A | An intended mechanism: the agent iterates reason → act → observe until done |
| **Where** | Across features, in the trigger→effect graph | Inside one agent, per task |
| **Owned by** | `automation-lens/architecture/loop-guards.md` | this sub-module |
| **Risk** | Runaway re-triggering across the system | Non-termination / unbounded iteration within one task |

The runaway *guards* from `loop-guards.md` still apply to the agent as a system actor. This file adds the control the deliberate loop needs and the event-cycle guards do not: **an explicit termination contract per task.**

---

## Decision Framework

### 1. Loop Pattern Selection

| Pattern | How it works | Best for |
|---------|-------------|----------|
| **ReAct** (reason + act) | Interleave a reasoning step and a tool call each iteration; observe, repeat | General tool-using agents; most tasks |
| **Plan-execute** | Produce a full plan up front, then execute steps (optionally re-planning on failure) | Tasks with a knowable multi-step structure; auditable plans |
| **Reflection** | After acting, the agent critiques its own output and may retry/refine | Quality-sensitive generation where a self-check materially helps |

**Design rule:** pick the simplest pattern that fits. Reflection adds iterations (and cost); use it only where the self-critique demonstrably improves the outcome. Patterns can compose (plan-execute with per-step ReAct), but each composition multiplies the step budget — account for it in `agent-cost.md`.

### 2. Termination Contract (mandatory)

Every agent task MUST have an explicit, enforced termination contract. This is the defining safety control of the reasoning loop.

| Limit | Definition | Design note |
|-------|-----------|-------------|
| **Max steps / iterations** | Hard cap on loop passes for one task | The primary limit; derive from the task-completion definition + a safety margin, not guesswork |
| **Wall-clock** | Max elapsed time for one task | Backstop for slow tools / long model calls |
| **Cost budget** | Max spend (tokens/step-cost) per task | Ties to `agent-cost.md` cost-ceiling termination |
| **Success condition** | The positive stop: the task-completion signal is met | The intended exit; from POLC's task-completion acceptance criterion |
| **No-progress detector** | Stop if N consecutive steps make no measurable progress (repeating the same tool call, looping on the same state) | Catches "spinning" before the step cap does |

**Design requirements:**
- **At least one hard limit (steps) is non-negotiable** — an agent loop with no step cap is the agentic equivalent of an infinite loop.
- Termination limits are enforced by the **loop runner**, not by asking the model to stop.
- The limits are **explicit numbers in the design**, recorded in the ADR — not "a reasonable number."

### 3. Exhaustion Behavior (what happens at the limit)

Reaching a limit without success is a **normal, designed outcome** — not a crash.

- **Stop cleanly** — do not leave partial state uncommitted; apply the reliability sub-module's idempotency/compensation for any partial actions.
- **Escalate** — hand off to the escalation path from POLC's agentic acceptance criteria (a human queue, a fallback non-agentic path, or a safe default).
- **Record why** — capture which limit was hit (steps / time / cost / no-progress) in the reasoning trace.
- **Never silently retry the whole task** — a fresh attempt without new information repeats the same exhaustion at double the cost.

### 4. Reasoning-Trace Capture

The agent must record **why** it took each action — the agentic addition to the immutable audit trail from `automation-lens/architecture/audit-observability.md`.

- Per step, capture: the step index, the reasoning/decision, the tool called + arguments, the observed result, and the running cost/step count.
- Write traces to the **audit sink designed by the automation facet** — do not invent a second store.
- Redact per the PII boundary (`memory.md` / `ai-lens/architecture/security.md`) — a reasoning trace can capture sensitive content.
- The trace is what `AIG__` inspects for excessive-agency review and what `ATQ__` reads to assert termination.

### 5. Human Checkpoints (attended agents)

For `attended` agents, define **where** in the loop a human intervenes:

| Checkpoint | When to use |
|------------|-------------|
| **Plan approval** | Human approves the plan before any action (plan-execute) |
| **Pre-action gate** | Human approves each consequential/irreversible action |
| **Post-hoc review** | Agent acts, human reviews a batch afterward (lighter oversight) |

The checkpoint UX (working state, interruptibility) is AI-UXD's lane — this file only fixes *where* the architectural gate sits.

---

## ADR Triggers

- Loop pattern selection (and any composition)
- The termination contract (the specific step / wall-clock / cost numbers)
- Exhaustion + escalation behavior
- Reasoning-trace schema and its binding to the audit sink
- Human-checkpoint placement for attended agents

---

## Handoff to Layer 3

AI-DWG provisions the **loop runner** with the termination contract baked in (step cap, wall-clock, cost ceiling), the reasoning-trace writer bound to the audit sink, and the kill-switch hook from `automation-lens/architecture/loop-guards.md`.

`ATQ__` (AI-TGE) runs the **termination test**: start a task and assert the loop terminates within its step/cost budget (including a deliberately hard/looping input). `AIG__` (AI-GCE) verifies the reasoning trace is present and the kill-switch is reachable.

---

## Anti-Patterns

- **No step cap** — an agent loop with no hard iteration limit is an infinite loop waiting for a bad input.
- **"Stop when done" as the only limit** — if "done" is never reached, nothing stops it; always pair with a hard cap.
- **Termination requested in the prompt** — the model can ignore it; enforce in the runner.
- **Silent whole-task retry on exhaustion** — repeats the failure at multiplied cost.
- **Reasoning trace in a separate ad-hoc log** — fragments the audit trail; use the automation facet's audit sink.
- **Reflection everywhere** — adds iterations and cost without always improving the outcome.
- **Treating the deliberate loop with only the event-cycle guards** — hop-budget/`causedBy` do not bound an internal per-task loop; it needs its own step contract.

---

*Agentic Architecture Sub-Module — Reasoning Loop | v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens)*
