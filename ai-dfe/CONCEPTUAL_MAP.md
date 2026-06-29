# AI-DFE — Conceptual Map (Navigation)

**Package:** AI-DFE — AI-Driven Data Fabric
**Version:** 1.0.0

> The navigational layer between the README (what it is) and the core engine (how it works) — Lesson 30. This is the authoritative file list.

---

## Reading Order

1. **`README.md`** — what AI-DFE is, family position, features.
2. **`PLAN.md`** — why it is shaped this way (design rationale).
3. **`ai-dfe-rules/core-engine.md`** — the spec: 3 phases, gate contract, persona, pipeline.
4. **`USER_GUIDE.md`** — how to run it day to day.
5. **`WHITEPAPER.md`** — the design narrative and the data-fabric idea.

---

## File Inventory

### Root (shared shell)

| File | Purpose |
|------|---------|
| `README.md` | Overview, family table, features, install |
| `LICENSE` · `NOTICE` | Apache 2.0 + attribution |
| `PLAN.md` | Design rationale (summary) |
| `CONCEPTUAL_MAP.md` | This file — navigation |
| `USER_GUIDE.md` | End-user walkthrough |
| `WHITEPAPER.md` | Design narrative |

### `ai-dfe-rules/`

| File | Purpose |
|------|---------|
| `core-engine.md` | Master orchestration (THE spec) + `§ Gate Contract` |

### `ai-dfe-rule-details/`

| Folder / File | Purpose |
|---------------|---------|
| `common/process-overview.md` | Phase map, interaction model, commands |
| `common/session-continuity.md` | Resume logic, `dfe-state.md` spec |
| `configure/family-discovery.md` | Stage 1 — read family table, map layout |
| `configure/package-discovery.md` | Stage 2 — read each package's SOURCE_MAP + schema, cache |
| `configure/demand-discovery.md` | Stage 3 — demander discovery: read `CONSUMER_REGISTRY.md`, resolve each consumer's `data-demand/` (+ ad-hoc drops) |
| `operate/gather.md` | Layer 1 — sources → per-package JSON |
| `operate/shape.md` | Layer 2 — per-package JSON → consumer output |
| `operate/distribute.md` | Write outputs + REGISTRY.json to `data/` |
| `operate/monitor.md` | Timestamp checks, staleness detection |
| `operate/cross-project.md` | Per-project roll-up across `projects/` |
| `operate/cross-family.md` | Master-mode multi-family aggregation |
| `govern/validation.md` | Schema validation before write |
| `govern/freshness.md` | Staleness/lag assessment |
| `govern/history.md` | Millisecond-timestamped snapshots |
| `govern/cleanup.md` | Retention + `DAT__ cleanup` |
| `data-schema/dfe-data.schema.json` | DFE's own output shape |
| `data-schema/SOURCE_MAP.md` | DFE's own source declaration |
| `data-schema/SCHEMA_README.md` | DFE's own schema docs |

### `ai-dfe-rule-details/templates/`

| File | Purpose |
|------|---------|
| `dfe-state.md` | State file template (discovery + demand registry) |
| `CONSUMER_REGISTRY.md` | Consumer registry template — demander index (runtime copy lives at `{family}-ws/data/`) |
| `DATA_INTERFACES.md` | Human-readable manifest of all data files |
| `SOURCE_MAP.md` | Template every package uses to declare its sources |
| `demand-template.md` | Template every consumer uses to declare its needs |
| `data-samples/` | Generic sample data + schemas (reference/test fixtures) |
| `agents/data-fabric-health-check.md` | `DHC__` readiness check (DFE-AG-02) — "can DFE operate here?" |
| `agents/data-fabric-agent.md` | `DFA__` integrity agent (DFE-AG-01) — 18 checks / 5 categories |
| `agents/shortcut-rules-block.md` | Marker-fenced shortcut rules for workspace-rules (`DHC__` + `DFA__`) |

### `setup/`

| File | Purpose |
|------|---------|
| `INSTALL.md` | Multi-platform install guide |

---

## Trigger Map

| Trigger | What |
|---------|------|
| `_DFE_` | Activate AI-DFE |
| `_ACTIVE_` | Report active package (read-only) |
| `DAT__` | Data operations (gather/shape/distribute/discover/aggregate/cleanup/master) |
| `DHC__` | Data-fabric health check — bootstrap readiness ("can DFE run here?"), report-only |
| `DFA__` | Data-fabric integrity agent — 18 checks / 5 categories, report-only |
