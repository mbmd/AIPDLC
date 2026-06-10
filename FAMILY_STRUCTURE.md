# AI-* Family — Complete Package & Output Structure

**Version:** 1.0.0
**Date:** 2026-06-06
**Author:** Maheri

---

## The AI-* Family

```
╔════════════════ PORTFOLIO LAYER · scope = MANY projects ════════════════╗

   (optional)
    AI-ILC  ⇢  AI-PILC  ⇢  AI-PPM
    Decide it   Initiate it   Govern it (portfolio of N projects)

╚═════════════════════════════════╤═══════════════════════════════════════╝
                                   │
                                AI-FLO   Route it — package-to-package
                                   │     flow on the edge between layers
╔════════════════ PROJECT LAYER · scope = ONE project ════════════════════╗

    AI-ADLC ──┐                                                
    Design it │                                                
              ├──►  AI-DWG  ──►  AI-DLC (build) ¹              
    AI-POG ───┘     Prepare it       ▲                          
    Own it      └───────────────────┘  AI-POG ⇄ AI-DLC (back-and-forth)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | (Requirements + Charter) / PIP | Architecture Package (AP) |
| Project | **AI-POG** ³ | Interactive workflow (lifecycle) | PIP and/or AP | Product Backlog Package (PBP) |
| Project | **AI-DWG** | One-time generator | AP + PBP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POG) | Working Software |

> ¹ **AI-DLC** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ **AI-PPM**, **AI-FLO**, and **AI-POG** are **new and pending build**. AI-PPM (portfolio engine) and AI-FLO (router) are registered as ideas; AI-POG (product ownership lifecycle) is idea 006. Within the Project layer, **AI-ADLC and AI-POG run in parallel and both feed AI-DWG**; **AI-GCE and AI-TGE run alongside AI-DLC** as continuous quality engines; and **AI-POG ⇄ AI-DLC** exchange backlog/acceptance throughout delivery.

---

## Naming & Ownership Convention

All file naming and provenance across the family follows one ratified convention:

> **See `ai-packages/NAMING_AND_OWNERSHIP.md` (the source of truth).**

**The A-dominant hybrid in one paragraph:** every generated `.md` artifact carries a provenance front-matter block (`generated-by`, `source`, `ownership: generated|hybrid|user`); hooks carry a `generatedBy` field. Filenames stay generic so artifacts read as the team's own — except *tool-owned* files, which are separated by **folder** (`.governance/`, `.kiro/hooks/`), never by filename prefix. Chain **marker files** (`pilc-state.md`, `adlc-state.md`, `workspace-rules.md`, the `.kiro/hooks/` folder) keep their exact names — renaming them breaks detection (Lesson 14).

**Ownership legend** (used to annotate PART 2 below):

| Marker | Meaning |
|--------|---------|
| `[gen]` | Tool-generated; re-derivation may overwrite (`ownership: generated`) |
| `[hyb]` | Tool-seeded, team-edited; `<!-- custom -->` content preserved on re-derivation (`ownership: hybrid`) |
| `[tool]` | Tool-owned, in a dedicated folder; not hand-edited |
| `[marker]` | Chain detection anchor — name is non-negotiable |

---

## PART 1: Package Source Structure (What We Build & Publish)

```
ai-packages/
│
├── ai-pilc/                                    ← AI-Driven Project Initiation Life Cycle
│   ├── README.md
│   ├── LICENSE
│   ├── ai-pilc-rules/
│   │   └── core-workflow.md                    ← Master orchestration
│   ├── ai-pilc-rule-details/
│   │   ├── common/
│   │   │   ├── process-overview.md
│   │   │   ├── session-continuity.md
│   │   │   ├── question-format-guide.md
│   │   │   ├── content-validation.md
│   │   │   └── welcome-message.md
│   │   ├── inception/                          ← Phase 1 stages
│   │   │   ├── workspace-detection.md
│   │   │   ├── source-ingestion.md
│   │   │   └── requirement-structuring.md
│   │   ├── assessment/                         ← Phase 2 stages
│   │   │   ├── requirements-analysis.md
│   │   │   ├── clarification-cycle.md
│   │   │   ├── feasibility-assessment.md
│   │   │   └── prioritization.md
│   │   ├── justification/                      ← Phase 3 stages
│   │   │   └── business-case.md
│   │   ├── authorization/                      ← Phase 4 stages
│   │   │   └── project-charter.md
│   │   ├── planning/                           ← Phase 5 stages
│   │   │   ├── stakeholder-management.md
│   │   │   ├── scope-definition.md
│   │   │   ├── resource-budget.md
│   │   │   ├── risk-management.md
│   │   │   └── governance-communication.md
│   │   ├── mobilization/                       ← Phase 6 stages
│   │   │   ├── kickoff-preparation.md
│   │   │   └── package-assembly.md
│   │   └── templates/
│   │       ├── requirement-intake-form.md
│   │       ├── feasibility-assessment.md
│   │       ├── business-case.md
│   │       ├── project-charter.md
│   │       ├── stakeholder-register.md
│   │       ├── scope-statement.md
│   │       ├── resource-plan.md
│   │       ├── risk-register.md
│   │       ├── raci-matrix.md
│   │       ├── kickoff-agenda.md
│   │       ├── decision-log.md
│   │       ├── change-log.md
│   │       ├── issue-log.md
│   │       ├── action-items.md
│   │       ├── assumptions-dependencies.md
│   │       └── lessons-learned.md
│   └── kiro-setup/
│       └── INSTALL.md
│
├── ai-adlc/                                    ← AI-Driven Architecture Design Life Cycle
│   ├── README.md
│   ├── LICENSE
│   ├── ROADMAP.md
│   ├── ai-adlc-rules/
│   │   └── core-workflow.md                    ← Master orchestration
│   ├── ai-adlc-rule-details/
│   │   ├── common/
│   │   │   ├── process-overview.md
│   │   │   ├── session-continuity.md
│   │   │   ├── question-format-guide.md
│   │   │   ├── content-validation.md
│   │   │   ├── diagram-standards.md
│   │   │   └── welcome-message.md
│   │   ├── foundation/                         ← Phase 1 stages
│   │   │   ├── workspace-detection.md
│   │   │   ├── requirements-ingestion.md
│   │   │   └── architecture-vision.md
│   │   ├── decomposition/                      ← Phase 2 stages
│   │   │   ├── system-context.md
│   │   │   └── container-design.md
│   │   ├── decisions/                          ← Phase 3 stages
│   │   │   ├── technology-stack.md
│   │   │   ├── multi-tenancy.md
│   │   │   └── security-identity.md
│   │   ├── design/                             ← Phase 4 stages
│   │   │   ├── data-architecture.md
│   │   │   ├── api-architecture.md
│   │   │   ├── integration-infrastructure.md
│   │   │   └── component-design.md
│   │   ├── assembly/                           ← Phase 5 stages
│   │   │   └── package-assembly.md
│   │   ├── templates/
│   │   │   ├── adr-template.md
│   │   │   ├── brownfield-strategy-adr.md
│   │   │   ├── architecture-vision.md
│   │   │   ├── system-context.md
│   │   │   ├── container-diagram.md
│   │   │   ├── technology-stack.md
│   │   │   ├── multi-tenancy.md
│   │   │   ├── security-architecture.md
│   │   │   ├── data-architecture.md
│   │   │   ├── api-architecture.md
│   │   │   ├── integration-architecture.md
│   │   │   ├── component-design.md
│   │   │   └── architecture-workbook.md
│   │   └── extensions/                         ← v1.1 opt-in patterns
│   │       ├── README.md
│   │       ├── ddd-tactical/
│   │       │   ├── ddd-tactical.opt-in.md
│   │       │   └── ddd-tactical.md
│   │       ├── microservices/
│   │       │   ├── microservices.opt-in.md
│   │       │   └── microservices.md
│   │       ├── bff-pattern/
│   │       │   ├── bff-pattern.opt-in.md
│   │       │   └── bff-pattern.md
│   │       ├── event-sourcing-cqrs/
│   │       │   ├── event-sourcing-cqrs.opt-in.md
│   │       │   └── event-sourcing-cqrs.md
│   │       ├── resilience-patterns/
│   │       │   ├── resilience-patterns.opt-in.md
│   │       │   └── resilience-patterns.md
│   │       └── feature-flags/
│   │           ├── feature-flags.opt-in.md
│   │           └── feature-flags.md
│   └── kiro-setup/
│       └── INSTALL.md
│
├── ai-dwg/                                     ← AI-Driven Workspace Generator
│   ├── README.md
│   ├── LICENSE
│   ├── PLAN.md
│   ├── ai-dwg-rules/
│   │   └── core-generator.md                   ← Master generation logic
│   ├── ai-dwg-rule-details/
│   │   ├── common/
│   │   │   ├── process-overview.md
│   │   │   ├── ap-reading-guide.md
│   │   │   └── validation-rules.md
│   │   ├── mapping/                            ← AP → Workspace transformation rules
│   │   │   ├── vision-to-workspace-rules.md
│   │   │   ├── techstack-to-config.md
│   │   │   ├── components-to-structure.md
│   │   │   ├── components-to-domain-context.md
│   │   │   ├── security-to-steering.md
│   │   │   ├── api-to-steering.md
│   │   │   ├── data-to-steering.md
│   │   │   ├── tenancy-to-steering.md
│   │   │   ├── infra-to-config.md
│   │   │   ├── infra-to-cicd.md
│   │   │   ├── infra-to-observability.md
│   │   │   ├── components-to-error-handling.md
│   │   │   ├── integration-to-resilience.md
│   │   │   ├── quality-to-performance.md
│   │   │   ├── containers-to-frontend.md
│   │   │   ├── governance-derivation.md
│   │   │   ├── quality-to-dod.md
│   │   │   ├── team-to-agreements.md
│   │   │   ├── extension-ddd-enrichment.md
│   │   │   ├── extension-microservices-enrichment.md
│   │   │   ├── extension-eventsourcing-enrichment.md
│   │   │   ├── extension-featureflags-enrichment.md
│   │   │   └── brownfield-to-steering.md
│   │   ├── reconciliation/                     ← Delta update logic
│   │   │   ├── diff-strategy.md
│   │   │   ├── merge-strategy.md
│   │   │   ├── provenance-tracking.md
│   │   │   └── downstream-signaling.md
│   │   └── templates/                          ← Generic templates for output
│   │       ├── steering/
│   │       │   ├── workspace-rules.md
│   │       │   ├── architecture-principles.md
│   │       │   ├── tech-stack.md
│   │       │   ├── coding-standards.md
│   │       │   ├── project-governance.md
│   │       │   ├── scope-and-risks.md
│   │       │   ├── session-governance.md
│   │       │   ├── role-isolation.md
│   │       │   ├── domain-context.md
│   │       │   ├── multi-tenancy.md
│   │       │   ├── api-standards.md
│   │       │   ├── api-versioning.md
│   │       │   ├── security-rules.md
│   │       │   ├── module-structure.md
│   │       │   ├── testing-strategy.md
│   │       │   ├── database-rules.md
│   │       │   ├── naming-conventions.md
│   │       │   ├── git-workflow.md
│   │       │   ├── error-handling.md
│   │       │   ├── resilience-standards.md
│   │       │   ├── observability-logging.md
│   │       │   ├── observability-tracing.md
│   │       │   ├── observability-sensitive.md
│   │       │   ├── performance-standards.md
│   │       │   ├── workflow-engine.md
│   │       │   ├── frontend-standards.md
│   │       │   ├── event-sourcing.md
│   │       │   ├── feature-flags.md
│   │       │   └── brownfield-patterns.md
│   │       ├── operational/
│   │       │   ├── project-instructions.md
│   │       │   ├── definition-of-done.md
│   │       │   ├── contributing.md
│   │       │   ├── cicd-guide.md
│   │       │   ├── team-agreements.md
│   │       │   ├── onboarding.md
│   │       │   └── pr-template.md
│   │       ├── planning/
│   │       │   ├── session-planning.md
│   │       │   ├── sprint-planning.md
│   │       │   └── estimation-guide.md
│   │       ├── config/
│   │       │   ├── readme-skeleton.md
│   │       │   ├── editorconfig.md
│   │       │   └── codeowners.md
│   │       └── docker-compose/
│   │           ├── node-typescript.md
│   │           ├── python-django.md
│   │           ├── dotnet.md
│   │           ├── java-spring.md
│   │           └── generic.md
│   └── kiro-setup/
│       └── INSTALL.md
│
└── ai-gce/                                     ← AI-Driven Governance & Compliance Engine
    ├── README.md
    ├── LICENSE
    ├── PLAN.md
    ├── ai-gce-rules/
    │   └── core-generator.md                   ← Master derivation logic (4 modes, tier model, two-source)
    ├── ai-gce-rule-details/
    │   ├── common/
    │   │   ├── process-overview.md
    │   │   ├── workspace-reading-guide.md
    │   │   ├── validation-rules.md
    │   │   ├── scoring-model.md
    │   │   └── knowledge-map-guide.md
    │   ├── generators/                         ← Derivation logic per output category (23 files)
    │   │   ├── --- ARCHITECTURAL ---
    │   │   ├── architecture-compliance-gen.md
    │   │   ├── api-compliance-generator.md
    │   │   ├── security-compliance-gen.md
    │   │   ├── data-governance-generator.md
    │   │   ├── module-boundary-generator.md
    │   │   ├── naming-generator.md
    │   │   ├── error-handling-generator.md
    │   │   ├── logging-generator.md
    │   │   ├── domain-context-generator.md
    │   │   ├── conditional-arch-generator.md   (covers tenant-isolation, resilience, tracing, etc.)
    │   │   ├── hooks-from-steering.md
    │   │   ├── --- NON-ARCHITECTURAL ---
    │   │   ├── phase-gates-generator.md
    │   │   ├── session-governance-generator.md
    │   │   ├── role-isolation-generator.md
    │   │   ├── team-topology-generator.md
    │   │   ├── sprint-governance-generator.md
    │   │   ├── pr-governance-generator.md
    │   │   ├── cicd-gates-generator.md
    │   │   ├── devops-generator.md
    │   │   ├── steering-governance-gen.md
    │   │   ├── compliance-log-gov-gen.md
    │   │   ├── change-management-gen.md
    │   │   └── mcp-governance-gen.md           (conditional)
    │   ├── re-derivation/                      ← Delta re-derivation logic
    │   │   ├── change-detection.md
    │   │   ├── selective-regeneration.md
    │   │   └── upstream-signaling.md
    │   └── templates/
    │       ├── hooks/                          ← 15 files (14 JSON + INSTALL-GUIDE)
    │       │   ├── session-discipline.json
    │       │   ├── pre-code-spec-check.json
    │       │   ├── api-contract-check.json
    │       │   ├── module-boundary-check.json
    │       │   ├── security-gate-check.json
    │       │   ├── naming-check.json
    │       │   ├── migration-safety.json
    │       │   ├── coverage-check.json
    │       │   ├── post-task-governance.json
    │       │   ├── pre-pr-checklist.json
    │       │   ├── periodic-audit.json
    │       │   ├── sensitive-data-check.json
    │       │   ├── domain-layer-purity.json
    │       │   ├── segregation-check.json
    │       │   └── INSTALL-GUIDE.md
    │       ├── agents/
    │       │   ├── compliance-audit-agent.md
    │       │   ├── project-init-agent.md
    │       │   └── compliance-readme.md
    │       ├── compliance-log/
    │       │   ├── compliance-log-schema.md
    │       │   ├── exception-workflow.md
    │       │   ├── remediation-workflow.md
    │       │   ├── brownfield-baseline.md
    │       │   ├── incremental-adoption-plan.md
    │       │   └── compliance-dashboard-template.md
    │       └── steering-templates/             ← Used by project-init-agent
    │           ├── 01-architecture-templates.md
    │           ├── 02-domain-templates.md
    │           ├── 03-security-templates.md
    │           ├── 04-error-resilience-templates.md
    │           ├── 05-observability-templates.md
    │           ├── 06-testing-templates.md
    │           ├── 07-api-versioning-templates.md
    │           ├── 08-frontend-templates.md
    │           ├── 09-multi-tenancy-templates.md
    │           ├── 10-event-sourcing-templates.md
    │           ├── 11-feature-flags-templates.md
    │           ├── 12-session-context-templates.md
    │           └── 13-brownfield-templates.md
    └── kiro-setup/
        └── INSTALL.md
```

---

## PART 2: Runtime Output Structure (What Each Package Produces When Run)

> **Ownership map** (per `NAMING_AND_OWNERSHIP.md`; legend defined above):
>
> | Package output | Default ownership | Notes |
> |---|---|---|
> | AI-PILC docs (`project-initiation/`) | `[hyb]` | Team owns and edits; `pilc-state.md` is `[marker]` |
> | AI-ADLC docs (`architecture/`) | `[hyb]` | Team owns and edits; `adlc-state.md` is `[marker]` |
> | AI-DWG steering (`.kiro/steering/*.md`) | `[hyb]` | Living team docs; `workspace-rules.md` is `[marker]` |
> | AI-DWG config (`.editorconfig`, `docker-compose.yml`, …) | `[gen]` | Regenerated; ecosystem-standard names |
> | AI-GCE hooks (`.kiro/hooks/*.kiro.hook`) | `[tool]` | Folder boundary; carry `generatedBy` |
> | AI-GCE rules (`.governance/rules/*.md`) | `[tool]` | Folder boundary; carry provenance front-matter |
> | AI-GCE steering enrichments (`compliance-*.md`) | `[hyb]` | `compliance-` namespace + front-matter |
>
> Every generated `.md` carries the front-matter block from `NAMING_AND_OWNERSHIP.md` §5.2; every hook carries the `generatedBy` field from §5.3.

When a user installs and runs these packages on their own project:

```
{user-project}/                                 ← The user's project workspace
│
│ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
│ 📦 AI-PILC OUTPUT — Project Initiation Package
│ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
│
├── project-initiation/                         ← User-chosen folder (or root)
│   ├── pilc-state.md                           ← Workflow state
│   ├── 01_Requirement_Intake_Form.md
│   ├── 02_Requirements_Analysis_Report.md
│   ├── 03_Clarification_Questionnaire.md      (conditional)
│   ├── 04_Feasibility_Assessment.md
│   ├── 05_Business_Case.md
│   ├── 06_Project_Charter.md
│   ├── 07_Stakeholder_Register.md
│   ├── 08_Scope_Statement.md
│   ├── 09_Resource_Plan.md
│   ├── 10_Risk_Register.md
│   ├── 11_RACI_Matrix.md
│   ├── 12_Kickoff_Agenda.md
│   └── PROJECT_INITIATION_PACKAGE_README.md    ← Final assembled PIP (summary + reading guide)
│
│ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
│ 📦 AI-ADLC OUTPUT — Architecture Package
│ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
│
├── architecture/                               ← User-chosen folder (or root)
│   ├── adlc-state.md                           ← Workflow state + extension tracking
│   ├── Architecture_Workbook.md                ← Living decisions tracker
│   ├── 01_Architecture_Vision.md
│   ├── 02_System_Context_C4L1.md
│   ├── 03_Container_Diagram_C4L2.md
│   ├── 04_Technology_Stack.md
│   ├── 05_MultiTenancy_Architecture.md         (conditional)
│   ├── 06_Security_Identity_Architecture.md
│   ├── 07_Data_Architecture.md
│   ├── 08_API_Architecture.md
│   ├── 09_Integration_Architecture.md
│   ├── 10_Infrastructure_Deployment.md
│   ├── 11_Component_Diagram_C4L3.md
│   ├── ADR/
│   │   ├── ADR-000_Template.md
│   │   ├── ADR-001_{Decision}.md
│   │   ├── ADR-002_{Decision}.md
│   │   └── ...
│   ├── management_framework/              ← Architecture phase governance
│   │   ├── Decision_Log.md               ← Decisions below ADR threshold
│   │   ├── Change_Log.md                 ← Architecture scope changes
│   │   ├── Issue_Log.md                  ← Design blockers
│   │   └── Lessons_Learned.md            ← Architecture design lessons
│   └── ARCHITECTURE_PACKAGE_README.md
│
│ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
│ 📦 AI-DWG OUTPUT — Development Workspace (writes to project root)
│ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
│
├── .kiro/
│   └── steering/
│       ├── workspace-rules.md                  ← ALWAYS
│       ├── architecture-principles.md          ← ALWAYS
│       ├── tech-stack.md                       ← ALWAYS
│       ├── coding-standards.md                 ← ALWAYS
│       ├── project-governance.md               ← ALWAYS
│       ├── scope-and-risks.md                  ← ALWAYS
│       ├── session-governance.md               ← ALWAYS
│       ├── role-isolation.md                   ← ALWAYS
│       ├── domain-context.md                   ← ALWAYS
│       ├── api-standards.md                    ← ALWAYS
│       ├── security-rules.md                   ← ALWAYS
│       ├── module-structure.md                 ← ALWAYS
│       ├── testing-strategy.md                 ← ALWAYS
│       ├── database-rules.md                   ← ALWAYS
│       ├── naming-conventions.md               ← ALWAYS
│       ├── git-workflow.md                     ← ALWAYS
│       ├── error-handling.md                   ← ALWAYS
│       ├── observability-logging.md            ← ALWAYS
│       ├── observability-sensitive.md          ← ALWAYS
│       ├── [multi-tenancy.md]                  ← IF multi-tenant
│       ├── [api-versioning.md]                 ← IF multi-version API
│       ├── [resilience-standards.md]           ← IF distributed / >3 integrations / extension
│       ├── [observability-tracing.md]          ← IF tracing tool specified / extension
│       ├── [performance-standards.md]          ← IF latency SLOs defined
│       ├── [workflow-engine.md]                ← IF workflow component exists
│       ├── [frontend-standards.md]             ← IF UI containers / BFF extension
│       ├── [event-sourcing.md]                 ← IF Event Sourcing extension active
│       └── [feature-flags.md]                  ← IF Feature Flags extension active
│
├── PROJECT_INSTRUCTIONS.md                     ← Master developer guide
├── DEFINITION_OF_DONE.md                       ← Quality criteria
├── CONTRIBUTING.md                             ← Commit/PR/branching process
├── TEAM_AGREEMENTS.md                          ← Operating rules
├── ONBOARDING.md                               ← New developer checklist
├── README.md                                   ← Project README
│
├── .github/
│   └── pull_request_template.md                ← PR checklist
│
├── templates/
│   ├── session-planning.md                     ← AI session planning
│   ├── sprint-planning.md                      ← Sprint structure
│   └── estimation-guide.md                     ← Size estimation
│
├── .gitignore                                  ← Tech-stack appropriate
├── .editorconfig                               ← Code style
├── docker-compose.yml                          ← Infrastructure skeleton
├── CODEOWNERS                                  ← Module ownership
│
├── management_framework/                       ← Development phase governance
│   ├── Decision_Log.md                         ← Implementation decisions
│   ├── Change_Log.md                           ← Build scope changes
│   ├── Issue_Log.md                            ← Blockers and problems
│   └── Lessons_Learned.md                      ← Sprint/session insights
│
├── {src-structure}/                            ← Folder layout from C4 L3
│   ├── {module-1}/
│   ├── {module-2}/
│   ├── {module-n}/
│   └── {shared-kernel}/                        (if applicable)
│
│ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
│ 📦 AI-GCE OUTPUT — Compliance & Enforcement Layer (on top of AI-DWG)
│ ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
│
├── .compliance-state.json                      ← Tier tracking, readiness, score history
│
├── .kiro/
│   ├── hooks/                                  ← Auto-generated compliance hooks
│   │   ├── INSTALL-GUIDE.md                    ← Tier-based installation roadmap
│   │   │── — TIER A (fileEdited — security-critical) —
│   │   ├── security-gate-check.json
│   │   ├── secret-detection.json
│   │   ├── migration-safety.json
│   │   ├── sensitive-data-check.json
│   │   ├── [tenant-isolation-check.json]       (IF multi-tenancy)
│   │   │── — TIER B (agentStop — advisory) —
│   │   ├── domain-layer-purity.json
│   │   ├── module-boundary-check.json
│   │   ├── coverage-check.json
│   │   ├── naming-check.json
│   │   ├── documentation-reminder.json
│   │   ├── steering-quality-check.json
│   │   │── — OTHER EVENT TYPES —
│   │   ├── session-discipline.json             (promptSubmit)
│   │   ├── pre-code-spec-check.json            (preToolUse/write)
│   │   ├── post-task-governance.json           (postTaskExecution)
│   │   ├── segregation-check.json              (postTaskExecution, Tier 2+)
│   │   ├── api-contract-check.json             (fileCreated)
│   │   ├── pre-pr-checklist.json               (userTriggered, Tier 2+)
│   │   ├── periodic-audit.json                 (userTriggered)
│   │   └── [change-readiness-gate.json]        (preTaskExecution, Tier 3)
│   │
│   └── steering/                               ← May enrich existing steering (Step 4b)
│       ├── [compliance-phase-context.md]        (fileMatch — IF team ≥ 3)
│       ├── [compliance-code-rules.md]           (fileMatch — IF team ≥ 3)
│       ├── [compliance-test-conventions.md]     (fileMatch — IF team ≥ 3)
│       └── [compliance-api-conventions.md]      (fileMatch — IF team ≥ 3)
│
├── docs/
│   └── compliance-dashboard.md                 ← Generated by audit agent (maintained ongoing)
│
└── .governance/                                ← Full governance infrastructure
    ├── COMPLIANCE_README.md                    ← How compliance works in THIS project
    │
    ├── rules/
    │   ├── — ARCHITECTURAL (always) —
    │   ├── architecture-compliance.md
    │   ├── api-first-compliance.md
    │   ├── security-compliance.md
    │   ├── data-governance.md
    │   ├── module-boundaries.md
    │   ├── naming-conventions.md
    │   ├── error-handling-compliance.md
    │   ├── logging-compliance.md
    │   ├── sensitive-data-protection.md
    │   ├── domain-context-enforcement.md
    │   ├── — NON-ARCHITECTURAL (tier-gated) —
    │   ├── phase-gates.md                      (Tier 1 basic → Tier 3 full)
    │   ├── session-governance.md               (Tier 1 basic / Tier 2 full)
    │   ├── governance-checklist.md             (Tier 2+)
    │   ├── role-isolation.md                   (Tier 2+)
    │   ├── team-topology.md                    (Tier 2+)
    │   ├── sprint-governance.md                (Tier 2+)
    │   ├── pr-governance.md                    (Tier 2+)
    │   ├── cicd-gates.md                       (Tier 2+)
    │   ├── devops-deployment.md                (Tier 2+)
    │   ├── steering-governance.md              (Tier 2+)
    │   ├── compliance-log-governance.md        (Tier 2+)
    │   ├── change-management.md                (Tier 3)
    │   ├── — CONDITIONAL —
    │   ├── [tenant-isolation.md]               (IF multi-tenancy.md)
    │   ├── [api-versioning-compliance.md]      (IF api-versioning.md)
    │   ├── [resilience-compliance.md]          (IF resilience-standards.md)
    │   ├── [performance-compliance.md]         (IF performance-standards.md)
    │   ├── [frontend-compliance.md]            (IF frontend-standards.md)
    │   ├── [event-sourcing-compliance.md]      (IF event-sourcing.md)
    │   ├── [feature-flag-compliance.md]        (IF feature-flags.md)
    │   └── [mcp-governance.md]                 (IF .kiro/settings/mcp.json configured)
    │
    ├── agents/
    │   ├── compliance-audit-agent.md           ← 9-step with scoring, dashboard, tiers
    │   └── project-init-agent.md               ← 5-question scaffolding agent
    │
    ├── compliance-log/
    │   ├── compliance-log-schema.md            ← JSONL schema (CHECK/EXCEPTION/REMEDIATION/AUDIT/REDERIVATION)
    │   ├── exception-workflow.md               ← 5-step formal bypass process
    │   └── remediation-workflow.md             ← Violation resolution with SLAs
    │
    ├── [brownfield-baseline.md]                (IF brownfield-patterns.md exists)
    └── [incremental-adoption-plan.md]          (IF brownfield-patterns.md exists)
```

---

## PART 3: Data Flow Between Packages

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│             │         │             │         │             │         │             │
│   AI-PILC   │────────►│   AI-ADLC   │────────►│   AI-DWG    │────────►│   AI-GCE    │
│             │         │             │         │             │         │             │
└─────────────┘         └─────────────┘         └─────────────┘         └─────────────┘
       │                       │                       │                       │
       ▼                       ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   OUTPUT:   │         │   OUTPUT:   │         │   OUTPUT:   │         │   OUTPUT:   │
│             │         │             │         │             │         │             │
│ PIP folder  │         │ AP folder   │         │ Project     │         │.kiro/hooks  │
│ (governance │         │ (arch docs  │         │ root itself │         │.governance/ │
│  documents) │         │  + ADRs)    │         │ (.kiro/     │         │.compliance- │
│             │         │             │         │  steering,  │         │ state.json  │
│             │         │             │         │  configs,   │         │(enforcement │
│             │         │             │         │  structure) │         │ layer on    │
│             │         │             │         │             │         │ top of DW)  │
└─────────────┘         └─────────────┘         └─────────────┘         └─────────────┘
                                                                               
  Separate folder          Separate folder         IS the workspace         Layered on
  (reference docs)         (reference docs)        (you work inside it)     workspace
```

### Input/Output Contract Summary

| Package | Reads From | Produces At | Key File to Detect |
|---------|-----------|------------|-------------------|
| **AI-PILC** | Raw requirements (any format) | `{pilc-output}/` folder | `pilc-state.md` |
| **AI-ADLC** | PIP or standalone requirements | `{adlc-output}/` folder | `adlc-state.md` |
| **AI-DWG** | `{adlc-output}/` (reads `adlc-state.md` for extensions) | `{project-root}/` directly | `.kiro/steering/workspace-rules.md` |
| **AI-GCE** | `{project-root}/.kiro/steering/` (AI-DWG output) | `{project-root}/.kiro/hooks/` + enrichments | `.kiro/hooks/` folder exists |

### Standalone vs. Chain Usage

Each package can be used independently OR as part of the chain:

| Package | Standalone Input | Chain Input |
|---------|-----------------|-------------|
| **AI-PILC** | Raw requirement document, verbal brief, or existing PRD | — (first in chain) |
| **AI-ADLC** | Requirements + Charter, existing architecture to extend | PIP from AI-PILC |
| **AI-DWG** | Any Architecture Package (structured markdown) | AP from AI-ADLC |
| **AI-GCE** | Any workspace with `.kiro/steering/` files | DW from AI-DWG |

---

## PART 4: Chain Contracts (Detection by Marker, Not by Path)

Each package is **contract-aware** — it knows what its predecessor produces and what its successor expects. But paths are NEVER hardcoded. Users choose WHERE things go; packages define WHAT files must exist.

### Contract Design Principles

| Principle | Meaning |
|-----------|---------|
| **Detection by marker** | Look for a specific file name, not a specific folder path |
| **User owns WHERE** | Output folder location is always user's choice |
| **Package owns WHAT** | File names, state file schema, and internal structure are fixed |
| **Graceful standalone** | Every package works without the chain (accepts equivalent manual input) |
| **Format tolerant** | Supports both numbered docs and phase-folder structures from predecessor |
| **Cross-repo capable** | Predecessor output can be anywhere — different folder, repo, or drive |

---

### AI-PILC Contract

```
┌─────────────────────────────────────────────────────────────┐
│  AI-PILC                                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  READS: Raw requirements (any format, any location)          │
│  ─────  No predecessor in chain.                             │
│         Accepts: document, verbal, existing artifacts         │
│                                                              │
│  MARKER (input): None — first in chain                       │
│                                                              │
│  ─────────────────────────────────────────────────────────── │
│                                                              │
│  PRODUCES: Project Initiation Package                         │
│  ────────  Location: {user-chosen path}                      │
│                                                              │
│  MARKER (output): pilc-state.md                              │
│                                                              │
│  GUARANTEED FILES (relative to marker):                       │
│  • pilc-state.md (state + completion status)                 │
│  • Numbered artifacts (01_*.md through 12_*.md)              │
│  • PROJECT_INITIATION_PACKAGE.md (final assembly)            │
│                                                              │
│  SUCCESSOR EXPECTS: AI-ADLC looks for pilc-state.md         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### AI-ADLC Contract

```
┌─────────────────────────────────────────────────────────────┐
│  AI-ADLC                                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  READS: PIP (from AI-PILC) OR standalone requirements        │
│  ─────  Detection: scan for pilc-state.md                    │
│         Fallback: ask user for requirements location         │
│                                                              │
│  MARKER (input): pilc-state.md                               │
│  DETECTION STRATEGY:                                         │
│    1. User provides path → use it                            │
│    2. Scan: ./, ../project-initiation/, ../pip/              │
│    3. Not found → ask user OR accept raw requirements        │
│                                                              │
│  ─────────────────────────────────────────────────────────── │
│                                                              │
│  PRODUCES: Architecture Package                               │
│  ────────  Location: {user-chosen path}                      │
│                                                              │
│  MARKER (output): adlc-state.md                              │
│                                                              │
│  GUARANTEED FILES (relative to marker):                       │
│  • adlc-state.md (state + extensions + structure choice)     │
│  • Architecture docs (numbered OR phase-folder)              │
│    - Architecture Vision                                     │
│    - System Context (C4 L1)                                  │
│    - Container Diagram (C4 L2)                               │
│    - Technology Stack                                        │
│    - Security & Identity Architecture                        │
│    - Data Architecture                                       │
│    - API Architecture                                        │
│    - Integration Architecture                                │
│    - Infrastructure & Deployment                             │
│    - Component Design (C4 L3)                                │
│  • ADR/ folder (Architecture Decision Records)               │
│  • Architecture_Workbook.md                                  │
│  • ARCHITECTURE_PACKAGE_README.md                            │
│  • [Multi-Tenancy Architecture] (conditional)                │
│                                                              │
│  STATE FILE SCHEMA (fields AI-DWG reads):                    │
│  • Output Structure: {numbered | phase-folder}               │
│  • Enabled Extensions: {list of active v1.1 extensions}      │
│  • Completed Stages: {list with timestamps}                  │
│  • ADR Register: {ADR-001: title, ADR-002: title, ...}      │
│                                                              │
│  SUCCESSOR EXPECTS: AI-DWG looks for adlc-state.md          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### AI-DWG Contract

```
┌─────────────────────────────────────────────────────────────┐
│  AI-DWG                                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  READS: Architecture Package (from AI-ADLC) OR equivalent    │
│  ─────  Detection: scan for adlc-state.md                    │
│         Fallback: ask user to point to architecture docs     │
│                                                              │
│  MARKER (input): adlc-state.md                               │
│  DETECTION STRATEGY:                                         │
│    1. User provides path → use it                            │
│    2. Scan: ./architecture/, ./docs/architecture/,           │
│       ../, ./ (current directory)                            │
│    3. Not found → ask: "Where is your Architecture Package?" │
│    4. No adlc-state.md at all → manual mode (user maps docs) │
│                                                              │
│  FORMAT TOLERANCE:                                           │
│  • Numbered: 01_Architecture_Vision.md, 02_System_Context... │
│  • Phase-folder: foundation/, decomposition/, decisions/...  │
│  • Determined by reading adlc-state.md "Output Structure"    │
│                                                              │
│  ─────────────────────────────────────────────────────────── │
│                                                              │
│  PRODUCES: Development Workspace                              │
│  ────────  Location: {user-chosen workspace root}            │
│                                                              │
│  MARKER (output): .kiro/steering/workspace-rules.md          │
│                                                              │
│  GUARANTEED FILES (relative to workspace root):               │
│  • .kiro/steering/workspace-rules.md                         │
│  • .kiro/steering/architecture-principles.md                 │
│  • .kiro/steering/tech-stack.md                              │
│  • .kiro/steering/coding-standards.md                        │
│  • .kiro/steering/project-governance.md                      │
│  • .kiro/steering/scope-and-risks.md                         │
│  • .kiro/steering/session-governance.md                      │
│  • .kiro/steering/role-isolation.md                          │
│  • .kiro/steering/domain-context.md                          │
│  • .kiro/steering/api-standards.md                           │
│  • .kiro/steering/security-rules.md                          │
│  • .kiro/steering/module-structure.md                        │
│  • .kiro/steering/testing-strategy.md                        │
│  • .kiro/steering/database-rules.md                          │
│  • .kiro/steering/naming-conventions.md                      │
│  • .kiro/steering/git-workflow.md                            │
│  • .kiro/steering/error-handling.md                          │
│  • .kiro/steering/observability-logging.md                   │
│  • .kiro/steering/observability-sensitive.md                 │
│  • PROJECT_INSTRUCTIONS.md                                   │
│  • DEFINITION_OF_DONE.md                                     │
│  • CONTRIBUTING.md                                           │
│  • TEAM_AGREEMENTS.md                                        │
│  • ONBOARDING.md                                             │
│  • CODEOWNERS                                                │
│  • management_framework/ (Decision_Log, Change_Log,          │
│    Issue_Log, Lessons_Learned)                                │
│  • .kiro/steering/[conditional files based on AP]            │
│                                                              │
│  SIGNAL FORMAT (sent after generation/reconciliation):       │
│  ⚡ From: AI-DWG | To: AI-GCE                                │
│     Event: workspace-generated | steering-files-updated      │
│     Workspace root: {path}                                   │
│     Affected files: {list}                                   │
│                                                              │
│  SUCCESSOR EXPECTS: AI-GCE looks for                         │
│    .kiro/steering/workspace-rules.md                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### AI-GCE Contract

```
┌─────────────────────────────────────────────────────────────┐
│  AI-GCE                                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  READS: Development Workspace (from AI-DWG) OR equivalent    │
│  ─────  Detection: scan for .kiro/steering/workspace-rules.md│
│         Fallback: ask user to point to workspace root        │
│                                                              │
│  MARKER (input): .kiro/steering/workspace-rules.md           │
│  DETECTION STRATEGY:                                         │
│    1. Current directory contains .kiro/steering/ → use it    │
│    2. User provides workspace path → use it                  │
│    3. Not found → ask: "Where is your workspace root?"       │
│    4. No workspace-rules.md → cannot proceed                 │
│       (AI-DWG must run first, or user provides equivalent)   │
│                                                              │
│  READS ALL FILES IN:                                         │
│  • .kiro/steering/*.md (every steering file present)         │
│  • DEFINITION_OF_DONE.md (quality criteria)                  │
│  • TEAM_AGREEMENTS.md (PR process, commit conventions)       │
│  • CODEOWNERS (ownership mapping)                            │
│  • PROJECT_INSTRUCTIONS.md (project context)                 │
│  • Folder structure (actual module layout)                   │
│                                                              │
│  ─────────────────────────────────────────────────────────── │
│                                                              │
│  PRODUCES: Compliance & Enforcement Layer                     │
│  ────────  Location: same workspace root (layered on top)    │
│                                                              │
│  MARKER (output): .kiro/hooks/ folder exists                 │
│                                                              │
│  GUARANTEED FILES (relative to workspace root):               │
│  • .compliance-state.json (tier tracking, readiness, scores) │
│  • .kiro/hooks/INSTALL-GUIDE.md (tier-based roadmap)         │
│  • .kiro/hooks/*.json (18+ compliance hooks, tier-gated)     │
│  • .governance/COMPLIANCE_README.md                          │
│  • .governance/rules/*.md (10 always + 12 tier-gated +       │
│    up to 8 conditional)                                      │
│  • .governance/agents/compliance-audit-agent.md              │
│  • .governance/agents/project-init-agent.md                  │
│  • .governance/compliance-log/compliance-log-schema.md       │
│  • .governance/compliance-log/exception-workflow.md          │
│  • .governance/compliance-log/remediation-workflow.md        │
│  • docs/compliance-dashboard.md                              │
│  • [.governance/brownfield-baseline.md] (IF brownfield)      │
│  • [.governance/incremental-adoption-plan.md] (IF brownfield)│
│                                                              │
│  SUCCESSOR: None — last in chain                             │
│  (Development teams + AI-DLC consume the workspace)          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Cross-Package Marker File Summary

| Package | Input Marker | Output Marker |
|---------|:------------:|:-------------:|
| **AI-PILC** | — (first) | `pilc-state.md` |
| **AI-ADLC** | `pilc-state.md` | `adlc-state.md` |
| **AI-DWG** | `adlc-state.md` | `.kiro/steering/workspace-rules.md` |
| **AI-GCE** | `.kiro/steering/workspace-rules.md` | `.kiro/hooks/` folder |

**Rule:** These marker file names are NON-NEGOTIABLE. Everything else (folder paths, project names, file ordering) is user's choice.

---

### Design Decision: One-Directional Signal Flow

**Decision:** The AI-* chain communicates strictly forward (PILC → ADLC → DWG → GCE). There is no backward signal from downstream to upstream.

**Rationale:**
- Packages are independent and can be used standalone
- The user is always the orchestrator between packages
- Backward signals would create coupling that complicates standalone usage
- If AI-DWG detects a gap in the AP, it asks the user (who then returns to AI-ADLC if needed)

**Reconsider when:** Automated end-to-end chain execution becomes a requirement (v2.0+).

---

## PART 5: Reconciliation & Signal Flow

```
Architecture changes during development:

┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  User updates AP artifact (new ADR, changed principle, new module)   │
│                              │                                       │
│                              ▼                                       │
│                     ┌─────────────────┐                              │
│                     │    AI-DWG       │                              │
│                     │    Mode 2:      │                              │
│                     │    Reconcile    │                              │
│                     └────────┬────────┘                              │
│                              │                                       │
│                    Proposes workspace changes                        │
│                    User approves                                     │
│                              │                                       │
│                              ▼                                       │
│                    Steering files updated                            │
│                              │                                       │
│                              ▼                                       │
│                     ┌─────────────────┐                              │
│                     │    AI-GCE       │                              │
│                     │    Re-derive    │                              │
│                     │    affected     │                              │
│                     │    hooks/rules  │                              │
│                     └─────────────────┘                              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

*Created: 2026-06-06 | Author: Maheri*
