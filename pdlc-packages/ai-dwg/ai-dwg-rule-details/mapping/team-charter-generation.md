<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Team Assignment → TEAM_CHARTER.md (per-team scope statement)

## Purpose

Generate a `TEAM_CHARTER.md` at the root of each Layer-3 per-team workspace — the one file a team reads first that states, in one place, **what it owns and what it must move**: its owned bounded contexts/services, the contracts it produces, the contracts it consumes (pinned version + producing team), its interaction modes, and its team type. This is how each team becomes "aware of what it needs to move" without reading the whole set.

**Output:** `{project_root}/{slug}-workspaces/{team}/TEAM_CHARTER.md`

**Condition:** Generate IF `workspaceTopology ∈ {per-team, hybrid}` (Config Gate Q4), one per team member. SKIP for `single`.

**Cluster:** Multi-workspace (per-member, Layer-3). Runs during per-team generation.

---

## MANDATORY: Stage Sub-Role — Team Topology Architect + Workspace Architect

Team Topology Architect (`#persona-subrole-team-topology-architect` — the team's scope + seams) layered with Workspace Architect (day-1 clarity). ADDS a dimension — does NOT replace the primary role.

### Behavioral Shifts
- State the team's scope so a developer joining this workspace understands ownership + seams in one read.
- Make the contracts the team produces vs. consumes explicit (with pinned versions + producing teams).
- Keep it to the team's own slice — no cross-workspace bookkeeping (that lives in the L2 control plane).

### Anti-Patterns
- Do NOT restate the whole set (that is the L2 `WORKSPACE_SET_CONTEXT_MAP.md`).
- Do NOT list contracts the team neither produces nor consumes.
- Do NOT invent ownership not in the team-context-registry.

---

## Source Inputs

| Source | What to Extract | Used For |
|--------|-----------------|----------|
| AP `team-context-registry.md` | This team's `TEAM-*`, type, owned `BC-*`/`SVC-*`, produces/consumes contracts | The charter body |
| AP `team-topology-map.md` | This team's interaction modes (TT-03) | Interaction section |
| L2 `contracts/registry.yaml` | Pinned versions + producing team of each consumed contract | Consumed-contracts table |

---

## Target Structure: TEAM_CHARTER.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "team-context-registry.md + team-topology-map.md + contracts/registry.yaml"
generatedOn: "{ISO-date}"
ownership: generated
projectId: "{project-id}"
team: "TEAM-{slug}"
---

# Team Charter: TEAM-{slug}

## Team Type
{stream-aligned | platform | enabling | complicated-subsystem} — {one line: why this type}

## What This Team Owns
- **Bounded Contexts:** {BC-slug, BC-slug}
- **Services:** {SVC-slug, ... or n/a}
- **Modules (in `src/`):** {module paths — the team's 1..N services as modules within this workspace}

## Contracts This Team PUBLISHES (its "team API")
| Contract | Format | Version | Compatibility Policy |
|----------|--------|---------|----------------------|
| {contract ref} | {openapi/asyncapi/json-schema} | {semver} | {backward/forward/full} |

## Contracts This Team CONSUMES
| Contract | Producing Team | Pinned Version | Local (read-only) copy |
|----------|----------------|----------------|------------------------|
| {contract ref} | TEAM-{slug} | @{semver} | `contracts/{...}` |

## Interaction Modes
| With Team | Mode | Notes / end condition |
|-----------|------|-----------------------|
| TEAM-{slug} | collaboration \| x-as-a-service \| facilitating | {time-box or contract ref} |

## What This Team Must Move
{Plain-language summary: the slice of the product this team is accountable for delivering —
its contexts, the contracts it must publish for others, and the ones it depends on. This is
the team's mandate in the wider set. Cross-workspace status/governance lives in the L2 control
plane (`{slug}-management/`), not here.}
```

---

## Transformation Rules

### Rule 1: One Charter Per Team
Exactly one `TEAM_CHARTER.md` at each L3 workspace root. It is the first file a team reads.

### Rule 2: Produced vs. Consumed Are Explicit
Publishes = the contracts this team owns (editable only at the L2 source). Consumes = pinned-version contracts owned by other teams (local copy is read-only).

### Rule 3: Team's Own Slice Only
The charter covers only this team's scope + seams. The set-wide view is the L2 `WORKSPACE_SET_CONTEXT_MAP.md`.

### Rule 4: Interaction Modes From the Topology Map
Each interaction row names exactly one mode (TT-03), sourced from `team-topology-map.md`.

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| `workspaceTopology: single` | SKIP — no per-team charter in a single workspace |
| No `team-context-registry.md` (CODEOWNERS fallback) | Populate ownership from CODEOWNERS/MS-01; contracts section best-effort from `contracts/` ownership |
| Platform team | teamType: platform; "publishes" lists the platform capabilities offered X-as-a-Service |
| Team consumes nothing | Consumed-contracts table shows "none — self-contained" |

---

## Output Validation

- [ ] Runs only when `workspaceTopology ∈ {per-team, hybrid}`
- [ ] One `TEAM_CHARTER.md` at each L3 workspace root
- [ ] Owned `BC-*`/`SVC-*` + modules listed
- [ ] Publishes table (with compatibility policy) + Consumes table (with producing team + pinned version) present
- [ ] Interaction modes sourced from `team-topology-map.md` (one mode per row)
- [ ] "What This Team Must Move" summary present; no cross-workspace bookkeeping in the charter
- [ ] Provenance front-matter + projectId + team stamped

---

*Generated by AI-DWG · AIFLC PDLC Family · © Mohammad Maheri · https://github.com/mbmd/AIFLC*
