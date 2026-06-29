# AI-* Family — Complete Installation Guide for OpenAI Codex

**Applies to:** OpenAI Codex CLI — full workflow support with `AGENTS.md` integration.

> **Why Codex?** Codex CLI is a sandboxed coding agent with full workspace file access. It reads `AGENTS.md` files automatically at every session start, supports on-demand file reading, and writes deliverables to disk. All workflow packages, generators, and governance rule generation work at 100%. Only AI-GCE hook auto-execution is unavailable (Kiro-only).

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
- [AI-GCE Governance on Codex](#ai-gce-governance-on-codex)
- [Session Continuity](#session-continuity)
- [Coexistence with Other Instructions](#coexistence-with-other-instructions)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **OpenAI Codex CLI** | Installed and authenticated (`npm install -g @openai/codex`) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Python, Docker, or any additional runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

Each AI-* package installs **two things** into your workspace, both **family-scoped** to the AI-* PDLC Family (core files live under an `.ai-rules/pdlc/` folder segment; rule-details live under a `.pdlc/` folder — so multiple AIFLC families can coexist in one workspace):

1. **Core workflow/engine file** — a Markdown file that Codex reads automatically at session start (placed as the root `AGENTS.md` index plus per-package `AGENTS.md` files under `.ai-rules/pdlc/`)
2. **Rule-details folder** — phase-specific instructions and templates that the core workflow loads on demand during execution (placed under `.pdlc/`)

```
your-workspace/
├── AGENTS.md                      ← Codex reads this automatically (always-loaded steering)
├── .pdlc/
│   └── ai-pilc-rule-details/      ← Loaded on-demand by the core workflow
│       ├── common/
│       ├── inception/
│       ├── assessment/
│       ├── templates/
│       └── ...
├── pdlc-ws/                       ← All runtime outputs land here (never workspace root)
└── (your project files)
```

Codex reads `AGENTS.md` at the workspace root on every session start. This is how the packages inject their expertise into Codex's context without you needing to paste anything.

> **The Kiro-style split:** core files load as always-on steering (root `AGENTS.md` + `.ai-rules/pdlc/`); rule-details are read on demand (`.pdlc/`); and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root.

### Subdirectory AGENTS.md (Multi-Package Approach)

Codex supports hierarchical `AGENTS.md` files — it reads the root file plus any `AGENTS.md` in subdirectories relevant to the work. The installer leverages this for multi-package installs, family-scoped under `.ai-rules/pdlc/`:

```
your-workspace/
├── AGENTS.md                      ← Root: package index + shared instructions
├── .ai-rules/
│   └── pdlc/                      ← AI-* PDLC Family scope
│       ├── AGENTS.md              ← Optional: aggregated workflows (Codex reads this too)
│       ├── ai-pilc/
│       │   └── AGENTS.md          ← AI-PILC core workflow
│       ├── ai-adlc/
│       │   └── AGENTS.md          ← AI-ADLC core workflow
│       └── ai-dwg/
│           └── AGENTS.md          ← AI-DWG core workflow
├── .pdlc/
│   └── ai-pilc-rule-details/      ← On-demand details
├── pdlc-ws/                       ← All runtime outputs
└── (your project files)
```

---

## Method 1: Automated Installer (Recommended)

The interactive installer handles all file placement automatically.

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive (asks platform, packages, target)
.\installer\install.ps1

# Option B: One-liner for Codex with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform codex -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform codex -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Codex
./installer/install.sh --target <your-project-path> --platform codex --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform codex --bundle full
```

### Preset Bundles

| Bundle | Command Flag | Packages | Best For |
|--------|-------------|----------|----------|
| **Greenfield Full** | `-Bundle full` | AI-ILC + AI-PILC + AI-PPM + AI-FLO + AI-POLC + AI-UXD + AI-ADLC + AI-DWG + AI-GCE + AI-TGE + AI-DFE | New project, complete family |
| **Greenfield Minimal** | `-Bundle minimal` | AI-PILC + AI-ADLC + AI-DWG | Quick start, architecture focus |
| **Architecture Focus** | `-Bundle arch` | AI-ADLC + AI-DWG + AI-GCE | Architecture → workspace → governance |
| **Governance Only** | `-Bundle governance` | AI-GCE + AI-TGE | Existing project, add compliance |
| **Portfolio** | `-Bundle portfolio` | AI-ILC + AI-PILC + AI-PPM + AI-FLO | Multi-project management |

### Dry Run (Preview Without Installing)

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform codex -Bundle full -DryRun
```

---

## Method 2: Manual Installation

### Single Package Example (AI-PILC)

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Copy the core workflow as AGENTS.md (Codex reads this automatically)
Copy-Item "$Source\ai-pilc\ai-pilc-rules\core-workflow.md" "$Target\AGENTS.md"

# Copy the rule-details folder (family-scoped under .pdlc/)
New-Item -ItemType Directory -Force -Path "$Target\.pdlc\ai-pilc-rule-details"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details\*" "$Target\.pdlc\ai-pilc-rule-details\"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Copy the core workflow as AGENTS.md
cp "$SOURCE/ai-pilc/ai-pilc-rules/core-workflow.md" "$TARGET/AGENTS.md"

# Copy the rule-details folder (family-scoped under .pdlc/)
mkdir -p "$TARGET/.pdlc/ai-pilc-rule-details"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details/"* "$TARGET/.pdlc/ai-pilc-rule-details/"
```

### Multi-Package Manual Install (Subdirectory Approach)

For multiple packages, use the subdirectory pattern so each package gets its own `AGENTS.md`:

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Create the rules directory structure (family-scoped under .ai-rules/pdlc/)
New-Item -ItemType Directory -Force -Path "$Target\.ai-rules\pdlc"

# Install AI-PILC
New-Item -ItemType Directory -Force -Path "$Target\.ai-rules\pdlc\ai-pilc"
Copy-Item "$Source\ai-pilc\ai-pilc-rules\core-workflow.md" "$Target\.ai-rules\pdlc\ai-pilc\AGENTS.md"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.pdlc\ai-pilc-rule-details"

# Install AI-ADLC
New-Item -ItemType Directory -Force -Path "$Target\.ai-rules\pdlc\ai-adlc"
Copy-Item "$Source\ai-adlc\ai-adlc-rules\core-workflow.md" "$Target\.ai-rules\pdlc\ai-adlc\AGENTS.md"
Copy-Item -Recurse "$Source\ai-adlc\ai-adlc-rule-details" "$Target\.pdlc\ai-adlc-rule-details"

# Install AI-DWG
New-Item -ItemType Directory -Force -Path "$Target\.ai-rules\pdlc\ai-dwg"
Copy-Item "$Source\ai-dwg\ai-dwg-rules\core-generator.md" "$Target\.ai-rules\pdlc\ai-dwg\AGENTS.md"
Copy-Item -Recurse "$Source\ai-dwg\ai-dwg-rule-details" "$Target\.pdlc\ai-dwg-rule-details"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Create the rules directory structure (family-scoped under .ai-rules/pdlc/)
mkdir -p "$TARGET/.ai-rules/pdlc"

# Install AI-PILC
mkdir -p "$TARGET/.ai-rules/pdlc/ai-pilc"
cp "$SOURCE/ai-pilc/ai-pilc-rules/core-workflow.md" "$TARGET/.ai-rules/pdlc/ai-pilc/AGENTS.md"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details" "$TARGET/.pdlc/ai-pilc-rule-details"

# Install AI-ADLC
mkdir -p "$TARGET/.ai-rules/pdlc/ai-adlc"
cp "$SOURCE/ai-adlc/ai-adlc-rules/core-workflow.md" "$TARGET/.ai-rules/pdlc/ai-adlc/AGENTS.md"
cp -R "$SOURCE/ai-adlc/ai-adlc-rule-details" "$TARGET/.pdlc/ai-adlc-rule-details"

# Install AI-DWG
mkdir -p "$TARGET/.ai-rules/pdlc/ai-dwg"
cp "$SOURCE/ai-dwg/ai-dwg-rules/core-generator.md" "$TARGET/.ai-rules/pdlc/ai-dwg/AGENTS.md"
cp -R "$SOURCE/ai-dwg/ai-dwg-rule-details" "$TARGET/.pdlc/ai-dwg-rule-details"
```

### Alternative: Single Root AGENTS.md (Concatenated)

If you prefer a single root `AGENTS.md` with all packages merged:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

$header = @"
# AI-* Family Steering (AIFLC)

This workspace uses AIFLC injectable workflow packages.
Activate a package by saying: "Using AI-{PKG}, ..."

---

"@
$header | Out-File -FilePath "$Target\AGENTS.md" -Encoding utf8

$packages = @(
    @{ Name = "ai-pilc"; Core = "core-workflow.md";  Rules = "ai-pilc-rules";  Details = "ai-pilc-rule-details" }
    @{ Name = "ai-adlc"; Core = "core-workflow.md";  Rules = "ai-adlc-rules"; Details = "ai-adlc-rule-details" }
    @{ Name = "ai-dwg";  Core = "core-generator.md"; Rules = "ai-dwg-rules";  Details = "ai-dwg-rule-details" }
)

foreach ($pkg in $packages) {
    $coreSource = Join-Path $Source "$($pkg.Name)\$($pkg.Rules)\$($pkg.Core)"
    if (Test-Path $coreSource) {
        "`n---`n`n## PDLC / $($pkg.Name.ToUpper())`n`n" | Add-Content "$Target\AGENTS.md"
        Get-Content $coreSource -Raw | Add-Content "$Target\AGENTS.md"
        $detailsSource = Join-Path $Source "$($pkg.Name)\$($pkg.Details)"
        if (Test-Path $detailsSource) {
            Copy-Item -Recurse $detailsSource "$Target\.pdlc\$($pkg.Details)" -Force
        }
    }
}
```

> **Trade-off:** Single file is simpler; subdirectory approach allows independent updates per package.

### File Placement Convention (Codex)

| Package | Core File (always loaded) | Details Folder (on-demand) |
|---------|--------------------------|---------------------------|
| AI-ILC | `.ai-rules/pdlc/ai-ilc/AGENTS.md` | `.pdlc/ai-ilc-rule-details/` |
| AI-PILC | `.ai-rules/pdlc/ai-pilc/AGENTS.md` | `.pdlc/ai-pilc-rule-details/` |
| AI-ADLC | `.ai-rules/pdlc/ai-adlc/AGENTS.md` | `.pdlc/ai-adlc-rule-details/` |
| AI-UXD | `.ai-rules/pdlc/ai-uxd/AGENTS.md` | `.pdlc/ai-uxd-rule-details/` |
| AI-POLC | `.ai-rules/pdlc/ai-polc/AGENTS.md` | `.pdlc/ai-polc-rule-details/` |
| AI-DWG | `.ai-rules/pdlc/ai-dwg/AGENTS.md` | `.pdlc/ai-dwg-rule-details/` |
| AI-GCE | `.ai-rules/pdlc/ai-gce/AGENTS.md` | `.pdlc/ai-gce-rule-details/` |
| AI-TGE | `.ai-rules/pdlc/ai-tge/AGENTS.md` | `.pdlc/ai-tge-rule-details/` |
| AI-PPM | `.ai-rules/pdlc/ai-ppm/AGENTS.md` | `.pdlc/ai-ppm-rule-details/` |
| AI-FLO | `.ai-rules/pdlc/ai-flo/AGENTS.md` | `.pdlc/ai-flo-rule-details/` |

---

## Multi-Package Installation

### Installing All 10 Packages (Full Chain)

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform codex -Bundle full
```

Or manually:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.ai-rules\pdlc" | Out-Null

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
    $pkgDir = Join-Path $Target ".ai-rules\pdlc\$($pkg.Name)"
    New-Item -ItemType Directory -Force -Path $pkgDir | Out-Null

    $coreSource = Join-Path $Source "$($pkg.Name)\$($pkg.Rules)\$($pkg.Core)"
    if (Test-Path $coreSource) {
        Copy-Item $coreSource (Join-Path $pkgDir "AGENTS.md") -Force
        $detailsSource = Join-Path $Source "$($pkg.Name)\$($pkg.Details)"
        $detailsDest = Join-Path $Target ".pdlc\$($pkg.Details)"
        if (Test-Path $detailsSource) {
            if (Test-Path $detailsDest) { Remove-Item -Recurse -Force $detailsDest }
            Copy-Item -Recurse $detailsSource $detailsDest
        }
        Write-Host "Installed $($pkg.Name)" -ForegroundColor Green
    } else {
        Write-Host "Skipped $($pkg.Name) - source not found" -ForegroundColor Yellow
    }
}

# Create root AGENTS.md with package index
$rootAgents = @"
# AI-* Family (AIFLC) — Package Index

This workspace has AIFLC injectable workflow packages installed.

## Installed Packages

Activate any package by saying: "Using AI-{PKG}, ..."

| Package | Activation | What It Does |
|---------|-----------|--------------|
| AI-ILC | "Using AI-ILC, evaluate this idea" | Idea evaluation → Approved Brief |
| AI-PILC | "Using AI-PILC, initiate a project" | Requirement → Project Initiation Package |
| AI-PPM | "Using AI-PPM, manage my portfolio" | Portfolio governance |
| AI-FLO | "Using AI-FLO, route this output" | Inter-package handoff routing |
| AI-ADLC | "Using AI-ADLC, design the architecture" | Requirements → Architecture Package |
| AI-UXD | "Using AI-UXD, design the user experience" | PIP/AP → UX Design Package |
| AI-POLC | "Using AI-POLC, build the product backlog" | PIP/AP → Product Backlog |
| AI-DWG | "Using AI-DWG, generate the workspace" | Architecture → Ready-to-code workspace |
| AI-GCE | "Using AI-GCE, set up governance" | Workspace → Compliance enforcement |
| AI-TGE | "Using AI-TGE, establish test governance" | Workspace → Test strategy |

## How It Works

Each package's full instructions are in `.ai-rules/pdlc/{package}/AGENTS.md`.
Phase-specific details are in `.pdlc/{package}-rule-details/` (loaded on demand during execution).
State markers (e.g. `pilc-state.md`) enable chain handoffs between packages.
"@
$rootAgents | Out-File -FilePath "$Target\AGENTS.md" -Encoding utf8
```

### Context Window Consideration

Codex loads `AGENTS.md` files from the workspace hierarchy. With 10 packages installed in subdirectories:

- **Recommended:** Install only the packages you'll use in a given project. Most projects need 3–5 packages, not all 10.
- **If installing all 10:** Core files are orchestration logic (1–3 KB each). The root `AGENTS.md` serves as a lightweight index; subdirectory files are loaded based on relevance.
- **The AI activates only one package at a time** — the others are dormant until you invoke them.

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
| Need UX design alongside architecture | AI-UXD | (runs parallel to AI-ADLC) |
| Need a product backlog | AI-POLC | (runs parallel to AI-ADLC) |

---

## Resulting Workspace Structure

After a full install (`-Bundle full`), your workspace looks like this:

```
your-project/
├── AGENTS.md                            ← Root: package index (always loaded by Codex)
├── .ai-rules/
│   └── pdlc/                            ← AI-* PDLC Family scope
│       ├── ai-ilc/
│       │   └── AGENTS.md               ← AI-ILC core workflow
│       ├── ai-pilc/
│       │   └── AGENTS.md               ← AI-PILC core workflow
│       ├── ai-ppm/
│       │   └── AGENTS.md               ← AI-PPM core engine
│       ├── ai-flo/
│       │   └── AGENTS.md               ← AI-FLO core engine
│       ├── ai-adlc/
│       │   └── AGENTS.md               ← AI-ADLC core workflow
│       ├── ai-uxd/
│       │   └── AGENTS.md               ← AI-UXD core workflow
│       ├── ai-polc/
│       │   └── AGENTS.md               ← AI-POLC core workflow
│       ├── ai-dwg/
│       │   └── AGENTS.md               ← AI-DWG core generator
│       ├── ai-gce/
│       │   └── AGENTS.md               ← AI-GCE core generator
│       └── ai-tge/
│           └── AGENTS.md               ← AI-TGE core engine
├── .pdlc/                               ← AI-* PDLC Family rule-details (on-demand)
│   ├── ai-ilc-rule-details/                ← idea lifecycle details
│   ├── ai-pilc-rule-details/               ← project initiation details
│   │   ├── common/
│   │   ├── inception/
│   │   ├── assessment/
│   │   ├── justification/
│   │   ├── authorization/
│   │   ├── planning/
│   │   ├── mobilization/
│   │   └── templates/
│   ├── ai-adlc-rule-details/               ← architecture design details
│   ├── ai-uxd-rule-details/                ← UX design details
│   ├── ai-polc-rule-details/               ← product ownership details
│   ├── ai-ppm-rule-details/                ← portfolio management details
│   ├── ai-flo-rule-details/                ← flow routing details
│   ├── ai-dwg-rule-details/                ← workspace generation details
│   ├── ai-gce-rule-details/                ← governance engine details
│   └── ai-tge-rule-details/                ← test governance details
├── pdlc-ws/                             ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   ├── .ai-family-manifest.json         ← Installer tracking (for uninstall)
│   └── tools/                           ← Family tools (visual tools / extensions)
│       └── extensions/
│           ├── AIFLC-PDLC-Dashboard/    ← HTML dashboard + .vsix (reads ../../data/ via AI-DFE)
│           └── AIFLC-CommandBoard/      ← Trigger palette (HTML + .vsix)
└── (your project files)
```

> **Note:** The `.ai-rules/` and `.pdlc/` folders are dot-prefixed (hidden) and won't clutter your project view in most file explorers.

---

## Verification

After installation, verify everything is working:

### Step 1: Confirm files are in place

```powershell
# Windows
Get-ChildItem "<your-project-path>\AGENTS.md"
Get-ChildItem "<your-project-path>\.ai-rules\pdlc" -Directory
Get-ChildItem "<your-project-path>\.pdlc\ai-*-rule-details" -Directory
```

```bash
# macOS/Linux
ls <your-project-path>/AGENTS.md
ls -d <your-project-path>/.ai-rules/pdlc/*/
ls -d <your-project-path>/.pdlc/ai-*-rule-details/
```

### Step 2: Start Codex in your workspace

```bash
# Navigate to your project
cd <your-project-path>

# Start Codex CLI
codex
```

### Step 3: Test activation

Type one of these prompts:

```
Using AI-PILC, initiate a project from this requirement: [paste your requirement]
```

```
Using AI-ADLC, design the architecture for this system: [describe your system]
```

```
Using AI-ILC, evaluate this idea: [describe your idea]
```

**Expected:** Codex should respond with the package's welcome message and begin the structured workflow, asking about depth level and presenting the first stage.

### Step 4: Verify on-demand loading

During a workflow, when Codex transitions to a new phase, it reads the corresponding rule-details file. You'll see file-read operations in Codex's output referencing paths like `.pdlc/ai-pilc-rule-details/inception/stage-01-...`.

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell Codex which package to use with the activation phrase
2. **Choose depth:** The package asks if you want Minimal, Standard, or Comprehensive output
3. **Work through stages:** Each package has defined stages. Codex guides you through them sequentially
4. **Approve at gates:** At the end of each stage, Codex presents output and waits for your approval before proceeding
5. **Get deliverables:** Each stage produces one professional deliverable (written to disk as a file)

### Depth Levels

| Level | Output Volume | Best For |
|-------|--------------|----------|
| **Minimal** | Key essentials only | Prototypes, small projects, time-pressed |
| **Standard** | Professional baseline | Most projects (recommended default) |
| **Comprehensive** | Enterprise-grade detail | Regulated industries, large teams, audit-heavy |

### Example: Running AI-PILC

```
You: Using AI-PILC, initiate a project from this requirement:

We need a customer portal that allows clients to submit and track support
tickets, view their account status, and download invoices. It should
integrate with our existing Salesforce CRM and support SSO via Azure AD.
Target launch is Q1 2027 with a budget around $400K.
```

Codex will respond with the AI-PILC welcome, ask about depth, then walk you through 6 phases / 16 stages producing professional deliverables at each gate.

---

## Chain Handoffs Between Packages

Packages detect each other's output through **state marker files**. When a package completes, it writes a marker (e.g., `pilc-state.md`). When the next package starts, it looks for upstream markers and enriches its work with that context.

### Example Chain: PILC → POLC → UXD → ADLC → DWG

```
1. Run AI-PILC → produces Project Initiation Package (PIP) + pilc-state.md
2. Run AI-POLC → detects pilc-state.md, reads PIP as input → produces Product Backlog Package (PBP) + polc-state.md
3. Run AI-UXD → detects pilc-state.md + polc-state.md → produces UX Design Package (UXP) + uxd-state.md
4. Run AI-ADLC → detects pilc-state.md + polc-state.md + uxd-state.md → produces Architecture Package (AP) + adlc-state.md
5. Run AI-DWG → detects adlc-state.md (+ polc-state.md, uxd-state.md) → generates ready-to-code workspace
```

**No manual wiring needed.** Just run packages sequentially and they find each other's output automatically.

---

## AI-GCE Governance on Codex

AI-GCE generates all governance files correctly on Codex, but enforcement is advisory rather than automatic:

### What Works (100%)

- Rule generation (`.governance/rules/`) — full mode 1/2/3/4
- Compliance documentation
- Brownfield baseline scanning
- Hook and agent file generation (structurally valid but inert)

### What Doesn't Work (Kiro-only features)

| Feature | Why | Workaround |
|---------|-----|------------|
| Hook auto-execution | No event bus in Codex | Add governance rules to root `AGENTS.md` |
| Agent shortcut triggers | No `.kiro/agents/` runtime | Paste agent prompts manually when needed |
| Automatic compliance logging | Triggered by hooks | Ask Codex to log manually |
| Re-derivation auto-trigger | Requires file-edit events | Say "re-derive governance" manually |

### Best Practice: Maximizing Governance Value

After AI-GCE generates your governance layer, append this to your root `AGENTS.md`:

```markdown
## Governance Rules (Always Enforce)

The following rules from `.governance/rules/` apply to ALL work in this workspace.
Check compliance on every file you create or modify.

- See: .governance/rules/security-rules.md (CRITICAL)
- See: .governance/rules/architecture-rules.md
- See: .governance/rules/naming-conventions.md
- See: .governance/COMPLIANCE_README.md for full rule index
```

Then periodically ask Codex: "Run a compliance check against `.governance/rules/` on recent changes."

This gives you ~70% of Kiro's enforcement value through advisory compliance.

---

## Session Continuity

Each workflow package maintains a **state file** (e.g., `pilc-state.md`) that records:
- Current phase and stage
- Completed stages
- Pending decisions
- Selected depth level
- Key outputs produced

**This means you can close Codex and resume later.** When you start a new session and say "Continue AI-PILC", Codex reads the state file and picks up exactly where you left off.

> **Important:** Don't delete state files unless you want to restart a workflow from scratch.

---

## Coexistence with Other Instructions

AI-* package files coexist peacefully with your existing Codex configuration:

- **Existing `AGENTS.md`**: The installer merges or appends to your existing file (never overwrites without asking).
- **Existing subdirectory `AGENTS.md` files**: Untouched. Packages use `.ai-rules/pdlc/` as their namespace.
- **Other project files**: Never modified. Only AI-* steering files are added.
- **Package isolation**: Each package activates ONLY when you invoke it by name. Dormant packages don't interfere.

### Approval Mode Compatibility

Codex's sandbox and approval modes work transparently with AI-* packages:

| Mode | Compatibility |
|------|--------------|
| `suggest` (default) | ✅ Full — Codex proposes file writes, you approve |
| `auto-edit` | ✅ Full — file writes happen automatically |
| `full-auto` | ✅ Full — entire workflow runs hands-free |

> **Recommendation:** Use `auto-edit` or default `suggest` mode for your first run so you can see what each stage produces before it writes to disk.

---

## Uninstalling

### Via Installer

```powershell
# Windows
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall
```

```bash
# macOS/Linux
./installer/install.sh --target <your-project-path> --uninstall
```

The installer reads `.ai-family-manifest.json` and removes exactly what it installed.

### Manual Removal

```powershell
# Remove the family rules directory
Remove-Item -Recurse -Force "<your-project-path>\.ai-rules\pdlc"

# Remove all rule-details folders
Get-ChildItem "<your-project-path>\.pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force

# Remove the manifest (lives under pdlc-ws/)
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue

# Remove installed family tools (extensions)
Remove-Item "<your-project-path>\pdlc-ws\tools\extensions" -Recurse -Force -ErrorAction SilentlyContinue

# Remove runtime outputs if you want a clean slate (this deletes all generated work — back up first)
# Remove-Item "<your-project-path>\pdlc-ws" -Recurse -Force -ErrorAction SilentlyContinue

# Remove or revert root AGENTS.md (if you had a pre-existing one, restore from git)
Remove-Item "<your-project-path>\AGENTS.md" -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Codex doesn't recognize the package | Root `AGENTS.md` missing or not referencing packages | Verify `AGENTS.md` exists at workspace root with the package index |
| "Can't find rule-details" | Path mismatch | Ensure `.pdlc/ai-{pkg}-rule-details/` exists at workspace root |
| No welcome message | Wrong activation phrase | Use the exact format: "Using AI-PILC, ..." (uppercase package name) |
| State file not created | First interaction only | State is created after the first stage completes, not immediately |
| Chain detection not working | Upstream state file missing | Run packages in order. Verify `pilc-state.md` exists before running AI-ADLC |
| Sandbox blocks file writes | Restrictive sandbox mode | Use `--sandbox workspace-write` or `auto-edit` mode |
| Codex not reading subdirectory AGENTS.md | Version-dependent behavior | Use the concatenated single-file approach instead (see Alternative above) |
| Context window getting large | Too many packages loaded | Remove packages you don't actively need |

---

## Platform Capabilities Summary

| Feature | Codex CLI |
|---------|:---------:|
| Core workflow execution | ✅ |
| On-demand file loading | ✅ |
| Deliverable file output | ✅ |
| State persistence | ✅ |
| Chain marker detection | ✅ |
| Multi-package install | ✅ All 10 |
| AI-DWG workspace gen | ✅ |
| AI-GCE rule generation | ✅ |
| AI-GCE hook enforcement | ❌ (Kiro only) |
| Agent shortcut triggers | ❌ (Kiro only) |
| Automatic compliance logging | ⚠️ Manual |
| Depth adaptation | ✅ |
| Session continuity | ✅ Cold resume |

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
