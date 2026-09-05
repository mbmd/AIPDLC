<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Team Topology — Derivation Logic

## Purpose

Derives team topology governance rules (GOV-TT-*) from `module-structure.md` and `CODEOWNERS`. Ensures module ownership boundaries, cognitive load limits, and independent deployability are maintained.

**Multi-workspace awareness (per-team topology).** When the workspace is part of a per-team set — detected via the Layer-2 `workspace-set-manifest.yaml` (`workspaceTopology ∈ {per-team, hybrid}`) — this generator ALSO derives **set-level** rules (GOV-TT-008/009/010) that keep the isolated per-team workspaces honest: contract-compatibility gating, no cross-workspace source coupling, and interaction-mode conformance. In a single workspace, only GOV-TT-001..007 apply (today's behavior, unchanged).

---

## MANDATORY: Stage Sub-Role — Team Topology Architect

During THIS activity, ALSO adopt the mindset of a **Team Topology Architect** (`#persona-subrole-team-topology-architect`). This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC Engineer) — it ADDS a thinking dimension. This is the **ENFORCE** half of the sub-role's dual mandate: the same voice that designed the topology in AI-ADLC (DEFINE) now governs that L3 development stays true to it. *(This sub-role replaces the former Change Manager here, so DEFINE and ENFORCE speak with one organizational-design voice — Q-D4.)*

### Behavioral Shifts
- Think in organizational boundaries: team topology rules ensure that module ownership, cognitive load, and deployment independence align with team structure
- Evaluate ownership from CODEOWNERS: one bounded context must have exactly one owning team — shared ownership creates coordination overhead
- Enforce cognitive load limits: no team should own more than 2-3 modules (beyond that, context switching degrades quality)
- Consider backward compatibility obligations: platform/shared-kernel changes affect ALL consuming teams
- Ensure independent deployability: circular dependencies between modules prevent independent team release cadence

### Anti-Patterns for This Activity
- Do NOT generate team topology rules without CODEOWNERS (ownership rules need ownership data)
- Do NOT conflate team topology (GOV-TT-*) with role isolation (GOV-ROLE-*): TT is about TEAM boundaries, ROLE is about INDIVIDUAL duties
- Do NOT create rules that assume specific organizational structures — derive from what CODEOWNERS and module-structure actually state

### Quality Check
A good output from this activity sounds like:
- "GOV-TT-001: Each bounded context owned by exactly one team. Derived from CODEOWNERS: `src/Modules/Finance/** @finance-team`. No shared ownership detected."
- "GOV-TT-005: Cognitive load limit: max 2-3 modules per team. CODEOWNERS shows @platform-team owns 4 module paths → flagging for team lead review."

---

## Source Files

| File | What to Extract |
|------|----------------|
| `module-structure.md` | Module list, module ownership statements, dependency rules |
| `CODEOWNERS` | Module → team mapping (who owns what) |
| `role-isolation.md` | Team size (used for cognitive load rules) |
| `workspace-set-manifest.yaml` (L2 — multi-workspace only) | Member set, per-team owned contexts/services, `publishes`/`consumes` contracts (@version), `interactions[]` modes — drives GOV-TT-008/009/010 |
| `contracts/registry.yaml` (L2 — multi-workspace only) | Contract owners + compatibility policy — drives GOV-TT-008 |

---

## Generated Rules

| Rule ID | Statement | Derived From |
|---------|-----------|-------------|
| GOV-TT-001 | Each bounded context owned by exactly one team | CODEOWNERS: one team per module path |
| GOV-TT-002 | Cross-context communication via events/APIs only — no direct class references | module-structure.md dependency rules |
| GOV-TT-003 | Platform/shared kernel changes MUST be backward-compatible | module-structure.md shared kernel section |
| GOV-TT-004 | Stream teams can deploy independently (no circular dependencies). **In a per-team set: independent deployability spans workspaces — no source-level dependency across member workspaces, only contract dependencies.** | module-structure.md dependency graph + (multi-ws) workspace-set-manifest.yaml |
| GOV-TT-005 | Cognitive load limit: max 2-3 modules per team | CODEOWNERS ownership count per team |
| GOV-TT-006 | API contracts owned by producing team. **In a per-team set: a team may edit only the contracts it OWNS in the L2 registry** (consumed contracts are read-only pinned copies). | CODEOWNERS: contracts/ path ownership + (multi-ws) contracts/registry.yaml owners |
| GOV-TT-007 | Steering file ownership documented and enforced | CODEOWNERS: rules/ entries |
| **GOV-TT-008** (new — multi-workspace) | **Contract-compatibility gate** — a producing team cannot publish a breaking contract version without satisfying the declared compatibility policy (backward/forward/full); consumers pin versions. | contracts/registry.yaml `compatibilityPolicy` + MS-06/MS-10 (when microservices active) |
| **GOV-TT-009** (new — multi-workspace) | **No cross-workspace source import** — coupling between member workspaces is only via published contracts (the point of isolation); no member imports another member's source. | workspace-set-manifest.yaml members + each member's dependency graph |
| **GOV-TT-010** (new — multi-workspace) | **Interaction-mode conformance** — flag when an observed dependency violates the designed interaction mode (e.g. a permanent "collaboration" where an X-as-a-Service was designed, or a supposedly-temporary "facilitating" enabling team that has become a permanent runtime dependency). | workspace-set-manifest.yaml `interactions[]` (from TT-03 / team-topology-map.md) |

> **GOV-TT-008/009/010 are set-level rules — derived ONLY when a Layer-2 `workspace-set-manifest.yaml` is present** (`workspaceTopology ∈ {per-team, hybrid}`). In a single workspace they are N/A (not violations). They realize the design's isolation guarantees: contract-first is the only sanctioned coupling across the isolation boundary (MS-06 / MS-10 / DDD-12).

---

## Cross-Workspace Enforcement (multi-workspace only)

When a set-manifest is present, GOV-TT-008/009/010 are enforced at the **set level** and rolled up into the Layer-2 control plane. Authority sits in L2; GCE reads each L3 workspace *down* and writes the cross-workspace roll-up into `{slug}-management/rollup/` — see `generators/cross-workspace-rollup.md`. Each L3 workspace also self-governs locally (GOV-TT-001..007) as today. **No governance workspace lives in L3** (one-way boundary). Change detection per member is `generators/l3-change-detection.md` (Q-D3).

**Mode-transparent (Q-D6):** GCE governs via the set-manifest identically in subfolder mode (one GCE instance iterating members) and polyrepo mode (one GCE per member repo + the L2 roll-up). It reads `physicalLayout` only to resolve each member's governance home (folder path vs repo URL) — it never branches on mode beyond path resolution.

---

## Hook: `module-boundary-check.json`

Same hook as module-boundary-generator — shared enforcement. GOV-TT-002 and MOD-03 are verified together (both check cross-module references). GOV-TT-009 (no cross-workspace source import) extends the same boundary check across member workspaces when a set-manifest is present.

## Tier: 2 (team topology enforcement needs multiple contributors — Tier 2 readiness criterion)
