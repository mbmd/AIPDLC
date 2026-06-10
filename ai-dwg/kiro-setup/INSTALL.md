# AI-DWG — Installation Guide

## Prerequisites

- An AI-capable IDE (Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, or GitHub Copilot)
- An Architecture Package (produced by AI-ADLC or equivalent structured markdown docs)

---

## Platform-Specific Setup

Choose your platform below. All platforms follow the same pattern:
1. Place `core-generator.md` where your AI agent reads rules (always-loaded)
2. Place `ai-dwg-rule-details/` where the agent can read files on-demand

---

## Kiro IDE

### Quick Setup

From your target workspace root (where you want to run AI-DWG):

### PowerShell (Windows)

```powershell
# Copy steering rules (core generator)
New-Item -ItemType Directory -Force -Path ".kiro\steering"
Copy-Item -Recurse "<path-to-ai-dwg>\ai-dwg-rules" ".kiro\steering\"

# Copy rule details (mapping rules, reconciliation, templates)
Copy-Item -Recurse "<path-to-ai-dwg>\ai-dwg-rule-details" ".kiro\"
```

### Bash (macOS/Linux)

```bash
# Copy steering rules (core generator)
mkdir -p .kiro/steering
cp -R <path-to-ai-dwg>/ai-dwg-rules .kiro/steering/

# Copy rule details (mapping rules, reconciliation, templates)
cp -R <path-to-ai-dwg>/ai-dwg-rule-details .kiro/
```

### Resulting Structure

```
<your-workspace>/
├── .kiro/
│   ├── steering/
│   │   └── ai-dwg-rules/
│   │       └── core-generator.md         ← Always loaded by Kiro
│   └── ai-dwg-rule-details/
│       ├── common/                       ← Process overview, AP reading, validation
│       ├── mapping/                      ← 23 transformation rule files (AP → DW)
│       ├── reconciliation/               ← Delta update logic
│       └── templates/                    ← 48 output file templates
```

### Verification

1. Open your workspace in Kiro IDE
2. Open the **Steering Files** panel
3. Confirm `core-generator` appears under **Workspace** as always-active
4. Start a new chat and say: "Using AI-DWG, generate the development workspace from my architecture package"
5. AI-DWG should ask for the Architecture Package location

---

## Amazon Q Developer

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".amazonq\rules"
Copy-Item -Recurse "<path-to-ai-dwg>\ai-dwg-rules" ".amazonq\rules\"
Copy-Item -Recurse "<path-to-ai-dwg>\ai-dwg-rule-details" ".amazonq\"
```

```bash
# macOS/Linux
mkdir -p .amazonq/rules
cp -R <path-to-ai-dwg>/ai-dwg-rules .amazonq/rules/
cp -R <path-to-ai-dwg>/ai-dwg-rule-details .amazonq/
```

### Resulting Structure

```
<your-workspace>/
├── .amazonq/
│   ├── rules/
│   │   └── ai-dwg-rules/
│   │       └── core-generator.md
│   └── ai-dwg-rule-details/
```

---

## Cursor IDE

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".cursor\rules"

$frontmatter = @"
---
description: "AI-DWG (AI-Driven Workspace Generator) - transforms architecture into development workspace"
alwaysApply: true
---

"@
$frontmatter | Out-File -FilePath ".cursor\rules\ai-dwg-generator.mdc" -Encoding utf8
Get-Content "<path-to-ai-dwg>\ai-dwg-rules\core-generator.md" | Add-Content ".cursor\rules\ai-dwg-generator.mdc"

New-Item -ItemType Directory -Force -Path ".ai-dwg-rule-details"
Copy-Item -Recurse "<path-to-ai-dwg>\ai-dwg-rule-details\*" ".ai-dwg-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .cursor/rules

cat > .cursor/rules/ai-dwg-generator.mdc << 'EOF'
---
description: "AI-DWG (AI-Driven Workspace Generator) - transforms architecture into development workspace"
alwaysApply: true
---

EOF
cat <path-to-ai-dwg>/ai-dwg-rules/core-generator.md >> .cursor/rules/ai-dwg-generator.mdc

mkdir -p .ai-dwg-rule-details
cp -R <path-to-ai-dwg>/ai-dwg-rule-details/* .ai-dwg-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .cursor/
│   └── rules/
│       └── ai-dwg-generator.mdc         ← Frontmatter + core generator
└── .ai-dwg-rule-details/
    ├── common/
    ├── mapping/
    └── ...
```

---

## Cline

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".clinerules"
Copy-Item "<path-to-ai-dwg>\ai-dwg-rules\core-generator.md" ".clinerules\"
New-Item -ItemType Directory -Force -Path ".ai-dwg-rule-details"
Copy-Item -Recurse "<path-to-ai-dwg>\ai-dwg-rule-details\*" ".ai-dwg-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .clinerules
cp <path-to-ai-dwg>/ai-dwg-rules/core-generator.md .clinerules/
mkdir -p .ai-dwg-rule-details
cp -R <path-to-ai-dwg>/ai-dwg-rule-details/* .ai-dwg-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .clinerules/
│   └── core-generator.md
└── .ai-dwg-rule-details/
```

---

## Claude Code

### Setup

```powershell
# Windows (PowerShell)
Copy-Item "<path-to-ai-dwg>\ai-dwg-rules\core-generator.md" ".\CLAUDE.md"
New-Item -ItemType Directory -Force -Path ".ai-dwg-rule-details"
Copy-Item -Recurse "<path-to-ai-dwg>\ai-dwg-rule-details\*" ".ai-dwg-rule-details\"
```

```bash
# macOS/Linux
cp <path-to-ai-dwg>/ai-dwg-rules/core-generator.md ./CLAUDE.md
mkdir -p .ai-dwg-rule-details
cp -R <path-to-ai-dwg>/ai-dwg-rule-details/* .ai-dwg-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── CLAUDE.md                             ← Core generator (always loaded)
└── .ai-dwg-rule-details/
```

---

## GitHub Copilot

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".github"
Copy-Item "<path-to-ai-dwg>\ai-dwg-rules\core-generator.md" ".github\copilot-instructions.md"
New-Item -ItemType Directory -Force -Path ".ai-dwg-rule-details"
Copy-Item -Recurse "<path-to-ai-dwg>\ai-dwg-rule-details\*" ".ai-dwg-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .github
cp <path-to-ai-dwg>/ai-dwg-rules/core-generator.md .github/copilot-instructions.md
mkdir -p .ai-dwg-rule-details
cp -R <path-to-ai-dwg>/ai-dwg-rule-details/* .ai-dwg-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .github/
│   └── copilot-instructions.md           ← Core generator
└── .ai-dwg-rule-details/
```

---

## Universal Setup (Any Platform)

If your platform is not listed above:

1. Place `ai-dwg-rules/core-generator.md` where your AI IDE reads steering/rules/instructions
2. Place `ai-dwg-rule-details/` where the core generator can resolve it (same project, adjacent path)
3. Instruct the AI to follow core-generator.md as the primary workflow

The core generator includes automatic path resolution logic — it checks:
- `.kiro/ai-dwg-rule-details/`
- `.ai-dwg-rule-details/`
- `ai-dwg-rule-details/`

---

## General Notes (All Platforms)

- The `core-generator.md` file is always loaded by the AI agent (steering inclusion: always)
- Rule detail files are loaded on-demand by the AI when executing generation or reconciliation
- This keeps context usage minimal while providing full instructions when needed
- Replace `<path-to-ai-dwg>` with the actual path to the AI-DWG package folder

---

## Usage

### First Time (Full Generation)

```
Using AI-DWG, generate the development workspace from my architecture package.
The AP is located at: <path-to-architecture-package>
```

AI-DWG will:
1. Read your Architecture Package
2. Ask 2-4 configuration questions
3. Generate all workspace files in one pass

### After Architecture Changes (Reconciliation)

```
Using AI-DWG, reconcile the workspace — the API Architecture was updated.
```

AI-DWG will:
1. Detect what changed
2. Propose workspace updates
3. Apply approved changes (preserving your customizations)

### Brownfield Overlay (Existing Codebase)

```
Using AI-DWG, add governance to this existing workspace.
```

AI-DWG will:
1. Detect existing files and conventions
2. Generate steering files (safe — .kiro/steering/ is new)
3. Merge configs additively (never overwrite)
4. Skip existing operational docs

---

## Coexistence

AI-DWG steering files coexist with any other rules you have. The core generator activates ONLY when you request workspace generation or reconciliation. It does not interfere with other workflows or development tasks.

- **AI-ADLC** — Run AI-ADLC first for architecture, then AI-DWG to generate the workspace
- **AI-GCE** — Run AI-DWG first for workspace generation, then AI-GCE for compliance derivation
- **AI-DLC** — AI-DWG produces the workspace that AI-DLC operates within
- **Other steering files** — AI-DWG generates new steering files but never modifies manually-created ones

---

## Compatibility

- **AI-ADLC v1.0:** Full support (core workflow output)
- **AI-ADLC v1.1:** Full support (6 extensions detected automatically)
- **Standalone AP:** Supported (without `adlc-state.md` — manual artifact mapping required)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure `ai-dwg-rule-details/` is in one of the 3 resolved paths (see Universal Setup) |
| Extensions not detected | Verify `adlc-state.md` exists in AP folder with `Enabled Extensions` section |
| Conditional files not generated | Check that AP contains the trigger artifact (see core-generator conditional logic table) |
| Reconciliation overwrites customizations | Ensure team-added content is NOT placed between `<!-- begin: AP-sourced -->` markers |
