<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Tri-Input (AP + PBP + UXP) → Per-Team L3 Workspace Slices (PARTITIONING)

## Purpose

When `workspaceTopology` is `per-team` or `hybrid` (Config Gate Q4), partition the three peer inputs — Architecture Package (AP), Product Backlog Package (PBP), UX Design Package (UXP) — **by team** so each team gets its own scoped Layer-3 development workspace. This is the step that turns "one workspace with everything" into "N clean per-team workspaces," each containing only its team's slice.

**Output:** the scoped input slices consumed by each per-team workspace under `{project_root}/{slug}-workspaces/{team}/` (architecture/, backlog/, ux/, src/, CODEOWNERS, contracts/).

**Condition:** Generate IF `workspaceTopology ∈ {per-team, hybrid}` (from Q4). Otherwise SKIP entirely (single workspace = today's behavior).

**Cluster:** Multi-workspace (Layer-2 → Layer-3 partitioning). Runs before per-member workspace generation.

> **Granularity is ALWAYS team-level — never per service.** A team owns 1..N services / bounded contexts; they all stay as modules inside that team's ONE workspace. The existing services-as-modules enrichment (`mapping/extension-microservices-enrichment.md`) applies *within* each team workspace, unchanged. This partitioner sits **above** it.

---

## MANDATORY: Stage Sub-Role — Team Topology Architect + Workspace Architect

Team Topology Architect (`#persona-subrole-team-topology-architect` — owns the team→context→contract intent) layered with Workspace Architect (structure). ADDS a dimension — does NOT replace the primary DevOps/Platform Engineer role.

### Behavioral Shifts
- Slice by the **team** boundary, never finer — a team's multiple services/contexts stay together as modules in its one workspace.
- Join deterministically on the shared identity (`TEAM-*` / `BC-*`) when present; fall back to name-matching only when no identity exists.
- Never leak one team's slice into another's workspace — each L3 workspace is self-contained and scoped to exactly one team.

### Anti-Patterns
- Do NOT split at service granularity (that is a bug — the boundary is the team).
- Do NOT duplicate a shared artifact into every team as if team-owned (design-system tokens + a11y baseline are SHARED — see UX rule below).
- Do NOT invent a team not present in the ownership source.

---

## Source Inputs (join key in priority order)

| # | Source | What to Extract | Join Basis |
|:-:|--------|-----------------|------------|
| 1 | **AP `team-context-registry.md`** (team-topologies extension) | `TEAM-*` roster + team → `BC-*`/`SVC-*` assignment + produced/consumed contracts | **Authoritative** — the deterministic join key |
| 2 | AP `component-design.md` (C4 L3) | Module names/paths (`src/modules/{x}/`) → their `BC-*` | Map each module to its owning team via BC → TEAM |
| 3 | AP `CODEOWNERS` / MS-01 "Owning Team" / DDD-08 | Team-per-context ownership | Fallback join when no registry (name-based) |
| 4 | PBP `backlog/epics/*` | Epic `Owning Team` (`TEAM-*`) + child stories | Slice backlog by team |
| 5 | UXP flows / journeys / wireframes | `Owning Team`/`BC-*` tag, else persona→epic→BC | Slice UX by team; **shared** design-system/a11y excluded |

---

## Partitioning Strategy

### Step 1: Resolve the team set
- If `team-context-registry.md` present → the `TEAM-*` roster IS the team set (authoritative).
- Else → derive the team set from CODEOWNERS / MS-01 "Owning Team" / DDD-08 team-per-context (name-based).
- If one team owns everything, or no team data → **abort partition**, fall back to single workspace (Q4 should not have offered per-team; defensive).

### Step 2: Assign each artifact to a team
For each team `TEAM-{slug}`:
- **architecture/** — the AP slice for its owned `BC-*`/`SVC-*`: the component-design modules, the ADRs/constraints scoped to those contexts, its section of the container diagram.
- **backlog/** — epics whose `Owning Team` = this team (+ their stories, traceability rows, prioritization rows).
- **ux/** — flows/journeys/wireframes tagged (or derived via persona→epic→BC) to this team's `BC-*`.
- **src/** — the module structure for its owned modules (1..N services as modules within — services-as-modules enrichment applies here, unchanged).
- **CODEOWNERS** — this team only.
- **contracts/** — a READ-ONLY, version-pinned copy of the contracts it **produces** + **consumes** (from the L2 authoritative registry; see `mapping/contract-registry-generation.md`).

### Step 3: Handle shared artifacts (NOT team-scoped)
- **Design-system tokens + the accessibility baseline are SHARED** — copied to every team workspace identically (a team never owns half the design system).
- **Canonical `rules/`** — byte-identical across teams (guardrail uniformity by construction; per-team scoped rules layer on top, never replace — see `reconciliation/guardrail-sync.md`).
- **Cross-cutting ADRs / global constraints** — included in every team's `architecture/` global section.

### Step 4: Emit the per-team slice
Each team's scoped inputs feed the existing single-workspace generator (run once per team, scoped) — see `flows/full-generation.md` invoked per member. The result is exactly today's single-workspace shape, scoped to one team, plus a `TEAM_CHARTER.md` (`mapping/team-charter-generation.md`) and a team-scoped relevance map (`mapping/relevance-map-generation.md`).

---

## Transformation Rules

### Rule 1: Team-Granular Split Only
The partition boundary is the team. A team's 1..N services/contexts stay as modules within its one workspace. NEVER split per service.

### Rule 2: Deterministic Join When Identity Present
When `team-context-registry.md` exists, join on `TEAM-*`/`BC-*` (deterministic). Only fall back to name-matching when no registry exists.

### Rule 3: No Cross-Team Leakage
Each L3 workspace contains only its team's slice. No other team's epics, flows, or modules appear.

### Rule 4: Shared Artifacts Stay Shared
Design-system tokens, a11y baseline, canonical `rules/`, and global ADRs/constraints go to every team identically — never carved up per team.

### Rule 5: Contract-Only Cross-Team Coupling
A team's `contracts/` is a read-only, version-pinned copy of what it produces + consumes. Cross-team dependency is via published contracts only (never another team's source).

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| `workspaceTopology: single` | SKIP — this file does not run |
| No `team-context-registry.md`, CODEOWNERS present | Name-based team partition from CODEOWNERS / MS-01 |
| One team owns everything | Fall back to single workspace (defensive; Q4 should not have offered per-team) |
| Untagged UX unit | Derive team via persona → epic → `BC-*`/`TEAM-*` (UXD fallback) |
| POLC/UXD absent | Partition the architecture-only slice per team (degrades gracefully — architecture + src + CODEOWNERS still split) |
| Hybrid topology | Keep the monorepo core; extract only the teams that justify isolation |

---

## Output Validation

- [ ] Runs only when `workspaceTopology ∈ {per-team, hybrid}`
- [ ] Team set resolved from the registry (authoritative) or CODEOWNERS/MS-01/DDD-08 (fallback)
- [ ] Each team's architecture/backlog/ux/src/CODEOWNERS slice is complete and non-overlapping
- [ ] Shared design-system tokens + a11y baseline copied to every team (not carved up)
- [ ] Each team's `contracts/` is a read-only pinned copy of produced + consumed contracts
- [ ] No cross-team leakage; split is team-granular (never per-service)
- [ ] Downstream: per-member generation + `TEAM_CHARTER.md` + team-scoped relevance map produced

---

*Generated by AI-DWG · AIFLC PDLC Family · © Mohammad Maheri · https://github.com/mbmd/AIFLC*
