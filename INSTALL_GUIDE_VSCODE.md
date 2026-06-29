# AI-* Family — Complete Installation Guide for VS Code (Agent Framework)

**Applies to:** VS Code's built-in AI Agent framework — works with any model provider (Copilot, Claude, Gemini, OpenAI, or custom via API key).

> **What is this?** Since VS Code 1.102+ (2025), the editor has a unified AI customization system that works with multiple AI providers simultaneously. You can use GitHub Copilot, Claude (via Anthropic API), or any other model — the customization layer is the same. This guide targets that unified system using `AGENTS.md`, `.github/instructions/`, and `.github/copilot-instructions.md`.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [How It Works](#how-it-works)
- [VS Code Instruction System Overview](#vs-code-instruction-system-overview)
- [Method 1: Automated Installer (Recommended)](#method-1-automated-installer-recommended)
- [Method 2: Manual Installation](#method-2-manual-installation)
- [Multi-Package Installation](#multi-package-installation)
- [Package Reference](#package-reference)
- [Resulting Workspace Structure](#resulting-workspace-structure)
- [Verification](#verification)
- [Using the Packages](#using-the-packages)
- [Chain Handoffs Between Packages](#chain-handoffs-between-packages)
- [AI-GCE Governance on VS Code](#ai-gce-governance-on-vs-code)
- [Session Continuity](#session-continuity)
- [Advanced: Using .instructions.md Files](#advanced-using-instructionsmd-files)
- [Coexistence with Other Customizations](#coexistence-with-other-customizations)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **VS Code 1.102+** | With at least one AI provider configured (Copilot, Claude, etc.) |
| **An AI provider** | GitHub Copilot subscription, Anthropic API key, OpenAI key, or other |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

Each AI-* package installs **two things** into your workspace, both **family-scoped** to the AI-* PDLC Family (per-package instruction files carry a `pdlc-` filename prefix; rule-details live under a `.pdlc/` folder — so multiple AIFLC families can coexist in one workspace):

1. **Core workflow/engine file** — placed as an always-on instruction that VS Code's agent reads automatically
2. **Rule-details folder** — phase-specific instructions and templates loaded on demand during execution (placed under `.pdlc/`)

VS Code's agent framework supports multiple instruction file formats. The AI-* packages use the most universal approach:

```
your-workspace/
├── AGENTS.md                              ← Always loaded (any AI agent in VS Code)
├── .github/
│   ├── copilot-instructions.md            ← Always loaded (Copilot-specific, also read by others)
│   └── instructions/
│       ├── pdlc-ai-pilc.instructions.md   ← Per-package instruction files (family-scoped)
│       ├── pdlc-ai-adlc.instructions.md
│       └── ...
├── .pdlc/                                 ← AI-* PDLC Family rule-details (on-demand)
│   └── ai-pilc-rule-details/
│       ├── common/
│       ├── inception/
│       └── ...
├── pdlc-ws/                               ← All runtime outputs land here (never workspace root)
└── (your project files)
```

> **The Kiro-style split:** core instructions load always-on; rule-details are read on demand (`.pdlc/`); and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root.

---

## VS Code Instruction System Overview

VS Code now supports **multiple instruction formats** that all feed into the same AI context. Understanding these helps you choose the right installation approach:

| Format | File | Scope | Best For |
|--------|------|-------|----------|
| **Always-on (Copilot)** | `.github/copilot-instructions.md` | All requests | Single package or merged multi-package |
| **Always-on (Universal)** | `AGENTS.md` | All AI agents | Cross-agent compatibility (Copilot + Claude + others) |
| **Always-on (Claude)** | `CLAUDE.md` | Claude-based agents | If primary agent is Claude |
| **File-scoped** | `.github/instructions/*.instructions.md` | Matches `applyTo` pattern | Per-package isolation with glob control |
| **Custom agents** | `.github/agents/*.agent.md` | On-demand persona | Each package as a named agent |

### Recommended Approach for AI-* Packages

**Option A — `AGENTS.md` (simplest, broadest compatibility):**
A single merged file that any VS Code AI agent reads. Works with Copilot, Claude, and third-party models.

**Option B — `.github/instructions/` (cleanest multi-package):**
Each package as a separate `.instructions.md` file with `applyTo: "**"` (always active). Modular, easy to update individually.

**Option C — `.github/copilot-instructions.md` (Copilot-only):**
Same as the existing Copilot guide. Works if you exclusively use GitHub Copilot.

This guide covers **Options A and B** (the universal approaches).

---

## Method 1: Automated Installer (Recommended)

The interactive installer supports VS Code via the `copilot` platform flag. For the universal `AGENTS.md` approach, use manual installation (Method 2) or the instructions below.

### Using the Installer (Copilot mode)

```powershell
cd "<path-to-AIPDLC>"
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform copilot -Packages "ai-pilc,ai-adlc,ai-dwg"
```

> **Note:** The installer's `copilot` mode creates `.github/copilot-instructions.md`. For the `AGENTS.md` or `.instructions.md` approach, use Method 2 below.

### macOS / Linux

```bash
cd <path-to-AIPDLC>
./installer/install.sh --target <your-project-path> --platform copilot --packages ai-pilc,ai-adlc,ai-dwg
```

---

## Method 2: Manual Installation

### Option A: Using AGENTS.md (Universal — Any AI Agent)

This creates a single `AGENTS.md` file that VS Code loads for ALL AI agents (Copilot, Claude, etc.):

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Create AGENTS.md with package orchestration
$header = @"
# AI-* Family — Workspace Instructions

This workspace uses AIFLC injectable workflow packages.
Activate a package by saying "Using AI-{PKG}, ..." (e.g., "Using AI-PILC, initiate a project").

Each package loads detail files from its `.ai-{pkg}-rule-details/` folder on demand.
Only activate one package at a time.

---

"@
$header | Out-File "$Target\AGENTS.md" -Encoding utf8

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
        "`n---`n`n## PDLC / $($pkg.Name.ToUpper())`n`n" | Add-Content "$Target\AGENTS.md"
        Get-Content $coreSource | Add-Content "$Target\AGENTS.md"

        if (Test-Path $detailsSource) {
            if (Test-Path $detailsDest) { Remove-Item -Recurse -Force $detailsDest }
            Copy-Item -Recurse $detailsSource $detailsDest
        }
    }
}
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Create AGENTS.md header
cat > "$TARGET/AGENTS.md" << 'EOF'
# AI-* Family — Workspace Instructions

This workspace uses AIFLC injectable workflow packages.
Activate a package by saying "Using AI-{PKG}, ..." (e.g., "Using AI-PILC, initiate a project").

Each package loads detail files from its `.ai-{pkg}-rule-details/` folder on demand.
Only activate one package at a time.

---
EOF

# Append packages (example: ai-pilc + ai-adlc + ai-dwg)
for pkg in ai-pilc ai-adlc ai-dwg; do
    core_file="core-workflow.md"
    [ "$pkg" = "ai-dwg" ] && core_file="core-generator.md"
    
    echo -e "\n---\n\n## PDLC / ${pkg^^}\n" >> "$TARGET/AGENTS.md"
    cat "$SOURCE/$pkg/${pkg}-rules/$core_file" >> "$TARGET/AGENTS.md"
    
    mkdir -p "$TARGET/.pdlc/${pkg}-rule-details"
    cp -R "$SOURCE/$pkg/${pkg}-rule-details/"* "$TARGET/.pdlc/${pkg}-rule-details/"
done
```

### Option B: Using .instructions.md Files (Modular — Per Package)

This creates individual instruction files per package — cleaner for large installs:

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Create instructions directory
New-Item -ItemType Directory -Force -Path "$Target\.github\instructions" | Out-Null

$packages = @(
    @{ Name = "ai-ilc";  Core = "core-workflow.md";  Rules = "ai-ilc-rules";  Details = "ai-ilc-rule-details";  Desc = "AI-ILC: Idea evaluation lifecycle" }
    @{ Name = "ai-pilc"; Core = "core-workflow.md";  Rules = "ai-pilc-rules"; Details = "ai-pilc-rule-details"; Desc = "AI-PILC: Project initiation lifecycle" }
    @{ Name = "ai-ppm";  Core = "core-engine.md";    Rules = "ai-ppm-rules";  Details = "ai-ppm-rule-details";  Desc = "AI-PPM: Portfolio management engine" }
    @{ Name = "ai-flo";  Core = "core-engine.md";    Rules = "ai-flo-rules";  Details = "ai-flo-rule-details";  Desc = "AI-FLO: Package flow router" }
    @{ Name = "ai-adlc"; Core = "core-workflow.md";  Rules = "ai-adlc-rules"; Details = "ai-adlc-rule-details"; Desc = "AI-ADLC: Architecture design lifecycle" }
    @{ Name = "ai-uxd";  Core = "core-workflow.md";  Rules = "ai-uxd-rules";  Details = "ai-uxd-rule-details";  Desc = "AI-UXD: UX design lifecycle" }
    @{ Name = "ai-polc"; Core = "core-workflow.md";  Rules = "ai-polc-rules"; Details = "ai-polc-rule-details"; Desc = "AI-POLC: Product ownership lifecycle" }
    @{ Name = "ai-dwg";  Core = "core-generator.md"; Rules = "ai-dwg-rules";  Details = "ai-dwg-rule-details";  Desc = "AI-DWG: Workspace generator" }
    @{ Name = "ai-gce";  Core = "core-generator.md"; Rules = "ai-gce-rules";  Details = "ai-gce-rule-details";  Desc = "AI-GCE: Governance and compliance engine" }
    @{ Name = "ai-tge";  Core = "core-engine.md";    Rules = "ai-tge-rules";  Details = "ai-tge-rule-details";  Desc = "AI-TGE: Test governance engine" }
)

foreach ($pkg in $packages) {
    $coreSource = Join-Path $Source "$($pkg.Name)\$($pkg.Rules)\$($pkg.Core)"
    $instrDest = Join-Path $Target ".github\instructions\pdlc-$($pkg.Name).instructions.md"
    $detailsSource = Join-Path $Source "$($pkg.Name)\$($pkg.Details)"
    $detailsDest = Join-Path $Target ".pdlc\$($pkg.Details)"

    if (Test-Path $coreSource) {
        # Create .instructions.md with YAML frontmatter
        $frontmatter = "---`nname: '$($pkg.Desc)'`ndescription: 'AIFLC workflow package — activate with: Using $($pkg.Name.ToUpper()), ...'`napplyTo: '**'`n---`n`n"
        $frontmatter | Out-File -FilePath $instrDest -Encoding utf8 -NoNewline
        Get-Content $coreSource -Raw | Add-Content $instrDest -NoNewline

        # Copy rule-details
        if (Test-Path $detailsSource) {
            if (Test-Path $detailsDest) { Remove-Item -Recurse -Force $detailsDest }
            Copy-Item -Recurse $detailsSource $detailsDest
        }
        Write-Host "Installed $($pkg.Name)" -ForegroundColor Green
    }
}
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

mkdir -p "$TARGET/.github/instructions"

declare -A CORES=(
    ["ai-ilc"]="core-workflow.md"
    ["ai-pilc"]="core-workflow.md"
    ["ai-ppm"]="core-engine.md"
    ["ai-flo"]="core-engine.md"
    ["ai-adlc"]="core-workflow.md"
    ["ai-uxd"]="core-workflow.md"
    ["ai-polc"]="core-workflow.md"
    ["ai-dwg"]="core-generator.md"
    ["ai-gce"]="core-generator.md"
    ["ai-tge"]="core-engine.md"
)

for pkg in "${!CORES[@]}"; do
    core="${CORES[$pkg]}"
    instr_file="$TARGET/.github/instructions/pdlc-${pkg}.instructions.md"
    
    cat > "$instr_file" << EOF
---
name: '${pkg^^} workflow package'
description: 'AIFLC workflow — activate with: Using ${pkg^^}, ...'
applyTo: '**'
---

EOF
    cat "$SOURCE/$pkg/${pkg}-rules/$core" >> "$instr_file"
    
    mkdir -p "$TARGET/.pdlc/${pkg}-rule-details"
    cp -R "$SOURCE/$pkg/${pkg}-rule-details/"* "$TARGET/.pdlc/${pkg}-rule-details/"
    
    echo "Installed $pkg"
done
```

---

## Multi-Package Installation

### Context Window Considerations

VS Code loads ALL always-on instruction files at session start. With 10 packages:

- **Option A (AGENTS.md):** Single large file — may hit context limits with some models. Best for 3–5 packages.
- **Option B (.instructions.md):** Individual files all loaded — same total context but VS Code can manage them independently. Works better for large installs because VS Code shows which instructions were applied.

### Recommended: Install What You Need

| Scenario | Packages | Approach |
|----------|----------|----------|
| 1–3 packages | Any subset | Either option works well |
| 4–6 packages | Selective | Option B preferred (modular) |
| 7–10 packages | Full chain | Option B required (AGENTS.md gets too large) |

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

### Option A (AGENTS.md)

```
your-project/
├── AGENTS.md                                ← Single merged file, all AI agents read this
├── .pdlc/                                   ← AI-* PDLC Family rule-details (on-demand)
│   ├── ai-pilc-rule-details/
│   ├── ai-adlc-rule-details/
│   └── ai-dwg-rule-details/
├── pdlc-ws/                                 ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
└── (your project files)
```

### Option B (.instructions.md — Recommended for 4+ packages)

```
your-project/
├── .github/
│   └── instructions/
│       ├── pdlc-ai-ilc.instructions.md      ← Always loaded
│       ├── pdlc-ai-pilc.instructions.md     ← Always loaded
│       ├── pdlc-ai-ppm.instructions.md      ← Always loaded
│       ├── pdlc-ai-flo.instructions.md      ← Always loaded
│       ├── pdlc-ai-adlc.instructions.md     ← Always loaded
│       ├── pdlc-ai-uxd.instructions.md      ← Always loaded
│       ├── pdlc-ai-polc.instructions.md     ← Always loaded
│       ├── pdlc-ai-dwg.instructions.md      ← Always loaded
│       ├── pdlc-ai-gce.instructions.md      ← Always loaded
│       └── pdlc-ai-tge.instructions.md      ← Always loaded
├── .pdlc/                                   ← AI-* PDLC Family rule-details (on-demand)
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
├── pdlc-ws/                                 ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
└── (your project files)
```

---

## Verification

### Step 1: Check instruction loading

1. Open your workspace in VS Code
2. Open the Command Palette (`Ctrl+Shift+P`)
3. Run `Chat: Configure Instructions` or open the **Agent Customizations** editor
4. Confirm your AI-* instruction files appear in the list

### Step 2: Verify with diagnostics

1. Open any Chat view
2. Right-click → **Diagnostics**
3. Check that AI-* instructions appear in the loaded instructions list

### Step 3: Test activation

Start a chat and type:

```
Using AI-PILC, initiate a project from this requirement: [your requirement]
```

**Expected:** The AI responds with the package's welcome message and begins the structured workflow.

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell the AI which package to use with the activation phrase
2. **Choose depth:** Minimal, Standard, or Comprehensive
3. **Work through stages:** The AI guides you sequentially
4. **Approve at gates:** Output presented for approval before proceeding
5. **Get deliverables:** Each stage produces one professional deliverable (written to disk)

### Which AI Model Works Best?

| Model | Works | Notes |
|-------|:-----:|-------|
| Claude (Anthropic) | ✅ | Excellent instruction-following. Best results. |
| GPT-4o / GPT-4.1 | ✅ | Good instruction-following. Works well. |
| Copilot (GPT-based) | ✅ | Good. Use Chat view, not inline suggestions. |
| Gemini | ✅ | Works. May need more explicit prompting for gates. |
| Local models (Ollama, etc.) | ⚠️ | Depends on model size. 70B+ recommended. |

---

## Chain Handoffs Between Packages

Packages detect each other through **state marker files** (e.g., `pilc-state.md`). Run packages sequentially and they find each other's output automatically.

---

## AI-GCE Governance on VS Code

AI-GCE generates all governance files correctly, but auto-enforcement varies by feature:

| Feature | VS Code (Copilot/Claude) | Notes |
|---------|:------------------------:|-------|
| Rule generation | ✅ | `.governance/rules/` created normally |
| VS Code hooks | ✅ | VS Code 1.102+ supports `.github/hooks/` |
| Kiro-style hook execution | ❌ | Kiro's event bus is proprietary |
| Agent file generation | ✅ | `.github/agents/` works in VS Code |
| Compliance logging | ⚠️ Manual | Ask AI to log manually |

### Best Practice: Governance Instructions

After AI-GCE generates governance, create a governance instruction file:

```markdown
<!-- .github/instructions/governance.instructions.md -->
---
name: 'Governance enforcement'
description: 'Checks compliance against workspace governance rules'
applyTo: '**'
---

## Governance Rules (Always Enforce)

Before completing any file modification, verify against:
- .governance/rules/security-rules.md (CRITICAL)
- .governance/rules/architecture-rules.md
- .governance/rules/naming-conventions.md

See .governance/COMPLIANCE_README.md for the full rule index.
```

### VS Code Hooks (New in 1.102+)

VS Code now supports hooks (`.github/hooks/`) that run at specific points in the agent loop. AI-GCE can be adapted to generate VS Code-format hooks for basic enforcement. This is not yet automatic but is on the roadmap (Idea 011: Platform-Portable Governance Adapters).

---

## Session Continuity

State files persist between sessions. Say "Continue AI-PILC" to resume where you left off.

---

## Advanced: Using .instructions.md Files

### File-Scoped Instructions for Package Details

You can create instructions that only activate when working in specific folders:

```markdown
<!-- .github/instructions/pdlc-ai-pilc-details.instructions.md -->
---
name: 'AI-PILC detail loading'
description: 'Loads AI-PILC phase details when working in PILC output folders'
applyTo: '**/pdlc-ws/**'
---

When working in `pdlc-ws/`, reference the AI-PILC templates in `.pdlc/ai-pilc-rule-details/templates/` for consistent formatting.
```

### User-Level Instructions (Cross-Project)

Store shared instructions in `~/.copilot/instructions/` to have them available in all workspaces:

```powershell
# Copy the AI-* Family activation guide to user-level
New-Item -ItemType Directory -Force -Path "$HOME\.copilot\instructions"
# Create a brief activator that tells the AI how to handle "Using AI-*" prompts
```

---

## Coexistence with Other Customizations

AI-* packages coexist with all other VS Code AI customizations:

- **Existing `copilot-instructions.md`**: Untouched (unless you use the Copilot installer mode).
- **Existing `AGENTS.md`**: If using Option A, packages are appended. If using Option B, untouched.
- **Existing `.instructions.md` files**: Untouched. AI-* packages add their own files.
- **Custom agents**: AI-* packages don't create `.agent.md` files by default (but you can convert them — see below).
- **Other project files**: Never modified.

### Converting Packages to Custom Agents (Advanced)

VS Code supports `.github/agents/*.agent.md` files that define specialized personas. You could wrap each AI-* package as a custom agent:

```markdown
<!-- .github/agents/pdlc-ai-pilc.agent.md -->
---
name: AI-PILC
description: Project Initiation Life Cycle — guides you from raw requirement to a professional Project Initiation Package
instructions:
  - .github/instructions/pdlc-ai-pilc.instructions.md
tools:
  - read_file
  - write_file
  - list_directory
---

You are the AI-PILC agent. When invoked, follow the core workflow in your instructions to guide the user through project initiation.
```

This lets users invoke `@ai-pilc` in chat directly. This is an advanced configuration not yet handled by the installer.

---

## Uninstalling

### Option A (AGENTS.md)

```powershell
Remove-Item "<your-project-path>\AGENTS.md"
Get-ChildItem "<your-project-path>\.pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
```

### Option B (.instructions.md)

```powershell
Remove-Item "<your-project-path>\.github\instructions\pdlc-ai-*.instructions.md"
Get-ChildItem "<your-project-path>\.pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
```

### Via Installer (Copilot mode)

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Instructions not loading | Setting disabled | Ensure `chat.includeApplyingInstructions` is enabled in settings |
| AGENTS.md not recognized | Feature disabled | Enable `chat.useAgentsMdFile` in VS Code settings |
| .instructions.md not applied | Missing `applyTo` | Add `applyTo: '**'` to frontmatter for always-on behavior |
| "Can't find rule-details" | Path mismatch | Ensure `.pdlc/ai-{pkg}-rule-details/` exists at workspace root |
| Wrong model being used | Model selection | Check your model selection in Chat view dropdown |
| Instructions too long | Context overflow | Switch from AGENTS.md to individual .instructions.md files |
| Instructions applied but not followed | Model limitation | Try a stronger model (Claude or GPT-4o recommended) |
| Nested instructions not found | Monorepo setting | Enable `chat.useCustomizationsInParentRepositories` |

### Diagnostics

Right-click in Chat view → **Diagnostics** to see:
- Which instruction files were loaded
- Which ones applied to the current request
- Any errors in instruction file parsing

---

## Platform Capabilities Summary

| Feature | VS Code (Agent Framework) |
|---------|:-------------------------:|
| Core workflow execution | ✅ |
| On-demand file loading | ✅ |
| Deliverable file output | ✅ |
| State persistence | ✅ |
| Chain marker detection | ✅ |
| Multi-package install | ✅ All 10 (via .instructions.md) |
| AI-DWG workspace gen | ✅ |
| AI-GCE rule generation | ✅ |
| AI-GCE hook enforcement | ⚠️ Partial (VS Code hooks exist, different format) |
| VS Code native hooks | ✅ (1.102+, `.github/hooks/`) |
| Custom agent wrapping | ✅ (`.github/agents/`) |
| Multi-model support | ✅ (Any provider) |
| Depth adaptation | ✅ |
| Session continuity | ✅ Cold resume |

### Comparison: VS Code Agent Framework vs. Platform-Specific Guides

| If you use... | Use this guide | Or this platform guide |
|---------------|----------------|----------------------|
| VS Code + Copilot | This guide (Option B) | `INSTALL_GUIDE_COPILOT.md` |
| VS Code + Claude (API) | This guide (Option A or B) | `INSTALL_GUIDE_CLAUDE.md` (for Claude Code CLI) |
| VS Code + Cline extension | `INSTALL_GUIDE_CLINE.md` | — |
| VS Code + Any model via API | This guide | — |
| Kiro (VS Code-based) | `INSTALL_GUIDE_KIRO.md` | — |

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
