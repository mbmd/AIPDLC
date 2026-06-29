# AI-DFE — Design Rationale (PLAN)

**Package:** AI-DFE — AI-Driven Data Fabric
**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)

> **This is a summary, not the spec (Lesson 26).** The authoritative, step-by-step behavior lives in `ai-dfe-rules/core-engine.md`. This file records *why* DFE is shaped the way it is.

---

## Problem

The family produces rich output, but it is scattered across dozens of markdown files in per-project role folders. Anything that needs the data in bulk — a dashboard, a portfolio roll-up, an extension, a status query — has to know where every file lives and how to parse it. There was no structured handover layer and no single component that owns the data lifecycle. FLO routes but does not produce; packages produce but do not aggregate.

## Solution

AI-DFE is a continuous adaptive engine that owns one folder per family — `{family}-ws/data/` — and runs a three-phase loop:

| Phase | Stages | What |
|-------|--------|------|
| **Configure** | family-discovery · package-discovery · demand-discovery | Learn the family layout, each package's data interface, and what each consumer needs. Cache it (discover-once). |
| **Operate** | gather · shape · distribute · monitor · cross-project · cross-family | Read sources → per-package JSON (Layer 1); shape per-package JSON → consumer outputs (Layer 2); write to `data/`; monitor timestamps. |
| **Govern** | validation · freshness · history · cleanup | Validate against schemas, assess staleness, snapshot history, prune old snapshots. |

## Key Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | **Sole-writer of `data/`** | One writer eliminates merge conflicts and makes the data surface trustworthy (Principle 3). |
| 2 | **Distributed schemas** | Each package owns its `data-schema/` (`ai-{pkg}-rule-details/data-schema/`). DFE owns only aggregation/demand schemas. Keeps each package the authority on its own shape. |
| 3 | **Discover-once, monitor-continuously** | Reading package internals is expensive; timestamp checks are cheap. Cache discovery in `dfe-state.md`. |
| 4 | **Consumers declare DEMANDs** | Decouples consumers from source layout. They read `REGISTRY.json` → get a path → read clean JSON. |
| 5 | **Empty runtime bootstrap; samples in the package** | The installer creates an empty `data/`. Generic sample data lives in `templates/data-samples/` as reference/test fixtures (Decision 1A). |
| 6 | **Two triggers: `DAT__` + `DFA__`** | `DAT__` does work (produces/refreshes data); `DFA__` is a report-only quality agent. Clean separation of mutation vs. assessment (Decision 2B). |
| 7 | **Hook-free governance** | Convention + sole-writer ownership + the `DFA__` agent + the `ICG__` L3 invariant. No IDE hooks (Lesson 49). |
| 8 | **Family-scoped, single-active master** | Each family owns its `data/`. In multi-family setups one DFE is master; others go dormant (Lesson 113). Deferred until a 2nd family exists. |

## Relationship to FLO

FLO and DFE are peers. FLO decides *what happens next* (routing); DFE decides *where data lands and what shape it takes*. FLO never touches `data/`; DFE never routes. DFE reads FLO's own state (`flo-state.md`) to emit `flo-data.json`, the same way it reads every other package's markers.

## Source Design

Full design, open decisions, and gap history: the AI-DFE design document maintained during package development.
