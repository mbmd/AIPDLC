<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# `aidlc/` Emitter — orchestrates the AI-DLC v2 output tree

> **Load this file** when `buildProfile: aidlc` and AI-DWG is generating or reconciling. It orchestrates the emission of the `aidlc/` tree. Every path, filename, and front-matter block it writes is governed by the FROZEN contract `common/aidlc-v2-output-contract.md` — load that alongside this file.

## Preconditions

1. `.governance/workspace-manifest.yaml` exists and `buildProfile: aidlc`.
2. The canonical `rules/` and the peer-input clusters (AP / PBP / UXP) that are present have been read (the same inputs the workspace generation used).
3. The space slug is known (`aidlc/spaces/<space>/` — default `default` unless the project declares otherwise).

If `buildProfile` ≠ `aidlc`, this emitter does not run — dispatch belongs to `buildmethod-model.md`.

## The emission sequence

The emitter runs these steps in order; each delegates to a detail file and writes to the contract-fixed paths.

| # | Step | Delegates to | Writes | Condition |
|:-:|---|---|---|---|
| 0 | **Split each steering file** (shared front step for 1+2) | `rules-knowledge-splitter.md` | — (in-memory: rules portion vs knowledge portion) | Always (under `aidlc`) |
| 1 | **Behavioural rules** (consumes the split's rules portion) | `memory-mapping.md`, then `practices-preseeding.md`, then `phase-rules.md` | `aidlc/spaces/<space>/memory/team.md`, `memory/project.md`, `memory/phases/{ideation,inception,construction,operation}.md` | Always (under `aidlc`) |
| 2 | **Per-agent knowledge** (consumes the split's knowledge portion) | `knowledge-routing.md` | `aidlc/spaces/<space>/knowledge/<agent>/…` | A directory only where content exists (conditional emission rule) |
| 3 | **Narrative documents** | `documents-placement.md` | `aidlc/spaces/<space>/knowledge/documents/…` | Where full narrative docs exist |
| 4 | **Code knowledge base** | `codekb-seeding.md` | `aidlc/spaces/<space>/codekb/<repo>/…` (7 of 9 artifacts) | **Greenfield only** AND AI-ADLC present |
| 5 | **Sensor manifests + wiring** | `sensor-manifests.md` | `<project>/{platform-dir}/sensors/aidlc-<id>.md` + `.governance/AIDLC_SENSOR_WIRING.md` | Always (under `aidlc`); manifest set per contract §4 |
| 6 | **Bootstrap record + scope recommendation** (emits LAST — `seeded:` records the actual outcome of steps 1–5) | `bootstrap-record.md`, `scope-recommendation.md` | `.governance/aidlc-bootstrap.yaml` (incl. `recommended_scope: classic`) + the `/aidlc --scope classic` start instruction in workspace onboarding | Always (under `aidlc`) |

**Step 1 runs in three parts.** `memory-mapping.md` routes each rule to its frozen heading across `team.md`/`project.md`/`phases/`; then `practices-preseeding.md` (merged item 14) enforces the one obligation the mapping alone does not — `memory/team.md` is written with **all five** Practices-Discovery sections as a complete unit (never conditionally) so v2's Stage 2.2 fast-affirms rather than interviewing; then `phase-rules.md` (merged item 16) emits the four `memory/phases/{ideation,inception,construction,operation}.md` files from item 7's phase-vocabulary mapping, honouring the three emission traps (`ideation.md` emitted-with-reason never blank; `PG-SETUP-*`/`PG-FOUND-*` re-formed not dropped; `construction.md`'s two source groupings labelled). The team.md completeness is the exception to invariant 1 (conditional emission), scoped to `team.md` only.

**All six steps are now fully built.** Step 5 (sensor manifests) was completed at merged item 25 — it renders each manifest from AI-GCE's neutral intermediate (item 23) into v2's §4 field set, emits the executable check-scripts, and writes `.governance/AIDLC_SENSOR_WIRING.md`; steps 4 (code-KB, item 15) and 6 (bootstrap record, item 17) were built earlier. This emitter establishes the orchestration and the call sites; the step files under this folder carry the detail.

## Invariants the emitter enforces

1. **Conditional emission.** A directory is created only when there is content for it. An empty agent directory is never written — it is indistinguishable from v2's own empty-at-bootstrap state while implying content was intended (contract §3). **One deliberate exception:** `memory/team.md`'s five Practices-Discovery sections are always emitted as a complete unit (per `practices-preseeding.md`), because structural parity with what Stage 2.2 itself writes is what makes the pre-seed safe under append / overwrite / section-replace alike.
2. **Front-matter on every file.** Rule files carry `status:` + `pairing:` (contract §2); knowledge files carry the standard provenance block (contract §3). The emitter never writes a rule file without `pairing:` — an omitted pairing shows as a coverage gap on v2's first health check.
3. **Tool-neutral by default.** `memory/`, `knowledge/`, `documents/`, `codekb/` are written at fixed paths with no platform call. **Only** sensor manifests (step 5) consult the platform adapter as a path-resolution service (the seam in `buildmethod-model.md`).
4. **Never write the forbidden targets.** `memory/org.md` (v2 supplies org defaults), `knowledge/documentkb/` (v2's cataloguing tool only), and the two never-seed code-KB artifacts (`code-quality-assessment`, `reverse-engineering-timestamp`) are NEVER written. See contract §2, §5 and the placement never-write list.
5. **Additive, not overriding.** Seeded rules sit alongside org/team defaults in v2's additive chain — the emitter writes only what is genuinely this project's, and avoids restating framework defaults (contract §2, to keep v2's overlap-contradiction advisory quiet).

## Reconciliation (Mode 2)

On regeneration, treat the `aidlc/` tree as **team-modified**: preserve `<!-- custom -->` blocks and any v2-appended dated learning entries in `memory/project.md`/`team.md`. Re-derive only the seeded content that has not been hand-edited; never clobber a confirmed learning.

## What the emitter records for downstream

After emission, the bootstrap record's `seeded:` block (contract §6) reflects what was actually written — `memory: true`, `phases: true`, `knowledge: true|false`, `documents: true|false`, `codekb: true|false` (false on brownfield), `sensors: manifests-only` (until wiring is applied). AI-GCE reads this to know what to expect and to verify sensor wiring (contract §7a Clause 3).

---

*Developer-side design detail · AI-DWG `aidlc/` emitter · © Mohammad Maheri*
