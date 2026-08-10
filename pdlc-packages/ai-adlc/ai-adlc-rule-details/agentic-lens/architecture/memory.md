# Agentic Architecture — Memory

> **Sub-module of** `agentic-lens/facet.md`. Loaded on demand when designing what the agent remembers, for how long, and under what controls.
> **Sub-role:** `#persona-subrole-data-architect`
> **Reuses from (do not re-document):** grounding retrieval (vector store, embeddings, chunking, knowledge base) from `ai-lens/architecture/data-rag.md`; the PII boundary and redaction strategy from `ai-lens/architecture/security.md`. This file designs **agent memory**, which is a distinct concern from RAG grounding.

---

## Memory is not RAG

Retrieval-for-grounding (RAG) answers *"what does the knowledge base say about X?"* — it is designed in `ai-lens/architecture/data-rag.md`. **Agent memory** answers *"what has this agent seen, decided, and done — in this task and across tasks?"* They may share infrastructure (a vector store), but they are different design concerns with different retention, ownership, and privacy properties. Do not fold one into the other.

---

## Decision Framework

### 1. Memory Tiers

| Tier | Scope | Lifetime | Typical backing |
|------|-------|----------|-----------------|
| **Scratchpad (short-term)** | One task / one loop run | Ephemeral — discarded at task end | In-context / working buffer |
| **Episodic (long-term)** | Past task instances ("what happened last time") | Persisted; retention-governed | Store keyed by task/entity + time |
| **Semantic (long-term)** | Distilled facts/preferences the agent accumulates | Persisted; retention-governed | Vector or key-value store |

**Design rule:** start with scratchpad only. Add episodic/semantic memory **only when a requirement needs cross-task recall** — long-term memory is a privacy and correctness liability, not a default feature.

### 2. Read / Write Policy

For each tier, define explicitly:

| Question | Why it matters |
|----------|----------------|
| **What is written?** | Uncontrolled writes grow unbounded and capture things they shouldn't |
| **When is it written?** | End-of-step, end-of-task, or on an explicit "remember" action |
| **What is read back, and when?** | Reading stale/irrelevant memory degrades decisions |
| **Who can read it?** | Cross-task/cross-user memory is a data-boundary decision (see §5) |
| **How is it invalidated?** | Memory that is never invalidated becomes wrong over time |

### 3. Context-Window Management

The scratchpad competes with grounding, tool schemas, and reasoning for a finite context window.

| Technique | Use when |
|-----------|----------|
| **Truncation / recency window** | Keep the last N steps; drop the oldest | Default for bounded tasks |
| **Summarization / compaction** | Summarize older steps into a compact state as the window fills | Long tasks that exceed the window |
| **Selective retrieval** | Keep the working set small; retrieve older detail on demand | When most history is irrelevant most of the time |

**Design rule:** define the behavior **before** the window overflows. An agent whose context silently overflows loses the earliest (often the goal-defining) content.

### 4. Retention

| Tier | Retention decision |
|------|-------------------|
| Scratchpad | Discarded at task completion; never persisted beyond the run unless explicitly promoted to episodic |
| Episodic / Semantic | Explicit retention period tied to purpose; a defined deletion mechanism; honored subject-deletion requests |

Retention that cannot be enforced (no deletion mechanism) is not a policy. Record the retention period and the deletion mechanism in the ADR.

### 5. PII Boundary (binds to AI security)

Long-term memory is a **standing store of potentially personal data** — it inherits the PII boundary from `ai-lens/architecture/security.md`.

**Design requirements:**
- **Do not persist PII into long-term memory** unless a requirement demands it and the retention/deletion controls exist.
- **Redact before write** — apply the same redaction the security sub-module defines for prompts, at the memory-write boundary.
- **Scope memory to its subject** — per-user memory must not leak across users; a multi-tenant agent must scope memory by tenant (the data-boundary rule from `automation-lens/architecture/actor-identity.md` §6 applies).
- **Subject deletion must reach memory** — a "delete my data" request must purge episodic/semantic memory, not just the primary store.

### 6. Consistency with Reasoning & Tools

- Memory writes are part of the reasoning trace (`reasoning-loop.md`) — what the agent chose to remember is auditable.
- Memory is **not** a bypass for tool permissions — an agent cannot "remember" a capability it isn't permitted to call.
- Treat retrieved long-term memory as **input to validate**, not trusted fact — poisoned or stale memory is a correctness and injection risk.

---

## ADR Triggers

- Introducing any long-term (episodic or semantic) memory tier
- The read/write policy for a persisted tier
- Context-window management strategy for long tasks
- Retention period + deletion mechanism for persisted memory
- PII handling in memory (what may be stored, redaction, subject deletion)

---

## Handoff to Layer 3

AI-DWG provisions the **memory store(s)** (reusing the vector infrastructure from `ai-lens/architecture/data-rag.md` where shared), the retention/deletion configuration, and the redaction hook at the write boundary.

`AIG__` (AI-GCE) verifies PII controls and retention in the implementation; subject-deletion coverage is checked against the store. `AIQ__` (AI-TGE) may assert memory scoping (no cross-user/tenant bleed).

---

## Anti-Patterns

- **Persisting the whole scratchpad by default** — unbounded growth + a privacy liability nobody asked for.
- **Treating memory as RAG (or vice versa)** — different retention, ownership, and privacy; design them separately even if they share a store.
- **No context-overflow strategy** — the goal falls out of the window first.
- **PII in long-term memory with no deletion mechanism** — a standing compliance breach.
- **Cross-user / cross-tenant memory bleed** — one agent instance leaks another subject's data.
- **Trusting retrieved memory as fact** — stale or poisoned memory drives wrong actions.
- **Long-term memory "because agents have memory"** — add it for a requirement, not for completeness.

---

*Agentic Architecture Sub-Module — Memory | v1.0.0 | Intersection facet (AI Lens ∩ Automation Lens)*
