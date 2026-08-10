# AI Architecture Rules — Data & RAG

> Sub-module of the AI-LENS ADLC facet. Loaded on demand when designing data strategy, retrieval-augmented generation, and knowledge infrastructure for an AI feature.
> **Sub-role:** `#persona-subrole-ai-engineer`

---

## Decision Framework

### 1. Knowledge Source Strategy

| Source type | When to use | Architecture implications |
|-------------|-------------|--------------------------|
| **Retrieval corpus (RAG)** | Feature needs grounded answers from a specific knowledge base | Vector DB + embedding pipeline + chunking strategy |
| **Structured database** | Feature queries structured data (SQL/NoSQL) for factual answers | Query generation or tool-use pattern; no embedding needed |
| **Knowledge graph** | Feature needs relationship reasoning (entity connections, paths) | Graph DB + entity extraction + graph traversal |
| **Direct context** (in-prompt) | Knowledge fits in the context window; no retrieval needed | Simple but limited by window size; no infra overhead |
| **Hybrid** | Combine retrieval + structured queries + context | Multi-source orchestration; routing logic |

### 2. Vector Store Selection Criteria

| Criterion | Questions to answer |
|-----------|---------------------|
| Scale | How many vectors? (thousands → simple; millions → purpose-built) |
| Update frequency | Real-time ingestion vs batch? |
| Hosting | Managed (Pinecone, Weaviate Cloud) vs self-hosted (pgvector, Qdrant, Milvus)? |
| Filtering | Need metadata filtering alongside similarity search? |
| Multi-tenancy | Per-tenant isolation required? |

### 3. Embedding & Chunking

| Decision | Options |
|----------|---------|
| **Embedding model** | OpenAI text-embedding-3, Cohere embed, self-hosted (sentence-transformers) |
| **Chunk size** | Small (256 tokens — precise retrieval) vs large (1024 — more context) vs adaptive (semantic boundaries) |
| **Chunk overlap** | 10-20% overlap to preserve context across boundaries |
| **Update cadence** | On-change (real-time), scheduled (hourly/daily), manual trigger |

### 4. Feature Store (if applicable)

For ML models that consume structured features:
- **Feature definition:** what features are computed, from what sources
- **Serving mode:** online (real-time) vs offline (batch)
- **Freshness:** how stale can features be before they degrade predictions?
- **Versioning:** feature schema evolution strategy

### 5. Data Versioning

- Knowledge bases: version the corpus (snapshots, changelogs)
- Embeddings: track which embedding model + version produced each vector set
- Training data: version control (DVC, MLflow artifacts, cloud object versioning)

### 6. Data Quality Pipeline

- **Validation:** schema checks, completeness, format conformity on ingestion
- **Monitoring:** freshness alerts, volume anomalies, embedding drift detection
- **Lineage:** trace each vector/feature back to its source document/record

---

## ADR Triggers

- Vector DB technology chosen
- RAG vs direct-context vs hybrid decision
- Embedding model selected
- Chunking strategy defined
- Feature store introduced
- Multi-tenant data isolation approach

---

## Anti-Patterns

- RAG without a defined update cadence (knowledge goes stale silently).
- Embedding all content uniformly without considering retrieval quality per content type.
- No data versioning (can't rollback a bad knowledge update).
- Ignoring chunk boundary quality (splitting mid-sentence degrades retrieval).

---

*Data & RAG Rules v1.0.0 | AI-LENS ADLC Sub-Module*
