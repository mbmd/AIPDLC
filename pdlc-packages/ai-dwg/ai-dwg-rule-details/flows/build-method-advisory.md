<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Flow: Build-Method Advisory (Soft Notice — Never Blocks)

## Purpose

DWG reads the story style from `polc-state.md` and generates an advisory in `info/PROJECT_INSTRUCTIONS.md` (or `info/BUILD_NOTES.md`) that informs the user which build methods fit their story format — **without asking or blocking**.

**When:** Generated during the output phase of Mode 1 (Full Generation) and Mode 2 (Delta Reconciliation, if POLC input changed). Placed into `info/` alongside operational guides.

**Design principle:** DWG *generation* is build-method-agnostic — the workspace serves ALL build methods (AI-DLC, spec-driven via Spec Kit, freestyle) identically. This advisory is informational only; it never blocks or gates. (Separately, DWG records a *derived* `buildProfile` governance signal in the manifest for AI-GCE cadence — a downstream signal, not a generation gate; see Background.)

---

## Advisory Logic (Story Format → Build-Method Fit)

| Story Style (from POLC) | Fits well | Advisory if planning spec-driven |
|-------------------------|-----------|----------------------------------|
| **EARS** | spec-driven (Spec Kit), AI-DLC, freestyle | None — EARS is spec-ready |
| **Classic INVEST (G/W/T)** | AI-DLC, freestyle | Spec Kit favors EARS — G/W/T is convertible but not 1:1; review before feeding a spec runner |
| **Job Story** | freestyle, AI-DLC | Same EARS caveat as INVEST |
| **Freestyle** | freestyle only | Not structured for AI-DLC or spec runners |
| **Hybrid** | depends per-story | Mixed — check individual stories |

---

## Reading the Story Style

1. Read `polc-state.md` → look for the `storyStyle` field (one of: `ears`, `invest`, `job-story`, `freestyle`, `hybrid`)
2. If `polc-state.md` absent (POLC not a peer input) → skip advisory entirely (no POLC = no stories = no advisory needed)
3. If `storyStyle` field absent in state → default to `invest` (the classic Scrum format)

---

## Generated Output (Template)

Place this section in `info/PROJECT_INSTRUCTIONS.md` (after the main dev guide content) OR as a standalone `info/BUILD_NOTES.md` if PROJECT_INSTRUCTIONS is already long:

```markdown
## Build Method Advisory

Your backlog stories are in **{storyStyle}** format (from AI-POLC).
- Works with: {fitting methods from table above}
- {caveat line from table above, if applicable — otherwise omit}

This is advisory — nothing blocks. The workspace serves all build methods.
```

---

## Rules

1. **Never blocks.** The advisory is soft — no gate, no question, no compatibility check that could halt generation.
2. **Never asks the build method.** DWG does NOT ask "how will you build this?" — that's a downstream consumption choice.
3. **Generated once per workspace.** Mode 1 creates it; Mode 2 updates it only if `storyStyle` changed in `polc-state.md`.
4. **Concise.** The advisory is 3-5 lines in the generated file, never a full page.
5. **Source: POLC only.** The advisory derives solely from `storyStyle` in `polc-state.md`. No other input affects it.

---

## Background (Build-Profile Axis — Generation-Gate Rejected; Governance Signal Un-Parked 2026-08-09)

An earlier design (2026-07-05) proposed a third axis to DWG (build profile: aidlc-v1 / spec-driven / freestyle) as a **hard generation gate**. That **generation gate stays rejected** because:
- A generation gate contradicts build-method-agnosticism (the generated workspace serves all methods identically)
- It would add a config question with no action — DWG's *output* is the same regardless

**What changed (2026-08-09, delivery-method-timing un-park):** `buildProfile` is now populated in the workspace manifest as a **downstream governance signal** — **derived** from the upstream delivery method + story style (never asked): `spec-driven` / `aidlc` / `freestyle`, or omitted for manual/AI-assisted (→ GCE Standard mode). It does **not** gate or alter DWG generation (output stays identical and agnostic). Its sole effect is downstream: AI-GCE reads it to tune drift-detection depth + gate cadence (`drift/gate-integration.md`). This reconciles the original objections — DWG generation stays agnostic, `buildProfile` is derived (not a config question), and it now carries a real downstream action the 2026-07-05 *gate* design lacked. The soft advisory above is unchanged.

See `DWG_DUAL_GENERATOR_DESIGN.md` (deferred) for the separate question of explicit spec-kit vs AI-DLC workspace *generation* variants.
