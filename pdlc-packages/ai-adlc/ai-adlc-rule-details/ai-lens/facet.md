# AI-LENS Facet — AI-ADLC

> **Loaded by the lens seam** when `Lens_Status.md` AI-LENS row = `AI-Powered`.
> **Integration points:** `design/component-design.md` + `design/data-architecture.md` + `design/integration-infrastructure.md` + `decisions/`.
> **Persona:** CTO / Chief Architect (primary; sub-roles per domain: `#persona-subrole-ai-engineer` for model-serving / data-RAG / MLOps / responsible-AI, `#persona-subrole-data-architect`, `#persona-subrole-security-architect`).

---

## Purpose

Design the **AI architecture** for every `aiFeature`-tagged item. This is the confirmed gap-closer: no AI/ML architecture module existed in AI-ADLC before AI-LENS. For each AI feature, this facet covers model & serving, data & RAG, MLOps/LLMOps, responsible-AI architecture, AI cost architecture, and AI security — producing architecture decisions (ADRs) and design artifacts.

This is the **largest facet** in the AI-LENS family. It delegates its deep rules to the `ai-lens/architecture/` sub-module (loaded on demand per domain).

---

## Guardrail

This facet operates strictly within the CTO / Architect's lane:
- Design **how** AI features are architecturally realized (model, data, infrastructure, operations, safety).
- DO NOT identify or classify features (AI-POLC did that).
- DO NOT design user interaction patterns (AI-UXD did that).
- DO NOT provision the workspace (AI-DWG will consume these decisions).
- DO NOT enforce governance rules at runtime (AI-GCE `AIG__`).

---

## When This Facet Fires

For each `aiFeature`-tagged item (from PBP + UXP), during the Design phase:
1. **Component design** — model & serving architecture
2. **Data architecture** — data/RAG/vector/embedding/feature-store
3. **Integration/infrastructure** — model APIs, streaming, async patterns, GPU infra
4. **Decisions** — one ADR per material AI architecture decision

---

## Inputs Consumed

| Source | What to read | Key fields |
|--------|-------------|------------|
| PBP (AI-POLC) | Tagged epics/stories | `aiFeatureId`, `aiSubMode`, `aiCapability`, `aiAcceptanceCriteria[]` |
| UXP (AI-UXD) | AI interaction design | `aiInteractionModel`, `aiHitlLevel`, latency requirements |
| PIP (AI-PILC) | Feasibility + EU AI Act | `aiFeasibility`, `aiCostModel`, `euAiActClass` |

---

## Architecture Domains (6)

Each domain has deep rules in the `ai-lens/architecture/` sub-module. The facet orchestrates; the sub-module provides the detailed design guidance per domain.

| # | Domain | Sub-module file | Produces |
|---|--------|-----------------|----------|
| 1 | Model & Serving | `architecture/model-serving.md` | Model selection, hosting strategy, latency/scaling, batching |
| 2 | Data & RAG | `architecture/data-rag.md` | Datasets, vector DB, embeddings, feature store, versioning, knowledge base |
| 3 | MLOps / LLMOps | `architecture/mlops.md` | Model versioning, prompt versioning, drift detection, retraining, rollback, A/B |
| 4 | Responsible AI | `architecture/responsible-ai.md` | Guardrails, bias mitigation, HITL enforcement, moderation, model cards |
| 5 | AI Cost Architecture | `architecture/cost.md` | Token budgets, inference caps, cost attribution, usage monitoring, alerts |
| 6 | AI Security | `architecture/security.md` | Prompt injection, data poisoning, output filtering, PII boundary, red-teaming |

---

## Step 1: Per-Feature Architecture Pass

For each AI feature (by `aiFeatureId`), run through the 6 domains:

### 1.1 Model & Serving

`Read` → `ai-lens/architecture/model-serving.md`

Decide and document:
- **Model source:** managed API (OpenAI, Anthropic, Bedrock, etc.) vs. self-hosted (open-source) vs. fine-tuned vs. from-scratch
- **Serving pattern:** synchronous (request-response) vs. streaming vs. batch vs. async-queue
- **Scaling model:** auto-scale, fixed capacity, serverless inference
- **Latency target:** derived from POLC's acceptance criteria + UXD's interaction model
- **Fallback strategy:** primary + fallback provider, graceful degradation on failure

**ADR trigger:** every material model selection decision produces an ADR.

### 1.2 Data & RAG

`Read` → `ai-lens/architecture/data-rag.md`

Decide and document:
- **Knowledge source:** retrieval corpus, structured DB, knowledge graph, combination
- **Vector store:** choice + embedding model + chunk strategy + update cadence
- **Feature store** (if applicable): feature engineering, serving, freshness
- **Data versioning:** how training data and knowledge bases are versioned
- **Data quality:** validation pipeline, monitoring, freshness alerts

### 1.3 MLOps / LLMOps

`Read` → `ai-lens/architecture/mlops.md`

Decide and document:
- **Model/prompt versioning:** how model versions and prompt templates are tracked
- **Evaluation pipeline:** offline eval (golden sets), online metrics, quality gates
- **Drift detection:** what triggers retraining/re-prompting (statistical thresholds, quality drop)
- **Rollback:** how to revert to a previous model/prompt version safely
- **A/B / canary:** experimentation infrastructure for model changes

### 1.4 Responsible AI

`Read` → `ai-lens/architecture/responsible-ai.md`

Decide and document:
- **Guardrails:** input/output filtering, topic restriction, safety boundaries
- **Bias mitigation:** testing approach, fairness metrics, monitoring
- **Explainability:** what degree of explanation the system provides (aligns with UXD disclosure)
- **HITL enforcement:** architectural controls that ensure the HITL level from UXD is technically enforced (not just UX)
- **Model card:** maintain a living model card documenting capabilities, limitations, intended use, bias testing results

**EU AI Act high-risk:** if PILC classified a feature as `high`, this domain produces the mandatory risk-management and human-oversight architecture.

### 1.5 AI Cost Architecture

`Read` → `ai-lens/architecture/cost.md`

Decide and document:
- **Token/inference budgets:** per-request and daily/monthly caps
- **Cost attribution:** how AI costs are attributed to features/teams/tenants
- **Usage monitoring:** real-time dashboards, alerting thresholds
- **Cost controls:** rate limiting, token truncation, cheaper-model fallback at budget ceiling

### 1.6 AI Security

`Read` → `ai-lens/architecture/security.md`

Decide and document:
- **Prompt injection mitigation:** input sanitization, delimiter enforcement, output validation
- **Data poisoning prevention:** training/knowledge-base integrity controls
- **PII boundary:** what data can/cannot reach the model; redaction strategy
- **Output filtering:** content safety, hallucination guardrails, format enforcement
- **Red-teaming plan:** adversarial testing scope and cadence

---

## Step 2: Produce ADRs

For each material decision across the 6 domains, produce an Architecture Decision Record:

```markdown
# ADR-{NNN}: {Decision Title}

**Status:** Accepted
**Date:** {date}
**Feature:** AIF-{NNN} ({feature name})
**Domain:** {model-serving | data-rag | mlops | responsible-ai | cost | security}

## Context
{Why this decision is needed — reference the capability, acceptance criteria, and constraints}

## Options Considered
1. {Option A} — {pros/cons}
2. {Option B} — {pros/cons}
3. {Option C} — {pros/cons}

## Decision
{Chosen option and rationale}

## Consequences
- {Positive consequence}
- {Negative consequence / accepted trade-off}
- {Follow-up required}
```

Tag each ADR with AI-LENS front-matter:
```yaml
---
aiFeature: true
aiFeatureId: AIF-{NNN}
aiSubMode: {value}
aiCapability: {value}
---
```

---

## Step 3: Record Architecture Summary

For each AI feature, record a compact architecture summary in the AP:

```markdown
## AI Architecture — {feature name} (AIF-{NNN})

| Domain | Decision | ADR |
|--------|----------|-----|
| Model & Serving | {e.g. Managed API (Anthropic Claude) + fallback (Bedrock)} | ADR-{N} |
| Data & RAG | {e.g. Vector DB (Pinecone) + resolved-ticket KB, chunked 512 tokens} | ADR-{N} |
| MLOps | {e.g. Prompt-versioned in git, weekly eval against golden set} | ADR-{N} |
| Responsible AI | {e.g. Guardrails: topic filter + PII redaction + model card} | ADR-{N} |
| Cost | {e.g. Token-metered, 50K tokens/day cap, Bedrock fallback at 80% budget} | ADR-{N} |
| Security | {e.g. Prompt-injection: delimiter + output validation; PII: redact before prompt} | ADR-{N} |
```

---

## Sub-Mode Calibration

| Sub-mode | Architecture depth |
|----------|-------------------|
| `opportunity` | Light: managed API, minimal MLOps, basic guardrails. Aim for fast, low-risk deployment. |
| `augmented` | Full: all 6 domains designed comprehensively. Strategic investment — engineer for quality and scale. |
| `native` | Mandatory full + RAI + EU AI Act high-risk compliance architecture. The feature's existence depends on the AI working correctly. |

---

## What This Facet Does NOT Do

- Does not identify or tag AI features (AI-POLC).
- Does not design user interaction patterns (AI-UXD).
- Does not generate workspace scaffolding (AI-DWG reads these decisions).
- Does not enforce rules at runtime (AI-GCE `AIG__`).
- Does not evaluate quality or detect drift (AI-TGE `AIQ__`).
- Does not write product-level acceptance criteria (reads them from POLC).

---

*AI-LENS ADLC Facet v1.0.0 | Integration: Design phase (component + data + integration + decisions) | Author: Maheri*
