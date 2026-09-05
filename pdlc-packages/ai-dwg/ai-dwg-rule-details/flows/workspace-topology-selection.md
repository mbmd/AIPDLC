<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Flow: Workspace Topology Selection (Config Gate Q4 — Opt-In)

## Purpose

Decide whether DWG generates ONE workspace (today's default) or **N per-team workspaces** (multi-workspace), and — when multi — whether the physical layout is a monorepo-of-workspaces (subfolder) or separate repos (polyrepo). This flow owns the **Config Gate Q4** logic and its **justification gate**.

**When:** During the Config Gate (after Q1–Q3, before mode execution). Q4 is **offered only when the architecture justifies it** — otherwise it is a silent no-op and the default single workspace is used.

**Design principle (opt-in, default-safe — DWG Law 4):** the default is unchanged (single monorepo workspace). Nothing changes for existing users. Multi-workspace generation activates ONLY when the user explicitly chooses it at Q4, and Q4 only appears when the inputs justify it. Fully backward-compatible.

> **Granularity is ALWAYS team-level — never per service.** A team owns 1..N services / bounded contexts; they all stay together as modules inside that team's ONE workspace (the existing services-as-modules enrichment applies *within* each team workspace, unchanged). DWG splits **up to team level, never at service granularity.**

---

## Justification Gate — When Is Q4 Offered?

Offer Q4 **only when ALL** of the following hold:

1. **ADLC is a present peer input** (an Architecture Package exists — `adlc-state.md` detected), AND
2. **Stage-5 decomposition** (`Q-DEC-02` in the AP) ∈ {service-oriented, microservices, hybrid} — NOT a modular monolith, AND
3. **≥ 2 TEAMS with ownership data** — NOT ≥ 2 services. Team count comes from the ownership source (below).

If any condition fails → **do NOT ask Q4**; silently use the single workspace (default). This mirrors the Stage-5 "skip" no-op pattern — no prompt, no noise.

### Where team-ownership data comes from (in priority order)

| # | Source | Signal read | Split basis |
|:-:|--------|-------------|-------------|
| 1 | **`team-topologies` extension active** (AI-ADLC) | `team-context-registry.md` + `team-topology-map.md` — the `TEAM-*` roster + team→BC/SVC assignment | One workspace per **stream-aligned team** (authoritative) |
| 2 | **Team-ownership data present** (no topology extension) | MS-01 "Owning Team" / `CODEOWNERS` / DDD-08 team-per-context | One workspace per **team** derived from that mapping |
| 3 | **AI-POLC team roster** | `polc-state.md` → Planning Artifacts → Team Roster (`TEAM-*`) + epics' `Owning Team` | Corroborates the team set for slicing |
| — | **None of the above, OR one team owns everything, OR modular monolith** | — | **Single workspace, silent no-op. NEVER a per-service split.** |

---

## The Question (when offered)

```
Q4: Workspace topology?

  (a) Single workspace / monorepo              ← DEFAULT (today's behavior, unchanged)
  (b) Per-team workspaces (multi-workspace / polyrepo)
  (c) Hybrid (monorepo core + extracted team workspaces)

  Recommendation:
    • team-topologies extension ACTIVE → strongly recommend (b): one workspace per
      stream-aligned team from the Team Topology Map.
    • team-ownership data present (no extension) → offer (b) from that data.

  Sub-question (only if (b) or (c)):
    Physical layout?
      • subfolder — monorepo-of-workspaces (one repo, N workspace folders)
      • polyrepo  — separate repos (one repo per team workspace)
```

- **On (a) Single** → record `workspaceTopology: single`; proceed exactly as today. Phase-3 multi-workspace generation does not run.
- **On (b) Per-team** → record `workspaceTopology: per-team` + the chosen `physicalLayout`; hand to multi-workspace generation (`mapping/team-workspace-partitioning.md` + the L2 control-plane flow).
- **On (c) Hybrid** → record `workspaceTopology: hybrid` + `physicalLayout`; generate the monorepo core + extract the team workspaces that justify isolation.

---

## Recorded Metadata

Written to `.governance/workspace-manifest.yaml` (per-member manifest) and surfaced in the Layer-2 workspace-set manifest when multi:

```yaml
workspaceTopology: {single | per-team | hybrid}
physicalLayout: {subfolder | polyrepo}   # only meaningful when workspaceTopology ≠ single
```

---

## Rules

1. **Opt-in, default-safe.** No Q4 answer other than (a), or Q4 not offered at all → identical to today's single-workspace output.
2. **Team-granular only.** The split boundary is the **team**. Never split per service. A team's multiple services stay as modules inside its one workspace.
3. **Justified only.** Q4 appears only when ADLC is present, decomposition is service-oriented/microservices/hybrid, AND ≥ 2 teams have ownership data.
4. **Structural, not build-method.** Q4 chooses workspace isolation, not how code is built. It is independent of `buildProfile` (the governance signal) and of the two-axis `output = f(peer inputs, platform targets)` model.
5. **Graceful fallback.** With the `team-topologies` extension absent, fall back to CODEOWNERS / MS-01 / DDD-08 ownership data; with none, single workspace.

---

## Downstream

- **Multi-workspace generation** (Phase 3): `mapping/team-workspace-partitioning.md` partitions the tri-input (AP + PBP + UXP) by `TEAM-*`; `baseline/workspace-set-manifest-generation.md` builds the L2 authoritative index; `mapping/contract-registry-generation.md` + `mapping/team-charter-generation.md` complete the set.
- **Governance** (Phase 4): AI-GCE reads the set-manifest for cross-workspace GOV-TT roll-up.

See `TEAM_TOPOLOGY_WORKSPACES_DESIGN.md` §4.1 for the full design rationale.
