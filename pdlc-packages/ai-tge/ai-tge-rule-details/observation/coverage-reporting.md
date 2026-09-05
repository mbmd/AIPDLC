<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Coverage Reporting

## Stage: 9 of 12
## Phase: 🟢 OBSERVATION
## Execution: ALWAYS (in Observation Phase)

---

## Purpose

Generate a multi-dimensional **Coverage Report** showing how well the project's actual tests match the required tests in the register. Coverage is calculated from register data (tests existing / tests required) — this is commitment-based coverage, not line-of-code coverage. The report provides multiple views to help teams understand WHERE gaps exist, not just that gaps exist.

---

## Depth Adaptation

| Depth | Report Scope | Views Provided |
|-------|-------------|:-------------:|
| **Minimal** | Single overall percentage + category breakdown. Top 5 gaps listed. No trend data. | 2 views (overall + by category) |
| **Standard** | Multi-view: by commitment, by component, by test type, by risk level. Gap list with specific entry details. Trend data if prior reports exist. | 4 views + trend |
| **Comprehensive** | All Standard views + traceability matrix + heat map by component + historical trend chart + coverage velocity (rate of improvement) + forecasting ("at current pace, 80% coverage in {n} sprints"). | 6+ views + trend + forecast |

---

## MANDATORY: Stage Sub-Role — Audit Specialist

During THIS stage, ALSO adopt the mindset of an **Audit Specialist**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Report facts, not opinions — "42% coverage" not "coverage is concerning"
- Present multiple views because different stakeholders need different angles (dev team needs component view; PM needs risk view; architect needs commitment view)
- Calculate precisely — exclude Deprecated and Overridden from denominators
- Compare against TARGETS (from test strategy) — not just raw numbers

### Anti-Patterns for This Stage
- Do NOT claim 100% coverage without verifying every entry Status = Exists
- Do NOT present a single percentage as "the" coverage number — always contextualize
- Do NOT hide low coverage — the point of governance is transparency
- Do NOT include Deprecated/Overridden entries in calculations — they're excluded by design

### Quality Check
A good output at this stage sounds like:
- "Overall coverage: 58% (39/67 active entries). By risk: Critical = 67% (2/3 gaps addressed), High = 50%, Medium = 62%, Low = 45%. By component: PaymentService = 33% (highest-risk area), UserService = 75%, OrderService = 60%. Trend: +13% since last report (3 tests added in Sprint 4). At current velocity, 80% target in ~2 sprints."

---

## Step-by-Step Execution

### Step 0: Read Observation Fidelity — BEFORE calculating anything

Read `tge-state.md → Observation Fidelity`. This stage **reports** fidelity; it never assesses it (assessment belongs to Stage 1 and Stage 7).

| Fidelity | What this stage does |
|:--------:|----------------------|
| **✅ Full** | Report normally. No banner, no markers. |
| **⚠️ Degraded** | Compile the banner and the `### Observation Fidelity` subsection of `## Completeness & Downstream Resolution` into the report (Step 8), lead the summary with it (Step 9), and mark every affected figure. |
| **❌ Unknown** | **Treat exactly as Degraded.** An unassessed run is never reported as a clean one (fail-closed rule F1). Banner states that fidelity was not assessed. |

**Why this is Step 0 and not Step 8.** Every figure this stage produces may be derived from a substitute. Reading fidelity after the calculations would mean deciding what to qualify *after* deciding what to say, and the qualification would be applied by memory rather than by rule. Definition, the three canonical blocks, and the fail-closed rules: `common/observation-fidelity.md`.

---

### Step 1: Calculate Base Metrics

From the current test register:

```markdown
## Metric Definitions

Active entries = Total - Deprecated - Overridden
Coverage % = (Exists + Failing*) / Active entries × 100

* Failing tests COUNT as covered (test exists, just needs fixing).
  They're tracked separately but don't penalize coverage %.
  ONLY Missing entries are true gaps.
```

| Metric | Formula | Value |
|--------|---------|:-----:|
| Total register entries | Count all | {N} |
| Deprecated | Status = Deprecated | {n} |
| Overridden | Status = Overridden | {n} |
| **Active entries** | Total - Deprecated - Overridden | **{N}** |
| Exists | Status = Exists or Exists (unverified) | {n} |
| Failing | Status = Failing | {n} |
| Missing | Status = Missing or Required | {n} |
| **Coverage %** | (Exists + Failing) / Active × 100 | **{n}%** |

---

### Step 2: Generate View — By Architectural Commitment

Group register entries by commitment category:

```markdown
## Coverage by Commitment Category

| Category | Active | Covered | Missing | Coverage % | Target | Gap to Target |
|----------|:------:|:-------:|:-------:|:----------:|:------:|:-------------:|
| API | {n} | {n} | {n} | {n}% | {from strategy} | {±n}% |
| Security | {n} | {n} | {n} | {n}% | {target} | {±n}% |
| Business Logic | {n} | {n} | {n} | {n}% | {target} | {±n}% |
| Integration | {n} | {n} | {n} | {n}% | {target} | {±n}% |
| Data | {n} | {n} | {n} | {n}% | {target} | {±n}% |
| Performance/NFR | {n} | {n} | {n} | {n}% | {target} | {±n}% |
| Workflow | {n} | {n} | {n} | {n}% | {target} | {±n}% |
| Configuration | {n} | {n} | {n} | {n}% | {target} | {±n}% |
```

---

### Step 3: Generate View — By Component

Group by architectural component:

```markdown
## Coverage by Component

| Component | Active | Covered | Missing | Coverage % | Risk Exposure |
|-----------|:------:|:-------:|:-------:|:----------:|:-------------:|
| {ComponentName} | {n} | {n} | {n} | {n}% | {sum of missing risk scores} |
| ... | ... | ... | ... | ... | ... |

**Most at-risk component:** {component} (coverage {n}%, risk exposure {score})
**Best-covered component:** {component} (coverage {n}%)
```

---

### Step 4: Generate View — By Test Level

Distribution across the test pyramid:

```markdown
## Coverage by Test Level

| Level | Active | Covered | Missing | Coverage % | Pyramid Target |
|-------|:------:|:-------:|:-------:|:----------:|:--------------:|
| Unit | {n} | {n} | {n} | {n}% | {n}% |
| Integration | {n} | {n} | {n} | {n}% | {n}% |
| System | {n} | {n} | {n} | {n}% | {n}% |
| Acceptance | {n} | {n} | {n} | {n}% | {n}% |

**Pyramid health:** {Assessment — e.g., "Heavy on unit tests, integration gap"}
```

---

### Step 5: Generate View — By Risk Level

Coverage within each risk bucket:

```markdown
## Coverage by Risk Level

| Risk Bucket | Active | Covered | Missing | Coverage % | Interpretation |
|-------------|:------:|:-------:|:-------:|:----------:|---------------|
| 🔴 Critical | {n} | {n} | {n} | {n}% | {comment: "2 Critical gaps remain — highest priority"} |
| 🟠 High | {n} | {n} | {n} | {n}% | {comment} |
| 🟡 Medium | {n} | {n} | {n} | {n}% | {comment} |
| 🟢 Low | {n} | {n} | {n} | {n}% | {comment} |

**Risk-weighted coverage:** Critical risks at {n}% is {"acceptable" / "concerning" / "critical gap"}
```

---

### Step 6: Trend Analysis (If Prior Report Exists)

Compare to previous coverage report:

```markdown
## Coverage Trend

| Metric | Previous | Current | Delta | Direction |
|--------|:--------:|:-------:|:-----:|:---------:|
| Overall coverage | {n}% | {n}% | {±n}% | {↑/→/↓} |
| Critical gaps | {n} | {n} | {±n} | {↑/→/↓} |
| High gaps | {n} | {n} | {±n} | {↑/→/↓} |
| Total active entries | {n} | {n} | {±n} | — |

**Period:** {previous date} → {current date}
**Velocity:** {n} tests added per sprint (average)
{IF any cycle in this period was not ✅ Full:}
⚠️ **This trend spans a degraded cycle** ({cycle} — {which input did not resolve}). The delta measures the change in **observation**, not only the change in **tests**.
```

**MANDATORY — check every contributing cycle's fidelity, not just the current one.** Read the Fidelity column of `tge-state.md → Observation History` across the period.

A trend is the figure most easily corrupted by degradation, and it corrupts in a **flattering** direction: when a degraded cycle is followed by a full one, coverage appears to jump because the engine started seeing entries it previously could not, and the report reads as progress nobody made. **NEVER present a cross-cycle delta as test progress when any contributing cycle was degraded.** Suppress the velocity figure and the forecast entirely in that case — a forecast extrapolated from a measurement artefact is worse than no forecast, because it carries a date.

**Comprehensive depth — forecast:**
```markdown
## Coverage Forecast

At current velocity ({n} tests per sprint):
- 70% coverage: ~{n} sprints
- 80% coverage: ~{n} sprints
- 90% coverage: ~{n} sprints

**Bottleneck:** {category/component with slowest progress}
**Recommendation:** {prioritize X to unblock Y}
```

---

### Step 7: Identify Specific Gaps

List the most important missing tests:

```markdown
## Top Gaps — Immediate Attention

| # | ID | Test Name | Component | Risk Score | Bucket |
|---|:--:|-----------|-----------|:----------:|:------:|
| 1 | {id} | {name} | {comp} | {score} | 🔴 |
| 2 | {id} | {name} | {comp} | {score} | 🔴 |
| 3 | {id} | {name} | {comp} | {score} | 🟠 |
| 4 | {id} | {name} | {comp} | {score} | 🟠 |
| 5 | {id} | {name} | {comp} | {score} | 🟠 |
```

---

### Step 8: Compile Coverage Report

```markdown
# Coverage Report

**Type:** Coverage Report
**Generated:** {ISO timestamp}
**Engine:** AI-TGE v1.0.0
**Mode:** {mode}
**Observation Fidelity:** {✅ Full / ⚠️ Degraded / ❌ Unknown}
**Depth:** {depth level}

{IF fidelity is not ✅ Full — the banner goes HERE, above the Executive Summary:}
> ⚠️ **DEGRADED OBSERVATION — these figures are incomplete.**
> {n} of {N} declared inputs for {mode} mode did not resolve:
> - **{input}** — expected at `{path}`; substituted with {substitute}
>
> **Therefore unmeasured:** {unmeasured consequence}
> {IF ❌ Unknown:} Fidelity was not assessed for this cycle, so it is reported as degraded.
>
> Per-input detail: `.governance/test/tge-state.md` → Observation Fidelity.

## Executive Summary
- **Overall coverage:** {n}%{⚠️ if degraded} ({n}/{n} active entries)
- **Critical gaps:** {n} remaining
- **Trend:** {↑ Improving / → Stable / ↓ Declining} ({±n}% since last report){⚠️ if any contributing cycle was degraded}
- **Target:** {n}% (from test strategy)
- **Gap to target:** {n}%

{View 1: By Commitment Category}
{View 2: By Component}
{View 3: By Test Level}
{View 4: By Risk Level}
{View 5: Trend — if prior data exists}
{View 6: Top Gaps}

{The mandatory Completeness section — ALWAYS emitted, per IMP-002, whatever the fidelity:}
## Completeness & Downstream Resolution

### Observation Fidelity — {✅ Full / ⚠️ Degraded / ❌ Unknown}
{Per-input resolution table, copied from tge-state.md: input · expected at · resolved · substitute used · unmeasured consequence}

### What This Report Measures Completely
### What Is Partial — and Where It Gets Resolved
{one row per unresolved input, naming the action that would resolve it}
### What Is Out of Scope
```

**IMP-002 is emitted on every run, not only degraded ones.** `common/artifact-sections.md` declares it BLOCKING for every artifact, and a completeness section that appears only when something is wrong is itself a signal — a reader learns to check whether the section exists rather than reading what it says. On a `✅ Full` run it states that every declared input resolved. Full structure: `templates/coverage-report.md`.

Save to `.governance/test/coverage-report.md` (overwrites previous — each report is a current snapshot).

**Marking rules — apply to every affected figure, not only the headline:**

| Figure | Mark when |
|--------|-----------|
| Overall coverage | Fidelity is not `✅ Full` |
| The Acceptance row of View 3 (By Test Level) | The user-story location did not resolve — the 0 there is unmeasured, not untested |
| The Performance/NFR row of View 1 | The NFR location did not resolve |
| Trend, velocity, forecast | Any contributing cycle was not `✅ Full` (Step 6) |
| Any chart in the Visualization Pack | Its source data carries a marker — the caption states it |

**The "What is unaffected" line is not optional padding.** A degraded report is still useful, and saying which views survived intact is what keeps it useful. A blanket warning over a whole report teaches a reader to discount all of it, including the parts that are exactly right.

---

### Step 9: Present Summary

```markdown
{IF fidelity is not ✅ Full — this block comes FIRST, before any figure:}
## ⚠️ Coverage Report Generated — DEGRADED

⚠️ **DEGRADED OBSERVATION — the figures below are incomplete.**
{n} of {N} declared inputs for {mode} mode did not resolve:
- **{input}** — expected at `{path}`; substituted with {substitute}

**Therefore unmeasured:** {unmeasured consequence}
**Unaffected:** {which views are intact}

---

{THEN, or immediately if fidelity is ✅ Full:}
## 🟢 Coverage Report Generated

**Overall:** {n}%{⚠️ if degraded} coverage ({n}/{n} active requirements)
**Vs. target:** {n}% gap to {target}%
**Critical gaps:** {n} remaining
**Trend:** {direction} ({±n}% since last){⚠️ if any contributing cycle was degraded}

**Key insight:** {One sentence: what's the most important thing the team should know?}
{IF degraded, the key insight names the degradation — it is the most important thing:}
- Example: "Acceptance coverage reads 0% because the story location was not found, not because acceptance tests are missing — confirm where this workspace keeps its stories before reading any acceptance figure"
- Example: "PaymentService is the biggest risk: 33% coverage with 3 Critical-risk gaps"
- Example: "All Critical tests now exist — focus on High-priority integration tests"

**Full report:** `.governance/test/coverage-report.md`

---

**Your response:**
- (a) **Acknowledge** — I've seen the coverage; continue observation
- (b) **Drill down** — show me details for {component/category}
- (c) **Reprioritize** — I want to adjust which gaps we address first
- (d) **Override** — I want to accept certain gaps (mark as Overridden)
```

---

### Visualization Pack (depth-gated)

| Depth | Diagram | Mermaid type | Source |
|-------|---------|:------------:|--------|
| Standard | Coverage dashboard (component × coverage %) | `xychart-beta` | Coverage data |
| Comprehensive | Coverage trend over time | `xychart-beta` | Historical data |

Emit from coverage data. No new content introduced.

---

## Gate

**Soft gate.** Coverage reporting presents results for review. The user CAN acknowledge and continue without action. But if coverage is below target and Critical gaps exist, highlight this clearly.

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Coverage Report | `.governance/test/coverage-report.md` | Current coverage snapshot (multi-view) |
| Updated state file | `.governance/test/tge-state.md` | Coverage % and stats updated |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| **Fidelity read before calculating** | Step 0 ran; the value is `✅ Full`, `⚠️ Degraded` or `❌ Unknown`, and `❌ Unknown` was handled as Degraded |
| **Banner present in the artifact** | If fidelity is not `✅ Full`: the banner sits **above** the Executive Summary in `coverage-report.md`. A degraded report with unqualified figures is a FAIL |
| **IMP-002 section present** | `## Completeness & Downstream Resolution` is emitted on **every** run with its `### Observation Fidelity` subsection populated — BLOCKING per `common/artifact-sections.md`, not conditional on degradation |
| **Banner present in the summary** | If fidelity is not `✅ Full`: the in-session summary leads with it, before any figure |
| **Every affected figure marked** | Overall coverage, the Acceptance row, the NFR row, and any chart whose source data is degraded each carry the marker — not the headline alone |
| **Trend fidelity-checked across cycles** | Every contributing cycle's Fidelity value read from Observation History; velocity and forecast suppressed if any was not `✅ Full` |
| **What is unaffected is stated** | A degraded report names which views remain intact, so the reader discounts the affected figures and not the whole report |
| Calculations correct | Coverage % = (Exists + Failing) / Active × 100 |
| Deprecated/Overridden excluded | Not counted in Active entries |
| Multiple views provided | At least 3 views for Standard+, 2 for Minimal |
| Trend included | If prior report exists, delta calculated |
| Gaps specific | Named entries, not just counts |
| Targets referenced | Coverage goals from test strategy shown |
| Report saved | `.governance/test/coverage-report.md` updated |
| State file updated | Coverage stats current |
