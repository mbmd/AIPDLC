# Automation Architecture — Orchestration

> **Sub-module of** `automation-lens/facet.md`. Loaded on demand when designing the orchestration layer.
> **Sub-role:** `#persona-subrole-distributed-systems-engineer`

---

## Decision: Which orchestration model?

### The four models

| Model | Shape | State | Best for |
|-------|-------|-------|----------|
| **Workflow engine** | Central coordinator drives steps | Engine persists state | Long-running, multi-step, needs visibility + resumability |
| **Scheduler** | Clock fires a job | Stateless per run | Periodic batch work, no inter-step dependency |
| **Event consumer** | Reactive to a message | Stateless per event | High-volume, single-step reactions |
| **Queue worker** | Pulls work items | State in the queue + item | Work distribution with retry semantics |

### Choosing

Ask in order:

1. **Does the automation have more than one step that can fail independently?**
   - Yes → workflow engine or saga (see `reliability.md`)
   - No → continue

2. **What triggers it?**
   - Clock → scheduler
   - Event → event consumer
   - Work arriving in a backlog → queue worker
   - Human → invoke directly (attended mode)

3. **Does it run longer than the trigger's timeout?**
   - Yes → must be async; hand off to a queue/workflow, don't block the trigger
   - No → can execute inline

4. **Does the user need to see it mid-flight?** (from the UXP's monitoring model)
   - `live-dashboard` or `run-history` with in-progress state → workflow engine (it gives you this free)
   - `notification-only` → simpler model is fine

---

## Workflow engine specifics

If choosing a workflow engine:

**Decide:**
- **Orchestration vs. choreography** — see `reliability.md` (saga section); this is the same decision
- **Which engine** — evaluate against: does the team know it? operational burden? cost at your volume? does it support your language?
- **State persistence** — where does workflow state live? What is the backup/recovery story?
- **Versioning** — what happens to in-flight workflows when you deploy a new version? (This is the most-commonly-missed question.)

**ADR must cover:**
- The engine choice + alternatives + why
- Operational ownership (who runs it, who is on call)
- The in-flight-version-change policy
- Cost model at projected volume

---

## Scheduler specifics

If choosing a scheduler:

**Decide:**
- **Where the schedule lives** — cron in the platform? A scheduling service? Application-internal?
- **Overlap policy** — what if run N is still going when run N+1 fires? (skip / queue / run concurrently)
- **Missed-run policy** — if the scheduler was down, do you catch up or skip?
- **Clock authority** — timezone, DST handling. (DST is a classic source of double-runs or skipped runs.)

**Design requirement:** never assume a scheduled run happened. Record every run's start/end/outcome so a missed run is detectable.

---

## Event consumer specifics

If choosing an event consumer, see `event-infrastructure.md` for delivery guarantees, ordering, and scaling. The orchestration decision here is:

- **One consumer per event type, or one consumer handling many?** (Prefer narrow consumers — easier to reason about, scale, and fail independently.)
- **Where does the consumer run?** (Serverless function / long-running service / container)
- **Concurrency** — how many events processed in parallel? Does ordering matter? (see `event-infrastructure.md`)

---

## Queue worker specifics

**Decide:**
- **Queue technology** — see `event-infrastructure.md`
- **Worker pool sizing** — fixed or autoscaled? What signal drives scaling? (queue depth is the usual answer)
- **Visibility timeout** — how long before an unacknowledged item returns to the queue? Must exceed worst-case processing time.
- **Priority** — does the queue need priority lanes? (Beware: priority queues starve low-priority work; consider separate queues instead.)

---

## State machine design (any model)

If the automation progresses an entity through states (`automationPattern: state-transition` or any multi-step flow):

**Define explicitly:**
- The complete set of states
- The legal transitions (a table or diagram — not implied by code)
- Which transitions the automation may perform vs. which require a human
- Terminal states (success + each failure mode)
- What "stuck" looks like and how it is detected

**Design requirement:** an entity must never be in an undefined state. Every failure path must land in a defined terminal or recoverable state.

Produce a Mermaid state diagram in the AP per `common/diagram-standards.md`.

---

## Anti-patterns

- **Chained schedulers** — job A at 01:00 assumes job B finished by 00:59. Fragile. Use event-triggered or a workflow instead.
- **Implicit state in a database column with no transition table** — nobody knows the legal moves; every bug is a surprise.
- **Long-running work inside an event handler** — the event times out, redelivers, and you process twice. Hand off to a queue.
- **One giant workflow for everything** — a 40-step workflow is unmaintainable and its failure modes are untestable. Decompose.
- **Orchestration hidden in application code** — if the steps and their order live in an if/else chain, you have a workflow engine with no visibility. Make it explicit.

---

*Automation Architecture Sub-Module — Orchestration | v1.0.0*
