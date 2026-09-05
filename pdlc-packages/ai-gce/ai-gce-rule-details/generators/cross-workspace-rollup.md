<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Cross-Workspace Roll-Up — Derivation Logic (Multi-Workspace Only)

## Purpose

In a per-team set, read each Layer-3 team workspace *down* and aggregate its compliance, drift, and contract-conformance into the **Layer-2 control plane** so the architects/owners see and govern the whole set from one place — without entering any individual workspace. This is the "maximum management from Layer 2" surface (design §5, Half 1).

**Output:** `{project_root}/{slug}-management/rollup/` — `compliance-rollup.md`, `drift-rollup.md`, `contract-conformance.md`.

**Condition:** Runs ONLY when a Layer-2 `workspace-set-manifest.yaml` is present (`workspaceTopology ∈ {per-team, hybrid}`). In a single workspace, GCE governs locally as today — no roll-up.

**Tier:** 2 (needs multiple contributors / multiple member workspaces).

> **Layer discipline (one-way):** GCE reads each L3 workspace *down* and writes the roll-up into the **L2** `rollup/` area. Each L3 workspace also self-governs locally (GOV-TT-001..007). Authority + visibility stay in L2; **no governance workspace lives in L3**; L3 never reaches up.

---

## MANDATORY: Stage Sub-Role — Team Topology Architect + Audit Specialist

Team Topology Architect (`#persona-subrole-team-topology-architect` — the ENFORCE half: is L3 development true to the designed topology?) layered with Audit Specialist (evidence, roll-up scoring). ADDS a dimension — does NOT replace the primary Compliance/Governance role.

### Behavioral Shifts
- Aggregate, never recompute per-workspace detail — each member self-governs; the roll-up summarizes across members.
- Surface set-level violations (GOV-TT-008/009/010) that no single workspace can see on its own.
- Present the whole set to the architect as one pane; drill-down links resolve to each member's local evidence.

### Anti-Patterns
- Do NOT write governance artifacts into an L3 workspace (roll-up is L2-only).
- Do NOT duplicate a member's local compliance log — reference it; aggregate the summary.
- Do NOT run when there is no set-manifest (single workspace = local governance only).

---

## Source Files

| File | What to Extract |
|------|----------------|
| `workspace-set-manifest.yaml` (L2) | Member list, per-member governance home (folder path or repo URL via `physicalLayout`), interactions, contract ownership |
| Each member's `.governance/compliance-log/` (read-down) | Per-member compliance events + score |
| Each member's `.governance/drift-register.md` (read-down) | Per-member drift entries |
| `contracts/registry.yaml` (L2) | Contract owners + versions + compatibility policy — for conformance |

---

## Generated Roll-Up Artifacts

### `rollup/compliance-rollup.md`
Per-member compliance score + tier + open violations, aggregated to a set-level view:

```markdown
# Compliance Roll-Up — {projectId}
| Member (TEAM) | Tier | Compliance % | Open Violations | GOV-TT set-level | Last Read |
|---------------|:----:|:-----------:|:---------------:|------------------|-----------|
| TEAM-{slug} | {1/2/3} | {%} | {n} | {008/009/010 flags} | {ISO} |
- Set health: {green | amber | red}   ← worst-member or weighted
```

### `rollup/drift-rollup.md`
Per-member drift entries aggregated; cross-workspace drift (a contract change in one member affecting consumers) highlighted.

### `rollup/contract-conformance.md`
For each contract in the L2 registry: producer version vs. each consumer's pinned version; flag GOV-TT-008 breaches (a producer published a breaking version without satisfying the compatibility policy) and version-skew (a consumer pinned to a retired version).

---

## Rules

### Rule 1: Aggregate, Don't Recompute
Each member self-governs (GOV-TT-001..007 locally). The roll-up aggregates member summaries + adds the set-level checks (GOV-TT-008/009/010) that only the set view can see.

### Rule 2: L2-Only Output
All roll-up artifacts are written to `{slug}-management/rollup/` (L2). Never into an L3 workspace.

### Rule 3: Read Down, Never Up
GCE reads each member's `.governance/` down (folder path or repo URL from the set-manifest). Members never push up; L2 pulls.

### Rule 4: Mode-Transparent (Q-D6)
Identical logic in subfolder (iterate member folders) and polyrepo (iterate member repos). `physicalLayout` only resolves the member's governance-home locator.

### Rule 5: Contract Conformance Is Set-Level
GOV-TT-008 breaches are visible only by comparing a producer's published version against every consumer's pinned version across the set — this is the roll-up's unique value.

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| No set-manifest (single workspace) | Do not run — local governance only |
| A member unreachable (polyrepo repo down) | Mark "member unreachable — roll-up stale for {TEAM}"; aggregate the rest |
| A member not yet governed (GCE not activated there) | Show "not yet governed"; do not treat as a violation |
| Contract with no consumers | Conformance = trivially OK (no version skew possible) |

---

## Output Validation

- [ ] Runs only when a Layer-2 `workspace-set-manifest.yaml` is present
- [ ] `rollup/compliance-rollup.md`, `drift-rollup.md`, `contract-conformance.md` written to `{slug}-management/rollup/` (L2)
- [ ] Every member in the set-manifest has a row (or an explicit unreachable/not-governed note)
- [ ] GOV-TT-008/009/010 set-level flags surfaced
- [ ] No roll-up artifact written into any L3 workspace
- [ ] Identical logic in subfolder + polyrepo (path/URL resolution only)

---

*Generated by AI-GCE · AIFLC PDLC Family · © Mohammad Maheri · https://github.com/mbmd/AIFLC*
