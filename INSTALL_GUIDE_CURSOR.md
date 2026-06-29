# AI-* Family — Complete Installation Guide for Cursor

**Applies to:** Cursor IDE — full workflow support with `.cursor/rules/` integration.

> **Why Cursor?** Cursor supports workspace-level rules via `.cursor/rules/` with `.mdc` frontmatter for always-apply behavior. All workflow packages, generators, and governance rule generation work at 100%. Only AI-GCE hook auto-execution is unavailable (Kiro-only).

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [How It Works](#how-it-works)
- [Method 1: Automated Installer (Recommended)](#method-1-automated-installer-recommended)
- [Method 2: Manual Installation](#method-2-manual-installation)
- [Multi-Package Installation](#multi-package-installation)
- [Package Reference](#package-reference)
- [Resulting Workspace Structure](#resulting-workspace-structure)
- [Verification](#verification)
- [Using the Packages](#using-the-packages)
- [Chain Handoffs Between Packages](#chain-handoffs-between-packages)
- [AI-GCE Governance on Cursor](#ai-gce-governance-on-cursor)
- [Session Continuity](#session-continuity)
- [Coexistence with Other Rules](#coexistence-with-other-rules)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Cursor IDE** | Installed ([cursor.com](https://cursor.com)) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

Each AI-* package installs **two things** into your workspace, both **family-scoped** to the AI-* PDLC Family (core files carry a `pdlc-` filename prefix; rule-details live under a `.pdlc/` folder — so multiple AIFLC families can coexist in one workspace):

1. **Core workflow/engine file** — a `.mdc` rule file with `alwaysApply: true` frontmatter in `.cursor/rules/` (loaded automatically every session)
2. **Rule-details folder** — phase-specific instructions and templates that the core workflow loads on demand during execution (placed under `.pdlc/`)

```
your-workspace/
├── .cursor/
│   └── rules/
│       └── pdlc-ai-pilc-workflow.mdc  ← Always loaded (frontmatter: alwaysApply: true)
├── .pdlc/
│   └── ai-pilc-rule-details/          ← Loaded on-demand by the core workflow
│       ├── common/
│       ├── inception/
│       ├── assessment/
│       ├── templates/
│       └── ...
├── pdlc-ws/                           ← All runtime outputs land here (never workspace root)
└── (your project files)
```

Cursor reads all `.mdc` files in `.cursor/rules/` and loads those with `alwaysApply: true` at every session start.

> **The Kiro-style split:** core files load as always-on rules (`.cursor/rules/pdlc-*.mdc`); rule-details are read on demand (`.pdlc/`); and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root.

---

## Method 1: Automated Installer (Recommended)

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive
.\installer\install.ps1

# Option B: One-liner for Cursor with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cursor -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cursor -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Cursor
./installer/install.sh --target <your-project-path> --platform cursor --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform cursor --bundle full
```

### Preset Bundles

| Bundle | Command Flag | Packages | Best For |
|--------|-------------|----------|----------|
| **Greenfield Full** | `-Bundle full` | AI-ILC + AI-PILC + AI-PPM + AI-FLO + AI-POLC + AI-UXD + AI-ADLC + AI-DWG + AI-GCE + AI-TGE + AI-DFE | New project, complete family |
| **Greenfield Minimal** | `-Bundle minimal` | AI-PILC + AI-ADLC + AI-DWG | Quick start, architecture focus |
| **Architecture Focus** | `-Bundle arch` | AI-ADLC + AI-DWG + AI-GCE | Architecture → workspace → governance |
| **Governance Only** | `-Bundle governance` | AI-GCE + AI-TGE | Existing project, add compliance |
| **Portfolio** | `-Bundle portfolio` | AI-ILC + AI-PILC + AI-PPM + AI-FLO | Multi-project management |

---

## Method 2: Manual Installation

### Single Package Example (AI-PILC)

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Create the rules directory
New-Item -ItemType Directory -Force -Path "$Target\.cursor\rules"

# Create .mdc file with frontmatter + core workflow content
$frontmatter = @"
---
description: "AI-PILC (AI-Driven Project Initiation Life Cycle) workflow"
alwaysApply: true
---

"@
$frontmatter | Out-File -FilePath "$Target\.cursor\rules\pdlc-ai-pilc-workflow.mdc" -Encoding utf8
Get-Content "$Source\ai-pilc\ai-pilc-rules\core-workflow.md" | Add-Content "$Target\.cursor\rules\pdlc-ai-pilc-workflow.mdc"

# Copy rule-details folder (family-scoped under .pdlc/)
New-Item -ItemType Directory -Force -Path "$Target\.pdlc\ai-pilc-rule-details"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details\*" "$Target\.pdlc\ai-pilc-rule-details\"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Create the rules directory
mkdir -p "$TARGET/.cursor/rules"

# Create .mdc file with frontmatter + core workflow content
cat > "$TARGET/.cursor/rules/pdlc-ai-pilc-workflow.mdc" << 'EOF'
---
description: "AI-PILC (AI-Driven Project Initiation Life Cycle) workflow"
alwaysApply: true
---

EOF
cat "$SOURCE/ai-pilc/ai-pilc-rules/core-workflow.md" >> "$TARGET/.cursor/rules/pdlc-ai-pilc-workflow.mdc"

# Copy rule-details folder (family-scoped under .pdlc/)
mkdir -p "$TARGET/.pdlc/ai-pilc-rule-details"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details/"* "$TARGET/.pdlc/ai-pilc-rule-details/"
```

### File Naming Convention (Cursor)

| Package | Rule File (.mdc) | Details Folder |
|---------|-----------------|----------------|
| AI-ILC | `.cursor/rules/pdlc-ai-ilc-workflow.mdc` | `.pdlc/ai-ilc-rule-details/` |
| AI-PILC | `.cursor/rules/pdlc-ai-pilc-workflow.mdc` | `.pdlc/ai-pilc-rule-details/` |
| AI-ADLC | `.cursor/rules/pdlc-ai-adlc-workflow.mdc` | `.pdlc/ai-adlc-rule-details/` |
| AI-UXD | `.cursor/rules/pdlc-ai-uxd-workflow.mdc` | `.pdlc/ai-uxd-rule-details/` |
| AI-POLC | `.cursor/rules/pdlc-ai-polc-workflow.mdc` | `.pdlc/ai-polc-rule-details/` |
| AI-DWG | `.cursor/rules/pdlc-ai-dwg-workflow.mdc` | `.pdlc/ai-dwg-rule-details/` |
| AI-GCE | `.cursor/rules/pdlc-ai-gce-workflow.mdc` | `.pdlc/ai-gce-rule-details/` |
| AI-TGE | `.cursor/rules/pdlc-ai-tge-workflow.mdc` | `.pdlc/ai-tge-rule-details/` |
| AI-PPM | `.cursor/rules/pdlc-ai-ppm-workflow.mdc` | `.pdlc/ai-ppm-rule-details/` |
| AI-FLO | `.cursor/rules/pdlc-ai-flo-workflow.mdc` | `.pdlc/ai-flo-rule-details/` |

> **Important:** The `.mdc` extension and `alwaysApply: true` frontmatter are required for Cursor to load the rules automatically. The installer handles this for you.

---

## Multi-Package Installation

### Installing All 10 Packages

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cursor -Bundle full
```

Or manually (PowerShell example for multiple packages):

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.cursor\rules" | Out-Null

$packages = @(
    @{ Name = "ai-ilc";  Core = "core-workflow.md";  Rules = "ai-ilc-rules";  Details = "ai-ilc-rule-details";  Desc = "AI-ILC (Idea Life Cycle) workflow" }
    @{ Name = "ai-pilc"; Core = "core-workflow.md";  Rules = "ai-pilc-rules"; Details = "ai-pilc-rule-details"; Desc = "AI-PILC (Project Initiation Life Cycle) workflow" }
    @{ Name = "ai-ppm";  Core = "core-engine.md";    Rules = "ai-ppm-rules";  Details = "ai-ppm-rule-details";  Desc = "AI-PPM (Portfolio Management) engine" }
    @{ Name = "ai-flo";  Core = "core-engine.md";    Rules = "ai-flo-rules";  Details = "ai-flo-rule-details";  Desc = "AI-FLO (Flow Router) engine" }
    @{ Name = "ai-adlc"; Core = "core-workflow.md";  Rules = "ai-adlc-rules"; Details = "ai-adlc-rule-details"; Desc = "AI-ADLC (Architecture Design Life Cycle) workflow" }
    @{ Name = "ai-uxd";  Core = "core-workflow.md";  Rules = "ai-uxd-rules";  Details = "ai-uxd-rule-details";  Desc = "AI-UXD (UX Design Life Cycle) workflow" }
    @{ Name = "ai-polc"; Core = "core-workflow.md";  Rules = "ai-polc-rules"; Details = "ai-polc-rule-details"; Desc = "AI-POLC (Product Ownership Life Cycle) workflow" }
    @{ Name = "ai-dwg";  Core = "core-generator.md"; Rules = "ai-dwg-rules";  Details = "ai-dwg-rule-details";  Desc = "AI-DWG (Workspace Generator)" }
    @{ Name = "ai-gce";  Core = "core-generator.md"; Rules = "ai-gce-rules";  Details = "ai-gce-rule-details";  Desc = "AI-GCE (Governance & Compliance Engine)" }
    @{ Name = "ai-tge";  Core = "core-engine.md";    Rules = "ai-tge-rules";  Details = "ai-tge-rule-details";  Desc = "AI-TGE (Test Governance Engine)" }
)

foreach ($pkg in $packages) {
    $coreSource = Join-Path $Source "$($pkg.Name)\$($pkg.Rules)\$($pkg.Core)"
    $mdcDest = Join-Path $Target ".cursor\rules\pdlc-$($pkg.Name)-workflow.mdc"
    $detailsSource = Join-Path $Source "$($pkg.Name)\$($pkg.Details)"
    $detailsDest = Join-Path $Target ".pdlc\$($pkg.Details)"

    if (Test-Path $coreSource) {
        $frontmatter = "---`ndescription: `"$($pkg.Desc)`"`nalwaysApply: true`n---`n`n"
        $frontmatter | Out-File -FilePath $mdcDest -Encoding utf8 -NoNewline
        Get-Content $coreSource -Raw | Add-Content $mdcDest -NoNewline

        if (Test-Path $detailsSource) {
            if (Test-Path $detailsDest) { Remove-Item -Recurse -Force $detailsDest }
            Copy-Item -Recurse $detailsSource $detailsDest
        }
        Write-Host "Installed $($pkg.Name)" -ForegroundColor Green
    } else {
        Write-Host "Skipped $($pkg.Name) - source not found" -ForegroundColor Yellow
    }
}
```

---

## Package Reference

| # | Package | What It Does | Activation Phrase |
|---|---------|-------------|-------------------|
| 1 | **AI-ILC** | Evaluates raw ideas → Approved Idea Brief | "Using AI-ILC, evaluate this idea" |
| 2 | **AI-PILC** | Raw requirement → Project Initiation Package | "Using AI-PILC, initiate a project" |
| 3 | **AI-PPM** | Portfolio governance across multiple projects | "Using AI-PPM, manage my portfolio" |
| 4 | **AI-FLO** | Routes handoffs between packages | "Using AI-FLO, route this output" |
| 5 | **AI-ADLC** | Requirements → Architecture Package | "Using AI-ADLC, design the architecture" |
| 6 | **AI-UXD** | PIP/AP → UX Design Package (personas, flows) | "Using AI-UXD, design the user experience" |
| 7 | **AI-POLC** | PIP/AP → Product Backlog Package | "Using AI-POLC, build the product backlog" |
| 8 | **AI-DWG** | Architecture → Ready-to-code workspace | "Using AI-DWG, generate the workspace" |
| 9 | **AI-GCE** | Workspace → Compliance enforcement layer | "Using AI-GCE, set up governance" |
| 10 | **AI-TGE** | Workspace → Test strategy & coverage tracking | "Using AI-TGE, establish test governance" |

### Common Starting Points

| Scenario | Start With | Then |
|----------|-----------|------|
| New project from scratch | AI-PILC | → AI-POLC → AI-UXD → AI-ADLC → AI-DWG |
| Have requirements, need architecture | AI-ADLC | → AI-DWG |
| Have architecture, need workspace | AI-DWG | → AI-GCE + AI-TGE |
| Idea evaluation (pre-project) | AI-ILC | → AI-PILC if approved |
| Existing project, add compliance | AI-GCE | + AI-TGE |

---

## Resulting Workspace Structure

After a full install:

```
your-project/
├── .cursor/
│   └── rules/
│       ├── pdlc-ai-ilc-workflow.mdc     ← Always loaded
│       ├── pdlc-ai-pilc-workflow.mdc    ← Always loaded
│       ├── pdlc-ai-ppm-workflow.mdc     ← Always loaded
│       ├── pdlc-ai-flo-workflow.mdc     ← Always loaded
│       ├── pdlc-ai-adlc-workflow.mdc    ← Always loaded
│       ├── pdlc-ai-uxd-workflow.mdc     ← Always loaded
│       ├── pdlc-ai-polc-workflow.mdc    ← Always loaded
│       ├── pdlc-ai-dwg-workflow.mdc     ← Always loaded
│       ├── pdlc-ai-gce-workflow.mdc     ← Always loaded
│       └── pdlc-ai-tge-workflow.mdc     ← Always loaded
├── .pdlc/                               ← AI-* PDLC Family rule-details (on-demand)
│   ├── ai-ilc-rule-details/
│   ├── ai-pilc-rule-details/
│   ├── ai-adlc-rule-details/
│   ├── ai-uxd-rule-details/
│   ├── ai-polc-rule-details/
│   ├── ai-ppm-rule-details/
│   ├── ai-flo-rule-details/
│   ├── ai-dwg-rule-details/
│   ├── ai-gce-rule-details/
│   └── ai-tge-rule-details/
├── pdlc-ws/                             ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   └── .ai-family-manifest.json         ← Installer tracking
└── (your project files)
```

---

## Verification

1. Open your workspace in Cursor
2. Open Settings → Features → Rules
3. Confirm the AI-* `.mdc` files appear in the rules list with "Always" status
4. Start a new chat and say: "Using AI-PILC, initiate a project"
5. You should see the AI-PILC welcome message

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell the AI which package to use with the activation phrase
2. **Choose depth:** The package asks if you want Minimal, Standard, or Comprehensive output
3. **Work through stages:** Each package has defined stages with sequential guidance
4. **Approve at gates:** The AI presents output and waits for approval before proceeding
5. **Get deliverables:** Each stage produces one professional deliverable (written to disk)

### Depth Levels

| Level | Output Volume | Best For |
|-------|--------------|----------|
| **Minimal** | Key essentials only | Prototypes, small projects, time-pressed |
| **Standard** | Professional baseline | Most projects (recommended default) |
| **Comprehensive** | Enterprise-grade detail | Regulated industries, large teams, audit-heavy |

---

## Chain Handoffs Between Packages

Packages detect each other's output through **state marker files**. When a package completes, it writes a marker (e.g., `pilc-state.md`). The next package detects the marker and enriches its work with that context.

**No manual wiring needed.** Just run packages sequentially.

---

## AI-GCE Governance on Cursor

AI-GCE generates all governance files correctly on Cursor, but enforcement is advisory rather than automatic:

### What Works

- Rule generation (`.governance/rules/`) — full mode 1/2/3/4
- Compliance documentation
- Brownfield baseline scanning
- Hook and agent file generation (structurally valid but inert)

### What Doesn't Work

| Feature | Why | Workaround |
|---------|-----|------------|
| Hook auto-execution | No event bus in Cursor | Add governance rules as `.mdc` files with `alwaysApply: true` |
| Agent shortcut triggers | No agent runtime | Paste agent prompts manually when needed |
| Automatic compliance logging | Triggered by hooks | Ask the AI to log manually |

### Best Practice

After AI-GCE generates governance, create an additional rule file:

```
.cursor/rules/governance-enforce.mdc
```

```markdown
---
description: "Governance rules enforcement (derived from AI-GCE)"
alwaysApply: true
---

## Governance Rules (Always Enforce)

Check compliance on every file you create or modify against:
- .governance/rules/security-rules.md (CRITICAL)
- .governance/rules/architecture-rules.md
- .governance/rules/naming-conventions.md

See .governance/COMPLIANCE_README.md for full rule index.
```

---

## Session Continuity

State files persist between sessions. Say "Continue AI-PILC" to resume where you left off.

---

## Coexistence with Other Rules

- **Existing `.cursor/rules/`**: Untouched. AI-* packages add their own `.mdc` files alongside yours.
- **Existing `.cursorrules`**: Untouched (legacy format, still respected by Cursor).
- **Other project files**: Never modified.

---

## Uninstalling

```powershell
# Via installer
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall

# Manual
Remove-Item "<your-project-path>\.cursor\rules\pdlc-ai-*-workflow.mdc"
Get-ChildItem "<your-project-path>\.pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Rules not loading | Missing frontmatter | Ensure `.mdc` files have `alwaysApply: true` in YAML frontmatter |
| "Can't find rule-details" | Path mismatch | Ensure `.pdlc/ai-{pkg}-rule-details/` exists at workspace root |
| No welcome message | Wrong activation phrase | Use "Using AI-PILC, ..." format |
| State file not created | First interaction only | State is created after first stage completes |

---

## Platform Capabilities Summary

| Feature | Cursor |
|---------|:------:|
| Core workflow execution | ✅ |
| On-demand file loading | ✅ |
| Deliverable file output | ✅ |
| State persistence | ✅ |
| Chain marker detection | ✅ |
| Multi-package install | ✅ All 10 |
| AI-DWG workspace gen | ✅ |
| AI-GCE rule generation | ✅ |
| AI-GCE hook enforcement | ❌ (Kiro only) |
| Depth adaptation | ✅ |
| Session continuity | ✅ Cold resume |

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
