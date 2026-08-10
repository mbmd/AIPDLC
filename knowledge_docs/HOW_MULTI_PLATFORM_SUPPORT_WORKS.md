# How Multi-Platform Support Works

**Purpose:** Explains how AI-* Family packages work across different AI coding platforms — the uniform placement model, per-platform orchestrator deployment, Claude Code's extended integration (skills + slash commands), and what's universal vs. what adapts per platform.

---

## The Platform-Agnostic Design

AI-* packages are **platform-agnostic markdown workflows**. The content — cores, rule-details, templates, state files, gate contracts — is identical regardless of which AI platform executes it. Only TWO things differ per platform:

1. **Where the session orchestrator lands** (each platform's native auto-load slot).
2. **Platform-specific extras** (Claude Code gets slash commands and a skill; Kiro gets deployed agents).

Everything else — the package home, the family workspace, the fabric trio — is uniform.

```
┌──────────────────────────────────────────────────────────────────────┐
│  UNIFORM LAYER (same across ALL platforms)                            │
│                                                                       │
│  .aiflc/{family}/                                                     │
│  ├── ai-{pkg}-rules/core-*.md          (package cores)                │
│  ├── ai-{pkg}-rule-details/            (stage-specific rules)         │
│  ├── FAMILY_BINDINGS.md                (fabric routing graph)         │
│  ├── GATE_PROTOCOL.md                  (gate matching algorithm)      │
│  └── FAMILY_INTERFACE.md               (seam surface)                 │
│                                                                       │
│  {family}-ws/                                                         │
│  ├── ideas/ projects/ portfolio/ data/ tools/                         │
│  └── .ai-family-manifest.json                                         │
└──────────────────────────────────────────────────────────────────────┘
        │
        ▼  (thin adapter: orchestrator placement + platform extras)
┌──────┐ ┌──────────┐ ┌──────────┐ ┌───────┐ ┌─────────────┐ ┌─────────┐
│ Kiro │ │ Amazon Q │ │  Cursor  │ │ Cline │ │ Claude Code │ │ Copilot │
└──────┘ └──────────┘ └──────────┘ └───────┘ └─────────────┘ └─────────┘
```

---

## What's Universal (Works Everywhere, Unchanged)

| Capability | Platform Dependency |
|-----------|:-------------------:|
| Package cores (workflow orchestration) | None — pure markdown in `.aiflc/{family}/` |
| Rule-details (stage-specific rules + templates) | None — same location on every platform |
| State files (session continuity) | None — file-based, in `{family}-ws/` |
| Chain contracts and gate matching | None — Communication Fabric is file-based |
| Role/persona adoption | None — prompt-based |
| Depth levels (Minimal / Standard / Comprehensive) | None — logic-based |
| Output generation (PIP, AP, PBP, UXP, DW) | None — file creation into `{family}-ws/` |
| Family workspace skeleton | None — identical on every platform |
| Fabric trio (FLO/DFE routing) | None — deployed identically |
| Activation keys (`_PILC_`, `_ADLC_`, etc.) | None — text-based, recognized by the orchestrator |
| Data fabric (AI-DFE gather/shape/distribute) | None — operates on `{family}-ws/data/` |

---

## What Adapts Per Platform (The Thin Adapter)

| Capability | What changes |
|-----------|--------------|
| **Session orchestrator slot** | The one always-loaded file lands in a different native location per platform |
| **Package agents** | Kiro: deployed to `.kiro/agents/`. Others: shortcut-rules blocks pasted per INSTALL.md |
| **Hook enforcement (AI-GCE)** | Kiro: native `.kiro/hooks/` execution. Others: CI/pre-commit translation |
| **Claude Code extras** | Slash commands (`.claude/commands/{family}/`) + skill (`.claude/skills/{family}/`) |

---

## Per-Platform Details

### Session Orchestrator Placement

The installer deploys the orchestrator into each platform's native auto-load slot:

| Platform | Orchestrator Path | Auto-Load Mechanism |
|----------|-------------------|---------------------|
| **Kiro** | `.kiro/steering/session-orchestrator-{family}.md` | All files in `.kiro/steering/` auto-load |
| **Amazon Q Developer** | `.amazonq/rules/{family}/session-orchestrator.md` | Rules folder auto-loads |
| **Cursor** | `.cursor/rules/{family}-session-orchestrator.mdc` | Rules folder auto-loads |
| **Cline** | `.clinerules/{family}-session-orchestrator.md` | Root rules file auto-loads |
| **Claude Code** | `CLAUDE_{FAMILY}_ORCHESTRATOR.md` | Imported via root `CLAUDE.md` (`@` import) |
| **GitHub Copilot** | `.github/copilot-instructions-{family}-orchestrator.md` | Copilot instructions auto-load |

The orchestrator content is functionally identical across platforms — only the filename, path, and (for Cursor) the `.mdc` extension differ. Claude Code gets a parallel variant that uses `Read` directives instead of `#hashtag` steering syntax (since Claude Code has no hashtag file-reference).

---

### Kiro (Full Support — Reference Implementation)

| Feature | Implementation |
|---------|---------------|
| Package home | `.aiflc/{family}/` (uniform) |
| Orchestrator | `.kiro/steering/session-orchestrator-{family}.md` (auto-loaded) |
| Hook enforcement | `.kiro/hooks/*.json` (event-driven, fires on IDE events) |
| Agents | `.kiro/agents/*.md` (auto-deployed by installer; shortcut-triggered) |
| File-match steering | Supported (conditional loading based on active file) |

Kiro is the only platform where AI-GCE's hooks fire natively on IDE events and agents activate via typed shortcuts. This makes it the reference implementation for the full governance layer.

---

### Amazon Q Developer (Full Workflow Support)

| Feature | Implementation |
|---------|---------------|
| Package home | `.aiflc/{family}/` (uniform) |
| Orchestrator | `.amazonq/rules/{family}/session-orchestrator.md` |
| Hook enforcement | Not native — use CI/pre-commit as enforcement alternative |
| Agents | Shortcut-rules blocks per package INSTALL.md |

All workflow packages execute identically to Kiro. The orchestrator routes to cores on demand.

---

### Cursor (Full Workflow Support)

| Feature | Implementation |
|---------|---------------|
| Package home | `.aiflc/{family}/` (uniform) |
| Orchestrator | `.cursor/rules/{family}-session-orchestrator.mdc` |
| Hook enforcement | Not native — use CI/pre-commit |
| Agents | Shortcut-rules blocks per package INSTALL.md |

Cursor's `.mdc` extension is the only file-format difference. The orchestrator content is the same.

---

### Cline (Full Workflow Support)

| Feature | Implementation |
|---------|---------------|
| Package home | `.aiflc/{family}/` (uniform) |
| Orchestrator | `.clinerules/{family}-session-orchestrator.md` |
| Hook enforcement | Not native — use CI/pre-commit |
| Agents | Shortcut-rules blocks per package INSTALL.md |

---

### Claude Code (Full Workflow + Extended Integration)

| Feature | Implementation |
|---------|---------------|
| Package home | `.aiflc/{family}/` (uniform) |
| Orchestrator | `CLAUDE_{FAMILY}_ORCHESTRATOR.md` (imported via root `CLAUDE.md`) |
| Hook enforcement | Not native — append governance rules to `CLAUDE.md` + CI |
| Agents | Shortcut-rules blocks; also via slash commands (below) |
| **Slash commands** | `.claude/commands/{family}/*.md` → `/{family}:<key>` in chat |
| **Skill registration** | `.claude/skills/{family}/SKILL.md` → Claude auto-discovers the family |

**Claude Code entry point:** Claude Code auto-loads only a real `CLAUDE.md` (no glob). The installer appends a marker-guarded `@import` line to your root `CLAUDE.md` that pulls in the orchestrator. If you don't have a `CLAUDE.md`, the installer creates one.

**Slash commands:** The installer generates one command per installed package (e.g. `/pdlc:pilc`, `/pdlc:adlc`) plus destination agent shortcuts (e.g. `/pdlc:dat`, `/pdlc:fhc`). Each command `Read`s the canonical core from `.aiflc/{family}/` — zero workflow duplication.

**Skill registration:** The installer copies the family's `SKILL.md` to `.claude/skills/{family}/SKILL.md` and appends a pointer to the orchestrator. Claude auto-discovers skills by folder — so multiple families coexist cleanly.

---

### GitHub Copilot (Partial — Workspace-Level Only)

| Feature | Implementation |
|---------|---------------|
| Package home | `.aiflc/{family}/` (uniform) |
| Orchestrator | `.github/copilot-instructions-{family}-orchestrator.md` |
| Hook enforcement | GitHub Actions + branch protection |
| Agents | Not available natively |

Copilot's instructions mechanism is workspace-level only. All workflow packages function, but governance enforcement requires GitHub Actions rather than IDE-native hooks.

---

## Governance Portability

AI-GCE generates governance artifacts designed for Kiro but translatable:

| AI-GCE Output | Kiro | Other Platforms |
|---------------|------|-----------------|
| `.kiro/hooks/*.json` | Native hook execution (event-driven) | Translate to pre-commit hooks or CI checks |
| `.kiro/agents/*.md` | Native agent triggers (shortcut-activated) | Include as documentation / paste shortcut-rules blocks |
| `.governance/rules/*.md` | Referenced by hooks | Documentation + manual/CI enforcement |
| `.compliance-state.json` | Read by hooks for tier logic | Read by scripts for CI gate decisions |

**Key principle:** The RULES are portable (markdown). The ENFORCEMENT mechanism varies. A team on Cursor gets the same rules as a team on Kiro — enforced differently (CI instead of IDE hooks).

---

## Platform Capabilities Matrix

| Capability | Kiro | Amazon Q | Cursor | Cline | Claude Code | Copilot |
|-----------|:----:|:--------:|:------:|:-----:|:-----------:|:-------:|
| Workflow packages (all 11) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Session orchestrator | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Activation keys | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| State files & chain handoff | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Family workspace outputs | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Data fabric (AI-DFE) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Communication Fabric (gates) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Event-driven hooks (AI-GCE) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Agent shortcuts (native) | ✅ | ❌ | ❌ | ❌ | ⚠️ via `/` | ❌ |
| Slash commands | — | — | — | — | ✅ | — |
| Skill registration | — | — | — | — | ✅ | — |
| Automatic compliance logging | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Re-derivation triggers (auto) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Summary:** All 11 workflow packages, the chain, and the data fabric work identically on every platform. Only IDE-event enforcement (hooks, automatic agents, compliance logging) is Kiro-exclusive — because only Kiro has a hook runtime that intercepts IDE events.

---

## Choosing a Platform

| If You Need | Recommended |
|-------------|-------------|
| Full governance enforcement (hooks fire on saves/commits) | Kiro |
| Workflow packages + manual governance | Any platform |
| Slash-command shortcuts for package activation | Claude Code |
| CI-based enforcement (not IDE-based) | Any platform + CI pipeline |
| Team uses multiple AI tools | Install on each; use CI for enforcement; family workspace is shared |

---

## Multi-Family Coexistence Across Platforms

The uniform home (`.aiflc/{family}/`) and family-scoped orchestrator filenames mean multiple families install cleanly on any platform:

- Kiro: `.kiro/steering/session-orchestrator-pdlc.md` + `session-orchestrator-balc.md`
- Claude Code: `.claude/skills/pdlc/SKILL.md` + `.claude/skills/balc/SKILL.md`
- Cursor: `.cursor/rules/pdlc-session-orchestrator.mdc` + `balc-session-orchestrator.mdc`

Each family is fully isolated — installing one never touches another.

---

## Additional Platforms (Expected to Work, Not Yet Validated)

The following AI assistants are expected to work (they support workspace-level rules files) but are not yet installer-validated:

- Windsurf (via `.windsurfrules`)
- Augment Code
- Tabnine
- JetBrains AI Assistant
- Sourcegraph Cody
- Continue
- Aider

For these, use the "Universal" install instructions in each package's INSTALL.md: copy the orchestrator content into the platform's native rules file, point it at `.aiflc/{family}/`, and the workflow packages function normally.

---

## Related Documents

| Document | Location |
|----------|----------|
| How Package Installation Works | `knowledge_docs/HOW_PACKAGE_INSTALLATION_WORKS.md` |
| How Steering File Loading Works | `knowledge_docs/HOW_STEERING_FILE_LOADING_WORKS.md` |
| How Package Activation & Isolation Works | `knowledge_docs/HOW_PACKAGE_ACTIVATION_ISOLATION_WORKS.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How to Adopt Governance on a Project | `knowledge_docs/HOW_TO_ADOPT_GOVERNANCE_ON_A_PROJECT.md` |

---

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-08-10 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
