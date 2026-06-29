# AI-TGE — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-TGE is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-tge"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-tge
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-TGE writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── pdlc/
│   │       └── ai-tge-rules/core-engine.md   ← always-loaded steering (core)
│   └── pdlc/
│       └── ai-tge-rule-details/              ← on-demand rule details
└── pdlc-ws/                                   ← AI-TGE OUTPUT lands here (created by installer)
```

> **Kiro split:** the core file goes under `.kiro/steering/pdlc/` (Kiro auto-loads only from `steering/`); rule-details go under `.kiro/pdlc/` (read on-demand by the core file).

---

## Manual Install (Per Platform)

If you prefer manual install, place the two artifacts at these locations (replace `<src>` with the path to the `ai-tge` package source):

| Platform | Core file → | Rule-details → |
|----------|-------------|----------------|
| Kiro | `.kiro/steering/pdlc/ai-tge-rules/core-engine.md` | `.kiro/pdlc/ai-tge-rule-details/` |
| Amazon Q | `.amazonq/rules/pdlc/ai-tge-rules/core-engine.md` | `.amazonq/pdlc/ai-tge-rule-details/` |
| Cursor | `.cursor/rules/pdlc-ai-tge-workflow.mdc` (prepend frontmatter: `---\ndescription: "AI-TGE"\nalwaysApply: true\n---`) | `.pdlc/ai-tge-rule-details/` |
| Cline | `.clinerules/pdlc-ai-tge-core.md` | `.pdlc/ai-tge-rule-details/` |
| Claude Code | `CLAUDE_PDLC_AI_TGE.md` | `.pdlc/ai-tge-rule-details/` |
| Copilot | `.github/copilot-instructions-pdlc-ai-tge.md` | `.pdlc/ai-tge-rule-details/` |

(Where the Claude Code filename uses the package code uppercased with hyphens as underscores, e.g. ai-tge → AI_TGE.)

> **Note:** On Kiro, `test-mode.md` ships alongside `core-engine.md` in `ai-tge-rules/` with `inclusion: manual` frontmatter (see Test Mode below).

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Using AI-TGE, derive a test governance strategy for this project".
4. AI-TGE output appears under `pdlc-ws/`.

---

## Notes

- The core file is always-loaded; rule-details load on demand.
- AI-TGE coexists with other AI-* packages — each is family-scoped under `pdlc/`. It reads AP (AI-ADLC) + DW (AI-DWG) and observes AI-DLC v1; it reads existing steering files but never modifies them.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## First Interaction

After installation, start AI-TGE with any of these prompts:

| Prompt | What Happens |
|--------|-------------|
| "Derive a test governance strategy" | Full strategy phase: detect inputs → read architecture → derive tests → assess brownfield → generate strategy → score risks |
| "Check my test coverage" | Observation: scan test directories, update register, produce coverage report |
| "What tests should I have?" | Architecture-only: read AP and derive required tests from commitments |
| "Assess my existing tests" | Brownfield: scan existing tests, map to architecture, identify gaps |
| "Log a defect" | Defect logging: structured bug entry with governance linkage |

AI-TGE will auto-detect your workspace mode (Full Chain / Architecture Only / Brownfield / Observation Only) based on what inputs exist.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure the rule-details folder is at the correct location for your platform (see Manual Install) |
| "No inputs detected" | Provide an Architecture Package path, or ensure test directories exist for brownfield mode |
| Only baseline tests derived | No Architecture Package found — provide AP for architecture-specific test derivation |
| State file not persisting | Ensure the AI-TGE output folder under `pdlc-ws/` is not gitignored if you want cross-session persistence |
| Coverage report shows 0% | Run brownfield assessment (Stage 4) to scan existing tests against the register |
| Risk scores all identical | Review architecture — uniform scoring indicates insufficient differentiation in the register |

---

## Uninstallation

To remove AI-TGE generated output, delete its output folder under the family workspace (`pdlc-ws/`). This removes all generated test governance artifacts (strategy, register, coverage reports, debt scorecard, defect log, state file). The AI-TGE package rules in your steering folder remain until manually removed.

---

## Test Mode (Optional)

AI-TGE includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode is **automatically installed** when the core rules are placed — `test-mode.md` is included with `inclusion: manual` frontmatter, meaning it only activates when you reference it.

**To activate:** Type `#test-mode` in your chat prompt, or say "activate test mode".

**To verify it's available:** Check the Steering Files panel — `test-mode` should appear under manual-inclusion files.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot

For non-Kiro platforms, test mode requires manually including the instructions:

```powershell
# Windows — copy test-mode steering alongside the core file
Copy-Item "<src>\ai-tge-rules\test-mode.md" "<your-rules-folder>\"
```

```bash
# macOS/Linux
cp <src>/ai-tge-rules/test-mode.md <your-rules-folder>/
```

Then tell the AI: "I want to use test mode" — and it will follow the test mode instructions.

> **Note:** On platforms without `inclusion: manual` support, `test-mode.md` loads alongside the core file. To avoid unwanted checkpoints, keep it in a separate location and only include it when you want test mode active.

### What Test Mode Does

- Adds brief feedback checkpoints after each phase (non-blocking — always skippable)
- Assists in filling structured bug/improvement/RCA templates via conversation
- Saves findings to a local `test-feedback-outbox/` folder (gitignored, never transmitted)
- Submission to maintainers is 100% manual and opt-in

### Privacy

- ❌ No network calls, no telemetry, no data collection
- ❌ No PII fields in templates
- ✅ All data stays local until you manually submit
- ✅ Review obligation rests entirely with you (the end user)

See `TEST_MODE_USER_GUIDE.md` (in this folder) for the full user guide.
