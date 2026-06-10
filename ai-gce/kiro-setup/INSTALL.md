# AI-GCE — Installation Guide

## Prerequisites

- An AI-capable IDE (Kiro, Amazon Q Developer, Cursor, Cline, Claude Code, or GitHub Copilot)
- An AI-DWG development workspace (`.kiro/steering/` populated) — or at minimum:
  - `.kiro/steering/workspace-rules.md` (marker file — MUST exist)
  - `.kiro/steering/tech-stack.md` (technology drives hook patterns)
  - `.kiro/steering/module-structure.md` (module paths drive hook patterns)
- Git repository initialized

Without these three steering files, AI-GCE can only apply the 10 built-in baseline rules.

---

## Platform-Specific Setup

Choose your platform below. All platforms follow the same pattern:
1. Place `core-generator.md` where your AI agent reads rules (always-loaded)
2. Place `ai-gce-rule-details/` where the agent can read files on-demand

---

## Kiro IDE

### Quick Setup

From your target workspace root (where you want to run AI-GCE):

### PowerShell (Windows)

```powershell
# Copy steering rules (core generator)
New-Item -ItemType Directory -Force -Path ".kiro\steering"
Copy-Item -Recurse "<path-to-ai-gce>\ai-gce-rules" ".kiro\steering\"

# Copy rule details (generators, templates, re-derivation logic)
Copy-Item -Recurse "<path-to-ai-gce>\ai-gce-rule-details" ".kiro\"
```

### Bash (macOS/Linux)

```bash
# Copy steering rules (core generator)
mkdir -p .kiro/steering
cp -R <path-to-ai-gce>/ai-gce-rules .kiro/steering/

# Copy rule details (generators, templates, re-derivation logic)
cp -R <path-to-ai-gce>/ai-gce-rule-details .kiro/
```

### Resulting Structure

```
<your-workspace>/
├── .kiro/
│   ├── steering/
│   │   └── ai-gce-rules/
│   │       └── core-generator.md         ← Always loaded by Kiro
│   └── ai-gce-rule-details/
│       ├── common/                       ← Cross-cutting docs (5 files)
│       ├── generators/                   ← Derivation logic per rule category (23 files)
│       ├── re-derivation/                ← Incremental update logic (3 files)
│       └── templates/                    ← Hook, agent, and log templates
│           ├── hooks/                    ← 15 hook JSON templates + install guide
│           ├── agents/                   ← Audit agent + init agent + README
│           └── compliance-log/           ← Schema + workflows + dashboard
```

### Verification

1. Open your workspace in Kiro IDE
2. Open the **Steering Files** panel
3. Confirm `core-generator` appears under **Workspace** as always-active
4. Start a new chat and say: "Using AI-GCE, generate the compliance engine for this workspace"
5. AI-GCE should read your steering files and begin derivation

---

## Amazon Q Developer

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".amazonq\rules"
Copy-Item -Recurse "<path-to-ai-gce>\ai-gce-rules" ".amazonq\rules\"
Copy-Item -Recurse "<path-to-ai-gce>\ai-gce-rule-details" ".amazonq\"
```

```bash
# macOS/Linux
mkdir -p .amazonq/rules
cp -R <path-to-ai-gce>/ai-gce-rules .amazonq/rules/
cp -R <path-to-ai-gce>/ai-gce-rule-details .amazonq/
```

### Resulting Structure

```
<your-workspace>/
├── .amazonq/
│   ├── rules/
│   │   └── ai-gce-rules/
│   │       └── core-generator.md
│   └── ai-gce-rule-details/
```

---

## Cursor IDE

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".cursor\rules"

$frontmatter = @"
---
description: "AI-GCE (AI-Driven Governance & Compliance Engine) generator"
alwaysApply: true
---

"@
$frontmatter | Out-File -FilePath ".cursor\rules\ai-gce-generator.mdc" -Encoding utf8
Get-Content "<path-to-ai-gce>\ai-gce-rules\core-generator.md" | Add-Content ".cursor\rules\ai-gce-generator.mdc"

New-Item -ItemType Directory -Force -Path ".ai-gce-rule-details"
Copy-Item -Recurse "<path-to-ai-gce>\ai-gce-rule-details\*" ".ai-gce-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .cursor/rules

cat > .cursor/rules/ai-gce-generator.mdc << 'EOF'
---
description: "AI-GCE (AI-Driven Governance & Compliance Engine) generator"
alwaysApply: true
---

EOF
cat <path-to-ai-gce>/ai-gce-rules/core-generator.md >> .cursor/rules/ai-gce-generator.mdc

mkdir -p .ai-gce-rule-details
cp -R <path-to-ai-gce>/ai-gce-rule-details/* .ai-gce-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .cursor/
│   └── rules/
│       └── ai-gce-generator.mdc         ← Frontmatter + core generator
└── .ai-gce-rule-details/
    ├── common/
    ├── generators/
    └── ...
```

---

## Cline

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".clinerules"
Copy-Item "<path-to-ai-gce>\ai-gce-rules\core-generator.md" ".clinerules\"
New-Item -ItemType Directory -Force -Path ".ai-gce-rule-details"
Copy-Item -Recurse "<path-to-ai-gce>\ai-gce-rule-details\*" ".ai-gce-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .clinerules
cp <path-to-ai-gce>/ai-gce-rules/core-generator.md .clinerules/
mkdir -p .ai-gce-rule-details
cp -R <path-to-ai-gce>/ai-gce-rule-details/* .ai-gce-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .clinerules/
│   └── core-generator.md
└── .ai-gce-rule-details/
```

---

## Claude Code

### Setup

```powershell
# Windows (PowerShell)
Copy-Item "<path-to-ai-gce>\ai-gce-rules\core-generator.md" ".\CLAUDE.md"
New-Item -ItemType Directory -Force -Path ".ai-gce-rule-details"
Copy-Item -Recurse "<path-to-ai-gce>\ai-gce-rule-details\*" ".ai-gce-rule-details\"
```

```bash
# macOS/Linux
cp <path-to-ai-gce>/ai-gce-rules/core-generator.md ./CLAUDE.md
mkdir -p .ai-gce-rule-details
cp -R <path-to-ai-gce>/ai-gce-rule-details/* .ai-gce-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── CLAUDE.md                             ← Core generator (always loaded)
└── .ai-gce-rule-details/
```

---

## GitHub Copilot

### Setup

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".github"
Copy-Item "<path-to-ai-gce>\ai-gce-rules\core-generator.md" ".github\copilot-instructions.md"
New-Item -ItemType Directory -Force -Path ".ai-gce-rule-details"
Copy-Item -Recurse "<path-to-ai-gce>\ai-gce-rule-details\*" ".ai-gce-rule-details\"
```

```bash
# macOS/Linux
mkdir -p .github
cp <path-to-ai-gce>/ai-gce-rules/core-generator.md .github/copilot-instructions.md
mkdir -p .ai-gce-rule-details
cp -R <path-to-ai-gce>/ai-gce-rule-details/* .ai-gce-rule-details/
```

### Resulting Structure

```
<your-workspace>/
├── .github/
│   └── copilot-instructions.md           ← Core generator
└── .ai-gce-rule-details/
```

---

## Universal Setup (Any Platform)

If your platform is not listed above:

1. Place `ai-gce-rules/core-generator.md` where your AI IDE reads steering/rules/instructions
2. Place `ai-gce-rule-details/` where the core generator can resolve it (same project, adjacent path)
3. Instruct the AI to follow core-generator.md as the primary workflow

The core generator includes automatic path resolution logic — it checks:
- `.kiro/ai-gce-rule-details/`
- `.ai-gce-rule-details/`
- `ai-gce-rule-details/`

---

## General Notes (All Platforms)

- The `core-generator.md` file is always loaded by the AI agent (steering inclusion: always)
- Rule detail files are loaded on-demand by the AI when executing derivation
- This keeps context usage minimal while providing full instructions when needed
- Replace `<path-to-ai-gce>` with the actual path to the AI-GCE package folder

---

## Coexistence

AI-GCE steering files coexist with any other rules you have. The core generator activates ONLY when you request compliance generation or re-derivation. It does not interfere with other workflows or development tasks.

- **AI-DWG** — Run AI-DWG first to generate the development workspace, then AI-GCE to derive compliance
- **AI-ADLC** — AI-ADLC produces the Architecture Package that AI-DWG consumes (upstream of AI-GCE)
- **AI-DLC** — AI-GCE runs as a continuous compliance companion alongside AI-DLC, enforcing governance throughout the build (not a one-time prior stage)
- **Other steering files** — AI-GCE reads existing steering files but never modifies them

---

## Uninstallation

To remove AI-GCE output from a workspace (does NOT affect steering files from AI-DWG):

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
rm -f docs/compliance-dashboard.md
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AI doesn't find rule-details | Ensure `ai-gce-rule-details/` is in one of the 3 resolved paths (see Universal Setup) |
| "No steering files found" | Ensure `.kiro/steering/workspace-rules.md` exists (minimum requirement) |
| Only baseline rules generated | Steering files are missing or incomplete — add `tech-stack.md` and `module-structure.md` for full derivation |
| Hooks not firing | Check `.kiro/hooks/INSTALL-GUIDE.md` for tier-based activation instructions |
| Re-derivation overwrites customs | Ensure team-added rules are marked with `<!-- custom -->` comments |
