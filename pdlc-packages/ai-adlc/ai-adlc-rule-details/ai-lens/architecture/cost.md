# AI Architecture Rules — AI Cost Architecture

> Sub-module of the AI-LENS ADLC facet. Loaded on demand when designing cost controls and budget architecture for an AI feature.

---

## Decision Framework

### 1. Token / Inference Budgets

| Scope | What to define | Example |
|-------|---------------|---------|
| **Per-request** | Max tokens (input + output) per single invocation | 4096 tokens max per suggestion request |
| **Per-user/session** | Daily/hourly cap per user to prevent runaway usage | 50 requests/hour/user; 200K tokens/day/user |
| **Per-feature** | Monthly budget ceiling for the entire feature | $500/month max for the reply-suggestion feature |
| **System-wide** | Global daily/monthly spend cap across all AI features | $5,000/month total AI spend; hard-stop at ceiling |

### 2. Cost Attribution

| Model | Description | Use when |
|-------|-------------|----------|
| **Per-feature** | Each AI feature is a cost center; usage tracked independently | Multiple AI features with separate budgets/owners |
| **Per-tenant** | Multi-tenant system; each tenant's AI usage billed separately | SaaS with per-tenant pricing or fair-use policies |
| **Per-team** | Internal teams own their AI budget | Enterprise with team-level cost accountability |
| **Blended** | AI costs distributed across all users (part of platform cost) | Small-scale or early-stage; not worth fine-grained tracking |

### 3. Usage Monitoring

- **Real-time dashboard:** tokens consumed, requests/minute, cost accumulation (current vs budget)
- **Alerting thresholds:** warn at 70%, alert at 90%, hard-stop at 100% of budget
- **Granularity:** per-feature, per-tenant, per-model breakdown

### 4. Cost Control Mechanisms

| Control | Effect | When to apply |
|---------|--------|---------------|
| **Rate limiting** | Cap requests/minute per user or globally | Prevent burst-spend from automation or abuse |
| **Token truncation** | Limit context window or max output length | Reduce per-request cost at slight quality trade-off |
| **Cheaper-model fallback** | Route to a smaller/cheaper model when budget ceiling approaches | Maintain availability at reduced quality/cost |
| **Caching** | Cache identical or similar requests; serve cached response | Repeated queries (FAQ, common classifications) |
| **Batch consolidation** | Aggregate low-priority requests and process in bulk (cheaper batch pricing) | Non-latency-sensitive operations (nightly summarization) |

### 5. Cost Scaling Analysis

For the ADR, model cost at multiple scales:

| Scale | Requests/day | Estimated cost/month | Viability |
|-------|-------------|---------------------|-----------|
| Pilot (10 users) | {estimate} | {estimate} | {viable / stretch / prohibitive} |
| Growth (100 users) | {estimate} | {estimate} | {viable / stretch / prohibitive} |
| Scale (1000+ users) | {estimate} | {estimate} | {viable / stretch / prohibitive} |

Flag any scale tier where cost becomes prohibitive — this is a risk for the PILC risk register.

---

## ADR Triggers

- Budget ceiling and enforcement strategy defined
- Cost attribution model chosen
- Cheaper-model fallback or caching introduced
- Per-tenant billing implications designed
- Cost-prohibitive scale identified (risk escalation)

---

## Anti-Patterns

- No per-feature budget (all AI spend is one opaque number; can't manage individual features).
- Hard-stop without graceful degradation (user sees an error instead of a cheaper fallback).
- Cost projections at current scale only (no growth scenario; budget surprises at scale).
- Caching without invalidation strategy (stale responses when knowledge changes).

---

*AI Cost Architecture Rules v1.0.0 | AI-LENS ADLC Sub-Module*
