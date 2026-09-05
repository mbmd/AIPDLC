<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Flow: Build the Layer-2 Workspace-Set Control Plane

## Purpose

Orchestrate the construction of the **Layer-2 control plane** for a multi-workspace generation and the generation of the **N Layer-3 per-team workspaces** below it. This flow is the L2→L3 hinge: it produces the two clearly separated things the owner asked for — a control plane the architects/owners keep in the design workspace, and a set of clean, consistent per-team dev workspaces pushed down.

**When:** During Mode-1 Full Generation (and Mode-2 delta) when `workspaceTopology ∈ {per-team, hybrid}` (Config Gate Q4). SKIP for `single` — the existing single-workspace flow runs unchanged.

**Design principle (owner's two requirements):** (1) **maximum management from Layer 2** — the set-manifest, authoritative contract registry, and roll-up all live in the L2 control plane; (2) **very clear, consistent Layer-3 workspaces** — each L3 workspace is today's proven single-workspace shape, scoped to one team, self-contained, no orchestration clutter.

> **Layer discipline (LAYERED_TOPOLOGY §1.1):** L2 generates the L3 workspaces + pushes guardrails/contracts down + reads L3 status down for control; L3 never reaches up. No orchestration/registry/roll-up artifact ever lives inside an L3 workspace.

---

## MANDATORY: Stage Sub-Role — Team Topology Architect + Workspace Architect

Team Topology Architect (`#persona-subrole-team-topology-architect`) layered with Workspace Architect. ADDS a dimension — does NOT replace the primary DevOps/Platform Engineer role.

---

## The Two Layers This Flow Produces

### (1) Layer-2 control plane — `{project_root}/{slug}-management/` (stays with architects/owners)

```
{project_root}/{slug}-management/                 ← LAYER 2 — control plane
├── workspace-set-manifest.yaml                   ← baseline/workspace-set-manifest-generation.md
├── contracts/                                    ← mapping/contract-registry-generation.md (AUTHORITATIVE)
│   ├── registry.yaml
│   └── {svc}/ openapi.yaml · asyncapi.yaml · events/*.schema.json
├── team-topology-map.md                          ← from AI-ADLC (copied in)
├── WORKSPACE_SET_CONTEXT_MAP.md                  ← human single-pane index across all L3 workspaces
└── rollup/                                        ← scaffold; AI-GCE/AI-DFE populate (read L3 down)
    ├── compliance-rollup.md · drift-rollup.md · contract-conformance.md
```

### (2) Layer-3 per-team workspaces — `{project_root}/{slug}-workspaces/{team}/` (pushed down, clean)

```
{project_root}/{slug}-workspaces/{team}/           ← LAYER 3 — one clean workspace per team
├── TEAM_CHARTER.md      ← mapping/team-charter-generation.md
├── rules/               ← canonical guardrails (IDENTICAL across teams) + this team's scoped rules
│   └── relevance-map.md (team-scoped)
├── backlog/             ← this team's epics/stories (sliced by TEAM-*)
├── ux/                  ← this team's flows/screens (sliced by BC-*/TEAM-*; design-system + a11y SHARED)
├── architecture/        ← this team's slice of the AP
├── src/                 ← this team's 1..N services/contexts as modules
├── contracts/           ← READ-ONLY pinned copy (produced + consumed)
├── CODEOWNERS           ← this team only
└── .governance/workspace-manifest.yaml            ← the existing per-member manifest (+ setMembership back-pointer)
```

**Elegant reuse:** each L3 workspace is *exactly today's single-workspace output*, scoped to one team's slice. Multi-workspace = "run the existing generator N times (scoped by the partition) + build the L2 control plane above them." No rewrite of the core generator — a partition step in front + an L2 set-assembly step after.

---

## Execution Sequence

1. **Partition** the tri-input by team — `mapping/team-workspace-partitioning.md` (team-granular; deterministic join on `TEAM-*` when the registry is present).
2. **Generate each L3 workspace** — run the existing `flows/full-generation.md` once per team member, scoped to that team's slice. Produces today's single-workspace shape + `TEAM_CHARTER.md` (`mapping/team-charter-generation.md`) + team-scoped `relevance-map.md` + the per-member manifest with a `setMembership` back-pointer.
3. **Build the L2 authoritative contract registry** — `mapping/contract-registry-generation.md` (registry in L2; read-only pinned copies pushed into each L3 `contracts/`).
4. **Build the L2 set-manifest** — `baseline/workspace-set-manifest-generation.md` (authoritative index of all members).
5. **Copy the Team Topology Map** into the control plane + **generate `WORKSPACE_SET_CONTEXT_MAP.md`** (the human single-pane index across the set).
6. **Scaffold `rollup/`** — empty compliance/drift/contract-conformance files that AI-GCE/AI-DFE populate by reading each L3 workspace *down* (Phase 4/5).
7. **Establish guardrail distribution** — `reconciliation/guardrail-sync.md` seeds the canonical guardrail set as the single L2 source; every L3 `rules/` is generated FROM it (byte-identical), version-stamped.

---

## Modes

- **Mode 1 — Full Generation:** build the L2 control plane + generate the N L3 workspaces (full sequence above).
- **Mode 2 — Delta Reconciliation:** when a team boundary or contract changes, re-scope + re-baseline only the affected L3 workspaces; regenerate the L2 set-manifest + registry; re-run guardrail-sync for changed guardrails.
- **Mode 3 — Brownfield:** register existing repos as L3 members under a newly-built L2 control plane (no forced relocation; detect-and-adapt per existing DWG brownfield rules).

---

## Rules

1. **Two layers, cleanly separated.** Management artifacts (set-manifest, authoritative registry, roll-up, set-context-map) live in `{slug}-management/` (L2). Dev workspaces live in `{slug}-workspaces/{team}/` (L3). Never mix.
2. **L3 uniformity by construction.** Every L3 workspace has the identical single-workspace shape; canonical `rules/` are byte-identical across teams; team-specific rules layer on top.
3. **Team-granular.** One L3 workspace per team; a team's 1..N services stay as modules within.
4. **One-way boundary.** L2 pushes down + reads down; L3 never reaches up. No management artifact inside an L3 workspace.
5. **Opt-in, default-safe.** Runs only on Q4 `per-team`/`hybrid`. `single` → this flow does not run; today's behavior is unchanged.

---

## Output Validation

- [ ] `{slug}-management/` control plane built (set-manifest + authoritative contracts/registry.yaml + team-topology-map + WORKSPACE_SET_CONTEXT_MAP + rollup/ scaffold)
- [ ] N L3 per-team workspaces generated, each = single-workspace shape + TEAM_CHARTER + team-scoped relevance-map + read-only contracts/ + per-member manifest with setMembership
- [ ] Canonical `rules/` byte-identical across all L3 workspaces (guardrail-sync seeded)
- [ ] No management/roll-up/registry artifact inside any L3 workspace
- [ ] Shared design-system tokens + a11y baseline present in every L3 workspace (not carved up)
- [ ] Single-workspace path unaffected when Q4 = single

---

*Generated by AI-DWG · AIFLC PDLC Family · © Mohammad Maheri · https://github.com/mbmd/AIFLC*
