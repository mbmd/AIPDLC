# AI-POLC — Build Plan

**Package:** AI-POLC (AI-Driven Product Ownership Life Cycle)
**Version:** 1.0.0
**Date:** 2026-06-11
**Author:** Maheri
**Status:** APPROVED — proceeding to build

---

## 1. Package Identity

| Field | Value |
|-------|-------|
| **Name** | AI-POLC |
| **Full Title** | AI-Driven Product Ownership Life Cycle |
| **Package Type** | Interactive workflow (lifecycle) |
| **Primary Input** | PIP (from AI-PILC) and/or AP (from AI-ADLC) — standalone: product brief / vision statement |
| **Primary Output** | Product Backlog Package (PBP) |
| **User Persona** | Product Owner (primary); Product Manager, Business Analyst, Delivery Lead, solo founder |
| **Family Position** | Project layer — parallel to AI-ADLC and AI-UXD; feeds AI-DWG; bidirectional exchange with AI-DLC |
| **Marker File** | `polc-state.md` |
| **Governance Spine Prefix** | `POLC-` |

### Name Challenge (Lesson 12)

| Candidate | Pros | Cons | Verdict |
|-----------|------|------|---------|
| **AI-POLC** (Product Ownership Life Cycle) | Emphasizes the *role* (PO) and its lifecycle; parallel to AI-PILC; pronounceable ("polk") | Could be confused with "policy" at first glance | ✅ Selected |
| AI-PBLC (Product Backlog Life Cycle) | Emphasizes the *artifact* (backlog) | Reduces the PO to just the backlog; misses strategy, stakeholders, metrics | ❌ Too narrow |
| AI-PVLC (Product Value Life Cycle) | Emphasizes *value* | Abstract; unclear what it does | ❌ Too vague |

**Decision:** AI-POLC. It names the accountability (product ownership) not just the artifact (backlog).

---

## 2. Phase/Stage Structure

6 phases, 16 stages. Phases 1-5 are the initial pass (setup → assembly). Phase 6 is continuous operations (repeating).

| # | Stage | Phase | Primary Output | Core/Ext |
|---|-------|-------|---------------|----------|
| 1 | Workspace Detection & Intake | Foundation | Context established, upstream changes detected | Core |
| 2 | Product Vision & Goals | Foundation | Vision statement, OKRs/KPIs, success metrics | Core |
| 3 | PO Charter & Authority | Foundation | PO role charter, RACI, decision boundaries | Core |
| 4 | Product Discovery & Roadmap | Strategy | Roadmap (Now/Next/Later), value proposition | Core + Ext |
| 5 | Epic Decomposition | Strategy | Goal→Epic mapping, epic definitions + AC | Core |
| 6 | Value-Based Prioritization | Strategy | Ranked backlog with model + rationale | Core |
| 7 | Release & Increment Slicing | Strategy | Release plan, MVP/MMP scope definition | Core |
| 8 | Definition of Ready / Done | Governance | DoR/DoD checklists, governance rules | Core |
| 9 | Product Risk & Assumptions | Governance | Product risk register, assumption log | Core + Ext |
| 10 | Traceability Spine | Governance | Intent→Epic traceability matrix | Core + Ext |
| 11 | Stakeholder Management | Stakeholders | Stakeholder map, communication cadence | Core |
| 12 | Product Documentation | Stakeholders | Release notes governance, changelog | Core + Ext |
| 13 | PBP Assembly & Handoff | Assembly | Assembled PBP, polc-state.md finalized | Core |
| 14 | Backlog Operations | Operations | Refinement cadence, splitting criteria | Core |
| 15 | Acceptance & Feedback Loop | Operations | Increment acceptance, DLC feedback | Core |
| 16 | Value & Metrics Engine | Operations | Product KPIs, benefits realization | Extension |

---

## 3. Tier Architecture

| Tier | Activation | Contents |
|------|-----------|----------|
| **Tier 1** (always active) | All modes | Stages 1–15 (full PO governance + operations) |
| **Tier 2** (user-activated) | Default OFF in chain mode | Story elaboration (INVEST + Given/When/Then AC) |

### Operations Phase Behavior (Decision: mode-dependent)

| Mode | Stages 14-16 behavior |
|------|----------------------|
| **Standalone (no AI-DLC)** | Repeating cycle — POLC drives the full product cadence |
| **Chain with AI-DLC** | Re-entry points — user opens POLC sessions as needed |

---

## 4. File Structure

See `FAMILY_STRUCTURE.md` for the full tree once built. Summary:

- `ai-polc-rules/core-workflow.md` — master orchestration
- `ai-polc-rule-details/common/` — 5 cross-cutting files
- `ai-polc-rule-details/foundation/` — 3 stage detail files
- `ai-polc-rule-details/strategy/` — 4 stage detail files
- `ai-polc-rule-details/governance/` — 3 stage detail files
- `ai-polc-rule-details/stakeholders/` — 2 stage detail files
- `ai-polc-rule-details/assembly/` — 1 stage detail file
- `ai-polc-rule-details/operations/` — 3 stage detail files
- `ai-polc-rule-details/tier2/` — 1 file (story elaboration)
- `ai-polc-rule-details/extensions/` — 14 files (7 pairs)
- `ai-polc-rule-details/templates/` — 17 templates
- `README.md`, `LICENSE`, `kiro-setup/INSTALL.md`

**Total:** ~56 files

---

## 5. Key Design Decisions

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| 1 | Package type | Lifecycle | Repeating cycle — passes Lesson 1 test |
| 2 | Tier model | Two tiers (Lesson 35) | Tier 1 = full PO; Tier 2 = DLC overlap toggle |
| 3 | Concurrency | Session separation | Files are the communication channel |
| 4 | DLC integration | Workspace-mediated | We don't control DLC; rules reach it via DWG steering |
| 5 | Upstream intake | File-based scan at session start | Detect ILC, PILC, UXD, DLC changes automatically |
| 6 | Context factors | 13 factors | Detected from state files or user questions |
| 7 | Governance spine | Append-if-exists (Lesson 45) | POLC-* prefixed entries |
| 8 | MVP/MMP | In Stage 7 (Release Slicing) | Natural home for scope-gating |
| 9 | Personas | Consumer from AI-UXD, not producer | Lesson 38 — producer→consumer |
| 10 | Operations loop | Mode-dependent | Standalone = repeating cycle; chain = re-entry |

---

## 6. Chain Contracts (Lesson 13)

### I Read

| Source | What | Detection |
|--------|------|-----------|
| AI-PILC | PIP | `pilc-state.md` marker |
| AI-ADLC | AP | `adlc-state.md` marker |
| AI-UXD | UXP (personas, journeys) | `uxd-state.md` marker |
| AI-ILC | Feature Brief (routed features) | `ilc-state.md` Route=feature |
| AI-DLC | Execution feedback | `aidlc-docs/` changes |
| Governance spine | Existing entries | `management_framework/MANAGEMENT_FRAMEWORK.md` |

### I Produce

| Artifact | Always/Conditional | Consumer |
|----------|:-:|-----------|
| `polc-state.md` (marker) | Always | AI-DWG, AI-DLC, user |
| Product Vision & Goals | Always | AI-DWG, user |
| PO Charter & Authority | Always | User, AI-GCE |
| Prioritized Epic Backlog | Always | AI-DLC, AI-DWG |
| DoR / DoD | Always | AI-DWG, AI-GCE |
| Release Plan | Always | AI-DWG |
| Traceability Matrix | Always (minimal) / Ext (full) | AI-GCE, audit |
| Stakeholder Map | Always | User |
| Product Risk Register | Always (light) / Ext (full) | User, AI-GCE |
| `management_framework/` contributions | Always | All spine consumers |
| PBP README | Always | User, downstream |

---

## 7. Design References

- **Feature Analysis:** `ai-packagebuilder/sessions-open-items/AI-POLC_FEATURE_ANALYSIS.md`
- **Idea Record:** `ai-packagebuilder/idea-management/ideas/006-product-owner-governance.md`
- **Critical Design Constraint:** AI-DLC is NOT our product — workspace-mediated integration only
- **Concurrent Operation Design:** Session separation (Option A) for v1.0

---

*Approved: 2026-06-11 | Proceeding to Step 4 (core-workflow.md)*
