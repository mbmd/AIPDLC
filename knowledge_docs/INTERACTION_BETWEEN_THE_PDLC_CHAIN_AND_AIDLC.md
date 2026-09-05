# Interaction Between the PDLC Chain and AI-DLC

**Purpose:** Explains how the AI-* PDLC Family relates to **AI-DLC** (AI-Driven Development Life Cycle — Amazon's open-source build lifecycle, `awslabs/aidlc-workflows`), and specifically: how the design chain *feeds* AI-DLC, exactly where AI-Driven Workspace Generator (AI-DWG) sources every piece of what it hands over, and how AI-Driven Governance & Compliance Engine (AI-GCE) and AI-Driven Test Governance Engine (AI-TGE) run *alongside* AI-DLC and what they add that AI-DLC does not provide on its own.

> **Read this if** you plan to build with AI-DLC and want to understand what the PDLC family does before AI-DLC starts, what it hands over, and what keeps running while AI-DLC builds.

---

## What AI-DLC Is — and What It Is Not

AI-DLC is **Amazon's open-source build lifecycle** — the external project `awslabs/aidlc-workflows`, licensed separately under MIT-0. It is the tool that actually turns a prepared workspace into working software.

**AI-DLC is NOT part of the AI-* PDLC Family.** None of the eleven PDLC packages *is* AI-DLC, and installing the family does not install AI-DLC. The relationship is one direction: **the PDLC chain produces the ready-to-build workspace that AI-DLC consumes.** In the family diagram AI-DLC is drawn as a downstream box the chain feeds into, not as one of the family's own steps.

Four PDLC packages are designed to work *with* AI-DLC and carry the "Inspired By: awslabs/aidlc-workflows" attribution: AI-Driven Architecture Design Life Cycle (AI-ADLC), AI-DWG, AI-GCE, and AI-TGE. The other packages have no AI-DLC lineage.

```
   THE PDLC DESIGN CHAIN                          THE BUILD                ALONGSIDE THE BUILD
   (produces the workspace)                       (external tool)          (PDLC companions)

   AI-PILC → AI-POLC → AI-UXD → AI-ADLC → AI-DWG ───────► AI-DLC ◄──────── AI-GCE (guard it)
   initiate  own it   design   design      prepare        build            AI-TGE (test it)
                                the         the                             run continuously
                                design      workspace                       while AI-DLC builds
```

---

## The Three Places Work Happens

To follow the interaction, separate three stages that a project passes through:

| Stage | What happens | Who / what runs |
|-------|--------------|-----------------|
| **Design** | The chain turns a raw requirement into governed design artifacts — a Project Initiation Package, a Product Backlog Package, a UX Design Package, and an Architecture Package. Coherence is established here, before any code exists. | AI-PILC → AI-POLC → AI-UXD → AI-ADLC |
| **Prepare** (the hinge) | AI-DWG reads whichever design artifacts exist and generates the **development workspace** — the steering rules, project docs, configuration, source skeleton, and the specific inputs AI-DLC reads. This is the design→build hinge. | AI-DWG |
| **Build + govern** | AI-DLC builds the software inside the prepared workspace. AI-GCE and AI-TGE run *alongside* it — not as steps you pass through, but as continuous companions that guard compliance and govern test coverage against the built reality. | AI-DLC · AI-GCE · AI-TGE |

The design chain establishes *what to build and how it must behave*. AI-DWG *lays that down as a workspace*. AI-DLC *builds it*. AI-GCE and AI-TGE *watch the build stay honest to the design*.

---

## How AI-DWG Feeds AI-DLC — the Build-Method Switch

AI-DWG supports more than one build method. Which one it prepares for is an explicit setup question with five recognised values, recorded in the workspace manifest at `.governance/workspace-manifest.yaml`:

```yaml
buildProfile: aidlc          # one of: aidlc | spec-driven-kiro | spec-driven-speckit | freestyle | manual
```

**Everything AI-DLC-specific below is emitted only when `buildProfile: aidlc`.** Choose a different build method and none of the `aidlc/` surface appears — the field is the single switch a consumer (or AI-GCE / AI-TGE) reads to know whether the AI-DLC handoff is in play.

When AI-DLC *is* the chosen method, AI-DWG **pre-seeds the workspace in the shape AI-DLC v2 reads** — behavioural rules, per-agent knowledge, the design documents, and (on greenfield projects) a code knowledge base. The intent is that AI-DLC's own stages **affirm that context instead of interviewing you from scratch**. The design work already done by the PDLC chain is handed forward rather than re-elicited.

---

## Where AI-DWG Brings Every Piece From — the Full Provenance Map

AI-DWG invents nothing. It is a **convergence-point generator**: it reads the design artifacts produced upstream and maps each one to an output. Every generated file traces back to a specific PDLC package and a specific artifact within it. This section is the complete "where does each piece come from" trace.

### The three upstream inputs AI-DWG reads

| Input | Producer | How AI-DWG detects it | Output it drives |
|-------|----------|-----------------------|------------------|
| **AP** — Architecture Package | AI-ADLC | `adlc-state.md` marker | Technical cluster (steering, configs, source structure) |
| **PBP** — Product Backlog Package | AI-POLC | `polc-state.md` marker | Product cluster (vision, backlog, traceability, value) |
| **UXP** — UX Design Package | AI-UXD | `uxd-state.md` marker | UX cluster (design system, navigation, content, theming) |

AI-DWG accepts **any non-empty subset** of these three. It generates only the clusters whose input is present; an absent input skips its cluster (with a quality-impact disclosure and your approval first). One input → one cluster; no input dominates.

### General handoff — the AI-DLC input documents (every build method)

Regardless of build method, when AI-DLC is downstream AI-DWG writes these AI-DLC-facing documents at the workspace root, each sourced from a specific upstream package:

| AI-DLC input document | Sourced from | Specific upstream artifact |
|-----------------------|-------------|----------------------------|
| `vision.md` (Vision Document) | AI-POLC (PBP) | Product vision + scope + metrics — enriched with AI-UXD personas/journeys when UXP is present |
| `technical-environment.md` (Technical Environment) | AI-ADLC (AP) | Technology stack + security + quality attributes — enriched with AI-UXD frontend patterns/tokens when UXP is present |
| `ui-implementation-spec.md` (UI spec) | AI-UXD (UXP) | Wireframe spec + user flows |
| `aidlc-rules/extensions/` (extension bundle) | AI-ADLC + AI-UXD + AI-TGE/AI-DWG | AP security rules + UXP accessibility baseline + testing rules |

The full file-by-file mapping (all steering files, configs, and scaffolds, with their always/conditional rules) is in `REFERENCE_MAP_DWG_INPUT_TO_OUTPUT.md`.

### AI-DLC v2 pre-seed — behavioural rules (`aidlc/spaces/<space>/`)

When `buildProfile: aidlc`, AI-DWG writes AI-DLC's behavioural rule files. Each section it writes is sourced from a specific PDLC package. The section set is fixed, and the source of each section is:

| Section AI-DWG writes | Rule file | Sourced from |
|-----------------------|-----------|--------------|
| `## Way of Working` | `memory/team.md` | AI-ADLC git workflow **+** AI-DWG contributing / team-agreement **+** AI-POLC definition of done |
| `## Code Style` | `memory/team.md` | AI-ADLC technology stack **+** naming conventions |
| `## Testing Posture` | `memory/team.md` | AI-ADLC quality attributes — **or AI-TGE when it is active** |
| `## Deployment` | `memory/team.md` | AI-ADLC infrastructure decisions **+** AI-DWG CI/CD mapping |
| `## Security` | `memory/project.md` | AI-ADLC security and identity architecture |
| `## Architecture` | `memory/project.md` | AI-ADLC architecture principles **+** module structure |
| `## Accessibility` | `memory/project.md` | AI-UXD accessibility baseline |
| `## Domain Language` | `memory/project.md` | AI-ADLC ubiquitous language / domain context |
| `## Walking Skeleton` | `memory/project.md` | Optional override only — AI-DLC supplies a default at org level |

AI-DWG also writes four phase-rule files — `memory/phases/{ideation, inception, construction, operation}.md` — carrying the rules for each phase. It **never writes** `memory/org.md`; AI-DLC supplies org-level defaults itself. Every rule file it writes carries a small front-matter block declaring the file's status and its pairing (which sensor verifies it, or `feedforward-only` when none does).

### AI-DLC v2 pre-seed — per-agent knowledge (routing)

AI-DLC loads any knowledge file placed in an agent's directory. AI-DWG's job is to **route** each piece of upstream design into the correct agent directory. The routing — and therefore the source of each — is:

| AI-DLC agent directory | What AI-DWG routes here | Sourced from |
|------------------------|-------------------------|--------------|
| `aidlc-shared/` | Project identity, domain context, naming conventions, git workflow | AI-ADLC + AI-DWG |
| `aidlc-product-agent/` | Product vision, roadmap, personas, journeys, epics, elaborated stories, scope and risks | AI-POLC + AI-UXD |
| `aidlc-architect-agent/` | Technology stack, architecture principles, module structure, C4 views, ADRs, data architecture, integration patterns | AI-ADLC |
| `aidlc-developer-agent/` | API standards, database conventions, error handling | AI-ADLC |
| `aidlc-design-agent/` | Design system, tokens, frontend standards, accessibility baseline, navigation, content, theming | AI-UXD |
| `aidlc-quality-agent/` | Testing strategy, coverage expectations, performance standards | AI-ADLC — or AI-TGE when active |
| `aidlc-devsecops-agent/` | Security architecture, authN/authZ model | AI-ADLC |
| `aidlc-operations-agent/` | Observability and logging standards | AI-ADLC |
| `aidlc-pipeline-deploy-agent/` | CI/CD standards, deployment gates | AI-ADLC + AI-DWG |
| `aidlc-delivery-agent/` | Definition of done, definition of ready, planning cadence | AI-POLC |
| `aidlc-compliance-agent/` | Data classification, regulatory requirements | AI-ADLC — only when compliance content exists |
| `aidlc-aws-platform-agent/` | Cloud account structure, service constraints | AI-ADLC — only when cloud specifics exist |

A directory is created **only when there is content for it** — an empty agent directory would be indistinguishable from AI-DLC's own empty-at-bootstrap state, so AI-DWG never emits one.

### AI-DLC v2 pre-seed — code knowledge base (greenfield only)

On a greenfield project, and **only when AI-ADLC is among the present inputs**, AI-DWG seeds a code knowledge base (`codekb/<repo>/`) so AI-DLC starts with a real picture of the intended system rather than a blank scan:

| Seeded artifact | Sourced from |
|-----------------|--------------|
| `business-overview` | AI-POLC product vision + scope and risks |
| `architecture` | AI-ADLC C4 context and container views |
| `code-structure` | AI-DWG's generated source scaffold + canonical module-structure rules |
| `component-inventory` | AI-ADLC C4 level-3 component design |
| `technology-stack` | AI-ADLC technology-stack decision record |
| `dependencies` | AI-ADLC integration architecture |
| `api-documentation` | AI-ADLC API architecture |

Two artifacts are deliberately **never seeded** — `code-quality-assessment` and `reverse-engineering-timestamp` — because they record a *real* code scan and *when* it ran. Fabricating them could cause AI-DLC to skip a scan it actually needs. On a brownfield project nothing is seeded here; AI-DLC's own reverse-engineering stage runs against the real code.

### AI-DLC v2 pre-seed — the bootstrap record

AI-DWG writes one summary file, `.governance/aidlc-bootstrap.yaml`, that records what it did and what it recommends. **AI-DLC does not read this file** — its readers are the human, AI-GCE, and AI-TGE. It captures a recommended stock scope and depth, the project type (greenfield / brownfield), a per-package completeness map for the chain (which of AI-ILC / AI-PILC / AI-POLC / AI-UXD / AI-ADLC / AI-DWG were complete, partial, or absent), what was seeded, and any coverage waivers. It is how the companions learn what to expect before they start observing.

### The one-line summary of provenance

> **Product decisions come from AI-POLC. Experience decisions come from AI-UXD. Architecture, technology, security, data, API, and domain decisions come from AI-ADLC. Workspace mechanics — CI/CD wiring, contributing/team agreements, the source scaffold — come from AI-DWG itself. Testing posture comes from AI-ADLC unless AI-TGE is active, in which case AI-TGE owns it.** AI-DWG's entire contribution is *routing and rendering* those decisions into the exact shape AI-DLC reads — it makes no product, design, or architecture decisions of its own.

---

## How AI-GCE Runs Alongside AI-DLC — and What It Adds

AI-GCE is a **companion**, not a step. AI-DWG provisions it into the generated workspace, and it runs continuously while AI-DLC builds. Its normal job is to derive a compliance and enforcement layer from the workspace's own steering — the rules, checks, and audit trail that keep the build inside its declared standards.

### First, the most important thing to understand about AI-GCE: it observes and records — it does not stop your work

**AI-GCE's default behaviour is to detect a problem and register a finding, not to halt the machine.** This is a deliberate design stance, and it is true for essentially everything AI-GCE does:

- When a check runs and something is wrong, AI-GCE **records a compliance event** (a timestamped `pass` / `fail` / `warn` entry in the compliance log) and surfaces the finding to you. The write still happens; the build still proceeds. You see the finding and correct it on your next turn.
- When everything passes, AI-GCE stays **silent** — no output at all. It only speaks when something is wrong.
- This applies to **all** of its architecture, naming, API-contract, module-boundary, data-governance, domain-context, logging, session-discipline, role-isolation, and phase-gate checks. Every one of them is **observe-and-report**. None of them blocks a file from being written.

So the correct mental model is: **AI-GCE is a continuous auditor that writes findings into a log, not a gate that stops you.** If you remembered it as "GCE registers findings, it doesn't stop the machine" — that is correct, and it is the rule.

### The single, narrow exception — and exactly when it applies

There is **exactly one** case where AI-GCE can stop something before it happens, and it is worth stating its boundaries precisely so it is not mistaken for general behaviour:

- **What it is:** a *pre-write blocking* check for **hardcoded secrets and PII only** (API keys, connection strings with passwords, private keys, credentials, and personal data in logs). If the write would place a secret on disk, this one check can refuse the write before it lands.
- **Why only this one:** a secret written to disk can be committed, pushed, and mirrored to other machines **irreversibly** within seconds — before any later check, log entry, or approval gate could react. For that specific irreversible-exposure risk, recording a finding *after the fact* is too late. Every *other* concern is safely handled by recording a finding, because the agent can correct it on the next turn with no irreversible harm done.
- **It is opt-in, not automatic.** AI-GCE ships **two** versions of the secrets/PII check: an **advisory** one (the default — it records a finding like every other check) and a **blocking** variant. The blocking variant is generated **only when both** of these are true: (1) the workspace has explicitly set the enforcement strength for secrets/PII to *block*, **and** (2) the platform/harness actually supports a pre-write blocking hook. If either condition is not met, AI-GCE emits the **advisory** version instead and discloses the limitation. In other words, **out of the box, even the secrets check only registers a finding** — blocking is something you must deliberately turn on, on a platform that can honour it.
- **It is still logged.** Even when the blocking variant stops a write, it writes a compliance event (`result: blocked`). Logging is never skipped — stopping the write and recording the finding both happen.

> **The plain-language summary:** AI-GCE **registers findings; it does not stop your work** — with one deliberately narrow, opt-in exception. If (and only if) you switch on blocking for **secrets/PII** on a platform that supports it, that single check will refuse a write that would leak a secret, because that exposure is irreversible. Everything else AI-GCE checks — architecture, naming, APIs, boundaries, auth presence, data governance, and the rest — always records a finding and lets the work proceed.

### How AI-GCE adapts under AI-DLC

With the register-don't-stop model clear, here is how AI-GCE fits its work into AI-DLC's native mechanisms rather than duplicating them:

| Under `buildProfile: aidlc`, AI-GCE… | Does it stop anything? | Why |
|---------------------------------------|------------------------|-----|
| Renders its file-checkable rules as **deterministic AI-DLC sensors** rather than standalone platform hooks | No — sensors **report** a pass/fail result inline in AI-DLC's flow | AI-DLC runs sensors as part of its own stages; expressing the checks as sensors makes them native and keeps the feedback inline |
| Keeps the **secrets / PII check as the one pre-write blocking hook** — *only when blocking is opted in and the platform supports it* | **Only this one, and only when opted in** — otherwise it too is advisory | A secret on disk is an irreversible exposure; a report after the write is too late. This is the sole reason to prevent rather than record |
| Expresses non-file-level rules (session discipline, role isolation, sprint governance, phase gates) as **prose rules** | No — these are guidance the agent reads, not gates | They aren't single-file checks; they belong in AI-DLC's behavioural rule surface |
| **Skips generating its own compliance log and process agents** | n/a | AI-DLC already has native audit shards and its own learning loop — duplicating them would be noise |
| **Verifies the sensor wiring actually landed** | No — it **reports** an unwired sensor as a finding | A sensor that no stage imports fires silently; AI-GCE flags that rather than letting it pass unnoticed |
| Reports which **enforcement surface** is present (`hooks`, `sensors`, `both`, or `docs-only`) | n/a — this is a disclosure, not an action | So a consumer knows what is actually in force instead of assuming hooks exist |

The sensors AI-GCE owns for AI-DLC cover architecture conformance, API contracts, module boundaries, data classification, domain context, domain purity, sensitive-data handling, auth presence, migration safety, and accessibility. **All of these are reporting sensors** — they record a result; they do not stop a write. (Test coverage is a sensor too, but it belongs to AI-TGE — see below.) Note also that AI-DLC's own approval gates can *pause a phase transition* until a gate-fired sensor passes — but that is AI-DLC's lifecycle gate acting, not AI-GCE stopping an individual write, and it is coarser than the one pre-write hook described above.

**What AI-GCE adds that AI-DLC v2 does not provide:** AI-DLC builds the software and can run checks; it does not, on its own, **derive** a project-specific compliance layer from *your* architecture and steering, decide which checks must exist, track baseline-versus-new violations, or produce the certification-oriented evidence a governance lead needs. AI-GCE is the source of *which* rules apply and *why* — AI-DLC is the surface that runs them. AI-GCE also deliberately leaves the AI-DLC rules-and-knowledge surface (the `aidlc/` tree) **out of its drift detection**, because that surface is co-authored by AI-DWG, AI-DLC's learning loop, and the team — drift is measured against the *design baseline*, not the living rules the team and AI-DLC edit together.

---

## How AI-TGE Runs Alongside AI-DLC — and What It Adds

AI-TGE is the second companion — a QA/test-architect engine that runs alongside AI-DLC together with AI-GCE. Like AI-GCE it is **not a stage you pass through**; it runs continuously. Its job answers one question: *did we test what we designed, and which missing tests matter most?*

It works in two phases. A **strategy phase** reads the Architecture Package, derives which tests *must* exist from the architectural commitments, and risk-scores the gaps. An **observation phase** then runs continuously, watching AI-DLC's build progress and updating coverage as units complete — it reads AI-DLC's own state to know what has been built.

Under `buildProfile: aidlc`, AI-TGE re-targets its output to AI-DLC's surfaces:

| Under `buildProfile: aidlc`, AI-TGE… | Where it lands |
|--------------------------------------|----------------|
| Writes the testing strategy as reference knowledge | AI-DLC's `aidlc-quality-agent/` directory |
| Writes coverage **MUST** statements as rules | `memory/team.md` under `## Testing Posture` |
| Owns the **test-coverage sensor** | The one `pdlc-test-coverage` AI-DLC sensor |
| Records its **engine depth** and AI-DLC's **test volume** as two independent settings | The bootstrap record |

**An important distinction:** AI-TGE's *test-governance depth* (how much detail its engine produces and which of its twelve stages run) is **independent** of AI-DLC's *test volume strategy* (how many tests to write). They share the same three level names but mean different things — a team could want AI-TGE Comprehensive with AI-DLC Minimal, or the reverse. In any workspace that also runs AI-DLC, the two are labelled distinctly so they are never confused.

**What AI-TGE adds that AI-DLC v2 does not provide:** AI-DLC's own build-and-test stage generates test *instructions* and can write test code. AI-TGE does **neither** — its hard boundary is that it **governs** tests, it does not write or run them, and it does not connect to CI/CD. What it adds is the accountability layer AI-DLC lacks: a register of which tests *must* exist derived from the architecture, a continuously updated coverage picture, risk-scored gaps that say *which* missing test matters most, and a technical-debt scorecard. In short, AI-DLC decides *how* tests are built; AI-TGE decides *whether the set of tests is sufficient for what was designed.*

---

## What the Companions Add — Summary

| Concern | AI-DLC v2 on its own | What the PDLC companion adds |
|---------|----------------------|------------------------------|
| **Starting context** | Interviews you at each stage to gather product, design, and architecture context | AI-DWG pre-seeds all of it from the chain, so AI-DLC's stages *affirm* rather than *elicit* |
| **Compliance** | Builds software; can run checks | AI-GCE **derives** which rules apply from *your* architecture, renders them as native sensors, tracks baseline-vs-new violations, and reports the enforcement surface |
| **Pre-write safety** | — | AI-GCE can, **as an opt-in exception to its register-don't-stop model**, block a write for **secrets/PII only** — the one irreversible-exposure case — when blocking is switched on and the platform supports it. Every other AI-GCE check records a finding and lets the work proceed |
| **Test accountability** | Generates test instructions; can write test code | AI-TGE **governs** whether the test set is sufficient — a must-exist register derived from the architecture, risk-scored coverage gaps, and a debt scorecard |
| **Audit & drift** | Native audit shards + learning loop | AI-GCE avoids duplicating these under AI-DLC, and deliberately excludes AI-DLC's living rules surface from its drift detection |

The division of labour is clean: **AI-GCE = "does the code follow the rules?"** · **AI-TGE = "do tests exist for what was designed?"** · **AI-DLC = "how is the software built and its tests written?"** The two companions are complementary and non-overlapping, and both are complementary to — never a replacement for — AI-DLC.

---

## Related Documents

| Document | What it adds |
|----------|--------------|
| [`INTERACTION_BETWEEN_AI_GCE_GOVERNANCE_AND_AIDLC_SENSORS.md`](INTERACTION_BETWEEN_AI_GCE_GOVERNANCE_AND_AIDLC_SENSORS.md) | The detailed AI-GCE-vs-sensors comparison — enforcement model (register vs block), what maps to sensors vs behavioural rules, and what each does the other cannot |
| [`HOW_AIDLC_V2_SUPPORT_WORKS.md`](HOW_AIDLC_V2_SUPPORT_WORKS.md) | The mechanics of the AI-DLC v2 build method — what AI-DWG emits into the `aidlc/` tree, the sensor manifests, and the `buildProfile` switch. This doc is the *interaction and provenance* view; that one is the *mechanism* view |
| [`REFERENCE_MAP_DWG_INPUT_TO_OUTPUT.md`](REFERENCE_MAP_DWG_INPUT_TO_OUTPUT.md) | The complete file-by-file map of what AI-DWG reads and where every generated file lands |
| [`HOW_DWG_GENERATION_ENGINE_WORKS.md`](HOW_DWG_GENERATION_ENGINE_WORKS.md) | How the AI-DWG generator engine converts design artifacts into a workspace |
| [`HOW_CHAIN_HANDOFF_WORKS.md`](HOW_CHAIN_HANDOFF_WORKS.md) | The marker-file detection and handoff mechanism that connects the chain |
| [`HOW_GCE_DERIVATION_PIPELINE_WORKS.md`](HOW_GCE_DERIVATION_PIPELINE_WORKS.md) | How AI-GCE derives its compliance layer from workspace steering |
| [`HOW_GCE_COMPLIANCE_AUDIT_WORKS.md`](HOW_GCE_COMPLIANCE_AUDIT_WORKS.md) | How AI-GCE runs compliance audits and tracks violations |
| [`HOW_TGE_TEST_GOVERNANCE_WORKS.md`](HOW_TGE_TEST_GOVERNANCE_WORKS.md) | How AI-TGE derives a strategy and observes coverage |
| [`HOW_PROJECT_LAYER_COLLABORATION_WORKS.md`](HOW_PROJECT_LAYER_COLLABORATION_WORKS.md) | How AI-ADLC, AI-UXD, and AI-POLC converge into AI-DWG |
| [`LIFECYCLE_OF_A_PROJECT_THROUGH_THE_CHAIN.md`](LIFECYCLE_OF_A_PROJECT_THROUGH_THE_CHAIN.md) | The end-to-end journey of a project across the whole chain |

---

*Knowledge Document | Interaction | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
