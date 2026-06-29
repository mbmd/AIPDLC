# AI-* Family — Complete Installation Guide for GitHub Copilot

**Applies to:** GitHub Copilot (VS Code / JetBrains) — partial support with workspace-level instructions.

> **⚠️ Partial Support:** GitHub Copilot supports workspace-level instructions via `.github/copilot-instructions.md`, but has limitations: only one instructions file is supported per workspace, and on-demand file reading behavior varies. Workflow packages work, but multi-package installs require merging into a single file.

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
- [AI-GCE Governance on Copilot](#ai-gce-governance-on-copilot)
- [Limitations and Workarounds](#limitations-and-workarounds)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **GitHub Copilot** | Active subscription + VS Code/JetBrains extension installed |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

Each AI-* package installs **two things** into your workspace, both **family-scoped** to the AI-* PDLC Family (per-package core files carry a `pdlc-` filename segment; rule-details live under a `.pdlc/` folder — so multiple AIFLC families can coexist in one workspace):

1. **Core workflow/engine file** — placed in `.github/` as a copilot instructions file
2. **Rule-details folder** — phase-specific instructions and templates loaded on demand (placed under `.pdlc/`)

```
your-workspace/
├── .github/
│   └── copilot-instructions-pdlc-ai-pilc.md    ← Copilot reads workspace instructions
├── .pdlc/
│   └── ai-pilc-rule-details/                    ← Loaded on-demand by the workflow
│       ├── common/
│       ├── inception/
│       ├── assessment/
│       ├── templates/
│       └── ...
├── pdlc-ws/                                      ← All runtime outputs land here (never workspace root)
└── (your project files)
```

> **Important:** GitHub Copilot only reads `.github/copilot-instructions.md` (singular). For multi-package installs, files must be merged into that one file (you cannot rename the file Copilot reads, so the family scope lives in the `pdlc-` per-package section headings and in the `.pdlc/` rule-details folder). The installer handles this. See [Multi-Package Installation](#multi-package-installation).

> **The Kiro-style split:** the core instructions load always-on; rule-details are read on demand (`.pdlc/`); and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root.

---

## Method 1: Automated Installer (Recommended)

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive
.\installer\install.ps1

# Option B: One-liner for Copilot with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform copilot -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform copilot -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Copilot
./installer/install.sh --target <your-project-path> --platform copilot --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform copilot --bundle full
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

### Single Package (Simple Case)

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Copy core workflow as copilot instructions
New-Item -ItemType Directory -Force -Path "$Target\.github"
Copy-Item "$Source\ai-pilc\ai-pilc-rules\core-workflow.md" "$Target\.github\copilot-instructions.md"

# Copy rule-details folder (family-scoped under .pdlc/)
New-Item -ItemType Directory -Force -Path "$Target\.pdlc\ai-pilc-rule-details"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details\*" "$Target\.pdlc\ai-pilc-rule-details\"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Copy core workflow as copilot instructions
mkdir -p "$TARGET/.github"
cp "$SOURCE/ai-pilc/ai-pilc-rules/core-workflow.md" "$TARGET/.github/copilot-instructions.md"

# Copy rule-details folder (family-scoped under .pdlc/)
mkdir -p "$TARGET/.pdlc/ai-pilc-rule-details"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details/"* "$TARGET/.pdlc/ai-pilc-rule-details/"
```

---

## Multi-Package Installation

### The Single-File Challenge

GitHub Copilot reads only `.github/copilot-instructions.md`. For multiple packages, you must **merge** all core workflows into that one file:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.github" | Out-Null

# Start the merged file
$header = @"
# AI-* Family — Workspace Instructions

This workspace uses AIFLC injectable workflow packages.
Activate a package by saying "Using AI-{PKG}, ..." (e.g., "Using AI-PILC, initiate a project").

---

"@
$header | Out-File "$Target\.github\copilot-instructions.md" -Encoding utf8

# Append each package's core workflow
$packages = @(
    @{ Name = "ai-pilc"; Core = "core-workflow.md";  Rules = "ai-pilc-rules"; Details = "ai-pilc-rule-details" }
    @{ Name = "ai-adlc"; Core = "core-workflow.md";  Rules = "ai-adlc-rules"; Details = "ai-adlc-rule-details" }
    @{ Name = "ai-dwg";  Core = "core-generator.md"; Rules = "ai-dwg-rules";  Details = "ai-dwg-rule-details" }
)

foreach ($pkg in $packages) {
    $coreSource = Join-Path $Source "$($pkg.Name)\$($pkg.Rules)\$($pkg.Core)"
    $detailsSource = Join-Path $Source "$($pkg.Name)\$($pkg.Details)"
    $detailsDest = Join-Path $Target ".pdlc\$($pkg.Details)"

    if (Test-Path $coreSource) {
        # Append separator + content (family-scoped section heading)
        "`n`n---`n`n## PDLC / $($pkg.Name.ToUpper())`n`n" | Add-Content "$Target\.github\copilot-instructions.md"
        Get-Content $coreSource | Add-Content "$Target\.github\copilot-instructions.md"

        # Copy rule-details
        if (Test-Path $detailsSource) {
            if (Test-Path $detailsDest) { Remove-Item -Recurse -Force $detailsDest }
            Copy-Item -Recurse $detailsSource $detailsDest
        }
        Write-Host "Installed $($pkg.Name)" -ForegroundColor Green
    }
}
```

### Context Window Warning

Merging all 10 packages into one `copilot-instructions.md` creates a large file. Copilot may truncate instructions that exceed its context limit.

**Recommendation:** Install 2–3 packages maximum on Copilot. For larger installs, use a different platform (Kiro, Claude Code, Cursor, or Cline).

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

### Recommended Packages for Copilot

Due to the single-file constraint and context limits, these combinations work best:

| Scenario | Packages | Why |
|----------|----------|-----|
| Quick start | AI-PILC + AI-ADLC | Core lifecycle without generator overhead |
| Architecture | AI-ADLC + AI-DWG | Design → generate |
| Governance | AI-GCE + AI-TGE | Compliance + test quality |
| Idea to project | AI-ILC + AI-PILC | Evaluation → initiation |

---

## Resulting Workspace Structure

After installation (example with 3 packages):

```
your-project/
├── .github/
│   └── copilot-instructions.md          ← Single merged file (all PDLC packages)
├── .pdlc/                               ← AI-* PDLC Family rule-details (on-demand)
│   ├── ai-pilc-rule-details/
│   ├── ai-adlc-rule-details/
│   └── ai-dwg-rule-details/
├── pdlc-ws/                             ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   └── .ai-family-manifest.json         ← Installer tracking
└── (your project files)
```

---

## Verification

1. Open your workspace in VS Code with GitHub Copilot active
2. Open Copilot Chat
3. Type: "Using AI-PILC, initiate a project"
4. **Expected:** Copilot responds with the workflow and begins guiding you

> **Note:** If Copilot doesn't reference the instructions, try `@workspace` prefix: "@workspace Using AI-PILC, initiate a project"

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell Copilot which package to use with the activation phrase
2. **Choose depth:** Minimal, Standard, or Comprehensive
3. **Work through stages:** Copilot guides you sequentially
4. **Approve at gates:** Output presented for approval before proceeding
5. **Get deliverables:** Each stage produces one deliverable

### Tips for Copilot

- Use `@workspace` prefix if Copilot doesn't pick up instructions automatically
- Reference rule-details files explicitly if Copilot doesn't read them: "Read `.pdlc/ai-pilc-rule-details/inception/stage-01-source-analysis.md` and execute it"
- Copilot Chat works better than inline suggestions for workflow execution

---

## Chain Handoffs Between Packages

Packages detect each other through **state marker files**. This works on Copilot if:
- You use Copilot Chat (not inline suggestions)
- Copilot has access to read workspace files

---

## AI-GCE Governance on Copilot

AI-GCE generates governance files, but enforcement is entirely advisory:

| Feature | Status |
|---------|--------|
| Rule generation | ✅ (files created) |
| Hook auto-execution | ❌ |
| Agent triggers | ❌ |
| Compliance logging | ❌ |

**Workaround:** After AI-GCE runs, append a governance reminder section to `copilot-instructions.md`:

```markdown
## Governance (Always Check)

Before completing any file, verify against:
- .governance/rules/security-rules.md
- .governance/rules/architecture-rules.md
```

---

## Limitations and Workarounds

| Limitation | Impact | Workaround |
|-----------|--------|------------|
| Single instructions file | Can't have per-package files | Merge into one (installer does this) |
| Context window limits | May truncate large merged files | Install 2–3 packages max |
| On-demand file reading inconsistent | May not auto-read rule-details | Reference files explicitly in prompts |
| No hook/agent execution | AI-GCE enforcement is advisory | Use CI/CD hooks instead |
| Workspace-level only | No per-folder scoping | All packages apply globally |

### When to Consider a Different Platform

If you need:
- More than 3 packages → Use Cursor, Claude Code, or Kiro
- AI-GCE enforcement → Use Kiro
- Reliable on-demand file loading → Use any other supported platform
- Full chain (all 10 packages) → Use Kiro, Claude Code, or Cursor

---

## Uninstalling

```powershell
# Via installer
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall

# Manual
Remove-Item "<your-project-path>\.github\copilot-instructions.md"
Get-ChildItem "<your-project-path>\.pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue
```

> **Warning:** If you had a pre-existing `copilot-instructions.md`, the installer backs it up as `copilot-instructions.md.bak`. Restore it after uninstalling.

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Copilot ignores instructions | File not in correct location | Must be exactly `.github/copilot-instructions.md` |
| "Can't find rule-details" | Copilot not reading workspace files | Reference files explicitly: "Read `.pdlc/ai-pilc-rule-details/...`" |
| Instructions seem truncated | File too large | Reduce to 2–3 packages |
| No structured workflow | Copilot treating as suggestions | Use Copilot Chat, not inline. Try `@workspace` prefix |
| State file not persisting | Copilot not writing files | Use Copilot Chat with "save this to file" instructions |

---

## Platform Capabilities Summary

| Feature | GitHub Copilot |
|---------|:--------------:|
| Core workflow execution | ✅ |
| On-demand file loading | ⚠️ Inconsistent |
| Deliverable file output | ✅ |
| State persistence | ✅ |
| Chain marker detection | ✅ |
| Multi-package install | ⚠️ 2–3 max (single file constraint) |
| AI-DWG workspace gen | ✅ |
| AI-GCE rule generation | ✅ |
| AI-GCE hook enforcement | ❌ (Kiro only) |
| Depth adaptation | ✅ |
| Session continuity | ✅ (if state file works) |

**GitHub Copilot is viable for 1–3 packages.** For larger installs or governance enforcement, use a platform with better multi-file rule support.

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
