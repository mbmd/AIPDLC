# AI-ILC — Installation Guide

## Prerequisites

- An AI-capable IDE (Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, or GitHub Copilot)
- A workspace where you want to manage ideas
- Git repository initialized (recommended for state tracking)

Without installation, AI-ILC cannot activate its pipeline — you'll get generic AI responses instead of the governed idea lifecycle.

---

## Platform-Specific Setup

Choose your platform below. All platforms follow the same pattern:
1. Place `core-workflow.md` where your AI agent reads rules (always-loaded)
2. Place `ai-ilc-rule-details/` where the agent can read files on-demand

---

## Kiro IDE

### Quick Setup

From your target workspace root (where you want to run AI-ILC):

### PowerShell (Windows)

```powershell
# Copy steering rules (core workflow)
New-Item -ItemType Directory -Force -Path ".kiro\steering\ai-ilc-rules"
Copy-Item "<path-to-ai-ilc>\ai-ilc-rules\core-workflow.md" ".kiro\steering\ai-ilc-rules\"

# Copy rule details (stage instructions + templates)
Copy-Item -Recurse "<path-to-ai-ilc>\ai-ilc-rule-details" ".kiro\"
```

### Bash (macOS/Linux)

```bash
# Copy steering rules (core workflow)
mkdir -p .kiro/steering/ai-ilc-rules
cp <path-to-ai-ilc>/ai-ilc-rules/core-workflow.md .kiro/steering/ai-ilc-rules/

# Copy rule details (stage instructions + templates)
cp -R <path-to-ai-ilc>/ai-ilc-rule-details .kiro/
```

### Resulting Structure

```
<your-workspace>/
├── .kiro/
│   ├── steering/
│   │   └── ai-ilc-rules/
│   │       └── core-workflow.md          ← Always loaded by Kiro
│   └── ai-ilc-rule-details/
│       ├── common/                       ← Cross-cutting rules (5 files)
│       ├── idea-lifecycle/               ← Stage execution (6 files)
│       ├── connectors/                   ← Portfolio connector spec
│       └── templates/                    ← Output templates (7+ files)
```

### Verification

1. Open your workspace in Kiro IDE
2. Open the **Steering Files** panel
3. Confirm `core-workflow` appears under **Workspace** as always-active
4. Start a new chat and say: "I have an idea"
5. You should see the AI-ILC welcome message with pipeline overview

---

## Amazon Q Developer

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".amazonq\rules\ai-ilc-rules"
Copy-Item "<path-to-ai-ilc>\ai-ilc-rules\core-workflow.md" ".amazonq\rules\ai-ilc-rules\"
Copy-Item -Recurse "<path-to-ai-ilc>\ai-ilc-rule-details" ".amazonq\"
```

```bash
# macOS/Linux
mkdir -p .amazonq/rules/ai-ilc-rules
cp <path-to-ai-ilc>/ai-ilc-rules/core-workflow.md .amazonq/rules/ai-ilc-rules/
cp -R <path-to-ai-ilc>/ai-ilc-rule-details .amazonq/
```

### Resulting Structure

```
<your-workspace>/
├── .amazonq/
│   ├── rules/
│   │   └── ai-ilc-rules/
│   │       └── core-workflow.md
│   └── ai-ilc-rule-details/
```

---

## Cursor IDE

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".cursor\rules"

$frontmatter = @"
---
description: "AI-ILC (AI-Driven Idea Life Cycle) workflow"
alwaysApply: true
---

"@
$frontmatter | Out-File -FilePath ".cursor\rules\ai-ilc-workflow.mdc" -Encoding utf8
Get-Content "<path-to-ai-ilc>\ai-ilc-rules\core-workflow.md" | Add-Content ".cursor\rules\ai-ilc-workflow.mdc"

New-Item -ItemType Directory -Force -Path ".ai-ilc-rule-details"
Copy-Item -Recurse "<path-to-ai-ilc>\ai-ilc-rule-details\*" ".ai-ilc-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .cursor/rules

cat > .cursor/rules/ai-ilc-workflow.mdc << 'EOF'
---
description: "AI-ILC (AI-Driven Idea Life Cycle) workflow"
alwaysApply: true
---

EOF
cat <path-to-ai-ilc>/ai-ilc-rules/core-workflow.md >> .cursor/rules/ai-ilc-workflow.mdc

mkdir -p .ai-ilc-rule-details
cp -R <path-to-ai-ilc>/ai-ilc-rule-details/* .ai-ilc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .cursor/
│   └── rules/
│       └── ai-ilc-workflow.mdc            ← Frontmatter + core workflow
└── .ai-ilc-rule-details/
```

---

## Cline

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".clinerules"
Copy-Item "<path-to-ai-ilc>\ai-ilc-rules\core-workflow.md" ".clinerules\"
New-Item -ItemType Directory -Force -Path ".ai-ilc-rule-details"
Copy-Item -Recurse "<path-to-ai-ilc>\ai-ilc-rule-details\*" ".ai-ilc-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .clinerules
cp <path-to-ai-ilc>/ai-ilc-rules/core-workflow.md .clinerules/
mkdir -p .ai-ilc-rule-details
cp -R <path-to-ai-ilc>/ai-ilc-rule-details/* .ai-ilc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .clinerules/
│   └── core-workflow.md
└── .ai-ilc-rule-details/
```

---

## Claude Code

### Setup

```powershell
# Windows (PowerShell)
Copy-Item "<path-to-ai-ilc>\ai-ilc-rules\core-workflow.md" ".\CLAUDE.md"
New-Item -ItemType Directory -Force -Path ".ai-ilc-rule-details"
Copy-Item -Recurse "<path-to-ai-ilc>\ai-ilc-rule-details\*" ".ai-ilc-rule-details\"
```

```bash
# macOS/Linux
cp <path-to-ai-ilc>/ai-ilc-rules/core-workflow.md ./CLAUDE.md
mkdir -p .ai-ilc-rule-details
cp -R <path-to-ai-ilc>/ai-ilc-rule-details/* .ai-ilc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── CLAUDE.md                             ← Core workflow (always loaded)
└── .ai-ilc-rule-details/
```

---

## GitHub Copilot

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".github"
Copy-Item "<path-to-ai-ilc>\ai-ilc-rules\core-workflow.md" ".github\copilot-instructions.md"
New-Item -ItemType Directory -Force -Path ".ai-ilc-rule-details"
Copy-Item -Recurse "<path-to-ai-ilc>\ai-ilc-rule-details\*" ".ai-ilc-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .github
cp <path-to-ai-ilc>/ai-ilc-rules/core-workflow.md .github/copilot-instructions.md
mkdir -p .ai-ilc-rule-details
cp -R <path-to-ai-ilc>/ai-ilc-rule-details/* .ai-ilc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .github/
│   └── copilot-instructions.md           ← Core workflow
└── .ai-ilc-rule-details/
```

---

## Universal (Any Platform)

If your platform is not listed above:

1. Place `ai-ilc-rules/core-workflow.md` where your AI IDE reads steering/rules/instructions
2. Place `ai-ilc-rule-details/` where the core workflow can resolve it (same project, adjacent path)
3. Instruct the AI to follow core-workflow.md as the primary workflow

The core workflow includes automatic path resolution logic — it checks:
- `.kiro/ai-ilc-rule-details/`
- `.ai-ilc-rule-details/`
- `ai-ilc-rule-details/`

---

## Important Notes

- The core workflow is the ONLY file that must be auto-loaded by your IDE
- Rule detail files are loaded on-demand by the AI when executing each stage
- This keeps context usage minimal while providing full instructions when needed
- Replace `<path-to-ai-ilc>` with the actual path to the AI-ILC package folder

---

## What Gets Installed

| Item | Purpose | File Count |
|------|---------|:----------:|
| `core-workflow.md` | Master orchestration (always loaded) | 1 |
| `common/` | Cross-cutting rules (welcome, session continuity, validation, questions, process overview) | 5 |
| `idea-lifecycle/` | Stage execution details (capture, shape, evaluate, scope, approve, route-handoff) | 6 |
| `connectors/` | Portfolio connector spec | 1 |
| `templates/` | Output templates (briefs, register, decision record, state, management-framework) | 8 |

**Total:** ~21 files

---

## Configuration (Optional)

### Custom Evaluation Rubric

If your organization wants custom scoring criteria, create:

```
{your-project}/.kiro/steering/ilc-evaluation-config.md
```

Define custom criteria there. AI-ILC's two-source model will use your criteria where provided and fall back to the built-in baseline where you're silent.

### Persona Steering (Optional)

If you want AI-ILC's personas to use your organization's voice/style, ensure the relevant persona files are in your `.kiro/steering/` folder. AI-ILC references:
- `#persona-product-manager` (lead at most stages)
- `#persona-process-designer` (lead at Scope)
- Sub-roles: business-analyst, financial-analyst, resource-planner, risk-analyst, change-manager

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

## Coexistence

AI-ILC steering files coexist with any other rules you have. The core workflow activates ONLY when you submit an idea. It does not interfere with other workflows or development tasks.

- **AI-PILC** — AI-ILC approves ideas; AI-PILC initiates the resulting project (AI-ILC's Mode E brief feeds AI-PILC)
- **AI-ADLC** — Architecture work flows through AI-PILC first; AI-ILC never routes directly to AI-ADLC
- **AI-POLC** — Feature-route ideas target AI-POLC's product backlog (when available); fallback: AI-DLC
- **AI-DWG** — Downstream of AI-ADLC; no direct interaction with AI-ILC
- **AI-GCE** — AI-GCE runs as a continuous companion alongside AI-DLC; no direct AI-ILC interaction

---

## Uninstallation

```powershell
# Windows (PowerShell)
Remove-Item -Recurse -Force ".kiro\steering\ai-ilc-rules"
Remove-Item -Recurse -Force ".kiro\ai-ilc-rule-details"
# Or wherever you placed the rule-details folder
```

```bash
# macOS/Linux
rm -rf .kiro/steering/ai-ilc-rules/
rm -rf .kiro/ai-ilc-rule-details/
# Or wherever you placed the rule-details folder
```

Your idea outputs (briefs, registers, state files) remain in your project — they're your artifacts, not the package's.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure `ai-ilc-rule-details/` is in one of the 3 resolved paths (see Universal section) |
| Welcome message not showing | Verify `core-workflow.md` is in the correct steering location for your platform |
| "No idea register found" | Normal on first run — AI-ILC creates the register during the first idea capture |
| Evaluation scores not applying | Ensure the built-in baseline is being loaded from `common/` — check path resolution |
| Route targets a non-existent package | Normal — forward-compatible routing (Lesson 47). The fallback target handles it. |

---

*Version 1.1.0 | AI-ILC — AI-Driven Idea Life Cycle | Multi-platform installation*
