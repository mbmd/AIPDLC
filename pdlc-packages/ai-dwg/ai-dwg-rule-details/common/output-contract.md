<!-- Internal detail file — loaded on-demand by AI-DWG dispatcher. -->
# AI-DWG Output Contract & Directory Structure

> **Load this file** when executing any generation/reconciliation mode, or when verifying output completeness. This carries the full guaranteed-output table and the runtime directory structure that AI-GCE depends on.

---

## Guaranteed Output (AI-GCE Can Depend On These Existing)

Scoped by present inputs. The successor (AI-GCE) can always find these relative to the dev-workspace root.

| Path | Content | Present When |
|------|---------|:------------:|
| `rules/workspace-rules.md` | Core rules + identity + Project ID (correlation key) | Always (minimal version even with single input) |
| `rules/` core tech steering — `architecture-principles`, `tech-stack`, `coding-standards`, `security-rules`, `api-standards`, `module-structure`, `testing-strategy` (unless TGE activated), `database-rules`, `naming-conventions`, `git-workflow`, `error-handling`, `observability-logging`, `observability-sensitive` | Per-file rules + conventions | IF ADLC |
| `rules/design-system.md` | Design tokens + component rules | IF UXD |
| `rules/frontend-standards.md` | UI patterns + a11y | IF UXD or ADLC (UI containers) |
| `rules/` UX steering — `navigation-structure`, `design-qa`, `content-guidelines`, `theming`, `i18n-standards` | Routes/taxonomy, drift rules, voice/tone, multi-brand, locales | IF UXD (respective artefact present) |
| `rules/[conditional files]` | Pattern-specific rules (multi-tenancy, api-versioning, resilience, tracing, performance, workflow-engine, event-sourcing, feature-flags, brownfield-patterns) | Depends on AP content |
| `info/vision.md` | AI-DLC v1 Vision Document | IF POLC |
| `architecture/technical-environment.md` | AI-DLC v1 Technical Environment Document | IF ADLC |
| `architecture/constraint-register.md` | Full architecture constraint set (hard + derived) | IF ADLC |
| `architecture/architecture-decision-records.md` | ADR register with rationale | IF ADLC |
| `ux/ui-implementation-spec.md` | AI-DLC v1 UI Implementation Spec | IF UXD |
| `ux/wireframes/` | Per-screen wireframe specifications | IF UXD (wireframes present) |
| `ux/user-flows/` | Multi-step interaction choreography | IF UXD (user flows present) |
| `ux/personas/` | User profiles for implementation context | IF UXD (personas present) |
| `ux/journey-maps/` | End-to-end experience maps | IF UXD (journey maps present) |
| `backlog/traceability-matrix.md` · `backlog/value-metrics.md` · `backlog/epics-and-backlog.md` + `backlog/epics/` | Traceability matrix · KPI register · prioritized epic/backlog scaffold + full story files (if Tier 2) | IF POLC (respective artefact present) |
| `backlog/user-stories.md` + `examples/acceptance/` | INVEST story index + G/W/T skeletons | IF POLC Tier 2 |
| `backlog/DEFINITION_OF_DONE.md` | Quality criteria | IF POLC or ADLC |
| `backlog/DEFINITION_OF_READY.md` | Sprint entry gate criteria | IF POLC |
| `backlog/scope-and-risks.md` | Scope definition + risk register | IF POLC |
| `backlog/po-charter.md` | Product Owner authority/escalation reference | IF POLC |
| `backlog/prioritization-register.md` | Build order rationale | IF POLC |
| `CODEOWNERS` | Module ownership | IF ADLC |
| `WORKSPACE_CONTEXT_MAP.md` | Root discovery index (pointers to all areas) | Always |
| `backlog/README.md` · `ux/README.md` · `architecture/README.md` | Folder-level context indexes | IF respective cluster present |
| `rules/relevance-map.md` | Code-area → reference-artifact mapping | IF ADLC + (POLC or UXD) |
| `.governance/workspace-manifest.yaml` | Discovery contract — consumers read paths by role | Always |
| Per-document baseline stamp (first line of every carried file) | Approach C: `v{N} (confirmed v{M})` | Always |
| Baseline archive (planning side) | `baselines/v{N}/baseline-manifest.yaml` + `snapshot-meta.yaml` | Always (planning workspace) |

> After generation or reconciliation, DWG signals AI-GCE (`workspace-generated` / `steering-files-updated`). The full DOWNSTREAM SIGNAL formats (Mode 1 + Mode 2), signal-delivery model, and when-to-signal rules live in `reconciliation/downstream-signaling.md`.

---

## Contract Principles

| Principle | Implementation |
|-----------|---------------|
| **Detection by marker, not by path** | Look for `adlc-state.md` / `polc-state.md` / `uxd-state.md`, not for `./architecture/` |
| **Fixed output root** | Dev workspace generated at `{project_root}/{slug}-workspace/`; package defines WHAT files exist |
| **Peer-input, no master** | {ADLC, POLC, UXD} are equal. Any non-empty subset is valid. None dominates. Missing inputs = skipped clusters + quality-impact disclosure |
| **Per-cluster generation** | Each output traces to exactly one input cluster. Absent input → cluster skipped, reported. Present input → cluster generated in full |
| **Quality-impact disclosure** | Missing inputs MUST be disclosed with downstream impact. User MUST explicitly approve reduced coverage before DWG proceeds |
| **Cross-repo support** | Peer inputs can be in different folders, drives, or repos — just point to them |
| **Format tolerance** | Support both numbered (`01_Architecture_Vision.md`) and phase-folder (`foundation/`) structures for ADLC |
| **Standalone capable** | Works without AI-ADLC state file if user provides equivalent markdown docs manually |
| **Conflict = anomaly** | ADLC, POLC, UXD are designed not to overlap. If overlap detected: DWG provides root-cause analysis + suggested correction → user resolves. DWG does NOT proceed until resolved |

---

## Directory Structure — AI-DWG Output (Runtime)

When AI-DWG completes, this structure exists in the generated dev workspace (maximum output shown — all three peer inputs present; conditional artifacts in `[brackets]`):

```
{workspace-root}/
├── .kiro/
│   └── steering/                                 ← Kiro platform adapter (includes from rules/)
│       └── (fileMatch + always-include wiring to rules/)
│
├── rules/                                        ← AI rules (canonical, platform-neutral)
│   ├── workspace-rules.md                        ← ALWAYS (identity adapts to present inputs)
│   ├── architecture-principles.md                ← IF ADLC
│   ├── tech-stack.md · coding-standards.md · naming-conventions.md   ← IF ADLC
│   ├── project-governance.md · session-governance.md · role-isolation.md  ← IF ADLC
│   ├── domain-context.md · module-structure.md                       ← IF ADLC
│   ├── api-standards.md · security-rules.md · database-rules.md      ← IF ADLC
│   ├── testing-strategy.md · error-handling.md                       ← IF ADLC
│   ├── observability-logging.md · observability-sensitive.md · git-workflow.md  ← IF ADLC
│   ├── design-system.md                          ← IF UXD
│   ├── [frontend-standards.md]                   ← IF UXD or ADLC (UI containers)
│   ├── [navigation-structure · design-qa · content-guidelines · theming · i18n-standards]  ← conditional (UXD)
│   ├── [multi-tenancy · api-versioning · resilience-standards · observability-tracing ·
│   │    performance-standards · workflow-engine · event-sourcing · feature-flags ·
│   │    brownfield-patterns]                     ← conditional (ADLC)
│   └── relevance-map.md                          ← Code-area → reference mapping (auto-generated)
│
├── info/                                         ← Operational guides for the team
│   ├── PROJECT_INSTRUCTIONS.md                   ← ALWAYS (master dev guide)
│   ├── CONTRIBUTING.md                           ← ALWAYS
│   ├── ONBOARDING.md                             ← ALWAYS
│   ├── CICD_GUIDE.md                             ← ALWAYS
│   ├── TEAM_AGREEMENTS.md                        ← ALWAYS
│   └── vision.md                                 ← IF POLC (+UXD personas/journeys)
│
├── architecture/                                 ← IF ADLC (reference material)
│   ├── technical-environment.md                  ← AI-DLC v1 Technical Environment Document
│   ├── constraint-register.md                   ← Full constraint set (hard + derived)
│   ├── architecture-decision-records.md         ← ADR register with rationale
│   └── docker-compose.yml                       ← Infrastructure config
│
├── backlog/                                      ← IF POLC
│   ├── README.md                                ← Folder-level context index
│   ├── epics-and-backlog.md                     ← Prioritized epic/backlog scaffold
│   ├── DEFINITION_OF_DONE.md                    ← Quality criteria
│   ├── DEFINITION_OF_READY.md                   ← Sprint entry gate
│   ├── scope-and-risks.md                       ← Scope definition + risk register
│   ├── traceability-matrix.md                   ← Requirements traceability
│   ├── value-metrics.md                         ← KPI register
│   ├── user-stories.md                          ← Story index/entry-point (if Tier 2)
│   ├── po-charter.md                            ← PO authority/escalation reference
│   ├── prioritization-register.md               ← Build order rationale
│   └── epics/                                   ← IF POLC Tier 2 (full story files)
│       ├── EPIC-001_*.md
│       ├── EPIC-001_stories/
│       └── ...
│
├── ux/                                           ← IF UXD (reference material)
│   ├── README.md                                ← Folder-level context index
│   ├── ui-implementation-spec.md                ← AI-DLC v1 UI Implementation Spec
│   ├── wireframes/                              ← Per-screen wireframe specs (if present)
│   ├── user-flows/                              ← Multi-step interaction flows (if present)
│   ├── personas/                                ← User profiles (if present)
│   └── journey-maps/                            ← End-to-end experience maps (if present)
│
├── README.md                                     ← Git convention + master pointer
├── CONTRIBUTING.md                               ← Git convention
├── CODEOWNERS                                    ← IF ADLC
├── WORKSPACE_CONTEXT_MAP.md                      ← Discovery index (auto-regenerated)
├── .github/pull_request_template.md              ← ALWAYS
├── examples/                                     ← skeleton patterns
├── aidlc-rules/extensions/                       ← AI-DLC v1 extension rules bundle
├── templates/                                    ← session-planning · sprint-planning · estimation-guide
├── .gitignore · .editorconfig                    ← IF ADLC
├── management_framework/                         ← Shared governance spine (active — GCE appends)
│   └── MANAGEMENT_FRAMEWORK.md · Decision_Log.md · Change_Log.md · Issue_Log.md · Lessons_Learned.md
├── .governance/                                  ← DWG/GCE runtime
│   ├── baseline-manifest.yaml
│   ├── drift-register.md
│   └── agents/
└── {src-structure}/                              ← IF ADLC (C4 L3 derived)
```
