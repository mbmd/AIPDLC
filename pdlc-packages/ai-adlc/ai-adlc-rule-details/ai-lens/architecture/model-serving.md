# AI Architecture Rules — Model & Serving

> Sub-module of the AI-LENS ADLC facet. Loaded on demand when designing model selection and serving architecture for an AI feature.
> **Sub-role:** `#persona-subrole-ai-engineer`

---

## Decision Framework

### 1. Model Source Selection

| Option | When to choose | Trade-offs |
|--------|---------------|------------|
| **Managed API** (OpenAI, Anthropic, Bedrock, Vertex) | Commodity capabilities (generation, summarization, classification); team lacks ML infra skills; time-to-market priority | Vendor dependency; data leaves boundary; per-token cost scales with volume |
| **Self-hosted open-source** (Llama, Mistral, Falcon) | Data sovereignty requirements; predictable cost at scale; customization needed | Infra burden; GPU procurement; ops responsibility; slower iteration |
| **Fine-tuned** (base + domain data) | Domain-specific quality is insufficient with prompting alone; custom vocabulary or style required | Training pipeline; eval before/after; ongoing retraining |
| **From-scratch training** | Rare — novel domain with no applicable foundation model | Highest cost/time; requires ML research team; almost never justified for enterprise features |

### 2. Serving Pattern

| Pattern | Latency | Use when |
|---------|---------|----------|
| **Synchronous** (request-response) | < 3s target | User waits for result (suggestion panel, inline assist) |
| **Streaming** (SSE/WebSocket) | First-token < 500ms | Long-form generation; user sees progressive output |
| **Batch** (offline) | Minutes–hours | Nightly processing, bulk classification, report generation |
| **Async-queue** (background + notify) | Seconds–minutes | Heavy computation; user doesn't block; notified when ready |

### 3. Scaling Model

| Strategy | Description | Choose when |
|----------|-------------|-------------|
| **Auto-scale** | Inference replicas scale with traffic | Variable load; cost tracks usage |
| **Fixed capacity** | Reserved GPU/instances | Predictable load; cost certainty; latency-sensitive |
| **Serverless inference** | Pay-per-invocation (Bedrock, SageMaker Serverless) | Low-volume; cold-start acceptable |

### 4. Fallback Strategy

Every AI feature MUST have a defined fallback:
- **Primary → fallback provider** (e.g. Anthropic → Bedrock)
- **Primary → degraded mode** (e.g. full model → smaller/cheaper model)
- **Primary → non-AI path** (feature still works without AI; maps to UXD fallback UX)

Document the fallback chain in the ADR.

---

## ADR Triggers (produce an ADR when…)

- Model vendor selected
- Serving pattern chosen (especially if non-obvious — streaming, async)
- Fallback strategy defined
- Self-hosted vs managed decision
- Fine-tuning decision
- Multi-model composition (ensemble, routing, cascading)

---

## Anti-Patterns

- Choosing self-hosted without confirmed GPU budget and ops capacity.
- No fallback defined ("if the API is down, the feature breaks").
- Selecting a model based on benchmarks alone without domain-specific eval.
- Synchronous serving with no timeout/circuit-breaker.

---

*Model & Serving Rules v1.0.0 | AI-LENS ADLC Sub-Module*
