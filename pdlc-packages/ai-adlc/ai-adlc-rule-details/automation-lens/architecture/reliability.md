# Automation Architecture — Reliability

> **Sub-module of** `automation-lens/facet.md`. Loaded on demand when designing idempotency, retry, and compensation.
> **Sub-role:** `#persona-subrole-resilience-engineer`

---

## The core premise

An automation will be re-triggered. Accept it as certain, not possible. Causes: retry after timeout, at-least-once delivery, duplicate events, manual re-run, replay after incident, scheduler overlap. **Design for repeat execution from the start.**

---

## 1. Idempotency

### The requirement

Executing the automation twice with the same input must produce the same end state as executing it once. Not "must not error" — must not *double-apply*.

### Choosing a strategy

| Strategy | Mechanism | Use when |
|----------|-----------|----------|
| **Natural key** | The domain has a unique identifier; check-then-act on it | The entity has a real unique key (ticket id, order number, invoice number) |
| **Idempotency-key header** | Caller supplies a key; you store and check it | API-triggered automation where the caller can generate a key |
| **Deduplication store** | Track processed message/event ids with a TTL | Event-driven where events carry ids but the domain has no natural key |
| **Exactly-once delivery** | Infrastructure guarantees it | Rare. Verify the guarantee's actual scope — most "exactly-once" is "at-least-once + dedup" |

### Design requirements

- **The check and the act must be atomic.** A check-then-act with a gap is a race. Use a database constraint, a conditional write, or a transaction — not a read followed by a write.
- **Define the idempotency window.** A dedup store needs a TTL. Choose it longer than your maximum retry window, and document why.
- **Idempotency is per-effect, not per-automation.** If the automation writes to a DB and calls an external API, both need idempotency. The external call is usually the hard one.
- **Non-idempotent external calls need a compensation plan** (see §3) or a proxy that adds idempotency.

### Verification

The design must state how idempotency will be tested: "fire the same event twice; assert exactly one assignment, one audit record, one outbound notification." `ATQ__` will run this.

---

## 2. Retry

### The retry budget

Define explicitly:

| Parameter | Decide |
|-----------|--------|
| **Max attempts** | A number (e.g. 5). Never unbounded. |
| **Backoff curve** | Fixed / linear / exponential. Exponential is the default; add jitter to avoid thundering herds. |
| **Base delay** | Starting interval (e.g. 1s) |
| **Max delay** | Cap so exponential doesn't reach hours (e.g. 5 min) |
| **Total time cap** | Wall-clock limit regardless of attempt count (e.g. 30 min) |
| **Terminal action** | What happens when the budget exhausts (see §4) |

### What is retryable

**Retry:** timeouts, 5xx, connection errors, rate limits (429 — honor Retry-After), transient lock contention.

**Do NOT retry:** 4xx validation errors, authorization failures, malformed input, business-rule rejections. These will fail identically forever — retrying wastes budget and delays the alert.

**Design requirement:** classify failures explicitly. A blanket `catch → retry` is a bug that turns a 5-second failure into a 30-minute one.

### Rate-limit interaction

If the automation calls a rate-limited API, retry must respect the limit or you amplify the problem. Honor `Retry-After`; consider a token-bucket client-side limiter.

---

## 3. Compensation (Saga)

Required when the automation performs **multiple state-mutating steps** that cannot be wrapped in a single transaction (typically across services or systems).

### The rule

For every step that mutates state, define its **compensating action** — the operation that semantically undoes it. Not a rollback (you cannot roll back a sent email); a *compensation* (send a correction, cancel the order, credit the charge).

### Orchestration vs. Choreography

| | Orchestrated | Choreographed |
|---|---|---|
| **Coordinator** | A central saga orchestrator drives each step and each compensation | Each service reacts to events and emits its own; no central brain |
| **Visibility** | High — one place shows the whole flow | Low — the flow is emergent across services |
| **Coupling** | Coordinator knows all participants | Participants know only events |
| **Failure reasoning** | Easier — the orchestrator knows what to compensate | Harder — must trace event chains |
| **Choose when** | The flow is complex, needs visibility, or has conditional branching | The flow is simple, linear, and services must stay decoupled |

**Default recommendation:** orchestrated, unless service decoupling is a hard requirement. The visibility is worth the coupling for most automation.

**ADR required** — this is a material architectural decision. Use `templates/adr-saga-pattern.md` (the dedicated saga ADR scaffold — it pre-frames these exact drivers, options, and the compensation/pivot design). This is the **same decision** the always-on **Stage 11 Cross-Service Consistency (Saga) loop** (`design/integration-infrastructure.md`) raises for multi-service operations: produce **one** ADR that satisfies both the lens and the core loop — do not double-record.

### Compensation design requirements

- **Compensations must be idempotent too** — compensation can be retried.
- **Compensations can fail.** Define what happens then (usually: alert a human, park in a "needs manual intervention" state — never silently ignore).
- **Some steps are not compensatable.** Identify them and order the saga so they happen **last** (the "pivot" step). After the pivot, only forward recovery is possible.
- **Document the compensation for each step** in the AP as a table: Step | Action | Compensation | Compensatable?

---

## 4. Terminal Failure Handling

When retries exhaust or a non-retryable error occurs:

| Approach | Behavior | Use when |
|----------|----------|----------|
| **Dead-letter queue** | Item moves to a DLQ for later inspection/reprocessing | Event/queue-driven; you want to reprocess after a fix |
| **Exception queue (business)** | Item lands in the human exception queue the UXP designed | The failure needs a business decision, not a technical fix |
| **Compensate + close** | Undo prior steps, mark the attempt failed, stop | Multi-step where partial completion is worse than none |
| **Alert + park** | Leave state as-is, alert a human, wait | Ambiguous failures where automated action could worsen things |

**Design requirements:**
- **Nothing disappears silently.** Every terminal failure produces (a) a durable record, (b) a signal a human will see.
- **The DLQ needs an owner and a process.** An unmonitored DLQ is a data-loss mechanism with extra steps.
- **DLQ reprocessing must be idempotent** — reprocessing is a retry.
- Connect to the UXP's exception model: technical failures → DLQ; business failures → exception queue.

---

## 5. Circuit Breaker

Required for automations calling external dependencies, and for any Unattended high-volume automation.

**Define:**
- **Failure threshold** — what opens the circuit (e.g. 50% failures over 20 requests, or 10 consecutive failures)
- **Open duration** — how long before trying again (half-open probe)
- **Fallback behavior when open** — queue for later? fail fast? use a cached/default response?
- **Who is alerted** when the circuit opens

**Why it matters for automation specifically:** an automation with retry and no circuit breaker will hammer a struggling dependency thousands of times per minute, turning a partial outage into a total one.

---

## 6. Reliability by Sub-Mode

| Sub-mode | Reliability bar |
|----------|----------------|
| **Assisted** | Light — a failed suggestion is a non-event; the human proceeds manually. Basic retry, no saga needed. |
| **Attended** | Medium — a failure must reach the human who triggered/supervises it. Retry + visible failure state. |
| **Unattended** | **Heavy — mandatory:** idempotency, bounded retry, defined terminal handling, circuit breaker, compensation for multi-step, and loop guards (see `loop-guards.md`). Nobody is watching; the architecture is the only safety net. |

---

## Anti-patterns

- **Unbounded retry** — turns a transient failure into an infinite loop and a cost incident.
- **Retry without idempotency** — creates duplicates. The most common automation defect.
- **Catch-all retry** — retrying validation errors wastes the budget and hides the real problem.
- **Silent swallow** — `catch { log.debug(e) }` in an unattended automation means failures are invisible.
- **Unmonitored DLQ** — items go in, nobody looks, work is lost.
- **Saga without compensation for every step** — a partial failure leaves inconsistent state permanently.
- **Retry with no circuit breaker** — amplifies dependency outages.

---

*Automation Architecture Sub-Module — Reliability | v1.0.0*
