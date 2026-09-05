<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Observability Spine — preserved in full; the one overlap is read-and-persist

> **Load this file** when `buildProfile: aidlc` and a check runs as a v2 sensor rather than an AI-GCE hook. This is Improvement 8. It states the one narrow change to AI-GCE's observability spine under `aidlc` — and, just as importantly, everything that does **not** change. Ledger rows A1–A9 (A9 is the audit-event mapping this file carries). Resolved once here; `build-method-resolution.md` points at it.

## The spine is preserved in full — this is the default, the change is the exception

AI-GCE's observability spine is a deliberate capability: **log every deviation and every drift silently, monitor them on a dashboard — silent when compliant, complete when audited.** Under `buildProfile: aidlc`, **the spine is retained in full.** v2's native audit does **not** replace it, for four reasons:

| | v2's audit | AI-GCE's spine |
|---|---|---|
| **Scope** | Per **work item** — events land in that intent's audit shard; logs only what happens *inside a v2 workflow* | **Continuous** — a developer editing a file outside any v2 workflow is most of their day, and v2 sees none of it |
| **Aggregation** | **None** — an append-only event stream; no score, no rating, no trend, no roll-up | Score, four-band rating, trend history, dashboard |
| **Drift** | Its health check compares *policy text* between org and project rule layers | The drift register tracks whether the **implementation diverged from the design baseline** — a different question; v2 has no equivalent |
| **Permanence** | Shards live with the intent, scoped to its lifetime | JSONL, git-committed, built for an auditor to query months later |

**Part-by-part, what stays under `aidlc`:**

| Part | Under `aidlc` |
|---|---|
| Silent-when-compliant | ✅ Kept (a principle; v2 sensors behave the same way) |
| Deviation logging **outside** a v2 workflow | ✅ Kept — v2 is blind here |
| Drift register | ✅ Kept entirely — no v2 equivalent |
| Score, rating, trend | ✅ Kept entirely — v2 has no aggregation layer |
| Compliance dashboard | ✅ Kept entirely — the monitoring surface; nothing in v2 substitutes |
| Dual score (overall vs new-code) | ✅ Kept entirely — v2 treats every file identically |
| Deviation logging for a check running **as a v2 sensor** | ⚠️ **The one genuine overlap — narrowed below** |

> **Reconciling with frozen contract §7.** §7 says AI-GCE, under `aidlc`, does not generate its own *compliance-log-and-process-agent* apparatus as a *primary* audit for what v2 already audits natively. Improvement 8 is the precise reading of that: the *permanent aggregating spine* (score / trend / drift / dashboard / queryable JSONL) is **kept** — what is narrowed is only the re-execution of a check v2's sensor already ran. §7 removes redundant *re-running*, not the observability spine.

## The one narrow change — read and persist, do not re-run

Where a check runs as a **v2 sensor**, AI-GCE does **not** re-run it and write a second event. Instead:

> AI-GCE **reads v2's audit outcome for that check and persists the derived compliance event into its own log** — rule ID, severity, timestamp, result, detail pointer.

**This is not double-logging, and the distinction is load-bearing.** v2's shard is an event stream scoped to a work item; AI-GCE's log is a **permanent, queryable audit record**. If the dashboard read v2's shards live, it would lose history the moment an intent was archived, and the trend line would break. Persisting the derived event keeps the permanent trail permanent — and the dashboard gains a window into v2 workflow activity it previously had no visibility into at all.

**Rule 5 (every action logged) survives intact — a clarification, not an exception:** nothing goes unlogged; where v2 has already established an outcome, AI-GCE **records that outcome rather than re-deriving it**.

## The audit-event mapping (ledger A9) — the scoping task this carries

Before the read-and-persist path can run, v2's audit taxonomy must be mapped onto AI-GCE's compliance-event schema. v2's taxonomy is large (a ~91-event set); AI-GCE's compliance log has a fixed event vocabulary (`CHECK` / `EXCEPTION` / `REMEDIATION` / `AUDIT` / `REDERIVATION`). The mapping is a **projection**: each v2 sensor-outcome event type maps to an AI-GCE `CHECK` event with the fields below.

**Derived-event shape (persisted into AI-GCE's JSONL log):**

| AI-GCE field | Source in v2's audit outcome |
|---|---|
| `eventType` | Always `CHECK` (a v2 sensor firing is a check outcome) |
| `ruleId` | The AI-GCE rule ID the sensor was rendered from (the sensor manifest carries it — contract §4) |
| `result` | v2's fired/passed/failed → `pass` / `fail` |
| `severity` | The rule's severity from its AI-GCE generator (not re-derived from v2) |
| `timestamp` | v2's event timestamp (the outcome's time, not the persist time) |
| `evidence` / `detailPointer` | A pointer into v2's audit shard for that event — not a copy of the payload |
| `source` | `aidlc-sensor` (marks the event as read-and-persisted, not hook-executed — so an auditor can tell the provenance) |

**Mapping rules:**
- **One v2 sensor outcome → one AI-GCE `CHECK` event.** Never fan out; never collapse two outcomes into one.
- **Unmapped v2 event types are ignored, not guessed.** A v2 event with no AI-GCE rule behind it (v2's own internal workflow events) is not persisted — AI-GCE logs only its own governed rules' outcomes.
- **The `source: aidlc-sensor` tag is mandatory** on every derived event, so the dashboard and any auditor can distinguish a read-and-persisted outcome from a hook-executed one.

Under every **non-`aidlc`** build method there are no v2 sensors, so nothing is read-and-persisted — checks run as AI-GCE hooks and log directly, exactly as before.

---

*Developer-side design detail · AI-GCE observability read-and-persist · © Mohammad Maheri*
