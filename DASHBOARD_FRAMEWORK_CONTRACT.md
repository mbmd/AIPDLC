# Dashboard Framework — Shared Cross-Package Contract

**Version:** 1.0.0
**Date:** 2026-06-10
**Author:** Maheri
**Authored under:** `#persona-process-designer` (lead) + `#persona-compliance-governance` (support)
**Status:** ADOPTED (2026-06-10, Plan Phase 2.3)
**Sibling:** `MANAGEMENT_FRAMEWORK_CONTRACT.md` v1.1.0 (governance spine — registers)
**Plan:** `ai-packagebuilder/sessions-open-items/DASHBOARD_FRAMEWORK_PLAN.md` (full vision, Phases A–F)

---

## 1. Purpose

Every AI-* family package produces governance, quality, or status information that benefits from a **visual roll-up** — a dashboard. Today one exists (AI-GCE's `compliance-dashboard.md`), placed ad hoc in `docs/`. This contract defines a single, consistent convention:

> **All dashboards live flat in `management_framework/dashboards/`**, attributed by `generatedBy` provenance front-matter (per `NAMING_AND_OWNERSHIP.md` §5). No per-package subfolders. No filename prefixes. One folder, one index, all packages contribute.

This is a **shared artifact contract** — the same stance as `MANAGEMENT_FRAMEWORK_CONTRACT.md`. No package "owns" or renders another's dashboard.

---

## 2. One Root, Two Mutually-Exclusive Operating Modes

The `management_framework/` root serves both project-level and portfolio-level work because the two are **mutually exclusive** — the user is in one mode or the other, never both simultaneously:

| Mode | Who is operating | What `management_framework/dashboards/` holds |
|------|------------------|-----------------------------------------------|
| **Project mode** | One project, end-to-end (all packages active) | Per-project dashboards — **flat** (one project, no subfolders) |
| **Portfolio mode** | Portfolio level (governing many projects, not descending to implementation) | Portfolio dashboards (PPM/FLO/ILC) **flat** + each project's dashboards under `{Project ID}/` |

Because the modes never coexist, per-project and portfolio records are never mixed in one flat list — the spine contract's per-project scope is preserved.

### 2.1 Project Mode Layout

```
management_framework/
├── MANAGEMENT_FRAMEWORK.md                ← spine marker (existing)
├── dashboards/
│   ├── DASHBOARDS.md                      ← dashboard hub marker + index
│   ├── compliance-dashboard.md            ← generatedBy: AI-GCE
│   ├── quality-dashboard.md              ← generatedBy: AI-TGE
│   ├── project-status-dashboard.md       ← generatedBy: AI-PILC
│   ├── architecture-dashboard.md         ← generatedBy: AI-ADLC
│   ├── ux-dashboard.md                   ← generatedBy: AI-UXD
│   ├── backlog-dashboard.md             ← generatedBy: AI-POLC
│   └── readiness-dashboard.md            ← generatedBy: AI-DWG (optional snapshot)
└── (registers: Decision_Log.md, etc.)
```

### 2.2 Portfolio Mode Layout

```
management_framework/
├── MANAGEMENT_FRAMEWORK.md
├── Portfolio_Register.md                  ← AI-PPM
├── dashboards/
│   ├── DASHBOARDS.md                      ← hub marker + index
│   ├── portfolio-dashboard.md            ← generatedBy: AI-PPM (flat, portfolio-level)
│   ├── flow-dashboard.md                ← generatedBy: AI-FLO (flat, portfolio-level)
│   ├── idea-pipeline-dashboard.md        ← generatedBy: AI-ILC (flat, portfolio-level)
│   ├── {Project-ID-A}/                   ← per-project partition (the ONLY subfolder)
│   │   ├── compliance-dashboard.md       ← generatedBy: AI-GCE
│   │   ├── quality-dashboard.md          ← generatedBy: AI-TGE
│   │   └── ...                           (same flat set as §2.1, for this project)
│   └── {Project-ID-B}/
│       └── ...
└── (registers)
```

The **only** subfolder in the convention is `{Project ID}/`, and it appears **only** in portfolio mode with more than one project. Everything else is flat, attributed by `generatedBy`.

---

## 3. Detection by Marker (Lesson 14)

| Element | Value |
|---------|-------|
| **Hub folder** | `management_framework/dashboards/` |
| **Hub marker** | `dashboards/DASHBOARDS.md` |
| **Detection strategy** | Scan for `DASHBOARDS.md` inside the management_framework folder (which is itself detected by its own marker per the spine contract §3) |

The user chooses WHERE the management_framework lives. This contract defines WHAT must exist inside `dashboards/`.

---

## 4. Contribution Behavior

Every package that emits a dashboard follows the same rule:

```
1. DETECT the dashboard hub (by marker — dashboards/DASHBOARDS.md).
2. IF the hub exists:
      → CREATE (or refresh) only this package's own dashboard FILE in dashboards/.
      → Register/refresh this package's row in the hub index.
      → NEVER read-modify-delete another package's file.
3. IF no hub exists:
      → CREATE dashboards/ + DASHBOARDS.md marker + this package's dashboard file.
      → Self-contained standalone (Lesson 6).
4. Refresh = overwrite own `ownership: generated` file only.
   Human-authored notes within `<!-- custom -->` markers are preserved (Lesson 45 / DWG Rule 6).
```

---

## 5. Hub Index Schema (`DASHBOARDS.md`)

```markdown
<!-- Dashboard hub | contract v1.0.0 -->

# Dashboards

Consolidated dashboard hub for **{project_name}** (Project ID: `{project_id}`).
Each AI-* package contributes its own dashboard here, identified by `generatedBy` front-matter.

## Contributing Dashboards

| Dashboard | File | Producer | Scope | Last Refreshed |
|-----------|------|----------|-------|:--------------:|
| Compliance | compliance-dashboard.md | AI-GCE | Per-project | {date} |
| Quality | quality-dashboard.md | AI-TGE | Per-project | {date} |

## Conventions
- One file per package, named by concern (`{concern}-dashboard.md`).
- Producer identified by `generatedBy` front-matter (not by filename or folder).
- Dashboards are regenerated (not hand-maintained) — `ownership: generated`.
- Filter by `generatedBy` to identify a package's contribution.
- Detection: this file's presence means "a dashboard hub exists here."
```

---

## 6. Provenance Front-Matter (per NAMING_AND_OWNERSHIP.md §5.2)

Every dashboard carries:

```yaml
---
generatedBy: AI-TGE
generatedVersion: 1.0.0
source: .tge/coverage-report.md, .tge/debt-scorecard.md
generatedOn: {date}
ownership: generated
projectId: {Project ID}
---
```

- `ownership: generated` — tool-regenerated on each refresh cycle.
- `projectId` — the immutable identifier minted at AI-PILC Stage 1 (Lesson 43); enables portfolio roll-up.
- `source` — upstream data file(s) that feed this dashboard.

---

## 7. Dashboard Inventory

### 7.1 Per-Project Dashboards

| Package | File | Class | What It Shows |
|---------|------|:-----:|---------------|
| AI-GCE | `compliance-dashboard.md` | Existing (relocate) | Tier progress, compliance score, rules/hooks inventory, active exceptions, MTTR, top violations |
| AI-TGE | `quality-dashboard.md` | Recommended | Coverage by commitment/component/risk, debt summary, open defects, trend |
| AI-PILC | `project-status-dashboard.md` | Extended | Open issues, top risks, recent decisions, action items, milestone RAG |
| AI-ADLC | `architecture-dashboard.md` | Extended | ADR status, requirement→component coverage, architecture risks, extension map |
| AI-UXD | `ux-dashboard.md` | Extended | Design-system coverage, accessibility baseline status, persona/journey/flow coverage |
| AI-POLC | `backlog-dashboard.md` | Extended | Priority distribution, DoR/DoD status, value-vs-effort, release readiness |
| AI-DWG | `readiness-dashboard.md` | Optional | One-time workspace readiness scorecard (point-in-time, not maintained) |

### 7.2 Portfolio Dashboards

| Package | File | Class | What It Shows |
|---------|------|:-----:|---------------|
| AI-PPM | `portfolio-dashboard.md` | Recommended | Cross-project health: phase/stage, progress %, RAG, top risks, prioritization, capacity |
| AI-FLO | `flow-dashboard.md` | Recommended | Pipeline view: where each project sits in the chain, next hop, pending handoffs |
| AI-ILC | `idea-pipeline-dashboard.md` | Optional | Idea funnel: captured → shaped → evaluated → approved/parked/rejected |

---

## 8. Roll-Up Wiring (Per-Project → Portfolio)

In portfolio mode, AI-PPM aggregates a **standard roll-up snapshot** from each project's dashboards, keyed by `Project ID`:

| Roll-Up Field | Per-Project Source |
|---------------|--------------------|
| Phase / Stage | Active `*-state.md` + AI-FLO `flow-state.md` position |
| Progress % | Completed vs. total stages in active state file |
| RAG / Health | Derived from open issues + risk exposure + schedule |
| Top Risks | Spine `Issue_Log.md` (severity H) + risk register |
| Open Issues | Spine `Issue_Log.md` (Status = Open) |
| Milestone Status | Charter milestones vs. actuals |
| Last Updated | Latest dashboard/state timestamp |

**Flow:** per-project dashboards (PILC/GCE/TGE) emit snapshot → AI-FLO carries position → AI-PPM aggregates into `portfolio-dashboard.md`. Keyed by `Project ID` (Lesson 43).

---

## 9. Shared Conventions

1. **Detection-by-marker** (Lesson 14) — `dashboards/DASHBOARDS.md` is the hub marker.
2. **Append-if-exists / create-if-absent** — same pattern as the spine (§4).
3. **Provenance is the ownership mechanism** — `generatedBy` front-matter identifies the producer (no subfolders, no prefixes). Keys: `generatedBy`, `generatedVersion`, `source`, `generatedOn`, `ownership`, `projectId` (camelCase, locked v1.0.1).
4. **Project-ID keyed** — every per-project dashboard records `projectId` for portfolio correlation.
5. **Silent-when-complete** — dashboards exist always, but engines only speak when there's something to report.
6. **100% generic templates** — `{placeholder}` syntax; no project-specific content.
7. **Non-destructive refresh** — overwrite only the owning package's `ownership: generated` file; preserve `<!-- custom -->` sections.
8. **RAG + freshness standard** — shared legend (🔴 Red / 🟡 Amber / 🟢 Green); `Last refreshed` timestamp; staleness note when source is newer than dashboard.
9. **One index per root** — `DASHBOARDS.md` lists Contributing Dashboards (the human entry point).
10. **Standalone honored** — a package run alone still produces its dashboard in `dashboards/`; the hub degrades gracefully to a single contributor.

---

## 10. Boundaries (What This Contract Does NOT Do)

1. **Not a package.** A shared artifact contract only — no orchestration of packages.
2. **Does not replace the spine registers.** Dashboards *visualize/roll up* registers and state files; registers remain the source of truth.
3. **Does not enforce anything at runtime.** Enforcement is AI-GCE; testing is AI-TGE; dashboards are the *report*.
4. **Does not hardcode location.** WHERE the management folder lives is always the user's choice.
5. **Does not aggregate at the edge.** AI-FLO carries position only; aggregation is AI-PPM's job.
6. **Not portfolio governance.** The portfolio *register* (managing many projects) is AI-PPM's contract, not this one.

---

## 11. Execution Phases (Build-Gated)

| Phase | What | Gated By |
|-------|------|----------|
| A | ✅ This contract + spine amendment (Plan 2.3) | Done |
| B | Relocate AI-GCE dashboard into `dashboards/` | Phase A (done); GCE exists today |
| C | AI-TGE quality dashboard template | Phase A; AI-TGE build |
| D | AI-PPM/AI-FLO portfolio dashboards | AI-PPM/AI-FLO builds (Phase 4.1) |
| E | Extended per-project dashboards (PILC, ADLC, UXD, POLC, DWG) | Each package's build/update |
| F | Cross-cutting wiring + FAMILY_STRUCTURE trees | After B–E land |

---

*Contract Version: 1.0.0 | Created: 2026-06-10 | Authored under #persona-process-designer + #persona-compliance-governance*
