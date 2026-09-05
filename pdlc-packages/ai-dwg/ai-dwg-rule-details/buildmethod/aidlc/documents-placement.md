<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Documents Placement — full narrative docs → `knowledge/documents/`

> **Load this file** during step 3 of the `aidlc/` emitter. It places the full, multi-page narrative documents where v2 can catalogue them. Authority: `common/aidlc-v2-output-contract.md` §3 + the placement table (§17 of the compatibility design).

## What goes here, and why it is different from `knowledge/<agent>/`

The per-agent knowledge files (`knowledge-routing.md`) are **derived reference summaries** — condensed, agent-scoped. This step places the **full original narrative documents** — the multi-page Architecture Package, Product Backlog Package, and UX Design Package originals — intact.

| Placed here | Source | Ownership |
|---|---|---|
| `aidlc/spaces/<space>/knowledge/documents/architecture-package.md` (+ its parts) | AI-ADLC AP | **User-owned** — v2 never moves or deletes anything here |
| `aidlc/spaces/<space>/knowledge/documents/product-backlog-package.md` | AI-POLC PBP | User-owned |
| `aidlc/spaces/<space>/knowledge/documents/ux-design-package.md` | AI-UXD UXP | User-owned |

These are placed for v2's **cataloguing tool** to index. They are the authoritative long-form; the agent-scoped summaries point back at them.

## The never-write boundary — `documentkb/`

⛔ **AI-DWG must NEVER write to `aidlc/spaces/<space>/knowledge/documentkb/`.** That is v2's cataloguing tool's territory — a **derived catalogue with an index, written transactionally**. Hand-writing into it corrupts the index. AI-DWG places the source documents in `documents/`; the team runs v2's catalogue command **once** to populate `documentkb/`. The split is deliberate:

| Directory | Writer | AI-DWG |
|---|---|---|
| `knowledge/documents/` | AI-DWG places source docs; user owns thereafter | ✅ writes |
| `knowledge/documentkb/` | v2's catalogue command (transactional, indexed) | ⛔ **NEVER** |

## Conditional emission

A document is placed only when its source package is present. Absent AI-UXD → no `ux-design-package.md`. The `documents/` directory itself is created only when at least one narrative document exists.

## Front-matter

Full narrative documents carry the standard provenance block (`generatedBy: AI-DWG`, `source`, `ownership: generated` at placement — the team may then edit, shifting ownership to `hybrid`/`user` on reconciliation).

---

*Developer-side design detail · AI-DWG `aidlc/` documents placement · © Mohammad Maheri*
