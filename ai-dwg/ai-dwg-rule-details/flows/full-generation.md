<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mode 1 — Full Generation Flow

## Purpose

The step-by-step orchestration for **Mode 1: Full Generation** — composing a complete development workspace from the present peer inputs in one pass. The core (`core-generator.md`) carries the Mode 1 intent + configuration questions; this file carries the detailed flow scaffolding and the literal output summary. Load it when Mode 1 is detected (after the pre-mode gate in `flows/input-selection-and-conflict.md` passes).

> Pipeline summary, per-cluster output inventory, and the mapping-file index live in `common/process-overview.md`. AP/PBP/UXP reading detail lives in `common/ap-reading-guide.md`. Cross-check rules live in `common/validation-rules.md`. Per-transformation rules live in `mapping/*.md`.

---

## Interaction Model

1. **User invokes:** "Generate the development workspace from my design packages" (or specifies specific inputs)
2. **AI detects** which peer inputs are available (scans for marker files)
3. **AI discloses** quality impact of any absent inputs; user approves coverage level (pre-mode gate)
4. **AI reads** all present peer inputs (AP, PBP, UXP — whichever markers were found)
5. **AI asks** 2-4 configuration questions (see core)
6. **AI generates** all files for present clusters in one pass
7. **AI presents** summary with file inventory
8. **User verifies** — done

---

## Full Generation Flow

```
STEP 1: DETECT & READ — Locate Peer Inputs and Load Present Packages
─────────────────────────────────────────────────────────────────────
Scan for marker files (adlc-state.md, polc-state.md, uxd-state.md).
At least ONE must be found — if zero, ask user.
If fewer than 3 found → quality-impact disclosure → user approves.

For EACH present input, load its package artifacts. Parse each for:
• Explicit decisions (what was chosen)
• Constraints (what is NOT allowed)
• Patterns (how things should be done)
• Names (technology labels, module names, entity names)
• Quality attributes (what defines "good")

For reading rules, load: common/ap-reading-guide.md

STEP 2: MAP — Transform Each Present Input → Workspace Artifacts (Per-Cluster)
───────────────────────────────────────────────────────────────────────────────
Generate ONLY the clusters whose input is present.

IF ADLC present — load tech-cluster mappings:
• mapping/vision-to-workspace-rules.md
• mapping/techstack-to-config.md
• mapping/components-to-structure.md
• mapping/components-to-domain-context.md
• mapping/security-to-steering.md
• mapping/api-to-steering.md
• mapping/data-to-steering.md
• mapping/tenancy-to-steering.md          (conditional)
• mapping/infra-to-config.md
• mapping/infra-to-cicd.md
• mapping/infra-to-observability.md
• mapping/components-to-error-handling.md
• mapping/integration-to-resilience.md    (conditional)
• mapping/quality-to-performance.md       (conditional)
• mapping/containers-to-frontend.md       (conditional)
• mapping/brownfield-to-steering.md       (conditional — brownfield mode)

IF POLC present — load product-cluster mappings:
• mapping/polc-uxd-to-vision-document.md  (+ UXD personas/journeys if UXD also present)
• mapping/quality-to-dod.md
• mapping/team-to-agreements.md
• mapping/governance-derivation.md
• mapping/polc-to-traceability.md          (conditional — PBP has traceability artefact)
• mapping/polc-to-value-metrics.md         (conditional — PBP has value/KPI artefact)
• mapping/polc-to-epics-backlog.md         (conditional — PBP has epic decomposition)
• mapping/polc-to-user-stories.md          (conditional — POLC Tier 2 stories activated)

IF UXD present — load UX-cluster mappings:
• mapping/uxd-to-design-system.md
• mapping/containers-to-frontend.md       (UXD frontend patterns overlay)
• mapping/ap-uxp-to-tech-environment.md   (UXD frontend section — if ADLC also present)
• mapping/uxd-to-information-architecture.md (conditional — UXP has IA artefact)
• mapping/uxd-to-design-qa.md              (conditional — UXP has Design QA framework)
• mapping/uxd-to-voice-tone.md             (conditional — UXP has voice & tone)
• mapping/uxd-to-theming.md                (conditional — UXP multi-brand/color-mode)
• mapping/uxd-to-i18n.md                   (conditional — UXP i18n/RTL/multi-locale)

Extension-enrichment mappings (loaded IF ADLC present AND extensions were active):
• mapping/extension-ddd-enrichment.md          (if DDD Tactical active)
• mapping/extension-microservices-enrichment.md (if Microservices active)
• mapping/extension-eventsourcing-enrichment.md (if Event Sourcing/CQRS active)
• mapping/extension-featureflags-enrichment.md  (if Feature Flags active)

STEP 3: GENERATE — Produce Files for Present Clusters
──────────────────────────────────────────────────────
Generate files using templates from: templates/
Only produce output for clusters whose input is present:

IF ADLC present:
• Tech steering files (13+ always when ADLC present + conditionals) → .kiro/steering/
• technical-environment.md → project root
• Config files → project root
• Folder structure → {src-structure}/

IF POLC present:
• vision.md → project root (enriched with UXD personas if UXD also present)
• DEFINITION_OF_DONE.md → project root
• Planning templates (3 files) → templates/
• scope-and-risks.md → .kiro/steering/
• traceability-matrix.md → project root          (IF PBP has traceability)
• value-metrics.md → project root                (IF PBP has value/KPIs; relays KPIs to observability if ADLC present)
• epics-and-backlog.md + backlog/EPIC-*.md       (IF PBP has epic decomposition)
• user-stories.md + examples/acceptance/*.feature.md (IF POLC Tier 2 stories activated)

IF UXD present:
• design-system.md → .kiro/steering/
• frontend-standards.md → .kiro/steering/
• ui-implementation-spec.md → project root
• Accessibility baseline relay → signaled to AI-GCE
• navigation-structure.md → .kiro/steering/       (IF UXP has IA)
• design-qa.md → .kiro/steering/ + relay to AI-GCE (IF UXP has Design QA framework)
• content-guidelines.md → .kiro/steering/         (IF UXP has voice & tone)
• theming.md → .kiro/steering/                    (IF UXP multi-brand/color-mode)
• i18n-standards.md → .kiro/steering/             (IF UXP i18n/RTL/multi-locale)

ALWAYS (regardless of which inputs):
• Operational docs (PROJECT_INSTRUCTIONS, CONTRIBUTING, ONBOARDING, etc.) → project root
• PR template → .github/

IMPORTANT: Generated content must be POPULATED, not placeholders.
Steering files derive actual rules from input decisions.
The output is ready-to-use, not fill-in-the-blank.

STEP 4: VALIDATE — Cross-Check Against Present Inputs
──────────────────────────────────────────────────────
Load: common/validation-rules.md

Verify (scoped to present inputs only):
• IF ADLC: All AP principles encoded in at least one steering file
• IF ADLC: All AP constraints reflected as rules (DO NOT / NEVER statements)
• IF ADLC: Folder structure matches C4 L3 module decomposition
• IF ADLC: Technology labels consistent across all generated files
• IF POLC: Vision document contains all PBP-sourced sections
• IF UXD: Design system covers all UXP-provided tokens/patterns
• No contradictions between generated steering files
• Conditional files generated ONLY when input justifies them
• Every generated rule is traceable to a specific input artifact
• Quality-impact disclosure was presented for absent inputs
• No cross-cluster contradictions (if multiple inputs present)

STEP 5: OUTPUT — Present Summary
────────────────────────────────
Present generation results:

"✅ AI-DWG GENERATION COMPLETE

📦 Workspace generated for: {system_name}
📁 Location: {workspace_root}

📊 Summary:
   • Steering files generated: {n} (of which {m} conditional)
   • Operational documents: {n}
   • Planning templates: {n}
   • Config files: {n}
   • Source folders created: {n} modules

📋 Conditional files generated:
   • {file}: because AP contains {justification}
   • ...

📋 Conditional files SKIPPED:
   • {file}: because AP does NOT contain {reason}
   • ...

🔗 Next steps:
   1. Review generated steering files for team-specific adjustments
   2. Run AI-GCE to derive compliance enforcement (hooks + rules)
   3. Begin AI-DLC v1 workflow with user stories

🔀 **Chain Navigation (what's next in the AI-* Family):**
   • Sequential next: **AI-GCE** (`_GCE_`) — Governance & Compliance Engine
   • Alongside: **AI-TGE** (`_TGE_`) — Test Governance (runs parallel with GCE)
   • Or ask AI-FLO: type `_FLO_` for routing guidance based on your project state
   • Dashboard data: type `DAT__ pdlc/dwg` to update the family dashboard

⚠️ **IMPORTANT: Start the next package (AI-GCE) in a NEW session.**
   Each AI-* package loads a full workflow into context;
   a fresh session keeps it fast and focused.

The workspace is ready for development."
```

---

## Configuration Questions (Asked Once)

Before generating, ask these 2-4 questions:

| # | Question | Purpose | Default |
|---|----------|---------|---------|
| 1 | What is the workspace root path? | Where to generate output | `./` (current directory) |
| 2 | Project display name? | Used in README, PROJECT_INSTRUCTIONS | Derived from AP system name |
| 3 | Team size (approximate)? | Affects operational doc depth (review standards, ownership model) | Medium (4-8) |
| 4 | Target Kiro autonomy mode? | Influences session-governance steering content | Autopilot |

**Do NOT ask about:** Technology (already in AP if ADLC present), architecture patterns (already decided), folder structure (derived from C4 L3 if ADLC present), which inputs to use (detect by marker — ask only if zero markers found). The entire point is: the peer inputs already contain the answers.

---

## Error Handling (Cross-Mode)

Applies to all modes; surfaced here as the primary generation flow.

| Situation | Response |
|-----------|----------|
| AP artifact missing (required) | Flag gap. Ask user: "Generate with assumptions?" or "Wait for artifact?" |
| AP artifact incomplete | Generate what's possible. Mark generated sections with `<!-- partial: {what's missing} -->` |
| Conflicting AP decisions | Flag contradiction. Ask user to resolve before generating affected steering file. |
| Workspace already exists (Mode 1 requested) | Warn: "Workspace exists. (a) Overwrite? (b) Switch to reconciliation mode? (c) Cancel?" |
| Reconciliation conflict | Present both versions (AP-derived vs. current). User picks. |
| Unknown technology in AP | Generate generic patterns. Mark with `<!-- customize: technology-specific rules needed -->` |

---

*Mode 1 flow — loaded by `core-generator.md` when Full Generation is detected.*
