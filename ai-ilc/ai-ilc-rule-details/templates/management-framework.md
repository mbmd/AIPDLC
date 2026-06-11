# Management Framework — Consolidated Spine Template (AI-ILC)

| Field | Value |
|-------|-------|
| **Package** | AI-ILC (Idea Life Cycle) |
| **Phase Code** | `ILC` |
| **Role** | Contributor — idea-stage decisions seed the governance spine at the earliest point |
| **Registers Produced** | 2 (Decision, Lessons) |
| **Contract Reference** | `ai-packages/MANAGEMENT_FRAMEWORK_CONTRACT.md` v1.1.0 |

---

## Purpose

This template defines how AI-ILC contributes to the **shared governance spine**. AI-ILC is the optional pre-stage package — it runs before AI-PILC to evaluate and approve ideas. Its governance contribution is lightweight: logging the **idea-gate decisions** (approve/park/reject) and any **lessons** from the evaluation process.

AI-ILC may be the **very first** package to run on a project, so in some chains it will **create** the spine. In others (rare — e.g., user manually seeds a spine first), it **appends**.

---

## Registers AI-ILC Produces

| Register | What ILC Logs | Example |
|----------|---------------|---------|
| Decision Log | Idea-gate decisions (approve, park, reject, merge, scope) | `ILC-D-001: Idea 010 APPROVED as standalone package AI-UXD` |
| Lessons Learned | Evaluation process insights | `ILC-L-001: Feedback-coupling analysis was the tiebreaker — add to standard evaluation` |

AI-ILC does NOT produce Change Log, Issue Log, Action Items, or Assumptions — those are project-execution concerns, not idea-stage concerns.

---

## Behavior: Append-if-Exists / Create-if-Absent

```
1. DETECT the spine by marker (Lesson 14):
   → Scan for management_framework/MANAGEMENT_FRAMEWORK.md
   → Detection path: user-provided path → ./management_framework/ → project root → ask user.

2. IF marker found (spine exists):
   → APPEND ILC-phase entries to Decision_Log and Lessons_Learned.
   → Use ID prefix ILC-{TYPE}-{NNN}.
   → Add/update the ILC row in the index's "Contributing Phases" table.
   → DO NOT touch other phases' rows (additive, non-destructive).

3. IF marker NOT found (no spine — ILC is first):
   → CREATE management_framework/ at the configured location.
   → Generate the index file (MANAGEMENT_FRAMEWORK.md) using the standard template.
   → Generate Decision_Log.md and Lessons_Learned.md from the schemas below.
   → Other registers are created later by AI-PILC when it runs.
```

---

## Register Schemas (ILC Phase)

### Decision_Log.md
```markdown
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Decision Log

| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| ILC-D-001 | ILC | {date} | {idea gate decision} | {options evaluated} | {rationale} | {user/sponsor} | {downstream impact} | ✅ Final |
```

**Typical ILC decisions:**
- Idea approved → proceed to AI-PILC (or direct to AI-ADLC)
- Idea parked → revisit on {date}
- Idea rejected → rationale documented
- Idea merged with another → combined identity rule
- Scope confirmed at idea stage → build scope locked

---

### Lessons_Learned.md
```markdown
<!-- Shared governance spine | see MANAGEMENT_FRAMEWORK.md -->

# Lessons Learned

| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| ILC-L-001 | ILC | {date} | {lesson} | {what happened during evaluation} | {corrective action} | {Process/Evaluation/Governance} |
```

---

## When AI-ILC Records (Mapping to Stages)

| ILC Stage | Registers Touched | Example |
|:---------:|-------------------|---------|
| Capture | — | (No governance — just idea intake) |
| Shape | — | (Shaping is a draft — no decisions logged) |
| Evaluate | Decisions | `ILC-D-001: Scored 28/35 — PROCEED` |
| Scope | Decisions | `ILC-D-002: v1.0 scope = 7 capabilities; v1.1 deferred` |
| Approve | Decisions, Lessons | `ILC-D-003: APPROVED — proceed to PLAYBOOK Step 1` |

---

## Contributing Phases Row (for the Index)

```markdown
| ILC | AI-ILC | {date} | Decision, Lessons |
```

---

*Template Version: 1.0.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.1.0 | Package: AI-ILC | Phase code: ILC*
