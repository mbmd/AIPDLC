<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Team Topologies

## When This Extension Applies

Your system likely needs this extension if:

- You chose "Service-Oriented", "Microservices", or "Hybrid" decomposition (Stage 5)
- Two or more teams will own different parts of the system
- You want team boundaries designed against the architecture (Conway / inverse-Conway), not left implicit
- You intend to generate one isolated development workspace per team downstream (AI-DWG per-team topology)
- You need an authoritative team → bounded-context/service → contract ownership map

## Opt-In Question

```
### Would you like to apply Team Topologies modeling?

This extension adds detailed guidance for:
- Team classification (stream-aligned, platform, enabling, complicated-subsystem)
- Team interaction modes (collaboration, X-as-a-Service, facilitating)
- Conway / inverse-Conway alignment — team boundaries mirror the fracture planes (bounded contexts)
- Cognitive-load budgeting per team
- A shared identity registry (TEAM-* / BC-* / SVC-*) that threads team/context ownership
  through backlog (AI-POLC), UX (AI-UXD), architecture, and workspace generation (AI-DWG)
- Each team's "team API" — the contracts it publishes at its seams

(a) Yes — Model the team topology and mint the team → context → contract assignment
(b) No — Team ownership stays implicit in the core workflow (CODEOWNERS + one-team-per-service)

Recommended for: 2+ teams, service-oriented/microservices/hybrid decomposition, per-team
workspace isolation planned downstream
Skip if: Single team owns everything, or a modular monolith with one deployable unit
```

## Composes With

- **`ddd-tactical`** — consumes DDD-08 (bounded-context relationship map); each stream-aligned team owns one or more bounded contexts.
- **`microservices`** — consumes MS-01 (one team per service); a team owns 1..N services, all kept together as modules within that team's workspace.

> The split downstream is **team-granular, never per-service**: a team owns 1..N services/contexts, and they stay as modules inside that team's single workspace.

## Status: ✅ Available (v1.1)
