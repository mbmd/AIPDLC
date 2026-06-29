# AI-PILC — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-PILC is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-pilc"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-pilc
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-PILC writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── pdlc/
│   │       └── ai-pilc-rules/core-workflow.md   ← always-loaded steering (core)
│   └── pdlc/
│       └── ai-pilc-rule-details/                ← on-demand rule details
└── pdlc-ws/                                      ← AI-PILC OUTPUT lands here (created by installer)
```

> **Kiro split:** the core file goes under `.kiro/steering/pdlc/` (Kiro auto-loads only from `steering/`); rule-details go under `.kiro/pdlc/` (read on-demand by the core file).

---

## Manual Install (Per Platform)

If you prefer manual install, place the two artifacts at these locations (replace `<src>` with the path to the `ai-pilc` package source):

| Platform | Core file → | Rule-details → |
|----------|-------------|----------------|
| Kiro | `.kiro/steering/pdlc/ai-pilc-rules/core-workflow.md` | `.kiro/pdlc/ai-pilc-rule-details/` |
| Amazon Q | `.amazonq/rules/pdlc/ai-pilc-rules/core-workflow.md` | `.amazonq/pdlc/ai-pilc-rule-details/` |
| Cursor | `.cursor/rules/pdlc-ai-pilc-workflow.mdc` (prepend frontmatter: `---\ndescription: "AI-PILC"\nalwaysApply: true\n---`) | `.pdlc/ai-pilc-rule-details/` |
| Cline | `.clinerules/pdlc-ai-pilc-core.md` | `.pdlc/ai-pilc-rule-details/` |
| Claude Code | `CLAUDE_PDLC_AI_PILC.md` | `.pdlc/ai-pilc-rule-details/` |
| Copilot | `.github/copilot-instructions-pdlc-ai-pilc.md` | `.pdlc/ai-pilc-rule-details/` |

(Where the Claude Code filename uses the package code uppercased with hyphens as underscores, e.g. ai-pilc → AI_PILC.)

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Using AI-PILC, initiate a project".
4. AI-PILC output appears under `pdlc-ws/`.

---

## Notes

- The core file is always-loaded; rule-details load on demand.
- AI-PILC coexists with other AI-* packages — each is family-scoped under `pdlc/`.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Test Mode (Optional)

AI-PILC includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode is **automatically installed** when the core rules are placed — `test-mode.md` is included with `inclusion: manual` frontmatter, meaning it only activates when you reference it.

**To activate:** Type `#test-mode` in your chat prompt, or say "activate test mode".

**To verify it's available:** Check the Steering Files panel — `test-mode` should appear under manual-inclusion files.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot

For non-Kiro platforms, test mode requires manually including the instructions:

```powershell
# Windows — copy test-mode steering alongside the core file
Copy-Item "<src>\ai-pilc-rules\test-mode.md" "<your-rules-folder>\"
```

```bash
# macOS/Linux
cp <src>/ai-pilc-rules/test-mode.md <your-rules-folder>/
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
