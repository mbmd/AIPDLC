# Automation Architecture — Loop Guards

> **Sub-module of** `automation-lens/facet.md`. Loaded on demand when designing loop prevention.
> **Sub-role:** `#persona-subrole-resilience-engineer`

---

## The failure mode

```
Automation A triggers on event X
  → A does its work
    → A's work emits event X (or an event that leads to X)
      → A triggers again
        → … forever
```

This is the signature automation failure. It is **not rare** — it is the default outcome when an automation both listens for and (directly or transitively) causes the same event. In a system with multiple automations and AI features, the cycle is often **transitive across features** and invisible in any single feature's design.

**Consequences:** runaway cost, database saturation, downstream system overload, audit-log explosion, and — worst — thousands of incorrect business actions before anyone notices.

---

## Detection is a design-time activity

Cycle detection happens in **Layer 2** (design), at the ADLC→DWG Coherence Gate, on the trigger→effect graph built from all features' `requires.events` and `provides.emits` — **across all active lenses**.

See `automation-lens/facet.md` §5–§7 for the graph construction and gate. This file covers the **guards** you design once a cycle is possible (and you design them defensively even when no cycle is detected, because runtime data can create paths static analysis cannot see).

---

## Guard 1: `causedBy` Provenance Stamp

**The mechanism:**

Every event emitted by an automation carries a provenance field identifying which automation caused it:

```yaml
event: ticket.assigned
causedBy: AUTO-001
correlationId: {trace-id}
```

Every automation's trigger filter **drops events it caused itself**:

```
On event X:
  IF event.causedBy == thisAutomationFeatureId → DROP (self-caused)
  ELSE → process
```

**Design requirements:**
- `causedBy` extends the existing `derivedFrom` provenance convention (design-time lineage) into **runtime causality**.
- The field must survive the full event path — if a message broker strips custom headers, use the payload.
- For multi-hop chains, `causedBy` should carry the **originating** automation, or a chain (see Guard 2).
- Human-initiated actions carry no `causedBy` (or `causedBy: user`) — automations should process those normally.

**Limitation:** `causedBy` filtering stops *direct* self-loops (A → A). It does not stop *transitive* loops (A → B → A). For those you need Guard 2.

---

## Guard 2: Causal Hop Budget (TTL)

**The mechanism:**

Every event carries a hop counter. Each automation that processes an event and emits a new one increments it. When the budget is exhausted, the chain stops.

```yaml
event: ticket.assigned
causedBy: AUTO-001
causalHops: 3
maxHops: 5
```

```
On event X:
  IF event.causalHops >= maxHops → DROP + ALERT (chain too long — probable loop)
  ELSE → process; emit with causalHops = event.causalHops + 1
```

**Design requirements:**
- **Choose an explicit budget.** A number, decided deliberately. Start at 5 for typical business automation — legitimate chains are rarely longer than 3.
- **Exhaustion is an alert, not a silent drop.** Hitting the budget means either a loop or a legitimately long chain you didn't model. Both need attention.
- **Propagate through every hop**, including AI features (this is why the guard must be lens-agnostic).
- A human action **resets** the counter to 0 (new causal chain).

**This is the guard that catches transitive and cross-lens loops** — the ones design-time detection is most likely to miss.

---

## Guard 3: Circuit Breaker (rate-based)

**The mechanism:**

Track execution rate per automation. If it exceeds a sane ceiling, open the circuit and stop executing.

```
IF executions_per_minute(AUTO-001) > threshold → OPEN circuit + ALERT
```

**Design requirements:**
- **Set the threshold from the expected volume**, with headroom: if peak is 200/hour, a ceiling of 2000/hour catches a loop without false-positiving on a busy day.
- **Opening must alert immediately** — this is an incident signal.
- Define the **reset policy** — manual only (safest for loop scenarios) or automatic after a cool-down.
- This is the **backstop** that limits blast radius when Guards 1 and 2 both fail (e.g. a path that bypasses event provenance entirely).

Distinct from the dependency circuit breaker in `reliability.md` — that one protects a struggling *dependency*; this one protects the *system from the automation*.

---

## Guard 4: Kill Switch

**The mechanism:**

A configuration flag the running automation checks before each execution. When set, the automation stops immediately.

```
On trigger:
  IF killSwitch(AUTO-001) == ON → EXIT (do nothing, log the skip)
  ELSE → process
```

**Design requirements:**
- **Must be architecturally real** — a value the running process reads, not just a UI toggle that updates a table nothing checks.
- **Must take effect fast** — define the maximum latency between flip and stop (target: next execution; for continuous automations, within seconds via a config-watch or short cache TTL).
- **Define in-flight behavior** — does current work complete, abort, or compensate? Document it; the UXP's stop control must present this accurately.
- **Mandatory for Unattended mode.** Mandatory with a documented SLA for `controlled` and `safety-critical` control classes.
- **Reachable without a deploy.** If stopping a runaway automation requires a code release, the kill switch does not exist.

---

## Guard Selection by Risk

| Situation | Required guards |
|-----------|----------------|
| Scheduled automation, no events emitted | Kill switch |
| Event-triggered, emits nothing | Kill switch |
| Event-triggered, emits events, no cycle detected | `causedBy` + hop budget + kill switch |
| Event-triggered, emits events, **cycle detected at the gate** | All four + redesign to break the cycle (guards contain; they don't fix the design) |
| Unattended + high volume | All four (`combined`) |
| `controlled` / `safety-critical` class | All four + documented kill-switch SLA + dual-control on activation |
| Cross-lens edge (AI feature emits → automation triggers) | All four; the hop budget is the critical one |

---

## Cycle detected at the gate — what to do

Guards contain a loop; they do not make a cyclic design correct. When the Coherence Gate flags a cycle:

1. **Break the cycle in the design** (preferred). Options:
   - Emit a *different* event than the one you trigger on (`ticket.assigned` not `ticket.updated`)
   - Narrow the trigger filter (trigger only on specific field changes, not any update)
   - Merge the two automations into one (the cycle often means they are one process artificially split)
   - Remove the redundant emit
2. **If the cycle is genuinely intentional** (rare — e.g. an iterative refinement loop with a natural termination condition):
   - Document why
   - Define the **explicit termination condition**
   - Set the hop budget to a value that permits the legitimate iterations plus one
   - Require `ATQ__` to test that it terminates
3. **Record the resolution in an ADR.**

---

## Handoff to Layer 3

These guards become **guardrails pushed down** by AI-DWG into the Layer-3 workspace:

| Guard | What Layer 3 receives |
|-------|----------------------|
| `causedBy` | The stamping convention + the filter rule |
| Hop budget | The `maxHops` value + exhaustion behavior |
| Circuit breaker | The rate threshold + reset policy |
| Kill switch | The mechanism + config location + in-flight policy |

- **`ATG__`** (AI-GCE) verifies the implementation **kept** the guards.
- **`ATQ__`** (AI-TGE) runs the **loop test**: fire the trigger, assert the causal chain terminates within the hop budget.

---

## Anti-patterns

- **Assuming "it won't loop"** — no cycle in the current design means no cycle *today*; one new automation next quarter creates one.
- **Triggering on a broad event** (`entity.updated`) while emitting a change to that entity — the classic self-loop.
- **Guarding with `causedBy` alone** — stops direct loops, misses transitive ones.
- **Kill switch that requires a deploy** — not a kill switch.
- **Silent hop-budget drop** — you never learn the loop exists.
- **Per-lens guards** — an AI feature emitting into an automation trigger bypasses automation-only provenance. Guards must be lens-agnostic.
- **Cycle "fixed" by lowering the hop budget** — that caps the damage; it does not fix the design.

---

*Automation Architecture Sub-Module — Loop Guards | v1.0.0*
