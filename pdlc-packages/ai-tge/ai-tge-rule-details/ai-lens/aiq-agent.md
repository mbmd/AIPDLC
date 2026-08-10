# AIFLC AI Quality & Drift — Agent Template

> **Trigger:** `AIQ__` (manual invocation)
> **Owner:** AI-TGE
> **Type:** Audit
> **Core impact:** None — the TGE core stays AI-agnostic. This agent is invoked manually by the user.
> **Dependency:** OI-200 (engine agnostic agent-hosting capability). Built against documented interface; final integration pending OI-200 delivery.

---

## Purpose

Evaluate AI feature quality and detect drift, using the couriered AI-feature context from `{slug}-workspace/.ai-lens/manifest.json` and the project's evaluation infrastructure (`eval/`). Writes results into `.tge/`.

This is the **test half** of the govern+test bracket around the (un-lensed) builder. It checks that AI features meet their acceptance criteria, evaluates quality, and monitors for drift — across any build engine (AI-DLC v1, spec-driven, freestyle).

---

## When to Invoke

- After initial AI feature implementation (first quality baseline)
- After model/prompt changes (regression check)
- After knowledge base updates (RAG quality check)
- Before release (final quality gate)
- Periodically during production (drift monitoring — weekly/monthly depending on feature criticality)

---

## Consequences of Skipping

- AI features ship without quality evidence (no eval baseline)
- Model drift goes undetected (quality degrades silently over time)
- Acceptance criteria from POLC are never validated against real output
- Hallucination, bias, and safety risks go untested
- No regression baseline — model/prompt changes cannot be compared

---

## Recovery

If `AIQ__` has not been run and quality is unknown:
1. Run `AIQ__` in **baseline mode** to establish current quality
2. Run against the golden set to produce initial scores
3. Document the baseline in `.tge/ai-lens/` for future comparison
4. Schedule recurring runs

---

## Input

Reads from `{slug}-workspace/.ai-lens/manifest.json` (the couriered context):
- Feature list with `aiFeatureId`, `aiSubMode`, `aiCapability`
- Acceptance criteria (quality thresholds, confidence bounds, safety constraints)
- Architecture decisions (model strategy — needed to know what to test)
- The `agentic` block (when present) — tool registry, loop termination + cost ceiling, task-completion definition — needed for the agentic check-set (Category 4)

Also reads from the live workspace:
- `eval/` directory (golden sets, eval scripts, existing baselines)
- `.tge/ai-lens/` previous results (for drift comparison)
- AI output logs (if available — for real-traffic quality sampling)

---

## Checks Performed

### Category 1: Evaluation Harness (Quality)

| Check | Method | Produces |
|-------|--------|----------|
| **Golden-set evaluation** | Run the AI feature against a labeled golden dataset; score on task-specific metrics | Quality scores (accuracy, relevance, faithfulness, etc.) |
| **Acceptance criteria validation** | Compare eval scores against POLC's AI acceptance criteria thresholds | PASS / FAIL per criterion |
| **Statistical acceptance** | For non-deterministic output: run N times; report confidence intervals | Mean score ± CI; pass if lower bound ≥ threshold |

### Category 2: Risk-Based Testing

| Check | Applies when | What it tests |
|-------|-------------|---------------|
| **Hallucination detection** | RAG/generation features | Does the output contain claims not grounded in the provided context? |
| **Bias evaluation** | `aiSubMode` = `augmented` or `native` | Output quality disparity across demographic slices |
| **Prompt injection resilience** | All user-facing AI features | Can adversarial inputs bypass system constraints? |
| **Red-team scenarios** | `aiSubMode` = `native` | Systematic adversarial testing per the security plan |
| **Robustness (edge cases)** | All AI features | Behavior on empty input, maximum-length input, unusual format, unsupported language |

### Category 3: Drift Monitoring

| Check | Method | Trigger |
|-------|--------|---------|
| **Quality drift** | Compare current eval scores against the stored baseline | Score drops below threshold → alert |
| **Output distribution shift** | Statistical comparison of output characteristics over time | KL divergence or PSI exceeds threshold → investigate |
| **Acceptance rate decline** | Track user acceptance/rejection rate of AI suggestions | Declining trend over N-day window → flag |
| **Latency drift** | Monitor response time trends | P95 exceeds target from POLC AC → alert |

### Category 4: Agentic Evaluation (when the feature carries the `agentic` block)

Applies only when the manifest entry carries `agentic.agenticProfile: true` — a feature that both reasons and acts autonomously. Evaluates the **trajectory**, not just single-shot output (a correct final answer reached via an unsafe or wasteful path is still a defect).

| Check | Method | Produces |
|-------|--------|----------|
| **Trajectory evaluation** | Run the agent on an agent-scenario set (incl. adversarial/looping inputs); score each step for validity, path efficiency vs. the step budget, and path safety | Trajectory scores + unsafe-step flags |
| **Task-completion evaluation** | Measure against the POLC task-completion definition: completion rate, escalation rate (a correct hand-off is a success, not a failure), and **false-completion** (declared done but not done) | Completion metrics; false-completion weighted heaviest |
| **Tool-call accuracy** | Assert the agent picked the right tool with schema-valid arguments and validated tool output before acting | Tool-call accuracy rate |

Agentic findings are reported in the same `aiq-findings.json` array (threaded by `aiFeatureId` + `automationFeatureId`) — no separate agentic result file.

---

## Output

Results written to `.tge/ai-lens/`:

```
.tge/ai-lens/
├── aiq-report-{date}.md          ← Full quality/drift report (human-readable)
├── aiq-findings.json             ← Machine-readable findings for dashboard/DFE
├── baselines/                     ← Stored quality baselines for drift comparison
│   └── AIF-{NNN}-baseline.json
└── eval-results/                  ← Raw evaluation run results
    └── AIF-{NNN}-eval-{date}.json
```

### Report Format

```markdown
# AI Quality & Drift Report — {date}

**Agent:** AIFLC AI Quality & Drift (AIQ__)
**Manifest version:** {from manifest}
**Features evaluated:** {count}

## Summary
| Feature | Quality | Drift | Overall |
|---------|---------|-------|---------|
| AIF-001 | PASS (87%) | STABLE | PASS |
| AIF-002 | DEGRADED (72%) | DRIFTING | WARNING |

## Per-Feature Detail

### {Feature name} (AIF-{NNN}) — {capability}

**Quality Scores:**
| Metric | Score | Threshold | Result |
|--------|-------|-----------|--------|
| {metric} | {value} | ≥ {threshold} | PASS / FAIL |

**Risk-Based Testing:**
| Test | Result | Findings |
|------|--------|----------|
| Hallucination | {n}/{total} grounded | {detail} |
| Bias | {disparity %} | {detail} |

**Drift Status:** {stable | drifting | critical}
| Signal | Current | Baseline | Delta |
|--------|---------|----------|-------|
| {metric} | {value} | {baseline} | {delta} |

## Recommendations
{prioritized list — e.g. "retrain", "update golden set", "investigate drift source"}
```

---

## Severity Model

| Verdict | Meaning | Action |
|---------|---------|--------|
| **PASS** | Quality meets thresholds; no drift detected | None — feature is healthy |
| **DEGRADED** | Quality below threshold but above critical; or early-stage drift | Investigate; schedule remediation within sprint |
| **FAIL** | Quality critically below threshold; or confirmed harmful output | Block release; immediate action required |
| **STABLE** | Drift status — no significant change from baseline | Continue monitoring |
| **DRIFTING** | Drift status — measurable decline trending toward threshold | Investigate root cause; consider retraining/re-prompting |
| **CRITICAL** | Drift status — below acceptable threshold; feature is degrading in production | Immediate action: rollback, retrain, or disable feature |

---

## Layering (Three Altitudes)

The AI feature's quality lifecycle spans three packages at different altitudes:

| Altitude | Package | Responsibility |
|----------|---------|---------------|
| **Design** | AI-ADLC | Designs the MLOps strategy (eval pipeline, drift detection, rollback) |
| **Enforce** | AI-GCE (`AIG__`) | Enforces that the designed obligations exist and are followed |
| **Operate** | AI-TGE (`AIQ__`) | Operates the actual tests, measures quality, detects drift |

`AIQ__` is the operational instrument; `AIG__` is the governance check; ADLC designed both.

---

## Automation (v1 vs future)

| Version | Behavior |
|---------|----------|
| **v1 (current)** | Manual trigger only (`AIQ__`). User invokes when ready. No auto-firing. |
| **v2 (deferred)** | Scheduled runs (CI/CD integration, post-deploy hooks). Requires OI-200 engine capability. |

---

## Related

- **AI_LENS_PROTOCOL.md** §6.2 (AI-TGE contract)
- **AI-GCE `AIG__`** — the governance counterpart (`AIQ__` = quality/drift; `AIG__` = compliance)
- **AI-DWG `.ai-lens/manifest.json`** — the couriered context this agent reads (incl. the `agentic` block)
- **`eval/`** — evaluation infrastructure generated by AI-DWG's facet
- **`agentic-lens/architecture/agent-eval.md` + `reasoning-loop.md`** — the design rules the agentic check-set (Category 4) evaluates
- **OI-200** — engine agnostic agent-hosting capability (build dependency)

---

*AIFLC AI Quality & Drift Agent v1.0.0 | Trigger: AIQ__ | Owner: AI-TGE | Author: Maheri*
