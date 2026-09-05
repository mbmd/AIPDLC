<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Debt Reassessment

## Stage: 12 of 12
## Phase: 🟢 OBSERVATION
## Execution: ALWAYS (after coverage report or reconciliation)

---

## Purpose

Re-score all missing tests because risk factors change over time. A test that was Low priority last sprint may now be Critical because the component entered active development (Change Frequency increased) or a related defect was filed (Architectural Risk reconfirmed). Produce an updated **Debt Scorecard** with current priorities and highlight score changes.

This stage closes the observation cycle and feeds back into sprint planning.

---

## Depth Adaptation

| Depth | Reassessment Scope | Output Detail |
|-------|-------------------|--------------|
| **Minimal** | Re-score only entries whose components were touched this cycle. Produce updated bucket counts and top 5 list. | Bucket summary + top 5 |
| **Standard** | Re-score all Missing/Failing entries. Compare to previous scores. Highlight movements (any entry that changed bucket). Updated full ranked scorecard. | Full re-score + delta + movement highlights |
| **Comprehensive** | Full re-score + score rationale per entry + effort re-estimation + updated sprint plan + defect-driven priority boosts + trend analysis (which components are accumulating debt fastest). | Complete analysis + trend + sprint replan |

---

## MANDATORY: Stage Sub-Role — Risk Analyst

During THIS stage, ALSO adopt the mindset of a **Risk Analyst**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Reassess with CURRENT information — don't just replay previous scores
- Factor in recent events: defects filed against a component INCREASE its risk; tests written REDUCE its debt
- Highlight movements explicitly: "SEC-003 moved from High → Critical because a related security defect (DEF-005) confirmed the risk is real"
- Think about trend: is debt accumulating faster than it's being addressed?

### Anti-Patterns for This Stage
- Do NOT simply copy previous scores — reassessment means RE-evaluation
- Do NOT ignore defect data — a defect in Component X means X's missing tests are now higher priority
- Do NOT present flat scores without context — explain WHY something moved up or down
- Do NOT skip this stage because "nothing changed" — at minimum, Change Frequency scores update based on git activity **where that evidence is available**
- Do NOT treat a carried-forward Change Frequency as a re-derived one — if no activity evidence resolved, say so (Step 2); a stale factor multiplies into every composite that depends on it and silently reorders the debt queue

### Quality Check
A good output at this stage sounds like:
- "Reassessed 24 remaining Missing entries. 4 movements: SEC-003 Medium → Critical (DEF-005 confirmed exploit path), BL-012 High → Medium (component stabilized, no changes in 3 sprints), INT-007 Low → High (integration under active development), API-009 removed from scorecard (test written). Net: 2 Critical (+1), 7 High (-1), 10 Medium (+1), 5 Low (-1). Sprint 5 recommendation: prioritize SEC-003 + INT-007."

---

## Step-by-Step Execution

### Step 1: Identify Entries to Re-Score

From current register, select all scoring targets:

| Condition | Action |
|-----------|--------|
| Status = Missing | ✅ Re-score (primary target) |
| Status = Failing | ✅ Re-score (failing = same risk as missing) |
| Status = Required (never assessed) | ✅ First-time scoring (new entries from reconciliation) |
| Status = Exists | ❌ Skip (no longer debt) |
| Status = Deprecated | ❌ Skip (no longer relevant) |
| Status = Overridden | ❌ Skip (user accepted) |

---

### Step 2: Gather New Evidence for Scoring

Before re-scoring, collect factors that may have changed:

| Evidence Source | Internal or external? | What It Affects | How |
|----------------|:--------------------:|----------------|-----|
| **Recent defects** (defect log) | internal | Architectural Risk ↑ | Defect in Component X confirms risk is real, not theoretical |
| **Code changes** (git activity or DLC state) | ⚠️ **external** | Change Frequency ↑↓ | Active development → higher frequency; stable → lower |
| **New dependencies** (reconciliation additions) | internal | Blast Radius ↑ | New consumers of a component increase blast radius |
| **Team changes** | internal | Logic Complexity perception | New team members on complex code → harder to catch bugs |
| **Sprint context** | internal | All factors | About to release → higher urgency for everything |

#### The one external evidence source, and what to do when it is unavailable

Every source above except one is derived from artifacts AI-TGE owns. **Change Frequency is the exception** — it needs git history or build state, and neither is guaranteed: a shallow clone carries no history, a workspace may have no version control at all, and the build state may not resolve (Stage 7's declared input, resolved via `manifest.files.buildState` — `common/manifest-resolution.md`).

| Situation | Behaviour | Fidelity |
|---|---|:---:|
| Git history or build state available | Re-derive Change Frequency from observed activity | unaffected |
| **Neither available** | **Carry the previous cycle's Change Frequency forward unchanged** — do not guess, do not default to a middle value, and do **not** silently drop the factor from the product | **⚠️ Degraded** |

**When carried forward, record:** input = *Change Frequency evidence (git activity or build state)* · substitute = *previous cycle's score carried forward* · unmeasured = **the debt ranking is carried forward, not recalculated — a component that entered active development this cycle is still ranked as though it had not.**

⚠️ **Why this factor matters more than its size suggests.** The four factors **multiply**: composite = Architectural Risk × Blast Radius × Logic Complexity × Change Frequency. A stale Change Frequency therefore does not shift one number slightly — it propagates through every composite that depends on it, and the composite is what **orders the debt scorecard**. The scorecard is the team's work queue, so a silently-assumed factor decides what gets tested next. That is why this is disclosed rather than absorbed (`common/observation-fidelity.md` · `INV-L2-021`).

**Mark the affected rows.** Any entry whose Change Frequency was carried forward gets `⚠️` on its composite in the scorecard, and the scorecard states that its ordering is partly carried forward rather than freshly derived.

---

### Step 3: Re-Score Each Entry

Apply the same four-factor model (from Stage 6), updated with current evidence:

| Factor | Original Score | Current Evidence | New Score | Change |
|--------|:--------------:|-----------------|:---------:|:------:|
| Architectural Risk | {n} | {evidence if changed} | {n} | {±n or "—"} |
| Blast Radius | {n} | {evidence if changed} | {n} | {±n or "—"} |
| Logic Complexity | {n} | {evidence if changed} | {n} | {±n or "—"} |
| Change Frequency | {n} | {evidence if changed / ⚠️ **carried forward — no activity evidence available**} | {n} | {±n or "—"} |

**Recalculate composite:** New composite = product of updated factors.
**Reassign bucket** if threshold crossed.

⚠️ **A composite containing a carried-forward factor is marked, not silently recomputed.** Write `{composite}⚠️` and keep the *Current Evidence* cell honest — *"carried forward"* is evidence of nothing having been observed, which is a different statement from *"—"* (observed, unchanged). Those two are the pair this stage must not collapse.

---

### Step 4: Detect Score Movements

Compare previous bucket to current bucket for each entry:

| Movement Type | Significance | Highlight? |
|:------------:|-------------|:----------:|
| Low → Medium | Minor escalation | ℹ️ Note |
| Medium → High | Meaningful escalation | ⚠️ Highlight |
| High → Critical | Major escalation — needs immediate attention | 🔴 Alert |
| Critical → High | De-escalation (rare — usually means partial mitigation) | ✅ Positive |
| Any → removed (test written) | Debt resolved | ✅ Celebrate |
| New entry (from reconciliation) | New debt | ➕ Flag as new |

```markdown
## Score Movements This Cycle

| ID | Test Name | Previous | Current | Direction | Reason |
|:--:|-----------|:--------:|:-------:|:---------:|--------|
| SEC-003 | MFA bypass test | 🟡 Medium (108) | 🔴 Critical (500) | ⬆⬆ | DEF-005 confirmed exploit; Arch Risk 3→5, Blast 3→5 |
| BL-012 | Discount edge case | 🟠 High (180) | 🟡 Medium (60) | ⬇ | No changes to module in 3 sprints; Change Freq 4→2 |
| INT-007 | Timeout handling | 🟢 Low (36) | 🟠 High (225) | ⬆⬆ | Integration under active rebuild; all factors increased |
| API-009 | User list pagination | 🟠 High (150) | — (resolved) | ✅ | Test written — removed from debt |
```

---

### Step 5: Update Debt Scorecard

Produce updated ranked scorecard:

```markdown
# Debt Scorecard (Updated)

**Type:** Debt Scorecard
**Generated:** {ISO timestamp}
**Engine:** AI-TGE v1.0.0
**Reassessment Cycle:** {n} (increments each time)

## Summary

| Bucket | Previous | Current | Delta |
|--------|:--------:|:-------:|:-----:|
| 🔴 Critical | {n} | {n} | {±n} |
| 🟠 High | {n} | {n} | {±n} |
| 🟡 Medium | {n} | {n} | {±n} |
| 🟢 Low | {n} | {n} | {±n} |
| **Total** | **{N}** | **{N}** | **{±n}** |

## Movements
{Table from Step 4}

## Current Ranked List
{Full ranked table — same format as Stage 6 output}

## Sprint Recommendation (Updated)
{Revised sprint allocation based on current scores}
```

---

### Step 6: Debt Trend Analysis (Comprehensive Depth)

```markdown
## Debt Trend

| Cycle | Total Debt | Critical | Resolved This Cycle | New This Cycle | Net |
|:-----:|:----------:|:--------:|:-------------------:|:--------------:|:---:|
| 1 (initial) | {n} | {n} | — | {n} | +{n} |
| 2 | {n} | {n} | {n} | {n} | {±n} |
| 3 | {n} | {n} | {n} | {n} | {±n} |
| Current | {n} | {n} | {n} | {n} | {±n} |

**Debt velocity:** {Accumulating / Stable / Decreasing}
- Resolved per sprint: {average}
- New per sprint: {average}
- Net trend: {direction}

{IF accumulating:}
⚠️ Debt is growing faster than it's being resolved. At current pace, Critical debt will increase by {n} per sprint. Recommend: allocate more capacity to test writing or reduce scope of new features.

{IF decreasing:}
✅ Debt is being resolved faster than new debt accumulates. At current pace, all Critical/High items addressed in {n} sprints.
```

---

### Step 7: Update Artifacts

1. **Debt Scorecard** (`.governance/test/debt-scorecard.md`) — overwrite with current ranked list
2. **Test Register** (`.governance/test/test-register.md`) — update Risk Score column for re-scored entries
3. **State File** (`.governance/test/tge-state.md`) — update timestamp, register stats

---

### Step 8: Report (Non-Blocking)

```markdown
## 🟢 Debt Reassessment Complete

**Entries re-scored:** {N}
**Movements:** {n} ({n} escalations, {n} de-escalations)
**Net debt change:** {±n} since last assessment

**Critical attention:**
{IF critical movements exist:}
🔴 {entry} escalated to Critical — {brief reason}

{IF all clear:}
✅ No new Critical escalations. Current priorities stable.

**Updated scorecard:** `.governance/test/debt-scorecard.md`
**Sprint recommendation:** Address {top entries} this sprint for maximum risk reduction.
```

**No gate.** Debt reassessment is informational — it updates priorities and informs sprint planning. No user action required to continue.

---

## Observation Phase Cycle

After Stage 12 completes, the observation phase loops:

```
Stage 7 (State Observation) → Stage 8 (Story Mapping, if new stories)
     → Stage 9 (Coverage Report) → Stage 10 (Reconciliation, if AP changed)
     → Stage 11 (Defect Logging, if defects reported) → Stage 12 (Debt Reassessment)
     → [back to Stage 7 on next invocation]
```

The engine remains in Observation phase indefinitely — it runs each time AI-TGE is invoked and loops through applicable stages.

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Updated Debt Scorecard | `.governance/test/debt-scorecard.md` | Current ranked priorities |
| Updated Test Register | `.governance/test/test-register.md` | Risk Score column updated |
| Updated state file | `.governance/test/tge-state.md` | Stats and timestamp current |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| **Activity-evidence availability established** | Git history or build state either resolved, or its absence recorded per Step 2. ⚠️ **A Change Frequency score derived from no evidence is a FAIL** — carried forward is acceptable, invented is not |
| **Carried-forward factors marked** | Every composite containing a carried-forward Change Frequency carries `⚠️`, and its *Current Evidence* cell reads *"carried forward"* rather than `—` |
| **Ranking provenance stated** | If any factor was carried forward, the debt scorecard states that its ordering is partly carried forward rather than freshly derived — the scorecard is the work queue, so its provenance is not optional |
| **Degradation disclosed in all three destinations** | If activity evidence did not resolve: the coverage report artifact, the state file, **and** this stage's report each say so. Two of three is a FAIL |
| All targets re-scored | Every Missing/Failing entry has current 4-factor score |
| Evidence considered | Recent defects, code changes, reconciliation factored in |
| Movements highlighted | Any bucket change explicitly noted with reason |
| Composite recalculated | Product of updated factors (not sum) |
| Scorecard updated | `.governance/test/debt-scorecard.md` reflects current rankings |
| Sprint recommendation current | Top priorities reflect latest evidence |
| Trend tracked (Comprehensive) | Accumulation vs. resolution rate assessed |
| State file updated | Timestamp and stats current |
| Non-blocking | No gate — inform and loop |
