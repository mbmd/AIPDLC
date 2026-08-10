<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Figma Sync Agent

> **Trigger:** `UXC__ sync-figma`
> **AG-ID:** UXD-AG-02
> **Domain:** AI-UXD ↔ Figma reconciliation

---

## Purpose

Reconciles a Figma-exported token set (dropped in `integrations/figma/in/`) against the governed canonical (`07_Design_System/design-tokens.json`) using a governed 3-way diff. Produces a human-reviewable reconciliation report; applies accepted changes only on approval.

**This is input reconciliation, not drift detection.** A Figma export is an input source (same family as brownfield Mode D) — it does NOT use the `drift-intake@1.0` back-flow reserved for AI-GCE / AI-FLO.

---

## When to Invoke

| Situation | Why |
|-----------|-----|
| A designer exported updated Variables from Figma | Reconcile tool-side changes with the governed source |
| After a design sprint that modified Figma tokens | Bring governed tokens up to date with approved design work |
| Periodic sync checkpoint (cadence: on-demand) | Prevent divergence from accruing silently |

---

## Prerequisites

1. A valid DTCG-shaped JSON file in `{project_root}/integrations/figma/in/` (Tokens Studio export, Figma Variables REST API export, or manual).
2. The canonical `{project_root}/ux/07_Design_System/design-tokens.json` exists (Stage 8 has been completed at least once).
3. A `.sync-manifest.json` alongside the canonical (created on first forward publish; records the baseline state for 3-way diff).

If prerequisite 3 is missing (first-ever sync), the agent treats the current canonical as the baseline (effectively a 2-way diff: canonical vs Figma).

---

## Execution Steps

### Step 1: Validate Input

- Schema-validate the Figma export against W3C DTCG structure. It is **untrusted external input** — reject malformed files with a clear error.
- Detect format variant (Tokens Studio multi-file set vs single-file Variables export) and normalize to a flat token map.
- Record the export's provenance: filename, size, modification date.

### Step 2: Load Baseline + Canonical

- **Baseline:** read `.sync-manifest.json` → `lastSyncState` (a snapshot of token IDs + values at the last successful sync).
- **Canonical ("ours"):** read `07_Design_System/design-tokens.json` — the current governed source of truth.
- **Theirs:** the validated Figma export from Step 1.

### Step 3: 3-Way Diff

For each token (matched by stable `$extensions."com.aiflc.uxd".id`):

| Case | Classification | Default Action |
|------|---------------|----------------|
| Present in Figma, absent in baseline + canonical | **Added in Figma** | Propose: assign tier (infer from naming) + semantic name; run governance checks |
| Same ID, value differs Figma vs canonical, baseline matches canonical | **Changed in Figma** | Propose: re-run governance for `$type`; pass → accept, fail → reject with reason |
| Present in baseline + canonical, absent in Figma | **Removed in Figma** | Propose deprecation (flag if downstream consumers reference it — never auto-remove) |
| Same ID, key/path differs Figma vs canonical, `$value` unchanged | **Renamed in Figma** | Propose rename (match by stable ID — this is why `$extensions` IDs exist) |
| Same ID, value differs in BOTH Figma and canonical vs baseline | **True conflict** | Flag for human resolution; UXD governance = default tiebreaker |
| Same ID, values identical across all three | **No change** | Skip |
| Present in canonical, absent in Figma AND baseline | **Added in canonical (not in Figma)** | No action (canonical is authoritative for new governed tokens) |

Tokens without a matching `$extensions."com.aiflc.uxd".id` in the Figma export are matched by path as a fallback (with lower confidence — noted in the report).

### Step 4: Governance Re-Check

For every proposed accept (add / change / rename):

- **Accessibility:** WCAG contrast re-check for all color tokens (AA ≥ 4.5:1 text, ≥ 3:1 UI).
- **Tier integrity:** no component-tier token may bypass semantic tier (direct global reference).
- **Naming schema:** token path must follow the `{category}.{item}.{variant}` convention.
- **Traceability:** every token must connect to a design principle (can be flagged "pending assignment" for new additions).

A governance failure on any check → the proposal is **rejected with reason** (not silently dropped — the designer sees why).

### Step 5: Component Parity Check (informational)

Compare the component inventory (Stage 9) against Figma's component/variant structure:
- **Name match:** component names align.
- **Variant axes:** Figma variant properties match the documented state/variant axes.
- Report mismatches as advisory (not blocking) — these inform the designer, not the merge.

### Step 6: Generate Reconciliation Report

```markdown
# UXC sync-figma — Reconciliation Report

**Date:** {date}
**Figma export:** {filename} ({size}, modified {date})
**Canonical version:** {from $extensions.com.aiflc.uxd.generatedVersion}
**Baseline:** {from .sync-manifest.json lastSyncDate}

## Summary

| Category | Count | Action |
|----------|:-----:|--------|
| Added in Figma | {N} | Propose (governance-checked) |
| Changed in Figma | {N} | Propose / Reject |
| Removed in Figma | {N} | Propose deprecation |
| Renamed in Figma | {N} | Propose rename |
| Conflicts | {N} | Human decision required |
| Governance rejections | {N} | Blocked — see reasons |
| No change | {N} | — |

## Proposals (Accept / Reject Each)

| # | Token ID | Delta | Figma Value | Canonical Value | Governance | Proposal |
|---|----------|-------|-------------|-----------------|:----------:|----------|
| 1 | {id} | {type} | {value} | {value} | ✅/❌ | Accept / Reject: {reason} |

## Conflicts (Human Decision Required)

| # | Token ID | Baseline | Canonical (ours) | Figma (theirs) | Recommendation |
|---|----------|----------|-----------------|----------------|----------------|
| 1 | {id} | {value} | {value} | {value} | {UXD governance suggests…} |

## Governance Rejections (Blocked)

| # | Token ID | Reason | Fix Required |
|---|----------|--------|--------------|
| 1 | {id} | {e.g., contrast 3.2:1 < 4.5:1} | {adjust value to meet AA} |

## Component Parity (Advisory)

| Component | Status | Note |
|-----------|:------:|------|
| {name} | ✅ / ⚠️ | {mismatch detail if any} |

## Next Steps

1. Review proposals above — approve, reject, or modify each.
2. Resolve conflicts (pick ours / theirs / merge).
3. On approval: canonical + projection regenerated; baseline updated.
```

### Step 7: Apply Approved Changes

On human approval (explicit — never auto-merge):

1. **Merge accepted proposals** into `07_Design_System/design-tokens.json`:
   - Bump `generatedVersion` (patch for changes, minor for additions/removals).
   - Update `generatedOn` to current ISO date.
   - Preserve stable `$extensions."com.aiflc.uxd".id` for renamed tokens (update path only).
2. **Regenerate the Figma projection** at `integrations/figma/out/design-tokens.json` (derived from the new canonical — adds Figma plumbing: mode sets, `$themes`).
3. **Update `.sync-manifest.json`** — record new baseline state (token IDs + values + sync date).
4. **Update `07_Design_System/Design_Tokens.md`** — the human-readable view (regenerated from the canonical).
5. **Run `UXC__` consistency checks** (CHK-02 token consistency at minimum) to verify no downstream breaks.

### Step 8: Post-Sync Confirmation

```
🔄 Figma Sync Complete
   • Accepted: {N} proposals
   • Rejected: {N} (governance)
   • Conflicts resolved: {N}
   • Canonical version: {new version}
   • Baseline updated: {ISO-date}
   • Run UXC__ for a full consistency check if additional artifacts were affected.
```

---

## Consequences of Skipping

- **Silent divergence** — Figma becomes a fork of the governed tokens over time
- **Governance bypass** — designers may introduce tokens that fail accessibility or tier rules
- **Rename confusion** — without periodic sync, stable IDs lose their matching value
- **Stale projection** — the `integrations/figma/out/` file drifts from what Figma actually uses

---

## Recovery (If Skipped Too Long)

1. Export the current Figma state → `integrations/figma/in/`
2. Run `UXC__ sync-figma` — the 3-way diff will show accumulated divergence
3. Treat the report as a "catch-up" reconciliation — review and approve in batches
4. After sync, re-run `UXC__` for a full consistency validation

---

## Authority & Invariants

- **UXD is authoritative.** The governed canonical always wins on conflict unless the human overrides.
- **Accessibility is non-negotiable.** A contrast failure blocks the merge — no override.
- **Tier integrity is structural.** A component→global shortcut is always rejected.
- **Stable IDs survive.** A rename in Figma produces a path change, not an ID change.
- **The `integrations/` folder remains derived + disposable.** Post-sync, deleting it loses nothing.

---

## Dependencies (Declared)

| Dependency | Nature | Required? |
|------------|--------|:---------:|
| Figma Variables export (JSON) | Input file | Yes |
| Tokens Studio / REST API access | Export mechanism | One of (user choice) |
| `.sync-manifest.json` | Baseline state | Auto-created on first forward publish |
| Design QA framework (Stage 13) | Validation of merge result | Recommended |
| `UXC__` consistency agent | Post-sync verification | Recommended |

---

## Related

- **Forward publish** — Stage 8 (`design-system-foundation.md`) emits canonical + projection
- **`figma-handoff.md`** — documents the import mechanism + surface
- **`ux-consistency-agent.md`** (`UXC__`) — validates UXP consistency (complementary; CHK-02 covers token integrity)
- **Design QA framework** (Stage 13) — validates design-to-code fidelity; this agent validates design-to-tool fidelity

---

*Agent template for AI-UXD Figma Sync | Installed by `agent-installation.md` | AIFLC PDLC Family*
