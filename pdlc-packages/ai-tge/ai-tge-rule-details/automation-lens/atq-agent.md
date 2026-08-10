# AIFLC Automation Quality — Agent Template

> **Trigger:** `ATQ__` (manual invocation)
> **Owner:** AI-TGE
> **Type:** Audit
> **Core impact:** None — the TGE core stays concern-agnostic. This agent is seeded into the Layer-3 workspace by AI-DWG and dispatched by TGE's existing Command Dispatch.

---

## Purpose

Verify automated-feature quality and correctness, using the couriered automation-feature context from `{slug}-workspace/.automation-lens/manifest.json`. Writes results into `.tge/`.

This is the **quality half** of the govern+verify bracket around the (un-lensed) builder. It tests that automated features meet their acceptance criteria and — critically — that the reliability and loop guards the architecture designed actually work. Runs across any build engine (AI-DLC v1, spec-driven, freestyle).

---

## When to Invoke

- After initial automation implementation (first correctness baseline)
- After changes to handler logic, retry config, or guards (regression check)
- Before release (final quality gate)
- Periodically during production (throughput/SLA + failure-rate monitoring)

---

## Consequences of Skipping

- Automation ships without exception-path testing — the unhappy path fails in production
- Idempotency untested — duplicate execution creates duplicate effects (the classic defect)
- **Loop termination untested — a cyclic automation runs away in production**
- Rollback/compensation untested — partial failures leave inconsistent state
- Throughput/SLA acceptance criteria from POLC never validated
- No regression baseline — guard or logic changes cannot be compared

---

## Recovery

If `ATQ__` has not been run and correctness is unknown:
1. Run `ATQ__` in **baseline mode** to establish current behavior
2. Prioritize the **loop test** and **idempotency test** — the two highest-risk automation defects
3. Document the baseline in `.tge/automation-lens/` for future comparison
4. Schedule recurring runs

---

## Input

Reads from `{slug}-workspace/.automation-lens/manifest.json` (couriered by AI-DWG):
- Feature list with `automationFeatureId`, `automationMode`, `automationPattern`, `automationTrigger`
- Acceptance criteria (throughput/SLA, exception handling, straight-through rate, reversibility)
- Architecture decisions (idempotency, retry/compensation strategy — needed to know what to test)
- The **guards** block (hop budget, kill switch — needed for the loop test)
- The `agentic` block (when present) — loop termination (max steps / wall-clock / cost ceiling) — needed for the agentic loop test (Category 5)

Also reads from the live workspace:
- `automation/` handlers, `automation/config.*`, `audit/` sink
- `.tge/automation-lens/` previous results (for regression comparison)
- Test infrastructure / harness

---

## Checks Performed

### Category 1: Correctness (Acceptance Criteria)

| Check | Method | Produces |
|-------|--------|----------|
| **Happy-path validation** | Trigger the automation with valid input; assert the expected effect | PASS / FAIL |
| **Straight-through rate** | Run a representative batch; measure the % completing without human intervention | Rate vs. POLC target |
| **SLA / throughput** | Measure processing time + throughput under representative load | p50/p95 vs. AC bound |

### Category 2: Reliability (the automation-specific risk tests)

| Check | Applies when | What it tests |
|-------|-------------|---------------|
| **Idempotency** | All (any retriable/re-triggerable automation) | Fire the same trigger twice → assert exactly one effect, one audit record, one emit |
| **Exception path** | All with an exception AC | Force the unhappy path (no match, bad input, dependency down) → assert it lands in the exception queue / DLQ with a reason, not silently lost |
| **Retry / backoff** | Retry strategy in architecture | Inject transient failures → assert retry with the configured budget; assert non-retryable errors are NOT retried |
| **Rollback / compensation** | `saga-*` strategy | Force a mid-saga failure → assert every prior step is compensated; assert final state is consistent |
| **Dead-letter handling** | `dead-letter-reprocess` | Exhaust retries → assert item lands in DLQ; assert reprocessing is idempotent |
| **Timeout handling** | Long-running / external calls | Force a timeout → assert graceful handling, no partial-commit |

### Category 3: The Loop Test (the signature automation test)

| Check | Applies when | What it tests |
|-------|-------------|---------------|
| **Loop termination** | `event`-triggered that emits events | Fire the trigger; follow the causal chain; **assert it terminates within the hop budget** (does not run forever) |
| **Self-caused filtering** | causedBy guard designed | Emit a self-caused event; assert the trigger filter drops it |
| **Hop-budget enforcement** | hop-budget guard designed | Construct a chain reaching the budget; assert it stops + alerts at the limit |
| **Cross-lens loop** | Feature interacts with an `aiFeature` | If an AI effect feeds this automation's trigger (or vice versa), assert the combined chain terminates |

### Category 4: Control & Regression

| Check | Method | Trigger |
|-------|--------|---------|
| **Kill-switch effectiveness** | Flip the kill switch; fire the trigger; assert the automation does NOT execute | Always for `unattended` |
| **Reversibility** | Perform an automated action; invoke the undo; assert original state restored | AC specifies reversibility |
| **Throughput regression** | Compare current throughput/latency against the stored baseline | Regression run |
| **Behavior regression** | Compare current outcomes against the baseline on a fixed input set | After logic/guard changes |

### Category 5: Agentic Loop Test (when the feature carries the `agentic` block)

Applies when `agentic.agenticProfile: true`. This tests the agent's **deliberate reasoning loop** — a different loop from the accidental event cycle in Category 3. Category 3 asks "does the event chain across features terminate?"; this asks "does the agent's own per-task reason→act loop terminate within its budget?"

| Check | Applies when | What it tests |
|-------|-------------|---------------|
| **Reasoning-loop termination** | Always (agentic) | Start a task — including a deliberately hard / looping input; **assert the loop terminates within its step + wall-clock budget** and does not spin |
| **Cost-ceiling termination** | Cost ceiling defined | Drive a task toward the cost ceiling; assert the loop hard-stops and escalates at the ceiling (not merely warns) |
| **Exhaustion → escalation** | Always (agentic) | Force exhaustion; assert the agent stops cleanly and hands off to the escalation path — no silent whole-task retry, no partial-commit |

Agentic findings are reported in the same `atq-findings.json` array (threaded by `aiFeatureId` + `automationFeatureId`).

---

## Output

Results written to `.tge/automation-lens/`:

```
.tge/automation-lens/
├── atq-report-{date}.md          ← Full quality report (human-readable)
├── atq-findings.json             ← Machine-readable findings for dashboard/DFE
├── baselines/                     ← Stored behavior/throughput baselines
│   └── AUTO-{NNN}-baseline.json
└── test-results/                  ← Raw test-run results
    └── AUTO-{NNN}-{date}.json
```

### Report Format

```markdown
# Automation Quality Report — {date}

**Agent:** AIFLC Automation Quality (ATQ__)
**Manifest version:** {from manifest}
**Features verified:** {count}

## Summary
| Feature | Correctness | Reliability | Loop | Overall |
|---------|-------------|-------------|------|---------|
| AUTO-001 | PASS | PASS | TERMINATES | PASS |
| AUTO-002 | PASS | DEGRADED | TERMINATES | WARNING |

## Per-Feature Detail

### {Feature name} (AUTO-{NNN}) — {pattern} / {sub-mode}

**Correctness:**
| Criterion | Result | Detail |
|-----------|--------|--------|
| Straight-through rate | {%} vs {target} | PASS / FAIL |
| SLA (p95) | {ms} vs {bound} | PASS / FAIL |

**Reliability:**
| Test | Result | Findings |
|------|--------|----------|
| Idempotency | PASS/FAIL | {detail} |
| Exception path | PASS/FAIL | {detail} |
| Rollback/compensation | PASS/FAIL | {detail} |

**Loop Test:**
| Test | Result | Detail |
|------|--------|--------|
| Loop termination | TERMINATES / BUDGET-EXCEEDED / UNTESTED | {hops observed} |

## Recommendations
{prioritized list}
```

---

## Severity Model

| Verdict | Meaning | Action |
|---------|---------|--------|
| **PASS** | Meets acceptance criteria; guards work | None — feature is healthy |
| **DEGRADED** | Below target but above critical; or a non-critical guard weakness | Investigate; remediate within sprint |
| **FAIL** | Critical defect — idempotency broken, exception path lost, or **loop does not terminate** | Block release; immediate action |

**Escalation rule:** a failed **loop termination** test — event-cycle (Category 3) *or* agentic reasoning-loop (Category 5) — or a failed **idempotency** test, is ALWAYS FAIL — never downgrade. These are the defects that cause the worst production incidents for automation.

---

## Layering (Three Altitudes)

| Altitude | Package | Responsibility |
|----------|---------|---------------|
| **Design** | AI-ADLC | Designs idempotency, retry/compensation, and loop guards |
| **Enforce** | AI-GCE (`ATG__`) | Enforces that the guards + audit exist in the implementation |
| **Operate** | AI-TGE (`ATQ__`) | Operates the tests — proves idempotency holds, loops terminate, exceptions are handled |

`ATQ__` is the operational instrument; `ATG__` is the governance check; ADLC designed both.

---

## Automation (v1 vs future)

| Version | Behavior |
|---------|----------|
| **v1 (current)** | Manual trigger only (`ATQ__`). User invokes when ready. No auto-firing. |
| **v2 (deferred)** | Scheduled runs (CI/CD integration, post-deploy hooks). |

---

## Related

- **AUTOMATION_LENS_PROTOCOL.md** §6.2 (AI-TGE contract)
- **AI-GCE `ATG__`** — the governance counterpart (`ATQ__` = quality/verification)
- **AI-DWG `.automation-lens/manifest.json`** — the couriered context (incl. guards + the `agentic` block) this agent reads
- **`automation-lens/architecture/reliability.md` + `loop-guards.md`** — the design rules this agent tests
- **`agentic-lens/architecture/reasoning-loop.md` + `agent-cost.md`** — the design rules the agentic loop test (Category 5) verifies

---

*AIFLC Automation Quality Agent v1.0.0 | Trigger: ATQ__ | Owner: AI-TGE | Author: Maheri*
