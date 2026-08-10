# Agentic Architecture — Tool Use

> **Sub-module of** `agentic-lens/facet.md`. Loaded on demand when designing how an agent invokes tools/functions to act.
> **Sub-role:** `#persona-subrole-security-architect`
> **Reuses from (do not re-document):** identity, least-privilege, and SoD from `automation-lens/architecture/actor-identity.md`; output-validation and prompt-injection controls from `ai-lens/architecture/security.md`. This file designs only the **tool layer** that sits on top of them.

---

## What is new here

The two lenses already decided **who the agent is** (actor identity, least privilege) and **how model output is filtered** (AI security). What neither covers is the **tool surface**: the discrete set of actions the agent may call to affect the world, the schemas it calls them with, how it chooses among them, and — critically — the binding between *a tool* and *the permission to use it*.

Tool use is where an agent stops being a chatbot and starts being an actor. It is the single highest-risk agentic domain: an over-broad tool surface is the "excessive agency" failure mode.

---

## Decision Framework

### 1. Tool Registry

The explicit, closed set of tools the agent may call. Agents do not invent tools at runtime; the registry is designed and reviewed.

| Attribute (per tool) | What to define |
|----------------------|----------------|
| **Name** | Stable identifier the model references |
| **Effect class** | `read` (no state change) vs. `write` (mutates state) vs. `external-call` (leaves the system) |
| **Backing capability** | The concrete `provides.writes` or `requires.auth` this tool maps to (see the action-coverage sub-check in `agentic-lens/facet.md` §Step 3) |
| **Reversibility** | Reversible / compensable / irreversible — irreversible write tools demand the strictest gating |
| **Permitted autonomy** | May the agent call this unsupervised, or only with human approval? |

**Design rule:** every registered tool maps to a declared effect or external call. A tool with no backing declaration is a ghost capability and fails the Coherence Gate.

### 2. Tool Schemas

Each tool is described to the model with a strict input/output contract (JSON schema / function signature).

- **Typed, bounded parameters** — enums over free strings wherever the domain is closed; explicit ranges on numerics.
- **No free-form "command" parameters** — a tool that takes an arbitrary string to execute is a remote-code-execution surface, not a tool.
- **Explicit required vs. optional** — the model should not be able to omit a safety-relevant field.
- **Output schema declared** — so tool output can be validated before the agent consumes it (§6).

### 3. Tool-Selection Strategy

How the agent decides which tool to call at each step.

| Strategy | When | Notes |
|----------|------|-------|
| **Model-driven (function calling)** | The model chooses from the registry per step | Default; the registry bounds the choice |
| **Constrained / policy-gated** | Some tools are only offered when preconditions hold | Offer high-risk tools only in the relevant state (e.g. refund tool only after eligibility verified) |
| **Deterministic router** | A rule, not the model, selects the tool | Use when selection must be auditable/predictable |

**Design rule:** narrow the tool set presented at each step to what the current state permits. Presenting every tool at every step maximizes both error rate and blast radius.

### 4. Permission Binding (the core control)

Bind each tool to the agent's actor identity from `automation-lens/architecture/actor-identity.md`. The agent may call a tool **only if** its identity holds the permission the tool requires.

- Derive tool permissions mechanically from the tool's backing `provides.writes` / `requires.auth` — same least-privilege derivation as the parent identity sub-module.
- **No tool grants more than its backing capability.** A `read` tool cannot carry write permission "for convenience."
- Enforce the binding at the **permission layer**, not in the prompt. A prompt instruction ("don't use the delete tool") is not a control; a missing permission is.
- For `unattended` agents, the **tool set as a whole** must satisfy SoD (it must not both initiate and approve the same effect) — see `agentic-lens/facet.md` §Step 3.2.

### 5. Sandboxing & Blast-Radius Containment

| Concern | Requirement |
|---------|-------------|
| **Execution isolation** | Tools that run code/queries execute in a sandbox with no ambient credentials |
| **Rate / quota per tool** | Cap invocations per task and per window — a tool-call storm is contained here |
| **Irreversible-action gate** | Irreversible write tools require an explicit precondition check and (for `attended`) human approval |
| **Timeout per tool call** | Every tool call is bounded; a hung tool must not hang the loop |

### 6. Output Validation Before Acting

The agent must validate a tool's output **before** it acts on it — this is where the tool layer binds to `ai-lens/architecture/security.md`.

- Validate tool output against the declared output schema; reject/handle malformed output rather than feeding it back into the loop unchecked.
- Treat tool output (especially from `external-call` tools) as **untrusted input** — a tool that returns model-consumable text is a prompt-injection vector. Sanitize before it re-enters the context.
- On validation failure: do not act; record the failure in the reasoning trace and route to the loop's exhaustion/escalation path (`reasoning-loop.md`).

---

## ADR Triggers

- Tool registry composition (which tools exist, their effect classes)
- Any irreversible or `external-call` write tool added to the registry
- The permission-binding model (tool → identity permission)
- Sandboxing / isolation approach for code- or query-executing tools
- Tool-output validation strategy (schema + untrusted-input handling)

---

## Handoff to Layer 3

AI-DWG provisions from these decisions:
- The **tool registry manifest** (names, effect classes, schemas) as generated slots — never live credentials.
- The **tool-permission binding** (which identity permission each tool requires) for review.
- The **sandbox / rate-limit** configuration.

`AIG__` (AI-GCE) verifies tool-permission least-privilege and excessive-agency in the implementation; `ATG__` verifies SoD on the tool set for unattended agents. `AIQ__` (AI-TGE) tests tool-call accuracy.

---

## Anti-Patterns

- **A single "execute" tool** taking an arbitrary command/string — that is not a tool, it is arbitrary code execution.
- **Presenting the full registry at every step** — maximizes wrong-tool selection and blast radius.
- **Permission granted in the prompt, not the permission layer** — the model can be talked out of a prompt rule; it cannot grant itself a missing permission.
- **A tool that outlives its backing capability** — a ghost tool the design never declared.
- **Acting on tool output without validation** — the fastest path to acting on injected or malformed data.
- **One over-privileged identity behind all tools** — the excessive-agency failure; scope tools to least privilege and split for SoD.
- **Irreversible write tools with no precondition gate** — one bad step becomes unrecoverable.

---

*Agentic Architecture Sub-Module — Tool Use | v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens)*
