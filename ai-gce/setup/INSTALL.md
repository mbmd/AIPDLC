# AI-GCE — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-GCE is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-gce"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-gce
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-GCE writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── pdlc/
│   │       └── ai-gce-rules/core-generator.md   ← always-loaded steering (core)
│   └── pdlc/
│       └── ai-gce-rule-details/                 ← on-demand rule details
└── pdlc-ws/                                      ← AI-GCE OUTPUT lands here (created by installer)
```

> **Kiro split:** the core file goes under `.kiro/steering/pdlc/` (Kiro auto-loads only from `steering/`); rule-details go under `.kiro/pdlc/` (read on-demand by the core file).

---

## Manual Install (Per Platform)

If you prefer manual install, place the two artifacts at these locations (replace `<src>` with the path to the `ai-gce` package source):

| Platform | Core file → | Rule-details → |
|----------|-------------|----------------|
| Kiro | `.kiro/steering/pdlc/ai-gce-rules/core-generator.md` | `.kiro/pdlc/ai-gce-rule-details/` |
| Amazon Q | `.amazonq/rules/pdlc/ai-gce-rules/core-generator.md` | `.amazonq/pdlc/ai-gce-rule-details/` |
| Cursor | `.cursor/rules/pdlc-ai-gce-workflow.mdc` (prepend frontmatter: `---\ndescription: "AI-GCE"\nalwaysApply: true\n---`) | `.pdlc/ai-gce-rule-details/` |
| Cline | `.clinerules/pdlc-ai-gce-core.md` | `.pdlc/ai-gce-rule-details/` |
| Claude Code | `CLAUDE_PDLC_AI_GCE.md` | `.pdlc/ai-gce-rule-details/` |
| Copilot | `.github/copilot-instructions-pdlc-ai-gce.md` | `.pdlc/ai-gce-rule-details/` |

(Where the Claude Code filename uses the package code uppercased with hyphens as underscores, e.g. ai-gce → AI_GCE.)

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Start a chat: "Using AI-GCE, generate the compliance engine for this workspace".
4. AI-GCE output appears under `pdlc-ws/`.

---

## Notes

- The core file is always-loaded; rule-details load on demand.
- AI-GCE coexists with other AI-* packages — each is family-scoped under `pdlc/`. Run AI-DWG first to generate the development workspace, then AI-GCE to derive compliance.
- AI-GCE reads existing steering files but never modifies them.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Input Prerequisites

AI-GCE derives a compliance layer by reading an AI-DWG development workspace. For full derivation it expects these steering files in the target workspace:

- `.kiro/steering/workspace-rules.md` (marker file — MUST exist)
- `.kiro/steering/tech-stack.md` (technology drives hook patterns)
- `.kiro/steering/module-structure.md` (module paths drive hook patterns)

Without these, AI-GCE can only apply the 10 built-in baseline rules.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure the rule-details folder is at the correct location for your platform (see Manual Install) |
| "No steering files found" | Ensure `.kiro/steering/workspace-rules.md` exists (minimum requirement) |
| Only baseline rules generated | Steering files are missing or incomplete — add `tech-stack.md` and `module-structure.md` for full derivation |
| Hooks not firing | Check `.kiro/hooks/ENFORCEMENT-GUIDE.md` for tier-based activation instructions |
| Re-derivation overwrites customs | Ensure team-added rules are marked with `<!-- custom -->` comments |

---

## Uninstallation

To remove AI-GCE generated output from a workspace (does NOT affect steering files from AI-DWG):

```powershell
# Windows (PowerShell)
Remove-Item -Recurse -Force ".kiro\hooks"
Remove-Item -Recurse -Force ".governance"
Remove-Item -Force ".compliance-state.json"
Remove-Item -Force "docs\compliance-dashboard.md"
```

```bash
# macOS/Linux
rm -rf .kiro/hooks/
rm -rf .governance/
rm -f .compliance-state.json
rm -f management_framework/dashboards/compliance-dashboard.md
```

---

## Test Mode (Optional)

AI-GCE includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode is **automatically installed** when the core rules are placed — `test-mode.md` is included with `inclusion: manual` frontmatter, meaning it only activates when you reference it.

**To activate:** Type `#test-mode` in your chat prompt, or say "activate test mode".

**To verify it's available:** Check the Steering Files panel — `test-mode` should appear under manual-inclusion files.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot

For non-Kiro platforms, test mode requires manually including the instructions:

```powershell
# Windows — copy test-mode steering alongside the core file
Copy-Item "<src>\ai-gce-rules\test-mode.md" "<your-rules-folder>\"
```

```bash
# macOS/Linux
cp <src>/ai-gce-rules/test-mode.md <your-rules-folder>/
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
