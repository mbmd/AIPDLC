---
inclusion: always
---
<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AIFLC Session Orchestrator — AI-* PDLC Family

> **This is the ONLY always-loaded steering file for the AI-* PDLC Family.** All package workflows (`ai-ilc-rules`, `ai-pilc-rules`, etc.) are set to `inclusion: manual` and load ONLY when activated. This keeps the context window free for actual work.

---

## Purpose

Prevent context overload. Instead of loading all package workflows into every session, this orchestrator:
1. Detects what the user wants to do
2. Loads ONLY the relevant package steering
3. Provides the activation keys as a routing table

---

## Activation Keys (Quick Reference)

> **Full trigger registry (all package keys + all agent shortcuts):**
> #[[file:TRIGGER_KEYS_REFERENCE.md]]

| Key | Package | When to Use |
|-----|---------|-------------|
| `_ILC_` | AI-ILC | New idea capture, evaluation, go/no-go |
| `_PILC_` | AI-PILC | Project initiation from requirements |
| `_PPM_` | AI-PPM | Portfolio management, cross-project governance |
| `_FLO_` | AI-FLO | Flow routing, entity position tracking |
| `_POLC_` | AI-POLC | Product backlog, product ownership |
| `_UXD_` | AI-UXD | UX design, personas, journeys, design system |
| `_ADLC_` | AI-ADLC | Architecture / system design |
| `_DWG_` | AI-DWG | Development workspace generation |
| `_GCE_` | AI-GCE | Compliance / enforcement governance |
| `_TGE_` | AI-TGE | Test governance, coverage analysis |
| `_DFE_` | AI-DFE | Data fabric (gather/shape/distribute) |
| `_ACTIVE_` | (read-only) | Report which package is currently active |
| `DAT__` | AI-DFE | Data operations (gather, status, discover) |
| `DFA__` | AI-DFE | Data fabric audit (read-only report) |
| `DHC__` | AI-DFE | Data fabric bootstrap readiness check |
| `FHC__` | AI-FLO | FLO health check — "is this workspace FLO-ready?" |
| `FIA__` | AI-FLO | FLO integrity audit — "is FLO's state correct?" |

---

## Session Detection Logic

When the user starts a session WITHOUT an explicit activation key, determine intent from their message:

| User Intent Signal | Route To |
|-------------------|----------|
| "I have an idea" / "new idea" / "evaluate this" | Load `#ai-ilc-rules/core-workflow` |
| "initiate project" / "start project" / "PIP" | Load `#ai-pilc-rules/core-workflow` |
| "portfolio" / "cross-project" / "prioritize projects" | Load `#ai-ppm-rules/core-engine` |
| "route" / "flow" / "handoff" / "where is entity" | Load `#ai-flo-rules/core-engine` |
| "backlog" / "epics" / "product ownership" / "prioritize" | Load `#ai-polc-rules/core-workflow` |
| "UX" / "personas" / "journeys" / "design system" / "user experience" | Load `#ai-uxd-rules/core-workflow` |
| "architecture" / "system design" / "containers" / "C4" | Load `#ai-adlc-rules/core-workflow` |
| "workspace" / "generate workspace" / "steering files" | Load `#ai-dwg-rules/core-generator` |
| "compliance" / "hooks" / "enforcement" / "rules derivation" | Load `#ai-gce-rules/core-generator` |
| "test governance" / "test strategy" / "coverage" | Load `#ai-tge-rules/core-engine` |
| "data" / "gather" / "DAT__" / "DFA__" / "freshness" | Load `#ai-dfe-rules/core-engine` |
| "FHC__" / "FLO health" / "is workspace ready for FLO" | Load `#ai-flo-rules/core-engine` → run FLO Health Check agent |
| "FIA__" / "FLO integrity" / "routing state" | Load `#ai-flo-rules/core-engine` → run Flow Integrity agent |
| "resume" / "continue" / "where was I" | Check `*-state.md` files for in-progress package → load that one |
| Ambiguous / general question | Ask: "Which AI-* package are you working with?" and list the keys |

---

## Resume Detection

When user says "resume" or "continue" without specifying a package:

1. Scan for any `*-state.md` with status ≠ "complete":
   - `{family}-ws/ideas/ilc-state.md` → check if an idea is in-progress
   - `{family}-ws/projects/*/pip/pilc-state.md` → check if PIP is in-progress
   - `{family}-ws/projects/*/backlog/polc-state.md` → check status field
   - `{family}-ws/projects/*/architecture/adlc-state.md` → check status
   - `{family}-ws/projects/*/ux/uxd-state.md` → check status
   - `{family}-ws/portfolio/ppm-state.md` → check status
2. If exactly ONE package is in-progress → load that package's steering and resume.
3. If MULTIPLE packages are in-progress → present the list, ask user which to resume.
4. If NONE in-progress → ask what they want to do.

---

## Multi-Package Isolation (Enforced)

- Only ONE package steering file is active at a time.
- A package switch NEVER happens without a direct user order or explicit confirmation.
- When switching, announce: "Active package: AI-{XXX}" as the first line.
- The `_ACTIVE_` key reports the current active package without switching.

---

## State Awareness (Lightweight)

> **PLACEHOLDER — populated per workspace.** A static source cannot know per-workspace package status. A future Workspace Initiator (or a manual update) fills this in from the actual `*-state.md` files. Leave as-is in the package source.

- **Active project:** {populated per workspace}
- **Packages complete:** {populated per workspace}
- **Package in-progress:** {populated per workspace}
- **Packages not started:** {populated per workspace}

> Update this section when a package transitions. This gives the orchestrator lightweight awareness without loading full state files.

---

## What This File Does NOT Do

- Does NOT contain any package workflow logic (that stays in each package's manual steering).
- Does NOT make routing decisions for the family (that is AI-FLO's job).
- Does NOT auto-activate packages based on state changes.
- Does NOT replace the activation key system — it supplements it with intent detection.

---

*Session Orchestrator v1.0.0 | AI-* PDLC Family | Author: Maheri*
