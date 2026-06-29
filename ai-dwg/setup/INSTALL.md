# AI-DWG — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-DWG is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-dwg"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-dwg
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-DWG writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── pdlc/
│   │       └── ai-dwg-rules/core-generator.md   ← always-loaded steering (core)
│   └── pdlc/
│       └── ai-dwg-rule-details/                 ← on-demand rule details
└── pdlc-ws/                                      ← AI-DWG OUTPUT lands here (created by installer)
```

> **Kiro split:** the core file goes under `.kiro/steering/pdlc/` (Kiro auto-loads only from `steering/`); rule-details go under `.kiro/pdlc/` (read on-demand by the core file).

---

## Manual Install (Per Platform)

If you prefer manual install, place the two artifacts at these locations (replace `<src>` with the path to the `ai-dwg` package source):

| Platform | Core file → | Rule-details → |
|----------|-------------|----------------|
| Kiro | `.kiro/steering/pdlc/ai-dwg-rules/core-generator.md` | `.kiro/pdlc/ai-dwg-rule-details/` |
| Amazon Q | `.amazonq/rules/pdlc/ai-dwg-rules/core-generator.md` | `.amazonq/pdlc/ai-dwg-rule-details/` |
| Cursor | `.cursor/rules/pdlc-ai-dwg-workflow.mdc` (prepend frontmatter: `---\ndescription: "AI-DWG"\nalwaysApply: true\n---`) | `.pdlc/ai-dwg-rule-details/` |
| Cline | `.clinerules/pdlc-ai-dwg-core.md` | `.pdlc/ai-dwg-rule-details/` |
| Claude Code | `CLAUDE_PDLC_AI_DWG.md` | `.pdlc/ai-dwg-rule-details/` |
| Copilot | `.github/copilot-instructions-pdlc-ai-dwg.md` | `.pdlc/ai-dwg-rule-details/` |

(Where the Claude Code filename uses the package code uppercased with hyphens as underscores, e.g. ai-dwg → AI_DWG.)

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Using AI-DWG, generate the development workspace from my architecture package".
4. AI-DWG output appears under `pdlc-ws/`.

---

## Notes

- The core file is always-loaded; rule-details load on demand.
- AI-DWG coexists with other AI-* packages — each is family-scoped under `pdlc/`. Run AI-ADLC first for architecture, then AI-DWG to generate the workspace.
- AI-DWG generates new steering files but never modifies manually-created ones.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Usage

### First Time (Full Generation)

```
Using AI-DWG, generate the development workspace from my architecture package.
The AP is located at: <path-to-architecture-package>
```

AI-DWG will read your Architecture Package, ask 2-4 configuration questions, and generate all workspace files in one pass.

### After Architecture Changes (Reconciliation)

```
Using AI-DWG, reconcile the workspace — the API Architecture was updated.
```

AI-DWG will detect what changed, propose workspace updates, and apply approved changes (preserving your customizations).

### Brownfield Overlay (Existing Codebase)

```
Using AI-DWG, add governance to this existing workspace.
```

AI-DWG will detect existing files and conventions, generate steering files (safe — new), merge configs additively (never overwrite), and skip existing operational docs.

---

## Compatibility

- **AI-ADLC v1.0:** Full support (core workflow output)
- **AI-ADLC v1.1:** Full support (6 extensions detected automatically)
- **Standalone AP:** Supported (without `adlc-state.md` — manual artifact mapping required)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure the rule-details folder is at the correct location for your platform (see Manual Install) |
| Extensions not detected | Verify `adlc-state.md` exists in the AP folder with an `Enabled Extensions` section |
| Conditional files not generated | Check that the AP contains the trigger artifact (see core-generator conditional logic table) |
| Reconciliation overwrites customizations | Ensure team-added content is NOT placed between `<!-- begin: AP-sourced -->` markers |

---

## Test Mode (Optional)

AI-DWG includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode is **automatically installed** when the core rules are placed — `test-mode.md` is included with `inclusion: manual` frontmatter, meaning it only activates when you reference it.

**To activate:** Type `#test-mode` in your chat prompt, or say "activate test mode".

**To verify it's available:** Check the Steering Files panel — `test-mode` should appear under manual-inclusion files.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot

For non-Kiro platforms, test mode requires manually including the instructions:

```powershell
# Windows — copy test-mode steering alongside the core file
Copy-Item "<src>\ai-dwg-rules\test-mode.md" "<your-rules-folder>\"
```

```bash
# macOS/Linux
cp <src>/ai-dwg-rules/test-mode.md <your-rules-folder>/
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
