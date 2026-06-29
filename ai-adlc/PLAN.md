# AI-ADLC — Package Build Plan

**Package:** AI-ADLC (AI-Driven Architecture Design Life Cycle)
**Type:** Interactive workflow (lifecycle)
**Status:** ✅ Complete (v1.1.0) — core workflow + 6 opt-in extensions delivered
**Build Sessions:** S05–S06 (2026-06-04 to 2026-06-05)
**Persona:** `#persona-cto-architect`

---

## Summary Report

| Field | Value |
|-------|-------|
| Status | ✅ COMPLETE — core (v1.0) + extensions (v1.1) built and passing dry tests (TR-029, TR-305) |
| Sessions | S05–S06: Core workflow + stages | S07–S08: Extensions (DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags) | Subsequent: sub-role embedding, hardening |
| Scope | v1.1 — Full architecture design lifecycle (13 stages, 5 phases) + 6 opt-in extensions |
| Key Decisions | C4 progressive decomposition, ADR-driven decisions, extension opt-in model, brownfield awareness |
| Persona | `#persona-cto-architect` (auto-loaded via `ai-adlc-rules.md`) |

---

## Package Identity

| Field | Value |
|-------|-------|
| **Name** | AI-ADLC *(challenged per Lesson 12: "SALC" → "ADLC" — better acronym, Architecture Design vs. Solution Architecture)* |
| **Full Title** | AI-Driven Architecture Design Life Cycle |
| **Package Type** | Interactive workflow (lifecycle) |
| **Primary Input** | PIP + PBP + UXP (from AI-PILC / AI-POLC / AI-UXD) |
| **Primary Output** | Architecture Package (AP) |
| **User Persona** | CTO, Solution Architect, Technical Lead |
| **Family Position** | Project-layer design (third, after AI-POLC and AI-UXD): AI-POLC → AI-UXD → **AI-ADLC** → AI-DWG |
| **Marker File** | `adlc-state.md` |

---

## Design Decisions

| # | Decision | Resolution |
|---|----------|-----------|
| 1 | Package name | AI-ADLC (not SALC) — Lesson 12 |
| 2 | Phase structure | 5 phases (Foundation → Decomposition → Decisions → Design → Assembly) |
| 3 | Stage count | 13 stages |
| 4 | Decomposition model | C4 (Simon Brown): System Context → Containers → Components |
| 5 | Decision tracking | ADRs for every major decision (technology, pattern, security, data) |
| 6 | Extensions model | Opt-in at Stage 5-6; blocking once activated (Lesson 9) |
| 7 | Depth model | Three-tier: Minimal / Standard / Comprehensive |
| 8 | Brownfield | First-class: existing system integration handled from Stage 1 (Lesson 23) |
| 9 | Diagrams | Mermaid syntax with consistent styling per `diagram-standards.md` |
| 10 | Sub-roles | Per-stage: BA, Systems Engineer, Security Architect, Data Architect, API Designer + extension sub-roles |

---

## File Structure

```
ai-adlc/
├── README.md
├── LICENSE
├── NOTICE
├── PLAN.md                              ← This file (retroactive)
├── ROADMAP.md                           ← Extension roadmap (v1.2+)
├── WHITEPAPER.md
├── CONCEPTUAL_MAP.md
├── ai-adlc-rules/
│   └── core-workflow.md                 ← Master orchestration (always loaded)
├── ai-adlc-rule-details/
│   ├── common/                          ← Cross-cutting rules (6 files incl. diagram-standards)
│   ├── foundation/                      ← Stages 1-3 (workspace, ingestion, vision)
│   ├── decomposition/                   ← Stages 4-5 (system context, containers)
│   ├── decisions/                       ← Stages 6-8 (tech stack, tenancy, security)
│   ├── design/                          ← Stages 9-12 (data, API, integration, components)
│   ├── assembly/                        ← Stage 13 (package consolidation)
│   ├── extensions/                      ← 6 opt-in extension folders
│   │   ├── ddd-tactical/
│   │   ├── microservices/
│   │   ├── bff-pattern/
│   │   ├── event-sourcing-cqrs/
│   │   ├── resilience-patterns/
│   │   └── feature-flags/
│   └── templates/                       ← 12 deliverable templates + ADR template
│       └── agents/                      ← Agent template + shortcut + guide
└── setup/
    ├── INSTALL.md
    └── TEST_MODE_USER_GUIDE.md
```

---

## Build Sequence

| Step | Activity | Status |
|------|----------|--------|
| 1 | Define Problem Space | ✅ Done |
| 2 | Research & Extract (C4, ADR patterns, TOGAF alignment) | ✅ Done |
| 3 | Present Plan for Approval | ✅ Done |
| 4 | Build Core File (`core-workflow.md`) | ✅ Done |
| 5 | Build Common Files (6 files) | ✅ Done |
| 6 | Build Stage Detail Files (13 files across 5 phase folders) | ✅ Done |
| 7 | Build Templates (12+ deliverable templates) | ✅ Done |
| 8 | Build Extensions (6 × opt-in + detail = 12 files) | ✅ Done (v1.1) |
| 9 | Build Agent Templates (3 files) | ✅ Done |
| 10 | Build README + LICENSE + INSTALL + WHITEPAPER | ✅ Done |
| 11 | Verify (Dry Test — TR-029, TR-305) | ✅ PASS |
| 12 | Register in FAMILY_TABLE_MAP.md | ✅ Done |

---

## Extension Status (see ROADMAP.md for details)

| Priority | Extensions | Status |
|----------|:----------:|:------:|
| v1.1 (High) | DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags | ✅ Delivered |
| v1.2 (Medium) | Serverless, AI/ML, Micro-Frontends, GraphQL Federation, Multi-Region | ⬜ Planned |
| v1.3+ (Lower) | Zero Trust, K8s-Native, Edge, Data Mesh, Chaos, Supply Chain, Offline-First, Streaming, Plugins | ⬜ Future |

---

## Applicable Lessons

| Lesson | How Applied |
|--------|------------|
| L1 | "Life Cycle" naming — correct (interactive multi-phase workflow) |
| L2 | Sub-roles per stage (Systems Engineer, Security Architect, etc.) |
| L3 | Reconciliation mode — AP delta detection for downstream signaling |
| L4 | Adaptive intake — PIP / raw requirements / brownfield |
| L5 | Downstream signaling — AP changes signal AI-DWG |
| L9 | Extensions — opt-in model for advanced patterns |
| L11 | Family table in README + core-workflow |
| L12 | Name challenged: SALC → ADLC |
| L13 | Explicit I/O contract |
| L14 | Marker file: `adlc-state.md` |
| L15 | Extension-awareness documented for downstream |
| L22 | Extension rule files follow consistent skeleton |
| L23 | Brownfield is first-class |

---

*Created retroactively: 2026-06-13 | Original build: 2026-06-04–05 (Sessions S05–S06)*
