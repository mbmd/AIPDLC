<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Technology Stack

**Document Status:** {Draft / Review / Approved}
**Version:** {n.n}
**Date:** {YYYY-MM-DD}
**Author:** {Role}

---

## 1. Core Stack

| Layer | Technology | Version | License | Rationale | ADR |
|-------|-----------|:-------:|:-------:|-----------|:---:|
| Backend Runtime | {tech} | {ver} | {license} | {1-line why} | ADR-{nnn} |
| Backend Framework | {tech} | {ver} | {license} | {why} | ADR-{nnn} |
| Frontend Framework | {tech} | {ver} | {license} | {why} | ADR-{nnn} |
| UI Component Library | {tech} | {ver} | {license} | {why} | — |
| Primary Database | {tech} | {ver} | {license} | {why} | ADR-{nnn} |
| ORM / Data Access | {tech} | {ver} | {license} | {why} | — |

---

## 2. Supporting Services

| Service | Technology | Version | License | Purpose | ADR |
|---------|-----------|:-------:|:-------:|---------|:---:|
| Cache | {tech} | {ver} | {license} | {purpose} | — |
| Search | {tech} | {ver} | {license} | {purpose} | — |
| Message Queue | {tech} | {ver} | {license} | {purpose} | — |
| File Storage | {tech} | {ver} | {license} | {purpose} | — |
| Real-Time | {tech} | {ver} | {license} | {purpose} | — |

---

## 3. Deployment & Operations

| Concern | Technology | Version | License | Purpose | ADR |
|---------|-----------|:-------:|:-------:|---------|:---:|
| Containerization | {tech} | {ver} | {license} | {purpose} | — |
| Orchestration | {tech} | {ver} | {license} | {purpose} | — |
| CI/CD | {tech} | {ver} | {license} | {purpose} | — |
| Metrics | {tech} | {ver} | {license} | {purpose} | — |
| Logging | {tech} | {ver} | {license} | {purpose} | — |
| Alerting | {tech} | {ver} | {license} | {purpose} | — |

---

## 4. Build & Development Tools

| Tool | Technology | Purpose |
|------|-----------|---------|
| Package Manager | {tech} | {purpose} |
| Linting | {tech} | {purpose} |
| Testing | {tech} | {purpose} |
| API Documentation | {tech} | {purpose} |

---

## 5. Stack Compatibility Notes

{Any notes on how components interact, known limitations, or version dependencies.}

---

## 6. Polyglot Technology Matrix

<!-- CONDITIONAL: Include this section when the microservices extension is active OR the system uses ≥2 distinct backend runtimes across containers. Delete this section (including the comment) for single-stack systems. -->

### Per-Service Technology Breakdown

| Service / Container | Language | Runtime + Version | Framework | Primary Data Store | Cache | Async Consumer | Protocol (Inbound) | Divergence Rationale |
|---------------------|----------|-------------------|-----------|-------------------|-------|:--------------:|-------------------|---------------------|
| {service_1} | {lang} | {runtime ver} | {framework} | {db + ver} | {cache or —} | {Yes/No} | {REST / gRPC / GraphQL / Event} | {Why this service diverges — 1 line} |
| {service_2} | {lang} | {runtime ver} | {framework} | {db + ver} | {cache or —} | {Yes/No} | {protocol} | {rationale} |
| {service_n} | {lang} | {runtime ver} | {framework} | {db + ver} | {cache or —} | {Yes/No} | {protocol} | {rationale} |

### Stack Diversity Summary

- **Distinct languages:** {n} ({list})
- **Distinct runtimes:** {n} ({list})
- **Distinct primary data stores:** {n} ({list})
- **Diversity classification:** {Focused Polyglot (2 langs) / Broad Polyglot (3+) / Mono-language with heterogeneous data}

### Polyglot Governance Decisions

| Concern | Decision | Justification |
|---------|----------|---------------|
| **Operational overhead** | {Acceptable / Mitigated by {mechanism}} | {Why the team can handle multiple stacks} |
| **Hiring & skills** | {Team covers all / Training plan / Contractor augmentation} | {How skills gap is addressed} |
| **Shared libraries / contracts** | {Proto/IDL contracts / Per-language SDK / OpenAPI generation / None needed} | {Cross-service code sharing strategy} |
| **CI/CD complexity** | {Per-service pipelines / Mono-repo with language-specific jobs / Hybrid} | {Build strategy for multiple toolchains} |
| **Observability uniformity** | {OpenTelemetry / Vendor SDK per language / Mesh-level (sidecar)} | {How tracing/metrics stay consistent} |
| **Local development** | {Docker Compose / Dev containers per language / Partial with mocks} | {Developer experience strategy} |
| **Dependency management** | {Per-service lockfiles / Centralized vulnerability scanning} | {Security patching across ecosystems} |

### Divergence Justification

Each stack divergence must satisfy at least one of:
1. **Performance requirement** — dominant language cannot meet latency/throughput target
2. **Ecosystem gap** — critical capability exists only in the alternative language
3. **Team expertise** — specialist team with >30% velocity advantage in alternative
4. **Regulatory/compliance** — constraint mandates a specific runtime or certified library
5. **Acquisition/legacy** — rewrite cost exceeds maintenance cost over planning horizon

{If none apply to a service → recommend converging to the dominant stack.}

→ _Polyglot strategy ADR: ADR-{nnn} (produced when ≥3 distinct runtimes or Comprehensive depth)_

---

*Technology Stack v{version} | {date} | Status: {status}*
