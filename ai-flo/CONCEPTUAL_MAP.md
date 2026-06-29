# AI-FLO Conceptual Map

> **What this file is:** A navigational guide to AI-FLO's internal structure. It answers "where does each routing concern live?" and helps you find the right file across 3 phases and 10 stages.

---

## How to Read This

AI-FLO is an **edge router / orchestration engine** with 3 phases containing 10 stages, plus 1 governance agent. It sits on the boundary between the Portfolio layer and the Project layer — carrying dispatch decisions down, relaying telemetry up, and tracking where every project sits in the chain. Unlike lifecycle packages that complete, AI-FLO operates continuously — projects enter, move, and exit over time. This map organizes files by *concern domain*.

**Key principle:** AI-FLO carries decisions, it doesn't make them. AI-PPM decides what gets built; the operator decides overrides; AI-FLO routes. Cross-layer communication ALWAYS goes through AI-FLO (L53); same-layer communication is direct marker reads.

---

## Concern → Location Map

### Core Orchestration

| Concern | File | Purpose |
|---------|------|---------|
| Master engine logic | `ai-flo-rules/core-engine.md` | Phases, modes, chain contract, conflict model, routing table |
| Family position | `ai-flo-rules/core-engine.md` → Family table | AI-FLO on the edge between Portfolio and Project layers |

### Cross-Cutting Rules

| Concern | File | Purpose |
|---------|------|---------|
| Process overview | `common/process-overview.md` | High-level map of FLO's routing process |
| Session continuity | `common/session-continuity.md` | State preservation across sessions (`flo-state.md`) |
| Question format | `common/question-format-guide.md` | Structured question formatting |
| Routing conventions | `common/routing-conventions.md` | Marker addressing + path resolution across topologies |
| Welcome message | `common/welcome-message.md` | One-time workflow greeting |

### Configure Phase (Phase 1: Stages 1–3)

| Stage | File | Purpose |
|:-----:|------|---------|
| 1 | `configure/workspace-detection.md` | Detect topology mode (1/2/3), inventory packages, init `flo-state.md` |
| 2 | `configure/routing-table-build.md` | Build canonical routing table, apply profiles + toggles |
| 3 | `configure/flow-state-init.md` | Determine per-project positions, init `routing-log.md`, produce route map |

### Route Phase (Phase 2: Stages 4–7)

| Stage | File | Purpose |
|:-----:|------|---------|
| 4 | `route/dispatch-down.md` | Carry AI-PPM dispatch authorization down to Project layer |
| 5 | `route/fan-out-fan-in.md` | Sequential routing (POLC→UXD→ADLC→DWG) and convergence readiness (AP+PBP+UXP→DWG) |
| 6 | `route/handoff-execution.md` | Produce handoff instruction per route, update position + history |
| 7 | `route/exceptions-overrides.md` | Block, cancel, rework, skip, escalate + operator route/toggle/priority overrides |

### Monitor Phase (Phase 3: Stages 8–10)

| Stage | File | Purpose |
|:-----:|------|---------|
| 8 | `monitor/position-tracking.md` | Scan state files for progression, detect stalls, refresh route map |
| 9 | `monitor/roll-up-relay.md` | Compile per-project status into roll-up report for AI-PPM |
| 10 | `monitor/health-conflicts-alerts.md` | Conflict detection (flag-and-hold), stall + bottleneck alerts |

### Output Templates

| Template | Purpose |
|----------|---------|
| `templates/flo-state.md` | Engine state/marker file — per-project positions |
| `templates/routing-table.md` | Active routes + per-project profiles |
| `templates/routing-log.md` | Append-only audit trail of every routing event |
| `templates/dispatch-record.md` | Per-dispatch record (PPM authorization → Project layer) |
| `templates/roll-up-report.md` | Project status compiled for AI-PPM |
| `templates/route-map.md` | Multi-project flow visualization |
| `templates/readiness-check.md` | Fan-in evaluation (which feeds ready / pending) |
| `templates/conflict-alert.md` | Flag-and-hold conflict report |
| `templates/flow-dashboard-template.md` | Flow status dashboard for portfolio monitoring |

### Governance Agent

| Agent | Folder | When Used |
|-------|--------|-----------|
| Flow Integrity Agent (`FIA__`, AG-ID `FLO-AG-01`) | `templates/agents/flow-integrity-agent.md` | On-demand 17-check integrity pass across routing state, table, conflicts, topology |
| Shortcut rules block | `templates/agents/shortcut-rules-block.md` | Paste into workspace rules to enable the `FIA__` shortcut |

---

## Cross-Cutting Mechanisms

| Mechanism | Where Defined | How It Works |
|-----------|--------------|--------------|
| **Layered communication (L53)** | `core-engine.md` | Cross-layer = via FLO; same-layer = direct marker read |
| **Continuous engine** | `core-engine.md` | No "workflow complete" — projects enter, move through hops, and exit over time |
| **Topology-aware** | `core-engine.md` | Detects Mode 1 (co-located) / Mode 2 (hub) / Mode 3 (portfolio) and adapts scanning |
| **Correlation key** | `core-engine.md` | `projectId` (camelCase) threads from PILC through the chain — FLO carries it on every routing hop |
| **Flag-and-hold conflicts** | `monitor/health-conflicts-alerts.md` | Bidirectional signal collisions are flagged + held, never silently resolved |
| **Anti-deadlock guarantee** | `core-engine.md` | Every hold has a timeout with deterministic fallback; operator can always force-through |
| **Session continuity** | `common/session-continuity.md` | `flo-state.md` preserves topology mode + per-project positions |
| **Governance spine (minimal)** | `core-engine.md` | Appends FLO-D- decisions + FLO-I- issues only — routine hops stay in routing log |

---

## Common Questions

### "How does AI-FLO know where each project is?"
→ `monitor/position-tracking.md` — scans each package's `*-state.md` marker for status changes and updates positions in `flo-state.md`. Detection is by marker (L14), keyed by `projectId`.

### "How does AI-PPM dispatch a project to the Project layer?"
→ Via FLO. `route/dispatch-down.md` reads AI-PPM's dispatch authorizations (`DA-*.md`), creates the project entry in `flo-state.md`, and routes to AI-POLC (first package in the Project-layer sequence per profile). Cross-layer communication ALWAYS goes through AI-FLO (L53).

### "What happens when the Portfolio and Project layers send conflicting signals?"
→ Flag-and-hold. `monitor/health-conflicts-alerts.md` compares up-signals vs. down-signals for the same `projectId` + field, produces a `conflict-alert.md`, and holds routing for that project until the operator resolves. FLO never silently picks a winner.

### "Does AI-FLO automatically start package sessions?"
→ No. AI-FLO is advisory in v1.0 — it records routing decisions as artifacts for human action. It does not auto-execute package sessions (deferred to v1.1+).

### "What if AI-FLO isn't installed?"
→ The family still works. Cross-layer communication degrades to manual coordination (the human bridges the gap); same-layer marker detection works regardless. FLO is additive — it adds coordination, never a single point of failure.

### "What's the fan-in rule for AI-DWG?"
→ `route/fan-out-fan-in.md` — AP (`adlc-state.md`) is the terminal input; the sequential flow guarantees PBP (`polc-state.md`) and UXP (`uxd-state.md`) are already present by the time ADLC completes. DWG proceeds once `adlc-state.md` appears, reading all three.

### "What agent does AI-FLO ship?"
→ `flow-integrity-agent` (`FIA__`) — ID `FLO-AG-01`. On-demand 17-check integrity pass across 5 categories (routing state, table integrity, conflict resolution, topology consistency). Located in `templates/agents/`.

---

*Created: 2026-06-12 | Lesson 30 compliance*

---

## AI-DFE Data Interface (`ai-flo-rule-details/data-schema/`)

This package ships a machine-readable data interface consumed by **AI-DFE** (the family data fabric). AI-DFE reads these files to gather this package's output into `{family}-ws/data/flo-data.json`.

| File | Purpose |
|------|---------|
| `flo-data.schema.json` | JSON Schema — the shape AI-DFE produces for this package |
| `SOURCE_MAP.md` | Declares where this package's raw output lives + field extraction rules |
| `SCHEMA_README.md` | Human documentation of the schema, fields, and consumers |

> These files do not change this package's runtime behavior — they are a read-only contract for the data fabric. See AI-DFE for how the data surface is gathered, shaped, and distributed.
