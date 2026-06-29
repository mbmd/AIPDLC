# AI-ILC — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-ILC is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-ilc"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-ilc
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-ILC writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── pdlc/
│   │       └── ai-ilc-rules/core-workflow.md   ← always-loaded steering (core)
│   └── pdlc/
│       └── ai-ilc-rule-details/                ← on-demand rule details
└── pdlc-ws/                                     ← AI-ILC OUTPUT lands here (created by installer)
```

> **Kiro split:** the core file goes under `.kiro/steering/pdlc/` (Kiro auto-loads only from `steering/`); rule-details go under `.kiro/pdlc/` (read on-demand by the core file).

---

## Manual Install (Per Platform)

If you prefer manual install, place the two artifacts at these locations (replace `<src>` with the path to the `ai-ilc` package source):

| Platform | Core file → | Rule-details → |
|----------|-------------|----------------|
| Kiro | `.kiro/steering/pdlc/ai-ilc-rules/core-workflow.md` | `.kiro/pdlc/ai-ilc-rule-details/` |
| Amazon Q | `.amazonq/rules/pdlc/ai-ilc-rules/core-workflow.md` | `.amazonq/pdlc/ai-ilc-rule-details/` |
| Cursor | `.cursor/rules/pdlc-ai-ilc-workflow.mdc` (prepend frontmatter: `---\ndescription: "AI-ILC"\nalwaysApply: true\n---`) | `.pdlc/ai-ilc-rule-details/` |
| Cline | `.clinerules/pdlc-ai-ilc-core.md` | `.pdlc/ai-ilc-rule-details/` |
| Claude Code | `CLAUDE_PDLC_AI_ILC.md` | `.pdlc/ai-ilc-rule-details/` |
| Copilot | `.github/copilot-instructions-pdlc-ai-ilc.md` | `.pdlc/ai-ilc-rule-details/` |

(Where the Claude Code filename uses the package code uppercased with hyphens as underscores, e.g. ai-ilc → AI_ILC.)

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Using AI-ILC, help me ...".
4. AI-ILC output appears under `pdlc-ws/`.

---

## Notes

- The core file is always-loaded; rule-details load on demand.
- AI-ILC coexists with other AI-* packages — each is family-scoped under `pdlc/`.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Using AI-ILC

After installation, these phrases activate the workflow:

| Say | Effect |
|-----|--------|
| "I have an idea" | Start new idea capture |
| "I have a new idea for..." | Start capture with initial context |
| "Resume" | Continue a previously-started idea |
| "Show the idea register" | Display all ideas in the pipeline |
| "Revisit parked idea" | Re-enter a parked idea |

---

## Configuration (Optional)

### Custom Evaluation Rubric

If your organization wants custom scoring criteria, create a steering file at `.kiro/steering/pdlc/ilc-evaluation-config.md` and define custom criteria there. AI-ILC's two-source model will use your criteria where provided and fall back to the built-in baseline where you're silent.

### Persona Steering (Optional)

If you want AI-ILC's personas to use your organization's voice/style, ensure the relevant persona files are in your `.kiro/steering/` folder. AI-ILC references `#persona-product-manager` (lead at most stages), `#persona-process-designer` (lead at Scope), and sub-roles: business-analyst, financial-analyst, resource-planner, risk-analyst, change-manager.

---

## Test Mode (Optional)

AI-ILC includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode is **automatically installed** when the core rules are placed — `test-mode.md` is included with `inclusion: manual` frontmatter, meaning it only activates when you reference it.

**To activate:** Type `#test-mode` in your chat prompt, or say "activate test mode".

**To verify it's available:** Check the Steering Files panel — `test-mode` should appear under manual-inclusion files.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot

For non-Kiro platforms, test mode requires manually including the instructions:

```powershell
# Windows — copy test-mode steering alongside the core file
Copy-Item "<src>\ai-ilc-rules\test-mode.md" "<your-rules-folder>\"
```

```bash
# macOS/Linux
cp <src>/ai-ilc-rules/test-mode.md <your-rules-folder>/
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
