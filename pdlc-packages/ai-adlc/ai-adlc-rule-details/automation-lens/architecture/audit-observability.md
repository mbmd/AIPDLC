# Automation Architecture — Audit & Observability

> **Sub-module of** `automation-lens/facet.md`. Loaded on demand when designing the audit trail and monitoring.
> **Sub-role:** `#persona-subrole-audit-specialist`

---

## The premise

When a human does something, there is an implicit witness — the human. When an automation does something unattended, **the audit record is the only evidence it happened, what it decided, and why.** If the record is missing or thin, the action is effectively unaccountable.

Two distinct concerns, often conflated:
- **Audit** — the durable, immutable record of *what the automation did* (compliance, forensics, dispute resolution)
- **Observability** — the operational signal of *whether the automation is healthy* (monitoring, alerting, debugging)

Design both. They have different retention, different consumers, and different schemas.

---

## 1. Audit Strategy Selection

| Strategy | Mechanism | Use when |
|----------|-----------|----------|
| **Event-sourced** | The domain event log IS the audit trail | The system is already event-sourced — don't build a parallel trail |
| **Append-log** | Dedicated append-only audit table | Relational system; need queryable audit with referential integrity |
| **Structured JSONL** | Structured log lines to an aggregator | Distributed system; audit consumed via log tooling |
| **External SIEM** | Pushed to a compliance/SIEM platform | Regulated environment with a mandated central audit system |

**Design requirement:** for `controlled` / `safety-critical` control class, the audit store must be **write-once** from the automation's perspective — the automation's identity must not hold UPDATE or DELETE on audit records.

---

## 2. The Audit Record

### Minimum required fields

Every state-mutating automated action produces a record containing:

| Field | Why |
|-------|-----|
| `timestamp` | When it happened (ISO-8601, UTC) |
| `automationFeatureId` | Which automation (`AUTO-{NNN}`) |
| `automationVersion` | Which version of the automation logic |
| `actorIdentity` | The identity that performed it (see `actor-identity.md`) |
| `onBehalfOf` | The human, if a delegated identity was used |
| `trigger` | What caused this run — event id, schedule occurrence, or human trigger |
| `correlationId` | Ties the whole causal chain together |
| `causedBy` / `causalHops` | Provenance (see `loop-guards.md`) |
| `targetEntity` | What was acted upon (type + id) |
| `decision` | **The rule/logic applied and the outcome chosen** |
| `inputSnapshot` | Reference to (or hash of) the input that drove the decision |
| `outcome` | `success` \| `failed` \| `skipped` \| `compensated` + detail |
| `beforeAfter` | For mutations: the prior and new value of changed fields |

### The field that gets skipped and shouldn't

**`decision`** — *why* the automation did what it did. "Assigned to Team B" is not enough; "matched routing rule R-14 (category=billing AND priority>=high) → Team B" is. Without it, every dispute becomes an archaeology project, and drift is undetectable.

### Design requirements

- **Immutable.** Append-only. No updates, no deletes, no "corrections" — a correction is a new record referencing the original.
- **Complete or absent, never partial.** Write the audit record in the same transaction as the mutation where possible; if not possible, write audit **first** (a recorded action that didn't happen is safer than an unrecorded action that did).
- **Include skips.** An automation that ran and deliberately did nothing must record that, with the reason. Silence is indistinguishable from failure.
- **Reference, don't embed, large payloads.** Store a pointer or hash; keep the record queryable.
- **No secrets, minimal PII.** Audit records are long-retained and widely read. Store references to sensitive data, not the data.

---

## 3. Retention

| Control class | Typical minimum | Driver |
|---------------|----------------|--------|
| Informational | 90 days | Operational debugging |
| Operational | 1 year | Business dispute resolution |
| Controlled | 7 years | SOX / financial regulation (verify your jurisdiction) |
| Safety-critical | Life of the system + statutory period | Regulatory / liability |

**Design requirements:**
- **State the retention period in the ADR** with its driver ("7 years — SOX scope").
- Define the **archival path** — retention rarely means "hot storage for 7 years." Design the tiering.
- Retention must be **enforced technically**, not by policy alone (lifecycle rules, immutable storage locks).
- Confirm retention does not conflict with data-deletion obligations (GDPR erasure vs. audit retention — usually audit wins under legal-obligation basis, but the tension must be documented, not discovered).

---

## 4. Traceability

The audit trail must answer, for any entity: **"what did automation do to this, when, and why?"**

**Design requirements:**
- **Indexed by target entity** — the primary query is "show me everything that happened to ticket #4471."
- **Indexed by correlation id** — the secondary query is "show me the whole causal chain from this trigger."
- **Queryable by `automationFeatureId`** — for per-automation review and the DFE traceability view.
- Connect to the UXP's monitoring model: the `run-history` and `queue-view` surfaces read from this data. The audit design must support the UX the designer specified.

---

## 5. Observability (operational)

Distinct from audit. Consumers are operators, not auditors.

### Required signals per automation

| Signal | Purpose |
|--------|---------|
| **Execution count** (by outcome) | Is it running? Succeeding? |
| **Duration** (p50/p95/p99) | Is it meeting the SLA from POLC's AC? |
| **Error rate** | Health |
| **Queue depth / lag** | Falling behind? (see `event-infrastructure.md`) |
| **Retry rate** | Hidden instability — high retries with eventual success masks a real problem |
| **DLQ depth** | Accumulating failures |
| **Straight-through rate** | The POLC acceptance criterion — measure it, don't assume it |
| **Circuit-breaker state** | Open = incident |
| **Kill-switch state** | Is it currently stopped? (surprisingly often the answer to "why isn't it working") |

### Required alarms for Unattended automation

| Alarm | Threshold |
|-------|-----------|
| Error rate elevated | Above baseline + margin |
| DLQ non-empty | Any items (or above a small tolerance) |
| Duration breaching SLA | p95 above the AC bound |
| Queue depth growing | Sustained growth over N minutes |
| Circuit breaker open | Immediate |
| **Zero executions when expected** | No runs in a window where runs are expected |

**The last one is the most-missed alarm.** A stopped automation produces no errors, no DLQ items, no latency spikes. It looks identical to a quiet period. For any scheduled or steady-volume automation, alarm on *absence*.

### Correlation with audit

Observability metrics and audit records should share `correlationId` so an operator investigating a metric spike can jump to the specific actions.

---

## 6. Monitoring by Sub-Mode

| Sub-mode | Observability bar |
|----------|------------------|
| **Assisted** | Basic — error logging; failure is visible to the human doing the work |
| **Attended** | Medium — failures must reach the supervising human; queue/approval depth visible |
| **Unattended** | **Full — all signals + all alarms above.** Nobody is watching; instrumentation is the only visibility. |

---

## 7. Handoff to Layer 3

AI-DWG provisions:
- The audit sink (table/topic/log destination) + the record schema
- The log/metric emission configuration
- The alarm definitions where the platform supports declarative alarms
- The dashboard scaffolding matching the UXP's monitoring model

`ATG__` (AI-GCE) verifies: audit completeness (every mutation has a record), immutability (no update/delete grants), required fields present (especially `decision`), retention configured.

`ATQ__` (AI-TGE) verifies: audit records are actually produced under test, including for failure and skip paths.

---

## Anti-patterns

- **Audit record without the decision rationale** — you know *what* happened but never *why*; disputes and drift become unresolvable.
- **Logging instead of auditing** — application logs rotate, are unstructured, and are not immutable. They are not an audit trail.
- **Auditing only successes** — failures and skips are the interesting cases.
- **Mutable audit records** — one UPDATE grant and the trail is no longer evidence.
- **Audit written after the mutation, best-effort** — crash between the two and the action is unrecorded.
- **Full PII / secrets in audit records** — long retention plus wide read access equals exposure.
- **No zero-execution alarm** — the automation silently stops and nobody notices for weeks.
- **Retention as policy without lifecycle enforcement** — data is deleted early or kept forever, both non-compliant.
- **Straight-through rate assumed, not measured** — the POLC acceptance criterion is unverifiable.

---

*Automation Architecture Sub-Module — Audit & Observability | v1.0.0*
