# AI-FLO — Installation Guide

## Recommended: Family Installer

The easiest way to install AI-FLO is via the AI-* Family installer (from the family root folder):

### Windows (PowerShell)
```powershell
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project" -Platform kiro -Packages "ai-flo"
```

### macOS / Linux
```bash
./installer/install.sh --target ~/path/to/your/project --platform kiro --packages ai-flo
```

The installer places package files in the correct location for your platform and creates the family workspace (`pdlc-ws/`) where AI-FLO writes its output.

---

## What Gets Installed (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── pdlc/
│   │       └── ai-flo-rules/core-engine.md   ← always-loaded steering (core)
│   ├── pdlc/
│   │   ├── ai-flo-rule-details/              ← on-demand rule details
│   │   ├── FAMILY_BINDINGS.md                ← fabric trio (routing graph) — REQUIRED
│   │   ├── GATE_PROTOCOL.md                  ← fabric trio (gate matching)  — REQUIRED
│   │   └── FAMILY_INTERFACE.md               ← fabric trio (discovery)      — REQUIRED
│   └── agents/
│       ├── flo-health-check.md               ← FHC__ health check (Kiro)
│       └── flow-integrity-agent.md           ← FIA__ integrity agent (Kiro)
└── pdlc-ws/                                   ← AI-FLO OUTPUT lands here (created by installer)
```

> **Kiro split:** the core file goes under `.kiro/steering/pdlc/` (Kiro auto-loads only from `steering/`); rule-details + the fabric trio go under `.kiro/pdlc/` (read on-demand by the core file).

> **Fabric trio (REQUIRED):** AI-FLO reads `FAMILY_BINDINGS.md`, `GATE_PROTOCOL.md`, and `FAMILY_INTERFACE.md` at runtime to build its routing graph. Without them FLO returns **NOT READY** — "no bindings = no routing; FLO never invents routes." The installer deploys them automatically; manual installers must copy them (see below). AI-FLO runs in the **planning / orchestration workspace** (where the lifecycle packages live), never inside an AI-DWG-generated dev workspace — so the trio belongs here, not in a generated workspace.

---

## Manual Install (Per Platform)

If you prefer manual install, place the two artifacts at these locations (replace `<src>` with the path to the `ai-flo` package source):

| Platform | Core file → | Rule-details → |
|----------|-------------|----------------|
| Kiro | `.kiro/steering/pdlc/ai-flo-rules/core-engine.md` | `.kiro/pdlc/ai-flo-rule-details/` |
| Amazon Q | `.amazonq/rules/pdlc/ai-flo-rules/core-engine.md` | `.amazonq/pdlc/ai-flo-rule-details/` |
| Cursor | `.cursor/rules/pdlc-ai-flo-workflow.mdc` (prepend frontmatter: `---\ndescription: "AI-FLO"\nalwaysApply: true\n---`) | `.pdlc/ai-flo-rule-details/` |
| Cline | `.clinerules/pdlc-ai-flo-core.md` | `.pdlc/ai-flo-rule-details/` |
| Claude Code | `CLAUDE_PDLC_AI_FLO.md` | `.pdlc/ai-flo-rule-details/` |
| Copilot | `.github/copilot-instructions-pdlc-ai-flo.md` | `.pdlc/ai-flo-rule-details/` |

(Where the Claude Code filename uses the package code uppercased with hyphens as underscores, e.g. ai-flo → AI_FLO.)

### Manual: copy the fabric trio (REQUIRED)

After placing the core + rule-details, copy the three fabric files from the family root into the **family rule-details root** for your platform (the parent of `ai-flo-rule-details/`):

| Platform | Fabric trio → |
|----------|---------------|
| Kiro | `.kiro/pdlc/` |
| Amazon Q | `.amazonq/pdlc/` |
| Cursor / Cline / Claude Code / Copilot | `.pdlc/` |

```powershell
# Windows (PowerShell) — Kiro example
Copy-Item "<family-root>\FAMILY_BINDINGS.md","<family-root>\GATE_PROTOCOL.md","<family-root>\FAMILY_INTERFACE.md" ".kiro\pdlc\"
```

```bash
# macOS/Linux — Kiro example
cp <family-root>/FAMILY_BINDINGS.md <family-root>/GATE_PROTOCOL.md <family-root>/FAMILY_INTERFACE.md .kiro/pdlc/
```

### Manual: install the FLO agents (Kiro)

```powershell
Copy-Item "<src>\ai-flo-rule-details\templates\agents\flo-health-check.md","<src>\ai-flo-rule-details\templates\agents\flow-integrity-agent.md" ".kiro\agents\"
```

Then add the `FHC__` / `FIA__` shortcut blocks (see `ai-flo-rule-details/templates/agents/shortcut-rules-block.md`) to your workspace rules. On non-Kiro platforms, agents are invoked via these shortcut blocks rather than an `agents/` folder.

---

## Verify

1. Open your workspace in your IDE.
2. Confirm the core file loads as steering (Kiro: check the Steering panel).
3. Run a health check: type `FHC__` in a chat. A **HEALTHY** (or **IDLE** if no project yet) verdict confirms the fabric trio resolved correctly.
4. Start a chat: "Show AI-FLO status". AI-FLO output appears under `pdlc-ws/`.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `FHC__` returns **NOT READY** / "no routing graph" | Fabric trio missing from `.kiro/{family}/` | Run the family installer, or copy `FAMILY_BINDINGS.md` / `GATE_PROTOCOL.md` / `FAMILY_INTERFACE.md` into the family rule-details root (see Manual: copy the fabric trio). |
| FLO activates but won't route | `FAMILY_BINDINGS.md` present but empty/partial | Confirm the family root copy has internal edges; regenerate if needed. |
| `FHC__` / `FIA__` not recognized | Agent files or shortcut blocks not installed | Install the agents (Kiro) or add the shortcut blocks (other platforms). |

---

## Notes

- The core file is always-loaded; rule-details load on demand.
- AI-FLO coexists with other AI-* packages — each is family-scoped under `pdlc/`. Install order doesn't matter; AI-FLO detects available packages by marker file.
- AI-FLO is the only cross-layer transport: it routes decisions down from AI-PPM and relays telemetry up from Project-layer packages.
- Runtime output is written under `pdlc-ws/`, never at the workspace root.

---

## Agent Installation (Optional)

The Flow Integrity Agent (`FIA__`) provides on-demand validation of routing state. Copy the agent template from the package source into your workspace agents folder:

```powershell
# Windows (PowerShell)
Copy-Item "<src>\ai-flo-rule-details\templates\agents\flow-integrity-agent.md" ".kiro\agents\"
```

```bash
# macOS/Linux
cp <src>/ai-flo-rule-details/templates/agents/flow-integrity-agent.md .kiro/agents/
```

Then add the shortcut block from `templates/agents/shortcut-rules-block.md` to your workspace steering rules. Invoke with `FIA__` in any prompt.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No project markers found" | Install at least one other AI-* package first (AI-PILC, AI-ADLC, etc.) |
| Routing fails silently | Verify the target package's state file exists in an accessible path |
| Core file not loading | Confirm it's in the correct steering location for your platform (see Manual Install) |
| `FIA__` shortcut not recognized | Install the Flow Integrity Agent (see Agent Installation above) |

---

## Test Mode (Optional)

AI-FLO includes a built-in **test mode** for capturing feedback (bugs, improvements, root-cause analyses) during package usage. Test mode is entirely optional and does not affect normal operation.

### Kiro IDE

Test mode is **automatically installed** when the core rules are placed — `test-mode.md` is included with `inclusion: manual` frontmatter, meaning it only activates when you reference it.

**To activate:** Type `#test-mode` in your chat prompt, or say "activate test mode".

**To verify it's available:** Check the Steering Files panel — `test-mode` should appear under manual-inclusion files.

### Amazon Q Developer / Cursor / Cline / Claude Code / Copilot

For non-Kiro platforms, test mode requires manually including the instructions:

```powershell
# Windows — copy test-mode steering alongside the core file
Copy-Item "<src>\ai-flo-rules\test-mode.md" "<your-rules-folder>\"
```

```bash
# macOS/Linux
cp <src>/ai-flo-rules/test-mode.md <your-rules-folder>/
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
