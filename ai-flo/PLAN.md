# AI-FLO — Design Plan

**Package:** AI-FLO (AI-Driven Flow Orchestrator)
**Version:** 1.0.0
**Date:** 2026-06-12
**Author:** Maheri
**Status:** Complete (v1.0.0)

---

## 1. Problem Space

### The Gap

The AI-* Family has a two-layer topology (Portfolio + Project) with branching, fan-out, loops, and a cross-layer boundary — but **no component owns routing**. Handoffs are passive (each package scans for its predecessor's marker), which works for linear chains but breaks when:

1. **Cross-layer dispatch** — AI-PPM authorizes a project but nothing carries that decision to the Project layer.
2. **Upward roll-up** — Project-layer packages produce status but nothing relays it to AI-PPM for portfolio-wide visibility.
3. **Sequential handoff** — the Project layer runs AI-POLC → AI-UXD → AI-ADLC and each handoff needs routing, but nothing coordinates the dispatch.
4. **Readiness** — AI-DWG needs AP + PBP + UXP before starting; in the sequential model AI-ADLC is the final predecessor, but nothing formally confirms the full chain up to that point completed cleanly.
5. **Flow state** — there is no record of where each project is in the chain or what's next.

### Identity Spine (Lesson 36)

> AI-FLO is the nervous system of the AI-* Family — it carries routing decisions down, telemetry up, and maintains awareness of where every project is in the chain at all times.

**Inclusion rule:** In scope = *what goes where next, and what's the current position of each project*. Out = *what to build* (PPM/PILC), *how to build it* (ADLC/UXD/POLC/DWG), *whether it's compliant* (GCE/TGE).

---

## 2. Package Identity

| Field | Value |
|-------|-------|
| **Name** | AI-FLO |
| **Full Title** | AI-Driven Flow Orchestrator |
| **Package Type** | Router / orchestration engine (continuous — not a lifecycle) |
| **Input** | Any package's output marker + AI-PPM dispatch authorization |
| **Output** | Routing decision + handoff instruction; `flo-state.md` (flow state) |
| **Primary Persona** | Delivery/platform engineer — thinks in pipelines, DAGs, routing, and message flow |
| **Marker File** | `flo-state.md` |
| **Family Position** | Edge layer — between Portfolio and Project layers; mediates all cross-layer flow |

### Name Challenge (Lesson 12)

| Candidate | Verdict |
|-----------|---------|
| **AI-FLO** ✓ | 3 letters, reads as "flow," immediately communicates function |
| AI-RTR | Unpronounceable, ugly |
| AI-ORCH | 4 letters, overloaded term (Kubernetes), implies too much autonomy |

---

## 3. Phase/Stage Structure

AI-FLO uses 3 phases with 10 stages:

```
Phase 1: CONFIGURE           Phase 2: ROUTE              Phase 3: MONITOR
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│ 1. Workspace    │         │ 4. Dispatch     │         │ 8. Position     │
│    Detection    │         │    (Down)       │         │    Tracking     │
│ 2. Routing     │────────▶│ 5. Fan-Out /    │────────▶│ 9. Roll-Up      │
│    Table Build  │         │    Fan-In       │         │    Relay        │
│ 3. Flow State  │         │ 6. Handoff      │         │10. Health,      │
│    Init        │         │    Execution    │         │    Conflicts    │
│                 │         │ 7. Exceptions   │         │    & Alerts     │
│                 │         │    & Overrides  │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### Phase Detail

| Phase | Name | Purpose | Stages |
|-------|------|---------|--------|
| 1 | **Configure** | Scan the workspace, build the routing table, initialize flow state | 1–3 |
| 2 | **Route** | Execute routing decisions — dispatch down, fan-out/fan-in, handoff, exceptions | 4–7 |
| 3 | **Monitor** | Track position, relay roll-up telemetry, detect conflicts/stalls/alerts | 8–10 |

### Stage Summary

| # | Stage | Always/Conditional | Primary Deliverable |
|---|-------|-------------------|---------------------|
| 1 | Workspace Detection | Always | Package inventory + topology map |
| 2 | Routing Table Build | Always | `routing-table.md` (marker → successor map) |
| 3 | Flow State Initialization | Always | `flo-state.md` (per-project positions) |
| 4 | Dispatch (Down) | Always | Dispatch records (PPM authorization → Project layer) |
| 5 | Fan-Out / Fan-In | Conditional | Parallel readiness checks (when graph topology) |
| 6 | Handoff Execution | Always | Handoff instructions per route + routing log entry |
| 7 | Exceptions & Overrides | Conditional | Re-route, block, cancel, skip, or user override of default route |
| 8 | Position Tracking | Always | Updated `flo-state.md` with current positions + route map visualization |
| 9 | Roll-Up Relay | Always | Roll-up report (Project status → PPM) |
| 10 | Health, Conflicts & Alerts | Always | Conflict detection (flag-and-hold), stall detection, bottleneck alerts |

---

## 4. File Structure

```
ai-flo/
├── README.md
├── LICENSE
├── PLAN.md                              ← This file
├── ai-flo-rules/
│   └── core-engine.md                   ← Master orchestration (THE spec)
├── ai-flo-rule-details/
│   ├── common/                          ← Cross-cutting (5 files)
│   │   ├── process-overview.md
│   │   ├── session-continuity.md
│   │   ├── question-format-guide.md
│   │   ├── routing-conventions.md       ← Marker addressing + path resolution
│   │   └── welcome-message.md
│   ├── configure/                       ← Phase 1 (3 files)
│   │   ├── workspace-detection.md
│   │   ├── routing-table-build.md
│   │   └── flow-state-init.md
│   ├── route/                           ← Phase 2 (4 files)
│   │   ├── dispatch-down.md
│   │   ├── fan-out-fan-in.md
│   │   ├── handoff-execution.md
│   │   └── exceptions-overrides.md      ← Re-route, block, cancel, skip, user override
│   ├── monitor/                         ← Phase 3 (3 files)
│   │   ├── position-tracking.md
│   │   ├── roll-up-relay.md
│   │   └── health-conflicts-alerts.md   ← Conflict detection + flag-and-hold
│   └── templates/                       ← Output templates (9 files)
│       ├── flo-state.md
│       ├── routing-table.md
│       ├── routing-log.md               ← Audit trail (timestamped routing history)
│       ├── dispatch-record.md
│       ├── roll-up-report.md
│       ├── route-map.md                 ← Multi-project flow visualization
│       ├── readiness-check.md
│       ├── conflict-alert.md            ← Flag-and-hold conflict report
│       └── agents/
│           ├── flow-integrity-agent.md
│           └── shortcut-rules-block.md
└── setup/
    └── INSTALL.md
```

**Total estimated files:** 31

---

## 5. Key Design Decisions

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| 1 | Package type | Engine (not lifecycle) | Continuous operation — not a one-time journey. Like AI-GCE/AI-PPM, not AI-PILC/AI-ADLC. |
| 2 | Core file name | `core-engine.md` | Follows AI-PPM and AI-GCE pattern (engines use `core-engine.md`; lifecycles use `core-workflow.md`). |
| 3 | Routing execution | Advisory (records decisions) | v1.0 produces routing decisions as artifacts for human action. NOT automated execution (deferred to v1.1). |
| 4 | Fan-in detection | Multi-marker readiness check | Scan for all required predecessor markers before declaring "ready for join." |
| 5 | Flow state scope | Per-project | One `flo-state.md` per project (multi-project = portfolio mode with multiple state entries). |
| 6 | Graceful degradation | FLO is additive | When FLO is not installed, same-layer packages continue with direct marker detection (fallback in AI-PPM already). |
| 7 | Persona | Hybrid: DevOps core, delivery-operator surface | Thinks in pipelines/state-machines; communicates in plain delivery language. Technical depth on request. |
| 8 | Routing table | Static base + per-project profile + runtime toggle | Canonical chain is default; projects declare which packages to skip at dispatch; operator can toggle on/off mid-flow. All changes logged. |
| 9 | Interaction model | Hybrid: Dashboard + Command + Alert | Shows state on request; accepts commands for actions; alerts proactively on anomalies (conflicts, stalls, readiness). |
| 10 | Spine contribution | Minimal (FLO-D- decisions + FLO-I- issues) | Overrides, toggles, cancellations, conflicts go to spine. Routine hops stay in routing log only. No spine flooding. |

---

## 6. Layered Communication Rule (Established)

This rule was established during the AI-PPM build and is now family-wide architectural law:

> **Cross-layer communication MUST go through AI-FLO. Same-layer communication is direct (marker-based).**

| Communication | Mechanism | Why |
|---|---|---|
| PPM reads PILC output | Direct (same layer) | Both Portfolio layer |
| PPM reads ILC output | Direct (same layer) | Both Portfolio layer |
| PPM dispatches to ADLC/UXD/POLC | Via FLO (cross-layer) | Portfolio → Project boundary |
| Project packages report to PPM | Via FLO (cross-layer) | Project → Portfolio boundary |
| ADLC → DWG, POLC → DWG, etc. | Direct (same layer) | Both Project layer |

**Fallback (no FLO installed):**
- Cross-layer: Degrades to manual coordination (human bridges the gap)
- Same-layer: Always works (unchanged)

---

## 7. Conflict Detection Model (Flag-and-Hold)

Certain data can be modified from BOTH the Portfolio layer (top-down) and Project layer (bottom-up) simultaneously. When FLO detects conflicting signals, it does NOT resolve them — it flags and holds.

### Bidirectional Data (Potential Conflicts)

| Data | Down (PPM→Project) | Up (Project→PPM) | Conflict Scenario |
|------|--------------------|--------------------|-------------------|
| **Priority** | Portfolio rebalancing | Scope discovery ("this is bigger") | PPM downgrades while POLC flags urgency |
| **Status** | "Pause" / "Resume" / "Cancel" | "Complete" / "Blocked" / "Ready" | PPM pauses while project signals completion |
| **Scope/Constraints** | Budget/timeline/team changes | "Constraints insufficient" signal | PPM tightens while project flags overflow |
| **Timeline** | New deadline imposed | "Deadline unrealistic" signal | PPM compresses while ADLC flags discovery |

### One-Way Data (No Conflict Possible)

| Data | Direction | Why |
|------|-----------|-----|
| Dispatch authorization | Down only | Only PPM authorizes |
| Position in chain | Up only | Only project packages move through stages |
| Routing decisions | FLO only | Neither layer routes; FLO does |
| Design artifacts | Up only | Only Project layer produces |

> **Note (same-layer lateral exchange is outside FLO):** "Design artifacts — Up only" describes their movement **across layers** (Project → Portfolio, via FLO). It does **not** mean design artifacts never move *laterally*. Within the Project layer, AI-POLC, AI-UXD, and AI-ADLC exchange directly (peer marker reads — value goals, personas/flows, feasibility/cost-risk, constraints) without FLO. FLO governs cross-layer transport only; same-layer lateral flow is direct and is not FLO's concern (Lesson 53).

### Resolution Model (v1.0): Flag-and-Hold

When FLO detects a conflict:
1. **Detect** — compare the timestamp and content of up-signal vs. down-signal for the same `Project ID` + data field
2. **Flag** — produce a `conflict-alert.md` with: both signals, their timestamps, the `Project ID`, the affected field, and suggested resolution options
3. **Hold** — pause routing for that project until the operator resolves (approve one signal, merge, or escalate)
4. **Resume** — operator marks resolution in the conflict alert → FLO resumes routing with the resolved value

**This is Stage 10's primary responsibility.** FLO never silently picks a winner.

---

## 8. Route Exceptions & Override Model

### Flow Exceptions (Stage 7)

| Exception | Trigger | FLO Action |
|-----------|---------|------------|
| **Block** | Predecessor incomplete / dependency unmet | Hold routing for this project; alert operator |
| **Cancel** | PPM issues "Cancel" signal OR operator requests | Terminate flow; update flo-state to `Cancelled`; notify downstream |
| **Rework** | Quality gate fails downstream | Route BACK to the relevant predecessor (e.g., DWG fails → back to ADLC) |
| **Skip** | User declares a package not needed for this project | Skip successor; advance to next in chain |
| **Escalate** | Conflict detected / stall exceeds threshold | Escalate to PPM with context |

### User Override

The operator can override any routing decision at any time:
- Override the default successor ("skip ADLC, go straight to DWG")
- Override fan-out targets ("don't run UXD for this project")
- Override priority of dispatch ("route Project B before Project A")

**Every override is logged** in the routing log with: timestamp, operator, original route, override route, reason.

FLO's routing table defines the **default** flow. The operator is always the authority.

---

## 9. Workspace Topology Modes

FLO operates across three deployment topologies that define how Portfolio and Project layers are distributed across workspaces:

### Mode Definitions

| Mode | Name | Description | Typical Use |
|------|------|-------------|-------------|
| **Mode 1** | Co-located Single | Portfolio + Project in ONE workspace, managing ONE project | Solo developer, small team, single product |
| **Mode 2** | Hub-and-Spoke | Portfolio + one Project in a HUB workspace, with additional Projects in REMOTE workspaces | Team managing a primary product locally + satellite projects |
| **Mode 3** | Fully Distributed | Portfolio in its own workspace; every Project in a separate workspace | Enterprise PMO, large multi-team organization |

### How Topology Affects FLO

| Concern | Mode 1 | Mode 2 | Mode 3 |
|---------|--------|--------|--------|
| Marker detection | Local file scan | Local + remote path references | Remote path references only |
| Dispatch delivery | Write to same folder tree | Local write + remote references | Remote references only |
| Roll-up collection | Read local state files | Local + remote state reads | Remote state reads only |
| `flo-state.md` location | Project folder (co-located) | Hub workspace (master) | Portfolio workspace (master) |
| Project addressing | Relative path | Relative (local) + absolute/URI (remote) | Absolute path / URI for all |

### FLO State Ownership (Option A — Master in Portfolio)

- `flo-state.md` lives in the **portfolio workspace** (or the co-located workspace in Mode 1)
- Each project is an entry (row) keyed by `Project ID`
- Each entry carries a `workspace_ref` field: the path/URI to the project's workspace root
  - Mode 1: `workspace_ref: ./` (same workspace)
  - Mode 2: `workspace_ref: ./` (local) or `workspace_ref: /path/to/remote-project/` (remote)
  - Mode 3: `workspace_ref: /path/to/project-workspace/` (all remote)
- v1.0: FLO scans local projects actively; remote projects are updated by **operator pull** (user reports status or points FLO at the path)
- v1.1+: Active remote sync (file watchers, periodic pull, or shared-drive resolution)

### Topology Detection (Stage 1)

Stage 1 (Workspace Detection) determines the active mode by scanning:
1. Does a `ppm-state.md` exist locally? → Portfolio layer is here
2. Do Project-layer markers exist locally (`adlc-state.md`, `polc-state.md`, etc.)? → Project layer is here
3. Both present = Mode 1 or Mode 2
4. Only portfolio present + remote references configured = Mode 3
5. Mode 2 vs. Mode 1 distinguished by: portfolio register contains >1 project AND some have non-local `workspace_ref`

---

## 10. Build Sequence

Per PLAYBOOK:

1. ✅ PLAN.md (this file)
2. `core-engine.md` — master orchestration
3. Common files (5)
4. Phase 1 detail files (3): configure/
5. Phase 2 detail files (4): route/
6. Phase 3 detail files (3): monitor/
7. Templates (9 + 2 agent)
8. README.md + LICENSE + INSTALL.md
9. Dry Test
10. Register in FAMILY_TABLE_MAP

One file at a time, approval between each.

---

## 11. Deferred to v1.1+

| Feature | Reason for Deferral |
|---------|---------------------|
| Automated trigger execution (auto-start sessions) | v1.0 is advisory; automation requires runtime hooks |
| Event-driven real-time routing (file-system watchers) | Complexity; v1.0 is scan-on-demand |
| Loop iteration tracking (POLC ⇄ DLC count + exit) | Needs AI-DLC v1 integration patterns that don't exist yet |
| Active remote workspace sync (Mode 2/3 file watchers) | v1.0 uses operator-pull for remote state; active sync adds complexity |
| Brownfield / mid-stream adoption | Needs reconciliation logic |
| Custom routing rules (user-defined beyond family table) | v1.0 uses family-standard routes only |
| Contention / resource-aware queuing | Complex; relates to AI-PPM capacity extension |
| Inter-project dependency blocking | Complex; coordinate with AI-PPM dependency-mapping extension |
| Throttling / capacity awareness | Optimization, not core routing |

---

*Created: 2026-06-12 | Author: Maheri | Source: Idea 008 (approved 2026-06-12, score 33/35)*
