# AI-PPM — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-PPM is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-ppm"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-ppm
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-PPM writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── pdlc/
│   │       └── ai-ppm-rules/core-engine.md   ← always-loaded steering (core)
│   └── pdlc/
│       └── ai-ppm-rule-details/              ← on-demand rule details
└── pdlc-ws/                                   ← AI-PPM OUTPUT lands here (created by installer)
```

> **Kiro split:** the core file goes under `.kiro/steering/pdlc/` (Kiro auto-loads only from `steering/`); rule-details go under `.kiro/pdlc/` (read on-demand by the core file).

---

## Manual Install (Per Platform)

If you prefer manual install, place the two artifacts at these locations (replace `<src>` with the path to the `ai-ppm` package source):

| Platform | Core file → | Rule-details → |
|----------|-------------|----------------|
| Kiro | `.kiro/steering/pdlc/ai-ppm-rules/core-engine.md` | `.kiro/pdlc/ai-ppm-rule-details/` |
| Amazon Q | `.amazonq/rules/pdlc/ai-ppm-rules/core-engine.md` | `.amazonq/pdlc/ai-ppm-rule-details/` |
| Cursor | `.cursor/rules/pdlc-ai-ppm-workflow.mdc` (prepend frontmatter: `---\ndescription: "AI-PPM"\nalwaysApply: true\n---`) | `.pdlc/ai-ppm-rule-details/` |
| Cline | `.clinerules/pdlc-ai-ppm-core.md` | `.pdlc/ai-ppm-rule-details/` |
| Claude Code | `CLAUDE_PDLC_AI_PPM.md` | `.pdlc/ai-ppm-rule-details/` |
| Copilot | `.github/copilot-instructions-pdlc-ai-ppm.md` | `.pdlc/ai-ppm-rule-details/` |

(Where the Claude Code filename uses the package code uppercased with hyphens as underscores, e.g. ai-ppm → AI_PPM.)

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Using AI-PPM, manage my project portfolio".
4. AI-PPM output appears under `pdlc-ws/`.

---

## Notes

- The core file is always-loaded; rule-details load on demand.
- AI-PPM coexists with other AI-* packages — each is family-scoped under `pdlc/`. Install order doesn't matter; each package detects predecessors by marker file.
- AI-PPM communicates with Project-layer packages exclusively through AI-FLO (the bidirectional data courier).
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Test Mode (Optional)

AI-PPM includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode is **automatically installed** when the core rules are placed — `test-mode.md` is included with `inclusion: manual` frontmatter, meaning it only activates when you reference it.

**To activate:** Type `#test-mode` in your chat prompt, or say "activate test mode".

**To verify it's available:** Check the Steering Files panel — `test-mode` should appear under manual-inclusion files.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot

For non-Kiro platforms, test mode requires manually including the instructions:

```powershell
# Windows — copy test-mode steering alongside the core file
Copy-Item "<src>\ai-ppm-rules\test-mode.md" "<your-rules-folder>\"
```

```bash
# macOS/Linux
cp <src>/ai-ppm-rules/test-mode.md <your-rules-folder>/
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
