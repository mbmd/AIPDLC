# AI-PILC — Installation Guide

## Prerequisites

- An AI-capable IDE (Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, or GitHub Copilot)
- Optionally: raw requirements or a project brief to feed into the workflow

---

## Platform-Specific Setup

Choose your platform below. All platforms follow the same pattern:
1. Place `core-workflow.md` where your AI agent reads rules (always-loaded)
2. Place `ai-pilc-rule-details/` where the agent can read files on-demand

---

## Kiro IDE

### Quick Setup

From your target workspace root (where you want to run AI-PILC):

### PowerShell (Windows)

```powershell
# Copy steering rules (core workflow)
New-Item -ItemType Directory -Force -Path ".kiro\steering"
Copy-Item -Recurse "<path-to-ai-pilc>\ai-pilc-rules" ".kiro\steering\"

# Copy rule details (phase instructions + templates)
Copy-Item -Recurse "<path-to-ai-pilc>\ai-pilc-rule-details" ".kiro\"
```

### Bash (macOS/Linux)

```bash
# Copy steering rules (core workflow)
mkdir -p .kiro/steering
cp -R <path-to-ai-pilc>/ai-pilc-rules .kiro/steering/

# Copy rule details (phase instructions + templates)
cp -R <path-to-ai-pilc>/ai-pilc-rule-details .kiro/
```

### Resulting Structure

```
<your-workspace>/
├── .kiro/
│   ├── steering/
│   │   └── ai-pilc-rules/
│   │       └── core-workflow.md          ← Always loaded by Kiro
│   └── ai-pilc-rule-details/
│       ├── common/                       ← Loaded at workflow start
│       ├── inception/                    ← Loaded during INCEPTION phase
│       ├── assessment/                   ← Loaded during ASSESSMENT phase
│       ├── justification/                ← Loaded during JUSTIFICATION phase
│       ├── authorization/                ← Loaded during AUTHORIZATION phase
│       ├── planning/                     ← Loaded during PLANNING phase
│       ├── mobilization/                 ← Loaded during MOBILIZATION phase
│       └── templates/                    ← Loaded when producing deliverables
```

### Verification

1. Open your workspace in Kiro IDE
2. Open the **Steering Files** panel
3. Confirm `core-workflow` appears under **Workspace** as always-active
4. Start a new chat and say: "Using AI-PILC, initiate a project"
5. You should see the AI-PILC welcome message

---

## Amazon Q Developer

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".amazonq\rules"
Copy-Item -Recurse "<path-to-ai-pilc>\ai-pilc-rules" ".amazonq\rules\"
Copy-Item -Recurse "<path-to-ai-pilc>\ai-pilc-rule-details" ".amazonq\"
```

```bash
# macOS/Linux
mkdir -p .amazonq/rules
cp -R <path-to-ai-pilc>/ai-pilc-rules .amazonq/rules/
cp -R <path-to-ai-pilc>/ai-pilc-rule-details .amazonq/
```

### Resulting Structure

```
<your-workspace>/
├── .amazonq/
│   ├── rules/
│   │   └── ai-pilc-rules/
│   │       └── core-workflow.md
│   └── ai-pilc-rule-details/
```

---

## Cursor IDE

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".cursor\rules"

$frontmatter = @"
---
description: "AI-PILC (AI-Driven Project Initiation Life Cycle) workflow"
alwaysApply: true
---

"@
$frontmatter | Out-File -FilePath ".cursor\rules\ai-pilc-workflow.mdc" -Encoding utf8
Get-Content "<path-to-ai-pilc>\ai-pilc-rules\core-workflow.md" | Add-Content ".cursor\rules\ai-pilc-workflow.mdc"

New-Item -ItemType Directory -Force -Path ".ai-pilc-rule-details"
Copy-Item -Recurse "<path-to-ai-pilc>\ai-pilc-rule-details\*" ".ai-pilc-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .cursor/rules

cat > .cursor/rules/ai-pilc-workflow.mdc << 'EOF'
---
description: "AI-PILC (AI-Driven Project Initiation Life Cycle) workflow"
alwaysApply: true
---

EOF
cat <path-to-ai-pilc>/ai-pilc-rules/core-workflow.md >> .cursor/rules/ai-pilc-workflow.mdc

mkdir -p .ai-pilc-rule-details
cp -R <path-to-ai-pilc>/ai-pilc-rule-details/* .ai-pilc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .cursor/
│   └── rules/
│       └── ai-pilc-workflow.mdc          ← Frontmatter + core workflow
└── .ai-pilc-rule-details/
    ├── common/
    ├── inception/
    └── ...
```

---

## Cline

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".clinerules"
Copy-Item "<path-to-ai-pilc>\ai-pilc-rules\core-workflow.md" ".clinerules\"
New-Item -ItemType Directory -Force -Path ".ai-pilc-rule-details"
Copy-Item -Recurse "<path-to-ai-pilc>\ai-pilc-rule-details\*" ".ai-pilc-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .clinerules
cp <path-to-ai-pilc>/ai-pilc-rules/core-workflow.md .clinerules/
mkdir -p .ai-pilc-rule-details
cp -R <path-to-ai-pilc>/ai-pilc-rule-details/* .ai-pilc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .clinerules/
│   └── core-workflow.md
└── .ai-pilc-rule-details/
```

---

## Claude Code

### Setup

```powershell
# Windows (PowerShell)
Copy-Item "<path-to-ai-pilc>\ai-pilc-rules\core-workflow.md" ".\CLAUDE.md"
New-Item -ItemType Directory -Force -Path ".ai-pilc-rule-details"
Copy-Item -Recurse "<path-to-ai-pilc>\ai-pilc-rule-details\*" ".ai-pilc-rule-details\"
```

```bash
# macOS/Linux
cp <path-to-ai-pilc>/ai-pilc-rules/core-workflow.md ./CLAUDE.md
mkdir -p .ai-pilc-rule-details
cp -R <path-to-ai-pilc>/ai-pilc-rule-details/* .ai-pilc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── CLAUDE.md                             ← Core workflow (always loaded)
└── .ai-pilc-rule-details/
```

---

## GitHub Copilot

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".github"
Copy-Item "<path-to-ai-pilc>\ai-pilc-rules\core-workflow.md" ".github\copilot-instructions.md"
New-Item -ItemType Directory -Force -Path ".ai-pilc-rule-details"
Copy-Item -Recurse "<path-to-ai-pilc>\ai-pilc-rule-details\*" ".ai-pilc-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .github
cp <path-to-ai-pilc>/ai-pilc-rules/core-workflow.md .github/copilot-instructions.md
mkdir -p .ai-pilc-rule-details
cp -R <path-to-ai-pilc>/ai-pilc-rule-details/* .ai-pilc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .github/
│   └── copilot-instructions.md           ← Core workflow
└── .ai-pilc-rule-details/
```

---

## Universal Setup (Any Platform)

If your platform is not listed above:

1. Place `ai-pilc-rules/core-workflow.md` where your AI IDE reads steering/rules/instructions
2. Place `ai-pilc-rule-details/` where the core workflow can resolve it (same project, adjacent path)
3. Instruct the AI to follow core-workflow.md as the primary workflow

The core workflow includes automatic path resolution logic — it checks:
- `.kiro/ai-pilc-rule-details/`
- `.ai-pilc-rule-details/`
- `ai-pilc-rule-details/`

---

## General Notes (All Platforms)

- The `core-workflow.md` file is always loaded by the AI agent (steering inclusion: always)
- Rule detail files are loaded on-demand by the AI when executing each phase
- This keeps context usage minimal while providing full instructions when needed
- Replace `<path-to-ai-pilc>` with the actual path to the AI-PILC package folder

---

## Coexistence

AI-PILC steering files coexist with any other rules you have. The core workflow activates ONLY when you request project initiation. It does not interfere with other workflows or development tasks.

- **AI-ADLC** — Run AI-PILC first for project initiation, then AI-ADLC for architecture design
- **AI-DWG** — AI-DWG consumes the Architecture Package that AI-ADLC produces (downstream of AI-PILC)
- **AI-GCE** — AI-GCE derives compliance from the workspace AI-DWG generates
- **AI-DLC** — AI-PILC handles project initiation (pre-execution); AI-DLC handles software construction (during execution)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure `ai-pilc-rule-details/` is in the correct location for your platform (see per-platform sections above) |
| Welcome message not showing | Verify `core-workflow.md` is in the correct steering location for your platform |
| State file not created | State is created on first interaction — start a chat using the activation phrase |
| Wrong phase loading | Verify the folder structure under `ai-pilc-rule-details/` matches the expected layout (common/, inception/, etc.) |
