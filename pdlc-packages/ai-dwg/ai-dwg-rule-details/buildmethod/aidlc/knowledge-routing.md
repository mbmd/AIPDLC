<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Knowledge Routing — which content goes to which agent directory

> **Load this file** during step 2 of the `aidlc/` emitter. It routes the **reference prose** portion of each PDLC input to the correct v2 per-agent knowledge directory. Authority: `common/aidlc-v2-output-contract.md` §3.

## The binding decision is the DIRECTORY, not the filename

v2 loads **any** `.md` file placed in an agent's directory — there is no naming convention. So routing chooses **which directory**; AI-DWG's filenames may be chosen for human readability (e.g. `security-architecture.md`, `api-standards.md`).

## Routing table

| Agent directory (`aidlc/spaces/<space>/knowledge/<agent>/`) | What AI-DWG routes here | Upstream source |
|---|---|---|
| `aidlc-shared/` | Project identity, domain context, naming conventions, git workflow | AI-ADLC + AI-DWG |
| `aidlc-product-agent/` | Product vision, roadmap, personas, user journeys, epics, elaborated stories, scope & risks | AI-POLC + AI-UXD |
| `aidlc-architect-agent/` | Technology stack, architecture principles, module structure, C4 views, ADRs, data architecture, integration patterns | AI-ADLC |
| `aidlc-developer-agent/` | API standards, database conventions, error handling | AI-ADLC |
| `aidlc-design-agent/` | Design system, tokens, frontend standards, accessibility baseline, navigation, content guidelines, theming | AI-UXD |
| `aidlc-quality-agent/` | Testing strategy, coverage expectations, performance standards | AI-ADLC, or AI-TGE when active |
| `aidlc-devsecops-agent/` | Security architecture, authN/authZ model | AI-ADLC |
| `aidlc-operations-agent/` | Observability & logging standards | AI-ADLC |
| `aidlc-pipeline-deploy-agent/` | CI/CD standards, deployment gates | AI-ADLC + AI-DWG |
| `aidlc-delivery-agent/` | Definition of done, definition of ready, planning cadence | AI-POLC |
| `aidlc-compliance-agent/` | Data classification, regulatory requirements | AI-ADLC — **only when compliance content exists** |
| `aidlc-aws-platform-agent/` | Cloud account structure, service constraints | AI-ADLC — **only when cloud specifics exist** |

## The knowledge vs rules split (input side)

Each source steering file splits **once** via `rules-knowledge-splitter.md` (the shared front step): the **rules portion** (MUST/MUST NOT/NEVER) goes to `memory/` (see `memory-mapping.md`); the **knowledge portion** (prose, tables, diagrams, reference material) routes here. A file contributes to *both* consumers from that single split — its rules to `memory/project.md`, its reference prose to its agent directory.

## Conditional emission — the hard rule

**A directory is created only when there is content for it.** An empty agent directory is NEVER written: it would be indistinguishable from v2's own empty-at-bootstrap state while implying content was intended. So `aidlc-compliance-agent/` and `aidlc-aws-platform-agent/` appear only when their conditional source content is present; likewise `aidlc-design-agent/` requires AI-UXD, `aidlc-product-agent/` requires AI-POLC/UXD, etc. When a peer input is absent, its agent directories are simply not created, and the bootstrap record's `pdlc_chain_completeness` reflects the gap.

## Front-matter on every knowledge file

```yaml
---
generatedBy: AI-DWG
generatedVersion: {version}
source: {upstream document path}
generatedOn: {ISO-8601 timestamp}
ownership: generated
---
```

This is the standard PDLC provenance block. It makes the seeded/authored distinction visible in a directory the team also writes into.

## What is NEVER written here

- `knowledge/documentkb/` — v2's **cataloguing tool only**, a derived index written transactionally; hand-writing corrupts the index. The team runs v2's catalogue command once. (Full narrative documents go to `knowledge/documents/` — see `documents-placement.md`.)

---

*Developer-side design detail · AI-DWG `aidlc/` knowledge routing · © Mohammad Maheri*
