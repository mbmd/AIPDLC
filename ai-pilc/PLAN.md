# AI-PILC — Package Build Plan

**Package:** AI-PILC (AI-Driven Project Initiation Life Cycle)
**Type:** Interactive workflow (lifecycle)
**Status:** ✅ Complete (v1.0.0) — first package built in the AI-* Family
**Build Session:** S05 (2026-06-04)
**Persona:** `#persona-pmo-project-manager`

---

## Summary Report

| Field | Value |
|-------|-------|
| Status | ✅ COMPLETE — fully built and passing dry tests (TR-028) |
| Sessions | S05 (2026-06-04): Initial build | Multiple subsequent sessions: hardening, traceability, sub-role embedding |
| Scope | v1.0 — Full project initiation lifecycle (16 stages, 6 phases) |
| Key Decisions | PMO-grade quality, PMBOK/PRINCE2 aligned, three-tier depth, 6 management registers |
| Persona | `#persona-pmo-project-manager` (auto-loaded via `ai-pilc-rules.md`) |

---

## Package Identity

| Field | Value |
|-------|-------|
| **Name** | AI-PILC |
| **Full Title** | AI-Driven Project Initiation Life Cycle |
| **Package Type** | Interactive workflow (lifecycle) |
| **Primary Input** | Raw requirement |
| **Primary Output** | Project Initiation Package (PIP) |
| **User Persona** | Project Manager, PMO Professional, Programme Manager |
| **Family Position** | First node in chain. Project layer it feeds runs: AI-PILC → AI-POLC → AI-UXD → AI-ADLC → AI-DWG → AI-GCE/TGE |
| **Marker File** | `pilc-state.md` |

---

## Design Decisions

| # | Decision | Resolution |
|---|----------|-----------|
| 1 | Package type | Interactive lifecycle — user approves at every gate |
| 2 | Phase count | 6 phases (Inception → Assessment → Justification → Authorization → Planning → Mobilization) |
| 3 | Stage count | 16 stages (one deliverable per stage) |
| 4 | Depth model | Three-tier: Minimal / Standard / Comprehensive |
| 5 | Framework alignment | PMBOK + PRINCE2 terminology and process structure |
| 6 | Register model | 6 management registers (Decision, Change, Issue, Action, Assumptions, Lessons) |
| 7 | Template approach | 100% generic with `{placeholder}` syntax |
| 8 | State management | `pilc-state.md` — full session continuity |
| 9 | Sub-roles | Stage-layered: BA, Risk Analyst, Financial Analyst, Resource Planner, Change Manager |

---

## File Structure

```
ai-pilc/
├── README.md
├── LICENSE
├── NOTICE
├── PLAN.md                              ← This file (retroactive)
├── WHITEPAPER.md
├── CONCEPTUAL_MAP.md
├── ai-pilc-rules/
│   └── core-workflow.md                 ← Master orchestration (always loaded)
├── ai-pilc-rule-details/
│   ├── common/                          ← Cross-cutting rules (5 files)
│   │   ├── content-validation.md
│   │   ├── process-overview.md
│   │   ├── question-format-guide.md
│   │   ├── session-continuity.md
│   │   └── welcome-message.md
│   ├── inception/                       ← Stages 1-3
│   │   ├── workspace-detection.md
│   │   ├── source-ingestion.md
│   │   └── requirement-structuring.md
│   ├── assessment/                      ← Stages 4-7
│   │   ├── requirements-analysis.md
│   │   ├── clarification-cycle.md
│   │   ├── feasibility-assessment.md
│   │   └── prioritization.md
│   ├── justification/                   ← Stage 8
│   │   └── business-case.md
│   ├── authorization/                   ← Stage 9
│   │   └── project-charter.md
│   ├── planning/                        ← Stages 10-14
│   │   ├── stakeholder-management.md
│   │   ├── scope-definition.md
│   │   ├── resource-budget.md
│   │   ├── risk-management.md
│   │   └── governance-communication.md
│   ├── mobilization/                    ← Stages 15-16
│   │   ├── kickoff-preparation.md
│   │   └── package-assembly.md
│   └── templates/                       ← 17 deliverable templates
│       ├── agents/                      ← Agent template + shortcut + guide
│       ├── action-items.md
│       ├── assumptions-dependencies.md
│       ├── business-case.md
│       ├── change-log.md
│       ├── decision-log.md
│       ├── feasibility-assessment.md
│       ├── issue-log.md
│       ├── kickoff-agenda.md
│       ├── lessons-learned.md
│       ├── management-framework.md
│       ├── project-charter.md
│       ├── project-status-dashboard-template.md
│       ├── raci-matrix.md
│       ├── requirement-intake-form.md
│       ├── resource-plan.md
│       ├── risk-register.md
│       ├── scope-statement.md
│       └── stakeholder-register.md
└── setup/
    ├── INSTALL.md
    └── TEST_MODE_USER_GUIDE.md
```

---

## Build Sequence

| Step | Activity | Status |
|------|----------|--------|
| 1 | Define Problem Space | ✅ Done |
| 2 | Research & Extract (PMBOK, PRINCE2) | ✅ Done |
| 3 | Present Plan for Approval | ✅ Done |
| 4 | Build Core File (`core-workflow.md`) | ✅ Done |
| 5 | Build Common Files (5 files) | ✅ Done |
| 6 | Build Stage Detail Files (16 files across 6 phase folders) | ✅ Done |
| 7 | Build Templates (17 deliverable templates) | ✅ Done |
| 8 | Build Agent Templates (3 files) | ✅ Done |
| 9 | Build README + LICENSE + INSTALL | ✅ Done |
| 10 | Build WHITEPAPER | ✅ Done |
| 11 | Verify (Dry Test — TR-028) | ✅ PASS |
| 12 | Register in FAMILY_TABLE_MAP.md | ✅ Done |

---

## Applicable Lessons

| Lesson | How Applied |
|--------|------------|
| L1 | "Life Cycle" naming — correct for interactive multi-phase workflow |
| L2 | Sub-roles per stage (BA, Risk Analyst, etc.) |
| L4 | Adaptive intake — multiple input modes (raw requirement / verbal / document) |
| L6 | OR-input pattern — PIP can be standalone or chain-fed |
| L7 | Conditional generation — depth drives what's produced |
| L11 | Family table in README + core-workflow |
| L13 | Explicit I/O contract (raw requirement → PIP) |
| L14 | Marker file: `pilc-state.md` |

---

*Created retroactively: 2026-06-13 | Original build: 2026-06-04 (Session S05)*
