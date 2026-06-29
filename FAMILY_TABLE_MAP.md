# AI-* Family Table — File Map

**Purpose:** Registry of all files that contain the AI-* Family chain diagram and/or Package/Type/Input/Output table. Use this to quickly locate and update all instances when the canonical table changes.

**Canonical Source:** `FAMILY_TABLE_MAP.md` → "Canonical Family Table (Copy From Here)" section below

**Rule:** Any new file that includes the AI-* Family table MUST be added to this map.

---

## Files Containing the Family Table

### Package READMEs

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 1 | `ai-gce/README.md` | ✅ | ✅ | ✅ |
| 2 | `ai-pilc/README.md` | ✅ | ✅ | ✅ |
| 3 | `ai-adlc/README.md` | ✅ | ✅ | ✅ |
| 4 | `ai-dwg/README.md` | ✅ | ✅ | ✅ |
| 21 | `ai-ilc/README.md` | ✅ | ✅ | ✅ |
| 28 | `ai-polc/README.md` | ✅ | ✅ | ✅ |
| 31 | `ai-ppm/README.md` | ✅ | ✅ | ✅ |
| 34 | `ai-uxd/README.md` | ✅ | ✅ | ✅ |
| 36 | `ai-flo/README.md` | ✅ | ✅ | ✅ |
| 27 | `ai-tge/README.md` | ✅ | ✅ | ✅ |
| 40 | `ai-dfe/README.md` | ✅ | ✅ | ✅ |

### Core Workflow / Generator Files (Runtime Rules)

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 5 | `ai-pilc/ai-pilc-rules/core-workflow.md` | ✅ | ❌ (diagram-only — WFO_S01) | ❌ |
| 6 | `ai-adlc/ai-adlc-rules/core-workflow.md` | ✅ | ✅ | ✅ |
| 7 | `ai-dwg/ai-dwg-rules/core-generator.md` | ✅ | ✅ | ✅ |
| 8 | `ai-gce/ai-gce-rules/core-generator.md` | ✅ | ✅ | ✅ |
| 22 | `ai-ilc/ai-ilc-rules/core-workflow.md` | ✅ | ✅ | ✅ |
| 26 | `ai-tge/ai-tge-rules/core-engine.md` | ✅ | ✅ | ✅ |
| 29 | `ai-polc/ai-polc-rules/core-workflow.md` | ✅ | ✅ | ✅ |
| 32 | `ai-ppm/ai-ppm-rules/core-engine.md` | ✅ | ✅ | ✅ |
| 35 | `ai-uxd/ai-uxd-rules/core-workflow.md` | ✅ | ✅ | ✅ |
| 37 | `ai-flo/ai-flo-rules/core-engine.md` | ✅ | ❌ (diagram-only — WFO_S01 converted) | ❌ |
| 41 | `ai-dfe/ai-dfe-rules/core-engine.md` | ✅ | ✅ (pending WFO_S01 diagram-only conversion) | ✅ |

> **Note (2026-06-11, Step 5.3):** #28/#29/#30 added — AI-POLC built and test-validated (TR-016/102/301/501 all PASS). All three files authored with the **current AI-UXD-inclusive canonical** (verified during TR-016 Phase 1.2). AI-POLC ships `setup/INSTALL.md` only — no setup steering mirror (consistent with AI-DWG/AI-GCE/AI-TGE/AI-ILC).

> **Note (2026-06-11, AI-PPM build):** #31/#32/#33 added — AI-PPM built and structural dry test PASSED (7/7 phases, zero failures). All three files authored with the **current AI-UXD-inclusive canonical**. AI-PPM ships `setup/INSTALL.md` only — no setup steering mirror (consistent with newer packages).

> **Note (2026-06-12, AI-UXD build):** #34/#35 added — AI-UXD built (42 files; 5 phases / 16 stages / 15 templates / 1 agent). Both files authored with the **current canonical**. AI-UXD ships `setup/INSTALL.md` only. Process-overview does NOT contain the family table (only internal workflow diagram) — therefore not registered.

> **Note (2026-06-12, AI-FLO build):** #36/#37 added — AI-FLO built (30 files; 3 phases / 10 stages / 9 templates / 1 agent). Both files authored with the **current canonical**. AI-FLO ships `setup/INSTALL.md` only. Process-overview does NOT contain the family table — not registered. Footnote ³ updated (AI-FLO is now built; no pending packages remain).

> **Note (2026-06-10, OI-027 / Plan 1.4):** #26 added — AI-TGE core file previously lacked the family table (gap). It was authored directly with the **current AI-UXD-inclusive canonical** (`AP+PBP+UXP`, AI-UXD row, footnote ³). It is therefore **ahead** of the 22 files awaiting the Step 1.5 AI-UXD top-up — Step 1.5 should treat #26 as already-current and not re-touch it.

> **Note (2026-06-12, OI-027 completion):** #27 added — AI-TGE `README.md` authored with the **current canonical** (all packages built, footnote ³ updated). Registered as #27 in Package READMEs table. OI-027 now fully resolved (core #26 + README #27). Also resolves OI-032 Step 5 (G2 standalone usage section included).

### Setup Copies (Mirror of Core Files)

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 9 | `ai-pilc/setup/.kiro/steering/ai-pilc-rules/core-workflow.md` | ✅ | ❌ (diagram-only — WFO_S01) | ❌ |
| 10 | `ai-adlc/setup/.kiro/steering/ai-adlc-rules/core-workflow.md` | ✅ | ✅ | ✅ |

> **Note (2026-06-10, OI-022):** Only **AI-PILC** and **AI-ADLC** pre-stage a setup steering core mirror. The newer packages (**AI-DWG, AI-GCE, AI-TGE, AI-ILC**) ship `setup/INSTALL.md` only — no pre-staged `.kiro/steering/.../core-workflow.md` copy. The former #23 (`ai-ilc/.../setup/.../core-workflow.md`) was **de-registered** as it does not exist and AI-ILC follows the INSTALL-only convention.

### PLAN Files

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 11 | `ai-dwg/PLAN.md` | ✅ | ✅ | ✅ |
| 12 | `ai-gce/PLAN.md` | ✅ | ✅ | ✅ |
| 20 | `ai-ilc/PLAN.md` | ✅ | ✅ | ✅ |
| 25 | `ai-tge/PLAN.md` | ✅ (bespoke) | ❌ | ❌ |
| 38 | `ai-ppm/PLAN.md` | ✅ | ✅ | ✅ |

### Structure & Documentation Files

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 13 | `FAMILY_STRUCTURE.md` | ✅ | ✅ | ✅ |
| 15 | `narrative/WHITEPAPER.md` | ✅ | ✅ | ✅ |
| 39 | `README.md` (root) | ✅ | ⚠️ simplified variant | ⚠️ partial |

> **Note:** Entry #14 (internal build README) de-registered from this publishable map (2026-06-18, DISC-001). That file is tracked internally and is not part of the published family surface.

> **Note (2026-06-15, OI-052):** The root `README.md` is now registered. It carries the **canonical chain diagram** (✅ — must stay verbatim-synced per Rule 10) but uses an **intentional simplified public-README "Packages" table** (columns: Layer / Package / Type / What It Does) instead of the canonical Input/Output table. This simplified table is an **approved presentation variant** for the top-level README and is **exempt from canonical Input/Output table propagation** — only its diagram is propagation-bound. When the canonical diagram changes, update this file's diagram; the simplified table is maintained independently for readability.

### Rule-Detail Process Overviews (Diagram Only)

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 16 | `ai-dwg/ai-dwg-rule-details/common/process-overview.md` | ✅ | ❌ | ❌ |
| 17 | `ai-gce/ai-gce-rule-details/common/process-overview.md` | ✅ | ❌ | ❌ |
| 18 | `ai-adlc/ai-adlc-rule-details/common/process-overview.md` | ✅ | ✅ | ✅ |
| 19 | `ai-tge/ai-tge-rule-details/common/process-overview.md` | ✅ | ✅ | ✅ |
| 24 | `ai-ilc/ai-ilc-rule-details/common/process-overview.md` | ✅ | ✅ | ✅ |
| 30 | `ai-polc/ai-polc-rule-details/common/process-overview.md` | ✅ | ✅ | ✅ |
| 33 | `ai-ppm/ai-ppm-rule-details/common/process-overview.md` | ✅ | ✅ | ✅ |

> **Note (2026-06-27, AI-DFE build / Phase E3):** #40 (`ai-dfe/README.md`) + #41 (`ai-dfe/ai-dfe-rules/core-engine.md`) added. **AI-DFE is NOT added as a row to the canonical Package/Type/Input/Output table** — like AI-FLO, it is a continuous engine that operates *alongside* the whole family (it reads every package's marker as a gather trigger; it has no single Input→Output chain cell). It is represented by the existing "AI-DFE's role relative to the table" explanatory note carried beneath the verbatim table in its own files (decision E3-A, 2026-06-27). Both files reproduce the **current 11-row canonical verbatim** + the AI-DFE role note; they are registered here as diagram+table propagation targets. The core (#41) still carries the full table and is a **pending WFO_S01 diagram-only conversion** target (tracked by `WFO_FAMILY_ROLLOUT_PLAN.md`), consistent with the WFO_S01 diagram-only conversion approach (#37 AI-FLO is already converted to diagram-only — see its row above).

---

## Total: 39 registry entries

> **Count note (2026-06-27):** Highest entry ID is now #41 (`ai-dfe/ai-dfe-rules/core-engine.md`). Actual count = **39** because #14 (internal file — de-registered DISC-001) and #23 (`ai-ilc/.../setup/.../core-workflow.md`, non-existent — de-registered OI-022) are both removed (41 IDs − 2 de-registered = 39). AI-DFE added 2 entries (#40 README, #41 core-engine) without changing the canonical table (alongside-engine, E3-A).

**OI-018 reshape propagation (2026-06-10):**
- **20** full canonical-table files updated to the reshaped two-layer table (#1–15, #18, #19, #21, #22, #24).
- **2** diagram-only files updated (#16, #17).
- **22 content files total** now carry the reshaped canonical (verified: `grep "PORTFOLIO LAYER"`).

**AI-UXD canonical top-up (2026-06-10, Plan 1.5 / OI-028):**
- The canonical was later extended to add **AI-UXD** (new Project-layer row, `AI-UXD ───┤` diagram node + `AI-UXD ⇢ AI-POLC … AI-DLC v1 ⇢ AI-UXD+AI-POLC (feedback)` line, AI-DWG input `AP + PBP` → `AP + PBP + UXP`, footnote ³ expanded).
- Re-propagated verbatim to the same **22 content files** (20 full-table + 2 diagram-only) — verified line-exact: AI-UXD diagram node = 1, Design UX line = 1, feedback line = 1 in every file; AI-UXD table row = 1 and zero bare `| AP + PBP |` in all 20 full-table files.
- **#26** (`ai-tge/ai-tge-rules/core-engine.md`) was authored already-current in Plan 1.4 — **excluded** from the top-up (not re-touched).
- AI-TGE's **bespoke** companion sub-diagram in #19 (`### AI-TGE Position (Companion Pattern)`) was left untouched (already UXD-correct from OI-019/Plan 1.3).
- **2** special-handling files (see table below): #20 (historical snapshot — pointer added), #25 (bespoke companion diagram — deferred to OI-019).
- **De-registered:** former #23 (AI-ILC setup mirror) — does not exist; AI-ILC ships INSTALL-only (OI-022).
- Old linear diagram intentionally retained in: the internal build assessment snapshot (excluded), `ai-ilc/PLAN.md` §4.1 (historical), and an archival idea record.

> **Note:** Files #20–24 are AI-ILC's. #20 (PLAN.md) exists (historical snapshot); #21/#22/#24 updated to the reshaped canonical; **#23 de-registered (2026-06-10, OI-022)** — AI-ILC ships INSTALL-only setup, no steering mirror (consistent with AI-DWG/AI-GCE/AI-TGE). AI-ILC was added to the canonical chain as an optional pre-stage on 2026-06-08 (idea 002, approved).
> **#25** (`ai-tge/PLAN.md`) added to the registry 2026-06-10; reclassified as bespoke companion diagram (no canonical table).

### Intentionally Excluded (not propagation targets)

| File | Reason |
|------|--------|
| _(internal build assessment snapshot)_ | Point-in-time assessment snapshot — documents a past chain state; rewriting its embedded diagram would falsify the historical record. Left as-is by decision (Plan Phase 1.1, 2026-06-10). |
| `session-orchestrator.md` | **Not a family-table file (OI-127, 2026-06-24).** The always-loaded session orchestrator carries an *activation-keys routing table* (key → package → when-to-use), NOT the AI-* Family chain diagram or the Package/Type/Input/Output table. Therefore it is not a propagation target for canonical-table changes. Recorded here so its absence from the registry is intentional, not an omission. |

### Special Handling (OI-018 propagation, 2026-06-10)

| File | # | Treatment |
|------|---|-----------|
| `ai-ilc/PLAN.md` | 20 | **Historical snapshot.** Its §4.1 table documents the AI-ILC *addition* proposal (linear canonical). Table NOT overwritten; a "SUPERSEDED" pointer to the reshaped canonical was added instead (same principle as the excluded assessment file). |
| `ai-ilc/.../setup/.../core-workflow.md` | ~~23~~ | **De-registered (OI-022, 2026-06-10).** Does not exist; AI-ILC ships INSTALL-only setup (no steering mirror), consistent with AI-DWG/AI-GCE/AI-TGE. Only AI-PILC (#9) and AI-ADLC (#10) pre-stage a mirror. |
| `ai-tge/PLAN.md` | 25 | **Bespoke companion diagram, not the canonical table.** Carries the "Family Position (Companion Pattern)" illustration showing AI-TGE alongside the chain. Redraw for the reshaped (two-layer) topology is deferred to **OI-019** (AI-GCE/AI-TGE repositioning), not OI-018. |
| `ai-tge/ai-tge-rule-details/common/process-overview.md` | 19 | Main canonical table updated (OI-018 ✅). It ALSO has a bespoke companion sub-diagram lower down → redraw deferred to **OI-019**. |

### Pending New Packages (registered in canonical, files not yet built)

The 2026-06-10 reshape added three packages to the canonical table. Their table-bearing
files do not exist yet and will be added to the numbered registry above **as each is built**:

| Package | Layer | Status | Idea Ref |
|---------|-------|--------|----------|
| **AI-PPM** | Portfolio | ✅ Built & registered (#31/#32/#33) | idea 007 |
| **AI-FLO** | Edge (router) | ✅ Built & registered (#36/#37) | idea 008 |
| **AI-POLC** | Project | ✅ Built & registered (#28/#29/#30) | idea 006 |
| **AI-UXD** | Project | ✅ Built & registered (#34/#35) | idea 010 (Approved) |

> **AI-UXD** was added to the canonical Project layer on 2026-06-10 (idea 010 approved) as a fourth pending package — separate from the reshape's original three. It runs parallel to AI-ADLC/AI-POLC, produces personas/journeys consumed by AI-POLC, feeds AI-DWG (design system → `frontend-standards.md` + new `design-system.md`) and AI-GCE (accessibility baseline → new `accessibility-compliance` rule), and receives AI-DLC v1 feedback. Its table-bearing files will be added to the numbered registry as built.

> **AI-TGE** already has a registry entry (#19, process-overview) and is now reflected in the
> canonical Project layer. Its remaining table-bearing files follow the standard build flow.

---

## Update Procedure

When the canonical table changes:

1. Update the "Canonical Family Table (Copy From Here)" section in THIS file **first**
2. Propagate verbatim to all listed files that contain the **full table** (excluding diagram-only files)
3. Files #16-17 (diagram-only) need only the **chain diagram** portion updated
4. **Propagate footnote ³ separately** if its text changed (even without table changes). Run the footnote-consistency check script to detect drift; use `-Fix` to auto-correct all registered files.
5. Verify table propagation with: `grep -rl "PORTFOLIO LAYER" ` (should hit every full-table file once the reshape is propagated — see OI-018)
6. Verify layer/router propagation with: `grep -rl "AI-FLO" ` and `grep -rl "AI-PPM" `

### ⚠️ Self-Exclusion Rule (Family Table Consistency Check)

`FAMILY_TABLE_MAP.md` is the **canonical SOURCE** of the family table — it is NOT a propagation target. The "Family Table Consistency Check" hook must **exclude this file**:

- When this file changes, do **NOT** flag or revert its table against any embedded/hard-coded snapshot in the hook. The hook's embedded table is a point-in-time copy and may lag behind this source.
- This file defines what "canonical" means. All other files are checked **against** this file — never the reverse.
- If the hook's embedded table differs from the table here, the table **here** wins, and the hook text is considered stale.

### Canonical Family Table (Copy From Here)

The family is organized into two **layers** joined by a **router on the edge**: the
Portfolio layer reasons across MANY projects; the Project layer executes ONE project.

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

> **AI-DWG Input semantics (peer-input model, OI-069 / decision 0.2 — 2026-06-15c):** The `AP + PBP + UXP` cell lists AI-DWG's three **inputs** (AP = AI-ADLC, PBP = AI-POLC, UXP = AI-UXD). In the default sequential flow, all three are guaranteed present by the time DWG starts (ADLC is the terminal predecessor). AI-DWG still accepts **any non-empty subset (≥1 of the three)** for brownfield/partial scenarios and generates only the output clusters whose input is present; absent inputs trigger a quality-impact disclosure + user approval (per `DWG_CONVERGENCE_DESIGN.md` Law 1). The cell text is kept **verbatim** as a compact input list — this note carries the semantics so no per-file table change/propagation is required.

---

*Created: 2026-06-07 | Last Updated: 2026-06-18 (OI-114 Phase 1: canonical diagram + table + footnote ³ updated from parallel to sequential topology — POLC→UXD→ADLC→DWG; Input columns corrected: POLC=PIP, UXD=PIP+PBP, ADLC=PIP+PBP+UXP; DWG semantics note updated for sequential guarantee; row order corrected to match execution sequence; total 39 entries)*
