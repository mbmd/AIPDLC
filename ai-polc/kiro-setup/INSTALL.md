# AI-POLC — Installation Guide

**Package:** AI-POLC (AI-Driven Product Ownership Life Cycle)
**Version:** 1.0.0

---

## Prerequisites

- A workspace with Kiro IDE (or compatible AI assistant)
- The AI-POLC package source files (this repository)

---

## Platform Setup

### Kiro IDE (Recommended)

**PowerShell (Windows):**
```powershell
# Copy AI-POLC rules to your workspace steering
Copy-Item -Recurse "<path-to-ai-polc>/ai-polc-rules" "<your-workspace>/.kiro/steering/ai-polc-rules"
Copy-Item -Recurse "<path-to-ai-polc>/ai-polc-rule-details" "<your-workspace>/.kiro/ai-polc-rule-details"
```

**Bash (macOS/Linux):**
```bash
# Copy AI-POLC rules to your workspace steering
cp -r <path-to-ai-polc>/ai-polc-rules <your-workspace>/.kiro/steering/ai-polc-rules
cp -r <path-to-ai-polc>/ai-polc-rule-details <your-workspace>/.kiro/ai-polc-rule-details
```

### Cursor / Windsurf / Other AI IDEs

**PowerShell (Windows):**
```powershell
# Copy to a location your AI can access
Copy-Item -Recurse "<path-to-ai-polc>/ai-polc-rules" "<your-workspace>/.ai-polc/ai-polc-rules"
Copy-Item -Recurse "<path-to-ai-polc>/ai-polc-rule-details" "<your-workspace>/.ai-polc/ai-polc-rule-details"
```

**Bash (macOS/Linux):**
```bash
cp -r <path-to-ai-polc>/ai-polc-rules <your-workspace>/.ai-polc/ai-polc-rules
cp -r <path-to-ai-polc>/ai-polc-rule-details <your-workspace>/.ai-polc/ai-polc-rule-details
```

### Standalone (Manual Reference)

**PowerShell (Windows):**
```powershell
# Place at workspace root
Copy-Item -Recurse "<path-to-ai-polc>/ai-polc-rules" "<your-workspace>/ai-polc-rules"
Copy-Item -Recurse "<path-to-ai-polc>/ai-polc-rule-details" "<your-workspace>/ai-polc-rule-details"
```

**Bash (macOS/Linux):**
```bash
cp -r <path-to-ai-polc>/ai-polc-rules <your-workspace>/ai-polc-rules
cp -r <path-to-ai-polc>/ai-polc-rule-details <your-workspace>/ai-polc-rule-details
```

---

## Resulting Structure

After installation, your workspace should have:

```
<your-workspace>/
├── .kiro/steering/ai-polc-rules/       (Kiro)
│   └── core-workflow.md
├── .kiro/ai-polc-rule-details/         (Kiro)
│   ├── common/
│   ├── foundation/
│   ├── strategy/
│   ├── governance/
│   ├── stakeholders/
│   ├── assembly/
│   ├── operations/
│   ├── tier2/
│   ├── extensions/
│   └── templates/
```

---

## Verification

After installation, start a new AI session and say:

```
Start the AI-POLC workflow for product ownership.
```

The AI should:
1. Load `core-workflow.md`
2. Display the welcome message
3. Begin Stage 1 (Workspace Detection)

If the AI doesn't recognize the workflow, verify that `core-workflow.md` is in a location the AI reads (steering folder for Kiro, or explicitly reference it).

---

## Coexistence

AI-POLC coexists with other AI-* packages:
- **AI-PILC:** POLC reads PIP output; no file conflicts
- **AI-ADLC:** POLC reads AP output; no file conflicts
- **AI-DWG:** POLC produces PBP that DWG reads; sequential operation
- **AI-GCE:** POLC's DoR/DoD rules flow to GCE via DWG steering; no direct dependency

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't recognize workflow | Verify `core-workflow.md` is in a steering/rules path the AI reads |
| "File not found" errors | Check that `ai-polc-rule-details/` is at the expected path (see Rule Details Loading in core-workflow) |
| Template errors | Ensure `templates/` folder was copied completely |
| Chain mode not detecting upstream | Verify predecessor marker files exist (`pilc-state.md`, `adlc-state.md`) |

---

*AI-POLC v1.0.0 | Installation Guide*
