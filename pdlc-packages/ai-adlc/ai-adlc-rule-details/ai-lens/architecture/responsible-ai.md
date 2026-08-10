# AI Architecture Rules — Responsible AI

> Sub-module of the AI-LENS ADLC facet. Loaded on demand when designing responsible-AI architecture for an AI feature.
> **Sub-role:** `#persona-subrole-ai-engineer`

---

## Decision Framework

### 1. Guardrails Architecture

| Layer | Purpose | Implementation options |
|-------|---------|----------------------|
| **Input guardrails** | Filter/reject harmful, out-of-scope, or injection-attempt inputs | Classifier pre-filter, regex blocklist, topic-scope enforcement |
| **Output guardrails** | Filter/block harmful, off-topic, or policy-violating outputs | Output classifier, content safety API, format enforcement |
| **Topic restriction** | Constrain the model to its intended domain | System prompt boundaries + topic classifier + rejection response |
| **Retrieval guardrails** | Ensure retrieved context is appropriate | Source filtering, freshness gate, PII scan on retrieval results |

### 2. Bias Mitigation

| Activity | Approach |
|----------|----------|
| **Testing** | Run eval on diverse demographic slices; measure performance disparity across groups |
| **Fairness metrics** | Demographic parity, equalized odds, calibration — select based on domain ethics |
| **Monitoring** | Ongoing bias monitoring on live traffic (disaggregated metrics) |
| **Mitigation** | Prompt debiasing, balanced training data, post-processing calibration |

### 3. Explainability

| Level | What the user sees | When required |
|-------|-------------------|---------------|
| **Attribution** | "Based on {source documents}" (RAG citation) | Any RAG-based feature |
| **Confidence** | Quality/certainty signal (designed at UXD; architecturally supported here) | All user-facing AI output |
| **Reasoning trace** | Chain-of-thought or rationale visible to the user | High-stakes decisions; EU AI Act high-risk |
| **None** | No explanation provided | Internal, low-stakes, fully autonomous features only |

### 4. HITL Enforcement (Architectural)

The HITL level defined by UXD must be **architecturally enforced**, not just a UX convention:

| Level | Architectural control |
|-------|----------------------|
| `review-before-action` | API does NOT execute actions; returns proposed actions; separate "confirm" endpoint required |
| `edit-after` | Actions execute but are reversible; undo endpoint + audit trail + time-window enforcement |
| `monitor-only` | Actions execute and log; alert pipeline for anomalies; human escalation path |
| `autonomous` | Full execution; periodic audit report; override via configuration |

### 5. Model Card

Every AI feature with sub-mode `augmented` or `native` MUST maintain a living model card:

```markdown
## Model Card — {feature name} (AIF-{NNN})

- **Model:** {name, version, provider}
- **Intended use:** {what this model does in this feature}
- **Limitations:** {known failure modes, edge cases}
- **Training data:** {description, date range, size, known biases}
- **Evaluation results:** {latest eval scores on golden set}
- **Bias testing:** {last tested, results, known disparities}
- **Responsible-AI controls:** {guardrails applied, HITL level}
- **Last updated:** {date}
```

### 6. EU AI Act High-Risk Architecture

If PILC classified a feature as `high` (EU AI Act), this domain MUST produce:
- **Risk management system:** documented risk identification, mitigation, residual-risk acceptance
- **Human oversight architecture:** technical mechanisms ensuring meaningful human control
- **Data governance:** training data documentation, quality metrics, bias assessment
- **Transparency:** technical documentation sufficient for conformity assessment
- **Accuracy monitoring:** ongoing performance measurement with defined thresholds

---

## ADR Triggers

- Guardrails approach chosen (what's blocked at input vs output)
- Bias mitigation strategy defined
- Explainability level decided
- HITL enforcement mechanism designed
- EU AI Act high-risk conformity architecture designed
- Model card policy established

---

## Anti-Patterns

- Relying on the system prompt alone for safety (prompt jailbreaks exist; use a classifier layer).
- "We'll add fairness testing later" (bias compounds; test from first deployment).
- HITL level in UX without architectural enforcement (a "confirm" button that doesn't actually gate the action).
- No model card for production AI features (invisible model risks).

---

*Responsible AI Rules v1.0.0 | AI-LENS ADLC Sub-Module*
