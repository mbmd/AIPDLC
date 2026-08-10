# SOURCE_MAP — AI-PILC

> Declares where AI-PILC's raw data lives and how AI-DFE extracts it. Paths relative to `pdlc-ws/`.

**Package:** AI-PILC — AI-Driven Project Initiation Life Cycle
**Schema:** `pilc-data.schema.json` (this folder)
**Schema version:** 1.0.0
**Scope:** per-project

---

## Presence Check

| Check | Path | Meaning if absent |
|-------|------|-------------------|
| Marker exists | `projects/PRJ-{ABBREV}-{slug}/pip/pilc-state.md` | `status: not-run` → all payload fields `null` |

## Source Files

| # | Source path (relative to `pdlc-ws/`) | Holds |
|---|-------------------------------------------|-------|
| 1 | `projects/PRJ-{ABBREV}-{slug}/pip/pilc-state.md` | state, projectId, status, phase, depth, progress, register counts |
| 2 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Decision_Log.md` | project decisions |
| 3 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Change_Log.md` | scope changes |
| 4 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Issue_Log.md` | issues/blockers |
| 5 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Action_Items.md` | actions |
| 6 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Assumptions_Dependencies.md` | assumptions |
| 7 | `projects/PRJ-{ABBREV}-{slug}/management_framework/Lessons_Learned.md` | lessons |
| 8 | `projects/PRJ-{ABBREV}-{slug}/pip/08_Risk_Management/Risk_Register.md` | risks |

## Field Extraction

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `projectId` | 1 | Configuration table → `Project ID` row value |
| `projectName` | 1 | Configuration table → `Project Name` row value |
| `projectHandle` | 1 | Configuration table → `Project Handle` row value |
| `status` | 1 | Configuration table → `Status` row value |
| `currentPhase` | 1 | Configuration table → `Current Phase` row value |
| `currentStage` | 1 | Configuration table → `Current Stage` row value (integer) |
| `workflowDepth` | 1 | Configuration table → `Workflow Depth` row value |
| `started` | 1 | Configuration table → `Started` row value (ISO 8601) |
| `lastUpdated` | 1 | Configuration table → `Last Updated` row value (ISO 8601) |
| `producerVersion` | 1 | Configuration table → `Producer Version` row value |
| `route` | 1 | Configuration table → `Route` row value |
| `derivedFrom` | 1 | Configuration table → `derivedFrom` row value |
| `progress[]` | 1 | Progress table → one object per row: `{ stage, name, status, completed, notes }` |
| `registerCounts` | 1 | Register Counts table → `{ decisions, changes, issues, actions, assumptions, lessons }` |
| `decisions[]` | 2 | One object per table row: `{ id, date, summary, status }` |
| `changes[]` | 3 | One object per table row: `{ id, date, description, status }` |
| `issues[]` | 4 | One object per table row: `{ id, description, priority, status, owner }` |
| `actions[]` | 5 | One object per table row: `{ id, description, owner, due, status }` |
| `assumptions[]` | 6 | One object per table row: `{ id, assumption, status, validated }` |
| `lessons[]` | 7 | One object per table row: `{ id, lesson, stage, captured }` |
| `risks[]` | 8 | One object per table row: `{ id, risk, probability, impact, score, mitigation, owner, status }` |

## AI-LENS Fields (AI_LENS_PROTOCOL §6.2)

> Present when the project has an AI-mode decision recorded in the spine Decision_Log (set by PILC at inception via the AI-LENS Resolution Protocol).

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `aiLens.aiMode` | 9 | Latest `Decision_Log` row where Decision contains "AI-LENS" or "AI Lens mode" → derive `no-ai` or `ai-powered`. `null` if no AI-mode row exists. |
| `aiLens.aiSubModes[]` | 9 | From the same Decision_Log row → parse chosen sub-modes array: `["opportunity"]`, `["augmented","native"]`, etc. Empty array if `no-ai`. |
| `aiLens.aiFeasibility` | 10 | PIP feasibility section (or `pilc-state.md` `dashboard-summary.aiFeasibility` if emitted) → free-text summary. `null` if not assessed. |
| `aiLens.aiCostModel` | 10 | PIP business case AI-cost section → cost model indicator: `token-metered`, `gpu-compute`, `managed-api`, `hybrid`. `null` if not assessed. |
| `aiLens.aiRiskLevel` | 10 | PIP risk section AI-specific risk → `low`, `medium`, `high`, `critical`. `null` if not assessed. |
| `aiLens.euAiActClass` | 10 | PIP feasibility section EU AI Act assessment → `minimal`, `limited`, `high`, `unacceptable`. `null` if not assessed. |

> **Source additions for AI-LENS:**
> - **#9** = `projects/PRJ-{ABBREV}-{slug}/management_framework/Decision_Log.md` — shared spine, AI-mode rows (prefix `PILC-{ABBREV}-D-*` with "AI-LENS" in Decision column).
> - **#10** = `projects/PRJ-{ABBREV}-{slug}/pip/` — PIP deliverables containing AI feasibility, cost, risk, EU AI Act sections (exact file determined by stage output — typically `03_feasibility-assessment.md` and `04_business-case.md`).

## Retention Policy

| Policy | Value |
|--------|-------|
| History retention | forever |

## Notes

- PILC is per-project scoped: one `pilc-data.json` per project (keyed by `projectId`). DFE iterates `projects/PRJ-…/` to gather across projects.
- The management_framework registers are shared with AI-ADLC (which appends its own entries). DFE attributes rows by their phase prefix (`PILC-{ABBREV}-*`).
- Numbered subfolder paths (`01_*/`, `02_*/`, etc.) are not read by DFE — their content is too unstructured for machine extraction. DFE reads the state file (summary) and the registers (structured tables).


## Automation-LENS Fields (AUTOMATION_LENS_PROTOCOL §6.2)

> Present when the project has an automation-mode decision recorded in the spine Decision_Log (set by PILC at inception via the Automation-LENS Resolution Protocol).

| Field path (in `data`) | Source (#) | Extraction rule |
|------------------------|------------|-----------------|
| `automationLens.automationMode` | 9 | Latest `Decision_Log` row where Decision contains "Automation Lens" or "Automation mode" → derive `manual` or `automated`. `null` if no automation-mode row exists. |
| `automationLens.automationSubModes[]` | 9 | From the same Decision_Log row → parse chosen sub-modes array: `["assisted"]`, `["attended","unattended"]`, etc. Empty array if `manual`. |
| `automationLens.processSuitability` | 10 | PIP assessment section (or `pilc-state.md` `dashboard-summary.processSuitability` if emitted) → free-text summary. `null` if not assessed. |
| `automationLens.automationRoi` | 10 | PIP business case automation-ROI section → ROI summary (hours saved, FTE, error-rate, cycle-time). `null` if not assessed. |
| `automationLens.automationControlClass` | 10 | PIP feasibility section automation control class → `informational`, `operational`, `controlled`, `safety-critical`. `null` if not assessed. |

> **Source additions for Automation-LENS:**
> - **#9** = `projects/PRJ-{ABBREV}-{slug}/management_framework/Decision_Log.md` — shared spine, automation-mode rows (prefix `PILC-{ABBREV}-D-*` with "Automation" in Decision column).
> - **#10** = `projects/PRJ-{ABBREV}-{slug}/pip/` — PIP deliverables containing process suitability, automation ROI, and control class sections.
