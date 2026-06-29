# AI-* Family — Complete Installation Guide for Claude

**Applies to:** Claude Code (CLI agent) — the recommended Claude platform for AIFLC packages.

> **Why Claude Code specifically?** The AI-* Family packages need workspace file access to function fully (reading rule-detail files on demand, writing deliverables, persisting state between sessions). Claude Code is the only Claude product that provides this. See the [claude.ai section](#claudeai-web--projects--limited) at the end for the web-based alternative and its limitations.

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
- [AI-GCE Governance on Claude Code](#ai-gce-governance-on-claude-code)
- [Session Continuity](#session-continuity)
- [claude.ai (Web / Projects) — Limited](#claudeai-web--projects--limited)
- [Coexistence with Other Rules](#coexistence-with-other-rules)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Claude Code** | Installed and authenticated ([claude.ai/download](https://claude.ai/download)) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

Each AI-* package installs **two things** into your workspace, both **family-scoped** to the AI-* PDLC Family (core files carry a `CLAUDE_PDLC_` filename prefix; rule-details live under a `.pdlc/` folder — so multiple AIFLC families can coexist in one workspace):

1. **Core workflow/engine file** — a Markdown file that Claude Code reads automatically at session start (placed at workspace root as `CLAUDE_PDLC_{PKG}.md` or in `.claude/rules/pdlc/`)
2. **Rule-details folder** — phase-specific instructions and templates that the core workflow loads on demand during execution (placed under `.pdlc/`)

```
your-workspace/
├── CLAUDE_PDLC_AI_PILC.md         ← Claude reads this automatically (always-loaded steering)
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

Claude Code reads all `CLAUDE*.md` files at workspace root on every session start. This is how the packages inject their expertise into Claude's context without you needing to paste anything.

> **The Kiro-style split:** core files load as always-on steering (`CLAUDE_PDLC_*.md`); rule-details are read on demand (`.pdlc/`); and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root.

---

## Method 1: Automated Installer (Recommended)

The interactive installer handles all file placement automatically.

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive (asks platform, packages, target)
.\installer\install.ps1

# Option B: One-liner for Claude Code with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform claude-code -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform claude-code -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Claude Code
./installer/install.sh --target <your-project-path> --platform claude-code --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform claude-code --bundle full
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
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform claude-code -Bundle full -DryRun
```

This shows exactly what files would be copied and where, without modifying anything.

---

## Method 2: Manual Installation

If you prefer to install manually or need to understand what goes where.

### Single Package Example (AI-PILC)

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Copy the core workflow (Claude reads CLAUDE_*.md files automatically), family-scoped filename
Copy-Item "$Source\ai-pilc\ai-pilc-rules\core-workflow.md" "$Target\CLAUDE_PDLC_AI_PILC.md"

# Copy the rule-details folder (family-scoped under .pdlc/)
New-Item -ItemType Directory -Force -Path "$Target\.pdlc\ai-pilc-rule-details"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details\*" "$Target\.pdlc\ai-pilc-rule-details\"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Copy the core workflow (family-scoped filename)
cp "$SOURCE/ai-pilc/ai-pilc-rules/core-workflow.md" "$TARGET/CLAUDE_PDLC_AI_PILC.md"

# Copy the rule-details folder (family-scoped under .pdlc/)
mkdir -p "$TARGET/.pdlc/ai-pilc-rule-details"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details/"* "$TARGET/.pdlc/ai-pilc-rule-details/"
```

### File Naming Convention (Claude Code)

The installer uses this naming pattern per package:

| Package | Core File (always loaded) | Details Folder (on-demand) |
|---------|--------------------------|---------------------------|
| AI-ILC | `CLAUDE_PDLC_AI_ILC.md` | `.pdlc/ai-ilc-rule-details/` |
| AI-PILC | `CLAUDE_PDLC_AI_PILC.md` | `.pdlc/ai-pilc-rule-details/` |
| AI-ADLC | `CLAUDE_PDLC_AI_ADLC.md` | `.pdlc/ai-adlc-rule-details/` |
| AI-UXD | `CLAUDE_PDLC_AI_UXD.md` | `.pdlc/ai-uxd-rule-details/` |
| AI-POLC | `CLAUDE_PDLC_AI_POLC.md` | `.pdlc/ai-polc-rule-details/` |
| AI-DWG | `CLAUDE_PDLC_AI_DWG.md` | `.pdlc/ai-dwg-rule-details/` |
| AI-GCE | `CLAUDE_PDLC_AI_GCE.md` | `.pdlc/ai-gce-rule-details/` |
| AI-TGE | `CLAUDE_PDLC_AI_TGE.md` | `.pdlc/ai-tge-rule-details/` |
| AI-PPM | `CLAUDE_PDLC_AI_PPM.md` | `.pdlc/ai-ppm-rule-details/` |
| AI-FLO | `CLAUDE_PDLC_AI_FLO.md` | `.pdlc/ai-flo-rule-details/` |

> **Why `CLAUDE_PDLC_AI_PILC.md` instead of `CLAUDE.md`?** Claude Code reads ALL files matching `CLAUDE*.md` at workspace root. The `CLAUDE_PDLC_` prefix family-scopes each file to the AI-* PDLC Family, so multiple packages (and multiple AIFLC families) coexist — each gets its own always-loaded file without conflicts.

### Alternative: Using `.claude/rules/` Directory

Claude Code also supports a `.claude/rules/` directory where each rule file is automatically loaded. Family-scope it under a `pdlc/` subfolder for a cleaner multi-package install:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Create the family-scoped rules directory
New-Item -ItemType Directory -Force -Path "$Target\.claude\rules\pdlc"

# Copy each package's core file into .claude/rules/pdlc/
Copy-Item "$Source\ai-pilc\ai-pilc-rules\core-workflow.md" "$Target\.claude\rules\pdlc\ai-pilc.md"
Copy-Item "$Source\ai-adlc\ai-adlc-rules\core-workflow.md" "$Target\.claude\rules\pdlc\ai-adlc.md"
Copy-Item "$Source\ai-dwg\ai-dwg-rules\core-generator.md" "$Target\.claude\rules\pdlc\ai-dwg.md"

# Copy rule-details folders (family-scoped under .pdlc/)
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.pdlc\ai-pilc-rule-details"
Copy-Item -Recurse "$Source\ai-adlc\ai-adlc-rule-details" "$Target\.pdlc\ai-adlc-rule-details"
Copy-Item -Recurse "$Source\ai-dwg\ai-dwg-rule-details" "$Target\.pdlc\ai-dwg-rule-details"
```

Both approaches work. The `CLAUDE_PDLC_*.md` approach (what the installer uses) is simpler; the `.claude/rules/pdlc/` approach is more conventional for Claude Code users.

---

## Multi-Package Installation

### Installing All 10 Packages (Full Chain)

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform claude-code -Bundle full
```

Or manually:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

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
    $upperName = $pkg.Name.ToUpper().Replace('-','_')
    $coreSource = Join-Path $Source "$($pkg.Name)\$($pkg.Rules)\$($pkg.Core)"
    $coreDest = Join-Path $Target "CLAUDE_PDLC_$upperName.md"
    $detailsSource = Join-Path $Source "$($pkg.Name)\$($pkg.Details)"
    $detailsDest = Join-Path $Target ".pdlc\$($pkg.Details)"

    if (Test-Path $coreSource) {
        Copy-Item $coreSource $coreDest -Force
        if (Test-Path $detailsSource) {
            Copy-Item -Recurse $detailsSource $detailsDest -Force
        }
        Write-Host "Installed $($pkg.Name)" -ForegroundColor Green
    } else {
        Write-Host "Skipped $($pkg.Name) - source not found" -ForegroundColor Yellow
    }
}
```

### Context Window Consideration

All `CLAUDE_*.md` files load at session start. With 10 packages installed, that's ~10 core workflow files in context. Each is designed to be concise (the heavy detail is in the rule-details folders, loaded on demand), but be aware:

- **Recommended:** Install only the packages you'll use in a given project. Most projects need 3–5 packages, not all 10.
- **If installing all 10:** Context usage is still manageable because core files are orchestration logic (1–3 KB each), not full instruction sets.
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
├── CLAUDE_PDLC_AI_ILC.md            ← Always loaded: Idea evaluation workflow
├── CLAUDE_PDLC_AI_PILC.md           ← Always loaded: Project initiation workflow
├── CLAUDE_PDLC_AI_PPM.md            ← Always loaded: Portfolio management engine
├── CLAUDE_PDLC_AI_FLO.md            ← Always loaded: Flow router engine
├── CLAUDE_PDLC_AI_ADLC.md           ← Always loaded: Architecture design workflow
├── CLAUDE_PDLC_AI_UXD.md            ← Always loaded: UX design workflow
├── CLAUDE_PDLC_AI_POLC.md           ← Always loaded: Product ownership workflow
├── CLAUDE_PDLC_AI_DWG.md            ← Always loaded: Workspace generator
├── CLAUDE_PDLC_AI_GCE.md            ← Always loaded: Governance engine
├── CLAUDE_PDLC_AI_TGE.md            ← Always loaded: Test governance engine
├── .pdlc/                           ← AI-* PDLC Family rule-details (on-demand)
│   ├── ai-ilc-rule-details/            ← idea lifecycle details
│   ├── ai-pilc-rule-details/           ← project initiation details
│   │   ├── common/
│   │   ├── inception/
│   │   ├── assessment/
│   │   ├── justification/
│   │   ├── authorization/
│   │   ├── planning/
│   │   ├── mobilization/
│   │   └── templates/
│   ├── ai-adlc-rule-details/           ← architecture design details
│   ├── ai-uxd-rule-details/            ← UX design details
│   ├── ai-polc-rule-details/           ← product ownership details
│   ├── ai-ppm-rule-details/            ← portfolio management details
│   ├── ai-flo-rule-details/            ← flow routing details
│   ├── ai-dwg-rule-details/            ← workspace generation details
│   ├── ai-gce-rule-details/            ← governance engine details
│   └── ai-tge-rule-details/            ← test governance details
├── pdlc-ws/                         ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   ├── .ai-family-manifest.json     ← Installer tracking (for uninstall)
│   └── tools/                       ← Family tools (visual tools / extensions)
│       └── extensions/
│           ├── AIFLC-PDLC-Dashboard/ ← HTML dashboard + .vsix (reads ../../data/ via AI-DFE)
│           └── AIFLC-CommandBoard/   ← Trigger palette (HTML + .vsix)
└── (your project files)
```

> **Note:** The `.pdlc/` rule-details folder is dot-prefixed (hidden) and won't clutter your project view in most file explorers.

---

## Verification

After installation, verify everything is working:

### Step 1: Confirm files are in place

```powershell
# Windows
Get-ChildItem "<your-project-path>\CLAUDE_PDLC_*.md"
Get-ChildItem "<your-project-path>\.pdlc\ai-*-rule-details" -Directory
```

```bash
# macOS/Linux
ls <your-project-path>/CLAUDE_PDLC_*.md
ls -d <your-project-path>/.pdlc/ai-*-rule-details/
```

### Step 2: Start Claude Code in your workspace

```bash
# Navigate to your project
cd <your-project-path>

# Start Claude Code
claude
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

**Expected:** Claude should respond with the package's welcome message and begin the structured workflow, asking about depth level and presenting the first stage.

### Step 4: Verify on-demand loading

During a workflow, when Claude transitions to a new phase, it should read the corresponding rule-details file automatically. You'll see file-read tool calls in Claude Code's output referencing paths like `.pdlc/ai-pilc-rule-details/inception/stage-01-...`.

If Claude says it can't find rule details, check the folder paths match what the core workflow expects (see [Troubleshooting](#troubleshooting)).

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell Claude which package to use with the activation phrase
2. **Choose depth:** The package asks if you want Minimal, Standard, or Comprehensive output
3. **Work through stages:** Each package has defined stages. Claude guides you through them sequentially
4. **Approve at gates:** At the end of each stage, Claude presents output and waits for your approval before proceeding
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

Claude will respond with the AI-PILC welcome, ask about depth, then walk you through 6 phases / 16 stages:
1. **Inception** — Source analysis, project definition, stakeholder identification
2. **Assessment** — Feasibility, risk analysis, resource assessment
3. **Justification** — Business case development
4. **Authorization** — Governance approval
5. **Planning** — Detailed planning across multiple dimensions
6. **Mobilization** — Team formation, kickoff

Each stage produces a deliverable file in your workspace.

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

### Packages That Run in Parallel

In the project layer, three packages can run simultaneously:
- **AI-ADLC** (architecture)
- **AI-UXD** (UX design)
- **AI-POLC** (product backlog)

All three accept PIP as input and produce independent outputs that AI-DWG combines.

---

## AI-GCE Governance on Claude Code

AI-GCE (Governance & Compliance Engine) is the one package with reduced capability on Claude Code vs. Kiro:

### What Works (100%)

- Rule generation (`.governance/rules/`) — full mode 1/2/3/4
- Compliance documentation
- Brownfield baseline scanning
- Hook and agent file generation (structurally valid)

### What Doesn't Work (Kiro-only features)

| Feature | Why | Workaround |
|---------|-----|------------|
| Hook auto-execution | No event bus in Claude Code | Append critical rules to CLAUDE.md |
| Agent shortcut triggers | No `.kiro/agents/` runtime | Paste agent prompts manually |
| Automatic compliance logging | Triggered by hooks | Ask Claude to log manually |
| Re-derivation auto-trigger | Requires file-edit events | Say "re-derive governance" manually |

### Best Practice: Maximizing Governance Value

After AI-GCE generates your governance layer, add this section to your root `CLAUDE.md` (create one if it doesn't exist):

```markdown
## Governance Rules (Always Enforce)

The following rules from `.governance/rules/` apply to ALL work in this workspace.
Check compliance on every file you create or modify.

- See: .governance/rules/security-rules.md (CRITICAL)
- See: .governance/rules/architecture-rules.md
- See: .governance/rules/naming-conventions.md
- See: .governance/COMPLIANCE_README.md for full rule index
```

Then periodically ask Claude: "Run a compliance check against `.governance/rules/` on recent changes."

This gives you ~70% of Kiro's enforcement value through advisory compliance.

---

## Session Continuity

Each workflow package maintains a **state file** (e.g., `pilc-state.md`) that records:
- Current phase and stage
- Completed stages
- Pending decisions
- Selected depth level
- Key outputs produced

**This means you can close Claude Code and resume later.** When you start a new session and say "Continue AI-PILC", Claude reads the state file and picks up exactly where you left off.

> **Important:** Don't delete state files unless you want to restart a workflow from scratch.

---

## claude.ai (Web / Projects) — Limited

If you only have access to claude.ai (the web chat), here's what works and what doesn't:

### Setup via Claude Projects

1. Go to [claude.ai](https://claude.ai) → Create a new **Project**
2. Upload `core-workflow.md` (from any package) as **Project Knowledge**
3. Upload the contents of the matching `*-rule-details/` folder as additional knowledge files
4. Set custom instructions: "Follow core-workflow.md as your primary orchestration"

### Limitations

| Feature | Status | Notes |
|---------|--------|-------|
| Core workflow logic | ✅ Works | If uploaded as project knowledge |
| Depth adaptation | ✅ Works | — |
| On-demand file loading | ❌ No | Must pre-upload all detail files |
| Template output | ⚠️ Chat only | Cannot write files to disk |
| State persistence | ❌ No | Cannot resume across sessions |
| Chain detection | ❌ No | No filesystem |
| AI-DWG workspace generation | ❌ No | Needs to create 30+ files |
| AI-GCE governance | ❌ No | Needs filesystem |
| Multi-package coexistence | ⚠️ Awkward | One project per package works best |

### When to Use claude.ai

- Quick exploration of a single workflow (AI-PILC or AI-ILC) in conversation mode
- Getting professional advice without needing file output
- Trying out a package before committing to Claude Code installation

### When to Use Claude Code Instead

- Any real project work (you need the file outputs)
- Multi-package workflows (chain handoffs require state files)
- AI-DWG, AI-GCE, AI-TGE (require filesystem)
- Any scenario where you want to resume across sessions

---

## Coexistence with Other Rules

AI-* package files coexist peacefully with your existing Claude configuration:

- **Existing `CLAUDE.md`**: Untouched. The installer creates `CLAUDE_PDLC_AI_*.md` files (different filenames).
- **Existing `.claude/rules/`**: Untouched. Installer uses root-level `CLAUDE_PDLC_*.md` by default.
- **Other project files**: Never modified. Only AI-* steering files are added.
- **Package isolation**: Each package activates ONLY when you invoke it by name. Dormant packages consume context but don't interfere with other work.

### If You Want a Single CLAUDE.md Instead

Some users prefer a single `CLAUDE.md`. You can concatenate:

```powershell
# Merge all package core files into one CLAUDE.md
$packages = Get-ChildItem "<your-project-path>\CLAUDE_PDLC_AI_*.md"
$header = "# AI-* PDLC Family Steering`n`nThis workspace uses AIFLC packages.`n`n---`n"
$header | Out-File "<your-project-path>\CLAUDE.md" -Encoding utf8

foreach ($pkg in $packages) {
    "`n`n---`n`n## $($pkg.BaseName)`n`n" | Add-Content "<your-project-path>\CLAUDE.md"
    Get-Content $pkg.FullName | Add-Content "<your-project-path>\CLAUDE.md"
}

# Then remove the individual files
Remove-Item "<your-project-path>\CLAUDE_PDLC_AI_*.md"
```

> **Trade-off:** A single file is cleaner but harder to update individual packages. The multi-file approach lets you update one package without touching others.

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
# Remove all CLAUDE_PDLC_AI_* files
Remove-Item "<your-project-path>\CLAUDE_PDLC_AI_*.md"

# Remove all rule-details folders
Get-ChildItem "<your-project-path>\.pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force

# Remove the manifest (lives under pdlc-ws/)
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue

# Remove installed family tools (extensions)
Remove-Item "<your-project-path>\pdlc-ws\tools\extensions" -Recurse -Force -ErrorAction SilentlyContinue

# Remove runtime outputs if you want a clean slate (this deletes all generated work — back up first)
# Remove-Item "<your-project-path>\pdlc-ws" -Recurse -Force -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Claude doesn't recognize the package | Core file not being read | Verify `CLAUDE_PDLC_AI_*.md` exists at workspace root. Claude Code reads all `CLAUDE*.md` files at root. |
| "Can't find rule-details" | Path mismatch | The core workflow checks `.pdlc/{pkg}-rule-details/`, `pdlc/{pkg}-rule-details/`, and `.kiro/pdlc/{pkg}-rule-details/`. Ensure one of these exists. |
| No welcome message | Wrong activation phrase | Use the exact format: "Using AI-PILC, ..." (uppercase package name) |
| State file not created | First interaction only | State is created after the first stage completes, not immediately |
| Chain detection not working | Upstream state file missing | Run packages in order. If AI-ADLC can't find PILC output, verify `pilc-state.md` exists |
| Context window getting large | Too many packages loaded | Remove packages you don't actively need. Or use `.claude/rules/` with path-scoped frontmatter |
| Claude Code not reading files | Working directory wrong | Ensure you launched `claude` from your project root (where the CLAUDE_*.md files are) |
| Installer "source not found" | Package folder missing | Verify `ai-{package}/` exists in your AIPDLC clone |

### Getting Help

If something doesn't work:
1. Run the installer with `-DryRun` to see expected file paths
2. Check that your AIPDLC clone contains the `ai-{package}/` folders
3. Verify Claude Code version is current (`claude --version`)

---

## Platform Capabilities Summary

| Feature | Claude Code | claude.ai (Projects) |
|---------|:-----------:|:--------------------:|
| Core workflow execution | ✅ Full | ✅ If uploaded |
| On-demand file loading | ✅ Automatic | ❌ Manual pre-upload |
| Deliverable file output | ✅ Writes to disk | ⚠️ Chat output only |
| State persistence | ✅ Across sessions | ❌ Single session |
| Chain marker detection | ✅ Automatic | ❌ Not possible |
| Multi-package install | ✅ All 10 | ⚠️ One per project |
| AI-DWG workspace gen | ✅ Full (30+ files) | ❌ Not possible |
| AI-GCE rule generation | ✅ Full | ❌ Not possible |
| AI-GCE hook enforcement | ❌ (Kiro only) | ❌ |
| Depth adaptation | ✅ | ✅ |
| Session continuity | ✅ Cold resume | ❌ |

**Bottom line:** Use **Claude Code** for real project work. Use **claude.ai** only for quick exploration or when Claude Code isn't available.

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
