<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
<!--
  PARALLEL TEMPLATE — Claude Code variant of session-orchestrator.md.
  Claude Code has NO `inclusion:` directive and does NOT auto-load `CLAUDE*.md`
  by filename glob — only a real `CLAUDE.md` (which the installer wires to import
  this file via `@CLAUDE_PDLC_ORCHESTRATOR.md`). Routing therefore uses on-demand
  `Read` of the deployed core files instead of Kiro `#hashtag` steering syntax.
  Any change to the routing/trigger semantics here MUST be mirrored in
  session-orchestrator.md (and vice versa). Enforced by INV-L3-030.
-->
# AIFLC Session Orchestrator — AI-* PDLC Family (Claude Code)

> **This is the only always-loaded steering for the AI-* PDLC Family on Claude Code.** It is imported by your workspace `CLAUDE.md` (`@CLAUDE_PDLC_ORCHESTRATOR.md`). All package workflows are deployed as `CLAUDE_PDLC_AI_<PKG>.md` files and are **not** auto-loaded — this orchestrator `Read`s the relevant one on demand. That keeps the context window free for actual work.

---

## Purpose

Prevent context overload. Instead of loading all package workflows into every session, this orchestrator:
1. Detects what the user wants to do
2. `Read`s ONLY the relevant package core file (and its rule-details on demand)
3. Provides the activation keys as a routing table

---

## Activation Keys (Quick Reference)

> **Full trigger registry (all package keys + all agent shortcuts):** `Read` `.pdlc/TRIGGER_KEYS_REFERENCE.md`

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

## Claude Code Path Map

On Claude Code, each package's core workflow is a root-level file and its rule-details live under `.pdlc/`. When you activate a package, `Read` its core file first, then its rule-details folder on demand:

| Package | Core file to `Read` | Rule-details folder (on demand) |
|---------|---------------------|---------------------------------|
| AI-ILC  | `CLAUDE_PDLC_AI_ILC.md`  | `.pdlc/ai-ilc-rule-details/`  |
| AI-PILC | `CLAUDE_PDLC_AI_PILC.md` | `.pdlc/ai-pilc-rule-details/` |
| AI-PPM  | `CLAUDE_PDLC_AI_PPM.md`  | `.pdlc/ai-ppm-rule-details/`  |
| AI-FLO  | `CLAUDE_PDLC_AI_FLO.md`  | `.pdlc/ai-flo-rule-details/`  |
| AI-POLC | `CLAUDE_PDLC_AI_POLC.md` | `.pdlc/ai-polc-rule-details/` |
| AI-UXD  | `CLAUDE_PDLC_AI_UXD.md`  | `.pdlc/ai-uxd-rule-details/`  |
| AI-ADLC | `CLAUDE_PDLC_AI_ADLC.md` | `.pdlc/ai-adlc-rule-details/` |
| AI-DWG  | `CLAUDE_PDLC_AI_DWG.md`  | `.pdlc/ai-dwg-rule-details/`  |
| AI-GCE  | `CLAUDE_PDLC_AI_GCE.md`  | `.pdlc/ai-gce-rule-details/`  |
| AI-TGE  | `CLAUDE_PDLC_AI_TGE.md`  | `.pdlc/ai-tge-rule-details/`  |
| AI-DFE  | `CLAUDE_PDLC_AI_DFE.md`  | `.pdlc/ai-dfe-rule-details/`  |

> If a core file is not present at the workspace root, that package was not installed in this bundle — tell the user which packages are available and how to install the missing one.

---

## Session Detection Logic

When the user starts a session WITHOUT an explicit activation key, determine intent from their message, then `Read` the matching core file:

| User Intent Signal | Route To (`Read`) |
|-------------------|-------------------|
| "I have an idea" / "new idea" / "evaluate this" | `CLAUDE_PDLC_AI_ILC.md` |
| "initiate project" / "start project" / "PIP" | `CLAUDE_PDLC_AI_PILC.md` |
| "portfolio" / "cross-project" / "prioritize projects" | `CLAUDE_PDLC_AI_PPM.md` |
| "route" / "flow" / "handoff" / "where is entity" | `CLAUDE_PDLC_AI_FLO.md` |
| "backlog" / "epics" / "product ownership" / "prioritize" | `CLAUDE_PDLC_AI_POLC.md` |
| "UX" / "personas" / "journeys" / "design system" / "user experience" | `CLAUDE_PDLC_AI_UXD.md` |
| "architecture" / "system design" / "containers" / "C4" | `CLAUDE_PDLC_AI_ADLC.md` |
| "workspace" / "generate workspace" / "steering files" | `CLAUDE_PDLC_AI_DWG.md` |
| "compliance" / "hooks" / "enforcement" / "rules derivation" | `CLAUDE_PDLC_AI_GCE.md` |
| "test governance" / "test strategy" / "coverage" | `CLAUDE_PDLC_AI_TGE.md` |
| "data" / "gather" / "DAT__" / "DFA__" / "freshness" | `CLAUDE_PDLC_AI_DFE.md` |
| "FHC__" / "FLO health" / "is workspace ready for FLO" | `CLAUDE_PDLC_AI_FLO.md` → run FLO Health Check agent |
| "FIA__" / "FLO integrity" / "routing state" | `CLAUDE_PDLC_AI_FLO.md` → run Flow Integrity agent |
| "resume" / "continue" / "where was I" | Check `*-state.md` files for in-progress package → `Read` that one |
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
2. If exactly ONE package is in-progress → `Read` that package's core file and resume.
3. If MULTIPLE packages are in-progress → present the list, ask user which to resume.
4. If NONE in-progress → ask what they want to do.

---

## Multi-Package Isolation (Enforced)

- Only ONE package core is active at a time.
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

- Does NOT contain any package workflow logic (that stays in each package's core file).
- Does NOT make routing decisions for the family (that is AI-FLO's job).
- Does NOT auto-activate packages based on state changes.
- Does NOT replace the activation key system — it supplements it with intent detection.

---

*Session Orchestrator v1.0.0 (Claude Code variant) | AI-* PDLC Family | Author: Maheri*
