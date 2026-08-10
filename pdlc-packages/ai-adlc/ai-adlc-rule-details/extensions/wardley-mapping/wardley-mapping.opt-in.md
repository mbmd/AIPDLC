<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Wardley Mapping

## When This Extension Applies

Your architecture likely benefits from Wardley Mapping if:

- You face significant build-vs-buy decisions and want a rigorous, visual way to reason about them
- The system spans components at very different maturity levels (some novel/custom, some commodity)
- You want to avoid the classic trap of custom-building what you should buy as a commodity (or over-investing in an immature component for something non-core)
- Technology-stack choices carry long-term cost and strategic implications
- You want to reason about how components will evolve and where to concentrate engineering effort

## Opt-In Question

```
### Would you like to build a Wardley Map for build-vs-buy positioning?

Wardley Mapping plots your value-chain components against an evolution axis
(genesis -> custom-built -> product -> commodity/utility) so you can decide,
per component, whether to build, buy, or adopt a commodity -- and spot where
you're custom-building something you should simply consume.

This extension adds guidance for:
- Anchoring the map on a user need and laying out the value chain
- Positioning each component on the evolution axis
- A build / buy / adopt-commodity disposition per component
- Flagging anti-patterns (custom-building a commodity) as hotspots
- Hand-off of dispositions into the Technology Stack (Stage 6) and ADRs

(a) Yes -- build a Wardley map and drive build/buy decisions from it
(b) No  -- make technology-stack decisions without an explicit evolution map

Recommended for: systems with meaningful build/buy choices, mixed component maturity,
cost-sensitive or long-lived platforms
Skip if: small system, stack is largely dictated by constraints, or all components are commodity
```

If yes → load `wardley-mapping.md`

## Relationship to Other Stages

Wardley Mapping is an **architecture-positioning** technique. It runs at **Stage 6 (Technology Stack Selection)** and also informs **Stage 5 (Container Design)**. Its dispositions feed:

- **Technology Stack** (Stage 6) — the build / buy / adopt-commodity call per component
- **ADRs** — build-vs-buy decisions with long-term impact are classic ADR material
- **Component-evolution notes** — where to invest custom engineering vs. consume commodities

**Altitude note:** this is the **architecture-altitude** use of Wardley (component build/buy/evolution). The **strategy-altitude** use (market positioning, where-to-play) belongs to the Strategy family (SFLC) when it is built — the same technique at a higher altitude.

## Status: ✅ Available (v1.1)
