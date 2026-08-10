<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# ADR-{NNN}: Saga Pattern — {Business Operation Name}

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** {YYYY-MM-DD}
**Deciders:** {Names/Roles — typically CTO/Architect + Distributed-Systems / Resilience Engineer}
**Category:** Integration | Architecture

> **Use this ADR when** a single business operation mutates state across **more than one** service (microservices), or across **more than one aggregate** (event-sourced systems), and you must choose how consistency is coordinated. Distributed transactions (2PC/XA) are not an option (MS-05) — the choice is *how* to run the saga, not *whether*. This is a specialization of `templates/adr-template.md`; it pre-frames the choreography-vs-orchestration decision and its compensation design. The detailed per-step design belongs in the operation's **Saga Design Card** (see `extensions/microservices/microservices.md`) — link it under **Related**, do not duplicate it here.

---

## Context

{2-3 sentences: what business operation is this, why does it span services/aggregates, and what goes wrong today if the steps are not coordinated (partial failure leaves inconsistent state). State that 2PC across services is prohibited (MS-05), so a saga is required — this ADR records the pattern choice and compensation approach.}

### Operation Profile

| Aspect | Value |
|--------|-------|
| **Business operation** | {e.g., "place order", "provision account", "close period"} |
| **Trigger** | {API request / event / scheduled / user action} |
| **Participating services / aggregates** | {list — MUST exist in the Stage 5 container set / the aggregate model} |
| **Steps that mutate state** | {count + one-line each} |
| **Consistency requirement** | {strong-per-service + eventual-across / read-after-write needed where?} |
| **Latency budget** | {real-time (<1s) / near-real-time / deferred} |
| **Reversibility** | {fully compensatable / has a pivot (non-compensatable) step / irreversible after step N} |
| **Failure blast radius** | {what a stuck/partial saga affects} |
| **Control class** (if Automation Lens active) | {assisted / attended / unattended} |

---

## Decision Drivers

- **Coupling tolerance** — can participants know each other, or must they stay decoupled?
- **Observability / traceability** — how important is a single place that shows the whole flow?
- **Failure semantics & compensation complexity** — how hard is it to undo each step?
- **Number of steps & branching** — linear vs. conditional/parallel paths.
- **Team ownership** — one team across all steps, or many teams owning separate services?
- **Latency budget** — synchronous coordination cost vs. eventual completion.
- {Principle reference — e.g., "P{n}: async-first / operational simplicity"}

---

## Considered Options

Mirrors the Automation Lens model (`automation-lens/architecture/reliability.md` §3) so the lens path and the core path resolve to one framing.

| | **(a) Orchestration** | **(b) Choreography** | **(c) Avoid — redesign** |
|---|---|---|---|
| **Coordinator** | A central saga orchestrator drives each step + each compensation | Each service reacts to events and emits its own; no central brain | Re-shape the operation so it is single-service (one transaction) |
| **Visibility** | High — one place shows the whole flow | Low — flow is emergent across services | N/A (no distributed flow) |
| **Coupling** | Coordinator knows all participants | Participants know only events | Removed |
| **Failure reasoning** | Easier — orchestrator knows what to compensate | Harder — must trace event chains | Trivial — local rollback |
| **Choose when** | Flow is complex, needs visibility, or has conditional branching | Flow is simple, linear, and services must stay decoupled | Boundaries were drawn wrong; the split adds no value |

**Default recommendation:** **orchestration**, unless service decoupling is a hard requirement — the visibility is usually worth the coupling. Always consider (c): the cheapest saga is the one you don't need because the operation stays inside one service boundary.

---

## Decision

**Chosen:** Option ({x}) — {Orchestration / Choreography / Redesign to single-service}

{State the choice in 1-2 sentences. If (c), record the boundary change and stop here — no saga is built.}

---

## Rationale

{3-5 sentences connecting the choice to the specific drivers: why this pattern for THIS operation given coupling, visibility, step count, team ownership, and latency. Address why the rejected options were not suitable.}

---

## Compensation Design (consequence of the choice)

Every state-mutating step needs a **compensating action** — a semantic undo (not a rollback; you cannot un-send an email — you send a correction). Full detail lives in the **Saga Design Card**; this table records the decision-critical shape.

| # | Service / Aggregate | Action | Compensating Action | Compensatable? |
|:-:|---------------------|--------|---------------------|:--------------:|
| 1 | {service} | {action} | {semantic undo} | Yes |
| 2 | {service} | {action} | {semantic undo} | Yes |
| 3 | {service — pivot} | {action} | — (**pivot**: not compensatable) | **No** |
| … | {service} | {action} | {forward recovery only} | No |

**Pivot rule:** order any **non-compensatable** step **last** (the "pivot"). Before the pivot, failure ⇒ compensate backwards; after the pivot, only **forward recovery** is possible. State the pivot step explicitly: {step #}.

| Design guarantee | Decision |
|------------------|----------|
| **Compensations are idempotent** | {how — compensation can itself be retried} |
| **Compensation can fail** | {what then — alert + park in "needs manual intervention"; never silently ignore} |
| **Saga state persistence** | {where the saga's progress is stored so it survives restarts (MS-05 / ES-11)} |
| **Timeout** | {max saga duration; what happens on timeout} |
| **Idempotency of steps** | {natural key / idempotency-key / dedup store — see `reliability.md` §1} |
| **Process-manager (event-sourced only)** | {if ES: the saga is a process manager per ES-11 — reacts to events, issues commands, event-sourced when long-lived} |

---

## Consequences

### Positive
- {What this enables — e.g., "cross-service operation completes with a defined, testable failure path"}
- {Benefit 2}

### Negative
- {Trade-off accepted — e.g., "orchestrator is a new component to run and monitor" / "choreography flow is harder to trace"}
- {Limitation}

### Risks
- {What could go wrong — e.g., "compensation gap leaves inconsistent state", "saga stuck mid-flight"}
- {Mitigation — circuit breaker, dead-letter, alerting, monitoring the in-flight saga count}

---

## Related

- **Saga Design Card** for {operation} — the full per-step design (`extensions/microservices/microservices.md`).
- **MS-05** (Saga Pattern for Distributed Transactions) — the rule this decision satisfies.
- **ES-11** (Process Manager / Saga for Cross-Aggregate Workflows) — if the system is event-sourced.
- **Automation Lens** `automation-lens/architecture/reliability.md` §3 (Compensation/Saga) — the aligned reliability model; `facet.md` §3.3 (`saga-orchestrated` / `saga-choreographed`).
- ADR-{NNN}: {Data Architecture / Event schema} — event contracts the saga depends on.
- Principle P{n} / Constraint C{n}: {relevant driver}

---

## Usage Notes (For AI-ADLC)

**When to produce this ADR:**
- The **Stage 11 per-operation saga loop** selects "Saga — choreography" or "Saga — orchestration" for a consistency-sensitive operation.
- **MS-05** or **ES-11** flags a choreography-vs-orchestration choice while an extension is active.
- The **Automation Lens** (`reliability.md` §3) requires an ADR for a `saga-orchestrated` / `saga-choreographed` `retryCompensationStrategy`.

**Depth adaptation:**
- **Minimal** — if multi-service consistency is needed but no extension is active, produce **one** Cross-Service Consistency ADR from this template covering the system's approach (no per-operation cards).
- **Standard** — one ADR per non-obvious per-operation choice; pair each with a Saga Design Card.
- **Comprehensive** — add a Mermaid **sequence diagram** per saga (per `common/diagram-standards.md`) showing the happy path + compensation path, plus an explicit timeout/idempotency matrix.

**Cross-reference integrity (Rule 12):** every service/aggregate named here MUST exist in the Stage 5 container set (or the aggregate model). A saga referencing a non-existent service is a build error.

---

*Generated by AI-ADLC · AIFLC PDLC Family · © Mohammad Maheri · https://github.com/mbmd/AIFLC*
