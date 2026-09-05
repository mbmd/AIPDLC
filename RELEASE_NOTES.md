# Release Notes — AIFLC · The AI-* PDLC (Product Development Life Cycle) Family

Repository: [mbmd/AIPDLC](https://github.com/mbmd/AIPDLC) · Part of [AIFLC](https://github.com/mbmd/AIFLC) (AI Full Life Cycle)

> Human-readable notes for each release. For the terse, structured record see [CHANGELOG.md](./CHANGELOG.md).

---

## v0.1.0-beta.6 — 2026-09-01

**AI-DLC v2 support across the build-and-govern surface.** Three packages step to `1.1.0` — AI-DWG
(AI-Driven Workspace Generator), AI-GCE (AI-Driven Governance & Compliance Engine) and AI-TGE
(AI-Driven Test Governance Engine) — so the family can target AI-DLC (AI-Driven Development Life
Cycle — Amazon's open-source build lifecycle) v2 as a build method. When you choose AI-DLC,
AI-DWG now pre-seeds the workspace in the shape v2 reads (behavioural rules, per-agent knowledge,
your design documents, and a code knowledge base on greenfield projects), so v2's own stages affirm
that context instead of interviewing you from scratch. AI-GCE can run its governance checks as
deterministic AI-DLC sensors and reports which enforcement surface is present, and AI-TGE re-targets
its coverage to v2's outcome. **Every other build method is unchanged** — the build method is now an
explicit setup question with five recognised values, and nothing new appears unless the method calls
for it. GitHub SpecKit is also supported (generates a constitution from your canonical rules).

Also in this release: AI-TGE degraded runs are now clearly reported rather than looking complete;
AI-TGE's test-governance depth and AI-DLC's test volume are separated into independent settings;
AI-TGE output moves under `.governance/test/`; and several internal corrections (AI-GCE hook
inventory, AI-TGE hand-over contract, AI-DLC version references). See [CHANGELOG.md](./CHANGELOG.md)
for the full structured list.

---

## v0.1.0-beta.5 — 2026-08-09

The current public beta of the PDLC family: **11 injectable workflow packages** that guide an
AI coding assistant through professional software delivery — from a raw idea to a governed,
ready-to-build workspace — with a human approval gate at every step. No plugins, no APIs,
no lock-in: just markdown files your AI reads. These notes describe the full feature set as of
`beta.5` (earlier betas are folded in).

### What's inside

Eleven packages across two layers, plus two fabric engines:

- **Portfolio layer** — AI-ILC (AI-Driven Idea Life Cycle — evaluate ideas), AI-PILC (AI-Driven Project Initiation Life Cycle — initiate a project), AI-PPM (AI-Driven Project Portfolio Management — govern a portfolio)
- **Project layer** — AI-POLC (AI-Driven Product Ownership Life Cycle — own the backlog), AI-UXD (AI-Driven UX Design — design UX), AI-ADLC (AI-Driven Architecture Design Life Cycle — design architecture), AI-DWG (generate the workspace)
- **Quality, alongside the build** — AI-GCE (compliance governance), AI-TGE (test governance)
- **Fabric** — AI-FLO (AI-Driven Flow Orchestrator — routes handoffs), AI-DFE (AI-Driven Data Fabric Engine — data fabric for dashboards and roll-ups)
- **Cross-cutting lenses** — an AI Lens and an Automation Lens (and derived Agentic coverage) that, when switched on, make every design package apply the matching facet

The chain: **AI-PILC → AI-POLC → AI-UXD → AI-ADLC → AI-DWG → AI-GCE + AI-TGE**. Each package's
output is the next one's input — and each also runs standalone.

### Highlights

- **Human at every gate** — the AI proposes, you decide. Nothing auto-progresses.
- **Chained decisions** — context flows forward so nothing is lost, re-asked, or silently ignored.
- **Standalone or composable** — run a single package or the whole chain; siblings enrich each other through output markers, and a missing predecessor degrades gracefully.
- **AI & Automation lenses** — flip on the AI Lens (`_AILENS_`) or Automation Lens (`_AUTOLENS_`) and every package designs the matching facet: model-serving/RAG and AI UX, or workflow automation and control UX; where both apply, agentic coverage is derived. Dedicated governance and quality agents — `AIG__` (AI Governance — EU AI Act / responsible-AI checks) and `AIQ__` (AI Quality & Drift — golden-set eval, drift detection), plus `ATG__` (Automation Governance — audit trail, kill-switch checks) and `ATQ__` (Automation Quality — idempotency, exception-path verification) — check the tagged features, EU AI Act obligations included.
- **Professional quality** — each package embeds a senior domain persona (PMO, CTO, DevOps, QA).
- **Governance derived, not bolted on** — AI-GCE derives compliance from the architecture; AI-TGE derives test strategy from the workspace; a shared Management Framework spine and Communication Fabric tie the chain together.
- **Data, dashboards & multi-project** — AI-DFE publishes a clean data surface (`DAT__`) for dashboards and roll-ups, and workspaces can hold many projects with the `_APROJ_` switch.
- **Browsable HTML** — publish the whole workspace as a self-contained HTML shadow with `HTM__`; your `.md` files stay the source of truth.
- **Stays current** — the `UPG__` upgrade agent retrofits new output-feature improvements into an existing workspace, non-destructively.
- **Adaptive depth** — Minimal / Standard / Comprehensive tiers scale to project complexity.
- **Brownfield-aware** — a first-class mode for injecting packages into an existing codebase.
- **File-based & portable** — everything is markdown: version-controlled, auditable, yours. Outputs land in `pdlc-ws/`, keeping your project root clean.
- **Feeds the build** — produces the ready-to-code workspace that AI-DLC (Amazon's open-source build lifecycle) consumes.

### Getting started

1. Clone this repo into a temporary `.aiflc-src/` folder (not your workspace root).
2. Run the installer from the repo root and pick the packages you want:
   - Windows: `.\installer\install.ps1`
   - macOS / Linux: `./installer/install.sh`
3. Delete `.aiflc-src/`. Packages install under `.aiflc/pdlc/`; outputs are written to `pdlc-ws/`, so your workspace root stays clean.
4. In your AI IDE, activate a package — e.g. `Using AI-PILC, help me initiate this project from my requirements.`

See the [README](./README.md) and [INSTALL_GUIDE.md](./INSTALL_GUIDE.md) for the full platform matrix and per-package steps.

### Supported platforms

Kiro (reference implementation), Amazon Q Developer, Cursor, Claude Code, Cline, OpenAI Codex,
and the VS Code agent framework ship with install steps. GitHub Copilot is **partial**
(workspace-level instructions only). Other assistants (Windsurf, Augment Code, Tabnine,
JetBrains AI Assistant, Sourcegraph Cody, Continue, Aider) are expected to work but are not
yet validated.

### Known limitations (beta)

- This is a **beta** — package interfaces and outputs may change before the stable 1.0.
- GitHub Copilot support is partial.
- **Brownfield use:** back up first and try a test branch — packages generate files into your
  workspace. See the Brownfield Deployment Warning in the [README](./README.md).

### License

**Apache License 2.0 with Attribution Addendum** — free for personal, commercial, educational,
and organizational use; modify and redistribute freely. One condition: any distributed product
substantially based on this work must credit *"Built on AIFLC by Mohammad Maheri."* See
[LICENSE](./LICENSE) and [NOTICE](./NOTICE) for full terms.

---

*Part of [AIFLC](https://github.com/mbmd/AIFLC) — the AI Full Life Cycle.*
