# Release Notes — AIFLC · The AI-* PDLC Family

Repository: [mbmd/AIPDLC](https://github.com/mbmd/AIPDLC) · Part of [AIFLC](https://github.com/mbmd/AIFLC) (AI Full Life Cycle)

> Human-readable notes for each release. For the terse, structured record see [CHANGELOG.md](./CHANGELOG.md).

---

## v0.1.0-beta.2 — 2026-08-09

The first public beta of the PDLC family: **11 injectable workflow packages** that guide an
AI coding assistant through professional software delivery — from a raw idea to a governed,
ready-to-build workspace — with a human approval gate at every step. No plugins, no APIs,
no lock-in: just markdown files your AI reads.

### What's inside

Eleven packages across two layers, plus two fabric engines:

- **Portfolio layer** — AI-ILC (evaluate ideas), AI-PILC (initiate a project), AI-PPM (govern a portfolio)
- **Project layer** — AI-POLC (own the backlog), AI-UXD (design UX), AI-ADLC (design architecture), AI-DWG (generate the workspace)
- **Quality, alongside the build** — AI-GCE (compliance governance), AI-TGE (test governance)
- **Fabric** — AI-FLO (routes handoffs between packages), AI-DFE (data fabric for dashboards and roll-ups)

The chain: **AI-PILC → AI-POLC → AI-UXD → AI-ADLC → AI-DWG → AI-GCE + AI-TGE**. Each package's
output is the next one's input — and each also runs standalone.

### Highlights

- **Human at every gate** — the AI proposes, you decide. Nothing auto-progresses.
- **Chained decisions** — context flows forward so nothing is lost, re-asked, or silently ignored.
- **Standalone or composable** — run a single package or the whole chain; siblings enrich each other through output markers, and a missing predecessor degrades gracefully.
- **Professional quality** — each package embeds a senior domain persona (PMO, CTO, DevOps, QA) so the output reads as senior work.
- **Governance derived, not bolted on** — AI-GCE derives compliance from the architecture; AI-TGE derives test strategy from the workspace.
- **Shared governance spine** — a common Management Framework, Naming & Ownership convention, Dashboard Framework, and Communication Fabric tie the packages together; AI-DFE rolls status up for dashboards.
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
