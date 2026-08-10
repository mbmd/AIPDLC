# How to Choose Architecture Extensions

**Purpose:** Practical guide for deciding which AI-ADLC extensions to activate — the decision criteria, common mistakes, composition rules, and downstream impact of each extension choice.

---

## Who This Is For

Architects and tech leads running AI-ADLC who reach the extension opt-in points and need to decide: "Does my architecture actually need this pattern? What are the consequences of activating it? Can I combine multiple extensions?"

---

## The Ten Extensions

| Extension | Pattern | One-Line Decision Criteria |
|-----------|---------|---------------------------|
| **Event Storming** | Collaborative domain discovery — events → commands → aggregates → bounded contexts | Process/behaviour-heavy domain where boundaries aren't obvious; run *before* DDD / Event Sourcing to discover the model |
| **Domain Storytelling** | Narrative domain discovery (actor → activity → work object) | Experts explain the domain by telling stories; a calmer alternative/complement to Event Storming (shared selector) |
| **DDD Tactical** | Domain-Driven Design (aggregates, entities, value objects, events) | Complex domain logic with multiple bounded contexts |
| **Microservices** | Independently deployable services | ≥3 services with separate deployment lifecycles |
| **BFF Pattern** | Backend-for-Frontend | Multiple frontend channels needing different API shapes |
| **Event Sourcing / CQRS** | Event store + command/query separation | Audit-critical data or temporal query requirements |
| **Resilience Patterns** | Circuit breakers, bulkheads, retries, fallbacks | ≥3 external integrations or high-availability requirement |
| **Feature Flags** | Controlled rollout, trunk-based delivery | Gradual rollout, A/B testing, or decoupled deployment/release |
| **Wardley Mapping** | Value-chain × evolution positioning | Significant build-vs-buy decisions; components at mixed maturity (Stage 6) |
| **Threat Modeling (deep)** | STRIDE DFD, attack trees, risk rating | High-security/regulated system where the always-run Stage 8 STRIDE baseline isn't enough |

---

## Decision Framework

For each extension, ask three questions:

### Question 1: "Does the architecture REQUIRE this pattern?"

| Extension | Required When | NOT Required When |
|-----------|--------------|-------------------|
| Event Storming | Domain is process-driven and bounded contexts/aggregates are unclear or contested; experts disagree on the model | Simple CRUD; domain already well understood; boundaries obvious |
| DDD Tactical | Domain has complex business rules spanning multiple entities; multiple teams own different domains | Simple CRUD; single domain; thin business logic layer |
| Microservices | Services need independent scaling, deployment, or technology choices | All components deploy together; single team owns everything |
| BFF Pattern | Mobile app needs different data than web; partner API needs different auth | Single frontend; all consumers need same API shape |
| Event Sourcing | Legal requirement to reconstruct past states; "what happened when" queries | Current-state-only queries; simple update-in-place sufficient |
| Resilience | SLA requires >99.9% uptime; cascade failure is a realistic risk | Internal tool; occasional downtime acceptable; few integrations |
| Feature Flags | Trunk-based development; need to deploy without releasing; A/B experiments | Feature branches with traditional release; no gradual rollout need |
| Domain Storytelling | Experts narrate the domain best as stories; want a linear discovery alternative to Event Storming | Boundaries already clear; Event Storming already chosen for the same slice |
| Wardley Mapping | Meaningful build-vs-buy choices; mixed component maturity; cost/lock-in matters | Small system; stack dictated by constraints; all components commodity |
| Threat Modeling (deep) | Regulated/sensitive data; complex trust boundaries; high attacker value | Low-sensitivity system where the baseline STRIDE checklist covers the risk |

**Key rule:** Activate because architecture DEMANDS it, not because it would be "nice to have." Each extension adds constraints, complexity, and cognitive overhead.

### Question 2: "Can the team deliver this pattern?"

| Extension | Team Capability Needed |
|-----------|----------------------|
| Event Storming | A facilitator; access to domain experts in the room; willingness to model behaviour before structure |
| DDD Tactical | Strong domain modeling experience; ability to identify aggregates and boundaries |
| Microservices | DevOps maturity; CI/CD per service; distributed tracing understanding |
| BFF Pattern | API design experience; understanding of client-specific optimization |
| Event Sourcing | Event modeling skill; eventual consistency tolerance; projection management |
| Resilience | Chaos engineering awareness; monitoring infrastructure; fallback design |
| Feature Flags | Flag lifecycle management; test complexity management; release coordination |
| Domain Storytelling | A facilitator; access to domain experts; willingness to narrate scenarios before structure |
| Wardley Mapping | Ability to assess market maturity of components; build-vs-buy judgment |
| Threat Modeling (deep) | Adversarial/security-analysis skill; DFD + attack-tree literacy; risk-rating discipline |

**If the team doesn't have the capability:** Consider whether the project timeline allows for learning, or whether a simpler pattern achieves 80% of the benefit with 20% of the complexity.

### Question 3: "What's the downstream impact?"

Each extension affects AI-DWG generation and AI-GCE governance:

| Extension | AI-DWG Impact | AI-GCE Impact |
|-----------|--------------|---------------|
| Event Storming | Indirect — no steering of its own; findings flow into DDD Tactical / Event Sourcing, which drive DWG output | Indirect — via the DDD / ES rules its findings produce |
| DDD Tactical | Domain-based folder structure; bounded context separation | Domain boundary enforcement; aggregate integrity rules |
| Microservices | Per-service folders; service mesh config; distributed tracing setup | Inter-service contract rules; deployment independence checks |
| BFF Pattern | BFF layer in container structure; per-client API routing | API versioning enforcement; BFF-specific security rules |
| Event Sourcing | Event store infrastructure; projection services; command/query separation | Event immutability rules; projection consistency checks |
| Resilience | Circuit breaker configs; health check endpoints; fallback implementations | Resilience pattern verification; SLA compliance rules |
| Feature Flags | Flag management service; evaluation endpoints; cleanup lifecycle | Flag hygiene rules (no stale flags); testing-with-flags requirements |
| Domain Storytelling | Indirect — findings flow into DDD Tactical (like Event Storming) | Indirect — via the DDD rules its findings produce |
| Wardley Mapping | Indirect — build/buy dispositions inform the Technology Stack + ADRs | Indirect — via the tech-stack decisions it drives |
| Threat Modeling (deep) | Indirect — mitigations become security controls | Security-compliance rules/hooks from the threat register; AI-TGE security tests |

---

## When Extensions Are Presented

AI-ADLC presents each extension at the stage where the decision is architecturally relevant:

| Extension | Presented At | Why |
|-----------|-------------|-----|
| Event Storming | Stage 5 (Container Design / Decomposition) | Boundaries and behaviour are discovered from the event flow before structure |
| DDD Tactical | Stage 4 (System Context) | Bounded contexts are a system-level concern |
| Microservices | Stage 5 (Container Design) | Service decomposition is a container decision |
| BFF Pattern | Stage 5 (Container Design) | BFF is an additional container |
| Event Sourcing / CQRS | Stage 9 (Data Architecture) | Fundamentally changes data model |
| Resilience Patterns | Stage 11 (Integration) | Applies to distributed communication |
| Feature Flags | Stage 12 (Component Design) | Affects component behavior implementation |
| Domain Storytelling | Stage 4/5 (System Context / Decomposition) | Narrative discovery; presented via a shared selector with Event Storming |
| Wardley Mapping | Stage 6 (Technology Stack) | Build-vs-buy positioning is a tech-stack decision |
| Threat Modeling (deep) | Stage 8 (Security & Identity) | Deep threat analysis layered on the always-run STRIDE baseline |

**You can decline now and activate later** — but activating later means re-running from the relevant stage (rules apply retroactively to prior decisions).

---

## Extension Composition (Combining Multiple)

Extensions are designed to compose without conflict:

### Common Combinations

| Combination | Use Case | Composition Notes |
|-------------|----------|-------------------|
| Event Storming + DDD | Discover the model, then formalize the tactics | Storming surfaces events/aggregates/contexts; DDD turns them into boundaries and invariants |
| Event Storming + Event Sourcing | Event-first discovery into an event-sourced design | The discovered domain events become the event store's backbone |
| DDD + Microservices | Bounded contexts mapped to services | DDD defines boundaries; Microservices defines deployment |
| Microservices + Resilience | Distributed services needing fault tolerance | Natural pair — distributed = needs resilience |
| Microservices + BFF | Multi-service backend with multiple frontends | BFF sits in front of the service mesh |
| Event Sourcing + DDD | Domain events as the core data model | Events ARE the domain model — deep synergy |
| Feature Flags + any | Gradual rollout for any architecture style | Purely additive — no conflicts with other patterns |
| Event Storming ↔ Domain Storytelling | Choose the discovery lens that fits the team | Alternatives via a shared selector; can run both (narrative first, event flow second); both feed DDD |
| Wardley + DDD / Microservices | Position build-vs-buy before decomposing | Wardley says what to build vs. buy; DDD / Microservices decompose what you build |
| Threat Modeling + Microservices / Event Sourcing | Deep security for complex distributed/audit systems | More trust boundaries → more to threat-model |

### Composition Rules

1. **Maximum active:** No formal limit, but >3 active extensions means very high complexity. Question whether the project truly needs all of them.
2. **No conflicts by design:** Each extension adds rules in its own namespace (EVS-*, DST-*, DDD-*, MICRO-*, BFF-*, ES-*, RES-*, FF-*, WDL-*, THM-*). No rule from one extension contradicts another.
3. **Additive only:** Extensions add constraints on top of core workflow. They never relax or remove core rules.
4. **Override triggers:** Some extensions force conditional generation in AI-DWG regardless of normal triggers. Example: Microservices forces `resilience-standards.md` generation even if <3 integrations.

---

## The Activation Decision Record

When you activate (or decline) an extension, AI-ADLC records it:

**In `adlc-state.md`:**
```yaml
Enabled Extensions:
  - DDD Tactical (activated Stage 4)
  - Resilience Patterns (activated Stage 11)
Declined Extensions:
  - Microservices (declined Stage 5 — single deployable unit)
  - Event Sourcing (declined Stage 9 — current-state queries sufficient)
  - BFF Pattern (declined Stage 5 — single frontend)
  - Feature Flags (declined Stage 12 — branch-based release)
```

**In ADR (for activated extensions):**
```markdown
# ADR-{N}: Activate {Extension Name}

## Decision
Activate {extension} because {rationale}.

## Consequences
- Adds {N} blocking rules to architecture stages
- AI-DWG will generate {additional steering files}
- AI-GCE will derive {additional rules}
- Team must be familiar with {pattern concepts}
```

---

## Common Mistakes

| Mistake | Why It Fails | Better Approach |
|---------|-------------|-----------------|
| "We might need microservices later" | Extensions add constraints NOW — activating "just in case" adds complexity without benefit | Decline. Activate when architecture demands it. |
| Activating DDD without domain expertise | DDD rules require aggregate identification, bounded context mapping | Build team capability first, or use simpler module patterns |
| All 10 extensions active on a small project | Overwhelming constraint set; most rules won't apply | Match extensions to actual complexity — most projects need 0-2 |
| Declining resilience with 5+ integrations | External dependencies WILL fail; no resilience = cascading outages | If you integrate heavily, resilience is not optional |
| Activating Event Sourcing for "audit logging" | ES is a fundamental data model change, not just an audit trail | Use append-only audit log instead — much simpler |

---

## Quick Decision Matrix

Answer Yes/No for your project:

| Question | Yes → Consider |
|----------|---------------|
| Domain is process/behaviour-heavy and boundaries are unclear? | Event Storming (then DDD / Event Sourcing) |
| Multiple business domains with different rules? | DDD Tactical |
| Services that must deploy independently? | Microservices |
| Mobile + Web + Partner needing different API shapes? | BFF Pattern |
| Must reconstruct historical state at any point in time? | Event Sourcing |
| ≥3 external services or 99.9%+ SLA requirement? | Resilience Patterns |
| Trunk-based delivery with gradual rollout needed? | Feature Flags |
| Experts explain the domain by telling stories (not events)? | Domain Storytelling (alternative to Event Storming) |
| Significant build-vs-buy decisions or mixed component maturity? | Wardley Mapping |
| Regulated/high-security system needing deep threat analysis? | Threat Modeling (deep) |
| All No? | No extensions — core workflow is sufficient |

---

## Related Documents

| Document | Location |
|----------|----------|
| How ADLC Extensions Work | `knowledge_docs/HOW_ADLC_EXTENSIONS_WORK.md` |
| How ADLC Progressive Decomposition Works | `knowledge_docs/HOW_ADLC_PROGRESSIVE_DECOMPOSITION_WORKS.md` |
| How to Design Architecture | `knowledge_docs/HOW_TO_DESIGN_ARCHITECTURE.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| Why Architecture Before Code Matters | `knowledge_docs/WHY_ARCHITECTURE_BEFORE_CODE_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-08-09 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
