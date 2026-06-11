# Management Framework — Spine Contribution Guide (AI-GCE)

| Field | Value |
|-------|-------|
| **Package** | AI-GCE (Governance & Compliance Engine) |
| **Phase Code** | `GCE` |
| **Role** | Contributor — logs compliance-governance decisions to the shared spine; primary operational record remains `.governance/compliance-log/` |
| **Registers Contributed To** | 2 (Decision, Lessons) |
| **Contract Reference** | `ai-packages/MANAGEMENT_FRAMEWORK_CONTRACT.md` v1.1.0 |

---

## Purpose

AI-GCE's primary record is its own `.governance/compliance-log/` (JSONL events, brownfield baselines, adoption plans). That remains unchanged — it is the **detailed operational audit trail**.

This guide defines when and how AI-GCE also writes **summary governance entries** to the shared project spine. The spine entries are the human-readable, cross-phase governance record; the compliance-log is the machine-readable detail.

---

## What AI-GCE Logs to the Spine (and What It Does NOT)

| Logs to Spine (summary, human-governance) | Stays in `.governance/compliance-log/` (detail, operational) |
|-------------------------------------------|--------------------------------------------------------------|
| `GCE-D-001: Baseline scan — 12 violations acknowledged as tech debt` | Every individual violation event (JSONL) |
| `GCE-D-002: Tier 2 activated — 8 new hooks deployed` | Per-hook trigger events, scores, timestamps |
| `GCE-L-001: Brownfield adoption took 3 sprints — plan for 4 next time` | Detailed remediation workflow history |
| `GCE-D-003: Exception granted — module X exempt from coverage rule` | Exception workflow JSON record |

**Rule of thumb:** if a human PM reading the Decision Log would care about it as a *project governance decision* → it goes in the spine. If it's a technical enforcement event → it stays in the compliance log.

---

## Behavior: Append-if-Exists Only

AI-GCE **always runs after AI-DWG** (it reads the development workspace). The spine will already exist by the time AI-GCE runs. Therefore:

```
1. DETECT the spine by marker: management_framework/MANAGEMENT_FRAMEWORK.md
2. APPEND GCE-phase entries to Decision_Log and Lessons_Learned.
3. Use ID prefix GCE-{TYPE}-{NNN}.
4. Add/update the GCE row in the index's "Contributing Phases" table.
5. DO NOT touch other phases' rows.
```

**Edge case (standalone AI-GCE on a workspace with no spine):** If marker is not found, AI-GCE does NOT create the spine — that's AI-DWG's or AI-PILC's job. Instead, log the entries to the console/output and note "No governance spine found — entries not persisted to management_framework/."

---

## Register Schemas (GCE Phase)

### Decision_Log.md (append)
```markdown
| ID | Phase | Date | Decision | Context / Options Considered | Rationale | Decision Maker | Impact | Status |
|----|-------|------|----------|------------------------------|-----------|----------------|--------|:------:|
| GCE-D-001 | GCE | {date} | {compliance governance decision} | {context} | {rationale} | {team/user} | {impact} | ✅ Final |
```

**Typical GCE decisions:**
- Brownfield baseline accepted (N violations acknowledged)
- Compliance tier activated (Tier 1/2/3)
- Exception granted (module/rule/justification)
- Hook classification changed (fileEdited → agentStop or vice versa)
- Re-derivation scope decision (full vs selective)

### Lessons_Learned.md (append)
```markdown
| ID | Phase | Date | Lesson | Context | Action Taken | Category |
|----|-------|------|--------|---------|--------------|----------|
| GCE-L-001 | GCE | {date} | {lesson} | {what happened} | {corrective action} | {Compliance/Adoption/Process} |
```

---

## When AI-GCE Records (Mapping to Modes)

| GCE Mode | Registers Touched | Example |
|:--------:|-------------------|---------|
| Mode 1 (Full Generation) | Decisions | `GCE-D-001: Full compliance engine generated — Tier 1 active (11 hooks)` |
| Mode 2 (Re-Derivation) | Decisions | `GCE-D-002: Re-derived api-standards rules after ADR-012 change` |
| Mode 3 (Brownfield) | Decisions, Lessons | `GCE-D-003: Baseline scan — 12 pre-existing violations acknowledged` |
| Mode 4 (Tier Activation) | Decisions | `GCE-D-004: Tier 2 readiness confirmed — 8 advisory hooks promoted to blocking` |

---

## Contributing Phases Row (for the Index)

```markdown
| GCE | AI-GCE | {date} | Decision, Lessons |
```

---

*Template Version: 1.0.0 | Contract: MANAGEMENT_FRAMEWORK_CONTRACT.md v1.1.0 | Package: AI-GCE | Phase code: GCE*
