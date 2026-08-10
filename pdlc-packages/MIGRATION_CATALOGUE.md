<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under the Apache License, Version 2.0. See LICENSE. Attribution required - see NOTICE. -->
# PDLC — Migration Catalogue (Artifact Feature Migrations)

> **What this is.** The list of *output-feature improvements* the family upgrade agent (`UPG__`) can retrofit into an existing `pdlc-ws/` workspace. When a PDLC package gains a new output feature, the feature is added here so workspaces created by an earlier version can be brought up to the current feature set without re-running the workflows.
>
> **Who reads it.** The `UPG__` family upgrade agent (`family-upgrade-agent.md`). Installed once per workspace (create-if-absent) by whichever PDLC package the user installs.
>
> **Design principle — detect by inspecting the artifact, not by trusting a version number.** Every migration carries a **Detection** check that inspects the actual `pdlc-ws/` files. A migration is "pending" only if detection finds artifacts lacking the feature. This makes every migration **idempotent** and independent of any manifest or version stamp.
>
> **AI-agnostic.** Every transform is expressed as plain markdown edits any assistant can perform on any platform.

---

## How the upgrade agent uses this file

For each **installed** package (detected by the presence of `.aiflc/pdlc/ai-{code}-rules/`), the agent:
1. Reads migrations whose **Applies to** includes that package.
2. Runs each migration's **Detection** against that package's `pdlc-ws/` artifacts.
3. Collects pending migrations (detection found artifacts lacking the feature) into a per-package list.
4. Presents the list and asks the user to **Apply** or **Skip** — per package.
5. For applied migrations: performs the **Transform**, honoring `ownership` (see table below).
6. Logs a governance entry and moves to the next package.

---

## Migration index

| ID | Feature | Applies to | Status |
|----|---------|-----------|:------:|
| **M1** | Clickable reference links | all 9 packages | Active |
| **M2** | Visual pairing (table + Mermaid diagram) | packages with framework tables (PILC, ADLC, POLC, PPM) | Active |
| **M3** | AI-LENS `aiFeature` tag support | ILC, PILC, POLC, UXD, ADLC, DWG | Active |
| **M4** | AI-LENS `data-schema/` AI fields | all 8 lens-aware packages (ILC, PILC, POLC, UXD, ADLC, DWG, GCE, TGE) | Active |
| **M5** | Companion placement correction (GCE/TGE → Layer 3) | DWG, GCE, TGE | Active |
| **M6** | Automation-LENS `automationFeature` tag support | ILC, PILC, POLC, UXD, ADLC, DWG | Active |
| **M7** | Automation-LENS `data-schema/` automation fields + `Lens_Status.md` | all 8 lens-aware packages (ILC, PILC, POLC, UXD, ADLC, DWG, GCE, TGE) | Active |
| **M8** | Agentic intersection-facet support (derived `agenticProfile`) | co-tagged features in ILC, PILC, POLC, UXD, ADLC, DWG | Active |
| **M9** | Workspace HTML publishing (browsable shadow site) | whole workspace (tool-level) | Active |

### Ownership handling (applies to every migration)

All transforms are **additive** — wrap existing code text in a link, add an anchor before a row, or insert a diagram after a table. Never rewrite or remove content.

| Ownership class | Migration behavior |
|-----------------|--------------------|
| tool-managed / `generated` | Apply directly |
| living / team-adopted / `hybrid` | Preview diff and confirm — additive edits preserve all custom content; `<!-- custom -->` regions untouched |
| user-locked / `user` | Skip and report |

---

## M1 — Clickable reference links

**Feature.** Codes defined in another generated file are written as relative markdown links (see `common/reference-linking.md`). In preview they render as clean clickable text; clicking opens the defining file.

**Applies to.** Every `pdlc-ws/` artifact that mentions a code defined elsewhere — project folders, idea register, management framework registers, architecture decisions.

**Detection (is it pending?).** Find **bare** code tokens (not already inside a `[…](…)` link) matching PDLC code patterns AND whose definition file exists:
- `IDEA-\d+` → `pdlc-ws/ideas/{NNN}-{slug}/idea.md`
- `PRJ-[A-Z]+-\d{4}-\d+` → `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`
- `ADR-\d+` → `pdlc-ws/projects/*/architecture/decisions/ADR-{NNN}.md`
- `CR-[A-Z]+-\d{4}-\d+` → change register
- If bare tokens with existing definition targets are found → **M1 is pending**.

**Transform.**
1. For each register this package owns, ensure every defined row carries a portable anchor (`<a id="code-id"></a>`). Add missing anchors; never duplicate.
2. Replace each detected bare code with a relative link to its definition, computing the relative path from the editing file to the target per `OUTPUT_AND_STATE_CONTRACT.md` layout.
3. Leave codes without a definition file as plain text; note in the run report.

**Idempotency.** Already-linked codes and existing anchors are detected and left untouched.

---

## M2 — Visual pairing (table + Mermaid diagram)

**Feature.** Framework artifacts pair their authoritative table with a Mermaid diagram beneath it. Table stays authoritative (machine-parseable); diagram is the human view. Diagram type: `flowchart` for hierarchy/sequence/process; `quadrantChart` for two-axis scored matrices.

**Applies to.** Framework artifacts with authoritative tables: PIP (PILC), Architecture Package / ADR log (ADLC), Backlog (POLC), Portfolio (PPM).

**Detection (is it pending?).** Find files with an authoritative table that have no accompanying ` ```mermaid ` block following it → **M2 is pending**.

**Transform.** Insert a `mermaid` fenced block immediately after the table, choosing the correct diagram type per the artifact. Populate nodes from table rows using existing labels/`{placeholder}`s. Obey `evidence-or-abstain` — no fabricated data.

**Idempotency.** Artifacts already having a paired Mermaid block are detected and skipped.

---

## M3 — AI-LENS `aiFeature` tag support

**Feature.** Artifacts produced by AI-LENS-aware packages carry `aiFeature` front-matter tags (per `AI_LENS_PROTOCOL.md` §4) so AI features are threaded across the lifecycle and discoverable by `DAT__`.

**Applies to.** Packages that produce artifacts which can be AI-tagged: AI-ILC (Idea Brief), AI-PILC (PIP + Decision_Log), AI-POLC (epics/stories), AI-UXD (UXP interaction designs), AI-ADLC (ADRs + component designs), AI-DWG (generated workspace + `.ai-lens/manifest.json`).

**Detection (is it pending?).** Check whether the workspace's `management_framework/Decision_Log.md` contains an AI-LENS mode row (any row with "AI-LENS" or "AI Lens mode" in the Decision column). If no such row exists AND the project has AI features (any `aiFeature: true` front-matter in `backlog/epics/` or a `.ai-lens/manifest.json`), the mode record was never formally captured → **M3 is pending** for PILC. For POLC: check `backlog/epics/*.md` for epics with AI-related content but missing `aiFeature` front-matter → pending. For DWG: check whether `.ai-lens/manifest.json` exists in the generated workspace → if absent and AI features exist upstream → pending.

**Transform.**
1. **PILC:** Append an AI-LENS mode `Decision_Log` row (ask user for the mode choice: No-AI / AI-Powered + sub-modes). ID format: `PILC-{ABBREV}-D-{N}`.
2. **POLC:** For each epic/story identified as AI-relevant, add `aiFeature: true` + `aiSubMode` + `aiCapability` + `aiFeatureId: AIF-{NNN}` to front-matter (confirm each with user). Add `## AI Acceptance Criteria` section.
3. **DWG:** Generate `.ai-lens/manifest.json` with the couriered context from the tagged artifacts.
4. **ILC/UXD/ADLC:** Add front-matter tags to relevant artifacts where missing.

**Idempotency.** Artifacts already carrying `aiFeature: true` with a valid `aiFeatureId` are skipped. Decision_Log rows are append-only (never edit existing).

---

## M4 — AI-LENS `data-schema/` AI fields

**Feature.** Each package's `data-schema/` includes an `aiLens` sub-object so AI-DFE's existing `DAT__` can gather the AI-feature thread into the traceability JSON (per `AI_LENS_PROTOCOL.md` §6.2).

**Applies to.** All 8 lens-aware packages: AI-ILC, AI-PILC, AI-POLC, AI-UXD, AI-ADLC, AI-DWG, AI-GCE, AI-TGE.

**Detection (is it pending?).** For each installed package, read `{pkg}-data.schema.json` and check for the presence of an `"aiLens"` key in `data.properties`. If absent → **M4 is pending** for that package.

**Transform.** Add the `aiLens` sub-object to `data.properties` in the schema JSON, matching the fields defined in `AI_LENS_PROTOCOL.md` §6.2 for that package. Also append the AI-LENS extraction rules to `SOURCE_MAP.md`.

**Idempotency.** If `"aiLens"` already exists in the schema, skip. Check for key presence, not content equality (allows forward-compatible field additions).

---

## M5 — Companion placement correction (GCE/TGE → Layer 3)

**Feature.** AI-GCE and AI-TGE are Layer-3 (Execute) companions — they belong in the AI-DWG-generated project workspace (`{slug}-workspace/`), not the Layer-2 design workspace. This migration detects workspaces where they were co-installed for use in Layer 2 (the legacy `full` install model) and offers to convert them to the correct two-workspace topology. [OI-204]

**Applies to.** Any `pdlc-ws/` workspace that has AI-GCE or AI-TGE **installed for use** alongside the design chain in a Layer-2 design workspace (i.e., the orchestrator routes `_GCE_`/`_TGE_` and the `packages[]` manifest list contains `ai-gce`/`ai-tge`).

**Detection (is it pending?).**
1. Check `pdlc-ws/.ai-family-manifest.json`: does `packages[]` contain `ai-gce` or `ai-tge`?
2. Check the deployed orchestrator: does it contain `_GCE_` or `_TGE_` activation rows?
3. If BOTH conditions are true AND the workspace also contains design-chain packages (ai-dwg, ai-adlc, ai-polc, ai-uxd, ai-pilc, ai-ilc) → this is a Layer-2 workspace with companions installed for use → **M5 is pending**.
4. If the workspace is standalone (only gce+tge, no design chain) or if GCE/TGE are in `provisioningSource[]` with `role: provisioning-source` → NOT pending (already correct).

**Transform.**
1. **Convert to provisioning source:** move `ai-gce` and `ai-tge` from `packages[]` to `provisioningSource[]` in the manifest (add `role: provisioning-source`).
2. **Strip routing rows from the orchestrator:** remove `_GCE_`/`_TGE_` activation rows + detection/path-map rows matching `ai-(gce|tge)-rules` from the deployed orchestrator. Insert the "Layer-3 companions staged inert" note (marker-guarded `AIFLC-COMPANION-NOTE`).
3. **Inform about provisioning:** display guidance: "AI-GCE and AI-TGE are now staged as provisioning sources. When you next run `_DWG_` (or re-run DWG in reconciliation mode), answer Q3 = Yes to provision them into your project workspace. Or install the `governance` bundle directly into an existing project repo."
4. **Non-destructive on existing outputs:** never delete or move any `.governance/`, `.kiro/hooks/`, or `.tge/` content the user already generated. Those are the team's outputs. This migration only adjusts the **package presence + routing**, not any derived governance artifacts.

**Idempotency.** If `packages[]` does not contain `ai-gce`/`ai-tge` (already in `provisioningSource[]` or absent), migration is not pending. If the orchestrator already lacks the companion rows, skip step 2.

**Ownership handling.** The manifest is `[gen]` (apply directly). The orchestrator is `[hyb]` (preview + confirm before stripping rows). User's `.governance/` content is never touched (`[user]` — skip).

---

## M6 — Automation-LENS `automationFeature` tag support

**Feature.** Artifacts produced by Automation-LENS-aware packages carry `automationFeature` front-matter tags (per `AUTOMATION_LENS_PROTOCOL.md` §4) so automated features are threaded across the lifecycle and discoverable by `DAT__`.

**Applies to.** Packages that produce artifacts which can be automation-tagged: AI-ILC (Idea Brief), AI-PILC (PIP + Decision_Log), AI-POLC (epics/stories), AI-UXD (UXP control designs), AI-ADLC (ADRs + component designs), AI-DWG (generated workspace + `.automation-lens/manifest.json`).

**Detection (is it pending?).** Check whether the workspace's `management_framework/Lens_Status.md` contains an Automation row (or, legacy, a `Decision_Log` row with "Automation Lens" / "Automation mode" in the Decision column). If no automation-mode record exists AND the project has automation features (any `automationFeature: true` front-matter in `backlog/epics/` or a `.automation-lens/manifest.json`), the mode was never formally captured → **M6 is pending** for PILC. For POLC: check `backlog/epics/*.md` for epics with automation-related content but missing `automationFeature` front-matter → pending. For DWG: check whether `.automation-lens/manifest.json` exists in the generated workspace → if absent and automation features exist upstream → pending.

**Transform.**
1. **PILC:** Append an Automation-LENS mode `Decision_Log` row (ask user: Manual / Automated + sub-modes) AND upsert the `Lens_Status.md` Automation row (dual-write per `LENS_STATUS_MECHANISM.md`). ID format: `PILC-{ABBREV}-D-{N}`.
2. **POLC:** For each epic/story identified as automation-relevant, add `automationFeature: true` + `automationMode` + `automationPattern` + `automationTrigger` + `automationFeatureId: AUTO-{NNN}` to front-matter (confirm each with user). Add `## Automation Acceptance Criteria` section + intent-level `requires`/`provides`.
3. **DWG:** Generate `.automation-lens/manifest.json` (incl. the guards block) with the couriered context from the tagged artifacts.
4. **ILC/UXD/ADLC:** Add front-matter tags to relevant artifacts where missing.

**Idempotency.** Artifacts already carrying `automationFeature: true` with a valid `automationFeatureId` are skipped. Decision_Log rows are append-only; `Lens_Status.md` rows are upserted (one per lens).

**Ownership handling.** Decision_Log + Lens_Status are `[gen]`/`[hyb]` spine files (append/upsert, preview on hybrid). Epic/story front-matter is `[hyb]` (preview + confirm). User-locked artifacts are skipped.

---

## M7 — Automation-LENS `data-schema/` automation fields + `Lens_Status.md`

**Feature.** Each package's `data-schema/` includes an `automationLens` sub-object so AI-DFE's existing `DAT__` can gather the automation-feature thread into the traceability JSON (per `AUTOMATION_LENS_PROTOCOL.md` §6.2). Additionally, the workspace spine gains `management_framework/Lens_Status.md` — the live current-mode SSOT for all lenses (per `LENS_STATUS_MECHANISM.md`).

**Applies to.** All 8 lens-aware packages: AI-ILC, AI-PILC, AI-POLC, AI-UXD, AI-ADLC, AI-DWG, AI-GCE, AI-TGE. The `Lens_Status.md` part applies once per workspace (spine-level).

**Detection (is it pending?).**
1. For each installed package, read `{pkg}-data.schema.json` and check for an `"automationLens"` key in `data.properties`. If absent → **M7 is pending** for that package.
2. Check `management_framework/` for `Lens_Status.md`. If absent AND any lens mode row exists in `Decision_Log` → the live SSOT was never created → **M7 (Lens_Status part) is pending**.

**Transform.**
1. Add the `automationLens` sub-object to `data.properties` in the schema JSON, matching the fields defined in `AUTOMATION_LENS_PROTOCOL.md` §6.2 for that package. Append the Automation-LENS extraction rules to `SOURCE_MAP.md`.
2. If `Lens_Status.md` is absent: create it (per `LENS_STATUS_MECHANISM.md` §3 template) and seed it from the latest lens-mode rows in `Decision_Log` (one row per lens found — AI-LENS and/or Automation). Also update the AI-PILC `SOURCE_MAP.md` mode-extraction rule to read `Lens_Status.md` rather than scanning `Decision_Log`.

**Idempotency.** If `"automationLens"` already exists in the schema, skip (key-presence check, forward-compatible). If `Lens_Status.md` already exists, do not overwrite — reconcile only if a mode row is missing.

**Ownership handling.** Schema + SOURCE_MAP are `[gen]` (apply directly). `Lens_Status.md` is `[hyb]` (create-if-absent; never overwrite existing state).

---

## M8 — Agentic intersection-facet support (derived `agenticProfile`)

**Feature.** A feature that both *reasons with a model* (AI Lens) **and** *acts across multiple steps on its own* (Automation Lens) is an **autonomous agent** — the intersection of the two lenses (NOT a third lens). Such a feature carries a **derived** `agenticProfile: true` marker and gains agentic guidance across the chain: an opportunity scan (POLC), agent architecture (ADLC), agent-interaction UX (UXD), agent-framework provisioning (DWG), and agentic checks in the existing governance/quality agents. The marker is a shadow of the two lens tags — it carries **no** `agenticFeatureId` and dissolves automatically if either lens tag drops below threshold.

**Applies to.** Co-tagged features in the lens-aware packages: AI-ILC (Idea Brief posture), AI-PILC (agent feasibility), AI-POLC (opportunity scan + agentic acceptance criteria), AI-UXD (agent-interaction design), AI-ADLC (agent architecture), AI-DWG (agent-framework provisioning + manifest block).

**Detection (is it pending?).**
- **POLC:** a feature in `backlog/epics/*.md` carries **both** `aiFeature: true` (`aiSubMode` ∈ {augmented, native}) **and** `automationFeature: true` (`automationMode` ∈ {attended, unattended}) but lacks the derived `agenticProfile: true` marker → **M8 is pending** for POLC.
- **DWG:** a feature entry in `.ai-lens/manifest.json` / `.automation-lens/manifest.json` qualifies as agentic (both tags at threshold) but the entry lacks the `agentic` block → pending.

**Transform.**
1. **POLC:** for each co-tagged feature at threshold, confirm with the user, then stamp `agenticProfile: true` (derived shadow — never an `agenticFeatureId`) and add an `## Agentic Acceptance Criteria` section (autonomy scope · tool inventory at intent level · task-completion definition · escalation path). Combinations below threshold are opt-in only, never auto-stamped.
2. **DWG:** augment **both** manifests with the derived `agentic` block for qualifying features (tool registry + permissions, loop termination + cost ceiling, reasoning-trace requirement, kill-switch reuse, memory) — no new manifest is created.
3. **ADLC / UXD:** where an architecture or interaction design exists for a co-tagged feature, the agentic facet guidance becomes available (additive — the agent-framework architecture + agent-interaction UX). No rewrite of existing lens content.

**Idempotency.** Features already carrying `agenticProfile: true` with both lens ids present are skipped. The marker is **derived**, never authored where both tags are not present; it dissolves automatically if either tag is later removed. Check for both-tags-at-threshold + marker consistency; skip if consistent.

**Ownership handling.** Epic/story front-matter + acceptance criteria are `[hyb]` (preview + confirm). Manifests are `[gen]` (apply directly). User-locked artifacts are skipped. The derived marker is never stamped where the two lens tags are not both present at threshold.

---

## M9 — Workspace HTML publishing (browsable shadow site)

**Feature.** The workspace can be published to a browsable, self-contained HTML **shadow** — one page per `.md` (diagrams, tables, and cross-links intact) plus a grouped landing page in reading order — via the `AIFLC-HtmlExport` tool and the `HTM__` trigger. The HTML is a read-only shadow; the `.md` files stay the single source of truth (SSOT-Shadow, INV-L4-011). This migration makes a workspace built before the feature existed aware of it and bootstraps the shadow + config idempotently.

**Applies to.** The **workspace as a whole** (tool-level, not package-specific) — available once any PDLC package is installed. Presented once per workspace, not per package.

**Detection (is it pending?).** Inspect the workspace root:
- Is `.publish/pdlc-html/index.html` absent AND `.publish/pdlc.config.yaml` absent?
- AND does the workspace contain publishable `pdlc-ws/` artifacts (any in-scope `.md`)?
- If both conditions hold → the publishing shadow was never initialized → **M9 is pending**.
- If either the shadow or the config already exists → NOT pending (already initialized; `HTM__` refreshes it on demand).

**Transform.** Non-destructive and one-directional (`.md → .html` only — never writes `.md`):
1. Confirm the `AIFLC-HtmlExport` tool is present under `tools/extensions/` (shipped via `EXTENSIONS_MANIFEST.md`). If absent, report and skip.
2. Run `HTM__` (equivalently `python tools/extensions/AIFLC-HtmlExport/publish.py pdlc-ws`) to bootstrap `.publish/pdlc.config.yaml` with family-correct defaults and build the shadow + landing page.
3. Report the page count and output location. Do not modify any `.md`.

**Idempotency.** `HTM__` is fully idempotent — every run rebuilds the shadow from the current Markdown. Once the config/shadow exist, detection reports not-pending, so re-running the migration is a safe no-op (beyond an optional refresh).

**Ownership handling.** The shadow (`.publish/pdlc-html/`) is `[gen]` — tool-owned and disposable, apply directly. `.publish/pdlc.config.yaml` is `[hyb]` — create-if-absent, never overwrite user edits. No `pdlc-ws/` `.md` source is ever touched (SSOT-Shadow).

---

## Adding a future migration

1. Add a row to the **Migration index** and a full section (Feature · Applies to · Detection · Transform · Idempotency · Ownership handling).
2. Detection MUST inspect the artifact — never rely solely on a version number.
3. Transform MUST be idempotent and expressed as platform-neutral markdown edits.
4. No change to `UPG__` itself is needed — the agent reads this catalogue at run time.

---

*PDLC Migration Catalogue · read by the `UPG__` family upgrade agent · Author: Maheri*
