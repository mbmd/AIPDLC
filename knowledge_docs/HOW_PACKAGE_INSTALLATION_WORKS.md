# How Package Installation Works

**Purpose:** Explains how AI-* Family packages are installed into a workspace — the interactive installer, the uniform file placement model, the family workspace skeleton, platform-specific orchestrator deployment, and how multiple packages and families coexist cleanly.

---

## What Installation Means

AI-* packages are not compiled software. They are injectable workflow packages — collections of markdown files (cores, rule-details, templates) that an AI assistant reads on demand. "Installation" means running an interactive installer that copies these files into a locked structure so any supported AI platform can find and load them.

```
FAMILY SOURCE (e.g. AIPDLC repo)
├── installer/
│   ├── install.ps1   (Windows)
│   └── install.sh    (macOS / Linux)
└── pdlc-packages/
    ├── ai-pilc/
    ├── ai-adlc/
    ├── ...
    └── session-orchestrator.md
        │
        ▼  (installer runs)
YOUR WORKSPACE
├── .aiflc/pdlc/          ← package cores + rule-details (uniform, read on demand)
├── .kiro/steering/        ← session orchestrator (the ONE always-loaded file)
├── pdlc-ws/               ← family workspace (all outputs live here)
└── (your project files)
```

---

## The Uniform Placement Model (OI-158)

Every package's core file and its rule-details folder install into ONE brand-scoped, family-scoped home that is **identical on every platform**:

```
.aiflc/{family}/
├── ai-pilc-rules/core-workflow.md
├── ai-pilc-rule-details/
├── ai-adlc-rules/core-workflow.md
├── ai-adlc-rule-details/
├── ... (one pair per installed package)
├── FAMILY_BINDINGS.md          ← fabric trio (routing graph)
├── GATE_PROTOCOL.md            ← fabric trio (gate matching)
├── FAMILY_INTERFACE.md         ← fabric trio (discovery anchor)
├── TRIGGER_KEYS_REFERENCE.md   ← all activation keys + agent shortcuts
└── MANAGEMENT_FRAMEWORK_CONTRACT.md
```

Only the **session orchestrator** — the family's single always-loaded file — sits in each platform's native auto-load slot (e.g. `.kiro/steering/` on Kiro). Everything else lives uniformly under `.aiflc/{family}/` and is read on demand.

**Why this design:**
- Package cores never land at your workspace root — your root stays clean.
- The same path works on Kiro, Cursor, Claude Code, Cline, Amazon Q, and Copilot.
- Multiple families coexist without collision (each gets its own `.aiflc/{family}/` folder).

---

## The Session Orchestrator

The installer deploys one small (~120-line) routing file into each platform's native auto-load slot. This is the **only** file that auto-loads on every session. It:

1. Detects what you want to do (activation key or natural-language intent).
2. `Read`s ONLY the relevant package's core from `.aiflc/{family}/`.
3. Keeps all other package cores dormant so the context window stays free.

| Platform | Where the orchestrator lands |
|----------|------------------------------|
| **Kiro** | `.kiro/steering/session-orchestrator-{family}.md` |
| **Amazon Q** | `.amazonq/rules/{family}/session-orchestrator.md` |
| **Cursor** | `.cursor/rules/{family}-session-orchestrator.mdc` |
| **Cline** | `.clinerules/{family}-session-orchestrator.md` |
| **Claude Code** | `CLAUDE_{FAMILY}_ORCHESTRATOR.md` (imported via root `CLAUDE.md`) |
| **GitHub Copilot** | `.github/copilot-instructions-{family}-orchestrator.md` |

This means a fresh session starts lightweight — one routing table, not eleven package workflows.

---

## The Family Workspace (`{family}-ws/`)

The installer creates a locked skeleton at the workspace root where all package outputs will land at runtime:

```
{family}-ws/
├── .ai-family-manifest.json   ← install manifest (what was installed, where)
├── ideas/                      ← AI-ILC output
├── projects/                   ← AI-PILC / AI-ADLC / AI-POLC / AI-UXD / AI-DWG output
│   └── PROJECTS.md            ← project registry (bootstrapped empty)
├── portfolio/                  ← AI-PPM output
├── data/                       ← AI-DFE territory (data fabric surface)
│   ├── REGISTRY.json          ← consumer lookup (rebuilt on every DFE write)
│   ├── CONSUMER_REGISTRY.md   ← registered data consumers
│   ├── dfe-state.md           ← DFE engine state
│   ├── demands/               ← consumer demand declarations
│   └── history/               ← data snapshots (retention-managed)
└── tools/                      ← family extensions (dashboard, command board)
    └── extensions/
```

**Rules:**
- The skeleton is created once; re-running the installer preserves it (update-mode).
- `{family}-ws/` always lives at the workspace root — never nested.
- Multiple families coexist: each gets its own `{family}-ws/` (e.g. `pdlc-ws/`, `balc-ws/`).

---

## What the Installer Copies (Step by Step)

The installer performs these operations in sequence:

| Step | What | Destination |
|------|------|-------------|
| 1 | Package cores + rule-details (per selected package) | `.aiflc/{family}/ai-{pkg}-rules/` + `ai-{pkg}-rule-details/` |
| 2 | Session orchestrator | Platform's native auto-load slot |
| 3 | Family workspace skeleton | `{family}-ws/` (if not already present) |
| 4 | Family tools (extensions) | `{family}-ws/tools/extensions/` |
| 5 | Fabric trio (FLO/DFE routing graph) | `.aiflc/{family}/` (beside the cores) |
| 6 | Package agents (Kiro only) | `.kiro/agents/` |
| 7 | Claude Code extras (Claude Code only) | `.claude/commands/{family}/` + `.claude/skills/{family}/` |
| 8 | Install manifest | `{family}-ws/.ai-family-manifest.json` |

On non-Kiro platforms, agent shortcuts are used via shortcut-rules blocks pasted into the platform's rules surface (documented in each package's INSTALL.md).

---

## Preset Bundles

The installer offers preset package selections to match common use cases:

| Bundle | Packages | Use Case |
|--------|----------|----------|
| **Full** | All 11 packages | Complete family (power users) |
| **Design** | 9 packages (excludes GCE + TGE) | Design workspace (recommended) — companions are staged inert |
| **Minimal** | AI-PILC + AI-ADLC + AI-DWG | Quick start |
| **Architecture** | AI-ADLC + AI-DWG + AI-GCE | Architecture → workspace → governance |
| **Governance** | AI-GCE + AI-TGE | Add compliance to an existing workspace |
| **Portfolio** | AI-ILC + AI-PILC + AI-PPM + AI-FLO | Multi-project portfolio management |
| **Custom** | You pick | Mix and match |

---

## The Companion Model (OI-204)

AI-GCE and AI-TGE are **Layer-3 companions** — they run in the AI-DWG-generated project workspace (where code is built), not in the Layer-2 design workspace (where packages orchestrate). The installer handles this transparently:

- **Design bundle** (or any install with AI-DWG present but without GCE/TGE selected): companions are **staged inert** — their files are copied into `.aiflc/{family}/` so AI-DWG can later provision them into the generated workspace, but the session orchestrator **omits their routing rows** (they are not activatable in this workspace).
- **Governance bundle** (GCE + TGE only, no design-chain packages): a direct install into an existing Layer-3 project repo — companions are fully active.
- **Full bundle**: all packages active in one workspace (power users).
- **Custom mix** of companions + design-chain: **blocked** with an explanation — choose a preset bundle instead.

---

## Fabric Trio (FLO/DFE Routing Graph)

The installer deploys three files into the family home (`.aiflc/{family}/`) that AI-FLO and AI-DFE require at runtime:

| File | Purpose |
|------|---------|
| `FAMILY_BINDINGS.md` | Generated routing topology (internal + external edges) |
| `GATE_PROTOCOL.md` | Universal gate matching algorithm |
| `FAMILY_INTERFACE.md` | Discoverable seam surface |

Without these, AI-FLO returns **NOT READY** ("no bindings = no routing"). The installer copies them from the family source and removes them on uninstall.

---

## Package Agents

On **Kiro**, the installer copies runnable agent markdown files from each installed package's `templates/agents/` into `.kiro/agents/`. These enable agent shortcuts like `FHC__` (FLO health check) and `FIA__` (FLO integrity audit).

On **other platforms**, agents are not auto-deployed. Each package's INSTALL.md documents the shortcut-rules block to paste into that platform's rules surface.

---

## Consumer Registration

The installer scans installed tools for `data-demand/*.demand.md` files and auto-registers them in `{family}-ws/data/CONSUMER_REGISTRY.md`. This fulfills the AI-DFE consumer contract (Obligation 1) — consumers declare what data they need, and AI-DFE discovers them from the registry.

---

## Running the Installer

### Windows (PowerShell)

```powershell
.\installer\install.ps1 -TargetWorkspace "C:\Projects\my-app" -Platform kiro -Bundle design
```

### macOS / Linux (Bash)

```bash
./installer/install.sh --target ~/projects/my-app --platform kiro --bundle design
```

### Interactive Mode (no arguments)

Run the installer with no flags and it prompts for platform, bundle, and target.

### Dry Run

Add `-DryRun` (PowerShell) or `--dry-run` (Bash) to see what would be installed without copying files.

---

## Uninstall

The manifest at `{family}-ws/.ai-family-manifest.json` records everything that was installed. Uninstall reads it and reverses:

```powershell
.\installer\install.ps1 -TargetWorkspace "C:\Projects\my-app" -Uninstall
```

It removes package files, the orchestrator, agents, fabric trio, tools, and the Claude Code entry point. It then asks whether to also remove the family workspace (`{family}-ws/`) — answer **no** to keep your project data.

---

## Coexistence (Multiple Packages in One Workspace)

All packages share the same `.aiflc/{family}/` home. Coexistence is safe because:

1. **One active at a time** — the session orchestrator routes to exactly one package per session.
2. **Separate output folders** — each package writes to a distinct area inside `{family}-ws/`.
3. **State markers** — each package's `*-state.md` tracks its own progress without touching siblings.

Switching packages requires an explicit activation key (e.g. `_ADLC_`) or user confirmation — never happens silently.

---

## Coexistence (Multiple Families in One Workspace)

Installing a second family (e.g. BALC alongside PDLC) creates a parallel structure:

```
your-workspace/
├── .aiflc/
│   ├── pdlc/     ← PDLC family home
│   └── balc/     ← BALC family home
├── pdlc-ws/      ← PDLC family workspace
├── balc-ws/      ← BALC family workspace
└── .kiro/steering/
    ├── session-orchestrator-pdlc.md
    └── session-orchestrator-balc.md
```

Each family's orchestrator is **family-scoped** (filename includes the family code). They coexist in the same platform slot without overwriting each other. Neither installer touches the other family's files.

---

## Version Management

Each package has a version in its README and core file. When updating:
1. Re-run the installer with `-Force` (overwrites existing files).
2. The family workspace skeleton is preserved — your project data is safe.
3. State files remain valid across versions (backward compatible).
4. The manifest is regenerated to reflect the updated set.

---

## What Is NOT Installed

The family repo contains reference material that stays in the repo (never copied into your workspace):

- `knowledge_docs/` — design patterns and reference material (repo-only reading)
- `narrative/` — whitepapers and HOW documents
- `contracts/` — cross-package conventions
- Package `README.md`, `USER_GUIDE.md`, `WHITEPAPER.md` files

These are for reading in the repo or your clone. The installer only installs the operational files your AI agent needs at runtime.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Multi-Platform Support Works | `knowledge_docs/HOW_MULTI_PLATFORM_SUPPORT_WORKS.md` |
| How Steering File Loading Works | `knowledge_docs/HOW_STEERING_FILE_LOADING_WORKS.md` |
| How Package Activation & Isolation Works | `knowledge_docs/HOW_PACKAGE_ACTIVATION_ISOLATION_WORKS.md` |
| How the Communication Fabric Works | `knowledge_docs/HOW_COMMUNICATION_FABRIC_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| Family Structure | `FAMILY_STRUCTURE.md` |

---

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-08-10 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
