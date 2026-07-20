# Stage 2.2 — Shape (Layer 2)

> Phase 2 (Operate). Per-package JSON → one `{consumer-output}.json` per DEMAND. The consumer-tailored view.

## Purpose

Assemble each consumer's demanded output by cherry-picking, aggregating, and transforming data drawn from per-package JSON (Layer 1) — never from raw sources.

## Inputs

- `dfe-state.md` `demands.{name}` (the DEMAND spec).
- The relevant `{pkg}-data.json` files produced by gather (2.1).

## Logic

For each DEMAND in the `demands` registry:
1. For each demanded field, read its value from the declared source domain's `{pkg}-data.json`.
2. Apply the DEMAND's transform (pick, rename, aggregate across projects, compute a roll-up, etc.).
3. A missing source-domain value → field = `null` (graceful).
4. Wrap in the metadata envelope with `$package: "AI-DFE"` (demand outputs are DFE-owned aggregations) and `$schema` pointing at the DFE-owned demand/aggregation schema.
5. Validate against the DFE-owned schema (3.1). On failure → block, report, keep prior version.

## Output

One `{consumer-output}.json` per DEMAND, staged for distribution (2.3).

## Hard Rule

Layer 2 NEVER re-reads raw sources. If a needed value isn't in any `{pkg}-data.json`, it is `null` — DFE does not reach back into the source files to "fix" it. This guarantees exactly one extraction point per fact (Layer 1).

## Dashboard pane assembly (a family dashboard demand, where one is shipped)

The dashboard output (`dashboard-data.json`) is assembled entirely from Layer-1 `{pkg}-data.json` files per the demand's field map:

| Output (`data`) | From Layer-1 |
|-----------------|--------------|
| `projects[].packages[]` | each `{pkg}-data` state-derived `{ status, phase, progress, stage, blockers, artifacts }` |
| `projects[].mgmt` / `mgmtDetail` | `pilc/adlc/polc-data` register counts + detail |
| `projects[].po` | **`polc-data.data.po`** (copy 1:1 — POLC now emits the full pane) |
| `projects[].arch` | **`adlc-data.data.arch`** (copy 1:1) |
| `projects[].ux` | **`uxd-data.data.ux`** (copy 1:1) |
| `projects[].gce` | **`gce-data.data`** (copy relevant fields: `complianceTier`, `complianceScore`, `activeAgentCount`, `agents[]`, `nextTierReadiness`, `dashboard`) — `null` if GCE not run |
| `projects[].tge` | **`tge-data.data`** (copy relevant fields: `registerStats`, `riskSummary`, `depthLevel`, `observationHistory[]`) — `null` if TGE not run |
| `projects[].edges[]` | `flo-data.routes` (else canonical chain order) |
| `ideas[]` | **`ilc-data.data.ideas`** (enriched: lowercase `stage`, `brief`, `routeTarget`, `files[]`) |
| `ppm` | `ppm-data` summary (mapped to `{ totalProjects, dispatched, pending, strategicFit, topPriority }`) |
| `health` | aggregate over packages (`totalBlockers`, `stalledProjects`, `overallProgress`) |

- The `po`/`arch`/`ux` panes are a **direct copy** of the producing package's pane object — the rich shape was already built at gather (Layer 1). If a producer is absent/unrun, its pane is `null` (graceful; the renderer guards it).
- **Serialize with depth ≥ 20** so nested arrays/objects are not truncated to `@{…}` strings (ISS-014).

## MANDATORY: mgmtDetail Field-Alias Transform

The dashboard renderer (`renderMgmt()`) expects each register item to have `title` and `path`. The producer packages (PILC, POLC, ADLC) emit varying field names (`summary`, `description`, `lesson`, `risk`). Shape MUST normalise these into the dashboard contract.

### Required object shape per mgmtDetail item:

```json
{
  "id": "DEC-001",
  "title": "Event-driven architecture for integration layer",
  "status": "Approved",
  "path": "projects/PRJ-FLT-fleet-tracking/management_framework/Decision_Log.md",
  "owner": "Solutions Architect",
  "dueDate": "2026-07-01",
  "description": "Extended context (optional)"
}
```

### Field-alias rules (during Shape):

For each register type (`decisions`, `risks`, `changes`, `actions`, `issues`, `lessons`) across PILC, POLC, and ADLC data:

1. **`title`** — map from the first available source field:
   - `decisions[]` → use `summary` field
   - `risks[]` → use `risk` field
   - `changes[]` → use `description` field
   - `actions[]` → use `description` field
   - `issues[]` → use `description` field
   - `lessons[]` → use `lesson` field
   - If the item already has a `title` field → keep it (no override).

2. **`path`** — resolve from the register's known source file:
   - `decisions[]` → `projects/{project}/management_framework/Decision_Log.md`
   - `risks[]` → `projects/{project}/pip/08_Risk_Management/Risk_Register.md` (PILC) OR `projects/{project}/backlog/product-risk-register.md` (POLC)
   - `changes[]` → `projects/{project}/management_framework/Change_Log.md`
   - `actions[]` → `projects/{project}/management_framework/Action_Items.md`
   - `issues[]` → `projects/{project}/management_framework/Issue_Log.md`
   - `lessons[]` → `projects/{project}/management_framework/Lessons_Learned.md`
   - If the item already has a `path` field → keep it (no override).

3. **`owner`** / **`dueDate`** — pass through from the source if present; else omit (renderer guards).

4. **Roll-up counts** — `projects[].mgmt` = `{ decisions: N, risks: N, changes: N, actions: N, issues: N, lessons: N }` derived from the array lengths of the merged detail.

### Merge logic (multi-package registers):

The management_framework spine is shared. PILC contributes during initiation, ADLC during architecture, POLC during operations. Shape merges all contributors' register entries into one `mgmtDetail` per register type, deduplicated by `id`. When IDs conflict, the latest `lastUpdated` wins.

## MANDATORY: Artifact List Population from Progress

When a package's Layer-1 `{pkg}-data.json` has `progress[]` (stage-level) but an empty or missing `artifacts[]`, Shape MUST derive file-level artifacts from the progress array combined with the known deliverable catalog.

### Derivation rules:

For each package in each project:

1. If `artifacts[]` is already populated with objects → use as-is (apply the Artifact Object Transform above for any plain strings).
2. If `artifacts[]` is empty or `null`, AND `progress[]` exists with completed stages:
   - Look up the package's known deliverable list (from the family's published artifact catalog — see below).
   - For each known deliverable, determine status:
     - If the stage that produces it has `status: "Complete"` in `progress[]` → `"produced"`
     - If the stage is the current active stage → `"in-progress"`
     - Otherwise → `"pending"`
   - Set `path` from the output-root (Package output-root resolution table above) + the deliverable's file name.
   - Set `name` from the deliverable's display name.

### Per-package deliverable catalogs:

| Package | Known deliverables (file name → display name) |
|---|---|
| AI-ILC | `idea-register.md` → Idea Register, `evaluation-scorecard.md` → Evaluation Scorecard, `Approved_Idea_Brief.md` → Approved Idea Brief |
| AI-PILC | `01_Intake_Analysis.md` → Intake Analysis, `02_Requirements_Analysis.md` → Requirements Analysis, `03_Scope_Statement.md` → Scope Statement, `04_Feasibility_Assessment.md` → Feasibility Assessment, `05_Stakeholder_Register.md` → Stakeholder Register, `06_Risk_Register.md` → Risk Register, `07_Communication_Plan.md` → Communication Plan, `08_Business_Case.md` → Business Case, `09_Project_Charter.md` → Project Charter, `10_Resource_Plan.md` → Resource Plan, `11_Management_Framework.md` → Management Framework, `PROJECT_INITIATION_PACKAGE.md` → PIP Assembly |
| AI-POLC | `product-vision.md` → Product Vision, `roadmap.md` → Product Roadmap, `epics/` → Epic Definitions, `prioritization-scorecard.md` → Prioritization Scorecard, `sprint-backlog.md` → Sprint Backlog, `release-plan.md` → Release Plan, `acceptance-criteria.md` → Acceptance Criteria, `stakeholder-feedback.md` → Stakeholder Feedback, `definition-of-ready.md` → Definition of Ready, `definition-of-done.md` → Definition of Done, `product-risk-register.md` → Product Risk Register, `velocity-tracking.md` → Velocity Tracking, `retrospectives/` → Sprint Retrospectives, `PRODUCT_BACKLOG_PACKAGE.md` → Product Backlog Package |
| AI-UXD | `01_Research_Synthesis.md` → Research Synthesis, `02_Personas/` → Persona Profiles, `03_Journey_Maps/` → User Journey Maps, `04_Information_Architecture.md` → Information Architecture, `05_User_Flows/` → User Flow Diagrams, `06_Wireframe_Specifications/` → Wireframes, `07_Design_System/` → Design System, `08_Component_Library/` → Component Specifications, `09_Accessibility_Baseline.md` → Accessibility Baseline, `10_Prototypes.md` → Prototypes, `11_Usability_Test_Plan.md` → Usability Test Plan, `12_Usability_Results.md` → Usability Results, `13_Design_System_Docs.md` → Design System Docs, `14_Dev_Handoff/` → Dev Handoff Specs, `UX_DESIGN_PACKAGE.md` → UX Package |
| AI-ADLC | `01_Architecture_Vision.md` → Architecture Vision, `02_System_Context.md` → System Context (C4-L1), `03_Container_Diagram.md` → Container Diagram (C4-L2), `04_Technology_Stack.md` → Technology Stack, `05_Security_Identity.md` → Security Architecture, `06_Data_Architecture.md` → Data Architecture, `07_API_Architecture.md` → API Architecture, `08_Integration_Architecture.md` → Integration Architecture, `09_Infrastructure.md` → Infrastructure, `10_NFR_Specifications.md` → NFR Specifications, `11_Component_Diagrams.md` → Component Diagrams (C4-L3), `ADR/` → Architecture Decisions, `ARCHITECTURE_PACKAGE.md` → Architecture Package |

For folder-type deliverables (ending with `/`), generate a parent artifact object with nested `files[]` from the folder scan in Layer-1 data (if available).

### Non-negotiable rule:

An empty `artifacts[]` array for a package that has completed stages is a **shape bug** — it means the dashboard shows no documents for a package the user has fully run. The derivation MUST populate at least the stage-matched deliverables.

## MANDATORY: portfolioHealth Mapping

The dashboard renderer reads `D.portfolioHealth` to render a Portfolio Health section in the Stats tab (KPIs, per-project health table, alerts). Shape MUST produce this object when `ppm-data.json` is available.

### Source: `ppm-data.data`

### Mapping rules:

```
D.portfolioHealth = {
  lastRefreshed: ppm-data.$generatedOn,
  size: {
    active:  ppm-data.data.summary.active,
    paused:  ppm-data.data.summary.paused,
    retired: ppm-data.data.summary.retired
  },
  overallHealth: derive from project RAGs (all green → "healthy", any red → "at-risk", else "mixed"),
  kpis: {
    totalActive:      ppm-data.data.summary.active,
    overallProgress:  D.health.overallProgress (computed from packages),
    onTrack:          count of ppm-data.data.projects[] where healthRag == "green",
    atRisk:           count where healthRag == "amber",
    blocked:          count where healthRag == "red",
    totalBudget:      null (not tracked by PPM currently),
    budgetConsumed:   null,
    openRisks:        sum of all projects' risk counts from mgmt.risks,
    criticalRisks:    count of risks with status "Blocked" or severity "High"
  },
  projectHealth: ppm-data.data.projects[].map(p => {
    id:        p.projectId,
    name:      p.name,
    priority:  p.priority || "P" + index,
    health:    p.healthRag || "green",
    progress:  look up from projects[].progress (matched by projectId),
    budget:    "on-track" (default — no budget tracking yet),
    timeline:  "on-track" (default — derive from release dates when available),
    topRisk:   first open risk title from that project's mgmtDetail.risks[]
  }),
  alerts: derive from:
    - any project with healthRag == "red" → { type: "critical", description: "{name} is RED", action: "Review blockers" }
    - any project stalled > 7 days → { type: "warning", description: "{name} stalled", action: "Investigate" }
    - upcoming cadence events → { type: "info", description: ppm-data.data.cadence.nextPortfolioSync, action: "" }
    - if no alerts → [{ type: "info", description: "All projects healthy", action: "" }]
}
```

### Graceful degradation:

- If `ppm-data` is absent or `status: not-run` → `D.portfolioHealth = null` (renderer guards with `if (ph) {}`).
- If individual fields are null (budget, cadence) → use defaults/nulls as shown above.

## MANDATORY: Artifact Object Transform

The `packages[].artifacts` array in `dashboard-data.json` MUST contain **objects**, never plain strings. The dashboard renderer (`renderPM()`) accesses `.name`, `.status`, and `.path` on each item — plain strings produce `undefined` across the board.

### Required object shape per artifact:

```json
{
  "name": "01_Architecture_Vision.md",
  "status": "produced",
  "path": "projects/PRJ-FLT-fleet-tracking/architecture/01_Architecture_Vision.md"
}
```

### Transform rules (during Shape):

For each package in each project:

1. Read the `artifacts` field from the package's Layer-1 `{pkg}-data.json`.
2. **If items are already objects** with `name` and `status` → pass through (add `path` if missing using the output-root resolution below).
3. **If items are plain strings** (file names only) → transform each to an object:
   - `name` = the string value
   - `status` = derive from context:
     - File name matches a deliverable the package has produced (package status is `complete`, or the artifact's stage is marked done in `progress[]`) → `"produced"`
     - Package is `active` and artifact belongs to the current stage → `"in-progress"`
     - Otherwise → `"pending"`
   - `path` = resolve from the package's known output root (see table below) + the file name

### Package output-root resolution:

| Package code | Output root pattern (relative to `pdlc-ws/`) |
|---|---|
| AI-ILC | `ideas/{idea-folder}/` |
| AI-PILC | `projects/{project}/pip/` |
| AI-PPM | `portfolio/` |
| AI-POLC | `projects/{project}/backlog/` |
| AI-UXD | `projects/{project}/ux/` |
| AI-ADLC | `projects/{project}/architecture/` |
| AI-DWG | `projects/{project}/` (workspace root) |
| AI-GCE | `.governance/` |
| AI-TGE | `.governance/testing/` |
| AI-FLO | `routing/` |

When a package's output root or project context cannot be resolved → `path` = `null` (graceful; link won't work but name/status still display).

### Non-negotiable rule:

A plain-string artifact array is a **shape bug**. The schema (`dashboard-data.schema.json`) requires each item to be an object with at minimum `name` and `status`. DFE validation (3.1) will block the write if this contract is violated.

## `DAT__ aggregate`

`DAT__ aggregate` runs ONLY this stage (plus distribute), assuming per-package data is already fresh — a cheap way to refresh consumer views without re-gathering.
