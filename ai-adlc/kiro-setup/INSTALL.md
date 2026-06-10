# AI-ADLC — Installation Guide

## Prerequisites

- An AI-capable IDE (Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, or GitHub Copilot)
- Optionally: a Project Initiation Package (PIP) from AI-PILC, or standalone requirements

---

## Platform-Specific Setup

Choose your platform below. All platforms follow the same pattern:
1. Place `core-workflow.md` where your AI agent reads rules (always-loaded)
2. Place `ai-adlc-rule-details/` where the agent can read files on-demand

---

## Kiro IDE

### Quick Setup

From your target workspace root (where you want to run AI-ADLC):

### PowerShell (Windows)

```powershell
# Copy steering rules (core workflow)
New-Item -ItemType Directory -Force -Path ".kiro\steering"
Copy-Item -Recurse "<path-to-ai-adlc>\ai-adlc-rules" ".kiro\steering\"

# Copy rule details (stage instructions, extensions + templates)
Copy-Item -Recurse "<path-to-ai-adlc>\ai-adlc-rule-details" ".kiro\"
```

### Bash (macOS/Linux)

```bash
# Copy steering rules (core workflow)
mkdir -p .kiro/steering
cp -R <path-to-ai-adlc>/ai-adlc-rules .kiro/steering/

# Copy rule details (stage instructions, extensions + templates)
cp -R <path-to-ai-adlc>/ai-adlc-rule-details .kiro/
```

### Resulting Structure

```
<your-workspace>/
├── .kiro/
│   ├── steering/
│   │   └── ai-adlc-rules/
│   │       └── core-workflow.md          ← Always loaded by Kiro
│   └── ai-adlc-rule-details/
│       ├── common/                       ← Cross-cutting rules (diagrams, validation)
│       ├── foundation/                   ← Stages 1-3 (workspace, ingestion, vision)
│       ├── decomposition/                ← Stages 4-5 (system context, containers)
│       ├── decisions/                    ← Stages 6-8 (tech stack, tenancy, security)
│       ├── design/                       ← Stages 9-12 (data, API, integration, components)
│       ├── assembly/                     ← Stage 13 (package consolidation)
│       ├── extensions/                   ← 6 opt-in advanced patterns (v1.1)
│       └── templates/                    ← Deliverable templates + ADR template
```

### Verification

1. Open your workspace in Kiro IDE
2. Open the **Steering Files** panel
3. Confirm `core-workflow` appears under **Workspace** as always-active
4. Start a new chat and say: "Using AI-ADLC, design the architecture for this system"
5. You should see the AI-ADLC welcome message

---

## Amazon Q Developer

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".amazonq\rules"
Copy-Item -Recurse "<path-to-ai-adlc>\ai-adlc-rules" ".amazonq\rules\"
Copy-Item -Recurse "<path-to-ai-adlc>\ai-adlc-rule-details" ".amazonq\"
```

```bash
# macOS/Linux
mkdir -p .amazonq/rules
cp -R <path-to-ai-adlc>/ai-adlc-rules .amazonq/rules/
cp -R <path-to-ai-adlc>/ai-adlc-rule-details .amazonq/
```

### Resulting Structure

```
<your-workspace>/
├── .amazonq/
│   ├── rules/
│   │   └── ai-adlc-rules/
│   │       └── core-workflow.md
│   └── ai-adlc-rule-details/
```

---

## Cursor IDE

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".cursor\rules"

$frontmatter = @"
---
description: "AI-ADLC (AI-Driven Architecture Design Life Cycle) workflow"
alwaysApply: true
---

"@
$frontmatter | Out-File -FilePath ".cursor\rules\ai-adlc-workflow.mdc" -Encoding utf8
Get-Content "<path-to-ai-adlc>\ai-adlc-rules\core-workflow.md" | Add-Content ".cursor\rules\ai-adlc-workflow.mdc"

New-Item -ItemType Directory -Force -Path ".ai-adlc-rule-details"
Copy-Item -Recurse "<path-to-ai-adlc>\ai-adlc-rule-details\*" ".ai-adlc-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .cursor/rules

cat > .cursor/rules/ai-adlc-workflow.mdc << 'EOF'
---
description: "AI-ADLC (AI-Driven Architecture Design Life Cycle) workflow"
alwaysApply: true
---

EOF
cat <path-to-ai-adlc>/ai-adlc-rules/core-workflow.md >> .cursor/rules/ai-adlc-workflow.mdc

mkdir -p .ai-adlc-rule-details
cp -R <path-to-ai-adlc>/ai-adlc-rule-details/* .ai-adlc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .cursor/
│   └── rules/
│       └── ai-adlc-workflow.mdc          ← Frontmatter + core workflow
└── .ai-adlc-rule-details/
    ├── common/
    ├── foundation/
    └── ...
```

---

## Cline

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".clinerules"
Copy-Item "<path-to-ai-adlc>\ai-adlc-rules\core-workflow.md" ".clinerules\"
New-Item -ItemType Directory -Force -Path ".ai-adlc-rule-details"
Copy-Item -Recurse "<path-to-ai-adlc>\ai-adlc-rule-details\*" ".ai-adlc-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .clinerules
cp <path-to-ai-adlc>/ai-adlc-rules/core-workflow.md .clinerules/
mkdir -p .ai-adlc-rule-details
cp -R <path-to-ai-adlc>/ai-adlc-rule-details/* .ai-adlc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .clinerules/
│   └── core-workflow.md
└── .ai-adlc-rule-details/
```

---

## Claude Code

### Setup

```powershell
# Windows (PowerShell)
Copy-Item "<path-to-ai-adlc>\ai-adlc-rules\core-workflow.md" ".\CLAUDE.md"
New-Item -ItemType Directory -Force -Path ".ai-adlc-rule-details"
Copy-Item -Recurse "<path-to-ai-adlc>\ai-adlc-rule-details\*" ".ai-adlc-rule-details\"
```

```bash
# macOS/Linux
cp <path-to-ai-adlc>/ai-adlc-rules/core-workflow.md ./CLAUDE.md
mkdir -p .ai-adlc-rule-details
cp -R <path-to-ai-adlc>/ai-adlc-rule-details/* .ai-adlc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── CLAUDE.md                             ← Core workflow (always loaded)
└── .ai-adlc-rule-details/
```

---

## GitHub Copilot

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".github"
Copy-Item "<path-to-ai-adlc>\ai-adlc-rules\core-workflow.md" ".github\copilot-instructions.md"
New-Item -ItemType Directory -Force -Path ".ai-adlc-rule-details"
Copy-Item -Recurse "<path-to-ai-adlc>\ai-adlc-rule-details\*" ".ai-adlc-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .github
cp <path-to-ai-adlc>/ai-adlc-rules/core-workflow.md .github/copilot-instructions.md
mkdir -p .ai-adlc-rule-details
cp -R <path-to-ai-adlc>/ai-adlc-rule-details/* .ai-adlc-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .github/
│   └── copilot-instructions.md           ← Core workflow
└── .ai-adlc-rule-details/
```

---

## Universal Setup (Any Platform)

If your platform is not listed above:

1. Place `ai-adlc-rules/core-workflow.md` where your AI IDE reads steering/rules/instructions
2. Place `ai-adlc-rule-details/` where the core workflow can resolve it (same project, adjacent path)
3. Instruct the AI to follow core-workflow.md as the primary workflow

The core workflow includes automatic path resolution logic — it checks:
- `.kiro/ai-adlc-rule-details/`
- `.ai-adlc-rule-details/`
- `ai-adlc-rule-details/`

---

## General Notes (All Platforms)

- The `core-workflow.md` file is always loaded by the AI agent (steering inclusion: always)
- Rule detail files are loaded on-demand by the AI when executing each stage
- This keeps context usage minimal while providing full instructions when needed
- Replace `<path-to-ai-adlc>` with the actual path to the AI-ADLC package folder

---

## Coexistence

AI-ADLC steering files coexist with any other rules you have. The core workflow activates ONLY when you request architecture design. It does not interfere with other workflows or development tasks.

- **AI-PILC** — Run AI-PILC first for project initiation, then AI-ADLC for architecture
- **AI-DWG** — Run AI-ADLC first for architecture, then AI-DWG to generate the development workspace
- **AI-GCE** — AI-GCE reads the workspace AI-DWG produces (downstream of AI-ADLC)
- **AI-DLC** — Run AI-ADLC for architecture, then AI-DLC for software construction

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure `ai-adlc-rule-details/` is in one of the 3 resolved paths (see Universal Setup) |
| Extensions not activating | Extensions are opt-in — they activate only when you request them or architecture justifies them |
| Welcome message not showing | Verify `core-workflow.md` is in the correct steering location for your platform |
| State file not created | State is created on first interaction — start a chat using the activation phrase |
