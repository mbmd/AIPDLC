# AI-FLO — AI-Driven Flow Orchestrator

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**License:** Apache 2.0 with Attribution

---

## What Is AI-FLO?

AI-FLO is the nervous system of the AI-* PDLC Family. It routes decisions down from the Portfolio layer, relays status up from the Project layer, and maintains awareness of where every project is in the chain at all times.

**In one sentence:** AI-FLO turns the AI-* PDLC Family from a collection of independent packages into a coordinated pipeline — tracking positions, dispatching projects, detecting conflicts, and ensuring nothing falls between the cracks.

---

## Family Position

AI-FLO is part of **AIFLC** (AI Full Life Cycle). It sits on the **edge** between the Portfolio layer and Project layer in the AI-* PDLC Family:

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

> **AI-DFE** ([Data Fabric Engine](../ai-dfe/)) is a family-scoped **companion** — it gathers data from all packages and distributes structured JSON for dashboards and status roll-ups. It runs alongside the chain rather than as a linear step, so it is not shown as a chain row above.

---

## Where AI-FLO Sits in the Chain

AI-FLO is a **fabric engine**, not a chain step — the family's **edge router**. It runs *alongside* the whole chain, on the edge between the Portfolio and Project layers: it reads every package's state marker, decides which package runs next, carries dispatch decisions down, and relays status up. In v2.0 the engine is **family-agnostic** — it operates on any family's bindings graph, with family-specific routing injected via an overlay.

| Aspect | AI-FLO |
|--------|---------|
| **Role** | Universal fabric router (edge) — carries entities between packages and layers |
| **Position** | Alongside the chain (the edge between Portfolio and Project layers); not a chain row |
| **Reads (input)** | Any package's `*-state.md` marker (wildcard) + each family's `FAMILY_BINDINGS.md` / `GATE_PROTOCOL.md` / `FAMILY_INTERFACE.md` |
| **Produces (output)** | Routing decisions + handoff instructions under `_FLO_/` (routing table, log, conflict alerts, readiness checks) |
| **Output marker** | `flo-state.md` |
| **Correlation key** | Carries `projectId` / `derivedFrom` lineage on every routing hop (across families) |
| **Capability emitted** | `orchestration-state@1` (internal — routing metadata, not a chain deliverable) |
| **Capability consumed** | `*` (all marker types, as routing triggers) |
| **Family footprint** | Cloned into every family at assemble — one canonical family-agnostic engine + a per-family overlay |

AI-FLO answers **"where is every project, what's the next hop, and is anything blocked?"** It is **advisory** (v1.0 behavior): it records routing decisions for a human to act on; it never auto-starts a package session, and it never decides *what* to build (AI-PPM decides; the operator overrides; AI-FLO carries).

### Standalone vs. chained

- **Additive, never required.** Without AI-FLO, same-layer packages still hand off via direct marker detection. AI-FLO adds coordination (especially cross-layer and cross-family) — it is never a single point of failure.
- **Graph-driven.** It reads `FAMILY_BINDINGS.md` and never invents routes — no bindings, no routing.
- **Gate-validated.** Every hop runs the `GATE_PROTOCOL` matching stack; failures flag-and-hold (never silently resolved), and every hold has a timeout with a deterministic fallback.
- **Cross-family.** A central FLO can route across families over the AIFLC Communication Fabric, following entity lineage across family boundaries.

---

## Features

- **3 phases, 10 stages** — Configure → Route → Monitor
- **Cross-layer dispatch** — carry AI-PPM's authorization down to Project-layer packages
- **Upward roll-up relay** — compile project status and surface to portfolio level
- **Sequential routing** — carry routing decisions through the Project-layer sequence (POLC → UXD → ADLC → DWG) and validate readiness at convergence (AP+PBP+UXP → DWG)
- **Flow state tracking** — know where every project is at all times (`flo-state.md`)
- **Routing table** — static canonical default + per-project profiles + runtime toggles
- **Conflict detection (flag-and-hold)** — detect bidirectional signal collisions; never silently resolve
- **10 conflict types (C1–C10)** — signal collision, routing contention, profile contradiction, stale signal, dependency deadlock, authority conflict (C1–C6); gate-failure conflicts (C7–C9); and drift gate block (C10)
- **Anti-deadlock guarantee** — every hold has a timeout with deterministic fallback; operator can always force-through
- **Flow exceptions** — block, cancel, rework, skip, escalate with full audit trail
- **Route override + toggle** — operator can deviate from canonical chain at any time (logged)
- **3 workspace topology modes** — co-located (1:1), hub-and-spoke (1:N), fully distributed (1:N remote)
- **Hybrid interaction model** — Dashboard (read state) + Command (execute actions) + Alert (proactive notifications)
- **Routing log** — append-only audit trail of every routing event
- **Governance spine contribution** — FLO-D- decisions, FLO-I- issues (routine hops stay in log only)
- **FIA__ governance agent** — on-demand integrity validation (17 checks across 5 categories)
- **Graceful degradation** — without FLO, same-layer packages still work via direct marker detection
- **Advisory model** — records decisions for human action; does not auto-execute package sessions (v1.0)

---

## Activation

**Explicit key:** type `_FLO_` in any prompt to activate AI-FLO unambiguously — even when other AI-* packages share the workspace. The status key `_ACTIVE_` reports which package is currently active. A package switch never happens without your explicit key or confirmation, and any switch is announced on the first line of the response (`Active package: AI-FLO`). See [`../TRIGGER_KEYS_REFERENCE.md`](../TRIGGER_KEYS_REFERENCE.md) for the full family key table.

---

## Installation

AI-FLO is pure Markdown — no runtime, no dependencies, no build step. "Installing" it means placing two folders and one always-loaded router file where your AI agent reads them, plus the **fabric trio** it routes against. (What AI-FLO then *produces* — routing state under `_FLO_/` — is written at run time.)

> **Fabric-engine note.** AI-FLO ships **inside every AI-* family** — if you installed the family, FLO is already present. Install it **directly** (below) only to add the router to a workspace that has other AI-* packages but no FLO yet. AI-FLO runs in the **planning / orchestration workspace** (where the lifecycle packages live), never inside an AI-DWG-generated dev workspace.

### The model (read this first)

Installation writes to four places:

1. **The package home** — `ai-flo-rules/` (the core **engine/dispatcher**) and `ai-flo-rule-details/` (configure / route / monitor stages + templates, read on demand) are copied into `.aiflc/pdlc/`. This path is **identical on every platform**.
2. **One always-loaded orchestrator** — a single small router placed in your platform's native auto-load slot. It is the *only* file that loads automatically; it `Read`s the AI-FLO core on demand when you activate the engine.
3. **The fabric trio (REQUIRED)** — `FAMILY_BINDINGS.md`, `GATE_PROTOCOL.md`, and `FAMILY_INTERFACE.md` are copied into `.aiflc/pdlc/`. AI-FLO reads them at runtime to build its routing graph; **without them FLO returns NOT READY** ("no bindings = no routing; FLO never invents routes").
4. **The output home** — AI-FLO writes routing state into `_FLO_/` at run time.

### Option A — Install alongside the family (recommended)

Use the family installer to place AI-FLO (and the fabric trio) into a workspace:

```powershell
# Windows (PowerShell)
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-flo"
```

```bash
# macOS / Linux
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-flo
```

Supported `-Platform` values: `kiro`, `cursor`, `claude-code`, `cline`, `amazonq`, `copilot`. The installer deploys the fabric trio automatically and creates the workspace where AI-FLO writes its output.

### Option B — Install this engine individually (manual)

Copy the two package folders into the uniform home (same on every platform):

```
ai-flo/ai-flo-rules/        →  <workspace>/.aiflc/pdlc/ai-flo-rules/
ai-flo/ai-flo-rule-details/ →  <workspace>/.aiflc/pdlc/ai-flo-rule-details/
```

Copy the fabric trio into the same home (REQUIRED — from the family root):

```
FAMILY_BINDINGS.md   →  <workspace>/.aiflc/pdlc/FAMILY_BINDINGS.md
GATE_PROTOCOL.md     →  <workspace>/.aiflc/pdlc/GATE_PROTOCOL.md
FAMILY_INTERFACE.md  →  <workspace>/.aiflc/pdlc/FAMILY_INTERFACE.md
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

> AI-FLO's agents are **report-only** (`FHC__` fabric health check — run first; `FIA__` flow integrity agent). On Kiro, copy them into `.kiro/agents/`; on other platforms, register their shortcut blocks in your workspace rules.

### For AI agents — machine-readable install manifest

An AI assistant can install AI-FLO by parsing and executing the block below. All `copy.from` and `orchestrator.source` paths are relative to `source_root`; every destination is relative to the workspace root. Pick the one `orchestrator.slot` row that matches the target platform. The manifest is **platform-agnostic** — everything except `orchestrator.slot` is identical on every platform.

```yaml
# AIFLC INSTALL MANIFEST — AI-FLO
package: AI-FLO
family: pdlc                       # package home: .aiflc/pdlc/
version: 2.0.0
runtime: none                      # pure Markdown; no deps, no build
role: fabric-engine                # ships in every family; the family's edge router
source_root: pdlc-packages/        # clone root of the AIPDLC repo
activation_phrase: "Using AI-FLO, what should I do next?"
trigger_key: "_FLO_"               # universal explicit key (recognized by the orchestrator on any platform); or use activation_phrase
status_key: "_ACTIVE_"             # reports which package is currently active
depends_on: []                     # standalone-capable; advisory — never blocks on missing markers
requires_fabric_trio:              # REQUIRED — without these FLO returns NOT READY
  - FAMILY_BINDINGS.md             # routing graph
  - GATE_PROTOCOL.md               # gate matching stack
  - FAMILY_INTERFACE.md            # family discovery
consumes_capability: "*"           # all marker types in the bindings graph, as routing triggers
emits_capability: "orchestration-state@1"   # internal — routing metadata, not a chain deliverable
output_marker: flo-state.md
output_dir: _FLO_/                 # routing state written here at run time
copy:
  - from: ai-flo/ai-flo-rules
    to: .aiflc/pdlc/ai-flo-rules
  - from: ai-flo/ai-flo-rule-details
    to: .aiflc/pdlc/ai-flo-rule-details
fabric_trio:                       # copy into the same home (from the family root)
  - to: .aiflc/pdlc/FAMILY_BINDINGS.md
  - to: .aiflc/pdlc/GATE_PROTOCOL.md
  - to: .aiflc/pdlc/FAMILY_INTERFACE.md
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
core_entry: .aiflc/pdlc/ai-flo-rules/core-engine.md       # orchestrator Reads this on activation
rule_details_home: .aiflc/pdlc/ai-flo-rule-details/       # core resolves these on demand
agents:                            # report-only; Kiro → .kiro/agents/, others → shortcut blocks
  - trigger: "FHC__"               # fabric health check — run first
  - trigger: "FIA__"               # flow integrity agent
verify:
  - path_exists: .aiflc/pdlc/ai-flo-rules/core-engine.md
  - path_exists: .aiflc/pdlc/FAMILY_BINDINGS.md
  - orchestrator_present_in_platform_slot: true
  - action: 'type "FHC__" and expect a HEALTHY or IDLE verdict (confirms the fabric trio resolved)'
```

### Verify

1. Open the target workspace in your IDE with the AI agent active.
2. Confirm the orchestrator loaded (Kiro: it appears in the Steering panel).
3. Run the health check: type `FHC__`. A **HEALTHY** (or **IDLE** if no project yet) verdict confirms the fabric trio resolved correctly.
4. Start a chat: `Using AI-FLO, what should I do next?` — AI-FLO reads the workflow state markers and tells you the next hop.

For the full per-platform walkthrough, see [setup/INSTALL.md](./setup/INSTALL.md) and the family-wide [INSTALL_GUIDE.md](../../INSTALL_GUIDE.md).

---

## Usage

1. Open a workspace where AI-* packages are installed
2. Start a chat and say:
   ```
   Using AI-FLO, what should I do next?
   ```
3. AI-FLO reads the current workflow state markers and tells you which package to activate next (and flags pending handoffs or conflicts)
4. It routes decisions and relays status between packages — it never produces package artifacts itself

## File Structure

```
ai-flo/
├── README.md                          ← This file
├── LICENSE                            ← Apache 2.0 + Attribution
├── PLAN.md                            ← Design rationale + decisions
├── ai-flo-rules/
│   └── core-engine.md                 ← Master orchestration engine (read on demand by the orchestrator)
├── ai-flo-rule-details/
│   ├── common/                        ← Cross-cutting (5 files)
│   ├── configure/                     ← Phase 1 stages (3 files)
│   ├── route/                         ← Phase 2 stages (4 files)
│   ├── monitor/                       ← Phase 3 stages (3 files)
│   └── templates/                     ← Output templates (9 files)
│       └── agents/                    ← Governance agent (2 files)
└── setup/
    └── INSTALL.md                     ← Platform setup guide
```

---

## Tenets

1. **Advisory, not autonomous** — records decisions for human action; never auto-executes
2. **Carry, don't decide** — PPM decides; operator overrides; FLO routes
3. **Log everything** — every hop, override, toggle, conflict is recorded
4. **Flag, never suppress** — conflicts always surface; FLO never silently picks a winner
5. **Canonical default, governed deviation** — family chain is default; deviations are explicit and auditable
6. **Topology-aware** — adapts to co-located, hub-and-spoke, or fully-distributed workspaces
7. **Additive, not blocking** — without FLO, the family still works; FLO adds coordination, never becomes a single point of failure

---

## Patterns, Methodologies & Frameworks Covered

AI-FLO operationalizes **workflow orchestration** — deciding the next hop and carrying entities between packages and layers. In v2.0 the engine is **family-agnostic**: the patterns below belong to the engine; family-specific routes, entity types, and fan-in rules are injected via the `{family}-overlay.md` seam. The table maps each pattern to *what AI-FLO applies* and *where it stops*.

| Pattern / methodology | How AI-FLO applies it | Where it stops (scope boundary) |
|---|---|---|
| **Orchestration (mediator / router)** | A central router carries entities package-to-package and across the Portfolio⇄Project edge along the declared `FAMILY_BINDINGS.md` graph | Routing only — it never produces a package's artifacts (source and destination packages own those) |
| **Orchestration ⇄ choreography (hybrid)** | Advisory orchestration layered over marker-based choreography (same-layer packages may also hand off directly) | Advisory in v1.0 behavior — records decisions for a human; never auto-starts a package session |
| **Marker-based pub/sub** | Reads any package's `*-state.md` marker as a routing trigger and relays handoff instructions | File-marker signals, not a runtime message bus or event stream |
| **Content-based routing** | Canonical default route + per-project profiles + runtime toggles + operator override | Every deviation from the canonical chain is explicit, logged, and operator-governed |
| **Quality-gate validation** | Runs the `GATE_PROTOCOL` matching stack on every hop before advancing | Validates readiness at the seam; it does not evaluate the *content* a package produced |
| **Flag-and-hold (circuit-breaker analog)** | Detects conflict types C1–C10 and halts rather than silently resolving; anti-deadlock timeout + deterministic fallback | Routing conflicts only — not application-level resilience or retry logic |
| **Saga / long-running coordination** | Tracks multi-stage flow; exceptions are block, cancel, rework, skip, escalate | Flow-level compensation, not transactional rollback of package work |
| **Correlation identifier** | Carries `projectId` / `derivedFrom` lineage on every hop, across family boundaries via the Communication Fabric | Routing metadata; it does not mutate the payloads it carries |
| **Append-only audit log** | `_FLO_/routing-log.md` records every hop, override, toggle, hold, and conflict | Audit trail — not full event-sourced state reconstruction |
| **Drift brokering** (`DFT__ route`) | Reads a drift envelope from `.governance/drift-register.md` and routes it (domainTag → target) | Brokers the address only — it never writes the drift register |

**Scope boundary (what AI-FLO does *not* do):** it never decides *what* to build (AI-PPM decides; the operator overrides), never produces a package deliverable, and — in v1.0 behavior — never auto-executes a session. It routes, validates at gates, and records; humans and packages act.

---

## Output (What You Get)

When AI-FLO is active, it writes its working state under `_FLO_/`:

```
{workspace}/
└── _FLO_/                              <- FLO's working folder
    ├── flo-state.md                    [marker]
    ├── routing-table.md                (active routes + profiles)
    ├── routing-log.md                  (append-only audit trail)
    ├── fabric-audit-log.md             (append-only; cross-family hops)
    ├── conflict-alerts/
    │   └── CA-{entity-id}-{NNN}.md     (one per conflict)
    └── readiness-checks/
        └── RC-{entity-id}.md           (one per fan-in evaluation)
```

---

## Author

**Mohammad Maheri** — Process designer specializing in injectable AI workflow packages.

AI-FLO was designed to complete the AI-* Family's architecture: turning a collection of independent packages into a coordinated system where work flows between layers as naturally as data flows through a pipeline.

---

*v1.0.0 | 2026-06-12*

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

---

*Part of [AIFLC](../../README.md) — the AI-* PDLC Family*
