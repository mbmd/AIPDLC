<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Team Topologies

**Extension ID:** team-topologies
**Version:** 1.0.0
**Rule Prefix:** TT
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 5 (Container Design) — where decomposition and "one team per service" first become real.
- **Secondary Stages:** Stage 12 (Component Design — aligns with the DDD-08 context map), Stage 6 / Stage 11 (platform- and enabling-team infrastructure).

These rules apply to team classification, team-to-team interaction, Conway alignment, cognitive-load budgeting, and the team → bounded-context/service → contract ownership assignment that downstream packages (AI-POLC, AI-UXD, AI-DWG, AI-GCE) consume.

---

## MANDATORY: Extension Sub-Role — Team Topology Architect

When this extension is active, ALSO adopt the mindset of a **Team Topology Architect** (`#persona-subrole-team-topology-architect`). This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension for the duration of team-topology work.

This sub-role carries a **dual mandate**: (1) organizational / topology *design* here in the DEFINE stage (this extension), and (2) governing that downstream development stays true to the designed topology (the same sub-role is layered by AI-GCE's team-topology generator in ENFORCE). Designing and governing the topology with one voice keeps the intent consistent across the DEFINE → GENERATE → ENFORCE relay.

### Behavioral Shifts
- Design team boundaries against the architecture's fracture planes (bounded contexts), not the existing org chart (inverse-Conway).
- Treat cognitive load as a hard budget — a team that owns too many unrelated contexts will not sustain flow.
- Name every team-to-team dependency's interaction mode explicitly; an unnamed dependency is an ungoverned coupling.
- Prefer stream-aligned teams that own a slice end to end; platform and enabling teams exist to reduce others' cognitive load, not to gate them.

### Anti-Patterns for This Extension
- Do NOT split ownership of one bounded context across two teams (shared ownership erases accountability).
- Do NOT make an enabling team a permanent runtime dependency (enabling is facilitating and temporary).
- Do NOT design a platform team that others must file tickets against for routine work (that is a bottleneck, not a platform).

### Quality Check
A good output with this extension sounds like:
- "4 teams: 3 stream-aligned (each owning 1–2 bounded contexts within cognitive-load budget) + 1 platform team exposing capabilities X-as-a-Service; interaction modes named for every seam; each team publishes the contracts at its edges."

---

## Composes With

- **`ddd-tactical`** (DDD-08 bounded-context relationship map) — each stream-aligned team owns one or more bounded contexts; TT-02/TT-08 build on the context map.
- **`microservices`** (MS-01 one-team-per-service, MS-09 independent deployment) — a team owns 1..N services; TT gives MS-01's "one team per service" an authoritative home and extends independent deployability to the team boundary.

---

## Rules

### Rule TT-01: Team Type Classification

**Statement:** Every team must be classified as exactly one of: stream-aligned, platform, enabling, or complicated-subsystem.

**Verification:**
- [ ] Every team in the topology has exactly one assigned type
- [ ] Stream-aligned teams are the majority (the default team type)
- [ ] Each platform / enabling / complicated-subsystem team has a stated reason it is not stream-aligned

**Anti-Pattern:** Unclassified teams, or a "component team" organized around a technical layer rather than a flow of change.

**ADR Trigger:** No

---

### Rule TT-02: One Stream-Aligned Team Owns Each Context

**Statement:** Each bounded context / service is owned by exactly one stream-aligned team. Ownership is never split across teams.

**Verification:**
- [ ] Every bounded context / service maps to exactly one owning stream-aligned team
- [ ] No context appears under two teams
- [ ] Every stream-aligned team owns at least one context

**Anti-Pattern:** Two teams jointly owning one context, producing merge conflicts, unclear accountability, and coordination overhead.

**ADR Trigger:** Yes — when a context's ownership is contested or a context must be split to fit team boundaries.

---

### Rule TT-03: Named Interaction Mode per Dependency

**Statement:** For every team-to-team dependency, name the interaction mode: collaboration, X-as-a-Service, or facilitating.

**Verification:**
- [ ] Every team-to-team edge has exactly one named interaction mode
- [ ] Collaboration modes are time-boxed (not permanent)
- [ ] X-as-a-Service dependencies point at a published contract (TT-10)

**Anti-Pattern:** Permanent, unnamed "we just talk to them" dependencies that hide coupling and erode team autonomy.

**ADR Trigger:** No

---

### Rule TT-04: Cognitive-Load Budget

**Statement:** Each team has a documented cognitive-load budget; the contexts/services it owns must fit within it.

**Verification:**
- [ ] Each team has a stated cognitive-load budget (e.g. a bounded number of owned contexts)
- [ ] No team owns more contexts than its budget allows
- [ ] Over-budget teams are flagged for splitting or platform support

**Anti-Pattern:** A team owning many unrelated contexts, guaranteeing shallow understanding and slow, error-prone change.

**ADR Trigger:** No

---

### Rule TT-05: Platform Teams Expose Capabilities as a Service

**Statement:** Platform team(s) expose their capabilities as a thinnest-viable-platform service; consumers self-serve without filing tickets for routine use.

**Verification:**
- [ ] Each platform team's offering is described as a self-serve capability
- [ ] Consuming teams do not require manual platform-team intervention for routine work
- [ ] The platform is "thinnest viable" — no capability included without a consuming team needing it

**Anti-Pattern:** A platform team that is a ticket-driven bottleneck, or a bloated platform built ahead of demand.

**ADR Trigger:** No

---

### Rule TT-06: Conway Alignment

**Statement:** Team boundaries must mirror the service/bounded-context (fracture-plane) boundaries. Mismatches are flagged as inverse-Conway maneuvers.

**Verification:**
- [ ] Each team boundary aligns to one or more whole bounded contexts (no team straddling half a context)
- [ ] Architecture fracture planes and team boundaries are cross-checked; mismatches are listed
- [ ] Where the org must change to fit the architecture, the required move is stated (inverse-Conway)

**Anti-Pattern:** Team boundaries cutting across a bounded context, so a single change requires two teams to coordinate.

**ADR Trigger:** Yes — when an inverse-Conway team reorganization is required to fit the designed architecture.

---

### Rule TT-07: Enabling Teams Are Temporary

**Statement:** Enabling teams operate in a facilitating mode and are never a permanent runtime dependency of a stream-aligned team.

**Verification:**
- [ ] Each enabling team's engagement has a stated end condition (capability transferred)
- [ ] No enabling team sits on a stream-aligned team's runtime critical path
- [ ] Enabling engagements are reviewed for exit

**Anti-Pattern:** An enabling team that becomes a permanent gate or a hidden runtime dependency.

**ADR Trigger:** No

---

### Rule TT-08: Fracture Planes Follow the Context Map

**Statement:** Fracture planes are bounded-context boundaries; team splits follow the DDD context map, not the org chart.

**Verification:**
- [ ] Every team split traces to a bounded-context boundary from the DDD-08 context map
- [ ] No split is justified only by existing reporting lines
- [ ] Shared-kernel and platform contexts are identified and assigned deliberately

**Anti-Pattern:** Splitting teams along seniority or reporting lines, cutting through cohesive contexts.

**ADR Trigger:** No

---

### Rule TT-09: Independent Deployability per Stream-Aligned Team

**Statement:** Stream-aligned teams deploy independently — no shared release train across teams.

**Verification:**
- [ ] Each stream-aligned team can deploy its owned services without coordinating other teams' releases
- [ ] No cross-team lockstep deployment is required
- [ ] Cross-team coupling is only via published contracts (TT-10), never source

**Anti-Pattern:** A shared release train forcing all teams to deploy together, negating team autonomy.

**ADR Trigger:** No

---

### Rule TT-10: Each Team Publishes the Contracts at Its Seams

**Statement:** Each team owns and publishes the contracts at its boundaries (its "team API") — the sanctioned coupling surface with other teams.

**Verification:**
- [ ] Every team lists the contracts it publishes (its produced APIs/events)
- [ ] Every cross-team dependency consumes a published contract at a pinned version
- [ ] No team reaches into another team's internals (only its published contracts)

**Anti-Pattern:** Teams integrating through shared internal code or databases instead of published contracts.

**ADR Trigger:** Yes — when defining the compatibility policy for a team's published contract (aligns with MS-06 when microservices is active).

---

## Shared Identity Registry (TEAM-* / BC-* / SVC-*)

This extension mints a stable identity that threads team/context ownership through the whole chain, replacing project-only correlation (`projectId`, too coarse) with a team/context-level key. This is a **formal ID** (not a name-matching heuristic).

| ID | Form (example) | Minted by | Referenced by |
|----|----------------|-----------|---------------|
| `TEAM-{slug}` | `TEAM-{payments}` | this extension | AI-POLC epics, AI-UXD flows, AI-DWG partitioning, AI-GCE CODEOWNERS |
| `BC-{slug}` | `BC-{payment}` (bounded context) | this extension (from the DDD-08 / component-design BC name → slug) | AI-POLC epics, AI-UXD flows, AI-DWG module→workspace map |
| `SVC-{slug}` | `SVC-{payment-api}` (service, if microservices) | the `microservices` extension | contract registry, AI-DWG module scoping |

**Rules for the registry:**
- Each team owns **1..N** `BC-*` / `SVC-*`. This one-team-to-many mapping is exactly what defines a per-team workspace split downstream (the split never goes finer than the team).
- Slugs are lower-case, hyphenated, derived from the context/service/team name — stable once minted (do not re-slug mid-project).
- The registry is recorded as a correlation key alongside `projectId` (finer-grained), per the family traceability and naming contracts.

---

## Artifacts Produced

When this extension is active, Stage 5 produces (in addition to the core container-design output):

| Artifact | Template | Content |
|----------|----------|---------|
| **Team Topology Map** (`team-topology-map.md`) | `templates/team-topology-map.md` | Teams, types, interaction modes — a Team-Topologies-style diagram (Mermaid, per `diagram-standards.md`). |
| **Team → Context → Contract Assignment + Registry** (`team-context-registry.md`) | `templates/team-context-registry.md` | The authoritative Team ↔ BC ↔ Service map + the `TEAM-*`/`BC-*`/`SVC-*` identity + each team's produced/consumed contracts. Machine-readable — AI-DWG reads it to partition the workspace. |
| **Team Definition Card** (per team) | `templates/team-definition-card.md` | Type · owned contexts/services · cognitive-load budget · interaction modes · published contracts. |

`adlc-state.md` records `Enabled Extensions += team-topologies` and the team roster + assignment, so downstream packages detect the topology by marker.

> This upgrades DDD-08's "team ownership per context is identified" checkbox and MS-01's "one team per service" note into first-class, designed artifacts with a shared identity.

---

## Verification Checklist (Stage Completion)

Before completing a stage with Team Topologies rules active, verify:

- [ ] Every team is classified as exactly one type (TT-01)
- [ ] Every bounded context / service has exactly one owning stream-aligned team (TT-02)
- [ ] Every team-to-team dependency names its interaction mode (TT-03)
- [ ] Every team is within its cognitive-load budget (TT-04)
- [ ] Platform teams expose self-serve capabilities (TT-05)
- [ ] Team boundaries align to fracture planes; mismatches flagged (TT-06, TT-08)
- [ ] Enabling teams have an exit condition (TT-07)
- [ ] Stream-aligned teams are independently deployable (TT-09)
- [ ] Every team publishes the contracts at its seams (TT-10)
- [ ] The `team-context-registry.md` (TEAM-*/BC-*/SVC-*) is produced and complete

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| TT-02 | A context's ownership is contested or a context must be split to fit teams |
| TT-06 | An inverse-Conway team reorganization is required to fit the architecture |
| TT-10 | Defining the compatibility policy for a team's published contract |

---

## Templates

### Team Definition Card

```
## Team: {TEAM-slug}

**Team Type:** stream-aligned | platform | enabling | complicated-subsystem
**Owned Bounded Contexts:** {BC-slug, BC-slug}
**Owned Services:** {SVC-slug, ...}  (if microservices)
**Cognitive-Load Budget:** {stated budget — e.g. max N contexts}
**Publishes Contracts:** {contract refs — this team's "team API"}
**Consumes Contracts:** {contract ref @ pinned version — producing team}
**Interaction Modes:**
| With Team | Mode | Notes / end condition |
|-----------|------|-----------------------|
| {TEAM-slug} | collaboration \| x-as-a-service \| facilitating | {time-box or contract ref} |
```

### Interaction Mode Entry

```
## Interaction: {TEAM-a} ↔ {TEAM-b}

**Mode:** collaboration | x-as-a-service | facilitating
**Direction:** {a consumes b | mutual}
**Sanctioned Coupling:** {contract ref — for x-as-a-service}
**End Condition:** {for collaboration/facilitating — when it ends}
```

### Team ↔ Context ↔ Service Registry (machine-readable block)

```
## Team-Context Registry

| TEAM | Owns BC | Owns SVC | Publishes | Consumes |
|------|---------|----------|-----------|----------|
| TEAM-{slug} | BC-{slug} | SVC-{slug} | {contract} | {contract@version} |
```
