---
generatedBy: AI-POLC
generatedVersion: 1.0.0
source: "management-framework-contract"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Management Framework — Governance Spine

**Scope:** Per-project governance trail
**Contributing Phase:** AI-POLC (Product Ownership Life Cycle)
**Phase Code:** POLC
**ID Formats:** POLC-D-NNN (Decision), POLC-C-NNN (Change), POLC-I-NNN (Issue), POLC-L-NNN (Lesson)

---

## Contributing Phases

| Phase Code | Package | Status |
|:---:|---|:---:|
| POLC | AI-POLC (Product Ownership) | Active |

---

## Registers

AI-POLC contributes to four universal registers:

### Decision Log (`Decision_Log.md`)

Records significant product decisions.

| ID | Date | Phase | Decision | Rationale | Status |
|---|---|:---:|---|---|:---:|
| POLC-D-001 | {date} | POLC | {Decision description} | {Why} | Open |

**When to log:** Priority model selection, scope acceptance/rejection, MVP boundary, DoR/DoD establishment, stakeholder escalation outcomes.

### Change Log (`Change_Log.md`)

Records changes to product governance or backlog structure.

| ID | Date | Phase | Change | Trigger | Impact | Status |
|---|---|:---:|---|---|---|:---:|
| POLC-C-001 | {date} | POLC | {What changed} | {Why} | {Affected items} | Open |

**When to log:** Reprioritization, DoR/DoD updates, release plan changes, epic scope changes, roadmap pivots.

### Issue Log (`Issue_Log.md`)

Records blockers and product-level issues.

| ID | Date | Phase | Issue | Severity | Owner | Status |
|---|---|:---:|---|:---:|---|:---:|
| POLC-I-001 | {date} | POLC | {Issue description} | {H/M/L} | {Role} | Open |

**When to log:** DLC blockers, stakeholder conflicts, dependency issues, assumption invalidation.

### Lessons Learned (`Lessons_Learned.md`)

Records product ownership insights.

| ID | Date | Phase | Lesson | Category | Action |
|---|---|:---:|---|---|---|
| POLC-L-001 | {date} | POLC | {What was learned} | {Category} | {Follow-up} |

**When to log:** Prioritization model effectiveness, estimation accuracy, stakeholder management insights, DoR/DoD calibration.

---

## Behavior Rules

- **Append-if-exists:** If `management_framework/MANAGEMENT_FRAMEWORK.md` already exists, append POLC-* entries to existing registers
- **Create-if-absent:** If no spine exists, create `management_framework/` with marker + registers
- **Non-destructive:** NEVER edit or delete another phase's entries
- **Namespace collision-free:** POLC-* prefix prevents ID conflicts with PILC-*, ADLC-*, etc.

---

*Template for AI-POLC governance spine contribution | Per MANAGEMENT_FRAMEWORK_CONTRACT.md*
