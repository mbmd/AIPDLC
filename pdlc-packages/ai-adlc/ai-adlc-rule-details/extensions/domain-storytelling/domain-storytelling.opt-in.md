<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Domain Storytelling

## When This Extension Applies

Your system likely benefits from Domain Storytelling if:

- Domain experts explain the domain best by telling stories — "first this person does X, then that system does Y"
- You want a calmer, more linear discovery technique than Event Storming's sticky-note storm
- The domain is role- and workflow-rich, and capturing actors, activities, and work objects in narrative form would build shared understanding
- You plan to opt into DDD Tactical and want a discovery step that feeds it
- You want an explicit as-is vs. to-be comparison of a process

## Opt-In Question — Discovery-Method Selector (shared with Event Storming)

Domain Storytelling and **Event Storming** are alternative domain-discovery lenses that feed the same DDD / decomposition hand-offs. Present this selector **once** at Stage 4/5 — do not prompt for the two techniques separately:

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

If (b) or (c) → load `domain-storytelling.md` (this extension). If (a) or (c) → also load `../event-storming/event-storming.md`.

## Relationship to Other Extensions

Domain Storytelling is a **discovery** technique (like Event Storming), not a design-pattern rule set. It feeds — it does not replace — the tactical extensions:

- **DDD Tactical** (`ddd-tactical`) — work objects → candidate aggregates (DDD-01); story clusters → bounded contexts (DDD-08); captured terms → ubiquitous language (DDD-11)
- **Security & Identity** (Stage 8) — actors → the role/identity model

It sits **beside** Event Storming: same **Domain Modeller** sub-role, same downstream hand-offs. If neither tactical extension is active, a domain story still stands alone as a decomposition aid whose candidate contexts reconcile with the Stage 5 containers.

## Status: ✅ Available (v1.1)
