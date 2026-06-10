# Management Framework — Shared Cross-Package Contract

**Version:** 1.0.0
**Date:** 2026-06-10
**Author:** Maheri
**Authored under:** `#persona-process-designer` (lead) + `#persona-compliance-governance` (support)
**Status:** DIRECTION APPROVED (2026-06-10, Plan Phase 0.3) — execution deferred to Plan Phase 2.1

> **Approval record (2026-06-10):** Shared-spine direction approved (Q1); Lesson 19 override via corrective Lesson 34 approved (Q2); phase-code set expanded to match the reshaped family (Q3 — see §5); default location = project root `management_framework/` with user override (Q4). Building of Lesson 34 + templates happens in Plan Phase 2.1, not yet.

---

## 1. Purpose

The `management_framework/` is the project's **governance spine** — the auditable trail of decisions, changes, issues, and lessons captured as a project moves through the AI-* Family chain.

Historically each package produced its own `management_framework/` under its own output folder (AI-PILC under `{pilc-output}/`, AI-ADLC under `{adlc-output}/management_framework/`, AI-DWG under `{project-root}/management_framework/`). That fragments the record: a single `Decision_Log` ends up in three places, and answering "what was decided on this project?" means reading three folders.

This contract defines a **single consolidated governance spine per project** that every chain package *contributes to* — without coupling the packages or breaking standalone use.

> **This is a shared CONTRACT, not a new package.** No package "owns" or "manages" the others. The spine is a shared artifact each package appends to. Cross-project / portfolio governance (managing *many* projects, or governing the package set) is out of scope here — that is AI-PPM (portfolio) and AI-GCE (runtime compliance) territory.

---

## 2. Relationship to Lesson 19 (Important)

Lesson 19 ("Each Package Owns Its Own Governance Registers") states: *no shared/global management framework — each phase owns its tracking.* This contract **deliberately evolves that position**, the way Lesson 20 corrected Lesson 18.

Lesson 19's rationale was sound; this contract preserves its *intent* by other means:

| Lesson 19 concern | How this contract honors it |
|---|---|
| **Clean ownership** (PM decisions don't mix with dev decisions) | Every entry carries a mandatory **Phase** column and a **phase-prefixed ID** (`PILC-D-001`, `ADLC-C-002`, `DWG-I-003`). Ownership is encoded in the row itself, not the folder. |
| **Audit trail per phase** | The Phase column makes the log filterable per phase; chronological-across-phases is now *also* possible (a strict improvement). |
| **Self-contained output** | In **standalone mode**, each package still produces its own self-contained spine. Consolidation only happens in **chain mode**, when a spine already exists. |
| **Know which phase by looking** | The phase-prefixed ID answers this at the row level — stronger than "by which folder it's in." |

**Required follow-up:** LESSONS.md must record a corrective lesson (proposed "Lesson 34") noting that Lesson 19 is superseded in chain mode by this contract. Do not silently leave Lesson 19 contradicting a live contract.

---

## 3. Detection by Marker (Lesson 14)

The spine is detected by **marker**, never by hardcoded path. The user chooses WHERE the spine lives; this contract defines WHAT must exist there.

| Element | Value |
|---|---|
| **Folder** | `management_framework/` (user may place at project root or a chosen governance folder) |
| **Marker file** | `MANAGEMENT_FRAMEWORK.md` (the spine index/README — its presence means "a consolidated spine already exists here") |
| **Detection strategy** | User provides path → scan common locations (`./management_framework/`, project root, predecessor output folder) → ask user |

**Marker registry addition** (to sit alongside the package markers in LESSONS.md Lesson 14):

```
Shared management framework marker: management_framework/MANAGEMENT_FRAMEWORK.md
```

---

## 4. Contribution Behavior — Append-if-Exists, Create-if-Absent

Every chain package follows the same rule when it reaches a stage that records governance:

```
1. Detect the spine (by marker — Section 3).
2. IF a spine exists (MANAGEMENT_FRAMEWORK.md found):
      → APPEND this phase's entries to the existing registers.
      → Use this phase's ID prefix so IDs never collide.
      → Register the phase in the index's "Contributing Phases" table.
3. IF no spine exists:
      → CREATE management_framework/ with the marker + this phase's registers.
      → The package operates exactly as it did standalone.
```

This keeps every package **independently runnable** (Lesson 6, graceful standalone) while producing one consolidated record whenever the chain is run end to end.

**Append is additive and non-destructive.** A package NEVER edits or deletes another phase's rows. It only adds its own.

---

## 5. Register Set

The consolidated spine carries up to six registers. Four are **universal** (every phase may write to them); two are **PILC-origin** (initiation governance) but remain available to any phase.

| Register | File | Universal? | ID type |
|---|---|:---:|---|
| Decision Log | `Decision_Log.md` | ✅ Universal | `{PHASE}-D-{NNN}` |
| Change Log | `Change_Log.md` | ✅ Universal | `{PHASE}-C-{NNN}` |
| Issue Log | `Issue_Log.md` | ✅ Universal | `{PHASE}-I-{NNN}` |
| Lessons Learned | `Lessons_Learned.md` | ✅ Universal | `{PHASE}-L-{NNN}` |
| Action Items | `Action_Items.md` | PILC-origin | `{PHASE}-A-{NNN}` |
| Assumptions & Dependencies | `Assumptions_Dependencies.md` | PILC-origin | `{PHASE}-AD-{NNN}` |

**Phase codes (approved 2026-06-10, Plan Phase 0.3 — reshaped-family set):**

The spine is **per-project**, so its contributors are the **Project-layer** governance producers:

| Phase code | Package | Contribution |
|------------|---------|--------------|
| `PILC` | AI-PILC | **Required** producer |
| `ADLC` | AI-ADLC | **Required** producer |
| `POG` | AI-POG | **Required** producer (new build) |
| `DWG` | AI-DWG | **Required** producer |
| `GCE` | AI-GCE | **Optional** — may log governance decisions (e.g. "baseline this violation"); primary record stays its own compliance log |
| `TGE` | AI-TGE | **Optional** — may log test-governance decisions |

**Excluded from the per-project spine:**
- `PPM` (AI-PPM) — portfolio-scope (governs *many* projects); has its own portfolio register.
- `FLO` (AI-FLO) — routing infrastructure; records no per-project governance.
- `ILC` (AI-ILC) — pre-project idea stage; its decisions predate the project and roll into PILC.

A package only creates the register files it actually writes to. The four universal registers exist in any spine; the two PILC-origin registers exist only if a phase that uses them has run.

---

## 6. Register Schemas

Every register adds a **Phase** column to the existing per-package schema. Columns are otherwise unchanged from the current templates, so existing package output stays compatible.

### Decision_Log.md
```markdown
| ID | Phase | Date | Decision | Context | Options Considered | Chosen | Rationale | Made By |
|----|-------|------|----------|---------|--------------------|--------|-----------|---------|
| PILC-D-001 | PILC | | | | | | | |
```

### Change_Log.md
```markdown
| ID | Phase | Date | Change | Reason | Impact | Approved By |
|----|-------|------|--------|--------|--------|-------------|
| ADLC-C-001 | ADLC | | | | | |
```

### Issue_Log.md
```markdown
| ID | Phase | Date | Issue | Severity | Area | Status | Resolution | Resolved |
|----|-------|------|-------|:--------:|------|:------:|-----------|----------|
| DWG-I-001 | DWG | | | H/M/L | | Open/Closed | | |
```

### Lessons_Learned.md
```markdown
| ID | Phase | Date | Lesson | Context | Action Taken |
|----|-------|------|--------|---------|--------------|
| PILC-L-001 | PILC | | | | |
```

### Action_Items.md
```markdown
| ID | Phase | Date | Action | Owner | Due | Status |
|----|-------|------|--------|-------|-----|--------|
| PILC-A-001 | PILC | | | | | Open/Done |
```

### Assumptions_Dependencies.md
```markdown
| ID | Phase | Date | Assumption / Dependency | Type | Impact if Invalid | Status |
|----|-------|------|-------------------------|------|-------------------|--------|
| PILC-AD-001 | PILC | | | A/D | | Open/Validated |
```

---

## 7. The Index File (Marker)

`MANAGEMENT_FRAMEWORK.md` is both the marker and the human entry point to the spine.

```markdown
<!-- Shared governance spine | contract v1.0.0 -->

# Management Framework

Consolidated governance spine for this project. Each phase of the AI-* chain
appends its decisions, changes, issues, and lessons here, tagged by phase.

## Registers
| Register | Purpose |
|----------|---------|
| Decision_Log.md | Decisions below formal-artifact threshold |
| Change_Log.md | Scope / approach / timeline changes |
| Issue_Log.md | Blockers and problems |
| Lessons_Learned.md | Insights to carry forward |
| Action_Items.md | Tracked follow-ups (if used) |
| Assumptions_Dependencies.md | Assumptions & dependencies (if used) |

## Contributing Phases
| Phase | Package | First Contributed | Registers Touched |
|-------|---------|-------------------|-------------------|
| PILC | AI-PILC | {date} | Decision, Change, Issue, Action, Assumptions, Lessons |

## Conventions
- Entry IDs are phase-prefixed: `{PHASE}-{TYPE}-{NNN}`.
- Entries are append-only — never edit or delete another phase's rows.
- Filter by the Phase column to view a single phase's governance.
```

When a package appends, it also adds its row to **Contributing Phases**.

---

## 8. Standalone vs. Chain Behavior

| Mode | Behavior |
|------|----------|
| **Standalone** (package run alone) | No spine exists → package creates `management_framework/` with its own registers, exactly as today. Self-contained (honors Lesson 19 intent). |
| **Chain** (predecessor already produced a spine) | Spine exists → package appends its phase entries to the shared registers and registers itself in the index. One consolidated record. |
| **Brownfield** (Lesson 23) | If a non-conforming `management_framework/` already exists, treat it as standalone-with-baseline: add the marker + Phase columns non-destructively, do not renumber existing human entries. |

---

## 9. Boundaries (What This Contract Does NOT Do)

1. **Not a package.** Nothing here manages or orchestrates other packages. It is a shared artifact contract only.
2. **Does not replace ADRs or the Architecture_Workbook.** AI-ADLC still records architecture decisions as ADRs; the Decision_Log captures only sub-threshold decisions (unchanged).
3. **Does not enforce compliance.** Runtime governance hooks/rules remain AI-GCE's responsibility.
4. **Not portfolio governance.** Managing many projects is AI-PPM (idea 007).
5. **Does not hardcode location.** WHERE the spine lives is always the user's choice (Lesson 14).

---

## 10. Impact — Files To Change When This Is Adopted

| File | Change |
|------|--------|
| `ai-pilc/.../templates/management-framework.md` | NEW — consolidated template referencing the shared contract + Phase column |
| `ai-adlc/.../templates/management-framework.md` | NEW — 4 registers with Phase column + shared-contract behavior |
| `ai-dwg/.../templates/operational/management-framework.md` | UPDATE — add Phase column, append-if-exists behavior, marker awareness |
| `ai-pog/.../templates/management-framework.md` | NEW (at AI-POG build, Phase 4) — POG-phase registers + shared-contract behavior |
| `ai-gce/.../templates/...` | UPDATE (optional contributor) — Phase-column awareness for governance decisions logged to the spine |
| `ai-tge/.../templates/...` | UPDATE (optional contributor) — Phase-column awareness for test-governance decisions |
| `ai-pilc/.../core-workflow.md` | UPDATE — Stage 6 references shared spine + detection |
| `ai-adlc/.../core-workflow.md` | UPDATE — output table references shared spine |
| `ai-dwg/.../core-generator.md` | UPDATE — generation references shared spine + append behavior |
| `FAMILY_STRUCTURE.md` | UPDATE — show consolidated spine in runtime output |
| Each package `CONCEPTUAL_MAP.md` | UPDATE — Concern → Location map points to shared spine |
| `ai-packagebuilder/LESSONS.md` | UPDATE — add corrective Lesson 34 (supersedes Lesson 19 in chain mode) |

> **Scope note (Plan Phase 0.3, 2026-06-10):** The original §10 list covered only PILC/ADLC/DWG. The approved reshaped-family phase set (§5) expands execution to AI-POG (new build, Phase 4) and optional Phase-column awareness in AI-GCE/AI-TGE. AI-POG's template is created during its build, not during the initial Phase 2.1 spine rollout.

---

*Contract Version: 1.0.0 | Created: 2026-06-10 | Authored under #persona-process-designer + #persona-compliance-governance*
