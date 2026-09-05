<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Sensor-Wiring Verification — confirm an emitted manifest is actually bound to a stage

> **Load this file** under `buildProfile: aidlc` when AI-GCE runs its post-generation verification (the V1–V10 pipeline, `common/validation-rules.md`). It closes the one failure mode the sensor model has: **a manifest no stage imports never fires, silently.** AI-GCE reads the bootstrap record's `seeded.sensors` and reports any emitted manifest that has not been wired — a finding, never a silent pass. This is merged item 26, ledger row A50 (the last new-work item). Loaded **on demand**, never into the always-loaded dispatcher (CC-2). `TR-819`.

## The silent failure this catches

Under `aidlc`, AI-DWG emits each sensor manifest and lists its intended stage binding in `.governance/AIDLC_SENSOR_WIRING.md`, but **AI-DWG does not edit v2's stage files** — the binding is applied by v2's own learning loop or a human (item 25). The v2 compiler discovers a sensor only through a **stage's import declaration**; a manifest that sits on disk with no stage importing it is **skipped with no error and no warning**. So a governance check can be fully authored, correctly named, and completely inert — the exact silent-drift shape `INV-L1-014` and the frozen naming contract exist to prevent. Someone has to **confirm the wiring landed**, and that someone is AI-GCE (it is the continuous compliance companion; AI-DWG is a one-shot generator that has already exited).

## What AI-GCE reads — `seeded.sensors` in the bootstrap record

The bootstrap record `.governance/aidlc-bootstrap.yaml` (AI-DWG, item 17; frozen contract §6) carries a `seeded.sensors` field with three states:

| `seeded.sensors` | Meaning | AI-GCE's response |
|---|---|---|
| `none` | No manifests were emitted (e.g. a build method with no sensor surface, or nothing sensor-convertible) | Nothing to verify — pass |
| `manifests-only` | AI-DWG emitted the manifests + the wiring instruction file, but the stage binding has **not** been confirmed applied | **Report** each manifest as present-but-unwired; do **not** assume the checks are live (contract §7a Clause 3) |
| `wired` | The stage bindings were applied and confirmed | Pass — the sensors will fire |

`manifests-only` is the **honest default** AI-DWG writes (item 17): it does not claim the sensors are live because it cannot apply the binding itself. AI-GCE's verification is what moves the workspace's understanding from "manifests exist" to "manifests fire" — and until it can confirm `wired`, it says so rather than reporting green.

## The verification procedure

Run this under `buildProfile: aidlc` only (no other build method emits v2 sensor manifests — `N/A` elsewhere, per `common/build-method-resolution.md`):

1. **Read the emitted manifest set** — the `aidlc-*.md` files in `<project>/{platform-dir}/sensors/` (the frozen §4 registry AI-DWG wrote).
2. **Read `.governance/AIDLC_SENSOR_WIRING.md`** — the per-sensor target stage + exact import line AI-DWG listed.
3. **Read `seeded.sensors`** from `.governance/aidlc-bootstrap.yaml`.
4. **Cross-check the pairing declarations** — every `memory/` rule carrying `pairing: aidlc-pdlc-<id>` must name a manifest that exists; a rule paired to a non-existent manifest is a coverage gap (the mirror of a manifest with no rule).
5. **For each emitted manifest, confirm a stage imports it.** Where AI-GCE can read the v2 stage files, it checks the import directly; where it cannot (v2 owns those files and may not expose them), it relies on `seeded.sensors: wired` as v2's own confirmation.
6. **Report the outcome** — see below. This is a **reportable finding**, not a silent pass: an emitted-but-unwired manifest is surfaced to the user exactly like any other V-category failure.

## The report — never a silent green

```
SENSOR-WIRING VERIFICATION (aidlc only)
  Manifests emitted:        {n}  (frozen §4 registry)
  seeded.sensors:           {none | manifests-only | wired}
  Wired (importing stage confirmed):    {n}/{m}
  Unwired (manifest present, no stage): {n}   ← each listed by id + intended stage from the wiring file
  Rules paired to a missing manifest:   {n}   ← each listed by rule id + named pairing
  Verdict: {✅ all wired | ⚠️ {n} manifests present but not firing — apply the wiring file}
```

An `⚠️` verdict names each unwired manifest and points at its row in `.governance/AIDLC_SENSOR_WIRING.md` so the team (or v2's learning loop) can apply the exact import line. AI-GCE does **not** apply the binding itself — that boundary belongs to v2 (item 25); AI-GCE's job is to make the gap **visible** rather than let a governance check silently never run.

## Why AI-GCE owns this and AI-DWG does not

AI-DWG is a **one-shot generator**: it emits the workspace and exits, so it cannot observe whether a later binding step succeeded. AI-GCE is the **continuous compliance companion**: it runs its verification pipeline after generation and on every re-derivation, so it is the engine positioned to notice that a manifest never got wired. This is the same division item 25 set — AI-DWG **lists** the wiring and emits the script; AI-GCE **verifies** it landed; v2 **applies** it. Three owners, one seam each, no one editing another's files.

## Preserves capability, only verifies delivery (INV-L2-022)

This item adds a **check on the delivery mechanism**, not a change to any governed capability. It does not move a capability cell — it makes the `aidlc` sensor path honest by ensuring an emitted check is confirmed live rather than assumed live. Ledger A50 flips to ✅ here: its emission half was in place at item 25 (AI-DWG writes the manifests + wiring file), and its **verification half** — AI-GCE reading `seeded.sensors` and reporting unwired manifests — is what this file adds.

## Interaction with other files

| Related | Relationship |
|---|---|
| `common/build-method-resolution.md` | Names this verification in its `aidlc` column ("**Verify** `seeded.sensors` … landed, §7a Clause 3"); this file is the procedure behind that row |
| `common/validation-rules.md` | The V1–V10 pipeline this runs alongside under `aidlc` — an unwired manifest is a reportable finding like any V-category failure |
| `ai-dwg/…/buildmethod/aidlc/sensor-manifests.md` (item 25) | The **emission half** — writes the manifests + `.governance/AIDLC_SENSOR_WIRING.md`; this file is the **verification half** |
| `ai-dwg/…/buildmethod/aidlc/bootstrap-record.md` (item 17) | Owns `seeded.sensors` — the field this verification reads (`none` / `manifests-only` / `wired`) |
| `common/gate-fired-sensors.md` (item 24d) | Defines the three gate-fired sensors whose wiring this verifies |
| `common/aidlc-v2-output-contract.md` §7a Clause 3 (AI-DWG) | The frozen authority for the verification responsibility |

## Output validation

- [ ] Runs under `buildProfile: aidlc` only (N/A elsewhere — no other method emits v2 sensor manifests).
- [ ] Reads `seeded.sensors` and treats `manifests-only` as present-but-not-firing (never assumes live).
- [ ] Every emitted manifest is checked for an importing stage; unwired manifests are listed by id + intended stage.
- [ ] Rules paired to a missing manifest are reported as coverage gaps.
- [ ] An unwired manifest is a **reportable finding**, never a silent pass.
- [ ] AI-GCE does NOT apply the binding — it reports; v2/the human applies from the wiring file.

---

*Developer-side design detail · AI-GCE sensor-wiring verification · © Mohammad Maheri*
