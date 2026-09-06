# Changelog

All notable changes to **AIFLC — the AI-* PDLC (Product Development Life Cycle) Family** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) with a
pre-release (beta) suffix until the first stable release.

> **Versioning note.** This changelog tracks the **family** release version (`0.1.0-beta.N`).
> Individual packages carry their own semantic versions (currently 1.0.0–1.1.0); those are
> recorded in each package's README, not here.

## [Unreleased]

<!-- New user-facing changes accrue here as they land, then get promoted to a version + date at release. -->

## [0.1.0-beta.6-r3] — 2026-09-05

### Added

- **Knowledge base — seven new how-it-works guides for the AI-DLC v2 feature set.** The knowledge
  base gained documentation for capabilities that shipped in beta.6: how AI-DLC v2 support works
  end to end, how team-aligned workspaces are produced across the design chain, how the lens system
  (AI Lens, Automation Lens, agentic coverage) applies domain facets, how workspace HTML publishing
  works, how draft-first gates operate, how the AI-FLO / AI-DFE fabric auto-refreshes, and how
  artifact-quality rules are enforced. These document existing behaviour — no package behaviour changed.

### Fixed

- **Documentation — corrected the retired test-governance output path.** Test-governance docs and
  references that still pointed at the former top-level `.tge/` folder now point at
  `.governance/test/`, matching where AI-TGE actually writes.
- **Documentation — architecture-extension coverage brought current.** The architecture-extension
  guides now describe the full set of opt-in patterns (adding Domain Storytelling, Wardley Mapping,
  and deep Threat Modeling) and note that cross-service consistency (Saga) is handled by the core
  workflow. The AI-DWG, AI-GCE, and AI-TGE package READMEs were refreshed to match.

## [0.1.0-beta.6-r2] — 2026-09-05

### Added

- **Knowledge doc — how the PDLC chain feeds AI-DLC.** A new interaction document explaining the
  chain-to-AI-DLC handoff, exactly where AI-DWG sources each piece it hands over, and how AI-GCE and
  AI-TGE run alongside AI-DLC.
- **Knowledge doc — AI-GCE governance vs AI-DLC sensors.** A new comparison document covering the
  enforcement model (AI-GCE registers findings by default, with one opt-in pre-write exception for
  secrets/PII), what maps to sensors vs behavioural rules, and what each does the other cannot.

### Fixed

- **Dashboard — sample data replaced with generic placeholders.** The AIFLC PDLC Dashboard's
  seed and demo content previously carried example values from an internal sample project. It now
  ships with neutral, generic placeholder data.
- **Documentation — internal references removed from published files.** The family README, the
  lens registry, and several shared package reference files carried pointers to internal build-side
  locations. Those references have been rewritten so every published file is self-contained.
- **Published surface — additional internal-reference scrub.** Always-loaded orchestrator files, the
  extensions manifest, the governance-contract header, and an AI-GCE core file were cleaned of
  build-side paths and internal identifiers so every published file is self-contained.

## [0.1.0-beta.6] — 2026-09-01

AI-DLC (AI-Driven Development Life Cycle — Amazon's open-source build lifecycle) v2 support across
the build-and-govern surface. AI-DWG (AI-Driven Workspace Generator, 1.1.0), AI-GCE (AI-Driven
Governance & Compliance Engine, 1.1.0), and AI-TGE (AI-Driven Test Governance Engine, 1.1.0) gain
the ability to target AI-DLC v2 as a build method — the generated workspace
is now pre-seeded in the shape v2 reads, governance checks can run as v2 sensors, and test
governance re-targets to v2's coverage outcome — while every other build method is unchanged.

### Added

- **AI-DWG — AI-DLC v2 support.** When a project's build method is AI-DLC, the generated
  workspace now includes the `aidlc/` tree that AI-DLC v2 reads: behavioural rules at team,
  project and per-phase scope; per-agent reference knowledge routed to the agent that needs it;
  your full design documents placed where AI-DLC can catalogue them; and a pre-seeded code
  knowledge base on greenfield projects. AI-DLC's own stages then affirm this context instead
  of interviewing you for it from scratch.
- **AI-DWG — GitHub SpecKit support.** Choosing the SpecKit build method now generates
  `.specify/memory/constitution.md` from your canonical rules.
- **AI-DWG — the build method is now an explicit question.** It is asked once during setup and
  confirmed on any regeneration, because it decides whether a whole folder tree is generated.
  Five values are recognised: `aidlc`, `spec-driven-kiro`, `spec-driven-speckit`, `freestyle`,
  and `manual`. `manual` names what an unset field previously implied.
- **AI-GCE — enforcement surface is now discoverable.** The hand-over contract reports which
  enforcement mechanism is present — platform hooks, AI-DLC sensors, both, or documentation
  only — so downstream tooling can read what it can rely on instead of assuming.
- **AI-GCE — AI-DLC sensor support.** Where a governance check can run as a deterministic
  AI-DLC sensor, AI-GCE now emits the rule, its pairing declaration and an executable check
  script. Three checks that had been consolidated away to reduce noise are restored as
  individual per-file checks.

### Changed

- **AI-TGE — degraded runs now say so.** Previously, running AI-TGE against a workspace whose
  layout it did not recognise produced a coverage report that looked complete but was derived
  from file timestamps and contained no story coverage, with no warning. A degraded run is now
  clearly reported as degraded in the report, the artifact and the state file.
- **AI-TGE — test-governance depth and test volume are separate settings.** They previously
  shared the names Minimal, Standard and Comprehensive while meaning different things: how much
  detail AI-TGE produces, versus how many tests AI-DLC generates. They are now independent and
  labelled distinctly.
- **AI-TGE — output location.** Artifacts are written under `.governance/test/`. The former
  top-level `.tge/` folder is retired.
- **AI-GCE — progressive tier activation under AI-DLC.** Because AI-DLC binds checks per stage
  rather than by team maturity, tier *scheduling* is suspended when the build method is AI-DLC;
  all checks activate together. Tier *assessment* — the readiness bands and score targets — is
  retained as dashboard reporting. Tier scheduling is unchanged for every other build method.

### Fixed

- **AI-GCE — hook inventory corrected.** Several internal listings disagreed about which hooks
  ship, and named some that had been converted to on-demand agents. The listings now agree, and
  a verification check that could fail on a correctly generated workspace has been corrected.
- **AI-TGE — hand-over contract corrected.** It described generated test *cases*; AI-TGE
  produces test *requirements* and never writes test code. Its declared output location now
  matches where it actually writes, and the Architecture Package is declared as an input.
- **Documentation — AI-DLC version references.** References to AI-DLC v1 across the family have
  been updated to reflect current AI-DLC.

## [0.1.0-beta.5] — 2026-08-09

First published changelog record for the AI-* PDLC Family — 11 injectable workflow packages that
take an AI coding assistant from a raw idea to a governed, ready-to-build workspace, with a human
approval gate at every step. Earlier pre-public betas (beta.1–beta.4) are folded into this entry.

### Added

**Packages (11, each independently installable and self-contained)**
- Portfolio layer — **AI-ILC** (evaluate raw ideas → routed Idea / Feature / Change-Request Brief; 6-stage funnel with intent routing), **AI-PILC** (raw requirement → Project Initiation Package; mints `projectId`; 6 gated phases), **AI-PPM** (many PIPs → portfolio governance, prioritization, dispatch; 5 phases / 10 stages + 7 opt-in extensions).
- Project layer — **AI-POLC** (→ Product Backlog Package; 6 phases / 16 stages + story elaboration + 7 extensions), **AI-UXD** (→ UX Design Package; personas → journeys → flows → design system, W3C tokens, WCAG 2.2 baseline), **AI-ADLC** (→ Architecture Package; C4 + ADRs + 10 opt-in extensions incl. DDD, Event Storming, CQRS, STRIDE threat modeling), **AI-DWG** (→ ready-to-code workspace; generate / reconcile / brownfield modes over 27 transforms).
- Quality companions — **AI-GCE** (→ compliance & enforcement layer: hooks, rules, process agents, audit log; 3-tier progressive maturity; Team Topologies enforcement), **AI-TGE** (→ test-governance layer: strategy, register, coverage, debt, defects; architecture-derived).
- Fabric engines — **AI-FLO** (edge router: reads state markers, routes the next hop, validates gates, flags conflicts; advisory), **AI-DFE** (data fabric: gathers Markdown → schema-validated JSON at `pdlc-ws/data/` for dashboards and roll-ups).

**Cross-cutting lenses (AI · Automation · Agentic)**
- **AI Lens** (`AI-Powered` / `No-AI`; toggle `_AILENS_`) — designs AI features across the chain: model-serving / RAG architecture, human-in-the-loop AI UX, AI governance & testing.
- **Automation Lens** (`Automated` / `Manual`; toggle `_AUTOLENS_`) — designs automated features: workflow automation and approval / monitoring / override UX.
- **Agentic** (derived where both lenses are active) — tool-use, memory, and reasoning-loop guidance; tool-permission / kill-switch governance; trajectory / step-cap testing.
- Threaded end-to-end: AI-PILC records the modes in the governance spine (`Lens_Status.md`) → AI-POLC tags features (`aiFeature` / `automationFeature`, derived `agenticProfile`) → AI-UXD / AI-ADLC design the facets → AI-DWG provisions scaffolding → AI-GCE / AI-TGE govern and test the tagged features via Layer-3 agents (`AIG__` / `ATG__` governance, `AIQ__` / `ATQ__` quality), including EU AI Act obligations. Adding a lens is a registry-only change.

**Chain & composition**
- Sequential chain AI-PILC → AI-POLC → AI-UXD → AI-ADLC → AI-DWG → AI-GCE + AI-TGE, with the optional portfolio layer (AI-ILC ⇢ AI-PILC ⇢ AI-PPM).
- Standalone or composable — each package runs alone or detects a sibling's output markers to enrich its work; a missing predecessor degrades gracefully.
- Produces the ready-to-code workspace that AI-DLC (Amazon's open-source build lifecycle) consumes.

**Workflow model**
- Human-in-the-loop approval gate at every stage — the AI proposes, you decide.
- Senior domain personas (PMO, CTO, DevOps, QA) so output reads as senior work.
- Three adaptive depth tiers (Minimal / Standard / Comprehensive).
- Brownfield-aware mode for injecting packages into existing codebases.

**Governance, fabric & triggers**
- Management Framework spine (shared governance; `LRN__` logs a lesson), Naming & Ownership convention, and Communication Fabric (family bindings, gate contracts, capability seams).
- Always-loaded session orchestrator that routes intent; deterministic package-activation keys (`_ILC_` … `_DFE_`) and the `_ACTIVE_` status key.
- Per-package governance / audit agents (e.g. `IQA__`, `ADA__`, `WIA__`, `TGV__`, `CVR__`, `DOD__`, `CRV__`) with tiered availability (Tier 1 / 2 / 3).
- Fabric health / integrity agents: `FHC__` / `FIA__` (AI-FLO), `DHC__` / `DFA__` (AI-DFE).

**Data, dashboards & multi-project**
- AI-DFE data surface via `DAT__` (gather → shape → distribute), with `DFA__` / `DHC__` integrity and readiness checks.
- Multi-project workspaces with the `_APROJ_` active-project switch and `projectId` correlation threaded throughout.
- Dashboard Framework plus extensions (AIFLC-PDLC-Dashboard, AIFLC-CommandBoard).

**Tooling, install & docs**
- Workspace HTML publishing — a browsable, self-contained shadow site via `HTM__` (AIFLC-HtmlExport extension); `.md` stays the single source of truth.
- Family upgrade agent `UPG__` — retrofits new output-feature improvements (clickable reference links, table + diagram pairing, lens tagging, and more) into an existing `pdlc-ws/` workspace, non-destructively and idempotently.
- Clickable reference links and table + Mermaid visual pairing in generated artifacts.
- Isolated `pdlc-ws/` output keeps the workspace root clean.
- Install guides for 8 platforms (Kiro, Amazon Q Developer, Cursor, Claude Code, Cline, GitHub Copilot [partial], OpenAI Codex, VS Code Agent) plus an interactive installer (PowerShell + Bash); whitepapers and 90+ HOW / WHY knowledge documents.

**Legal**
- Apache 2.0 license with Attribution Addendum + NOTICE; CONTRIBUTING, CLA, SECURITY policy, and a rollback policy.

### Known limitations
- GitHub Copilot support is partial (workspace-level instructions only).
- Additional assistants (Windsurf, Augment Code, Tabnine, JetBrains AI Assistant, Sourcegraph Cody, Continue, Aider) are expected to work but are not yet validated.

[Unreleased]: https://github.com/mbmd/AIPDLC/compare/v0.1.0-beta.6-r3...HEAD
[0.1.0-beta.6-r3]: https://github.com/mbmd/AIPDLC/compare/v0.1.0-beta.6-r2...v0.1.0-beta.6-r3
[0.1.0-beta.6-r2]: https://github.com/mbmd/AIPDLC/compare/v0.1.0-beta.6...v0.1.0-beta.6-r2
[0.1.0-beta.6]: https://github.com/mbmd/AIPDLC/compare/v0.1.0-beta.5...v0.1.0-beta.6
[0.1.0-beta.5]: https://github.com/mbmd/AIPDLC/releases/tag/v0.1.0-beta.5
