<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# FLO → DFE Data-Refresh Signal Contract

**Contract:** `data-refresh-signal@1.0`
**Version:** 1.0.0
**Date:** 2026-09-03
**Status:** ADOPTED
**Parties:** AI-FLO (producer / emitter) · AI-DFE (consumer / processor)
**Tracks:** OI-194
**Runtime home (per family):** `{family}-ws/data/SIGNAL_CONTRACT.md` (this file is the canonical fabric-source template, cloned into each family at `DEV__ promote`)

---

## 1. Purpose

Keep the DFE data surface fresh **automatically** as packages progress, without the user remembering to run `DAT__`. AI-FLO already detects when an entity advances (gate completion / stage change); this contract lets FLO **emit a lightweight file-based signal** that AI-DFE picks up and turns into a scoped `gather → shape → distribute` refresh for exactly the package that changed.

The signal is a **message, not a data product**. It is fire-and-forget: FLO writes it and moves on; DFE consumes it on its next pass (or same-session if the optional destination hook is installed — see §8). Nothing waits, nothing blocks.

> **This is a bilateral CONTRACT, not a package.** It defines only the envelope FLO writes and the rules DFE follows. It introduces no new engine and no new always-loaded content. Mirrors the marker-based communication-fabric pattern (file inbox: producer writes → consumer reads → consumer archives).

---

## 2. Territory & the sole-writer carve-out

AI-DFE is the **sole writer of all data products** in `{family}-ws/data/` (`*.json`, `REGISTRY.json`, snapshots). This contract declares **one narrow, explicit exception**:

- `{family}-ws/data/signals/` is a **FLO write-inbox**. AI-FLO MAY write `*.signal.md` files here — and ONLY here.
- Signal files are **operational messages**, never data products: they never appear in `REGISTRY.json`, are never served to a consumer, and are excluded from DFE's gather scope as *sources*.
- AI-DFE owns the folder's lifecycle (creates it, reads, archives to `processed/`, cleans up). AI-FLO only appends new signal files.
- DFE's sole-writer integrity over *data* (INV-L4-006 single-writer model) is preserved: FLO writes messages, DFE writes data.

| Concern | Owner |
|---|---|
| Write `*.signal.md` into `signals/` | AI-FLO (the only signal producer) |
| Read + process signals; refresh data; archive to `processed/`; cleanup | AI-DFE |
| The `signals/` + `signals/processed/` folders | AI-DFE's territory (declared inbox) |
| This envelope schema + processing rules | Shared (this contract, versioned) |

---

## 3. Signal envelope (`data-refresh-signal@1.0`)

**Location:** `{family}-ws/data/signals/`
**Filename:** `flo-refresh-{epoch-ms}.signal.md` (the `{epoch-ms}` is FLO's shell-sourced timestamp; it also gives deterministic FIFO ordering by filename)
**Processed archive:** `{family}-ws/data/signals/processed/`

Each signal file is front-matter only:

```yaml
---
signalType: data-refresh          # always "data-refresh" (this contract); future signal types reserve other values
signalVersion: "1.0"              # contract version
family: {family-code}             # e.g. pdlc
source: AI-FLO                    # always AI-FLO
timestamp: {ISO-8601}             # when FLO emitted (same clock as the epoch-ms filename)
entity: {entity-id}               # the entity/project whose package advanced
package: {package-code}           # the package to refresh (e.g. ai-ilc) — the scoped-refresh target
event: gate-complete | stage-advance   # what FLO detected
marker: {marker-file-path}        # path to the updated *-state.md that triggered the signal
---
```

| Field | Required | Meaning |
|-------|:--------:|---------|
| `signalType` | ✅ | Always `data-refresh` for this contract. |
| `signalVersion` | ✅ | Semver of this contract (`1.0`). DFE rejects a major it doesn't understand (→ error-archive, §5). |
| `family` | ✅ | Family code — scopes the refresh. |
| `source` | ✅ | Always `AI-FLO`. |
| `timestamp` | ✅ | ISO-8601 emit time (shell-sourced; never a hosted time tool). |
| `entity` | ✅ | Entity/project id that advanced. |
| `package` | ✅ | Package code to refresh — DFE runs a **scoped** `DAT__ {family}/{package}`. |
| `event` | ✅ | `gate-complete` (package fully done) or `stage-advance` (intra-package stage/status change). |
| `marker` | ✅ | Path to the `*-state.md` FLO observed change on (provenance / debugging). |

---

## 4. Emission rules (AI-FLO side)

FLO emits per the family's `dfeRefreshGranularity` setting (declared in the family's FLO overlay — see the overlay's "Data Refresh Signal Policy"):

| Granularity | FLO emits when… |
|-------------|-----------------|
| `gate-only` **(default)** | a marker's `status` changes to `complete` (the package finished). |
| `stage-advance` | any `stage`/`status` field on a marker changes (intra-package progress). |
| `off` | never (family opts out; DFE relies on timestamp staleness only). |

- **Fire-and-forget.** FLO writes the file and continues; it never waits for DFE, never switches to DFE, never activates DFE. The file IS the whole handoff.
- **Emitted from two FLO seams:** Position Tracking (continuous scan) and Handoff Execution (source package just completed).
- **Dedup at the source:** if Position Tracking already emitted a signal for the same `package` + `timestamp`, Handoff Execution skips the duplicate.

---

## 5. Processing rules (AI-DFE side)

On any DFE pass (Monitor preamble, or the explicit `DAT__ signals --process`):

1. **Discover.** Scan `{family}-ws/data/signals/` for `*.signal.md` (exclude `processed/`).
2. **Order.** Process **FIFO** — oldest `{epoch-ms}` first.
3. **Dedup.** If two pending signals share the same `package` + `timestamp`, process once; archive the duplicate without re-gathering.
4. **Refresh (per signal).** Read `package` → run scoped `Gather` → `Shape` (affected demands) → `Distribute` for that one package.
5. **Archive on success.** Move the signal file to `signals/processed/`.
6. **Error handling.** A malformed / unparseable envelope, or an unknown major `signalVersion`, is **not** processed — DFE logs a warning, moves the file to `processed/` with an appended `## Error` annotation, and continues with the remaining signals.
7. **Report.** "Processed {N} refresh signal(s): {package-list}."
8. **Priority + catch-all.** Signals take priority over timestamp checks (they are confirmed completions); the normal timestamp-staleness pass still runs afterward as a catch-all (manual edits, changes made while FLO was inactive).

---

## 6. Retention

- Processed signals are retained in `signals/processed/` for **30 days** (audit trail), then eligible for cleanup by DFE's Govern → Cleanup pass.
- Pending (unprocessed) signals are **never** auto-deleted — they are the outstanding work queue. Use `DAT__ signals --clear` to intentionally discard stale pending signals without processing them.

---

## 7. Graceful degradation

| Scenario | Behavior |
|----------|----------|
| AI-FLO not installed | No signals ever appear. DFE uses timestamp-based staleness only (current behavior — no regression). |
| AI-DFE not installed | Signals accumulate harmlessly in `signals/`. FLO never checks (fire-and-forget). |
| `signals/` folder absent | Created on first use — by DFE on its first pass, or by FLO on its first signal write. |
| DFE offline for days | Signals accumulate; next DFE activation processes all pending FIFO — data catches up in one pass. |
| Malformed signal | Logged, moved to `processed/` with an `## Error` note; remaining signals still process. |
| Duplicate signal | Deduplicated (§5.3). |
| `dfeRefreshGranularity: off` | FLO emits nothing; DFE timestamp fallback handles all staleness. |

The mechanism **adds** freshness when both engines are present and **never** breaks either one when the other is absent.

---

## 8. Optional same-session instant processing (destination-workspace hook)

By default, DFE processes pending signals on its **next activation** (small delay). A workspace that wants **same-session, near-real-time** refresh may install a `PostFileCreate` hook that fires when a `flo-refresh-*.signal.md` appears and prompts DFE to run `DAT__ signals --process`.

> **Rule-22 boundary (developer-side vs user-side).** This hook is a **destination-workspace** artifact — it is **generated by AI-GCE into the consumer's workspace** (`{consumer-workspace}/.kiro/hooks/`), NOT authored under the build workspace's `.kiro/`. The build repo never ships a live `.kiro/hooks/dfe-signal-processor.json`; AI-GCE emits it when it detects both AI-FLO and AI-DFE installed. The file-based model in §1–§7 works fully **without** this hook — it is a latency optimization only.

**Destination hook spec (AI-GCE emits this verbatim into `{consumer-workspace}/.kiro/hooks/dfe-signal-processor.json`):**

```json
{
  "version": "v1",
  "hooks": [{
    "name": "AIFLC DFE Signal Processor",
    "trigger": "PostFileCreate",
    "matcher": "data[/\\\\]signals[/\\\\]flo-refresh-.*\\.signal\\.md$",
    "action": {
      "type": "agent",
      "prompt": "A FLO data-refresh signal was created. Process it now: run `DAT__ signals --process` to refresh the DFE data surface for the signaled package (per SIGNAL_CONTRACT.md)."
    }
  }]
}
```

- **Name** starts with `AIFLC ` (Workspace Rule 28).
- **Generation condition:** AI-GCE generates it only when both AI-FLO and AI-DFE are detected in the destination workspace (both fabric engines installed) — a conditional destination hook, ships-enabled. If either engine is absent, the hook is not generated (the file-based fallback still works).
- **Never created in the build workspace.** This block is the *spec* AI-GCE renders; the build repo carries no live hook file for it (Rule 22).

---

## 9. Versioning

`data-refresh-signal@1.0`. A backward-compatible field addition bumps the minor (`1.1`) and DFE tolerates unknown optional fields. A breaking envelope change bumps the major (`2.0`); DFE error-archives (§5.6) any signal whose major it does not implement, so an upgrade never silently mis-processes.

---

*Shared bilateral contract for the AI-* family fabric. Producer: AI-FLO. Consumer: AI-DFE. Governs the file-based data-refresh signal inbox at `{family}-ws/data/signals/`. The `signals/` folder is FLO's sole declared write-exception to DFE's data sole-writer rule (INV-L4-006); signals are messages, not data products.*
