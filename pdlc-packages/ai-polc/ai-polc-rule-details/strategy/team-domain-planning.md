<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Team-Domain Planning Artifacts — Derivation Rules

**Phase:** Strategy (post-gate enrichment at Stages 5 and 7)
**Purpose:** Derive 4 purpose-built planning-view artifacts from existing epic files and `polc-state.md` — giving the PO single-glance answers to team load, domain topology, release rationale, and capacity fit without new elicitation.

---

## Overview

| Artifact | Generated At | Requires |
|----------|:------------:|----------|
| `team-epic-distribution.md` | Stage 5 post-gate | depth >= Standard; 2+ teams |
| `domain-topology-map.md` | Stage 5 post-gate | depth >= Standard; epic BC fields populated |
| `release-relevance-grouping.md` | Stage 7 post-gate | depth >= Standard; 2+ releases |
| `capacity-planning-matrix.md` | Stage 7 post-gate + Stage 14 | depth >= Standard; Velocity Model section present in `polc-state.md` |

**Core rule:** These artifacts are **derived, not elicited** — all data comes from existing epic files, `polc-state.md`, `release-plan.md`, `roadmap.md`, and `prioritization-register.md`. Do NOT ask the user new questions to populate them (no Q-nn blocks). If a data source is absent, skip that artifact or produce a partial version — never prompt for the missing data.

---

## Depth Adaptation

| Depth | Artifacts Generated | What-If Scenarios | Sprint Allocation | Mermaid Diagrams |
|-------|:-------------------:|:-----------------:|:-----------------:|:----------------:|
| **Minimal** | None (skip entirely) | — | — | — |
| **Standard** | All 4 (capacity-matrix requires velocity model) | No | No | Yes (2 per artifact) |
| **Comprehensive** | All 4 | Yes (3-5 scenarios) | Yes (next release) | Yes (expanded set) |

---

## Tier 2 Richness Branching (domain-topology-map)

The richness of `domain-topology-map.md` depends on the Tier 2 state at derivation time:

| Tier 2 State | Available Data | domain-topology-map Content |
|:------------:|----------------|----------------------------|
| **OFF** (default) | Epic → `Bounded Context` field (basic name) | Team-to-BC ownership table + basic domain classification. No event topology, no coupling analysis, no gravitational centers. |
| **ON** | Epic → full `DDD Alignment` section (domain type, integration events, producers/consumers) | Full content: domain classification (Core/Supporting/Generic) + event-flow topology (producer/consumer tables, tiered by fanout) + cross-team integration seams + gravitational-center analysis + coupling-risk assessment. |

**Rule:** Generate whatever is available — never block derivation because Tier 2 is off. A basic BC-to-team map is still useful for load distribution and release planning even without event detail.

---

## Derivation Rules

### Rule 1: Team Extraction

For each epic file in `epics/EPIC-NNN_*.md`:
- Read `Owning Team` field → primary assignment
- Read `Secondary Domains` or `Co-Owner` field → shared ownership (if present)
- Read `Story Points` or `Size` field → SP value (map S=3, M=5, L=8, XL=13 if textual sizing)
- Read `Release` field → release assignment
- Read `Bounded Context` field → BC assignment

### Rule 2: Domain Classification (Tier 2 ON only)

From each epic's `DDD Alignment` section:
- `Domain Type: Core` → competitive differentiator (revenue-linked)
- `Domain Type: Supporting` → essential but not differentiating
- `Domain Type: Generic` → platform/shared kernel (buy/reuse candidate)

When Tier 2 is OFF, attempt classification by heuristic:
- Epics with revenue/value metrics in AC → likely Core
- Epics serving multiple other epics → likely Generic/Platform
- Remainder → Supporting (default)

### Rule 3: Event Topology (Tier 2 ON only)

From each epic's `DDD Alignment > Integration` section:
- Parse `Publishes:` → producer events (event name + consuming BCs)
- Parse `Subscribes:` → consumer events (event name + producing BC)
- Compute fanout tier: Tier 1 (3+ consumers), Tier 2 (2 consumers), Tier 3 (1 consumer)
- Identify gravitational centers: BCs with highest total (published + consumed) event count

### Rule 4: Capacity Calculation

From `polc-state.md` → `## Velocity Model` section:
- Extract per-team velocity (SP/sprint). When the Delivery Method Profile records an **AI method**, extract BOTH the **baseline** (manual) and the **effective** (AI-adjusted = baseline × the team's blended multiplier) velocity; for **manual**, only the baseline.
- Extract sprint horizon from `release-plan.md` (sprints per release)
- Calculate: `capacity = velocity × sprints` — per track (baseline and, when present, effective)
- Calculate: `utilization = committed_SP / capacity × 100` — per track
- Flag: >80% = overloaded warning; <30% = underutilized warning
- **Dual render:** when an AI method is set, `capacity-planning-matrix.md` shows both tracks (manual baseline vs chosen method); the effective velocity's multiplier comes from `strategy/delivery-method-timing.md`.

**Graceful skip:** If the Velocity Model section does not exist in `polc-state.md`, do NOT generate `capacity-planning-matrix.md`. Generate the other 3 artifacts only.

### Rule 5: Release Relevance

For each release in `release-plan.md`:
- Collect all epics assigned to that release
- Extract inter-epic dependencies (from Integration sections or explicit `Depends On` fields)
- Compute build order (topological sort of dependencies within the release)
- Identify cross-release dependencies (epic depends on a prior-release epic)
- Derive functional theme from the combination of BCs and strategic themes

### Rule 6: Reference Linking

Per `reference-linking.md`:
- Epic IDs (EPIC-NNN) → clickable relative link to `epics/EPIC-NNN_*.md`
- Release names → link to the release's section in `release-plan.md` (via `<a id>` anchor)
- Team names → consistent naming (use exact string from epic files)

---

## Cascade Update Rule

**Trigger events:** Any of:
1. Epic added, removed, or team reassignment
2. Epic SP re-estimated
3. Release plan changed (epic moved between releases, release added/removed)
4. Velocity model updated (team velocity, delivery model, multiplier)
5. Tier 2 activated (domain-topology-map should be re-derived with richer data)

**Cascade sequence:**
1. Re-derive all 4 planning artifacts from current source data
2. Update `roadmap.md` Gantt/horizons if dates changed
3. Update `release-plan.md` sprint allocations if capacity changed
4. Update `polc-state.md` → Planning Artifacts section (mark as `generated`, refresh timestamp)
5. Log: `POLC-C-NNN: Planning artifacts re-derived. Trigger: {event}. Affected: {list}.`

> **Unification with the delivery-method velocity model:** The delivery-method velocity-model cascade (`strategy/delivery-method-timing.md`) and this cascade are the SAME mechanism — implement once, not twice. The trigger "velocity model updated" covers both sources.

**Staleness detection:** At Stage 14 entry, compare `Planning Artifacts > Last Derived` timestamp against the most recent modification of any epic file, `release-plan.md`, or `polc-state.md` Velocity Model. If source is newer → mark artifacts as `stale` and offer re-derivation: *"Planning artifacts are stale (source data changed since {date}). Re-derive now? (recommended)"*

---

## Visualization Pack (depth-gated)

### team-epic-distribution.md

| Depth | Diagram | Mermaid type | Source |
|-------|---------|:------------:|--------|
| Standard | Team load distribution | `pie` | Overview table SP totals |
| Standard | Shared-epic ownership graph | `graph LR` | Shared epics co-owner relationships |
| Comprehensive | Load-over-time (by release) | `xychart-beta` | Per-team SP by release |

### domain-topology-map.md

| Depth | Diagram | Mermaid type | Source |
|-------|---------|:------------:|--------|
| Standard | Domain cluster topology | `graph TB` | BC classification + team ownership |
| Standard | High-fanout event flow (Tier 2 only) | `graph LR` | Tier 1 producers → consumers |
| Comprehensive | Full integration topology | `graph LR` | All event flows across all tiers |

### release-relevance-grouping.md

| Depth | Diagram | Mermaid type | Source |
|-------|---------|:------------:|--------|
| Standard | Release timeline | `gantt` | Release dates + epic durations |
| Standard | Cross-release dependency graph | `graph TD` | Inter-release epic dependencies |
| Comprehensive | Alternative grouping comparison | `graph LR` | Descoping scenario visualization |

### capacity-planning-matrix.md

| Depth | Diagram | Mermaid type | Source |
|-------|---------|:------------:|--------|
| Standard | Demand vs. capacity per team | `pie` | Team utilization percentages |
| Standard | Team-activity timeline | `gantt` | Sprint allocation by team |
| Comprehensive | Bottleneck risk map | `quadrantChart` | Teams plotted by utilization × dependency-count |
| Comprehensive | What-if scenario comparison | `pie` | Before/after utilization per scenario |

---

## What-If Scenarios (Comprehensive depth only)

Generate 3-5 what-if scenarios covering these archetypes:

1. **Pull-forward:** Move an epic from a later release into the next release
2. **Defer:** Remove an epic from the next release to a later one
3. **Velocity disappointment:** Team delivers 20% less than projected
4. **Team augmentation:** Add capacity to the bottleneck team
5. **Merge releases:** Combine two small releases into one

For each scenario, state:
- Impact on affected team(s): utilization change (X% → Y%)
- Feasibility: within capacity yes/no
- Dependencies satisfied: yes/no/broken
- Business impact: what the PO gains or loses

---

## PO Decision Guide Templates

Each artifact ends with a decision-guide table. Templates:

### team-epic-distribution.md — Decision Guide

| Question | How This Artifact Answers It |
|----------|------------------------------|
| Is any team overloaded? | Load Balance Analysis → teams >80% utilization |
| Can I move epic X to team Y? | Per-Team Detail → check Y's remaining capacity vs X's SP |
| Which epics need cross-team coordination? | Shared Epics table → co-owned items requiring explicit sync |
| What happens if I reprioritize? | Load Profile → shows per-release distribution; moving an epic shifts the load |
| Are teams balanced? | Overview table → compare Total SP columns across teams |

### domain-topology-map.md — Decision Guide

| Question | How This Artifact Answers It |
|----------|------------------------------|
| Which epics are tightly coupled? | Integration Topology → shared events = tight coupling |
| What must be built first? | Gravitational Centers → high-fanout producers are foundation BCs |
| Where do teams need to coordinate? | Cross-Team Integration Seams table |
| Can epic X ship independently? | Check if it consumes events from unbuilt producers |
| Which domains are competitive differentiators? | Domain Classification → Core Domains table |

### release-relevance-grouping.md — Decision Guide

| Question | How This Artifact Answers It |
|----------|------------------------------|
| Why can't we just ship epic X alone? | Dependency Chain → shows what X depends on within this release |
| What's the cost of descoping epic Y? | Descoping Options → impact + cascade effect |
| Can we split this release? | Cross-Release Dependencies → shows which epics can be isolated |
| What value does this release deliver? | Relevance Justification → business + technical rationale |
| What if a stakeholder asks "why this order?" | Functional Theme + Relevance Justification = the answer |

### capacity-planning-matrix.md — Decision Guide

| Question | How This Artifact Answers It |
|----------|------------------------------|
| Can we fit epic X in this release? | Demand vs. Capacity table → check team's remaining buffer |
| Which team is the bottleneck? | Bottleneck Analysis → highest risk-level team |
| What if we add a sprint? | What-If Scenarios → team augmentation scenario |
| Should we defer anything? | Bottleneck Analysis → mitigation options column |
| Are we overcommitted? | Release-level assessment → "requires trade-off" flag |

---

## Provenance Front-Matter (All 4 Artifacts)

Every generated planning artifact carries:

```yaml
---
generatedBy: AI-POLC
generatedVersion: 1.0.0
source: derived-from-epics-and-polc-state
generatedOn: {ISO-date}
ownership: generated
---
```

`ownership: generated` because these are fully derived (no user-authored content in the body). Re-derivation overwrites the entire file.

---

## Integration Points Summary

| When | Action | Load This File? |
|------|--------|:---------------:|
| Stage 5, Step 5.8 (post-gate) | Derive `team-epic-distribution.md` + `domain-topology-map.md` | Yes |
| Stage 7, post-gate (after Viz Pack + Gate approval) | Derive `release-relevance-grouping.md` + `capacity-planning-matrix.md` | Yes |
| Stage 14, Step 14.7 (Persist Changes) | Re-derive stale artifacts (conditional) | Yes (if staleness detected) |
| Tier 2 activation (any stage) | Re-derive `domain-topology-map.md` with full DDD data | Yes |
| Cascade trigger (velocity/date/estimate change) | Re-derive all 4 | Yes |

---

*Detail file for AI-POLC Team-Domain Planning Artifacts | Phase: Strategy (post-gate enrichment)*
