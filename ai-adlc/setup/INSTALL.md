# AI-ADLC — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-ADLC is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-adlc"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-adlc
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-ADLC writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── pdlc/
│   │       └── ai-adlc-rules/core-workflow.md   ← always-loaded steering (core)
│   └── pdlc/
│       └── ai-adlc-rule-details/                ← on-demand rule details
└── pdlc-ws/                                      ← AI-ADLC OUTPUT lands here (created by installer)
```

> **Kiro split:** the core file goes under `.kiro/steering/pdlc/` (Kiro auto-loads only from `steering/`); rule-details go under `.kiro/pdlc/` (read on-demand by the core file).

---

## Manual Install (Per Platform)

If you prefer manual install, place the two artifacts at these locations (replace `<src>` with the path to the `ai-adlc` package source):

| Platform | Core file → | Rule-details → |
|----------|-------------|----------------|
| Kiro | `.kiro/steering/pdlc/ai-adlc-rules/core-workflow.md` | `.kiro/pdlc/ai-adlc-rule-details/` |
| Amazon Q | `.amazonq/rules/pdlc/ai-adlc-rules/core-workflow.md` | `.amazonq/pdlc/ai-adlc-rule-details/` |
| Cursor | `.cursor/rules/pdlc-ai-adlc-workflow.mdc` (prepend frontmatter: `---\ndescription: "AI-ADLC"\nalwaysApply: true\n---`) | `.pdlc/ai-adlc-rule-details/` |
| Cline | `.clinerules/pdlc-ai-adlc-core.md` | `.pdlc/ai-adlc-rule-details/` |
| Claude Code | `CLAUDE_PDLC_AI_ADLC.md` | `.pdlc/ai-adlc-rule-details/` |
| Copilot | `.github/copilot-instructions-pdlc-ai-adlc.md` | `.pdlc/ai-adlc-rule-details/` |

(Where the Claude Code filename uses the package code uppercased with hyphens as underscores, e.g. ai-adlc → AI_ADLC.)

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Using AI-ADLC, design the architecture for this system".
4. AI-ADLC output appears under `pdlc-ws/`.

---

## Notes

- The core file is always-loaded; rule-details load on demand.
- AI-ADLC coexists with other AI-* packages — each is family-scoped under `pdlc/`. Run AI-PILC first for project initiation, then AI-ADLC for architecture.
- Extensions are opt-in — they activate only when you request them or the architecture justifies them.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure the rule-details folder is at the correct location for your platform (see Manual Install) |
| Extensions not activating | Extensions are opt-in — they activate only when you request them or architecture justifies them |
| Core file not loading | Verify it's in the correct steering location for your platform |
| State file not created | State is created on first interaction — start a chat using the activation phrase |

---

## Test Mode (Optional)

AI-ADLC includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode is **automatically installed** when the core rules are placed — `test-mode.md` is included with `inclusion: manual` frontmatter, meaning it only activates when you reference it.

**To activate:** Type `#test-mode` in your chat prompt, or say "activate test mode".

**To verify it's available:** Check the Steering Files panel — `test-mode` should appear under manual-inclusion files.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot

For non-Kiro platforms, test mode requires manually including the instructions:

```powershell
# Windows — copy test-mode steering alongside the core file
Copy-Item "<src>\ai-adlc-rules\test-mode.md" "<your-rules-folder>\"
```

```bash
# macOS/Linux
cp <src>/ai-adlc-rules/test-mode.md <your-rules-folder>/
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
