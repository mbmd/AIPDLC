# AI-* PDLC Family — Installation Guide

**AIFLC · The AI-* PDLC Family** — Injectable Workflow Packages for AI-Assisted Software Delivery

This guide covers installation on all supported platforms. Pick your platform section below.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites (All Platforms)](#prerequisites-all-platforms)
- [How It Works](#how-it-works)
- [Preset Bundles](#preset-bundles)
- [Package Reference](#package-reference)
- [Platform-Specific Installation](#platform-specific-installation)
  - [Kiro](#kiro)
  - [Cursor](#cursor)
  - [Claude Code](#claude-code)
  - [Amazon Q Developer](#amazon-q-developer)
  - [Cline](#cline)
  - [OpenAI Codex](#openai-codex)
  - [GitHub Copilot](#github-copilot)
  - [VS Code Agent Framework](#vs-code-agent-framework)
- [Using the Packages](#using-the-packages)
- [Chain Handoffs Between Packages](#chain-handoffs-between-packages)
- [Session Continuity](#session-continuity)
- [Cross-Platform Capabilities Matrix](#cross-platform-capabilities-matrix)
- [Uninstalling](#uninstalling)

---

## Overview

The AI-* PDLC Family installs into any AI-capable IDE using a simple two-part model:

1. **One always-loaded orchestrator** — a compact router that sits in your platform's native auto-load slot. It detects which package you want and reads that package's core on demand.
2. **A uniform package home** (`.aiflc/pdlc/`) — every package's core AND rule-details live here, read on demand. Nothing auto-loads from this folder.

This keeps the context window free regardless of how many packages you install (all 11 can coexist).

---

## Prerequisites (All Platforms)

| Requirement | Details |
|-------------|---------|
| **Your IDE/agent** | Any supported platform (see list below) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone [AIPDLC](https://github.com/mbmd/AIPDLC) into a temporary `.aiflc-src/AIPDLC/` folder. Delete it after install so nothing but `.aiflc/pdlc/` and `pdlc-ws/` remains at your root. |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

```
your-workspace/
├── [platform auto-load slot]          ← The ONLY always-loaded file (orchestrator)
├── .aiflc/
│   └── pdlc/                          ← AI-* PDLC Family home (cores + rule-details + fabric)
│       ├── ai-pilc-rules/core-workflow.md    ← Read on demand
│       ├── ai-pilc-rule-details/             ← Read on demand by the core
│       └── ... one {pkg}-rules/ + {pkg}-rule-details/ per installed package
├── pdlc-ws/                           ← All runtime outputs land here
└── (your project files)
```

The orchestrator routes by intent: when you say "Using AI-PILC, ..." it reads `.aiflc/pdlc/ai-pilc-rules/core-workflow.md`, and the core reads its rule-details as each phase needs them.

---

## Preset Bundles

All platforms support the same preset bundles via the automated installer:

| Bundle | Flag | Packages | Best For |
|--------|------|----------|----------|
| **Full** | `-Bundle full` | AI-ILC + AI-PILC + AI-PPM + AI-FLO + AI-POLC + AI-UXD + AI-ADLC + AI-DWG + AI-GCE + AI-TGE + AI-DFE | New project, complete family |
| **Minimal** | `-Bundle minimal` | AI-PILC + AI-ADLC + AI-DWG | Quick start, architecture focus |
| **Architecture** | `-Bundle arch` | AI-ADLC + AI-DWG + AI-GCE | Architecture → workspace → governance |
| **Governance** | `-Bundle governance` | AI-GCE + AI-TGE | Existing project, add compliance |
| **Portfolio** | `-Bundle portfolio` | AI-ILC + AI-PILC + AI-PPM + AI-FLO | Multi-project management |

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
| 11 | **AI-DFE** | Gather, shape, and distribute structured data | "Using AI-DFE, gather data" |

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

## Platform-Specific Installation

### Per-Platform Orchestrator Slot

| Platform | Always-loaded orchestrator location | Support level |
|----------|-------------------------------------|:-------------:|
| **Kiro** | `.kiro/steering/session-orchestrator-pdlc.md` | Full (100%) |
| **Cursor** | `.cursor/rules/pdlc-session-orchestrator.mdc` | Full |
| **Claude Code** | `CLAUDE_PDLC_ORCHESTRATOR.md` (imported via root `CLAUDE.md`) | Full |
| **Amazon Q** | `.amazonq/rules/pdlc/session-orchestrator.md` | Full |
| **Cline** | `.clinerules/pdlc-session-orchestrator.md` | Full |
| **OpenAI Codex** | `AGENTS.md` (workspace root) | Full |
| **GitHub Copilot** | `.github/copilot-instructions-pdlc-orchestrator.md` | Partial |
| **VS Code Agent** | `AGENTS.md` or `.github/copilot-instructions.md` | Full |

On every platform, package cores live in the same uniform home: `.aiflc/pdlc/`

---

### Kiro

**The primary platform with full feature support** including hooks, agents, and auto-enforcement.

#### Automated Install

```powershell
# Windows — from the cloned AIPDLC root:
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform kiro -Bundle full
```

```bash
# macOS/Linux:
./installer/install.sh --target <your-project-path> --platform kiro --bundle full
```

#### Manual Install (single package example)

```powershell
$Source = "<path-to-AIPDLC>/pdlc-packages"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

New-Item -ItemType Directory -Force -Path "$Target\.kiro\steering"
Copy-Item "$Source\session-orchestrator.md" "$Target\.kiro\steering\session-orchestrator-pdlc.md"
```

#### Resulting Structure

```
your-project/
├── .kiro/
│   ├── steering/
│   │   └── session-orchestrator-pdlc.md   ← ONLY always-loaded file
│   └── agents/                            ← package agents (FHC__, FIA__, ...)
├── .aiflc/pdlc/                           ← all cores + rule-details (on demand)
├── pdlc-ws/                               ← all runtime outputs
└── (your project files)
```

#### AI-GCE on Kiro

All features work natively: hook auto-execution, agent shortcut triggers, automatic compliance logging, tier auto-progression, re-derivation auto-trigger. No workarounds needed.

#### Verification

1. Open workspace in Kiro → Steering Files panel → confirm orchestrator appears
2. New chat: "Using AI-PILC, initiate a project from this requirement: ..."
3. Expected: package welcome message + structured workflow begins

---

### Cursor

**Full workflow support** with `.cursor/rules/` integration.

#### Automated Install

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cursor -Bundle full
```

```bash
./installer/install.sh --target <your-project-path> --platform cursor --bundle full
```

#### Manual Install

```powershell
$Source = "<path-to-AIPDLC>/pdlc-packages"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

New-Item -ItemType Directory -Force -Path "$Target\.cursor\rules"
# The installer wraps the orchestrator with alwaysApply frontmatter:
$frontmatter = "---`ndescription: `"AI-* PDLC Family session orchestrator`"`nalwaysApply: true`n---`n`n"
$frontmatter | Out-File -FilePath "$Target\.cursor\rules\pdlc-session-orchestrator.mdc" -Encoding utf8 -NoNewline
Get-Content "$Source\session-orchestrator.md" -Raw | Add-Content "$Target\.cursor\rules\pdlc-session-orchestrator.mdc" -NoNewline
```

#### Resulting Structure

```
your-project/
├── .cursor/rules/
│   └── pdlc-session-orchestrator.mdc    ← ONLY always-loaded file (alwaysApply: true)
├── .aiflc/pdlc/                          ← all cores + rule-details (on demand)
├── pdlc-ws/                              ← all runtime outputs
└── (your project files)
```

#### AI-GCE on Cursor

Rule generation works fully. Hook auto-execution unavailable (Kiro-only). Workaround: create `.cursor/rules/governance-enforce.mdc` with `alwaysApply: true` referencing your governance rules.

---

### Claude Code

**Full workflow support** with `CLAUDE.md` + `@import` integration.

#### Automated Install

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform claude-code -Bundle full
```

```bash
./installer/install.sh --target <your-project-path> --platform claude-code --bundle full
```

#### Manual Install

```powershell
$Source = "<path-to-AIPDLC>/pdlc-packages"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

Copy-Item "$Source\session-orchestrator.claude.md" "$Target\CLAUDE_PDLC_ORCHESTRATOR.md"
if (-not (Test-Path "$Target\CLAUDE.md")) { New-Item -ItemType File -Path "$Target\CLAUDE.md" | Out-Null }
Add-Content "$Target\CLAUDE.md" "`n@CLAUDE_PDLC_ORCHESTRATOR.md`n"
```

#### Resulting Structure

```
your-project/
├── CLAUDE.md                            ← auto-loaded; imports @CLAUDE_PDLC_ORCHESTRATOR.md
├── CLAUDE_PDLC_ORCHESTRATOR.md          ← ONLY always-loaded family file
├── .claude/commands/pdlc/               ← generated slash commands (/pdlc:pilc, etc.)
├── .claude/skills/pdlc/SKILL.md         ← Claude skill registration
├── .aiflc/pdlc/                          ← all cores + rule-details (on demand)
├── pdlc-ws/                              ← all runtime outputs
└── (your project files)
```

#### AI-GCE on Claude Code

Rule generation works fully. Hook auto-execution unavailable. Workaround: append governance rules to root `CLAUDE.md`.

#### claude.ai (Web/Projects) — Limited

Upload `core-workflow.md` + rule-details as Project Knowledge. Limitations: no filesystem, no state persistence, no chain detection, no workspace generation. Use for quick exploration only.

---

### Amazon Q Developer

**Full workflow support** with `.amazonq/rules/` integration.

#### Automated Install

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform amazonq -Bundle full
```

```bash
./installer/install.sh --target <your-project-path> --platform amazonq --bundle full
```

#### Manual Install

```powershell
$Source = "<path-to-AIPDLC>/pdlc-packages"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

New-Item -ItemType Directory -Force -Path "$Target\.amazonq\rules\pdlc"
Copy-Item "$Source\session-orchestrator.md" "$Target\.amazonq\rules\pdlc\session-orchestrator.md"
```

#### Resulting Structure

```
your-project/
├── .amazonq/rules/pdlc/
│   └── session-orchestrator.md          ← ONLY always-loaded file
├── .aiflc/pdlc/                          ← all cores + rule-details (on demand)
├── pdlc-ws/                              ← all runtime outputs
└── (your project files)
```

#### AI-GCE on Amazon Q

Rule generation works fully. Hook auto-execution unavailable. Workaround: copy governance summary into `.amazonq/rules/governance-enforce.md`.

---

### Cline

**Full workflow support** with `.clinerules/` integration.

#### Automated Install

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cline -Bundle full
```

```bash
./installer/install.sh --target <your-project-path> --platform cline --bundle full
```

#### Manual Install

```powershell
$Source = "<path-to-AIPDLC>/pdlc-packages"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

New-Item -ItemType Directory -Force -Path "$Target\.clinerules"
Copy-Item "$Source\session-orchestrator.md" "$Target\.clinerules\pdlc-session-orchestrator.md"
```

#### Resulting Structure

```
your-project/
├── .clinerules/
│   └── pdlc-session-orchestrator.md     ← ONLY always-loaded file
├── .aiflc/pdlc/                          ← all cores + rule-details (on demand)
├── pdlc-ws/                              ← all runtime outputs
└── (your project files)
```

#### AI-GCE on Cline

Rule generation works fully. Hook auto-execution unavailable. Workaround: copy governance summary into `.clinerules/governance-rules.md`.

---

### OpenAI Codex

**Full workflow support** with `AGENTS.md` integration.

#### Automated Install

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform codex -Bundle full
```

```bash
./installer/install.sh --target <your-project-path> --platform codex --bundle full
```

#### Manual Install

```powershell
$Source = "<path-to-AIPDLC>/pdlc-packages"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

Copy-Item "$Source\session-orchestrator.md" "$Target\AGENTS.md"
```

#### Resulting Structure

```
your-project/
├── AGENTS.md                            ← ONLY always-loaded file (orchestrator)
├── .aiflc/pdlc/                          ← all cores + rule-details (on demand)
├── pdlc-ws/                              ← all runtime outputs
└── (your project files)
```

#### AI-GCE on Codex

Rule generation works fully. Hook auto-execution unavailable. Workaround: append governance rules to root `AGENTS.md`.

#### Sandbox Compatibility

| Mode | Compatibility |
|------|:------------:|
| `suggest` (default) | ✅ Full |
| `auto-edit` | ✅ Full |
| `full-auto` | ✅ Full |

---

### GitHub Copilot

**Partial support** — workspace-level instructions with some on-demand reading limitations.

#### Automated Install

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform copilot -Bundle full
```

```bash
./installer/install.sh --target <your-project-path> --platform copilot --bundle full
```

#### Manual Install

```powershell
$Source = "<path-to-AIPDLC>/pdlc-packages"
$Target = "<your-project-path>"

New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

New-Item -ItemType Directory -Force -Path "$Target\.github"
Copy-Item "$Source\session-orchestrator.md" "$Target\.github\copilot-instructions.md"
```

#### Resulting Structure

```
your-project/
├── .github/
│   └── copilot-instructions.md          ← ONLY always-loaded file (orchestrator block)
├── .aiflc/pdlc/                          ← all cores + rule-details (on demand)
├── pdlc-ws/                              ← all runtime outputs
└── (your project files)
```

#### Tips for Copilot

- Use `@workspace` prefix if Copilot doesn't pick up instructions automatically
- Reference cores explicitly if needed: "Read `.aiflc/pdlc/ai-pilc-rules/core-workflow.md`"
- Use Copilot Chat (not inline suggestions) for workflow execution

#### Limitations

| Limitation | Workaround |
|-----------|------------|
| On-demand file reading inconsistent | Reference files explicitly in prompts |
| Single instructions file | Not a problem — only the orchestrator goes there |
| No hook/agent execution | Use CI/CD hooks instead |

---

### VS Code Agent Framework

**Full support** — works with any model provider (Copilot, Claude, Gemini, OpenAI, or custom). Requires VS Code 1.102+.

#### Installation Options

**Option A — `AGENTS.md` (universal, any AI agent):**

```powershell
$Source = "<path-to-AIPDLC>/pdlc-packages"
$Target = "<your-project-path>"

Copy-Item "$Source\session-orchestrator.md" "$Target\AGENTS.md"
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc" | Out-Null
# Copy desired packages into .aiflc/pdlc/ (same as other platforms)
```

**Option B — `.github/copilot-instructions.md` (Copilot-focused):**

Use the automated installer with `-Platform copilot`.

#### Which AI Model Works Best?

| Model | Rating | Notes |
|-------|:------:|-------|
| Claude (Anthropic) | ✅ Best | Excellent instruction-following |
| GPT-4o / GPT-4.1 | ✅ Good | Works well |
| Copilot (GPT-based) | ✅ Good | Use Chat view, not inline |
| Gemini | ✅ OK | May need more explicit prompting |
| Local models (Ollama) | ⚠️ | 70B+ recommended |

#### Advanced: Custom Agents

VS Code supports `.github/agents/*.agent.md`. You can wrap each package as a named agent:

```markdown
<!-- .github/agents/pdlc-ai-pilc.agent.md -->
---
name: AI-PILC
description: Project Initiation Life Cycle
instructions:
  - .aiflc/pdlc/ai-pilc-rules/core-workflow.md
tools:
  - read_file
  - write_file
---
```

This lets users invoke `@ai-pilc` in chat directly (advanced configuration, not automated by installer).

#### AI-GCE on VS Code

Rule generation works fully. VS Code 1.102+ supports `.github/hooks/` for basic enforcement. AI-GCE hooks can be adapted to VS Code format (not yet automated). Workaround: create `.github/instructions/governance.instructions.md` with `applyTo: '**'`.

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

Packages detect each other's output through **state marker files**. When a package completes, it writes a marker (e.g., `pilc-state.md`). When the next package starts, it looks for upstream markers and enriches its work with that context.

### Example Chain: PILC → POLC → UXD → ADLC → DWG

```
1. Run AI-PILC → produces Project Initiation Package (PIP) + pilc-state.md
2. Run AI-POLC → detects pilc-state.md, reads PIP → produces Product Backlog Package (PBP)
3. Run AI-UXD  → detects pilc + polc state → produces UX Design Package (UXP)
4. Run AI-ADLC → detects all upstream state → produces Architecture Package (AP)
5. Run AI-DWG  → detects adlc-state.md → generates ready-to-code workspace
```

**No manual wiring needed.** Run packages sequentially and they find each other's output automatically.

---

## Session Continuity

Each workflow package maintains a **state file** (e.g., `pilc-state.md`) recording current phase, completed stages, pending decisions, depth level, and key outputs. Close your IDE and resume later — say "Continue AI-PILC" and the AI picks up exactly where you left off.

> Don't delete state files unless you want to restart a workflow from scratch.

---

## Cross-Platform Capabilities Matrix

| Feature | Kiro | Cursor | Claude Code | Amazon Q | Cline | Codex | Copilot | VS Code |
|---------|:----:|:------:|:-----------:|:--------:|:-----:|:-----:|:-------:|:-------:|
| Core workflow execution | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| On-demand file loading | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| Deliverable file output | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| State persistence | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Chain marker detection | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Multi-package install | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| AI-DWG workspace gen | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| AI-GCE rule generation | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| AI-GCE hook enforcement | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ |
| Agent shortcut triggers | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Automatic compliance log | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Depth adaptation | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Session continuity | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> **Kiro is the only platform with 100% feature coverage.** All other platforms lack hook execution and agent triggers but deliver the full workflow logic.

---

## Uninstalling

### Via Installer (all platforms)

```powershell
# Windows
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall
```

```bash
# macOS/Linux
./installer/install.sh --target <your-project-path> --uninstall
```

The installer reads `.ai-family-manifest.json` (in `pdlc-ws/`) and removes exactly what it installed. It will ask before deleting `pdlc-ws/` (your project data).

### Manual Removal (any platform)

```powershell
# Remove the package home (all cores + rule-details)
Remove-Item "<your-project-path>\.aiflc\pdlc" -Recurse -Force -ErrorAction SilentlyContinue

# Remove the orchestrator (platform-specific — see table above for location)
# Example for Kiro:
Remove-Item "<your-project-path>\.kiro\steering\session-orchestrator-pdlc.md" -ErrorAction SilentlyContinue

# Remove the manifest
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue

# Optionally remove all runtime outputs (back up first!)
# Remove-Item "<your-project-path>\pdlc-ws" -Recurse -Force
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Orchestrator not loading | Wrong location or format | Verify the orchestrator sits in your platform's native slot (see table above) |
| Package core not found | Path mismatch | Verify `.aiflc/pdlc/ai-{pkg}-rules/core-*.md` exists |
| "Can't find rule-details" | Path mismatch | Core resolves `.aiflc/pdlc/ai-{pkg}-rule-details/` |
| No welcome message | Wrong activation phrase | Use "Using AI-PILC, ..." format (uppercase package name) |
| State file not created | First interaction only | State is created after the first stage completes |
| Chain detection not working | Upstream state file missing | Run packages in order |
| Hooks not firing | Not on Kiro | AI-GCE hooks require Kiro for auto-execution |

---

*Part of the [AI-* PDLC Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./pdlc-packages/PLATFORM_CAPABILITIES.md) for the detailed cross-platform matrix*
