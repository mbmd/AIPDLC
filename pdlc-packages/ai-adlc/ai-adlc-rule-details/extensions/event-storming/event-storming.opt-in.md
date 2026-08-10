<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Event Storming

## When This Extension Applies

Your system likely benefits from Event Storming if:

- The domain is process-heavy or workflow-driven — behaviour (what happens) matters more than static data
- Bounded contexts are not yet obvious and need to be discovered from the flow of events
- Domain experts and the technical team need a shared, business-language model before design starts
- You plan to opt into DDD Tactical and/or Event Sourcing / CQRS and want a discovery step that feeds them
- Cross-context or cross-team workflows are a recurring source of ambiguity or disagreement

## Opt-In Question — Discovery-Method Selector (shared with Domain Storytelling)

Event Storming and **Domain Storytelling** are alternative domain-discovery lenses that feed the same DDD / decomposition hand-offs. Present this selector **once** at Stage 4/5 — do not prompt for the two techniques separately:

```
### Which domain-discovery technique would you like to run?

Both model the domain before structural design and feed DDD Tactical / the container
decomposition. Pick the lens that fits your team:

(a) Event Storming      -- sticky-note timeline of domain events; great for event-/process-rich
                           domains and for surfacing hotspots
(b) Domain Storytelling -- pictographic sentences (actor -> activity -> work object), numbered
                           in sequence; calmer and narrative; great when experts explain by example
(c) Both                -- narrate key scenarios with Domain Storytelling, then stress the
                           event flow with Event Storming (or vice-versa)
(d) Neither             -- decompose from requirements/containers without a discovery model

Recommended: (b) when domain experts explain by telling stories and the flow is role-driven;
(a) when behaviour/events dominate; (c) for a high-ambiguity core domain.
```

If (a) or (c) → load `event-storming.md` (this extension). If (b) or (c) → also load `../domain-storytelling/domain-storytelling.md`.

**What Event Storming adds if selected:** the sticky-note vocabulary (domain events, commands, actors, aggregates, policies/reactions, read models, external systems, hotspots); three levels (Big Picture → Process → Design); bounded-context discovery from event clusters; an Event Storming Board + Hotspot log; and hand-off rules that route each finding into DDD Tactical, Event Sourcing/CQRS, the Context Map, and ADRs — so the storming feeds the design, not a dead artifact. Best for process/workflow-rich domains and unclear context boundaries; skip for simple CRUD or when boundaries are already clear and agreed.

## Relationship to Other Extensions

Event Storming is a **discovery** technique, not a design-pattern rule set. It runs *before* the
tactical extensions and feeds them — it does not replace them:

- **DDD Tactical** (`ddd-tactical`) — events feed the Domain Event Catalog; command+event clusters become candidate aggregates; event clusters reveal the Context Map.
- **Event Sourcing / CQRS** (`event-sourcing-cqrs`) — events feed the event store; read models feed projections; policies feed process managers / sagas.

If neither tactical extension is active, Event Storming still stands alone as a decomposition aid for Stage 4/5.

## Status: ✅ Available (v1.1)
