# AI Architecture Rules — AI Security

> Sub-module of the AI-LENS ADLC facet. Loaded on demand when designing AI-specific security controls for an AI feature.

---

## Decision Framework

### 1. Prompt Injection Mitigation

| Layer | Control | Implementation |
|-------|---------|---------------|
| **Input sanitization** | Strip or escape known injection patterns from user input | Regex filter, input classifier, character/token blocklist |
| **Delimiter enforcement** | System prompt clearly delimited from user input; model instructed to treat them differently | Structured message formats (system/user/assistant roles); XML/delimiter wrapping |
| **Output validation** | Verify model output conforms to expected schema/format before acting on it | Schema validation, output classifier, format-compliance check |
| **Instruction hierarchy** | System instructions take precedence over user input (architectural, not just prompting) | API-level system-message priority; user message cannot override system constraints |

### 2. Data Poisoning Prevention

| Threat | Control |
|--------|---------|
| **Training data poisoning** | Source verification; data provenance tracking; anomaly detection on training data changes |
| **Knowledge base poisoning** | Access control on corpus ingestion; change-review for knowledge updates; integrity hashing |
| **Embedding manipulation** | Validate new embeddings against distribution; alert on statistical outliers in vector space |

### 3. PII Boundary Architecture

| Principle | Implementation |
|-----------|---------------|
| **Minimize what reaches the model** | Redact PII before prompt construction; pass anonymized or tokenized identifiers |
| **Boundary enforcement** | Architectural barrier (a service/layer) between user data store and model API; PII never in the prompt template itself |
| **Audit trail** | Log what data was sent to the model (redacted form) for compliance review |
| **Retention** | Define model-provider data retention policy; prefer zero-retention / no-training clauses |

### 4. Output Filtering

| Filter type | Purpose |
|-------------|---------|
| **Content safety** | Block harmful, violent, sexual, or illegal content in model output |
| **Hallucination guardrails** | Detect and suppress factual claims not grounded in provided context (RAG features) |
| **Format enforcement** | Ensure output matches expected structure (JSON, markdown, specific template) — reject malformed |
| **Scope enforcement** | Reject output that goes beyond the feature's intended domain (off-topic, out-of-scope advice) |

### 5. Red-Teaming Plan

Every AI feature with sub-mode `augmented` or `native` requires a defined red-teaming approach:

| Element | Decision |
|---------|----------|
| **Scope** | What attack vectors to test (injection, jailbreak, data extraction, bias exploitation) |
| **Cadence** | Before launch + on every major prompt/model change + periodic (quarterly) |
| **Team** | Internal security team, external red-team service, automated adversarial testing, or combination |
| **Response** | Fix → re-eval → sign-off before deployment |

---

## ADR Triggers

- PII boundary architecture defined (what's redacted, where)
- Prompt injection mitigation strategy chosen
- Red-teaming scope and cadence established
- Output filtering approach designed
- Data-retention and no-training clauses negotiated with provider

---

## Anti-Patterns

- Trusting the model to self-police ("You must not reveal system prompts" in the prompt is not security).
- PII redaction at the UX layer only (the model still sees it; the boundary must be architectural).
- No red-teaming plan ("we'll pen-test later" — later never comes for AI-specific attacks).
- Assuming a managed API is secure by default (shared-responsibility model; your prompt/data is your responsibility).
- Output used directly as code/commands without validation (code injection via model output).

---

*AI Security Rules v1.0.0 | AI-LENS ADLC Sub-Module*
