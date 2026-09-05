<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# L3 Change Detection & Report-Up — Derivation Logic (Multi-Workspace Only)

## Purpose

Detect **any change** in a Layer-3 team workspace — guardrail drift, contract edits, structural changes, new violations — and **report it up** into the Layer-2 control-plane roll-up, where the architects/owners see it. This is the **upward half** of the governance-circulation loop (design §5.1 ⬆): GCE detects + reports, AI-DFE digests, and the Layer-2 design packages refine and re-propagate. (Q-D3, owner directive.)

**Output:** entries in each member's local drift register + compliance log, aggregated into the L2 `rollup/` (via `generators/cross-workspace-rollup.md`).

**Condition:** Runs ONLY when a Layer-2 `workspace-set-manifest.yaml` is present. In a single workspace, ordinary GCE drift detection applies (no report-up — there is no set).

**Tier:** 2.

> **Upward half of the loop only.** This file detects + reports up. The downward half (re-propagate corrected guardrails to every member) is AI-DWG `reconciliation/guardrail-sync.md`. Together they close the circulation loop (design §5.1). One-way boundary preserved: L2 *reads* L3 down to detect; the correction flows back down through DWG, never L3→L2 writes.

---

## MANDATORY: Stage Sub-Role — Team Topology Architect + Audit Specialist

Team Topology Architect (`#persona-subrole-team-topology-architect`) layered with Audit Specialist (change evidence). ADDS a dimension — does NOT replace the primary Compliance/Governance role.

---

## What Counts as a "Change" (report-up triggers)

| Change class | Detected from | Reported as |
|--------------|---------------|-------------|
| **Guardrail drift** | member `rules/` `guardrailVersion` < L2 canonical version, or a canonical rule edited locally | Stale/diverged guardrail — flag for re-sync (DWG guardrail-sync) |
| **Contract edit** | member edited a contract it does NOT own (read-only copy touched), or an owner published a new version | GOV-TT-006 / GOV-TT-008 event → contract-conformance roll-up |
| **Structural change** | member added/removed a module, or a `src/` module now crosses a bounded-context boundary | Structural drift → drift-rollup |
| **New violation** | member's local compliance log shows a new GOV-TT-001..010 failure | Compliance event → compliance-rollup |
| **Interaction-mode violation** | observed dependency contradicts the designed interaction mode | GOV-TT-010 event |
| **Cross-workspace source import** | member imports another member's source (not via a contract) | GOV-TT-009 event |

---

## Detection Flow

1. **Read the set-manifest** to enumerate members + resolve each member's governance home (folder path or repo URL via `physicalLayout`).
2. **For each member, read down** its `.governance/` (compliance log, drift register) + its `rules/` version stamp + its contract copies.
3. **Compare against the L2 baseline** — canonical guardrail version, contract registry (owners + versions + compatibility policy), interaction-mode design.
4. **Classify** each detected change per the table above.
5. **Report up** — write the change into the member's local drift register (evidence stays local) AND aggregate into the L2 roll-up (`cross-workspace-rollup.md`).
6. **Signal the downward loop** — a guardrail-drift or design-affecting change is flagged for the L2 packages to digest (AI-DFE digest → ADLC/POLC/UXD refine → DWG re-propagate via guardrail-sync).

---

## Rules

### Rule 1: Detect Any Change, Report Every Change
No change class is silent — guardrail drift, contract edits, structural changes, and new violations all report up (Q-D3).

### Rule 2: Evidence Stays Local, Summary Goes Up
The detailed evidence stays in the member's local `.governance/`; the roll-up carries the summary + a drill-down pointer. (Do not duplicate logs upward.)

### Rule 3: Read Down, Never Write Down (here)
This generator only *reads* L3 down to detect. Corrections flow back down through DWG `guardrail-sync.md`, not from this file.

### Rule 4: Mode-Transparent (Q-D6)
Identical detection in subfolder + polyrepo; `physicalLayout` resolves the member locator only.

### Rule 5: Feeds the Circulation Loop
Design-affecting changes are flagged for the upward digest (AI-DFE + L2 packages), closing the loop with DWG's downward re-propagation (design §5.1).

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| No set-manifest (single workspace) | Do not run — ordinary local drift detection applies |
| Member unreachable | Record "unreachable — detection stale for {TEAM}"; continue with the rest |
| Change is an approved team customization (`<!-- custom -->`) | Not a violation — record as an intentional local rule, not drift |
| Guardrail version matches canonical | No-op (no drift) |

---

## Output Validation

- [ ] Runs only when a Layer-2 `workspace-set-manifest.yaml` is present
- [ ] Every member scanned; every change class detected + reported up
- [ ] Evidence stays local; summary + drill-down pointer in the L2 roll-up
- [ ] Design-affecting changes flagged for the upward digest (AI-DFE + L2 packages)
- [ ] No downward writes from this file (corrections flow via DWG guardrail-sync)
- [ ] Identical detection in subfolder + polyrepo

---

*Generated by AI-GCE · AIFLC PDLC Family · © Mohammad Maheri · https://github.com/mbmd/AIFLC*
