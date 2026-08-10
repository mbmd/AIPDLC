# AGENTIC Facet — AI-ADLC

> **Loaded by the lens seam as an INTERSECTION FACET** when `Lens_Status.md` shows **AI-LENS row = `AI-Powered`** AND **Automation row = `Automated`** — for each feature carrying `agenticProfile: true`.
> **Runs after** the AI-LENS facet (`ai-lens/facet.md`) and the Automation-LENS facet (`automation-lens/facet.md`) have designed their own domains. Agentic is **additive** — it never re-opens or overrides their decisions.
> **Integration points:** `design/component-design.md` + `design/integration-infrastructure.md` + `decisions/` (ADRs) + the Design Coherence Gate (ADLC→DWG boundary).
> **Persona:** CTO / Chief Architect (primary; sub-roles layered per domain — see the sub-module table).
> **Sub-module:** `agentic-lens/architecture/` — deep rules loaded on demand per domain.

---

## Purpose

Design the **connective tissue** that turns a feature already tagged by **both** lenses — it *reasons with a model* (AI Lens) **and** *acts across multiple steps without a human performing each one* (Automation Lens) — into a **safe autonomous agent**.

An agent is the top-right quadrant of intelligence × autonomy: it is **not a new kind of thing to architect from scratch**. Roughly two-thirds of an agent's architecture is already designed by the two lens facets (model serving, RAG, guardrails, cost, identity, loop guards, audit). This facet designs **only what neither lens covers alone**: how the agent uses tools, how its reasoning loop runs and terminates, and how it remembers — plus thin deltas for evaluating and costing a multi-step agent.

---

## Guardrail

This facet operates strictly within the CTO / Architect's lane, and strictly as a **delta over the two lenses**:
- Design **only** the agentic connective tissue in the Reuse Map's right-hand column.
- **DO NOT re-document** anything in the "Reused from" column — reference the named sub-module. The two lens facets own those domains and have already run.
- **DO NOT create a new mode, axis, or classification.** Agentic is derived from the two lens tags; there is no agentic mode switch and no agentic register.
- DO NOT identify or tag agentic features (AI-POLC's Agentic-Opportunity Scan did that).
- DO NOT design the agent's user-facing controls (AI-UXD owns interruptibility, working-state, and transparency UX).
- DO NOT provision the agent runtime (AI-DWG consumes these decisions).

---

## When This Facet Fires

For each feature carrying `agenticProfile: true` (both lens tags present at threshold — `aiSubMode ∈ {augmented, native}` AND `automationMode ∈ {attended, unattended}`), during the Design phase, **after** the two lens facets have completed their passes:

1. **Component design** — the agent's reasoning loop + tool-use component.
2. **Integration/infrastructure** — tool registry, memory store, loop runner.
3. **Decisions** — one ADR per material agentic decision.
4. **Design Coherence Gate** — the agentic action-surface sub-check (§Step 3).

---

## The Reuse Map (inherit — do not re-document)

An agent inherits most of its architecture from the two lens facets. Design each row below by running the **referenced** sub-module (already done by the two lens passes). This facet owns **only the right-hand column**.

| Agent architecture need | Reused from (already designed — reference, do not repeat) | New connective tissue (this facet owns) |
|---|---|---|
| Model source, serving, fallback | `ai-lens/architecture/model-serving.md` | — |
| Grounding retrieval (RAG, vector) | `ai-lens/architecture/data-rag.md` | agent **memory** is *distinct* — see `architecture/memory.md` |
| Guardrails, prompt-injection, output filtering | `ai-lens/architecture/responsible-ai.md` + `ai-lens/architecture/security.md` | **tool-output validation before acting** — see `architecture/tool-use.md` |
| Prompt/model versioning, eval harness | `ai-lens/architecture/mlops.md` | **trajectory / task-completion** eval — see `architecture/agent-eval.md` |
| Token/inference budgets | `ai-lens/architecture/cost.md` | **loop-amplified** cost + per-task **step budget** — see `architecture/agent-cost.md` |
| Agent identity, least-privilege, SoD (excessive-agency control) | `automation-lens/architecture/actor-identity.md` | **tool-permission binding** (which tools this identity may call) — see `architecture/tool-use.md` |
| Runaway protection: `causedBy`, hop-budget/TTL, circuit-breaker, kill-switch | `automation-lens/architecture/loop-guards.md` | reasoning-loop **step-cap + termination** (the deliberate internal loop, vs the accidental event cycle) — see `architecture/reasoning-loop.md` |
| Durable multi-step execution, idempotency, retry, compensation, state machine | `automation-lens/architecture/reliability.md` + `automation-lens/architecture/orchestration.md` | **multi-agent handoff** (agent-to-agent) — *deferred to v1.1* |
| Immutable audit of every action taken | `automation-lens/architecture/audit-observability.md` | **reasoning-trace capture** (the "why" behind each action) — see `architecture/reasoning-loop.md` |

> If a row's left column has not been designed, the feature is not ready for agentic architecture — return to the owning lens facet first. A missing reused domain is a coherence gap, not something this facet fills.

---

## New Architecture Domains (v1)

Each domain has deep rules in `agentic-lens/architecture/`. The facet orchestrates; the sub-module provides the detailed design guidance.

| # | Domain | Sub-module file | Weight | Sub-role to layer | Produces |
|---|--------|-----------------|:------:|-------------------|----------|
| 1 | Tool Use | `architecture/tool-use.md` | core | `#persona-subrole-security-architect` | Tool registry, tool schemas, selection strategy, permission binding, sandboxing, output validation |
| 2 | Reasoning Loop | `architecture/reasoning-loop.md` | core | `#persona-subrole-ai-engineer` | Loop pattern, termination (steps/time/cost), exhaustion behavior, reasoning-trace capture |
| 3 | Memory | `architecture/memory.md` | core | `#persona-subrole-data-architect` | Scratchpad, episodic + semantic stores, read/write policy, context-window management, retention/PII |
| 4 | Agent Evaluation | `architecture/agent-eval.md` | light | `#persona-subrole-ai-engineer` | Trajectory eval, task-completion eval, tool-call accuracy (references `ai-lens/architecture/mlops.md`) |
| 5 | Agent Cost | `architecture/agent-cost.md` | light | `#persona-subrole-ai-engineer` | Loop-amplified cost model, per-task step budget, cost-ceiling termination (references `ai-lens/architecture/cost.md`) |
| — | Multi-Agent | *(deferred to v1.1)* | — | — | Agent roles, orchestrator/worker, handoff protocols — activated only when the architecture has multiple cooperating agents |

---

## Step 1: Per-Agent Architecture Pass

For each agentic feature (threaded by its existing `aiFeatureId` + `automationFeatureId` — there is no `agenticFeatureId`), confirm the reused domains are designed, then run the new domains:

### 1.1 Confirm the reused foundation
Verify the two lens facets have produced, for this feature: model & serving, grounding data, guardrails + security, identity + least-privilege, loop guards, reliability, and audit. If any is missing, stop — resolve in the owning lens facet.

### 1.2 Tool Use
`Read` → `agentic-lens/architecture/tool-use.md`. Design the tool registry, per-tool JSON schema, selection strategy, **permission binding** to the actor identity from `automation-lens/architecture/actor-identity.md`, sandboxing, and output-validation-before-act (binds to `ai-lens/architecture/security.md`). **ADR** per material tool-permission decision.

### 1.3 Reasoning Loop
`Read` → `agentic-lens/architecture/reasoning-loop.md`. Select the loop pattern (ReAct / plan-execute / reflection); define **termination** (max steps, wall-clock, cost budget) and exhaustion behavior (stop + escalate); design reasoning-trace capture into the audit sink from `automation-lens/architecture/audit-observability.md`. **ADR** for the loop pattern + termination policy.

### 1.4 Memory
`Read` → `agentic-lens/architecture/memory.md`. Design the scratchpad + long-term stores, read/write policy, context-window management, and retention/PII (binds to `ai-lens/architecture/security.md` PII boundary). Keep distinct from RAG grounding. **ADR** for the memory architecture + retention.

### 1.5 Agent Evaluation (light)
`Read` → `agentic-lens/architecture/agent-eval.md`. Define trajectory + task-completion + tool-call eval as an extension of the eval harness in `ai-lens/architecture/mlops.md`. Layer-3 execution is delivered by the existing `AIQ__`/`ATQ__` quality agents (extended, not new).

### 1.6 Agent Cost (light)
`Read` → `agentic-lens/architecture/agent-cost.md`. Extend the budgets in `ai-lens/architecture/cost.md` with a loop-amplified model + per-task step budget + cost-ceiling termination (ties to §1.3).

---

## Step 2: Produce ADRs

For each material agentic decision, produce an ADR (same mechanism as the two lens facets), tagged with the feature's existing ids:

```yaml
---
agenticProfile: true
aiFeatureId: AIF-{NNN}
automationFeatureId: AUTO-{NNN}
domain: {tool-use | reasoning-loop | memory | agent-eval | agent-cost}
---
```

ADR triggers: tool registry + permission model, sandboxing approach, loop pattern, loop termination policy, memory architecture, memory retention/PII, step/cost ceiling.

---

## Step 3: Agentic Action-Surface Sub-Check (at the Design Coherence Gate)

At the **ADLC→DWG boundary**, the Automation-LENS facet already builds the trigger→effect graph and runs the three coherence checks (vertical / readiness / horizontal). For each agentic feature, add this **intra-feature action-surface sub-check** and record it as an agentic sub-section of the Coherence Report:

### 3.1 Action-coverage (readiness)
Every tool the agent can call MUST map to a declared `provides.writes` (an effect) or `requires.auth` (an external call). A tool with no matching declaration is a **ghost capability** — the agent can act in a way the design never accounted for. Red until reconciled: either declare the effect/call, or remove the tool from the registry.

### 3.2 Unattended-agent tool-set SoD (horizontal)
For an `unattended` agent, the tool-permission set MUST satisfy **segregation of duties** — the agent's tools must not allow it to both **initiate** and **approve** the same effect. This reuses the SoD rule from `automation-lens/architecture/actor-identity.md`, applied to the **tool set** rather than a single identity action. If the set violates SoD, split the tools across identities, insert a human-approval gate, or downgrade the autonomy to `attended`.

Record in the Coherence Report:

```markdown
### Agentic action-surface (per agentic feature)
| Feature | Tools declared | Ghost capabilities | Unattended SoD | Verdict |
|---------|:--------------:|:------------------:|:--------------:|:-------:|
| AIF-00N / AUTO-00N | {n} | none | ✅ | 🟢 |
```

Same gate rule as the parent facet: Red blocks generation; Amber needs explicit acknowledgment; Green proceeds.

---

## Step 4: Record & Inform Downstream

Record per agentic feature in the AP (derived marker + the new-domain decisions; no new id):

```yaml
---
agenticProfile: true                 # derived; dissolves if either lens tag drops below threshold
aiFeatureId: AIF-{NNN}
automationFeatureId: AUTO-{NNN}
agentToolRegistry: {ref}
reasoningLoopPattern: {react | plan-execute | reflection}
loopTermination: { maxSteps: {n}, wallClock: {t}, costCeiling: {c} }
memoryArchitecture: {scratchpad + episodic | + semantic}
---
```

Plus the ADRs. Inform: "Agentic facet: {N} agents architected; {M} ADRs; action-surface sub-check = {verdict}."

**Downstream:** AI-DWG provisions the agent framework (tool registry, memory store, loop runner) and couriers the agentic guardrails (step cap, cost ceiling, tool-permission manifest, reasoning-trace requirement) into Layer 3. `AIG__`/`ATG__` (AI-GCE) later verify tool-permission least-privilege, excessive-agency, kill-switch, and reasoning-trace presence; `AIQ__`/`ATQ__` (AI-TGE) run trajectory eval + the loop-termination test.

---

## Autonomy Calibration

| `automationMode` | Agentic architecture depth |
|------------------|----------------------------|
| `attended` | Lighter oversight: a human approves the agent's plan or its consequential actions. Termination + tool permissions still mandatory; SoD on the tool set is recommended. |
| `unattended` | Full guardrails: strict step/cost termination, least-privilege tool binding, **SoD on the tool set is mandatory**, kill-switch (from `automation-lens/architecture/loop-guards.md`) reachable, reasoning-trace captured for every action. |

---

## What This Facet Does NOT Do

- Does not re-document the two lenses' architecture domains (references them via the Reuse Map).
- Does not identify or tag agentic features (AI-POLC).
- Does not design the agent's user-facing controls (AI-UXD).
- Does not provision the agent runtime (AI-DWG).
- Does not enforce rules at runtime (AI-GCE `AIG__`/`ATG__`).
- Does not execute trajectory or termination tests (AI-TGE `AIQ__`/`ATQ__`).
- Does not create a new mode, axis, id, or register — the agentic profile is derived from the two lens tags.

---

*AGENTIC Facet — AI-ADLC v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens) — NOT a third lens | Integration: Design (component + integration + decisions) + Coherence Gate | Sub-module: `agentic-lens/architecture/` | Author: Maheri*
