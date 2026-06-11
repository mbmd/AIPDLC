---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Management Framework — Consolidated Spine Template (AI-DWG)

| Field | Value |
|-------|-------|
| **Package** | AI-DWG (AI-Driven Workspace Generator) |
| **Phase Code** | `DWG` |
| **Role** | Required producer — generates/appends the development-phase registers into the shared governance spine |
| **Registers Produced** | 4 (Decision, Change, Issue, Lessons) |
| **Contract Reference** | `ai-packages/MANAGEMENT_FRAMEWORK_CONTRACT.md` v1.1.0 |

---

## Purpose

This template defines how AI-DWG contributes to the **shared governance spine** — the consolidated `management_framework/` folder that tracks project decisions, changes, issues, and lessons across the AI-* Family chain.

AI-DWG is typically the **third required producer** in the chain (after AI-PILC and AI-ADLC). In chain mode, the spine already exists — AI-DWG **appends** its development-phase registers. In standalone mode (or when run first), it **creates** the spine from scratch.

---

## Registers AI-DWG Does NOT Produce

| Register | Why Not |
|----------|---------|
| Action Items | Development actions are tracked in project tickets / sprint backlogs, not in the governance spine |
| Assumptions & Dependencies | By the time AI-DWG runs, assumptions are resolved in the Architecture Package — they are decisions, not open assumptions |

AI-DWG writes to the **4 universal registers** only.

---

## Behavior: Append-if-Exists / Create-if-Absent

```
1. DETECT the spine by marker (Lesson 14):
   → Scan for management_framework/MANAGEMENT_FRAMEWORK.md
   → Detection path: user-provided path → ./management_framework/ → project root
     → predecessor output folder → ask user.

2. IF marker found (spine exists — typical in chain mode):
   → APPEND DWG-phase entries to the 4 registers.
   → Use ID prefix DWG-{TYPE}-{NNN}.
   → Add/update the DWG row in the index's "Contributing Phases" table.
   → DO NOT touch other phases' rows (additive, non-destructive).

3. IF marker NOT found (standalone — no predecessor has run):
   → CREATE management_framework/ at the configured location.
   → Generate the index file (MANAGEMENT_FRAMEWORK.md) using the standard template.
   → Generate the 4 registers from the schemas below.
   → This package operates exactly as standalone (Lesson 19 / Lesson 45).
```

**Mode 3 (Brownfield Overlay) note:** If a non-conforming `management_framework/` already exists (no marker, different schema), AI-DWG adds the marker + Phase column non-destructively. Existing entries are NOT renumbered — they are left in place and AI-DWG's new entries begin with `DWG-*` prefixes alongside them.

---

## Register Schemas (DWG Phase)

All schemas carry the **Phase** column per the contract. AI-DWG uses prefix `DWG-`.

### Decision_Log.md
```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Decision Log

| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| DWG-D-001 | DWG | {date} | {decision} | {context} | {rationale} | {maker} | {impact} | ✅ Final |
```

**When to log (DWG context):** Library choices, conditional steering-file inclusion/exclusion rationale, folder structure alternatives, mode selection (Mode 1/2/3), tech-stack-specific generation choices.

**NOT for:** Architecture decisions (those are ADRs in the AP) or project governance (those are in PILC's phase entries).

**Status values:** ✅ Final · ☐ Pending · 🔄 Under Review · ⏸️ Deferred · ❌ Reversed

---

### Change_Log.md
```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Change Log

| ID | Phase | Date Raised | Description | Raised By | Impact Assessment | Approval Status | Approved By | Date Approved | Implemented |
|----|-------|:-----------:|-------------|-----------|-------------------|:---------------:|-------------|:-------------:|:-----------:|
| DWG-C-001 | DWG | {date} | {description} | {role} | {steering-file/config impact} | ☐ Pending | _[TBD]_ | — | ☐ No |
```

**Status values:** ☐ Pending · 🔄 Under Assessment · ✅ Approved · ✅ Implemented · ❌ Rejected · ⏸️ Deferred

**Typical DWG changes:** Reconciliation decisions (accept/reject proposed steering updates), steering files added/removed post-generation, config merge overrides, depth-level adjustments.

---

### Issue_Log.md
```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Issue Log

| ID | Phase | Date Raised | Issue | Severity | Area | Owner | Status | Resolution | Resolved |
|----|-------|:-----------:|-------|:--------:|------|:-----:|:------:|-----------|:--------:|
| DWG-I-001 | DWG | {date} | {issue} | {H/M/L} | {area} | {owner} | ☐ Open | — | — |
```

**Status values:** ☐ Open · 🔄 Investigating · ✅ Resolved · ⏸️ On Hold · ❌ Escalated

**Typical DWG issues:** AP artifact missing (generation blocked), conflicting AP information, unknown technology (generic fallback needed), reconciliation conflict (AP-derived vs. team-customized content).

---

### Lessons_Learned.md
```markdown
<!-- AI-DWG generated | source: Project governance | date: {generation-date} -->
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Lessons Learned

| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| DWG-L-001 | DWG | {date} | {lesson} | {what happened} | {corrective action} | {Process/Technology/DX/Governance} |
```

**Category note:** AI-DWG adds "DX" (Developer Experience) as a category — this captures lessons about workspace ergonomics (e.g., "Generated 30 steering files but team only reads 5 — depth was too high for team size").

---

## Generation Rules

1. **ALWAYS generated** — every development workspace gets these registers (either in a new spine or appended to the existing one).
2. Registers start with headers + one example row (populated during development).
3. Entries are append-only — never delete logged items.
4. Each entry is sequentially numbered within the DWG phase (`DWG-D-001`, `DWG-D-002`, ...).
5. AI-DLC sessions should log decisions and lessons as they arise (using their own phase code if/when AI-DLC contributes to the spine).
6. Sprint retros feed into `Lessons_Learned.md`.

---

## When AI-DWG Records (Mapping to Generation Steps)

| DWG Step | Registers Typically Touched | Example Entry |
|:--------:|---------------------------|---------------|
| Mode Detection | Decisions | `DWG-D-001: Mode 1 selected (greenfield — no existing workspace)` |
| Configuration Questions | Decisions | `DWG-D-002: Autonomy mode = Autopilot` |
| AP Reading | Issues | `DWG-I-001: Multi-tenancy doc missing — single-tenant assumed` |
| Conditional Triggers | Decisions | `DWG-D-003: resilience-standards.md generated (>3 integrations)` |
| Validation | Issues | `DWG-I-002: AP principle P4 not encoded in any steering file` |
| Reconciliation (Mode 2) | Changes, Decisions | `DWG-C-001: api-standards.md updated — new versioning strategy from ADR-012` |
| Brownfield (Mode 3) | Decisions, Lessons | `DWG-L-001: Existing .gitignore had 200+ entries — merge took manual review` |

---

## Relationship to Other Packages (Shared Spine Model)

| Package | Phase Code | Registers | Primary Governance Mechanism |
|---------|:----------:|:---------:|------------------------------|
| AI-ILC | `ILC` | Decision, Lessons | Spine (idea-stage decisions) |
| AI-PILC | `PILC` | All 6 | Spine (full PMO governance) |
| AI-ADLC | `ADLC` | Decision, Change, Issue, Lessons | Spine + ADRs (architecture artifacts) |
| **AI-DWG** | **`DWG`** | **Decision, Change, Issue, Lessons** | **Spine (development-phase governance)** |
| AI-POLC | `POLC` | _TBD at build_ | Spine (product-ownership governance) |
| AI-GCE | `GCE` | Decision, Lessons | Spine (compliance decisions) + `.governance/compliance-log/` |
| AI-TGE | `TGE` | Decision, Lessons | Spine (test-governance decisions) + `.tge/` |

> All packages append to ONE consolidated spine per project (Lesson 45). Each package's primary operational record (ADRs, compliance-log, .tge/) stays alongside.

---

## Standalone vs. Chain Behavior (Summary)

| Mode | What Happens |
|------|-------------|
| **Standalone** (no predecessor has run) | AI-DWG creates the spine from scratch with 4 registers + index. Self-contained. |
| **Chain** (spine exists from AI-PILC/AI-ADLC) | AI-DWG appends `DWG-*` entries. One consolidated record. |
| **Brownfield** (existing non-conforming `management_framework/`) | Add marker + Phase columns non-destructively; do not renumber existing entries. |

---

## Contributing Phases Row (for the Index)

When AI-DWG appends to an existing spine, it adds this row to `MANAGEMENT_FRAMEWORK.md`:

```markdown
| DWG | AI-DWG | {date} | Decision, Change, Issue, Lessons |
```

---

*Template Version: 1.0.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.1.0 | Package: AI-DWG | Phase code: DWG*
