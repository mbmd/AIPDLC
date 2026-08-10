# Automation-LENS Facet — AI-ADLC

> **Loaded by the lens seam** when `Lens_Status.md` Automation row = `Automated`.
> **Integration points:** `design/component-design.md`, `design/data-architecture.md`, `design/integration-infrastructure.md`, `decisions/` (ADRs).
> **Persona:** CTO / Chief Architect (primary; sub-roles layered per topic — see the sub-module table below).
> **Sub-module:** `automation-lens/architecture/` — deep rules loaded on demand per topic.

---

## Purpose

Design the **real automation architecture** for each `automationFeature`. This closes a confirmed gap: today an automated process identified anywhere in the chain has no architectural home — nowhere to decide the orchestration engine, idempotency strategy, retry/compensation approach, dead-letter handling, actor identity, or audit model.

This facet is also the **design-time coherence integration point** — the architect is the only lane that designs data, triggers, effects, and actors together, so it is the only vantage from which cross-feature interaction is visible. It owns the trigger→effect graph, cycle detection, and the Design Coherence Gate.

---

## Guardrail

This facet operates within the Architect's lane:
- Decide **how** the automation is orchestrated, made reliable, secured, and audited.
- Produce **ADRs** for every material decision.
- DO NOT change the business rules or acceptance criteria (AI-POLC owns those — satisfy them, don't rewrite them).
- DO NOT design the human interfaces (AI-UXD owns those — support the control model they specified).

---

## When This Facet Fires

For each `automationFeature`-tagged item:

1. **At component design:** orchestration engine + component decomposition for the automation.
2. **At data architecture:** state management, idempotency store, audit sink.
3. **At integration/infrastructure design:** event bus, queues, scheduler, connectors, actor identity.
4. **At decisions:** ADRs for every material choice.
5. **At the ADLC→DWG boundary:** build the trigger→effect graph, run cycle detection, produce the Coherence Report (see §7).

---

## Step 1: Read the Upstream Context

For each tagged feature, read:

| Source | What to extract |
|--------|-----------------|
| **PBP** (AI-POLC) | `automationMode`, `automationPattern`, `automationTrigger`, acceptance criteria (throughput/SLA, exception handling, fallback, straight-through rate, reversibility, audit), intent-level `requires`/`provides` |
| **UXP** (AI-UXD) | `automationConfigModel`, `automationMonitoringModel`, `automationApprovalModel`, `automationOverrideControl` — the architecture MUST support these |
| **PIP** (AI-PILC) | Process suitability findings, `automationControlClass` (drives governance depth), ROI targets (drives performance requirements) |

**Consistency check:** if the UXP specifies a `kill-switch` but the architecture has no circuit-breaker, that is a vertical coherence failure — resolve it now, not at the gate.

---

## Step 2: Load the Architecture Sub-Module (per topic)

The deep rules live in `automation-lens/architecture/`. Load the file for the topic you are designing:

| Sub-module file | Covers | Sub-role to layer |
|-----------------|--------|-------------------|
| `orchestration.md` | Engine choice, workflow vs. choreography, scheduler, state machine | `#persona-subrole-distributed-systems-engineer` |
| `reliability.md` | Idempotency, exactly-once, retry/backoff, compensation (saga), dead-letter, circuit breaker | `#persona-subrole-resilience-engineer` |
| `event-infrastructure.md` | Event bus, queues, topics, delivery guarantees, ordering, throughput/scaling | `#persona-subrole-event-driven-architect` |
| `actor-identity.md` | The automation's identity, least-privilege, credential management, delegation, SoD enforcement | `#persona-subrole-security-architect` |
| `audit-observability.md` | Audit trail design, log schema, retention, traceability, monitoring/alerting hooks | `#persona-subrole-audit-specialist` |
| `loop-guards.md` | `causedBy` provenance, hop-budget/TTL, self-trigger filtering, kill-switch architecture | `#persona-subrole-resilience-engineer` |

Load only what the current stage needs. Do not load all six at once.

---

## Step 3: Make the Core Decisions (per feature)

For each automation feature, decide and record:

### 3.1 Orchestration Strategy (`automationEngineStrategy`)

| Strategy | When |
|----------|------|
| `workflow-engine` | Multi-step, long-running, needs state persistence + visibility (Temporal, Camunda, Step Functions) |
| `scheduler` | Time-triggered, stateless, short-running (cron, scheduled job) |
| `event-consumer` | Reactive to events, stateless per event (queue/topic consumer) |
| `queue-worker` | Work-item processing with retry semantics (job queue) |
| `hybrid` | Combination (e.g., event triggers a workflow) |

**ADR required.** Include: the choice, alternatives considered, why, operational implications (who runs it, how it's monitored, failure modes).

### 3.2 Idempotency Strategy (`idempotencyStrategy`)

Non-negotiable for any automation that can be retried or re-triggered.

| Strategy | When |
|----------|------|
| `natural-key` | The domain has a natural unique key (ticket id, order number) — use it |
| `idempotency-key-header` | External callers supply a key (API-driven automation) |
| `deduplication-store` | Track processed ids in a store with TTL |
| `exactly-once-delivery` | The infrastructure guarantees it (rare, expensive; verify the claim) |

**ADR required** if the choice is non-obvious or has cost implications.

### 3.3 Retry / Compensation Strategy (`retryCompensationStrategy`)

| Strategy | When |
|----------|------|
| `retry-with-backoff` | Transient failures; the operation is safe to repeat |
| `saga-orchestrated` | Multi-step across services; a central coordinator drives compensation |
| `saga-choreographed` | Multi-step; each service emits events and compensates on failure events |
| `dead-letter-reprocess` | Failures park in a DLQ for later human/automated reprocessing |

**Design requirements:**
- Define the **retry budget** (max attempts, backoff curve, total time cap).
- Define **what happens after retries exhaust** — dead-letter? alert? compensate?
- For multi-step automations: define the **compensation action for every step** that mutates state.
- Connect to the UXP's exception model — failed items must reach the exception queue the UX designed.

**ADR required** for saga choices (choreography vs. orchestration is a material architectural decision).

### 3.4 Actor Identity (`automationActorIdentity`)

| Model | When |
|-------|------|
| `service-account` | Dedicated non-human account with scoped permissions |
| `managed-identity` | Cloud-native identity (no stored credentials) |
| `api-key` | External system integration (rotate, vault-stored) |
| `delegated-user` | Acts on behalf of a specific user (OBO flow) — needed when the action must be attributed to a person |

**Design requirements:**
- **Least privilege** — the automation gets only the permissions its `provides.writes` requires.
- For `controlled` control class: **segregation of duties** — the automation's identity must not be able to both initiate and approve.
- Never share an identity across automations with different blast radii.

**ADR required** for `controlled` / `safety-critical` control class.

### 3.5 Audit Strategy (`auditStrategy`)

| Strategy | When |
|----------|------|
| `event-sourced` | The event log IS the audit trail (event-sourced system) |
| `append-log` | Dedicated append-only audit table/file |
| `structured-jsonl` | Structured log lines to a log aggregator |
| `external-siem` | Pushed to an external compliance/SIEM system |

**Design requirements:**
- Every automated action that mutates state must produce an audit record.
- Audit record minimum: timestamp, `automationFeatureId`, actor identity, trigger (what caused it), input reference, decision/rule applied, outcome, affected entity.
- Retention must satisfy the control class (regulated processes often require 7+ years).
- Audit records must be **immutable** — append-only, no updates or deletes.

### 3.6 Loop-Guard Strategy (`loopGuardStrategy`)

Mandatory for any `event`-triggered automation whose `provides.emits` could reach its own `requires.events` (directly or transitively).

| Guard | Purpose |
|-------|---------|
| `causedBy-filter` | Stamp `causedBy: {automationFeatureId}` on emitted events; the trigger filter drops self-caused events |
| `hop-budget-ttl` | Each causal chain carries a hop counter; drop when exceeded (prevents transitive loops) |
| `circuit-breaker` | Open the circuit after N failures/second — halts runaway execution |
| `kill-switch` | Manual emergency stop (architectural support for the UXP's kill-switch) |
| `combined` | Multiple guards (recommended for Unattended + high-volume) |

**Design requirements:**
- Extend the existing `derivedFrom` provenance convention with `causedBy` for runtime causality.
- Define the hop budget explicitly (a number, e.g. 5) and what happens at exhaustion (drop + alert).
- The kill-switch must be architecturally real — a config flag the running automation checks, not just a UI button.

**ADR required** for any Unattended automation.

---

## Step 4: Formalize `requires` / `provides`

POLC authored intent-level declarations. Formalize them into the technical contract:

```yaml
requires:
  data:   [ticket, agent, routing_rule]        # concrete entities/tables/streams
  auth:   [crm-api, notification-service]      # concrete external systems needing credentials
  roles:  [ticket-router-service-account]      # the concrete actor identity
  events: [ticket.created]                     # concrete event names/topics
provides:
  writes: [ticket.assignee, ticket.routed_at]  # concrete fields mutated
  emits:  [ticket.assigned]                    # concrete events raised
```

**Rules:**
- Every `requires.data` entity must exist in the data architecture (or be added).
- Every `requires.auth` must map to a concrete integration with a credential plan.
- Every `requires.roles` must map to a defined identity with explicit permissions.
- Every `requires.events` must have a producer somewhere in the system (or be flagged as a readiness gap).
- Every `provides.emits` must have a defined schema.

---

## Step 5: Build the Trigger→Effect Graph

Assemble the cross-feature graph from all features' `requires.events` and `provides.emits`, **across all active lenses** (AI + Automation).

```
Node   = a lens feature (aiFeature or automationFeature)
Edge   = an emit → event match (feature A emits X; feature B triggers on X)
```

Include AI features: an `aiFeature`'s effects can feed an `automationFeature`'s trigger. Cross-lens edges are exactly why this graph must be lens-agnostic.

---

## Step 6: Run the Three Coherence Checks

Per `lens-seam/LENS_COHERENCE_PROTOCOL.md` §3:

### 6.1 Vertical (down one feature's thread)
- Is every tagged feature architected? (tagged but no ADR = gap)
- Does the architecture satisfy POLC's acceptance criteria? (SLA achievable? exception path designed? reversibility possible?)
- Does the architecture support UXD's control model? (kill-switch → circuit-breaker exists? pause → state preserved?)

### 6.2 Readiness (feature's `requires` vs. the system's `provides`)
- Every `requires.data` entity defined?
- Every `requires.auth` has a provisioning plan?
- Every `requires.roles` has a permission definition?
- Every `requires.events` has a producer?

### 6.3 Horizontal (across features + across lenses)
- **Write conflicts:** do two features mutate the same field? (define precedence or serialize)
- **Trigger cycles:** run cycle detection on the graph. Any cycle = red.
- **Contradictions:** do two features enforce opposing rules?
- **Contention:** do multiple heavy automations share a schedule window or resource?

---

## Step 7: The Design Coherence Gate

At the **ADLC→DWG boundary** — the last Layer-2 checkpoint before AI-DWG generates Layer 3 — produce the **Coherence Report**:

```markdown
# Design Coherence Report

**Generated:** {timestamp}
**Overall verdict:** 🟢 Green | 🟡 Amber | 🔴 Red

## Per-Feature Verdicts

| Feature ID | Lens | Vertical | Readiness | Horizontal | Verdict |
|-----------|------|:--------:|:---------:|:----------:|:-------:|
| AUTO-001 | Automation | ✅ | ✅ | ✅ | 🟢 |
| AIF-001 | AI | ✅ | ⚠️ | ✅ | 🟡 |

## Findings

### Coverage gaps
{tagged features missing an architectural hop}

### Unmet requirements
{requires with no matching provides}

### Detected cycles
{cycles in the trigger→effect graph, naming participating feature ids}

### Write conflicts
{features mutating the same field}

### Cross-lens interactions
{AI effect → automation trigger edges, and whether guarded}

## Gate Decision
🟢 Green → proceed to AI-DWG generation.
🔴 Red → resolve in the Layer-2 design chain before generating Layer 3.
```

**Gate rule:** Red blocks generation. Amber requires explicit user acknowledgment. Green proceeds.

---

## Step 8: Record & Inform Downstream

Record per feature in the AP:

```yaml
---
automationFeature: true
automationFeatureId: AUTO-{NNN}
automationEngineStrategy: {value}
idempotencyStrategy: {value}
retryCompensationStrategy: {value}
automationActorIdentity: {value}
auditStrategy: {value}
loopGuardStrategy: {value}
requires: { ... }    # formalized
provides: { ... }    # formalized
---
```

Plus the ADRs. Inform: "Automation Lens: architecture designed for {N} features; {M} ADRs produced; Coherence Gate = {verdict}."

**Downstream:** AI-DWG reads the architecture to provision the runtime + courier the context (including the guards) into Layer 3.

---

## Guards Handed to Layer 3

The guards designed here become **guardrails pushed down** by AI-DWG:
- The `causedBy` stamping convention
- The hop-budget value
- The idempotency key definition
- The circuit-breaker thresholds
- The kill-switch mechanism
- The audit record schema

`ATG__` (GCE) will later verify the implementation kept them; `ATQ__` (TGE) will test that they work.

---

## What This Facet Does NOT Do

- Does not rewrite acceptance criteria (AI-POLC owns them).
- Does not design human interfaces (AI-UXD owns them).
- Does not generate workspace scaffolding or config (AI-DWG).
- Does not enforce compliance at runtime (AI-GCE `ATG__`).
- Does not execute tests (AI-TGE `ATQ__`).

---

*Automation-LENS ADLC Facet v1.0.0 | Integration: component + data + integration design + decisions + Coherence Gate | Sub-module: `automation-lens/architecture/` | Author: Maheri*
