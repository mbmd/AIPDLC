# AI-* Family Table — File Map

**Purpose:** Registry of all files that contain the AI-* Family chain diagram and/or Package/Type/Input/Output table. Use this to quickly locate and update all instances when the canonical table changes.

**Canonical Source:** `ai-packages/FAMILY_TABLE_MAP.md` → "Canonical Family Table (Copy From Here)" section below

**Rule:** Any new file that includes the AI-* Family table MUST be added to this map.

---

## Files Containing the Family Table

### Package READMEs

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 1 | `ai-packages/ai-gce/README.md` | ✅ | ✅ | ✅ |
| 2 | `ai-packages/ai-pilc/README.md` | ✅ | ✅ | ✅ |
| 3 | `ai-packages/ai-adlc/README.md` | ✅ | ✅ | ✅ |
| 4 | `ai-packages/ai-dwg/README.md` | ✅ | ✅ | ✅ |
| 21 | `ai-packages/ai-ilc/README.md` | ✅ | ✅ | ✅ |

### Core Workflow / Generator Files (Runtime Rules)

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 5 | `ai-packages/ai-pilc/ai-pilc-rules/core-workflow.md` | ✅ | ✅ | ✅ |
| 6 | `ai-packages/ai-adlc/ai-adlc-rules/core-workflow.md` | ✅ | ✅ | ✅ |
| 7 | `ai-packages/ai-dwg/ai-dwg-rules/core-generator.md` | ✅ | ✅ | ✅ |
| 8 | `ai-packages/ai-gce/ai-gce-rules/core-generator.md` | ✅ | ✅ | ✅ |
| 22 | `ai-packages/ai-ilc/ai-ilc-rules/core-workflow.md` | ✅ | ✅ | ✅ |
| 26 | `ai-packages/ai-tge/ai-tge-rules/core-engine.md` | ✅ | ✅ | ✅ |

> **Note (2026-06-10, OI-027 / Plan 1.4):** #26 added — AI-TGE core file previously lacked the family table (Lesson 11 gap). It was authored directly with the **current AI-UXD-inclusive canonical** (`AP+PBP+UXP`, AI-UXD row, footnote ³). It is therefore **ahead** of the 22 files awaiting the Step 1.5 AI-UXD top-up — Step 1.5 should treat #26 as already-current and not re-touch it. **AI-TGE `README.md` does not exist yet** (package is mid-build) — its family table will be authored when the README is created during the AI-TGE build, and registered as #27 at that point.

### Kiro-Setup Copies (Mirror of Core Files)

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 9 | `ai-packages/ai-pilc/kiro-setup/.kiro/steering/ai-pilc-rules/core-workflow.md` | ✅ | ✅ | ✅ |
| 10 | `ai-packages/ai-adlc/kiro-setup/.kiro/steering/ai-adlc-rules/core-workflow.md` | ✅ | ✅ | ✅ |

> **Note (2026-06-10, OI-022):** Only **AI-PILC** and **AI-ADLC** pre-stage a kiro-setup steering core mirror. The newer packages (**AI-DWG, AI-GCE, AI-TGE, AI-ILC**) ship `kiro-setup/INSTALL.md` only — no pre-staged `.kiro/steering/.../core-workflow.md` copy. The former #23 (`ai-ilc/.../kiro-setup/.../core-workflow.md`) was **de-registered** as it does not exist and AI-ILC follows the INSTALL-only convention.

### PLAN Files

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 11 | `ai-packages/ai-dwg/PLAN.md` | ✅ | ✅ | ✅ |
| 12 | `ai-packages/ai-gce/PLAN.md` | ✅ | ✅ | ✅ |
| 20 | `ai-packages/ai-ilc/PLAN.md` | ✅ | ✅ | ✅ |
| 25 | `ai-packages/ai-tge/PLAN.md` | ✅ (bespoke) | ❌ | ❌ |

### Structure & Builder Files

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 13 | `ai-packages/FAMILY_STRUCTURE.md` | ✅ | ✅ | ✅ |
| 14 | `ai-packagebuilder/README.md` | ✅ | ✅ | ✅ |
| 15 | `ai-packages/WHITEPAPER.md` | ✅ | ✅ | ✅ |

### Rule-Detail Process Overviews (Diagram Only)

| # | File Path | Contains Diagram | Contains Table | Contains Footnote |
|---|-----------|:----------------:|:--------------:|:-----------------:|
| 16 | `ai-packages/ai-dwg/ai-dwg-rule-details/common/process-overview.md` | ✅ | ❌ | ❌ |
| 17 | `ai-packages/ai-gce/ai-gce-rule-details/common/process-overview.md` | ✅ | ❌ | ❌ |
| 18 | `ai-packages/ai-adlc/ai-adlc-rule-details/common/process-overview.md` | ✅ | ✅ | ✅ |
| 19 | `ai-packages/ai-tge/ai-tge-rule-details/common/process-overview.md` | ✅ | ✅ | ✅ |
| 24 | `ai-packages/ai-ilc/ai-ilc-rule-details/common/process-overview.md` | ✅ | ✅ | ✅ |

---

## Total: 25 registry entries

**OI-018 reshape propagation (2026-06-10):**
- **20** full canonical-table files updated to the reshaped two-layer table (#1–15, #18, #19, #21, #22, #24).
- **2** diagram-only files updated (#16, #17).
- **22 content files total** now carry the reshaped canonical (verified: `grep "PORTFOLIO LAYER"`).

**AI-UXD canonical top-up (2026-06-10, Plan 1.5 / OI-028):**
- The canonical was later extended to add **AI-UXD** (new Project-layer row, `AI-UXD ───┤` diagram node + `AI-UXD ⇢ AI-POLC … AI-DLC ⇢ AI-UXD+AI-POLC (feedback)` line, AI-DWG input `AP + PBP` → `AP + PBP + UXP`, footnote ³ expanded).
- Re-propagated verbatim to the same **22 content files** (20 full-table + 2 diagram-only) — verified line-exact: AI-UXD diagram node = 1, Design UX line = 1, feedback line = 1 in every file; AI-UXD table row = 1 and zero bare `| AP + PBP |` in all 20 full-table files.
- **#26** (`ai-tge/ai-tge-rules/core-engine.md`) was authored already-current in Plan 1.4 — **excluded** from the top-up (not re-touched).
- AI-TGE's **bespoke** companion sub-diagram in #19 (`### AI-TGE Position (Companion Pattern)`) was left untouched (already UXD-correct from OI-019/Plan 1.3).
- **2** special-handling files (see table below): #20 (historical snapshot — pointer added), #25 (bespoke companion diagram — deferred to OI-019).
- **De-registered:** former #23 (AI-ILC kiro-setup mirror) — does not exist; AI-ILC ships INSTALL-only (OI-022).
- Old linear diagram intentionally retained in: `CONSISTENCY_ASSESSMENT.md` (excluded), `ai-ilc/PLAN.md` §4.1 (historical), `idea-management/ideas/002-idea-lifecycle.md` (archival idea record).

> **Note:** Files #20–24 are AI-ILC's. #20 (PLAN.md) exists (historical snapshot); #21/#22/#24 updated to the reshaped canonical; **#23 de-registered (2026-06-10, OI-022)** — AI-ILC ships INSTALL-only kiro-setup, no steering mirror (consistent with AI-DWG/AI-GCE/AI-TGE). AI-ILC was added to the canonical chain as an optional pre-stage on 2026-06-08 (idea 002, approved).
> **#25** (`ai-tge/PLAN.md`) added to the registry 2026-06-10; reclassified as bespoke companion diagram (no canonical table).

### Intentionally Excluded (not propagation targets)

| File | Reason |
|------|--------|
| `ai-packages/CONSISTENCY_ASSESSMENT.md` | Point-in-time assessment snapshot — documents a past chain state; rewriting its embedded diagram would falsify the historical record. Left as-is by decision (Plan Phase 1.1, 2026-06-10). |

### Special Handling (OI-018 propagation, 2026-06-10)

| File | # | Treatment |
|------|---|-----------|
| `ai-ilc/PLAN.md` | 20 | **Historical snapshot.** Its §4.1 table documents the AI-ILC *addition* proposal (linear canonical). Table NOT overwritten; a "SUPERSEDED" pointer to the reshaped canonical was added instead (same principle as the excluded assessment file). |
| `ai-ilc/.../kiro-setup/.../core-workflow.md` | ~~23~~ | **De-registered (OI-022, 2026-06-10).** Does not exist; AI-ILC ships INSTALL-only kiro-setup (no steering mirror), consistent with AI-DWG/AI-GCE/AI-TGE. Only AI-PILC (#9) and AI-ADLC (#10) pre-stage a mirror. |
| `ai-tge/PLAN.md` | 25 | **Bespoke companion diagram, not the canonical table.** Carries the "Family Position (Companion Pattern)" illustration showing AI-TGE alongside the chain. Redraw for the reshaped (two-layer) topology is deferred to **OI-019** (AI-GCE/AI-TGE repositioning), not OI-018. |
| `ai-tge/ai-tge-rule-details/common/process-overview.md` | 19 | Main canonical table updated (OI-018 ✅). It ALSO has a bespoke companion sub-diagram lower down → redraw deferred to **OI-019**. |

### Pending New Packages (registered in canonical, files not yet built)

The 2026-06-10 reshape added three packages to the canonical table. Their table-bearing
files do not exist yet and will be added to the numbered registry above **as each is built**:

| Package | Layer | Status | Idea Ref |
|---------|-------|--------|----------|
| **AI-PPM** | Portfolio | Pending build | idea 007 (registered) |
| **AI-FLO** | Edge (router) | Pending build | idea 008 (registered) |
| **AI-POLC** | Project | Pending build | idea 006 (Shaped) |
| **AI-UXD** | Project | Pending build | idea 010 (Approved) |

> **AI-UXD** was added to the canonical Project layer on 2026-06-10 (idea 010 approved) as a fourth pending package — separate from the reshape's original three. It runs parallel to AI-ADLC/AI-POLC, produces personas/journeys consumed by AI-POLC, feeds AI-DWG (design system → `frontend-standards.md` + new `design-system.md`) and AI-GCE (accessibility baseline → new `accessibility-compliance` rule), and receives AI-DLC feedback. Its table-bearing files will be added to the numbered registry as built.

> **AI-TGE** already has a registry entry (#19, process-overview) and is now reflected in the
> canonical Project layer. Its remaining table-bearing files follow the standard build flow.

---

## Update Procedure

When the canonical table changes:

1. Update the "Canonical Family Table (Copy From Here)" section in THIS file **first**
2. Propagate verbatim to all listed files that contain the **full table** (excluding diagram-only files)
3. Files #16-17 (diagram-only) need only the **chain diagram** portion updated
4. Verify table propagation with: `grep -rl "PORTFOLIO LAYER" ai-packages/` (should hit every full-table file once the reshape is propagated — see OI-018)
5. Verify layer/router propagation with: `grep -rl "AI-FLO" ai-packages/` and `grep -rl "AI-PPM" ai-packages/`

### ⚠️ Self-Exclusion Rule (Family Table Consistency Check)

`ai-packages/FAMILY_TABLE_MAP.md` is the **canonical SOURCE** of the family table — it is NOT a propagation target. The "Family Table Consistency Check" hook must **exclude this file**:

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

    AI-ADLC ──┐
    Design it │
    AI-UXD ───┤
    Design UX │
              ├──►  AI-DWG  ──►  AI-DLC (build) ¹
    AI-POLC ──┘     Prepare it       ▲
    Own it      └───────────────────┘  AI-POLC ⇄ AI-DLC (back-and-forth)
                AI-UXD ⇢ AI-POLC (personas/journeys)  ·  AI-DLC ⇢ AI-UXD+AI-POLC (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | (Requirements + Charter) / PIP | Architecture Package (AP) |
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP / AP; strategy-stage exchange with AI-POLC | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-POLC** ³ | Interactive workflow (lifecycle) | PIP and/or AP | Product Backlog Package (PBP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POLC) | Working Software |

> ¹ **AI-DLC** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ **AI-PPM**, **AI-FLO**, **AI-POLC**, and **AI-UXD** are **new and pending build**. AI-PPM (portfolio engine) and AI-FLO (router) are registered as ideas; AI-POLC (product ownership lifecycle) is idea 006; AI-UXD (UX design lifecycle) is idea 010 (approved). Within the Project layer, **AI-ADLC, AI-UXD, and AI-POLC run in parallel and all feed AI-DWG**; **AI-UXD produces personas/journeys that AI-POLC consumes** (and AI-POLC's value goals focus UX research); **AI-GCE and AI-TGE run alongside AI-DLC** as continuous quality engines; **AI-POLC ⇄ AI-DLC** exchange backlog/acceptance throughout delivery; and **AI-DLC runtime feedback flows back to both AI-UXD and AI-POLC**.

---

*Created: 2026-06-07 | Last Updated: 2026-06-10 (added AI-UXD to canonical Project layer — idea 010 approved; reshaped into Portfolio + Project layers; added AI-PPM, AI-FLO, AI-POLC, AI-TGE to canonical — see open items for propagation)*
