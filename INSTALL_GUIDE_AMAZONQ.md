# AI-* Family — Complete Installation Guide for Amazon Q Developer

**Applies to:** Amazon Q Developer — full workflow support with `.amazonq/rules/` integration.

> **Why Amazon Q?** Amazon Q Developer reads workspace rules from `.amazonq/rules/` and has full file system access. All workflow packages, generators, and governance rule generation work at 100%. Only AI-GCE hook auto-execution is unavailable (Kiro-only).

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
- [AI-GCE Governance on Amazon Q](#ai-gce-governance-on-amazon-q)
- [Session Continuity](#session-continuity)
- [Coexistence with Other Rules](#coexistence-with-other-rules)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Amazon Q Developer** | VS Code extension or JetBrains plugin installed |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

Each AI-* package installs **two things** into your workspace, both **family-scoped** under a `pdlc/` segment (this is the AI-* PDLC Family — every package file lives under the family name so multiple AIFLC families can coexist in one workspace):

1. **Core workflow/engine file** — a Markdown file placed in `.amazonq/rules/pdlc/` (Amazon Q reads these automatically)
2. **Rule-details folder** — phase-specific instructions and templates loaded on demand during execution (placed in `.amazonq/pdlc/`)

```
your-workspace/
├── .amazonq/
│   ├── rules/
│   │   └── pdlc/
│   │       └── ai-pilc-rules/
│   │           └── core-workflow.md       ← Always loaded by Amazon Q
│   └── pdlc/
│       └── ai-pilc-rule-details/          ← Loaded on-demand by the core workflow
│           ├── common/
│           ├── inception/
│           ├── assessment/
│           ├── templates/
│           └── ...
├── pdlc-ws/                               ← All runtime outputs land here (never workspace root)
└── (your project files)
```

Amazon Q reads all files in `.amazonq/rules/` (including the `pdlc/` subfolder) at session start. The rule-details folders sit alongside in `.amazonq/pdlc/` and get read on demand when the workflow transitions to each phase.

> **The Kiro-style split:** core files load as always-on rules (`.amazonq/rules/pdlc/`); rule-details are read on demand (`.amazonq/pdlc/`); and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root.

---

## Method 1: Automated Installer (Recommended)

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive
.\installer\install.ps1

# Option B: One-liner for Amazon Q with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform amazonq -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform amazonq -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Amazon Q
./installer/install.sh --target <your-project-path> --platform amazonq --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform amazonq --bundle full
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

# Copy steering rules (core workflow — always loaded), family-scoped under pdlc/
New-Item -ItemType Directory -Force -Path "$Target\.amazonq\rules\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.amazonq\rules\pdlc\"

# Copy rule details (phase instructions + templates — on demand), family-scoped under pdlc/
New-Item -ItemType Directory -Force -Path "$Target\.amazonq\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.amazonq\pdlc\"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Copy steering rules (family-scoped under pdlc/)
mkdir -p "$TARGET/.amazonq/rules/pdlc"
cp -R "$SOURCE/ai-pilc/ai-pilc-rules" "$TARGET/.amazonq/rules/pdlc/"

# Copy rule details (family-scoped under pdlc/)
mkdir -p "$TARGET/.amazonq/pdlc"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details" "$TARGET/.amazonq/pdlc/"
```

### File Placement Convention (Amazon Q)

| Package | Rules (always loaded) | Details (on-demand) |
|---------|----------------------|---------------------|
| AI-ILC | `.amazonq/rules/pdlc/ai-ilc-rules/core-workflow.md` | `.amazonq/pdlc/ai-ilc-rule-details/` |
| AI-PILC | `.amazonq/rules/pdlc/ai-pilc-rules/core-workflow.md` | `.amazonq/pdlc/ai-pilc-rule-details/` |
| AI-ADLC | `.amazonq/rules/pdlc/ai-adlc-rules/core-workflow.md` | `.amazonq/pdlc/ai-adlc-rule-details/` |
| AI-UXD | `.amazonq/rules/pdlc/ai-uxd-rules/core-workflow.md` | `.amazonq/pdlc/ai-uxd-rule-details/` |
| AI-POLC | `.amazonq/rules/pdlc/ai-polc-rules/core-workflow.md` | `.amazonq/pdlc/ai-polc-rule-details/` |
| AI-DWG | `.amazonq/rules/pdlc/ai-dwg-rules/core-generator.md` | `.amazonq/pdlc/ai-dwg-rule-details/` |
| AI-GCE | `.amazonq/rules/pdlc/ai-gce-rules/core-generator.md` | `.amazonq/pdlc/ai-gce-rule-details/` |
| AI-TGE | `.amazonq/rules/pdlc/ai-tge-rules/core-engine.md` | `.amazonq/pdlc/ai-tge-rule-details/` |
| AI-PPM | `.amazonq/rules/pdlc/ai-ppm-rules/core-engine.md` | `.amazonq/pdlc/ai-ppm-rule-details/` |
| AI-FLO | `.amazonq/rules/pdlc/ai-flo-rules/core-engine.md` | `.amazonq/pdlc/ai-flo-rule-details/` |

---

## Multi-Package Installation

### Installing All 10 Packages

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform amazonq -Bundle full
```

Or manually:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.amazonq\rules\pdlc" | Out-Null
New-Item -ItemType Directory -Force -Path "$Target\.amazonq\pdlc" | Out-Null

$packages = @(
    "ai-ilc", "ai-pilc", "ai-ppm", "ai-flo", "ai-adlc",
    "ai-uxd", "ai-polc", "ai-dwg", "ai-gce", "ai-tge"
)

foreach ($pkg in $packages) {
    $rulesSource = Join-Path $Source "$pkg\$pkg-rules"
    $detailsSource = Join-Path $Source "$pkg\$pkg-rule-details"

    if (Test-Path $rulesSource) {
        Copy-Item -Recurse $rulesSource "$Target\.amazonq\rules\pdlc\" -Force
        Write-Host "Rules installed: $pkg" -ForegroundColor Green
    }
    if (Test-Path $detailsSource) {
        Copy-Item -Recurse $detailsSource "$Target\.amazonq\pdlc\" -Force
        Write-Host "Details installed: $pkg" -ForegroundColor Green
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
├── .amazonq/
│   ├── rules/
│   │   └── pdlc/                         ← AI-* PDLC Family scope
│   │       ├── ai-ilc-rules/
│   │       │   └── core-workflow.md         ← Always loaded
│   │       ├── ai-pilc-rules/
│   │       │   └── core-workflow.md         ← Always loaded
│   │       ├── ai-ppm-rules/
│   │       │   └── core-engine.md           ← Always loaded
│   │       ├── ai-flo-rules/
│   │       │   └── core-engine.md           ← Always loaded
│   │       ├── ai-adlc-rules/
│   │       │   └── core-workflow.md         ← Always loaded
│   │       ├── ai-uxd-rules/
│   │       │   └── core-workflow.md         ← Always loaded
│   │       ├── ai-polc-rules/
│   │       │   └── core-workflow.md         ← Always loaded
│   │       ├── ai-dwg-rules/
│   │       │   └── core-generator.md        ← Always loaded
│   │       ├── ai-gce-rules/
│   │       │   └── core-generator.md        ← Always loaded
│   │       └── ai-tge-rules/
│   │           └── core-engine.md           ← Always loaded
│   └── pdlc/                             ← AI-* PDLC Family rule-details (on-demand)
│       ├── ai-ilc-rule-details/
│       ├── ai-pilc-rule-details/
│       ├── ai-adlc-rule-details/
│       ├── ai-uxd-rule-details/
│       ├── ai-polc-rule-details/
│       ├── ai-ppm-rule-details/
│       ├── ai-flo-rule-details/
│       ├── ai-dwg-rule-details/
│       ├── ai-gce-rule-details/
│       └── ai-tge-rule-details/
├── pdlc-ws/                             ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   └── .ai-family-manifest.json         ← Installer tracking
└── (your project files)
```

---

## Verification

1. Open your workspace in VS Code with Amazon Q Developer active
2. Start a new Amazon Q chat
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

### Depth Levels

| Level | Output Volume | Best For |
|-------|--------------|----------|
| **Minimal** | Key essentials only | Prototypes, small projects |
| **Standard** | Professional baseline | Most projects (recommended) |
| **Comprehensive** | Enterprise-grade detail | Regulated industries, large teams |

---

## Chain Handoffs Between Packages

Packages detect each other through **state marker files** (e.g., `pilc-state.md`). Run packages sequentially and they find each other's output automatically.

---

## AI-GCE Governance on Amazon Q

AI-GCE generates all governance files correctly, but enforcement is advisory:

| Feature | Status | Workaround |
|---------|--------|------------|
| Rule generation | ✅ Works | — |
| Hook auto-execution | ❌ | Include governance rules in `.amazonq/rules/` |
| Agent triggers | ❌ | Paste agent prompts manually |
| Compliance logging | ⚠️ Manual | Ask the AI to log checks |

### Best Practice

After AI-GCE generates governance, copy the compliance summary:

```powershell
Copy-Item ".governance\COMPLIANCE_README.md" "$Target\.amazonq\rules\governance-enforce.md"
```

This ensures Amazon Q always has governance context loaded alongside the workflow packages.

---

## Session Continuity

State files persist between sessions. Say "Continue AI-PILC" to resume where you left off.

---

## Coexistence with Other Rules

- **Existing `.amazonq/rules/`**: Untouched. AI-* packages add their own rule folders alongside yours.
- **Other project files**: Never modified.

---

## Uninstalling

```powershell
# Via installer
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall

# Manual
Get-ChildItem "<your-project-path>\.amazonq\rules\pdlc\ai-*-rules" -Directory | Remove-Item -Recurse -Force
Get-ChildItem "<your-project-path>\.amazonq\pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Rules not loading | Folder structure wrong | Verify `.amazonq/rules/pdlc/ai-{pkg}-rules/` exists |
| "Can't find rule-details" | Path mismatch | Ensure `.amazonq/pdlc/ai-{pkg}-rule-details/` exists |
| No welcome message | Wrong activation phrase | Use "Using AI-PILC, ..." format |
| State file not created | First interaction only | State is created after first stage completes |

---

## Platform Capabilities Summary

| Feature | Amazon Q |
|---------|:--------:|
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
