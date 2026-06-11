# AI-ILC — Build Plan

**Package:** AI-ILC — AI-Driven Idea Life Cycle
**Version (target):** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**Source idea:** `ai-packagebuilder/idea-management/ideas/002-idea-lifecycle.md` (Approved, score 30/35)
**Status:** 🟡 In progress — build started this session

> **Note on this file (Lesson 26):** This PLAN is the *design rationale + summary*. The detailed specification lives in `ai-ilc-rules/core-workflow.md` once built. Where this plan and the core file ever diverge, the core file wins.

---

## Summary Report (updated as the build progresses)

| Build Step | Artifact | Status |
|-----------|----------|:------:|
| 0 | PLAN.md (this file) | ✅ Done |
| 1 | Family-table propagation plan (below) + execution | ⏳ Pending approval |
| 2 | `ai-ilc-rules/core-workflow.md` (the heart) | ⏳ Blocked on Step 1 |
| 3 | Common files (5) | ⏳ |
| 4 | Stage detail files (6) | ⏳ |
| 5 | Templates (6) | ⏳ |
| 6 | README + LICENSE + kiro-setup/INSTALL.md | ⏳ |
| 7 | Additive AI-PILC intake edit | ⏳ |
| 8 | Dry Test + Fidelity + Chain Handoff | ⏳ |

---

## 1. Package Identity

| Field | Value |
|-------|-------|
| **Name** | AI-ILC |
| **Full Title** | AI-Driven Idea Life Cycle |
| **Type** | Interactive workflow (lifecycle) |
| **Input** | A raw idea (verbal / one-liner / document) |
| **Output** | Approved Idea Brief (→ AI-PILC) or Change Request Brief (→ AI-PILC change mgmt) or Feature Brief (→ AI-DLC backlog) + Go/No-Go Decision Record |
| **User Persona** | Innovation/Portfolio Manager (governs) + any employee (submits) |
| **Family Position** | **Optional pre-stage** before AI-PILC — the funnel before the funnel |
| **State File / Marker** | `ilc-state.md` |

---

## 2. Workflow Structure

**One phase — the Idea Life Cycle — with 6 stages (all ALWAYS execute, adaptive depth):**

| # | Stage | Produces | Lead Persona | Supporting |
|---|-------|----------|--------------|-----------|
| 1 | **Capture** | Idea entry (register row) | Product/Innovation Manager | — |
| 2 | **Shape** | Structured idea statement | Product/Innovation Manager | Process Designer |
| 3 | **Evaluate** | Score + Value Analysis | Product/Innovation Manager | Process Designer |
| 4 | **Scope** | Idea boundary + rough effort | Process Designer | Product/Innovation Manager |
| 5 | **Approve** | Go/No-Go Decision Record | Product/Innovation Manager | _idea's domain persona_ |
| 6 | **Route & Handoff** | Approved Idea Brief / Feature Brief | Product/Innovation Manager | _route's domain persona_ |

**Depth levels:** Minimal (small, clear idea) / Standard / Comprehensive (large, ambiguous, high-stakes idea).

---

## 3. Signature Design Decisions

### 3.1 Dynamic Stage-Based Personas
No single fixed persona. Each stage adopts its lead persona; a supporting persona is pulled from the idea's subject domain (architecture → CTO, governance → compliance, etc.), capped at two. Encoded workspace-wide in `.kiro/steering/persona-loading-guide.md` → "Dynamic / Stage-Based Selection."

### 3.2 Single-Project Context (v1.0)
AI-ILC operates against one project per workspace at a time. Feature routing targets *the* project present; no multi-project lookup.

### 3.3 Portfolio Connector (interface stub)
The only portfolio element in v1.0 — a defined seam where future multi-project portfolio management plugs in. No portfolio logic built now.

### 3.4 Impact-Driven Routing
When an idea is approved, routing is determined by project existence + impact size:
- No project exists → **AI-PILC** (new project initiation)
- Project exists + BIG change (impacts scope/criteria/architecture) → **AI-PILC change management**
- Project exists + SMALL change (no project-level impact) → **AI-DLC backlog** (new feature)

AI-ADLC is never a direct target from AI-ILC. If architecture needs rework, that flows *through* AI-PILC's change management process (which may then engage AI-ADLC).

### 3.5 Additive AI-PILC Contract (Lesson 6)
AI-PILC keeps all existing intake modes. "AI-ILC brief" (new project) and "AI-ILC change request" (big change) are added as optional modes. AI-ILC is never a prerequisite for AI-PILC.

### 3.6 Registers (Lesson 19)
AI-ILC owns two: **Idea Register** (portfolio funnel view) and **Decision Log** (go/no-go rationale, audit trail).

---

## 4. Family-Table Propagation Plan (Lesson 17) — DO FIRST

Adding AI-ILC to the family changes the canonical chain. Per workspace rule 10 and the `FAMILY_TABLE_MAP.md` update procedure, the canonical table must change **first**, then propagate to every registered file. This is a deliberate, planned step — not improvised mid-build.

### 4.1 Proposed Canonical Change

**Chain diagram (AI-ILC as optional front extension):**

```
(optional)
 AI-ILC  ⇢  AI-PILC  →  AI-ADLC  →  AI-DWG  →  AI-GCE  →  AI-DLC (build)
   │            │            │            │          │           │
   │            │            │            │          │           └── Build it (code)
   │            │            │            │          └── Guard it (compliance + monitor)
   │            │            │            └── Prepare it (workspace + steering)
   │            │            └── Design it (architecture)
   │            └── Initiate it (project governance)
   └── Decide it (idea → approved initiative)   [⇢ = optional pre-stage, not a mandatory link]
```

**Table (new AI-ILC row added at top):**

| Package | Type | Input | Output |
|---------|------|-------|--------|
| **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| **AI-ADLC** | Interactive workflow (lifecycle) | (Requirements + Charter) / PIP | Architecture Package (AP) |
| **AI-DWG** | One-time generator | AP | Ready-to-code development workspace (DW) |
| **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| **AI-DLC** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories | Working Software |

> ¹ **AI-DLC** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC consumes.
> ² **AI-ILC** is an **optional pre-stage**. The chain still starts at AI-PILC for users who don't use AI-ILC. AI-ILC's output optionally feeds AI-PILC (new project or change request) or routes a small feature directly to the AI-DLC backlog.

> ~~⚠️ **Above is a PROPOSAL pending your approval.**~~ ✅ APPROVED and canonical as of 2026-06-08.

> 📌 **SUPERSEDED (2026-06-10):** The table in §4.1 above is the AI-ILC-era *linear* canonical and is retained here as the historical record of the AI-ILC addition decision. The family was later reshaped into Portfolio + Project layers (adding AI-PPM, AI-FLO, AI-POLC, AI-TGE). For the current canonical, see `ai-packages/FAMILY_TABLE_MAP.md`. AI-ILC's live table-bearing files (README, core-workflow, process-overview) have been updated to the reshaped canonical (OI-018).

### 4.2 Propagation Sequence (after approval)
1. Update the "Canonical Family Table (Copy From Here)" section in `FAMILY_TABLE_MAP.md` **first**.
2. Propagate verbatim to all currently-registered files (READMEs, core files, kiro-setup mirrors, PLANs, FAMILY_STRUCTURE, WHITEPAPER, builder README, process-overviews).
3. Add AI-ILC's own table-bearing files to the map registry as they're built (README, core-workflow, this PLAN, process-overview).
4. Verify with a grep for the new AI-ILC row across all registered files.

### 4.3 Open Decision for User
- Confirm the exact wording of the AI-ILC row (Input = "Raw idea", Output = "Approved Idea Brief / Feature Brief") and footnote ².
- Confirm the `⇢` optional-link notation in the chain diagram, or propose an alternative visual.

---

## 5. Proposed File Structure

```
ai-ilc/
├── README.md
├── LICENSE
├── PLAN.md                         ← this file
├── ai-ilc-rules/
│   └── core-workflow.md            ← master orchestration (the heart)
├── ai-ilc-rule-details/
│   ├── common/
│   │   ├── process-overview.md
│   │   ├── session-continuity.md
│   │   ├── question-format-guide.md
│   │   ├── content-validation.md
│   │   └── welcome-message.md
│   ├── idea-lifecycle/             ← the single phase; 6 stage detail files
│   │   ├── capture.md
│   │   ├── shape.md
│   │   ├── evaluate.md
│   │   ├── scope.md
│   │   ├── approve.md
│   │   └── route-handoff.md
│   ├── connectors/
│   │   └── portfolio-connector.md  ← interface stub spec (single-project in v1.0)
│   └── templates/
│       ├── idea-register.md
│       ├── idea-entry.md
│       ├── decision-record.md
│       ├── approved-idea-brief.md
│       ├── change-request-brief.md
│       ├── feature-brief.md
│       └── ilc-state.md
└── kiro-setup/
    └── INSTALL.md
```

---

## 6. Risks & Mitigations (carried from idea file)

| Risk | Mitigation |
|------|-----------|
| Family-table change drifts across files | Execute §4 propagation deliberately; verify by grep |
| Overlap perception with AI-PILC | Hard boundary: ILC decides WHETHER; PILC initiates the approved one |
| Feature-path creep into brownfield/portfolio | v1.0 hard rule: single-project + Connector stub + portable brief |
| Productizing internal tool leaks specifics | Enforce generic `{placeholder}` syntax; no ITSM / builder names |

---

## 7. Build Considerations Carried from Conversion Checklist

1. **Two-source model (Lesson 25)** — ship a default evaluation rubric enterprises can override; silence still yields a working rubric. Handle in Evaluate-stage design.
2. **Conditional generation mapping (Lesson 7)** — document what AI-ILC always produces (idea register, decision log, state, go/no-go record) vs. conditionally (Project Brief vs. Feature Brief by route).

---

*Created: 2026-06-08 | Author: Maheri | Source: idea 002*
