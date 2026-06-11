# Management Framework — Spine Contribution Guide (AI-TGE)

| Field | Value |
|-------|-------|
| **Package** | AI-TGE (Test Governance Engine) |
| **Phase Code** | `TGE` |
| **Role** | Contributor — logs test-governance decisions to the shared spine; primary operational record remains `.tge/` |
| **Registers Contributed To** | 2 (Decision, Lessons) |
| **Contract Reference** | `ai-packages/MANAGEMENT_FRAMEWORK_CONTRACT.md` v1.1.0 |

---

## Purpose

AI-TGE's primary record is its own `.tge/` folder (test register, coverage reports, debt scorecard, defect log). That remains unchanged — it is the **detailed test-governance operational record**.

This guide defines when and how AI-TGE also writes **summary governance entries** to the shared project spine. The spine entries are the human-readable, cross-phase governance record; `.tge/` is the detailed test-specific record.

---

## What AI-TGE Logs to the Spine (and What It Does NOT)

| Logs to Spine (summary, human-governance) | Stays in `.tge/` (detail, operational) |
|-------------------------------------------|----------------------------------------|
| `TGE-D-001: Test strategy finalized — pyramid model, 80% coverage target` | Full `test-strategy.md` document |
| `TGE-D-002: Risk acceptance — module X deliberately untested (low blast radius)` | Debt scorecard entry + risk score |
| `TGE-D-003: Brownfield assessment — 45% existing coverage, 23 gaps identified` | Complete brownfield gap map |
| `TGE-L-001: Architecture reconciliation added 8 tests — reconcile earlier next time` | Register delta details |

**Rule of thumb:** if a human PM reading the Decision Log would care about it as a *project governance decision* → it goes in the spine. If it's a test register entry, coverage calculation, or risk score → it stays in `.tge/`.

---

## Behavior: Append-if-Exists Only

AI-TGE **reads from AI-ADLC + AI-DWG** and observes AI-DLC. The spine will typically exist by the time AI-TGE runs. Therefore:

```
1. DETECT the spine by marker: management_framework/MANAGEMENT_FRAMEWORK.md
2. APPEND TGE-phase entries to Decision_Log and Lessons_Learned.
3. Use ID prefix TGE-{TYPE}-{NNN}.
4. Add/update the TGE row in the index's "Contributing Phases" table.
5. DO NOT touch other phases' rows.
```

**Edge case (standalone AI-TGE — Architecture Only mode, no spine):** If marker is not found, AI-TGE does NOT create the spine. Log the entries to the console/output and note "No governance spine found — entries not persisted to management_framework/."

---

## Register Schemas (TGE Phase)

### Decision_Log.md (append)
```markdown
| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| TGE-D-001 | TGE | {date} | {test governance decision} | {context} | {rationale} | {user/QA lead} | {impact} | ✅ Final |
```

**Typical TGE decisions:**
- Test strategy finalized (model, coverage target, depth level)
- Risk acceptance (component deliberately untested — rationale documented)
- Override of a derived test requirement (user disagrees with AI's derivation)
- Brownfield baseline accepted (existing coverage level acknowledged)
- Architecture reconciliation — new tests added / old tests deprecated

### Lessons_Learned.md (append)
```markdown
| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| TGE-L-001 | TGE | {date} | {lesson} | {what happened} | {corrective action} | {Testing/Process/Architecture} |
```

---

## When AI-TGE Records (Mapping to Stages)

| TGE Stage | Registers Touched | Example |
|:---------:|-------------------|---------|
| 4 (Brownfield Assessment) | Decisions | `TGE-D-001: Brownfield baseline — 45% coverage, 23 gaps` |
| 5 (Test Strategy) | Decisions | `TGE-D-002: Test pyramid adopted — unit 70% / integration 20% / E2E 10%` |
| 6 (Risk Scoring) | Decisions | `TGE-D-003: 3 Critical-risk gaps accepted (team capacity)` |
| 10 (Architecture Reconciliation) | Decisions, Lessons | `TGE-L-001: AP change added 8 new requirements — reconcile earlier` |
| 12 (Debt Reassessment) | Lessons | `TGE-L-002: Debt reduced from 15→7 in 2 sprints — risk scoring drove focus` |

---

## Contributing Phases Row (for the Index)

```markdown
| TGE | AI-TGE | {date} | Decision, Lessons |
```

---

*Template Version: 1.0.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.1.0 | Package: AI-TGE | Phase code: TGE*
