# AI-* Family — Consistency Assessment & Correction Plan

**Date:** 2026-06-07
**Author:** Kiro (AI-assisted)
**Status:** ~~DECISIONS APPROVED — Awaiting execution approval~~ **RESOLVED (2026-06-07)**

> ⚠️ **This assessment is now largely resolved.** The license inconsistency (Issue #2 — BSL 1.1 vs MIT-0 mismatch) has been fully corrected: all four packages now use Apache 2.0 with Attribution Addendum, matching the current strategy in `ai-license/LDR-002_License-Strategy-Change.md`. README license sections, PLAN files, and steering rules have all been updated. Remaining items (family table standardization, tagline fixes) may still be relevant — check individual files before acting on this document.

---

## Summary

Assessed all files across the workspace that describe "The AI-* Family." Found **9 categories of inconsistency** spanning naming, descriptions, license declarations, chain diagrams, and table content. A total of **~20 files** need corrections.

---

## Inconsistencies Found

### 1. 🔴 CRITICAL — Suite Name: "AIFLC" vs. "AI-* Family"

**Problem:** Two different names are used for the same suite:
- `ai-license/` folder consistently uses **"AIFLC (AI Full Life Cycle)"** — in README, LICENSE_BSL_1.1.md, LDR-002, LDR-003, OPEN_ITEMS, ENFORCEMENT_GUIDE, CLA, THE_STORY_LEGAL_ASSESSMENT
- `ai-packages/` and `ai-packagebuilder/` consistently use **"The AI-* Family"** — no mention of "AIFLC"
- Exception: PILC README and ADLC README say "AI-DLC is NOT part of **AIFLC**" — mixing the terms

**Impact:** External readers encounter two different brand names. Legal documents define "AIFLC"; technical documents don't use it. The note in PILC/ADLC READMEs references a term that appears nowhere else in the technical documents.

**Decision needed:** Which is canonical?
- Option A: "AIFLC" everywhere (formal brand/legal name)
- Option B: "AI-* Family" as technical name, "AIFLC" only in legal documents (dual naming — define relationship)
- Option C: One name everywhere — pick one

---

### 2. 🔴 CRITICAL — License Declaration Mismatch (DWG & GCE READMEs)

**Problem:** 
- AI-DWG README says: `├── LICENSE ← MIT-0` and `## License\nMIT-0 — See [LICENSE](./LICENSE)`
- AI-GCE README says: `├── LICENSE ← MIT-0`
- **BUT** their actual LICENSE files contain Apache 2.0 with Attribution Addendum text covering the entire AIFLC suite
- `ai-license/README.md` correctly states all four packages are Apache 2.0 with Attribution Addendum
- AI-PILC and AI-ADLC READMEs correctly state Apache 2.0 with Attribution Addendum

**Impact:** A user reading the DWG/GCE README is told MIT-0; the actual LICENSE file says Apache 2.0 with Attribution Addendum. This is a legal inconsistency that could cause real confusion or disputes.

**Correction:** ~~Update DWG and GCE READMEs to state BSL 1.1~~ ✅ **RESOLVED** — All READMEs now correctly state Apache 2.0 with Attribution Addendum, matching `ai-license/LDR-002_License-Strategy-Change.md`.

---

### 3. 🟠 HIGH — AI-GCE Type Description Varies

**Problem:** AI-GCE is described differently across files:

| File | AI-GCE Type Description |
|------|------------------------|
| FAMILY_STRUCTURE.md | "Adaptive governance engine" |
| AI-GCE README | "Adaptive governance engine" ← undefined in family table |
| AI-GCE PLAN.md | "Adaptive governance engine" |
| AI-GCE core-generator.md | "Adaptive generator (runtime)" |
| AI-PILC core-workflow.md | "Adaptive generator (runtime)" |
| AI-ADLC core-workflow.md | "Adaptive generator (runtime)" |
| AI-DWG core-generator.md | "Adaptive generator (runtime)" |
| AI-DWG PLAN.md | "Adaptive generator (runtime)" |
| ai-packagebuilder README | "Adaptive generator (runtime)" |
| AI-PILC README | "Adaptive governance engine" |
| AI-ADLC README | "Adaptive governance engine" |
| AI-DWG README | "Adaptive governance engine" |

**Split:** READMEs + FAMILY_STRUCTURE say "Adaptive governance engine"; core-workflow/generator files + packagebuilder README say "Adaptive generator (runtime)"

**Decision needed:** One canonical type. Recommend: **"Adaptive governance engine"** (matches the GCE's own README and FAMILY_STRUCTURE which is the declared source of truth).

---

### 4. 🟠 HIGH — AI-ADLC Input Column Varies

**Problem:**

| File | AI-ADLC Input |
|------|---------------|
| FAMILY_STRUCTURE.md | `(Requirements + Charter) / PIP` |
| AI-PILC core-workflow.md | `(Requirements + Charter) / PIP` |
| AI-ADLC core-workflow.md | `(Requirements + Charter) / PIP` |
| AI-DWG core-generator.md | `(Requirements + Charter) / (PIP)` ← parentheses around PIP |
| AI-GCE core-generator.md | `(Requirements + Charter) / (PIP)` |
| AI-PILC README | `(Requirements + Charter) / (PIP) Project Initiation Package` ← verbose |
| AI-ADLC README | `(Requirements + Charter) / PIP` |
| AI-DWG PLAN.md | `(Requirements + Charter) / PIP` |
| AI-GCE PLAN.md | `(Requirements + Charter) / PIP` |
| ai-packagebuilder README | `(Requirements + Charter) / PIP` |

**Correction:** Standardize to `(Requirements + Charter) / PIP` (per FAMILY_STRUCTURE.md source of truth).

---

### 5. 🟠 HIGH — AI-DWG Input Column Varies

**Problem:**

| File | AI-DWG Input |
|------|-------------|
| FAMILY_STRUCTURE.md | `AP` |
| AI-PILC core-workflow.md | `AP` |
| AI-ADLC core-workflow.md | `AP` |
| AI-DWG core-generator.md | `(AP) Architecture Package` ← expanded |
| AI-GCE core-generator.md | `(AP) Architecture Package` ← expanded |
| AI-PILC README | `(AP) Architecture Package` ← expanded |
| AI-ADLC README | `(AP) Architecture Package` ← expanded in ADLC README table |
| AI-DWG PLAN.md | `AP` |
| AI-GCE PLAN.md | `AP` |
| ai-packagebuilder README | `AP` |

**Correction:** Standardize to `AP` (per FAMILY_STRUCTURE.md source of truth). The acronym is already defined in the Output column of AI-ADLC row.

---

### 6. 🟠 HIGH — AI-GCE Input Column Varies

**Problem:**

| File | AI-GCE Input |
|------|-------------|
| FAMILY_STRUCTURE.md | `DW` |
| AI-PILC core-workflow.md | `DW` |
| AI-ADLC core-workflow.md | `DW` |
| AI-DWG core-generator.md | `DW (AI-DWG output)` ← expanded |
| AI-GCE core-generator.md | `DW (AI-DWG output)` ← expanded |
| AI-PILC README | `AI-DWG workspace output` ← completely different |
| AI-GCE PLAN.md | `DW` |
| AI-GCE README | `DW (AI-DWG output)` |
| ai-packagebuilder README | `DW` |

**Correction:** Standardize to `DW` (per FAMILY_STRUCTURE.md). Context is already clear from the chain.

---

### 7. 🟡 MEDIUM — AI-DWG Output Column Varies

**Problem:**

| File | AI-DWG Output |
|------|--------------|
| FAMILY_STRUCTURE.md | `Ready-to-code development workspace (DW)` |
| Most core files | `Ready-to-code development workspace (DW)` |
| AI-ADLC README | `Ready-to-code development workspace(DW)(including architecture-specific steering files)` ← verbose, no spaces |
| AI-PILC README | `Ready-to-code development workspace` ← missing (DW) abbreviation |

**Correction:** Standardize to `Ready-to-code development workspace (DW)`.

---

### 8. 🟡 MEDIUM — AI-DLC Input Column Varies

**Problem:**

| File | AI-DLC Input |
|------|-------------|
| Most files | `DW + GCE + User Stories` |
| AI-PILC README | `(Architecture / (AP) Architecture Package) + User Stories` ← completely wrong! Missing GCE |

**Correction:** Standardize to `DW + GCE + User Stories`.

---

### 9. 🟡 MEDIUM — Chain Diagram Tagline Variations

**Problem:** The "Guard it" tagline for AI-GCE varies:

| File | Tagline |
|------|---------|
| FAMILY_STRUCTURE.md | `Guard it (compliance + monitoring)` |
| Most core-workflow/generator files | `Guard it (compliance and monitor)` |
| AI-DWG README | `Guard it (compliance)` ← shortened |

**Correction:** Standardize to `Guard it (compliance + monitoring)` (per FAMILY_STRUCTURE.md).

---

### 10. 🟡 MEDIUM — FAMILY_STRUCTURE.md Omits AI-DLC Row

**Problem:** FAMILY_STRUCTURE.md (the declared source of truth) shows only 4 packages in both the diagram and table — no AI-DLC row or footnote. All other files include AI-DLC with a footnote explaining it's external.

**Correction:** Either:
- A) Add AI-DLC row + footnote to FAMILY_STRUCTURE.md (match all other files)
- B) Remove AI-DLC from the chain diagram in FAMILY_STRUCTURE.md (currently it shows 4 packages in the table but the diagram ASCII still says "→ AI-DLC (build)" implicitly via the chain)

Wait — actually reviewing again: FAMILY_STRUCTURE.md diagram does NOT include AI-DLC. It stops at AI-GCE. But all other files show `AI-PILC → AI-ADLC → AI-DWG → AI-GCE → AI-DLC (build)`.

**Decision needed:** Should FAMILY_STRUCTURE.md include AI-DLC in the diagram + table (with footnote), matching all other files?

---

## Correction Plan

### Phase 1: Decisions ~~Required~~ APPROVED

| # | Decision | Options | **Final Decision** |
|---|----------|---------|----------------|
| D1 | Suite name canonical form | A: "AIFLC" everywhere / B: Dual naming / C: Pick one | **B: Dual naming — "AIFLC" in legal docs, "AI-* Family" in technical docs** |
| D2 | AI-GCE type | "Adaptive governance engine" / "Adaptive generator (runtime)" | **"Adaptive governance engine"** |
| D3 | FAMILY_STRUCTURE.md AI-DLC row | Include with footnote / Exclude | **Include with footnote** |

### Canonical Family Table (from AI-GCE README — declared source of truth)

```
AI-PILC  →  AI-ADLC  →  AI-DWG  →  AI-GCE  →  AI-DLC (build)
  │              │            │          │           │
  │              │            │          │           └── Build it (code)
  │              │            │          └── Guard it (compliance + monitor)
  │              │            └── Prepare it (workspace + steering)
  │              └── Design it (architecture)
  └── Initiate it (project governance)
```

| Package | Type | Input | Output |
|---------|------|-------|--------|
| **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| **AI-ADLC** | Interactive workflow (lifecycle) | (Requirements + Charter) / PIP | Architecture Package (AP) |
| **AI-DWG** | One-time generator | AP | Ready-to-code development workspace (DW) |
| **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| **AI-DLC** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories | Working Software |

> ¹ **AI-DLC** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC consumes.

### Phase 2: Corrections (After Decisions Approved)

#### Step 1: Update FAMILY_STRUCTURE.md (Source of Truth)
- Add AI-DLC row + footnote to table (if D3 = Include)
- This becomes the canonical reference for all other corrections

#### Step 2: Fix License Declarations in DWG & GCE READMEs ✅ DONE
- AI-DWG README: Change `LICENSE ← MIT-0` to `LICENSE ← Apache 2.0 + Attribution` and rewrite License section
- AI-GCE README: Change `LICENSE ← MIT-0` to `LICENSE ← Apache 2.0 + Attribution` and add License section

#### Step 3: Standardize Family Table Across All Files

Files to update (table content only):

| File | Corrections Needed |
|------|-------------------|
| `ai-pilc/ai-pilc-rules/core-workflow.md` | AI-GCE type → "Adaptive governance engine" |
| `ai-adlc/ai-adlc-rules/core-workflow.md` | AI-GCE type → "Adaptive governance engine" |
| `ai-dwg/ai-dwg-rules/core-generator.md` | AI-GCE type, AI-ADLC input format, AI-DWG input format, AI-GCE input format |
| `ai-gce/ai-gce-rules/core-generator.md` | AI-GCE type, AI-ADLC input format, AI-GCE input format |
| `ai-pilc/README.md` | AI-ADLC input, AI-DWG input, AI-GCE input/type, AI-DLC input, DWG output |
| `ai-adlc/README.md` | AI-DWG input, DWG output |
| `ai-dwg/README.md` | License section |
| `ai-gce/README.md` | AI-GCE input, license section |
| `ai-gce/PLAN.md` | Already correct (matches FAMILY_STRUCTURE) |
| `ai-dwg/PLAN.md` | Already correct |
| `ai-packagebuilder/README.md` | AI-GCE type → "Adaptive governance engine" |
| `ai-dwg/ai-dwg-rule-details/common/process-overview.md` | Verify table matches |
| `ai-pilc/kiro-setup/.kiro/steering/ai-pilc-rules/core-workflow.md` | Mirror changes from main core-workflow |
| `ai-adlc/kiro-setup/.kiro/steering/ai-adlc-rules/core-workflow.md` | Mirror changes from main core-workflow |

#### Step 4: Standardize Chain Diagram Tagline
- Update all files to use `Guard it (compliance + monitoring)` per FAMILY_STRUCTURE.md

#### Step 5: Fix AIFLC/AI-* Family Name Bridge
- In PILC and ADLC READMEs, change the footnote from "is NOT part of AIFLC" to a form consistent with the decided naming convention (D1)
- If dual naming: keep "AIFLC" only in legal docs; use "AI-* Family" in technical footnote

#### Step 6: Verify
- Run a grep across all `.md` files for the family table row content
- Confirm all tables match FAMILY_STRUCTURE.md exactly

---

## Files Affected (Complete List)

| # | File | Changes |
|---|------|---------|
| 1 | `ai-packages/FAMILY_STRUCTURE.md` | Add AI-DLC row + footnote (if D3 approved) |
| 2 | `ai-packages/ai-pilc/README.md` | Fix table (4 cells), fix tagline, fix AIFLC reference |
| 3 | `ai-packages/ai-pilc/ai-pilc-rules/core-workflow.md` | Fix AI-GCE type |
| 4 | `ai-packages/ai-pilc/kiro-setup/.kiro/steering/ai-pilc-rules/core-workflow.md` | Mirror #3 |
| 5 | `ai-packages/ai-adlc/README.md` | Fix table (2 cells), fix tagline, fix AIFLC reference |
| 6 | `ai-packages/ai-adlc/ai-adlc-rules/core-workflow.md` | Fix AI-GCE type |
| 7 | `ai-packages/ai-adlc/kiro-setup/.kiro/steering/ai-adlc-rules/core-workflow.md` | Mirror #6 |
| 8 | `ai-packages/ai-dwg/README.md` | Fix tagline, fix license section (MIT-0 → Apache 2.0 + Attribution) ✅ |
| 9 | `ai-packages/ai-dwg/ai-dwg-rules/core-generator.md` | Fix table (3 cells), fix tagline |
| 10 | `ai-packages/ai-dwg/ai-dwg-rule-details/common/process-overview.md` | Fix tagline |
| 11 | `ai-packages/ai-dwg/PLAN.md` | Fix AI-GCE type (if it uses "runtime") |
| 12 | `ai-packages/ai-gce/README.md` | Fix AI-GCE input, fix license section (MIT-0 → Apache 2.0 + Attribution) ✅ |
| 13 | `ai-packages/ai-gce/ai-gce-rules/core-generator.md` | Fix table (3 cells) |
| 14 | `ai-packages/ai-gce/PLAN.md` | Already mostly correct — verify tagline |
| 15 | `ai-packagebuilder/README.md` | Fix AI-GCE type |
| 16 | `ai-license/README.md` | No changes needed (correct) |

---

## Execution Estimate

- **Effort:** ~30 minutes of automated edits + verification
- **Risk:** Low — text-only changes to markdown descriptions
- **Reversibility:** Full — git revert if anything is wrong

---

*Awaiting your approval and decisions on D1, D2, D3 before executing.*
