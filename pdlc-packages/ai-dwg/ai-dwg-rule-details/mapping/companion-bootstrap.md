<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Companion Bootstrap — Provision AI-GCE / AI-TGE into the Generated Layer-3 Workspace

## Purpose

Copies the Layer-3 companion engines (AI-GCE governance, AI-TGE test governance) from the Layer-2 design-workspace **provisioning source** into the generated dev workspace's `.governance/engine/` directory. This is the Layer-2 → Layer-3 handoff: the companions are staged inert in Layer 2 (placed by the installer as a provisioning source) and activated in Layer 3 (where they derive their enforcement layer from the workspace steering).

**Trigger:** Config Gate Q3 ≠ No (runs after agent-installation, Mode 1 and Mode 3).

**Outputs:**
1. `.governance/engine/ai-gce/` — AI-GCE core + rule-details (operational content only)
2. `.governance/engine/ai-tge/` — AI-TGE core + rule-details (operational content only)
3. `.governance/GOVERNANCE_INDEX.md` — first-session bootstrap notice appended
4. `.governance/workspace-manifest.yaml` — `governance.provisioned` block recorded

**Grounding:** OI-204 (Companion Package Placement design); layout design Part 3E principle P3.

---

## MANDATORY: Stage Sub-Role — Automation Engineer

Automation Engineer mindset (copy operations, manifest updates, machine-readable contracts). ADDS a dimension — does NOT replace the primary role.

### Behavioral Shifts
- This is a COPY operation, not a derivation — DWG places files but does NOT run GCE/TGE logic
- Provenance is recorded in the manifest, not in the copied files (they already carry their own metadata)
- Never modify the companion cores — they are placed verbatim (ownership: `[tool]`)

### Anti-Patterns
- Do NOT run `_GCE_` or `_TGE_` derivation — the dev team does that on first activation
- Do NOT auto-activate companions — human-in-the-loop (the dev team must choose to start governance)
- Do NOT copy LICENSE/NOTICE/README/PLAN — those are package metadata, not operational runtime content
- Do NOT provision if already present — detect and skip (brownfield re-entry)

---

## Source (Layer-2 Provisioning Source)

The companion packages are staged by the installer into the uniform family home in the **design workspace** (the workspace where DWG itself runs):

```
{design-workspace-root}/.aiflc/{family}/ai-gce-rules/core-engine.md
{design-workspace-root}/.aiflc/{family}/ai-gce-rule-details/
{design-workspace-root}/.aiflc/{family}/ai-tge-rules/core-engine.md
{design-workspace-root}/.aiflc/{family}/ai-tge-rule-details/
```

> **Resolve the source:** DWG reads its own runtime path (resolved at load time via the standard AIFLC home detection) and looks for the companion directories beside its own core. If a selected companion is NOT present in the provisioning source, WARN and skip — inform the user to install the `design` bundle (which stages both companions).

---

## Target (Layer-3 Generated Workspace)

```
{generated-workspace-root}/
└── .governance/
    ├── engine/
    │   ├── ai-gce/
    │   │   ├── core-engine.md                    ← the GCE dispatcher
    │   │   └── ai-gce-rule-details/              ← full rule-details tree
    │   │       ├── common/
    │   │       ├── generators/
    │   │       ├── re-derivation/
    │   │       ├── rendering/
    │   │       └── templates/
    │   └── ai-tge/
    │       ├── core-engine.md                    ← the TGE dispatcher
    │       └── ai-tge-rule-details/              ← full rule-details tree
    │           ├── common/
    │           ├── strategy/
    │           └── templates/
    ├── GOVERNANCE_INDEX.md                       ← updated: first-session bootstrap notice appended
    └── workspace-manifest.yaml                   ← updated: governance.provisioned block added
```

---

## Transformation Rules

### Rule 1: Copy Operational Content Only

Copy the **entire** rules-dir + rule-details-dir trees for the selected companion(s). EXCLUDE these package-metadata files (present in the provisioning source but not runtime-relevant):

- `LICENSE`
- `NOTICE`
- `README.md`
- `PLAN.md`
- `CONCEPTUAL_MAP.md`
- `WHITEPAPER.md`
- `USER_GUIDE.md`
- `setup/` (installation guides — the package is already placed)

### Rule 2: Selection Respects Q3

| Q3 Answer | Copy |
|-----------|------|
| Yes (default) | Both AI-GCE + AI-TGE |
| GCE-only | AI-GCE only |
| TGE-only | AI-TGE only |
| No | Nothing (this mapping does not run) |

### Rule 3: Brownfield Detection (Skip If Present)

Before copying, check if `.governance/engine/ai-gce/core-engine.md` (and/or `ai-tge`) already exists. If present:
- **Skip** that companion (do not overwrite)
- **Inform** the user: "AI-GCE already provisioned in this workspace (version: {read from manifest}). Use `UPG__` to update."
- Continue with the other companion if applicable

### Rule 4: Populate GOVERNANCE_INDEX.md

After copying, append the first-session bootstrap notice to `.governance/GOVERNANCE_INDEX.md` (template: `templates/operational/governance-bootstrap-notice.md`). If the index file does not exist, create it with a minimal header + the notice. If the companion section already exists (marker-guarded `<!-- COMPANION-BOOTSTRAP:start/end -->`), replace it.

### Rule 5: Record in workspace-manifest.yaml

Add/update the `governance.provisioned` block:

```yaml
governance:
  # ... existing reserved paths (home, index, engine, rules, agents, hooks, test) ...
  provisioned:
    - package: ai-gce
      version: "{read from core-engine.md front-matter or best-available}"
      provisionedOn: "{ISO-timestamp}"
    - package: ai-tge
      version: "{read from core-engine.md front-matter or best-available}"
      provisionedOn: "{ISO-timestamp}"
  provisionedBy: AI-DWG
  provisionedForTools: [kiro, claude-code]   # = Config Gate Q2 platformTargets
```

Only list the companions actually placed (respects Q3 + brownfield skip).

### Rule 6: DWG Does NOT Derive

DWG places the engines but NEVER:
- Runs `_GCE_` or `_TGE_` logic (derivation is a developer action)
- Creates hooks, rules, or agents (that's GCE/TGE's job on first activation)
- Modifies the placed core files (ownership: `[tool]` — placed verbatim)
- Auto-activates the engines (human-in-the-loop)

The companion engines are **dormant** after provisioning — they activate when the developer types `_GCE_` or `_TGE_`.

### Rule 7: Mode 2 (Reconciliation) Behavior

On reconciliation, DWG:
- Reads the `governance.provisioned` block from the manifest
- If provisioned packages are present → leaves them untouched
- If the design-workspace provisioning source has a NEWER version (compare `version` field) → **offer** (never force): "AI-GCE has updated in the design workspace (v{old} → v{new}). Update? [y/N]"
- On approval: re-copy (overwrite `.governance/engine/ai-gce/`), bump `provisionedOn`, update `version`
- The `UPG__` shortcut also triggers this check from the companion side

---

## Interaction With Other Files

| File | Interaction |
|------|-------------|
| `core-generator.md` Config Gate Q3 | Reads the Q3 answer to decide whether/what to provision |
| `baseline/workspace-manifest-generation.md` | DWG writes manifest; this mapping extends the `governance:` block |
| `rendering/*` | NOT invoked by this mapping — companions do their own rendering at `_GCE_`/`_TGE_` activation |
| `flows/full-generation.md` | This mapping runs AFTER full generation + agent installation |
| `flows/brownfield-overlay.md` | Also triggers companion bootstrap (Mode 3 generates steering → companions consume it) |
| AI-GCE `templates/governance-index.md` | The GOVERNANCE_INDEX template that GCE creates/owns; DWG pre-populates it with the bootstrap notice only |

---

## Key Principles (from the design)

1. **DWG is the default provisioner for the greenfield chain, not the only path.** Standalone/brownfield teams can install the `governance` bundle directly into their Layer-3 repo.
2. **Companions are Layer-3 packages.** They have no role in the Layer-2 design workspace. DWG is the hinge that ferries them across.
3. **Human-in-the-loop.** The companions don't auto-activate; the dev team decides when to start governance enforcement.
4. **The workspace manifest is the discovery contract.** GCE/TGE find their own engine via `manifest.governance.engine` — never by hardcoded path.
