<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Reconciliation: Guardrail Sync — Spread Canonical Guardrails to Every L3 Workspace

## Purpose

Keep the guardrails / leads / guidelines **identical across every Layer-3 per-team workspace** in a multi-workspace set, and re-propagate them from a single Layer-2 canonical source whenever they change. This is the **downward half** of the governance-circulation loop (design §5.1): the L2 control plane holds the master guardrail set; every L3 workspace's `rules/` is generated FROM it, byte-identical; changes re-push to all members via the set-manifest.

**Output:** each member's `{slug}-workspaces/{team}/rules/` (canonical portion) + a version stamp; drift flagged in the L2 roll-up.

**Condition:** Runs when `workspaceTopology ∈ {per-team, hybrid}` (Config Gate Q4). For `single`, ordinary re-baseline applies (one workspace, nothing to spread).

**Cluster:** Multi-workspace reconciliation (Layer-2 → Layer-3 push). Mode-2 per-member pass.

> **Mode-transparent (Q-D6):** the same logic runs whether the set is `subfolder` (iterate member folders) or `polyrepo` (push per member repo). The set-manifest is the single discovery contract; only path/URL resolution differs.

---

## MANDATORY: Stage Sub-Role — Workspace Architect + Automation Engineer

Workspace Architect (guardrail structure) layered with Automation Engineer (deterministic, idempotent per-member propagation). ADDS a dimension — does NOT replace the primary role.

### Behavioral Shifts
- One canonical source of guardrails in L2 → every L3 `rules/` is a faithful copy (anti-drift by construction).
- Re-propagation is idempotent and per-member: same input → same output; a member already current is a no-op.
- Never overwrite a team's own scoped rules (marked `<!-- custom -->` or in a team-scoped section) — canonical guardrails layer, they don't replace.

### Anti-Patterns
- Do NOT let two members drift onto different guardrail versions silently — stamp + flag.
- Do NOT branch the logic on physical layout beyond resolving each member's path/URL.
- Do NOT clobber team-specific rules when re-pushing the canonical set.

---

## The Downward Loop (design §5.1 ⬇)

1. **Single canonical source in L2.** The control plane holds the master guardrail set — the canonical `rules/`, standing directives / "leads", and guidelines.
2. **Generate every member FROM it.** During per-team generation, each L3 `rules/` canonical portion is produced from this one source → **byte-identical guardrails everywhere** (anti-drift layer 1).
3. **Re-propagate on change.** When a guardrail/lead/guideline changes in L2, a guardrail-sync pass re-pushes to every member — one pass across folders in subfolder mode, a push per repo in polyrepo mode; the set-manifest drives the iteration so the logic is identical.
4. **Version stamp.** Each member's guardrails carry a `guardrailVersion`; the L2 roll-up flags any member left on a stale version (no silent divergence).

```
   L2 canonical guardrails ──generate/push──▶ every L3 rules/ (byte-identical)
        │                                            │
        └──── on change: re-push (per-member) ───────┘   version-stamp + stale-flag
```

> The **upward half** (GCE detect+report, AI-DFE digest, L2 packages refine) is design §5.1 ⬆ — implemented in Phase 4/5 (AI-GCE `l3-change-detection`, cross-workspace roll-up). This file owns only the downward spread.

---

## Transformation Rules

### Rule 1: Single Canonical Source
The master guardrail set lives once in the L2 control plane. Members never author canonical guardrails locally.

### Rule 2: Byte-Identical Canonical Portion
Every member's canonical `rules/` matches the L2 source exactly. Team-specific rules are a separate, additive layer (never replace canonical).

### Rule 3: Per-Member, Idempotent Re-Push
On change, iterate members via the set-manifest and re-push. A member already on the current version is a no-op. Same in subfolder + polyrepo (path vs URL only).

### Rule 4: Version Stamp + Stale Flag
Stamp `guardrailVersion` per member; the L2 roll-up (`rollup/`) flags any member on a stale version. No silent divergence.

### Rule 5: Preserve Team Customizations
`<!-- custom -->` rows and team-scoped rule sections survive re-push (same non-destructive rule as ordinary re-baseline).

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| `workspaceTopology: single` | N/A — ordinary re-baseline; nothing to spread |
| A member is on a stale guardrail version | Re-push + clear the stale flag in the L2 roll-up |
| polyrepo member repo unreachable | Record the member as "unreachable — sync pending" in the roll-up; do not block other members |
| Team added a `<!-- custom -->` rule | Preserve it; re-push only the canonical portion |
| Canonical guardrail removed in L2 | Remove it from every member on the next sync (idempotent) |

---

## Output Validation

- [ ] Runs only when `workspaceTopology ∈ {per-team, hybrid}`
- [ ] Canonical `rules/` byte-identical across all members after a sync
- [ ] Each member stamped with `guardrailVersion`; stale members flagged in the L2 roll-up
- [ ] Re-push is per-member + idempotent; identical logic in subfolder + polyrepo (path/URL only)
- [ ] Team `<!-- custom -->` rules preserved
- [ ] Downward loop only — upward digest is AI-GCE/AI-DFE (Phase 4/5)

---

*Generated by AI-DWG · AIFLC PDLC Family · © Mohammad Maheri · https://github.com/mbmd/AIFLC*
