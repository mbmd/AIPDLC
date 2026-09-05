# Stage 2.4 — Monitor

> Phase 2 (Operate). The cheap continuous loop — detect stale data and refresh only what changed.

## Purpose

Avoid re-gathering everything every pass. Compare each cached source's timestamp against the data file's `$generatedOn`; refresh only stale files.

## Inputs

- `dfe-state.md` (`discovered.{pkg}.sourceFiles[]`, `lastGenerated`).
- Filesystem timestamps of the declared source files.

## Signal-Check Preamble (FLO data-refresh signals)

Runs **first**, before the timestamp loop below. Consumes the FLO write-inbox at `{family}-ws/data/signals/` per `contracts/SIGNAL_CONTRACT.md` (`data-refresh-signal@1.0`).

1. Scan `{family}-ws/data/signals/` for `*.signal.md` files (exclude `signals/processed/`).
2. If found — process **FIFO** (oldest `{epoch-ms}` first):
   a. Read the envelope; take `package` as the scoped-refresh target.
   b. **Dedup:** if an earlier signal this pass already refreshed the same `package` at the same `timestamp`, archive this one without re-gathering.
   c. Run scoped refresh for that package: **Gather (2.1)** → **Shape (2.2)** for any DEMAND that draws on it → **Distribute (2.3)** (each write gated by 3.1 Validation + snapshotted by 3.3 History).
   d. **On success:** move the signal file to `signals/processed/`.
   e. **On failure** (malformed envelope, or an unknown major `signalVersion`): log a warning, move the file to `signals/processed/` with an appended `## Error` annotation, and continue with the remaining signals.
   f. Report: "Processed {N} refresh signal(s): {package-list}."
3. If none: proceed to the timestamp check below.

Signals take **priority** over the timestamp check (they are confirmed completions). After processing signals, the timestamp check still runs as a **catch-all** (manual edits, or changes made while FLO was inactive). If the `signals/` folder is absent, create it on first run.

## Logic

1. For each package, find the most-recent modification time across its cached `sourceFiles[]`.
2. If that time > the data file's `$generatedOn` → mark **stale**; re-run gather (2.1) for that package, then shape (2.2) for any DEMAND that draws on it, then distribute (2.3).
3. If fresh → skip (no work).
4. Two triggers can start a pass: a **FLO data-refresh signal** (see the Signal-Check Preamble above — a confirmed "package X completed / advanced", processed first) or a **timestamp pass** (the catch-all fallback). Signals take priority; the timestamp check always runs afterward.

## Output

Refreshed deltas only; unchanged files untouched.

## `DAT__ status`

Reports, per package/demand: `fresh | stale | not-run | no-interface`, the source that is newest, and the last-generated time. Report-only — no writes.
