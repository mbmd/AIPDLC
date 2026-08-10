# AI Architecture Rules — MLOps / LLMOps

> Sub-module of the AI-LENS ADLC facet. Loaded on demand when designing model lifecycle operations for an AI feature.
> **Sub-role:** `#persona-subrole-ai-engineer`

---

## Decision Framework

### 1. Model / Prompt Versioning

| Approach | When to use |
|----------|-------------|
| **Git-versioned prompts** | LLM-based features using prompt engineering; prompts are code | Most common for managed-API features |
| **Model registry** (MLflow, SageMaker Model Registry, Weights & Biases) | Self-hosted or fine-tuned models; need rollback + staging + production slots | Required for fine-tuned/trained models |
| **Prompt management platform** (Langsmith, Humanloop, custom) | High prompt iteration velocity; need A/B + analytics + team collaboration | Teams iterating prompts frequently |

### 2. Evaluation Pipeline

| Layer | What it checks | Cadence |
|-------|----------------|---------|
| **Offline eval (golden sets)** | Quality against labeled ground-truth examples | On every prompt/model change before promotion |
| **Online metrics** | Live quality signals (user feedback, implicit signals, error rates) | Continuous (real-time dashboards) |
| **Quality gates** | Automated pass/fail on eval metrics before deployment | CI/CD integration — block promotion below threshold |

### 3. Drift Detection

| Signal | Detection method | Response |
|--------|-----------------|----------|
| **Data drift** | Statistical tests on input distribution (KL divergence, PSI) | Alert → investigate → retrain if confirmed |
| **Output quality drift** | Eval score degradation over time (rolling window) | Alert → eval run → rollback or retrain |
| **Prompt effectiveness decay** | Declining acceptance rate or user overrides increasing | Alert → prompt revision cycle |

### 4. Rollback Strategy

- **Managed API:** revert prompt version in version control; deploy previous prompt template
- **Self-hosted model:** model registry points production slot to previous version; blue/green or canary rollback
- **Rollback trigger:** eval score below threshold, spike in user-reported errors, safety incident

### 5. Experimentation (A/B / Canary)

| Pattern | Use when |
|---------|----------|
| **A/B test** | Comparing two prompt/model variants on user quality metrics | Feature-flag controlled; statistical significance required before winner declared |
| **Canary release** | Gradual rollout of a new model version (1% → 10% → 50% → 100%) | Risk mitigation for model changes; auto-rollback on metric degradation |
| **Shadow mode** | New model runs in parallel but output not shown to users; compare offline | Validating a new model before any user exposure |

---

## ADR Triggers

- Versioning approach chosen (git prompts vs model registry vs platform)
- Evaluation pipeline designed (what metrics, what thresholds)
- Drift detection strategy defined
- A/B or canary infrastructure introduced
- Retraining trigger policy established

---

## Anti-Patterns

- Deploying prompt changes without offline eval ("it worked in testing" is not eval).
- No rollback plan (a bad model release with no revert path).
- Drift detection without a defined response (alerting without action).
- Manual-only model promotion (no quality gates in the pipeline).

---

*MLOps / LLMOps Rules v1.0.0 | AI-LENS ADLC Sub-Module*
