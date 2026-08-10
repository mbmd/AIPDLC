<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Event Storming

**Extension ID:** event-storming
**Version:** 1.1.0
**Rule Prefix:** EVS
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 5 (Container Design — decomposition)
- **Secondary Stages:** Stage 4 (System Context), Stage 11 (Integration & Infrastructure), Stage 12 (Component Design)

Event Storming is a **discovery technique**, not a design-pattern rule set. It models the domain as a timeline of events to reveal behaviour, boundaries, and ambiguity *before* structural design. Its output **feeds** the tactical extensions rather than replacing them:

- **DDD Tactical** (`ddd-tactical`) — events → Domain Event Catalog (DDD-04); command+event clusters → aggregates (DDD-01); event clusters → Context Map (DDD-08).
- **Event Sourcing / CQRS** (`event-sourcing-cqrs`) — events → event store (ES-01); read models → projections (ES-07); policies → process managers/sagas (ES-11).

If neither tactical extension is active, Event Storming still stands alone as a decomposition aid — its candidate bounded contexts reconcile with the Stage 5 containers.

---

## MANDATORY: Extension Sub-Role — Domain Modeller (Event Storming Facilitator)

When this extension is active, ALSO adopt the mindset of a **Domain Modeller facilitating an Event Storming session**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension for the duration of Event Storming rule enforcement. (This is the same **Domain Modeller** sub-role used by DDD Tactical, applied to discovery rather than design.)

### Behavioral Shifts
- Explore behaviour as a timeline first — ask "what happened, and then what happened?" before "what are the entities?"
- Facilitate, don't solve — surface disagreement as a hotspot instead of resolving it prematurely
- Speak the domain's language — capture the exact words domain experts use; those words become the ubiquitous language
- Let structure emerge — aggregates and contexts are *read out of* event clusters, not decided up front

### Anti-Patterns for This Extension
- Do NOT model data, entities, or tables before the event flow is understood ("nouns first")
- Do NOT resolve every question in the room — a hotspot tracked is better than a decision rushed
- Do NOT let the board become a deliverable in itself — its only value is what it feeds downstream

### Quality Check
A good output with this extension sounds like:
- "23 events across 3 candidate contexts; 4 policies (2 cross-context → sagas); 6 hotspots logged (2 → ADR); ubiquitous-language glossary started per context; candidate aggregates handed to DDD Tactical..."

---

## Rules

### Rule EVS-01: Domain Event as the Modeling Primitive

**Statement:** The domain is modeled first as a chronological series of domain events — facts that have already occurred, named in past tense and in the domain's language. Events are discovered before commands, actors, or structure.

**Verification:**
- [ ] Events are named in past tense and in business language (e.g., `OrderPlaced`, `TicketEscalated`) — not technical mutations (`RowInserted`)
- [ ] Each event represents a business-meaningful fact, not a CRUD operation
- [ ] Events are placed on a single timeline in the order they occur
- [ ] The event set is captured on the Event Storming Board before any structural modeling begins

**Anti-Pattern:** Jumping straight to entities/tables or aggregates before the event flow is understood — modeling the nouns first, which locks in structure the behaviour hasn't justified.

**ADR Trigger:** No — surviving domain events feed DDD-04 (Domain Event Catalog) and, when Event Sourcing is active, the ES-01 event store.

---

### Rule EVS-02: A Command Behind Every Event

**Statement:** Every domain event must be traceable to what caused it — a command (an actor's intent/decision), a policy (EVS-05), an external system (EVS-07), or a time trigger. Commands are named in the imperative and represent a decision to change the system.

**Verification:**
- [ ] Each domain event has an identified cause (command, policy, external, or temporal trigger)
- [ ] Commands are named imperatively (`PlaceOrder`, `EscalateTicket`)
- [ ] Command → event causality is captured on the board
- [ ] Events with no discernible cause are flagged as hotspots (EVS-08), never left implicit

**Anti-Pattern:** Recording events with no origin, hiding missing business rules or unknown triggers behind a tidy-looking timeline.

**ADR Trigger:** No — commands populate the "Commands Handled" field of the DDD Aggregate Design Card and, on the CQRS command side (ES-06), the write-model commands.

---

### Rule EVS-03: An Actor Behind Every Command

**Statement:** Every command must name the actor — the user role or system — that issues it. Actors express *who* needs the capability and are the seed of the role and permission model.

**Verification:**
- [ ] Each command has an identified actor (a human role or a system)
- [ ] Actor names are roles, never named individuals
- [ ] External-system actors are distinguished from human actors (links to EVS-07)
- [ ] Actors reconcile with the Security & Identity role model (Stage 8) and, where present, AI-UXD personas

**Anti-Pattern:** Modeling commands without asking "who does this?", producing a system with no clear ownership or authorization story.

**ADR Trigger:** No

---

### Rule EVS-04: Aggregates Emerge From Command–Event Clusters

**Statement:** Aggregates are discovered, not assumed. A candidate aggregate is the unit that receives a command and decides which events result, clustering the commands and events that must stay consistent together. Event Storming *identifies* candidate aggregates; their boundary and invariant design is owned by DDD Tactical.

**Verification:**
- [ ] Commands and the events they produce are grouped into candidate aggregates
- [ ] Each candidate aggregate has a business name in the ubiquitous language
- [ ] Consistency expectations are noted (what must be true immediately vs. eventually)
- [ ] Candidate aggregates are handed to DDD-01 for boundary/invariant design — this rule does NOT finalize internals

**Anti-Pattern:** Finalizing aggregate internals, invariants, or persistence during storming — pre-empting DDD Tactical and freezing the design before the flow is fully understood.

**ADR Trigger:** No — aggregate-boundary ADRs are raised under DDD-01 when a boundary is contested.

---

### Rule EVS-05: Policies Capture "Whenever X, Then Y"

**Statement:** Reactive rules — where an event automatically triggers a command without direct actor involvement — must be captured as policies ("whenever {event}, {command}"). Policies make implicit business automation explicit.

**Verification:**
- [ ] Each policy is written as "whenever {event} then {command}"
- [ ] The owning actor/system, or its automated nature, is noted
- [ ] Cross-aggregate policies are flagged (they become process managers / sagas)
- [ ] Time-based triggers (e.g., "after 24h unpaid") are modeled as policies with a temporal condition

**Anti-Pattern:** Leaving reactive automation implicit, so the built system carries hidden behaviour nobody modeled or agreed.

**ADR Trigger:** No — cross-aggregate policies hand off to ES-11 (process manager/saga); single-context stateless policies hand off to DDD-09 (domain service).

---

### Rule EVS-06: Read Models Capture Decision Information

**Statement:** Wherever an actor needs information to issue a command, capture the read model — the view the actor consults to decide. Read models express the query needs surfaced by the flow.

**Verification:**
- [ ] Each decision point notes the read model the actor consults
- [ ] Read models are named for the decision they support (e.g., "Open Tickets Queue")
- [ ] The events a read model is derived from are noted where known
- [ ] Read models are distinguished from write-side aggregates

**Anti-Pattern:** Designing commands without asking "what does the actor need to see to decide?", producing UIs and APIs with no informational basis.

**ADR Trigger:** No — read models hand off to ES-07 (projection design) when Event Sourcing is active, and otherwise inform the query/API surface (Stage 10) and data model (Stage 9).

---

### Rule EVS-07: External Systems at the Boundary

**Statement:** Systems outside the modeled domain that emit or consume events must be captured as external systems, marking the seams where integration and model translation are required.

**Verification:**
- [ ] Each external system that produces or consumes an event is captured
- [ ] The direction is noted (emits to us / consumes from us)
- [ ] Events that cross the boundary are marked as candidates for integration events (vs. internal domain events)
- [ ] Each external seam is flagged for an Anti-Corruption Layer

**Anti-Pattern:** Treating external systems as if they were part of the domain, letting foreign models leak into the core.

**ADR Trigger:** No — external seams hand off to DDD-07 (ACL) and DDD-12 (domain vs. integration event separation); boundary events feed Stage 11 integration.

---

### Rule EVS-08: Hotspots Capture Problems, Questions, and Risks

**Statement:** Every disagreement, unknown, risk, or assumption surfaced during storming must be captured as a hotspot rather than resolved on the spot. Hotspots are the backlog of what the design must still settle.

**Verification:**
- [ ] Hotspots are recorded in the Hotspot Log with a clear question or problem statement
- [ ] Each hotspot has a type (question / risk / assumption / conflict)
- [ ] Each hotspot has a disposition path: → ADR, → Issue register, → Assumption (Vision constraints table), or → resolved-in-session
- [ ] No hotspot is left without an owner or a disposition at stage completion

**Anti-Pattern:** Debating a hotspot to a premature conclusion mid-storm — losing the flow and burying the uncertainty instead of tracking it.

**ADR Trigger:** Yes — when a hotspot resolves into a decision between 2+ viable architectural options with long-term impact.

---

### Rule EVS-09: Pivotal Events and Timeline Ordering

**Statement:** Events must be arranged left-to-right in the order they occur, and pivotal events — those marking a significant state or phase transition — must be identified. Pivotal events reveal the natural phase and boundary lines in the flow.

**Verification:**
- [ ] The event timeline is ordered chronologically
- [ ] Pivotal events are explicitly marked
- [ ] Phases/swimlanes between pivotal events are named
- [ ] Parallel or alternative flows are represented, not forced into a single line

**Anti-Pattern:** An unordered pile of events with no temporal structure, from which no boundaries or phases can be read.

**ADR Trigger:** No

---

### Rule EVS-10: Bounded Contexts From Event Clusters

**Statement:** Candidate bounded contexts must be derived from the event flow — clusters of events and commands that share a language and change together, separated at pivotal events and at points where the same term changes meaning. These candidates reconcile with the Stage 5 container decomposition.

**Verification:**
- [ ] Candidate bounded contexts are drawn around cohesive event/command clusters
- [ ] Boundaries are placed where the ubiquitous language shifts (same word, different meaning)
- [ ] Each candidate context has a name and a one-line responsibility
- [ ] Candidate contexts are reconciled with Stage 5 containers (1:1, or the mismatch is explained)

**Anti-Pattern:** Drawing context boundaries along technical or organizational-chart lines instead of language and event cohesion.

**ADR Trigger:** Yes — when a bounded-context boundary is non-obvious or contested, or when it drives the container decomposition.

---

### Rule EVS-11: Ubiquitous Language Captured During Storming

**Statement:** The names used on events, commands, aggregates, and contexts during storming *are* the ubiquitous language — they must be captured verbatim into a glossary as they are agreed, per context.

**Verification:**
- [ ] A glossary is captured during (not after) the session
- [ ] Terms are recorded per candidate bounded context (the same term may differ across contexts)
- [ ] Event/command/aggregate names on the board match the glossary
- [ ] Disputed terms are logged as hotspots (EVS-08) rather than silently reconciled

**Anti-Pattern:** Letting the facilitator translate business terms into technical jargon on the board, losing the domain language at the exact moment it was available.

**ADR Trigger:** No — the glossary hands off to DDD-11 (Ubiquitous Language Enforcement).

---

### Rule EVS-12: Level Discipline and Hand-Off Completeness

**Statement:** Each session must declare its level — Big Picture (discovery), Process (commands/policies/read models), or Design (aggregates) — and must not skip ahead. At stage completion, every surviving board item must be routed to its downstream home; nothing is orphaned.

**Verification:**
- [ ] The session level (Big Picture / Process / Design) is declared and recorded in `adlc-state.md`
- [ ] Design-level modeling (aggregate internals) is NOT performed in a Big Picture session
- [ ] Every domain event maps to a DDD-04 catalog entry or an ES event (or is explicitly dropped, with reason)
- [ ] Every read model, policy, external system, and candidate context has a hand-off target (see the Tag → Artifact Hand-Off Map)
- [ ] Every hotspot has a disposition (EVS-08)
- [ ] Business-level events implying product capabilities are noted for AI-POLC epic identification — informational and upstream only (AI-POLC consumes this at its own Stage 5 discovery step; AI-ADLC does not own that hand-off)

**Anti-Pattern:** A rich storming board that never feeds the architecture — a "dead artifact" that impresses in the room and is never used again.

**ADR Trigger:** No

---

## Verification Checklist (Stage Completion)

Before completing a stage with Event Storming rules active, verify:

- [ ] Event timeline is captured, ordered, and pivotal events are marked
- [ ] Every event has a cause (command, policy, external, or temporal trigger) or is a logged hotspot
- [ ] Commands have actors; read models are noted at decision points
- [ ] Policies are captured as "whenever/then"; cross-aggregate ones flagged for sagas
- [ ] External systems and boundary events are identified
- [ ] Candidate aggregates and bounded contexts are named in the ubiquitous language
- [ ] Ubiquitous-language glossary is started, per context
- [ ] Hotspot Log is complete — each hotspot has a type and a disposition
- [ ] Session level is declared; every board item is routed (Tag → Artifact Hand-Off Map); no orphans remain

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| EVS-08 | A hotspot resolves into a decision between 2+ viable architectural options with long-term impact |
| EVS-10 | A bounded-context boundary is non-obvious/contested, or it drives the container decomposition |

---

## Templates

### Event Storming Board

The ordered flow. One row per domain event, left-to-right in time. Use `—` where a column does not apply.

```
| Seq | Domain Event (past tense) | Trigger (Command / Policy / External / Time) | Actor | Candidate Aggregate | Read Model consulted | External System | Bounded Context | Hotspot |
|----:|---------------------------|----------------------------------------------|-------|---------------------|----------------------|-----------------|-----------------|---------|
| 1 | {OrderPlaced} | Cmd: PlaceOrder | Customer | Order | Product Catalog | — | Ordering | — |
| 2 | {PaymentAuthorized} | Policy: whenever OrderPlaced | (system) | Payment | — | Payment Gateway | Payments | HS-02 |
| … | | | | | | | | |
```

> Optional: render the process-level command → aggregate → event → policy chain as a Mermaid flow per `common/diagram-standards.md`. The table is authoritative; the diagram is an aid.

### Hotspot Log

```
| ID | Board Item / Area | Question or Problem | Type | Disposition | Owner |
|----|-------------------|---------------------|------|-------------|-------|
| HS-01 | {event / area} | {what is unknown or contested} | question / risk / assumption / conflict | → ADR-{NNN} / → Issue / → Assumption / Resolved | {who} |
```

### Tag → Artifact Hand-Off Map

The routing contract — this is what makes Event Storming a feeder, not a silo. Every board item lands in one of these homes.

```
| Event Storming tag | Downstream home | Rule / artifact |
|--------------------|-----------------|-----------------|
| Domain Event | Domain Event Catalog · (ES) event store | DDD-04 · ES-01 |
| Command | Aggregate "Commands Handled" · (ES) command side | DDD Aggregate Design Card · ES-06 |
| Actor | Role/identity model · UXD personas | Stage 8 · AI-UXD |
| Candidate Aggregate | Aggregate boundary + design card | DDD-01 |
| Policy / Reaction | Process manager/saga · domain service | ES-11 · DDD-09 |
| Read Model | Projection · query/API + data model | ES-07 · Stages 10 / 9 |
| External System | Anti-Corruption Layer · integration events | DDD-07 · DDD-12 · Stage 11 |
| Bounded Context | Context Map · containers | DDD-08 · Stage 5 |
| Ubiquitous Language | Glossary per context | DDD-11 |
| Hotspot | ADR · Issue register · Assumption | EVS-08 · Architecture Workbook |
```
