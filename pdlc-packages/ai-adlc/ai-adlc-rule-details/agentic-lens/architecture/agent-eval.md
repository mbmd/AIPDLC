# Agentic Architecture — Agent Evaluation

> **Sub-module of** `agentic-lens/facet.md` (light delta). Loaded on demand when designing how an agent's quality is evaluated.
> **Sub-role:** `#persona-subrole-ai-engineer`
> **Reuses from (do not re-document):** the eval harness, golden sets, offline/online metrics, and quality gates from `ai-lens/architecture/mlops.md`. This file is a **thin delta** — it extends that harness from single-shot output eval to multi-step agent eval.

---

## What is new here

`ai-lens/architecture/mlops.md` evaluates a **single model response** against a golden set — the right unit for a copilot. An agent produces a **trajectory**: a sequence of reasoning steps and tool calls ending (or not) in a completed task. A correct final answer reached via a wrong or unsafe path is still a defect. So agent eval adds three units of measurement on top of the existing harness — it does **not** build a second harness.

---

## Decision Framework

### 1. Trajectory Evaluation

Evaluate the **path**, not only the endpoint.

| Signal | What it checks |
|--------|----------------|
| **Step validity** | Each step's tool call was appropriate for the state |
| **Path efficiency** | The agent reached the goal without excessive/looping steps (ties to the step budget in `reasoning-loop.md`) |
| **Safety of path** | No unsafe intermediate action, even if the final result was correct |
| **Termination** | The task ended via success or a clean exhaustion/escalation — never by hitting an unguarded limit |

### 2. Task-Completion Evaluation

The endpoint signal, defined by POLC's **task-completion acceptance criterion** (the agentic acceptance criteria authored at AI-POLC).

- **Completion rate** — fraction of tasks that reach the defined "done" state.
- **Escalation rate** — fraction that correctly hand off when they cannot complete (a *good* outcome, not a failure).
- **False-completion** — the agent declared done but the task was not actually complete (the most dangerous metric; weight it heavily).

### 3. Tool-Call Accuracy

- **Right tool** — the agent selected the correct tool for the step.
- **Right arguments** — arguments were valid against the tool schema (`tool-use.md` §2).
- **Output handling** — the agent validated tool output before acting (`tool-use.md` §6).

### 4. Agent Regression Set

Extend the golden set from `ai-lens/architecture/mlops.md` with **agent scenarios** — task inputs with expected trajectories/outcomes — including adversarial and looping inputs. Run on every material change to the prompt, model, tool set, or loop pattern; a change that improves single-shot output can still regress the trajectory.

---

## ADR Triggers

- The trajectory-eval approach and its metrics
- The task-completion metric definition (bound to POLC's task-completion criterion)
- The agent regression set and its trigger cadence

---

## Handoff to Layer 3

This domain is **executed by the existing quality agents** — no new agent, no new trigger:

- **`AIQ__`** (AI-TGE) runs trajectory eval, task-completion eval, and tool-call accuracy.
- **`ATQ__`** (AI-TGE) runs the reasoning-loop termination test (`reasoning-loop.md`).

The agentic facet supplies the metric definitions; the harness itself is the one from `ai-lens/architecture/mlops.md`, extended.

---

## Anti-Patterns

- **Single-shot eval for a multi-step agent** — passes the endpoint, misses an unsafe or wasteful path.
- **Ignoring false-completion** — "declared done but wasn't" is the costliest agent defect.
- **Treating escalation as failure** — a correct hand-off is a designed success; measure it as one.
- **Building a separate eval stack** — extend the mlops harness; don't fork it.
- **No adversarial/looping scenarios in the regression set** — the termination and safety paths go untested.

---

*Agentic Architecture Sub-Module — Agent Evaluation (light) | v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens) | References `ai-lens/architecture/mlops.md`*
