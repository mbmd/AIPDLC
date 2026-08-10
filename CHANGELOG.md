# Changelog

All notable changes to **AIFLC — the AI-* PDLC Family** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses pre-release (beta) versioning until the first stable release.
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-beta.2] — 2026-08-09

First public beta of the AI-* PDLC Family — 11 injectable workflow packages that take an
AI coding agent from a raw idea to a governed, ready-to-build workspace, with a human
approval gate at every step.

### Added

**Packages (11, each independently installable and self-contained)**
- Portfolio layer — **AI-ILC** (evaluate raw ideas → approved brief), **AI-PILC** (project initiation → Project Initiation Package), **AI-PPM** (govern a portfolio of projects).
- Project layer — **AI-POLC** (own the product backlog), **AI-UXD** (UX design), **AI-ADLC** (architecture design), **AI-DWG** (generate a ready-to-code workspace).
- Quality, alongside the build — **AI-GCE** (compliance governance derived from the architecture), **AI-TGE** (test strategy & coverage derived from the workspace).
- Fabric engines — **AI-FLO** (routes package-to-package handoffs), **AI-DFE** (data fabric: structured status for dashboards and roll-ups, via the `DAT__` / `DFA__` / `DHC__` triggers and a dashboard extension).

**Chain & composition**
- Sequential chain: AI-PILC → AI-POLC → AI-UXD → AI-ADLC → AI-DWG → AI-GCE + AI-TGE, with the optional portfolio layer (AI-ILC ⇢ AI-PILC ⇢ AI-PPM).
- Standalone **or** composable — each package runs alone, or detects a sibling's output markers to enrich its own work; missing predecessors degrade gracefully.
- Produces the ready-to-code workspace that AI-DLC (Amazon's open-source build lifecycle) consumes.

**Workflow model**
- Human-in-the-loop approval gate at every stage — the AI proposes, you decide; nothing auto-progresses.
- Per-package professional personas (PMO, CTO, DevOps, QA) so output reads as senior work.
- Three adaptive depth tiers (Minimal / Standard / Comprehensive) per package.
- Brownfield-aware mode for injecting packages into existing projects.

**Cross-package governance & fabric**
- Shared Management Framework spine, Naming & Ownership convention, and Dashboard Framework.
- Communication Fabric — gate contracts and family bindings for clean, machine-readable handoffs.
- Always-loaded session orchestrator that routes intent to the right package; per-package agents and trigger shortcuts.
- Isolated output workspace (`pdlc-ws/`) that keeps your project root clean; multi-project aware.

**Platform, install & docs**
- Install guides for 8 platforms (Kiro, Amazon Q Developer, Cursor, Claude Code, Cline, GitHub Copilot, OpenAI Codex, VS Code Agent) plus an interactive installer (PowerShell + Bash).
- Whitepapers and HOW/WHY reference material.

**Legal**
- Apache 2.0 license with Attribution Addendum + NOTICE; CONTRIBUTING, CLA, SECURITY policy, and a rollback policy.

### Known limitations
- GitHub Copilot support is partial (workspace-level instructions only).
- Additional assistants (Windsurf, Augment Code, Tabnine, JetBrains AI Assistant, Sourcegraph
  Cody, Continue, Aider) are expected to work but are not yet validated.

[0.1.0-beta.2]: https://github.com/mbmd/AIPDLC/releases/tag/v0.1.0-beta.2
