# How AI-DLC v2 Support Works

**Purpose:** Explains how the AI-* PDLC Family targets **AI-DLC** (AI-Driven Development Life Cycle — Amazon's open-source build lifecycle) **v2** as a build method — what the AI-Driven Workspace Generator (AI-DWG) emits, how the AI-Driven Governance & Compliance Engine (AI-GCE) enforces via v2 sensors, and how the AI-Driven Test Governance Engine (AI-TGE) re-targets — while every other build method stays unchanged.

---

## Who This Is For

Teams whose downstream build engine is AI-DLC v2, and anyone who needs to understand what a PDLC-generated workspace looks like when it is consumed by AI-DLC rather than by a spec-driven or freestyle flow.

---

## The One Idea

A PDLC workspace is **build-method-agnostic** at its core. The shared workspace — `rules/`, `backlog/`, `architecture/`, `ux/`, `info/` — is identical no matter how you build. AI-DLC v2 support adds a **conditional surface** that appears **only** when the build method is AI-DLC: a pre-seeded `aidlc/` tree in the exact shape v2 reads, governance checks expressed as v2 **sensors**, and test governance re-targeted to v2's coverage outcome. Nothing about the other build methods changes.

---

## The `buildProfile` field — how a workspace declares its build method

Every generated workspace carries a manifest at `.governance/workspace-manifest.yaml` with one field that decides all of this:

```yaml
buildProfile: aidlc
```

The five recognised values are:

| Value | Meaning |
|-------|---------|
| `aidlc` | AI-DLC v2 is the build engine — the `aidlc/` tree + sensors are emitted |
| `spec-driven-kiro` | Spec-driven build using Kiro specs |
| `spec-driven-speckit` | Spec-driven build using GitHub Spec Kit (generates `.specify/memory/constitution.md`) |
| `freestyle` | Free-form AI-assisted build, no specific harness |
| `manual` | No AI build harness — names what an unset field used to imply |

The `aidlc/` surface described below is present **if and only if** `buildProfile: aidlc`. Consumers dispatch on two fields that already exist — `platformTargets` for platform capability, `buildProfile` for build method — so no new manifest field is introduced.

---

## What AI-DWG emits under `buildProfile: aidlc`

When the build method is AI-DLC, AI-DWG generates the `aidlc/` tree that v2 reads. Four parts:

### 1. Behavioural rules (`aidlc/spaces/<space>/memory/`)

Plain-prose rule files that tell AI-DLC how this team and project work:

| File | Contains |
|------|----------|
| `memory/team.md` | Practices that outlive the project — branching model, review cadence, code style, testing posture, deployment |
| `memory/project.md` | This project's specialization — security, architecture, domain language, accessibility target |
| `memory/phases/{ideation,inception,construction,operation}.md` | Rules for each phase's stages |

AI-DWG never writes `memory/org.md` — v2 supplies org-level defaults. The rules chain is strictly **additive** (organization → team → project → phase → stage); a project rule sits alongside an org default, never replacing it. Seeded content is kept specific to the project so it does not restate framework defaults (v2 flags overlapping headings as possible contradictions).

### 2. Per-agent knowledge (`aidlc/spaces/<space>/knowledge/`)

Your design documents, routed to the AI-DLC agent that needs them — product knowledge to the product agent, architecture to the architect agent, design-system content to the design agent, and so on. The **routing is the contract** (which directory a document lands in); the filenames are not. A directory is created only when there is real content for it — an empty agent directory would be indistinguishable from v2's own empty-at-bootstrap state.

### 3. Sensor manifests

Deterministic checks that AI-GCE would otherwise run as platform hooks, written as v2 sensor manifests at the project tier. The naming is a hard contract: the file must carry the `aidlc-` prefix and its `id:` must equal the filename minus that prefix — a misnamed manifest is **silently skipped** by v2's compiler. AI-DWG also emits `.governance/AIDLC_SENSOR_WIRING.md` telling you which stage should import each sensor (AI-DWG never edits v2's stage files itself), and AI-GCE later verifies the wiring landed.

### 4. Code knowledge base (`aidlc/spaces/<space>/codekb/`)

On **greenfield** projects (and only when architecture content is present), AI-DWG pre-seeds v2's code knowledge base — business overview, architecture, code structure, component inventory, technology stack, dependencies, API documentation. Two artifacts are **never** seeded: a code-quality assessment and a reverse-engineering timestamp, because each records a real scan and a fabricated value could make v2 skip a scan it actually needs. On **brownfield**, nothing is seeded and v2's Reverse Engineering stage runs against the real code.

A bootstrap record at `.governance/aidlc-bootstrap.yaml` summarises what was seeded and which stock v2 scope is recommended. AI-DLC's own stages then **affirm** this context instead of interviewing you for it from scratch.

---

## What AI-GCE does under `buildProfile: aidlc`

AI-GCE reads the same profile and adapts its enforcement:

- **Sensor-convertible checks become sensors**, not platform hooks — a deterministic check that v2 can run as a sensor is emitted as one.
- **The secrets/PII check stays a pre-write blocking hook** — only a hook can stop a bad write *before* it lands, so this one genuine pairing is kept.
- **Non-file-level concerns** (session discipline, role isolation, sprint governance, phase gates) are expressed as **prose rules** in the behavioural files.
- AI-GCE **skips generating its own compliance log and process agents** — v2 has native audit shards and its own learning loop.
- The hand-over contract now reports an **enforcement surface** — `hooks | sensors | both | docs-only` — so downstream tooling reads what it can rely on instead of assuming.

The `aidlc/` rules-and-knowledge tree is deliberately **excluded from drift detection**: it is a generated-then-team-owned surface that v2's learning loop co-authors, so drift only covers divergence from the design baseline (architecture, data, infrastructure, UX, product), never the rules surface.

---

## What AI-TGE does under `buildProfile: aidlc`

AI-TGE writes its testing strategy as reference knowledge for the quality agent and its coverage MUST-statements as rules, and it owns the **test-coverage sensor manifest** (AI-GCE owns the rest). It keeps **two independent settings** that share names but mean different things:

- **Test-governance depth** — how much detail AI-TGE itself produces and which of its stages run.
- **Test volume strategy** — how many tests AI-DLC generates.

A team can legitimately want Comprehensive test-governance depth with Minimal test volume; the two are never derived from each other, and both are labelled distinctly in any workspace that also runs AI-DLC. AI-TGE's artifacts live under `.governance/test/` (the former `.tge/` folder is retired).

---

## What Stays the Same

- Every **other** build method (`spec-driven-kiro`, `spec-driven-speckit`, `freestyle`, `manual`) is unchanged — no `aidlc/` tree, no sensors.
- The **shared workspace core** is byte-for-byte identical across build methods; only the conditional `aidlc/` surface and the enforcement mechanism differ.
- **Attribution:** only `aidlc` workspaces carry the awslabs "Inspired By" line, because only they are shaped for AI-DLC.
- Bringing an existing workspace to a different build method's output shape is handled by the build-method migration (catalogue entry **M10**), without re-running the design chain.

---

## Related Documents

| Document | Location |
|----------|----------|
| Interaction Between the PDLC Chain and AI-DLC | `knowledge_docs/INTERACTION_BETWEEN_THE_PDLC_CHAIN_AND_AIDLC.md` |
| How DWG Generation Engine Works | `knowledge_docs/HOW_DWG_GENERATION_ENGINE_WORKS.md` |
| How to Prepare a Development Workspace | `knowledge_docs/HOW_TO_PREPARE_A_DEVELOPMENT_WORKSPACE.md` |
| Reference Map — DWG Input to Output | `knowledge_docs/REFERENCE_MAP_DWG_INPUT_TO_OUTPUT.md` |
| How GCE Compliance Audit Works | `knowledge_docs/HOW_GCE_COMPLIANCE_AUDIT_WORKS.md` |
| How TGE Test Governance Works | `knowledge_docs/HOW_TGE_TEST_GOVERNANCE_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

*Knowledge Document | Created: 2026-09-05 | Updated: 2026-09-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
