# AI-DFE — AI-Driven Data Fabric

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**License:** Apache 2.0 with Attribution

---

## What Is AI-DFE?

AI-DFE is the data layer of the AI-* PDLC Family. It gathers the scattered markdown outputs every package produces, shapes them into structured JSON per consumer needs, and distributes them to one read-point — so dashboards, extensions, and reports get clean, machine-readable data without ever knowing where the raw files live.

**In one sentence:** AI-DFE turns the family's scattered, human-readable outputs into a single governed, machine-readable data surface — gather, shape, distribute.

**Tagline:** *Fabric it.*

---

## Family Position

AI-DFE is part of **AIFLC** (AI Full Life Cycle) and the **AI-* PDLC Family**. Like AI-FLO, it lives in **every family** as a continuous adaptive engine — but where FLO routes decisions, DFE fabrics data. It owns one folder, `pdlc-ws/data/`, and is its sole writer.

```
╔════════════════ PORTFOLIO LAYER · scope = MANY projects ════════════════╗

   (optional)
    AI-ILC  ⇢  AI-PILC  ⇢  AI-PPM
    Decide it   Initiate it   Govern it (portfolio of N projects)

╚═════════════════════════════════╤═══════════════════════════════════════╝
                                   │
                                AI-FLO   Route it — package-to-package
                                   │     flow on the edge between layers
╔════════════════ PROJECT LAYER · scope = ONE project ════════════════════╗

    AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG ──► AI-DLC v1 (build) ¹
    Own it      Design UX   Design it   Prepare it       ▲
                                                         │
                        AI-POLC ⇄ AI-DLC v1 (back-and-forth)┘
                AI-DLC v1 ⇢ AI-UXD+AI-POLC (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC v1 (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC v1 = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-POLC** ³ | Interactive workflow (lifecycle) | PIP | Product Backlog Package (PBP) |
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP + PBP | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | PIP + PBP + UXP | Architecture Package (AP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC v1** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POLC) | Working Software |

> ¹ **AI-DLC v1** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC v1 consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ All packages in this table are **built**. AI-PPM (portfolio engine), AI-FLO (router), AI-POLC (product ownership lifecycle), and AI-UXD (UX design lifecycle) were the last four — completed June 2026. Within the Project layer, **AI-POLC, AI-UXD, and AI-ADLC run sequentially** (POLC→UXD→ADLC) — each feeds the next, culminating at AI-DWG which receives all three outputs (AP + PBP + UXP). **AI-GCE and AI-TGE run alongside AI-DLC v1** as continuous quality engines; **AI-POLC ⇄ AI-DLC v1** exchange backlog/acceptance throughout delivery; and **AI-DLC v1 runtime feedback flows back to both AI-UXD and AI-POLC**. Feedback loops (ADLC→POLC cost/risk, ADLC→UXD constraints) provide iterative refinement without changing the forward sequence.

> **Note on AI-DFE's table row:** AI-DFE is a continuous data-fabric engine that operates *alongside* the whole family (like AI-FLO, it is not a chain link). Its formal row is added to the canonical family table during family-governance integration; the diagram and table above are reproduced verbatim from the family canonical (`FAMILY_TABLE_MAP.md`) and are never improvised.

---

## Where AI-DFE Sits in the Chain

AI-DFE is a **fabric engine**, not a chain step — the family's **data layer**. Like AI-FLO it runs *alongside* the whole family rather than as a linear stage, but where FLO carries *decisions*, DFE carries *data*: it gathers every package's scattered Markdown output, shapes it into schema-validated JSON, and distributes it to one governed read-point so dashboards, extensions, and reports never touch raw source files. It owns exactly one folder — `{family}-ws/data/` — and is its sole writer.

| Aspect | AI-DFE |
|--------|---------|
| **Role** | Universal fabric data layer — gather → shape → distribute |
| **Position** | Alongside the whole family (a continuous engine); not a chain row |
| **Reads (input)** | Every package's output marker (`*` wildcard) + each consumer's declared `data-demand/` |
| **Produces (output)** | Schema-validated JSON under `{family}-ws/data/` — per-package (Layer 1) + demand-shaped (Layer 2) — indexed by `REGISTRY.json` |
| **Output marker** | `dfe-state.md` |
| **Correlation key** | Preserves each package's `projectId` in the data it shapes |
| **Capability emitted** | `data-surface@1` (internal — a consumption surface, not a chain deliverable) |
| **Capability consumed** | `*` (all marker types, as gather triggers) |
| **Territory** | Sole owner + sole writer of `{family}-ws/data/`; never writes into another package's folder |
| **Family footprint** | Cloned into every family at assemble — one canonical family-agnostic engine, family scope resolved from `{family}` tokens |

AI-DFE answers **"what does every package currently hold, in one clean machine-readable place?"** Producers and consumers are fully decoupled: a producer just emits its normal Markdown; a consumer declares a DEMAND and reads `REGISTRY.json` — neither knows where the other's files live.

### Standalone vs. chained

- **Additive, never required.** Nothing in the family depends on DFE to function — packages produce their Markdown outputs with or without it. DFE adds a machine-readable surface on top; remove it and the family still runs.
- **Discover-once, monitor-continuously.** It reads each package's data interface once (cached in `dfe-state.md`), then only checks timestamps — a missing or unrun package becomes a `null` field, never an error.
- **Schema-first, single-writer.** Every file validates against a schema before it is written; only DFE writes to `data/`, and every write is snapshotted into `history/` with a millisecond timestamp.
- **Family-scoped.** Each family owns its own `data/`; cross-family exchange reads the neighbour's surface, never mixes territories.

---

## Features

- **3 phases** — Configure (discover) → Operate (gather, shape, distribute, monitor) → Govern (validate, freshness, history, cleanup)
- **Two-layer pipeline** — sources → per-package JSON (Layer 1) → demand-shaped consumer output (Layer 2)
- **Single-writer territory** — DFE is the sole owner and sole writer of `pdlc-ws/data/`
- **Discover-once, monitor-continuously** — reads each package's interface once, then only checks timestamps
- **Consumer decoupling** — consumers declare a DEMAND; they never touch raw source files
- **REGISTRY.json discovery** — every consumer reads ONE fixed path to find all its data
- **Schema-first** — every data file validates against a JSON Schema (per-package + DFE-owned aggregations)
- **Historical snapshots** — millisecond-timestamped history with retention + cleanup
- **Graceful degradation** — a missing source becomes a `null` field, never an error
- **Multi-family ready** — single-active master mode for operating several families' data from one seat (deferred until a 2nd family exists)
- **`DAT__` operations trigger** — gather/shape/distribute/discover/aggregate/cleanup/master
- **`DHC__` data-fabric health check** — bootstrap readiness check ("can DFE operate in this workspace?"); the data-layer analogue of AI-FLO's `FHC__`. Run it first. Read-only.
- **`DFA__` data-fabric integrity agent** — standalone integrity pass, 18 checks across 5 categories (schema / registry / manifest / freshness / territory); the data-layer analogue of AI-FLO's `FIA__`. Reports, never writes.
- **Hook-free governance** — convention + sole-writer ownership + agent, no IDE hooks

---

## Activation

**Explicit key:** type `_DFE_` in any prompt to activate AI-DFE unambiguously — even when other AI-* packages share the workspace. The status key `_ACTIVE_` reports which package is currently active. A package switch never happens without your explicit key or confirmation, and any switch is announced on the first line of the response (`Active package: AI-DFE`). See [`../TRIGGER_KEYS_REFERENCE.md`](../TRIGGER_KEYS_REFERENCE.md) for the full family key table.

**Operations:** `DAT__` runs data operations (e.g. `DAT__ all`, `DAT__ pdlc/pilc`, `DAT__ status`). **Quality:** `DFA__` runs the data-fabric quality agent (report-only).

---

## Installation

AI-DFE is pure Markdown — no runtime, no dependencies, no build step. "Installing" it means placing two folders and one always-loaded router file where your AI agent reads them, plus a one-time bootstrap of its runtime territory (`{family}-ws/data/`). (What AI-DFE then *produces* — schema-validated JSON — is written into that territory at run time.)

> **Fabric-engine note.** AI-DFE ships **inside every AI-* family** — if you installed the family, DFE is already present and its territory is bootstrapped. Install it **directly** (below) only to add the data layer to a workspace that has other AI-* packages but no DFE yet.

### The model (read this first)

Installation writes to four places:

1. **The package home** — `ai-dfe-rules/` (the core **engine/dispatcher**) and `ai-dfe-rule-details/` (configure / operate / govern stages, data-schema, and templates, read on demand) are copied into `.aiflc/pdlc/`. This path is **identical on every platform**.
2. **One always-loaded orchestrator** — a single small router placed in your platform's native auto-load slot. It is the *only* file that loads automatically; it `Read`s the AI-DFE core on demand when you activate the engine.
3. **The runtime territory** — a one-time bootstrap of `{family}-ws/data/` (empty `REGISTRY.json`, empty `CONSUMER_REGISTRY.md`, a template `dfe-state.md`, and empty `demands/` + `history/` folders). The family installer does this automatically.
4. **The agents** — DFE's two report-only agents (`DHC__`, `DFA__`) plus their shortcut block.

### Option A — Install alongside the family (recommended)

Use the family installer to place AI-DFE and bootstrap its territory:

```powershell
# Windows (PowerShell)
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-dfe"
```

```bash
# macOS / Linux
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-dfe
```

Supported `-Platform` values: `kiro`, `cursor`, `claude-code`, `cline`, `amazonq`, `copilot`. The installer creates `{family}-ws/data/` with an empty registry so DFE is ready to populate on first run.

### Option B — Install this engine individually (manual)

Copy the two package folders into the uniform home (same on every platform):

```
ai-dfe/ai-dfe-rules/        →  <workspace>/.aiflc/pdlc/ai-dfe-rules/
ai-dfe/ai-dfe-rule-details/ →  <workspace>/.aiflc/pdlc/ai-dfe-rule-details/
```

Then place the always-loaded orchestrator (`session-orchestrator.md`, from the packages root) in your platform's slot:

| Platform | Orchestrator destination | How it loads |
|----------|--------------------------|--------------|
| **Kiro** | `.kiro/steering/session-orchestrator-pdlc.md` | Auto-loaded steering |
| **Amazon Q** | `.amazonq/rules/pdlc/session-orchestrator.md` | Auto-loaded rule |
| **Cursor** | `.cursor/rules/pdlc-session-orchestrator.mdc` | Add `alwaysApply: true` frontmatter |
| **Cline** | `.clinerules/pdlc-session-orchestrator.md` | Auto-loaded rule |
| **Claude Code** | `CLAUDE_PDLC_ORCHESTRATOR.md` | Import from root `CLAUDE.md` via `@CLAUDE_PDLC_ORCHESTRATOR.md` |
| **GitHub Copilot** | `.github/copilot-instructions-pdlc-orchestrator.md` | Workspace instructions |
| **Codex / VS Code agent** | `AGENTS.md` (workspace root) | Auto-loaded agent instructions |

Then bootstrap the territory and register the agents:

- Create `{family}-ws/data/` with an empty `REGISTRY.json`, an empty `CONSUMER_REGISTRY.md` (from `ai-dfe-rule-details/templates/CONSUMER_REGISTRY.md`, no rows), a template `dfe-state.md`, and empty `demands/` + `history/` folders.
- On Kiro, copy the agents (`DHC__`, `DFA__`) into `.kiro/agents/` and append their shortcut block into `workspace-rules.md`; on other platforms, register the shortcut block in your workspace rules.

### For AI agents — machine-readable install manifest

An AI assistant can install AI-DFE by parsing and executing the block below. All `copy.from` and `orchestrator.source` paths are relative to `source_root`; every destination is relative to the workspace root. Pick the one `orchestrator.slot` row that matches the target platform. The manifest is **platform-agnostic** — everything except `orchestrator.slot` is identical on every platform.

```yaml
# AIFLC INSTALL MANIFEST — AI-DFE
package: AI-DFE
family: pdlc                       # package home: .aiflc/pdlc/
version: 1.0.0
runtime: none                      # pure Markdown; no deps, no build
role: fabric-engine                # ships in every family; the family's data layer
source_root: pdlc-packages/        # clone root of the AIPDLC repo
activation_phrase: "Using AI-DFE, gather and publish the family data"
trigger_key: "_DFE_"               # universal explicit key (recognized by the orchestrator on any platform); or use activation_phrase
status_key: "_ACTIVE_"             # reports which package is currently active
operations_key: "DAT__"            # data operations (e.g. DAT__ all, DAT__ status)
depends_on: []                     # standalone-capable; advisory — degrades gracefully to null on missing sources
consumes_capability: "*"           # all marker types present, as gather triggers
emits_capability: "data-surface@1" # internal — a consumption surface, not a chain deliverable
output_marker: dfe-state.md
output_dir: pdlc-ws/data/          # sole-writer territory; JSON surface written here at run time
copy:
  - from: ai-dfe/ai-dfe-rules
    to: .aiflc/pdlc/ai-dfe-rules
  - from: ai-dfe/ai-dfe-rule-details
    to: .aiflc/pdlc/ai-dfe-rule-details
orchestrator:
  source: session-orchestrator.md            # the ONLY always-loaded file
  source_claude: session-orchestrator.claude.md   # use this source for claude-code
  slot:
    kiro: .kiro/steering/session-orchestrator-pdlc.md
    amazonq: .amazonq/rules/pdlc/session-orchestrator.md
    cursor: .cursor/rules/pdlc-session-orchestrator.mdc   # + frontmatter alwaysApply: true
    cline: .clinerules/pdlc-session-orchestrator.md
    claude-code: CLAUDE_PDLC_ORCHESTRATOR.md              # import from root CLAUDE.md
    copilot: .github/copilot-instructions-pdlc-orchestrator.md
    codex: AGENTS.md
    vscode: AGENTS.md
core_entry: .aiflc/pdlc/ai-dfe-rules/core-engine.md       # orchestrator Reads this on activation
rule_details_home: .aiflc/pdlc/ai-dfe-rule-details/       # core resolves these on demand
bootstrap_territory:               # one-time; the family installer does this automatically
  dir: pdlc-ws/data/
  create:
    - REGISTRY.json                # empty index
    - CONSUMER_REGISTRY.md         # from templates/, no rows
    - dfe-state.md                 # from template
    - demands/                     # empty
    - history/                     # empty
agents:                            # report-only; Kiro → .kiro/agents/, others → shortcut blocks
  - trigger: "DHC__"               # data-fabric health check — run first (read-only)
  - trigger: "DFA__"               # data-fabric integrity agent (18 checks / 5 categories)
verify:
  - path_exists: .aiflc/pdlc/ai-dfe-rules/core-engine.md
  - path_exists: pdlc-ws/data/REGISTRY.json
  - orchestrator_present_in_platform_slot: true
  - action: 'type "DHC__" and expect a readiness verdict, then "DAT__ all" to populate the surface'
```

### Verify

1. Open the target workspace in your IDE with the AI agent active.
2. Confirm the orchestrator loaded (Kiro: it appears in the Steering panel).
3. Run the health check: type `DHC__` — expect a readiness verdict (HEALTHY / DEGRADED / NOT READY / IDLE).
4. Populate the surface: `DAT__ all` — AI-DFE gathers from every installed package and writes `pdlc-ws/data/REGISTRY.json` + per-package `{pkg}-data.json`. Use `DFA__` for a report-only integrity pass.

For the full per-platform walkthrough, see [setup/INSTALL.md](./setup/INSTALL.md) and the family-wide [INSTALL_GUIDE.md](../../INSTALL_GUIDE.md).

---

## Usage

1. Open a workspace where AI-* packages have produced output
2. Start a chat and run the data trigger:
   ```
   DAT__ all
   ```
3. AI-DFE gathers data from every installed package, shapes it per consumer demands, and distributes structured JSON to `{family}-ws/data/`
4. Use `DAT__ full` for a complete-set pass with a readiness report, `DAT__ status` for a staleness check, or `DFA__` for a report-only quality assessment
5. Consumers (e.g. the dashboard) read the data via `REGISTRY.json`

## File Structure

```
ai-dfe/
├── README.md                          ← This file
├── LICENSE  ·  NOTICE                 ← Apache 2.0 + Attribution
├── PLAN.md  ·  CONCEPTUAL_MAP.md      ← rationale + navigation
├── USER_GUIDE.md  ·  WHITEPAPER.md    ← walkthrough + design narrative
├── ai-dfe-rules/
│   └── core-engine.md                 ← Master orchestration engine (read on demand by the orchestrator) + § Gate Contract
├── ai-dfe-rule-details/
│   ├── common/                        ← process-overview, session-continuity
│   ├── configure/                     ← Phase 1: family / package / demand discovery
│   ├── operate/                       ← Phase 2: gather, shape, distribute, monitor, cross-project, cross-family
│   ├── govern/                        ← Phase 3: validation, freshness, history, cleanup
│   ├── data-schema/                   ← DFE's own data interface (reports on itself)
│   └── templates/                     ← dfe-state, DATA_INTERFACES, SOURCE_MAP, demand, data-samples/, agents/
└── setup/
    └── INSTALL.md                     ← multi-platform install
```

---

## Tenets

1. **Generated, not hand-edited** — everything in `data/` is tool-produced.
2. **Single-writer** — only DFE writes to `data/`; any consumer may read.
3. **Schema-first** — no data file without a schema.
4. **Consumers are decoupled** — they declare a DEMAND and read the registry; they never reach into source files.
5. **Family-scoped** — each family owns its own `data/`; cross-family exchange reads the neighbour's data, never mixes.
6. **Graceful degradation** — incomplete is allowed; broken is not.

---

## Patterns, Methodologies & Frameworks Covered

AI-DFE operationalizes **data integration** — turning scattered, human-readable package outputs into one governed, machine-readable surface. It is family-agnostic; family scope is resolved from `{family}` tokens at clone time. The table maps each pattern to *what AI-DFE applies* and *where it stops*.

| Pattern / methodology | How AI-DFE applies it | Where it stops (scope boundary) |
|---|---|---|
| **ETL / ingestion pipeline** | Two-layer pipeline — gather sources → shape per-package JSON (Layer 1) → shape demand-driven consumer outputs (Layer 2) → distribute | It transforms and republishes existing package outputs; it never authors or edits source content |
| **Single source of truth / registry** | `REGISTRY.json` — every consumer resolves its data path through one fixed entry point | The registry indexes data; it is not a query API or a database |
| **Schema-on-write (contract-first)** | Every file validates against a JSON Schema before it is written; malformed data is rejected at the boundary | It enforces shape, not semantics — it does not judge whether a package's *content* is correct |
| **Publisher/subscriber decoupling** | Producers emit normal Markdown; consumers declare a `data-demand/` and read the registry — neither knows the other's file paths | Decoupling of data delivery only; it does not orchestrate *when* packages run (that is AI-FLO) |
| **Single-writer ownership** | DFE is the sole owner and sole writer of `{family}-ws/data/`; any consumer may read | It writes only the data surface — never into another package's territory |
| **Snapshotting / point-in-time history** | Every write is snapshotted into `history/` with a millisecond timestamp, plus retention and cleanup | Point-in-time history of the data surface, not full event-sourced replay of package state |
| **Graceful degradation (null-object)** | A missing or unrun package yields a `null` field, never an error; incomplete is allowed, broken is not | It reports absence; it never fabricates data to fill a gap |
| **Materialized view** | Demand-shaped Layer-2 outputs are pre-computed views tailored to each consumer, refreshed on each `DAT__` pass | Views refresh per pass; DFE is not a live/streaming view engine |

**Scope boundary (what AI-DFE does *not* do):** it never authors or edits a package's source content, never routes decisions or decides *when* a package runs (that is AI-FLO), and never writes outside `{family}-ws/data/`. Everything in `data/` is tool-generated, schema-validated, and reproducible from sources.

---

## License

**Apache License 2.0 with Attribution Addendum**

- **Free to use:** Personal, commercial, educational, and organizational use — all permitted
- **Modify and distribute:** Create derivative works, redistribute, sublicense — all permitted
- **Attribution required:** Any distributed product substantially based on this work must include:

> *"Built on AIFLC by Mohammad Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)"*

- **No warranty:** Provided "AS IS" without warranties of any kind

See `LICENSE` and `NOTICE` in this directory for full terms.

**Copyright:** © 2026 Mohammad Maheri

> **Note:** AI-DLC v1 (Development Life Cycle) is NOT part of the AI-* Family — it is a separate AWS product ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) licensed under MIT-0.

---

## Author

**Maheri** — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)

AI-DFE is part of **AIFLC** (AI Full Life Cycle), a family of injectable AI workflow packages. Built on AIFLC by Mohammad Maheri.
