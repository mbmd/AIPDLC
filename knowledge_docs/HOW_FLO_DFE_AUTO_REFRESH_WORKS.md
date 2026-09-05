# How FLO → DFE Auto-Refresh Works

**Purpose:** Explains how the AI-Driven Flow Orchestrator (AI-FLO) keeps the AI-Driven Data Fabric Engine (AI-DFE) surface fresh **automatically** — by emitting a lightweight file-based signal whenever a package advances, which AI-DFE picks up and turns into a scoped data refresh — so dashboards stay current without anyone remembering to run `DAT__`.

---

## Who This Is For

Anyone who relies on the DFE data surface or a dashboard built on it, and wants it to reflect progress as it happens rather than only after a manual refresh.

---

## The Problem It Solves

AI-DFE gathers your Markdown into structured data on a `DAT__` run. Historically that was a manual step, or a timestamp-staleness check — which meant a dashboard could sit stale between refreshes. AI-FLO already knows the moment a package advances (a gate completes, or a stage changes). Auto-refresh connects those two facts: **FLO tells DFE what just changed, DFE refreshes exactly that.**

---

## The Mechanism — a File-Based Signal Inbox

The two engines are coupled through a **bilateral contract** (`data-refresh-signal@1.0`), not a new engine and not any always-loaded content. It mirrors the family's marker-based communication pattern: a producer writes a message, a consumer reads and archives it.

1. **FLO emits.** When a package advances, AI-FLO writes a small front-matter-only signal file to `{family}-ws/data/signals/` named `flo-refresh-{epoch-ms}.signal.md`. The signal records the family, entity, the **package that changed**, the event (`gate-complete` or `stage-advance`), and the marker file it observed.
2. **Fire-and-forget.** FLO writes the file and moves on — it never waits for DFE, never switches to DFE, never blocks. The file *is* the whole handoff.
3. **DFE consumes.** On its next pass, AI-DFE scans `signals/`, processes the signals **FIFO** (oldest epoch-ms first), and for each one runs a **scoped** `gather → shape → distribute` for just the package named in the signal.
4. **Archive.** Each processed signal is moved to `signals/processed/` (kept ~30 days as an audit trail).

Crucially, the `signals/` folder is a narrow, explicit **write exception**: AI-FLO may write signal files there and only there. Signals are **messages, never data products** — they never appear in the registry and are never served to a consumer. AI-DFE remains the sole writer of all actual data, preserving its single-writer integrity.

---

## How Often FLO Emits — the Granularity Setting

Each family sets `dfeRefreshGranularity` in its FLO overlay:

| Value | FLO emits when… | Best for |
|-------|-----------------|----------|
| `gate-only` **(default)** | a marker's `status` changes to `complete` | low-frequency dashboards; minimal I/O |
| `stage-advance` | any `stage`/`status` change within a running package | real-time dashboards tracking intra-package progress |
| `off` | never | families that don't use AI-DFE or prefer manual `DAT__` |

Each signal still triggers only a **scoped** refresh of the one advancing package, and DFE deduplicates signals that share the same package and timestamp, so even `stage-advance` stays cheap.

---

## Instant vs Next-Pass

By default, DFE processes pending signals on its **next activation** — a small delay. A workspace that wants **same-session, near-real-time** refresh can have a `PostFileCreate` hook installed that fires when a signal file appears and prompts DFE to process it immediately. That hook is generated into the consumer's workspace by the AI-Driven Governance & Compliance Engine (AI-GCE) only when both AI-FLO and AI-DFE are present; it is a latency optimization, and the file-based model works fully without it.

---

## Graceful Degradation

The mechanism **adds** freshness when both engines are present and **never breaks** either when the other is absent:

| Scenario | Behavior |
|----------|----------|
| AI-FLO not installed | No signals ever appear; DFE uses timestamp-staleness only (no regression). |
| AI-DFE not installed | Signals accumulate harmlessly; FLO never checks (fire-and-forget). |
| DFE offline for days | Signals accumulate; the next activation processes all pending FIFO — data catches up in one pass. |
| Malformed / unknown-version signal | Logged, archived with an error note; the remaining signals still process. |
| `dfeRefreshGranularity: off` | FLO emits nothing; DFE's timestamp fallback handles all staleness. |

A confirmed signal takes priority over the timestamp check, and the normal timestamp-staleness pass still runs afterward as a catch-all (for manual edits or changes made while FLO was inactive).

---

## What Stays the Same

- `DAT__` still works exactly as before — auto-refresh supplements it, never replaces it.
- AI-DFE remains the single writer of the data surface; FLO only writes messages into its declared inbox.
- Families that don't use AI-DFE, or prefer manual refreshes, set `off` and see no change.

---

## Related Documents

| Document | Location |
|----------|----------|
| How DFE Data Fabric Works | `knowledge_docs/HOW_DFE_DATA_FABRIC_WORKS.md` |
| How to Run the Data Fabric | `knowledge_docs/HOW_TO_RUN_THE_DATA_FABRIC.md` |
| How Flow Orchestrator Works | `knowledge_docs/HOW_FLOW_ORCHESTRATOR_WORKS.md` |
| How to Use the Dashboard | `knowledge_docs/HOW_TO_USE_THE_DASHBOARD.md` |
| How the Communication Fabric Works | `knowledge_docs/HOW_COMMUNICATION_FABRIC_WORKS.md` |

*Knowledge Document | Created: 2026-09-05 | Updated: 2026-09-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
