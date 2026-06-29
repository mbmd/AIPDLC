# AI-* Family — Complete Installation Guide for Cline

**Applies to:** Cline (VS Code extension) — full workflow support with `.clinerules/` integration.

> **Why Cline?** Cline reads workspace rules from `.clinerules/` and has full file system access. All workflow packages, generators, and governance rule generation work at 100%. Only AI-GCE hook auto-execution is unavailable (Kiro-only).

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
- [AI-GCE Governance on Cline](#ai-gce-governance-on-cline)
- [Session Continuity](#session-continuity)
- [Coexistence with Other Rules](#coexistence-with-other-rules)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Cline** | VS Code extension installed ([marketplace](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

Each AI-* package installs **two things** into your workspace, both **family-scoped** to the AI-* PDLC Family (core files carry a `pdlc-` filename prefix; rule-details live under a `.pdlc/` folder — so multiple AIFLC families can coexist in one workspace):

1. **Core workflow/engine file** — a Markdown file placed in `.clinerules/` (Cline reads all files in this directory automatically)
2. **Rule-details folder** — phase-specific instructions and templates that the core workflow loads on demand (placed under `.pdlc/`)

```
your-workspace/
├── .clinerules/
│   └── pdlc-ai-pilc-core.md           ← Cline reads this automatically
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

Cline reads all Markdown files in `.clinerules/` at session start. Each package gets its own `pdlc-`prefixed file in that directory.

> **The Kiro-style split:** core files load as always-on rules (`.clinerules/pdlc-*.md`); rule-details are read on demand (`.pdlc/`); and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root.

---

## Method 1: Automated Installer (Recommended)

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive
.\installer\install.ps1

# Option B: One-liner for Cline with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cline -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cline -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Cline
./installer/install.sh --target <your-project-path> --platform cline --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform cline --bundle full
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

# Copy core workflow into .clinerules/ (family-scoped filename)
New-Item -ItemType Directory -Force -Path "$Target\.clinerules"
Copy-Item "$Source\ai-pilc\ai-pilc-rules\core-workflow.md" "$Target\.clinerules\pdlc-ai-pilc-core.md"

# Copy rule-details folder (family-scoped under .pdlc/)
New-Item -ItemType Directory -Force -Path "$Target\.pdlc\ai-pilc-rule-details"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details\*" "$Target\.pdlc\ai-pilc-rule-details\"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Copy core workflow into .clinerules/ (family-scoped filename)
mkdir -p "$TARGET/.clinerules"
cp "$SOURCE/ai-pilc/ai-pilc-rules/core-workflow.md" "$TARGET/.clinerules/pdlc-ai-pilc-core.md"

# Copy rule-details folder (family-scoped under .pdlc/)
mkdir -p "$TARGET/.pdlc/ai-pilc-rule-details"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details/"* "$TARGET/.pdlc/ai-pilc-rule-details/"
```

### File Naming Convention (Cline)

| Package | Rule File | Details Folder |
|---------|-----------|----------------|
| AI-ILC | `.clinerules/pdlc-ai-ilc-core.md` | `.pdlc/ai-ilc-rule-details/` |
| AI-PILC | `.clinerules/pdlc-ai-pilc-core.md` | `.pdlc/ai-pilc-rule-details/` |
| AI-ADLC | `.clinerules/pdlc-ai-adlc-core.md` | `.pdlc/ai-adlc-rule-details/` |
| AI-UXD | `.clinerules/pdlc-ai-uxd-core.md` | `.pdlc/ai-uxd-rule-details/` |
| AI-POLC | `.clinerules/pdlc-ai-polc-core.md` | `.pdlc/ai-polc-rule-details/` |
| AI-DWG | `.clinerules/pdlc-ai-dwg-core.md` | `.pdlc/ai-dwg-rule-details/` |
| AI-GCE | `.clinerules/pdlc-ai-gce-core.md` | `.pdlc/ai-gce-rule-details/` |
| AI-TGE | `.clinerules/pdlc-ai-tge-core.md` | `.pdlc/ai-tge-rule-details/` |
| AI-PPM | `.clinerules/pdlc-ai-ppm-core.md` | `.pdlc/ai-ppm-rule-details/` |
| AI-FLO | `.clinerules/pdlc-ai-flo-core.md` | `.pdlc/ai-flo-rule-details/` |

---

## Multi-Package Installation

### Installing All 10 Packages

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cline -Bundle full
```

Or manually:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.clinerules" | Out-Null

$packages = @(
    @{ Name = "ai-ilc";  Core = "core-workflow.md";  Rules = "ai-ilc-rules";  Details = "ai-ilc-rule-details" }
    @{ Name = "ai-pilc"; Core = "core-workflow.md";  Rules = "ai-pilc-rules"; Details = "ai-pilc-rule-details" }
    @{ Name = "ai-ppm";  Core = "core-engine.md";    Rules = "ai-ppm-rules";  Details = "ai-ppm-rule-details" }
    @{ Name = "ai-flo";  Core = "core-engine.md";    Rules = "ai-flo-rules";  Details = "ai-flo-rule-details" }
    @{ Name = "ai-adlc"; Core = "core-workflow.md";  Rules = "ai-adlc-rules"; Details = "ai-adlc-rule-details" }
    @{ Name = "ai-uxd";  Core = "core-workflow.md";  Rules = "ai-uxd-rules";  Details = "ai-uxd-rule-details" }
    @{ Name = "ai-polc"; Core = "core-workflow.md";  Rules = "ai-polc-rules"; Details = "ai-polc-rule-details" }
    @{ Name = "ai-dwg";  Core = "core-generator.md"; Rules = "ai-dwg-rules";  Details = "ai-dwg-rule-details" }
    @{ Name = "ai-gce";  Core = "core-generator.md"; Rules = "ai-gce-rules";  Details = "ai-gce-rule-details" }
    @{ Name = "ai-tge";  Core = "core-engine.md";    Rules = "ai-tge-rules";  Details = "ai-tge-rule-details" }
)

foreach ($pkg in $packages) {
    $coreSource = Join-Path $Source "$($pkg.Name)\$($pkg.Rules)\$($pkg.Core)"
    $coreDest = Join-Path $Target ".clinerules\pdlc-$($pkg.Name)-core.md"
    $detailsSource = Join-Path $Source "$($pkg.Name)\$($pkg.Details)"
    $detailsDest = Join-Path $Target ".pdlc\$($pkg.Details)"

    if (Test-Path $coreSource) {
        Copy-Item $coreSource $coreDest -Force
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

---

## Resulting Workspace Structure

After a full install:

```
your-project/
├── .clinerules/
│   ├── pdlc-ai-ilc-core.md              ← Always loaded
│   ├── pdlc-ai-pilc-core.md             ← Always loaded
│   ├── pdlc-ai-ppm-core.md              ← Always loaded
│   ├── pdlc-ai-flo-core.md              ← Always loaded
│   ├── pdlc-ai-adlc-core.md             ← Always loaded
│   ├── pdlc-ai-uxd-core.md              ← Always loaded
│   ├── pdlc-ai-polc-core.md             ← Always loaded
│   ├── pdlc-ai-dwg-core.md              ← Always loaded
│   ├── pdlc-ai-gce-core.md              ← Always loaded
│   └── pdlc-ai-tge-core.md              ← Always loaded
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

1. Open your workspace in VS Code with Cline extension active
2. Start a new Cline chat
3. Type: "Using AI-PILC, initiate a project"
4. **Expected:** The AI responds with the package's welcome message and begins the structured workflow

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell the AI which package to use with the activation phrase
2. **Choose depth:** Minimal, Standard, or Comprehensive
3. **Work through stages:** The AI guides you sequentially
4. **Approve at gates:** Output presented for approval before proceeding
5. **Get deliverables:** Each stage produces one professional deliverable (written to disk)

---

## Chain Handoffs Between Packages

Packages detect each other through **state marker files** (e.g., `pilc-state.md`). Run packages sequentially and they find each other's output automatically.

---

## AI-GCE Governance on Cline

AI-GCE generates all governance files correctly, but enforcement is advisory:

| Feature | Status | Workaround |
|---------|--------|------------|
| Rule generation | ✅ Works | — |
| Hook auto-execution | ❌ | Add a governance rule file in `.clinerules/` |
| Agent triggers | ❌ | Paste agent prompts manually |
| Compliance logging | ⚠️ Manual | Ask the AI to log checks |

### Best Practice

After AI-GCE generates governance, add a summary file:

```bash
cp .governance/COMPLIANCE_README.md .clinerules/governance-rules.md
```

This ensures Cline always has the governance context loaded.

---

## Session Continuity

State files persist between sessions. Say "Continue AI-PILC" to resume where you left off.

---

## Coexistence with Other Rules

- **Existing `.clinerules/`**: Untouched. AI-* packages add their own files alongside yours.
- **Other project files**: Never modified.

---

## Uninstalling

```powershell
# Via installer
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall

# Manual
Remove-Item "<your-project-path>\.clinerules\pdlc-ai-*"
Get-ChildItem "<your-project-path>\.pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Rules not loading | Cline not reading `.clinerules/` | Verify the folder exists at workspace root and files are `.md` |
| "Can't find rule-details" | Path mismatch | Ensure `.pdlc/ai-{pkg}-rule-details/` exists at workspace root |
| No welcome message | Wrong activation phrase | Use "Using AI-PILC, ..." format |
| State file not created | First interaction only | State is created after first stage completes |

---

## Platform Capabilities Summary

| Feature | Cline |
|---------|:-----:|
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
