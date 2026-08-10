# Automation Architecture — Event Infrastructure

> **Sub-module of** `automation-lens/facet.md`. Loaded on demand when designing the event/queue layer.
> **Sub-role:** `#persona-subrole-event-driven-architect`

---

## Scope

The transport layer beneath event-driven and queue-worker automations: brokers, topics, queues, delivery guarantees, ordering, and scaling. Orchestration model selection lives in `orchestration.md`; reliability semantics live in `reliability.md`.

---

## 1. Queue vs. Topic

| | Queue (point-to-point) | Topic (publish-subscribe) |
|---|---|---|
| **Consumers** | One logical consumer group; each message handled once | Many independent subscribers; each gets a copy |
| **Use for** | Work distribution — "process this item" | Event notification — "this happened" |
| **Coupling** | Producer knows work must be done | Producer does not know or care who listens |
| **Automation fit** | `task-automation`, `queue-worker`, `intake-processing` | `integration`, `notification`, reactive automations |

**Design rule:** if a second automation later needs the same signal, a queue forces you to change the producer; a topic does not. **Default to topics for events, queues for work.**

---

## 2. Delivery Guarantees

| Guarantee | Reality | Implication |
|-----------|---------|-------------|
| **At-most-once** | Fire and forget; messages can be lost | Only acceptable for non-critical signals (metrics, best-effort notifications) |
| **At-least-once** | Messages never lost; duplicates possible | **The practical default.** Requires idempotency (`reliability.md` §1) |
| **Exactly-once** | Usually "at-least-once + broker-side dedup within a window" | Verify the actual scope — the guarantee rarely spans your whole processing path |

**Design requirements:**
- State the guarantee explicitly in the ADR. "We use at-least-once; idempotency is handled by {strategy}."
- **Never claim exactly-once without naming the mechanism and its window.** End-to-end exactly-once across a broker, your service, and an external API almost never exists.
- Acknowledge **after** successful processing, not on receipt. Acknowledging early converts at-least-once into at-most-once silently.

---

## 3. Ordering

**Ask first: does this automation actually require ordering?** Most do not. Ordering constrains scaling significantly, so require it only when correctness demands it.

| Need | Mechanism | Cost |
|------|-----------|------|
| No ordering | Parallel consumers, unrestricted | None — scales freely |
| Per-entity ordering | Partition/shard by entity key | Parallelism limited to partition count; hot keys become bottlenecks |
| Global ordering | Single partition, single consumer | No parallelism. Avoid unless truly required. |

**Design requirements:**
- If per-entity ordering is needed, **name the partition key** (usually the entity id) and confirm the broker honors ordering within a partition.
- **Beware hot partitions** — if one entity generates most events, that partition saturates while others idle.
- **Out-of-order arrival must be handled** even with ordering guarantees, because retries reorder. Prefer designs that are order-insensitive (idempotent, state-based rather than delta-based).

---

## 4. Event Schema

**Every event needs a defined schema.** Automation consuming an undocumented event shape breaks on the producer's next change.

### Minimum event envelope

```yaml
eventType: ticket.created          # namespaced, past-tense
eventId: {uuid}                    # unique — enables dedup
occurredAt: {ISO-8601}             # when the fact happened (not when published)
producer: {service-name}
schemaVersion: 1
correlationId: {trace-id}          # ties a causal chain together
causedBy: {featureId | user}       # provenance — see loop-guards.md
causalHops: {n}                    # hop budget — see loop-guards.md
payload: { ... }                   # the fact
```

### Schema rules

- **Past-tense event names** — `ticket.created`, not `create.ticket`. Events are facts, not commands.
- **Namespaced** — `{domain}.{entity}.{action}` so topics stay navigable.
- **Additive evolution only** — add optional fields; never remove or repurpose. Breaking changes get a new `schemaVersion` and a migration window with both versions published.
- **Carry identity, not the whole world** — include the entity id and the changed facts; consumers fetch detail if needed. (Fat events couple consumers to your internal model.)
- **Never put secrets or full PII in events** — events fan out, are retained, and end up in logs.

---

## 5. Topic / Queue Topology

**Decide:**
- **Granularity** — one topic per event type (recommended: clear, filterable, independently scalable) vs. one topic per domain (fewer resources, consumers filter). Prefer per-event-type unless resource cost is prohibitive.
- **Naming convention** — establish and document one (e.g. `{env}.{domain}.{entity}.{action}`).
- **Retention** — how long are events kept? Long enough to replay after an incident; short enough to satisfy data policy.
- **Replay capability** — can you re-consume from a point in time? (Often the fastest incident recovery for automation.) If yes, replay must be idempotent.
- **Dead-letter topology** — one DLQ per queue/consumer, not one shared. A shared DLQ makes triage impossible.

---

## 6. Scaling & Throughput

Derive the target from POLC's throughput/SLA acceptance criteria and PILC's volume assessment.

**Design requirements:**
- **State the target explicitly** — "200 events/hour peak, 5-second processing SLA."
- **Choose the scaling signal** — queue depth is the standard for workers; lag is standard for stream consumers.
- **Define max concurrency** — unbounded scaling can overwhelm a downstream dependency. Cap it, and pair with the circuit breaker (`reliability.md` §5).
- **Backpressure** — what happens when input exceeds processing capacity? (Queue grows — acceptable if bounded and monitored; define the depth alarm.)
- **Cold start** — for serverless consumers, does cold-start latency breach the SLA? If so, provisioned concurrency or a long-running consumer.

---

## 7. Monitoring Hooks

The infrastructure must expose what the UXP's monitoring model needs:

| UXP model | Infrastructure must provide |
|-----------|----------------------------|
| `live-dashboard` | Real-time queue depth, throughput, error rate, consumer lag |
| `run-history` | Per-execution records with start/end/outcome (see `audit-observability.md`) |
| `queue-view` | Queryable in-flight and failed items |
| `notification-only` | Alert hooks on failure thresholds |

**Minimum alarms for any Unattended automation:**
- Queue depth above threshold (backlog building)
- Consumer lag growing (falling behind)
- DLQ non-empty (failures accumulating)
- Error rate above threshold
- **Zero throughput when throughput is expected** (the silent-failure alarm — the most-missed one)

---

## 8. Anti-patterns

- **Undocumented event schema** — every consumer guesses; the producer's next change breaks them all.
- **Command-shaped events** (`doTheThing`) — couples producer to consumer behavior; you built RPC with extra latency.
- **Fat events carrying full internal models** — consumers bind to your schema; you cannot refactor.
- **Shared dead-letter queue** — cannot tell which consumer failed or why.
- **Acknowledging before processing** — silently downgrades delivery guarantees; messages vanish on crash.
- **Global ordering "to be safe"** — destroys throughput for a requirement you probably don't have.
- **No zero-throughput alarm** — a stopped automation looks exactly like a quiet period.
- **Secrets or PII in event payloads** — they persist in broker storage, logs, and every subscriber.

---

*Automation Architecture Sub-Module — Event Infrastructure | v1.0.0*
