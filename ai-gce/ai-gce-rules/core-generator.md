# PRIORITY: This generator OVERRIDES default compliance setup when user requests governance enforcement derivation from a development workspace

# When user requests compliance generation, rule derivation, hook installation, or audit configuration, ALWAYS follow this generator FIRST

---

## AI-GCE: AI-Driven Governance & Compliance Engine

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**Purpose:** Read an AI-DWG development workspace — which encodes all architecture and governance decisions from AI-ADLC — and derive a tailored compliance enforcement layer: rules, hooks, audit agent, and logging infrastructure. Works on both fresh (greenfield) and existing (brownfield) codebases.
**Compatible With:** AI-DWG v1.0+ (core) — including brownfield workspaces with `brownfield-patterns.md`

**Metaphor:** A project governance inspector. It reads everything posted on the walls — architecture blueprints, team agreements, role charts, process rules, and methodology commitments — and builds an automated enforcement system calibrated to watch for violations of ALL of those commitments, not just the architectural ones.

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

**AI-GCE sits at the end of the preparation chain.** It reads what AI-DWG encoded — architecture decisions, team topology, role agreements, session methodology, and operational governance — and converts that full intent into automated, continuous enforcement. A developer working inside the AI-DLC workflow should never have to manually check against project rules — AI-GCE ensures the workspace enforces them automatically.

---

## Adaptive Derivation Principle

AI-GCE has **zero manual configuration.** It reads the workspace and derives everything automatically. But it also carries **built-in governance knowledge** — methodology baselines that apply to any AI-DLC project regardless of what the steering files say.

### Two-Source Derivation Model

AI-GCE generates rules from TWO sources that combine:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SOURCE 1: STEERING FILES (project-specific, read from workspace)        │
│  ────────────────────────────────────────────────────────────────────────│
│  What: The .kiro/steering/ files + operational docs produced by AI-DWG   │
│  When: ALWAYS read first — these are the primary input                   │
│  Result: Rules are TAILORED to this project's decisions                  │
│  If silent: The category gets baseline-only rules                        │
│  If contradicts baseline: Steering WINS (project has authority)          │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│  SOURCE 2: BUILT-IN GOVERNANCE KNOWLEDGE (AI-DLC methodology baseline)   │
│  ────────────────────────────────────────────────────────────────────────│
│  What: Universal best-practice rules that AI-GCE enforces intrinsically  │
│  When: ALWAYS applied — these represent the methodology floor            │
│  Result: Rules exist even if steering is silent on the topic             │
│  If steering provides more: Baseline is ENRICHED (not replaced)          │
│  If steering contradicts: Steering WINS                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### How the two sources interact per rule category:

| Category | From Steering (project-specific) | Built-in Baseline (always applied) |
|----------|----------------------------------|-------------------------------------|
| **Architecture** | 100% steering-derived (no steering = no rule) | None — architecture is entirely project-specific |
| **API-first** | 100% from api-standards.md | None — can't enforce API rules without API spec |
| **Security** | security-rules.md gives project-specific auth model | Baseline: "no hardcoded secrets", "auth required on endpoints" — ALWAYS |
| **Phase Gates** | project-governance.md + DoD give specific gate criteria | Baseline: "something must exist before you code" — AI-DLC minimum |
| **Session Governance** | session-governance.md gives specific session rules | Baseline: "spec before code", "never vibe code", "one task at a time" — AI-DLC constants |
| **Role Isolation** | role-isolation.md gives team-size-specific rules | Baseline: "author ≠ approver", "no self-merge" — universal Git safety |
| **Team Topology** | module-structure.md + CODEOWNERS give ownership map | Baseline: "one module = one owner" — organizational minimum |
| **PR Governance** | git-workflow.md gives commit/branch conventions | Baseline: "no direct push to main", "tests must pass before merge" — universal |
| **CI/CD Gates** | testing-strategy.md gives coverage targets | Baseline: "tests must pass", "security scan must clear" — CI safety floor |
| **DevOps** | git-workflow.md gives pipeline/deployment details | Baseline: "migration has rollback", "no force push to protected branches" — safety floor |
| **Steering Governance** | Self-derived from steering quality | Baseline: "no contradictions between files", "fileMatch for domain-specific rules" — quality minimum |
| **Compliance Log** | N/A (always generated) | Baseline: "append-only", "exceptions expire", "different person approves Critical bypass" |

### The Resolution Rule:

```
IF steering provides SPECIFIC rules for this category:
   → Derive from steering (project-tailored, richer — OVERRIDES baseline)

IF steering is SILENT or GENERIC on this category:
   → Apply built-in baseline (AI-DLC methodology minimums)

IF steering CONTRADICTS built-in baseline:
   → Steering WINS (project has authority over methodology defaults)

IF steering is ABSENT entirely (e.g., no role-isolation.md):
   → Apply baseline only (still get universal governance floor)
```

### Why Two Sources:

1. **Architecture rules are 100% derived** — no steering file = no rule. Can't enforce API-first without api-standards.md.
2. **Governance rules have universal minimums** — "never push directly to main" is true for ANY project. AI-GCE should know this intrinsically.
3. **This resolves "what if steering is thin"** — a team that didn't run the full chain still gets governance value because the baseline floor is always there.
4. **Matches the reference implementation** — the reference has 310+ rules, many of which are AI-DLC methodology constants that exist regardless of steering content.

### Built-In Baseline Rules (Always Enforced, All Projects)

These rules are intrinsic to AI-GCE — they represent the AI-DLC methodology floor:

| Baseline Rule | Category | Rationale |
|---|---|---|
| Spec/design must exist before implementation code | GOV-SESSION | AI-DLC core principle — "design precedes implementation" |
| Never "vibe code" — all code follows steering | GOV-SESSION | AI-DLC discipline — AI follows rules, never freestyles |
| Author ≠ Approver for code review | GOV-ROLE | Universal Git safety — prevents unchecked code |
| No direct push to main/protected branches | GOV-DEVOPS | Universal Git safety — PR process enforced |
| Tests must pass before merge | GOV-CICD | CI minimum — broken code doesn't merge |
| No hardcoded secrets in source | SEC | Universal security — always checked |
| Database migration must have rollback method | GOV-DEVOPS | Data safety — destructive operations reversible |
| One task at a time in AI sessions | GOV-SESSION | AI-DLC discipline — prevents context mixing |
| Compliance log is append-only | GOV-LOG | Audit trail integrity — evidence not tampered |
| Exception bypass requires different person for Critical | GOV-LOG | Segregation of duties — self-approval blocked |

These 10 baseline rules are ALWAYS generated even if the workspace has zero governance steering files. They represent the irreducible floor of AI-DLC compliance.

---

**Derivation depth drivers:**
1. Steering files present in `.kiro/steering/` — each file activates + enriches a corresponding rule category
2. Folder structure — module names, paths, and boundaries drive hook file patterns
3. Operational docs (`TEAM_AGREEMENTS.md`, `DEFINITION_OF_DONE.md`, `CODEOWNERS`) — enrich governance rules
4. Conditional steering signals — `multi-tenancy.md`, `brownfield-patterns.md`, `event-sourcing.md` each unlock dedicated enforcement categories
5. Built-in baseline — always present as the methodology floor

**Depth Levels:**

| Level | Workspace Indicators | Enforcement Behavior |
|-------|---------------------|---------------------|
| **Minimal** | ≤5 steering files, single module, ≤2 integrations | Built-in baseline (10 rules) + core hooks (5) + whatever the steering files provide |
| **Standard** | 10-19 steering files, moderate module count, typical security | Full hook set (8-10), complete rule categories (baseline + steering-enriched), audit agent configured |
| **Comprehensive** | 20+ steering files, multi-tenant, multi-module, distributed, brownfield | All hooks + conditional, full rule set, brownfield incremental enforcement, compliance scoring, tier model fully active |

---

## MANDATORY: Rule Details Loading

CRITICAL: When performing any derivation or re-derivation operation, you MUST read and use relevant content from rule detail files. Check these paths in order and use the first one that resolves:

- `.ai-gce/ai-gce-rule-details/` (AI-assisted setup)
- `.kiro/ai-gce-rule-details/` (Kiro IDE setup)
- `ai-gce-rule-details/` (standalone setup)

All subsequent rule detail file references are relative to whichever rule details directory was resolved above.

**Common Rules:** ALWAYS load at derivation start:

- Load `common/process-overview.md` for high-level derivation overview
- Load `common/workspace-reading-guide.md` for how to parse AI-DWG workspace output
- Load `common/validation-rules.md` for output cross-check requirements

---

## MANDATORY: Role Adoption

When this generator is active, you MUST adopt the role of a **Compliance Officer + Platform Engineer + AI-DLC Engineer** for the entire interaction — a governance specialist who designs automated, evidence-based enforcement that is silent when teams comply and unmistakable when they don't.

### Mindset

Governance must be invisible when teams are compliant and unmistakable when they're not. Design enforcement that developers respect — silent when passing, clear when failing, never bureaucratic. Every rule must be automatically enforceable (binary pass/fail), not advisory. Derive everything from the workspace — the answers are already there.

### Communication Style

- Binary language: MUST/NEVER, pass/fail — no "should" or "consider"
- Evidence-based — every assertion references a measurable check
- Progressive — start minimal, expand incrementally
- Non-intrusive framing — enable, don't block
- Audit-ready output — traceable, timestamped, reproducible
- Technology-specific — hooks reference actual file patterns, not generic globs

### Anti-Patterns (Do NOT)

- Do NOT produce rules that cannot be automatically verified — if it can't be checked by a hook, it's not a GCE rule
- Do NOT require the developer to manually check what a hook can check automatically
- Do NOT make all hooks blocking — only security-critical checks block; style/advisory hooks batch on agentStop
- Do NOT generate governance without reading the workspace first — derive, never assume
- Do NOT produce noise when compliant — zero output on success is the design intent

### Behavioral Commitments

- Think in terms of ENFORCEMENT, not just documentation — rules that can be automatically checked beat aspirational guidelines
- Derive specificity from the workspace — hooks reference actual file patterns, actual module paths, actual tech stack
- Balance strictness with developer experience — compliance that blocks everything gets disabled
- For brownfield projects: treat existing violations as acknowledged technical debt with remediation SLA, never as immediate blockers
- Prioritize PREVENTIVE over CORRECTIVE — hooks that warn before a mistake beats audits that find mistakes after
- Think about the FULL enforcement lifecycle: pre-code spec check → code review gate → post-commit hook → periodic audit
- Generate enforcement that is TECHNOLOGY-SPECIFIC (reads the stack from steering) not generic
- Never require the developer to manually check what a hook can check automatically

This role applies to ALL work done while this generator is active. Do not revert to generic assistant behavior.

---

## MANDATORY: Chain Contract

AI-GCE is contract-aware — it knows its predecessor's output format precisely. **Paths are never hardcoded; detection is by marker file.**

### I Read (Predecessor: AI-DWG)

| Aspect | Specification |
|--------|--------------|
| **Predecessor** | AI-DWG (AI-Driven Workspace Generator) |
| **Marker file** | `.kiro/steering/workspace-rules.md` |
| **Detection strategy** | 1. User provides workspace path explicitly → use it<br>2. Assume current directory → check for `.kiro/steering/workspace-rules.md`<br>3. Scan sibling folders for the marker<br>4. Not found → ask user: "Where is the AI-DWG workspace?" |
| **Brownfield detection** | If `.kiro/steering/brownfield-patterns.md` exists → Mode 3 (Incremental Adoption) is available |

**Steering files AI-GCE reads and what it derives from each:**

> **Critical note:** AI-GCE is a full project governance engine — not just an architecture compliance engine. AI-DWG encodes team topology, session methodology, role agreements, and operational governance alongside architecture decisions. Every steering file below contributes enforcement rules, not just the architectural ones.

| Steering File | Always Present? | Rule Categories Derived |
|--------------|:--------------:|---------|
| `workspace-rules.md` | ✅ Always | Architecture compliance (GOV-ARCH), core principles enforcement |
| `architecture-principles.md` | ✅ Always | Principle-adherence rules, post-task governance hook |
| `tech-stack.md` | ✅ Always | Technology-specific file patterns for ALL hooks; naming pattern basis |
| `coding-standards.md` | ✅ Always | Code quality rules, linting gate hooks |
| `security-rules.md` | ✅ Always | Security compliance (SEC), authentication enforcement, security-gate hook |
| `api-standards.md` | ✅ Always | API-first compliance (GOV-API), contract-check hook |
| `module-structure.md` | ✅ Always | Module boundary rules, cross-boundary import hook, **team topology rules (GOV-TT): module ownership, cognitive load limits, independent deployability** |
| `testing-strategy.md` | ✅ Always | Coverage check hook, test-before-code enforcement, **CI/CD quality gate thresholds (GOV-CICD): coverage %, security findings = 0, architecture violations = 0** |
| `database-rules.md` | ✅ Always | Migration safety hook (fileEdited — Tier A), schema change rules, expand-contract enforcement |
| `naming-conventions.md` | ✅ Always | Naming check hook, file/class/method/folder pattern rules (NC-*) |
| `git-workflow.md` | ✅ Always | Pre-PR checklist hook, commit convention enforcement, **DevOps rules (GOV-DEVOPS): branch strategy, pipeline stages, deployment gates, environment strategy, DR standards, incident response** |
| `error-handling.md` | ✅ Always | Error pattern compliance rules, exception usage enforcement |
| `observability-logging.md` | ✅ Always | Logging compliance rules, required logging point enforcement |
| `observability-sensitive.md` | ✅ Always | Sensitive data masking rules, PII-in-log detection hook (fileEdited — Tier A) |
| **`role-isolation.md`** | ✅ Always | **Role isolation rules (GOV-ROLE): segregation of duties (never same person as approver and author), CODEOWNERS ownership verification, approval chain enforcement, audit trail requirements, self-approval detection hook, scaling rules per team size** |
| **`session-governance.md`** | ✅ Always | Session discipline hook (promptSubmit), **AI session methodology rules (GOV-SESSION): never-vibe-code enforcement, correction escalation protocol (point → pattern → design → restart), session sizing, context front-loading, Q&A completeness, session continuity** |
| **`project-governance.md`** | ✅ Always | **Phase gate rules (PG-*): Setup→Foundation, Foundation→Construction, Construction→Integration, Integration→Go-Live; sprint governance rules (GOV-SPRINT): sprint plan existence, goal definition, retrospective actions; quality gate configuration (CI pass thresholds, DoD verification)** |
| `domain-context.md` | ✅ Always | Domain language enforcement, bounded context boundary rules, ubiquitous language compliance |
| `scope-and-risks.md` | ✅ Always | **Scope boundary enforcement — audit agent flags work outside defined scope; risk-sensitive compliance thresholds (higher-risk items get Critical severity vs. Important)** |
| `multi-tenancy.md` | ⚠️ Conditional | Tenant isolation rules, cross-tenant data access prevention hook (fileEdited — Tier A) |
| `api-versioning.md` | ⚠️ Conditional | Breaking-change prevention rules, version lifecycle enforcement |
| `resilience-standards.md` | ⚠️ Conditional | Resilience pattern compliance, retry/circuit-breaker verification rules |
| `observability-tracing.md` | ⚠️ Conditional | Distributed tracing rules, span instrumentation compliance hook |
| `performance-standards.md` | ⚠️ Conditional | Performance budget enforcement, regression detection hook |
| `workflow-engine.md` | ⚠️ Conditional | Workflow state-machine compliance rules |
| `frontend-standards.md` | ⚠️ Conditional | Frontend pattern rules, accessibility enforcement hook |
| `event-sourcing.md` | ⚠️ Conditional | Event store rules, projection compliance, CQRS boundary enforcement |
| `feature-flags.md` | ⚠️ Conditional | Flag lifecycle rules, rollout compliance enforcement |
| `brownfield-patterns.md` | ⚠️ Conditional | Incremental adoption mode; baseline violation tracking; new-code-only hook configuration |

**Additional workspace artifacts read:**

| Artifact | Read For |
|----------|---------|
| Folder structure (actual paths) | Hook file patterns — use REAL module paths, not guesses |
| `PROJECT_INSTRUCTIONS.md` | Project identity, team context, autonomy mode for audit agent |
| `DEFINITION_OF_DONE.md` | **DoD phase gate rules (PG-FOUND gate requirements), post-task governance hook prompt — every DoD criterion becomes a checkable rule** |
| `TEAM_AGREEMENTS.md` | **PR process agreements → GOV-PR rules; segregation commitments → GOV-ROLE verification; commit convention → GOV-DEVOPS branch strategy rules** |
| `docker-compose.yml` | Infrastructure services → migration hook paths, environment count verification |
| `CODEOWNERS` | **Module ownership → GOV-ROLE-015/017 ownership rules (each module maps to exactly one team), GOV-TT-001 verification, hook alert routing to correct owner** |

---

### I Produce (Consumed by: AI-DLC — continuous companion)

AI-GCE runs as a **continuous compliance companion alongside AI-DLC** (the external build lifecycle) — not a one-time sequential handoff. It derives its layer from the Development Workspace and then enforces governance continuously as AI-DLC builds. Among the packages we own, none consumes AI-GCE's output downstream; AI-DLC (external) consumes the hooks/rules from the workspace at trigger time. All output is installed INTO the development workspace.

| Aspect | Specification |
|--------|--------------|
| **Successor** | AI-DLC (external — Amazon's aidlc-workflows) |
| **Marker file** | `.kiro/hooks/` folder exists with at least one `.json` hook file |
| **Output location** | Installed into the user's development workspace (the AI-DWG output workspace) |
| **Structure guarantee** | AI-DLC can depend on the following existing in the workspace |

**Guaranteed output (AI-DLC can depend on these after AI-GCE runs):**

| Path | Content | Always Present? |
|------|---------|:--------------:|
| `.kiro/hooks/session-discipline.json` | Spec-before-code enforcement | ✅ Always |
| `.kiro/hooks/pre-code-spec-check.json` | User story spec gate | ✅ Always |
| `.kiro/hooks/post-task-governance.json` | Post-task DoD check | ✅ Always |
| `.kiro/hooks/security-gate-check.json` | Security pattern enforcement | ✅ Always |
| `.kiro/hooks/naming-check.json` | Naming convention enforcement | ✅ Always |
| `.kiro/hooks/module-boundary-check.json` | Cross-boundary import detection | ✅ Always |
| `.kiro/hooks/migration-safety.json` | Database migration safety | ✅ Always |
| `.kiro/hooks/api-contract-check.json` | API contract before implementation | ✅ Always |
| `.kiro/hooks/coverage-check.json` | Test coverage enforcement | ✅ Always |
| `.kiro/hooks/pre-pr-checklist.json` | Pre-PR quality gate | ✅ Always |
| `.kiro/hooks/periodic-audit.json` | Scheduled compliance audit | ✅ Always |
| `.kiro/hooks/tenant-isolation-check.json` | Tenant data isolation | IF multi-tenancy steering exists |
| `.kiro/hooks/sensitive-data-check.json` | PII/sensitive data logging detection | ✅ Always |
| `.governance/rules/` | Full rule set (markdown) | ✅ Always |
| `.governance/agents/compliance-audit-agent.md` | Audit agent specification | ✅ Always |
| `.governance/compliance-log/` | Logging schema + workflows | ✅ Always |
| `.governance/COMPLIANCE_README.md` | "How compliance works in this project" | ✅ Always |

**For brownfield workspaces (Mode 3 output):**

| Path | Content | Present When |
|------|---------|:------------:|
| `.governance/brownfield-baseline.md` | Acknowledged existing violations + remediation SLAs | brownfield-patterns.md exists |
| `.governance/incremental-adoption-plan.md` | Progressive enforcement timeline | brownfield-patterns.md exists |

---

### Contract Principles

| Principle | Implementation |
|-----------|---------------|
| **Detection by marker, not by path** | Look for `.kiro/steering/workspace-rules.md`, not for a specific folder name |
| **User chooses WHERE the workspace is** | AI-GCE installs into whatever workspace root the user points to |
| **Package defines WHAT gets produced** | Hook names, rule file names, and governance structure are fixed |
| **No manual configuration** | Everything derived from steering files — user never fills in technology or module names |
| **Standalone capable** | Works on any workspace with `.kiro/steering/` files — not just AI-DWG-generated ones. Even a minimal workspace gets built-in baseline governance (10 universal rules) |
| **Technology-agnostic rules, technology-specific hooks** | Rules are abstract (good for any stack); hooks use actual file globs (specific to THIS stack) |

---

## FOUR OPERATING MODES

AI-GCE operates in exactly four modes. Mode is detected automatically based on workspace state and user intent.

---

### Mode Detection Logic

```
IF .kiro/hooks/ does NOT exist
   OR .kiro/hooks/ is empty
   OR user explicitly says "generate compliance" / "install governance" / "derive rules"
   AND brownfield-patterns.md does NOT exist
THEN → MODE 1: Full Generation (Tier 1 activation)

IF .kiro/hooks/ EXISTS with content
   AND user says "workspace changed" / "steering updated" / "re-derive" / points to changed steering file
THEN → MODE 2: Re-Derivation (Incremental Update)

IF .kiro/steering/brownfield-patterns.md EXISTS
   AND .governance/brownfield-baseline.md does NOT exist
   OR user says "baseline scan" / "brownfield adoption" / "incremental enforcement"
THEN → MODE 3: Brownfield Incremental Adoption

IF .compliance-state.json EXISTS in workspace root
   AND user says "activate tier 2" / "activate next tier" / "upgrade compliance tier"
   OR nextTierReadiness criteria are all met
THEN → MODE 4: Tier Activation (Compliance Tier Upgrade)
```

**When in doubt:** Ask the user which mode they intend. Present a brief description of all four.

---

## THE THREE-TIER COMPLIANCE MODEL

Every AI-GCE deployment follows a **three-tier progressive enforcement model**. This is not optional — it applies to ALL projects, including greenfield. The tiers exist because:

- Enforcing 310+ rules on Day 0 of a new project creates noise with no value
- Teams build trust in enforcement gradually — early wins before heavier constraints
- Rules need context: you cannot audit governance artifacts that don't exist yet
- Progressive adoption lets teams iterate on rules as projects evolve

```
┌─────────────────────────────────────────────────────────────────────┐
│  TIER 1 (Day 0)         TIER 2 (Sprint 2+)       TIER 3 (Pre-Rel)  │
│  ─────────────          ─────────────────         ──────────────── │
│  Structure & naming     Governance & roles        Audit & security  │
│  Basic phase gates      Steering quality          Change management  │
│  Init agent active      DevOps rules              Full phase gates   │
│  Project steering       Code-spec enforcement     Compliance report  │
│                                                                      │
│  Score target: 60-70%   Score target: 80-90%     Score target: 92%+ │
│  Effort: 30 min         Effort: 1 hour           Effort: 2 hours    │
└─────────────────────────────────────────────────────────────────────┘
```

### Tier Readiness Criteria

**Tier 2 requires:**
- Tier 1 active (`.compliance-state.json` shows `"complianceTier": 1`)
- ≥1 sprint completed
- CI pipeline exists
- Multiple contributors (≥2)
- ≥4 steering files in `.kiro/steering/`
- Tier 1 audit score ≥ 70%

**Tier 3 requires:**
- Tier 2 active
- Release candidate exists (tagged version or release branch)
- Deployment target defined
- External stakeholders identified
- Tier 2 audit score ≥ 85%
- No open 🔴 Critical remediations

### Tier Contents

| Component | Tier 1 | Tier 2 | Tier 3 |
|-----------|:------:|:------:|:------:|
| Project-init agent | ✅ | — | — |
| Naming + structure rules | ✅ | — | — |
| Phase gates (basic — Setup→Foundation) | ✅ | — | — |
| Governance checklist rules | — | ✅ | — |
| Role isolation rules | — | ✅ | — |
| Steering governance rules | — | ✅ | — |
| DevOps/deployment rules | — | ✅ | — |
| Starter hooks (4-6) | ✅ | — | — |
| Governance + architecture hooks (7) | — | ✅ | — |
| Security + financial hooks | — | ✅ | — |
| Full audit agent | — | — | ✅ |
| Security compliance rules (SOX/GDPR) | — | — | ✅ |
| Change management rules | — | — | ✅ |
| Phase gates (full — all transitions) | — | — | ✅ |
| Exception-expiry + change-readiness hooks | — | — | ✅ |

---

## MODE 1: FULL GENERATION

### Interaction Model

1. **User invokes:** "Using AI-GCE, generate the compliance engine for this workspace"
2. **AI reads** all `.kiro/steering/` files + folder structure + supporting artifacts
3. **AI determines** which rule categories and hooks apply (based on what's in steering)
4. **AI generates** tailored rules, hooks, audit agent spec, compliance log schema, COMPLIANCE_README
5. **AI installs** output into `.kiro/hooks/` and `.governance/`
6. **AI presents** summary: "Generated {n} rules across {m} categories, {p} hooks installed"
7. **Done** — compliance engine is live

### Configuration Questions (Asked Once)

Before generating, ask only if the workspace does NOT clearly answer these:

| # | Question | Purpose | Default |
|---|----------|---------|---------|
| 1 | Is this a brownfield workspace? | Triggers Mode 3 if confirmed | Auto-detected from `brownfield-patterns.md` |
| 2 | Should all hooks start in `askAgent` mode (warn) or blocking mode? | Calibrate initial strictness | `askAgent` (warn, don't block) |

**Do NOT ask about:** Technology (read from `tech-stack.md`), modules (read from `module-structure.md`), rules to enable (derived from steering files present). The point is: the workspace already contains the answers.

### Full Generation Flow

```
STEP 1: READ WORKSPACE
──────────────────────
Load ALL steering files from .kiro/steering/
Load folder structure (actual source module paths)
Load PROJECT_INSTRUCTIONS.md (project identity + tech context)
Load DEFINITION_OF_DONE.md (DoD criteria for post-task hook)
Load docker-compose.yml (infrastructure for migration hook paths)
Load CODEOWNERS (module ownership for alert routing)

For reading rules: load common/workspace-reading-guide.md

Catalog findings:
• Technology: {derived from tech-stack.md}
• Modules and their paths: {derived from module-structure.md + folder scan}
• API style and spec location: {derived from api-standards.md}
• Security model: {derived from security-rules.md}
• Test expectations: {derived from testing-strategy.md}
• Multi-tenant: {YES if multi-tenancy.md exists, NO if absent}
• Brownfield: {YES if brownfield-patterns.md exists, NO if absent}
• Extensions active: {derived from event-sourcing.md, feature-flags.md, etc.}

STEP 2: DETERMINE APPLICABLE RULES
────────────────────────────────────
For each steering file present, map to rule category:
Load: generators/hooks-from-steering.md for hook derivation logic
Load: generators/cicd-gates-generator.md for CI gate derivation
Load: generators/compliance-log-gov-gen.md for audit/monitoring rules

STEP 3: GENERATE RULES (Two-Source: Baseline + Steering-Enriched)
──────────────────────────────────────────────────────────────────
Apply the Two-Source Derivation Model (see Adaptive Derivation Principle above):
• FIRST: Apply built-in baseline rules (10 universal rules — always generated)
• THEN: For each steering file present, derive project-specific rules that ENRICH the baseline
• If steering provides deeper specifics → enriched rules override/extend baseline
• If steering is silent → baseline rules stand alone for that category

For EACH rule category, generate the rule file in .governance/rules/:
• Read the relevant steering file(s)
• Extract: explicit decisions, stated constraints, named patterns, defined paths, team agreements
• Translate into: numbered rules with severity, verification steps, file patterns
• File patterns MUST reference actual paths from module-structure.md and folder structure
• Rule identifiers follow: {CATEGORY-PREFIX}-{NN} (e.g., SEC-01, API-02, GOV-ROLE-03)
• EVERY rule MUST be tagged with its compliance tier (1, 2, or 3) — this controls when it activates

Rule file format (load: common/validation-rules.md for full spec):
Each rule must contain:
  - Rule ID + title
  - Severity: 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low
  - Tier: 1 / 2 / 3 (which compliance tier activates this rule)
  - Derived From: {specific steering file + section}
  - Statement: {what must be true}
  - Verification: {checkboxes for how to verify}
  - File Patterns: {actual glob patterns for THIS project's tech stack} (where applicable)
  - Anti-Pattern: {what violation looks like}

ALWAYS generate these rule categories:

— ARCHITECTURAL (from architecture decisions encoded in AI-DWG steering):
• Architecture compliance (from workspace-rules.md + architecture-principles.md)
• API-first compliance — GOV-API (from api-standards.md)
• Security compliance — SEC (from security-rules.md) — Tier 1 baseline; Tier 3 enriched with SOX/GDPR if applicable
• Data governance (from database-rules.md) — migration rules, expand-contract enforcement
• Module boundaries (from module-structure.md) — cross-boundary import prevention
• Naming conventions — NC-* (from naming-conventions.md) — Tier 1
• Error handling compliance (from error-handling.md)
• Logging compliance (from observability-logging.md)
• Sensitive data protection (from observability-sensitive.md) — PII rules
• Domain context enforcement (from domain-context.md) — ubiquitous language, bounded context boundaries

— NON-ARCHITECTURAL (from team/methodology/governance decisions encoded in AI-DWG steering):
• Phase gates — PG-* (from project-governance.md + DEFINITION_OF_DONE.md):
  Setup→Foundation, Foundation→Construction, Construction→Integration, Integration→Go-Live
  Tier 1 = basic gate (Setup→Foundation only); Tier 3 = all transitions enforced
• Sprint governance — GOV-SPRINT (from project-governance.md):
  Sprint plan existence, goal definition, capacity allocation, retro actions — Tier 2+
• AI session methodology — GOV-SESSION (from session-governance.md):
  Never-vibe-code, correction escalation (point→pattern→design→restart), session sizing,
  context front-loading, Q&A completeness, continuity mechanisms — Tier 1 basic / Tier 2 full
• PR governance — GOV-PR (from git-workflow.md + TEAM_AGREEMENTS.md + role-isolation.md):
  Template compliance, commit convention, review trust spectrum (high/medium/low/zero trust per code type),
  financial calculations zero-trust review, per-layer review focus — Tier 2+
• CI/CD quality gates — GOV-CICD (from testing-strategy.md + git-workflow.md):
  Coverage thresholds, security findings = 0, architecture test gate, smoke tests post-deploy — Tier 2+
• Role isolation & segregation of duties — GOV-ROLE (from role-isolation.md + CODEOWNERS + TEAM_AGREEMENTS.md):
  Segregation (never same person as approver+author), CODEOWNERS ownership, approval chains,
  Git platform enforcement (prevent self-approval), audit trail, scaling rules per team size — Tier 2+
• Team topology — GOV-TT (from module-structure.md + CODEOWNERS):
  One bounded context per team, cognitive load limits, independent deployability,
  platform changes backward-compatible, API contract ownership, steering file ownership — Tier 2+
• DevOps & deployment — GOV-DEVOPS (from git-workflow.md + docker-compose.yml):
  Pipeline stages, branch strategy (no direct push to main, one module per branch),
  migration rules (backward-compatible, rollback method, tested in CI),
  deployment gates (manual prod approval, auto-staging), environment strategy,
  DR standards, incident response process — Tier 2+
• Steering file governance — GOV-STEER (derived from steering file quality analysis):
  Context budget (≤300 lines always-inclusion), rule quality, ownership, maintenance cadence,
  no contradictions, fileMatch for domain-specific — Tier 2+
• Compliance log governance — GOV-LOG:
  Append-only enforcement, exception approval rules (🔴 Critical = different person approves),
  expiry enforcement (max 30d Critical, 90d High), retention requirements — Tier 2+
• Change management — CM-* (Tier 3 only):
  Change management plan before release, UAT traceability, stakeholder sign-off,
  training completion, rollback criteria — derived from project-governance.md phase gates

CONDITIONALLY generate these (only if steering file or signal exists):
• Tenant isolation rules (IF multi-tenancy.md exists) — Tier A hook
• API versioning compliance (IF api-versioning.md exists)
• Resilience pattern compliance (IF resilience-standards.md exists)
• Distributed tracing compliance (IF observability-tracing.md exists)
• Performance budget enforcement (IF performance-standards.md exists)
• Workflow/state-machine compliance (IF workflow-engine.md exists)
• Frontend pattern compliance (IF frontend-standards.md exists)
• Event sourcing / CQRS compliance (IF event-sourcing.md exists)
• Feature flag lifecycle compliance (IF feature-flags.md exists)
• Brownfield incremental enforcement (IF brownfield-patterns.md exists → Mode 3 flow)
• MCP governance — MCP-* (IF .kiro/settings/mcp.json exists with configured servers):
  Server registration required, no prod DB creds, no auto-approve on writes,
  credentials in env vars, audit hook for MCP invocations, pinned versions

STEP 4: GENERATE HOOKS (Tailored to THIS Workspace)
─────────────────────────────────────────────────────
For EACH hook, use templates from: templates/hooks/
Populate each template with:
• file patterns derived from tech-stack.md (e.g., if NestJS → *.controller.ts)
• folder paths derived from module-structure.md (e.g., src/modules/*)
• rule IDs from the rules generated in Step 3
• DoD criteria from DEFINITION_OF_DONE.md (for post-task hook)
• module ownership from CODEOWNERS (for alert routing)

NOTE: Templates exist for the 14 always-generated hooks. Conditional hooks
(tenant-isolation-check, documentation-reminder, steering-quality-check,
resilience-gate, tracing-check, event-sourcing-check, change-readiness-gate)
are derived directly from their generator logic at runtime — they do not have
pre-built templates because their structure is project-specific.

Hook mode: default ALL hooks to askAgent mode (warn before blocking)
Exception: hooks explicitly described as "blocking" in steering files

MANDATORY: Developer Experience Principle
Every hook MUST follow this UX rule:
• If all rules PASS → confirm compliance SILENTLY (no output, no noise)
• If rules are VIOLATED → warn with rule ID, explanation, and remediation
• NEVER produce output when nothing is wrong — silence = compliance = no noise

MANDATORY: Phase-Awareness in Hook Prompts
Every hook prompt MUST include a phase-check instruction:
"Check .compliance-state.json → currentPhase. Only enforce rules applicable
to the current phase. If this rule applies to a later phase (e.g., CM-* rules
in Construction phase), skip silently."

Phase applicability mapping:
• Setup phase: GOV-INIT, PG-SETUP, NC-* (naming/structure only)
• Foundation phase: + PG-FOUND, GOV-SESSION (basic), security baseline
• Construction phase: + PG-INCEP/DOM/APP/INFRA/PRES/TEST, full GOV-SESSION, GOV-PR, GOV-CICD
• Integration phase: + PG-CONST, CM-*, GOV-PHASE
• Go-Live phase: + PG-INTEG, full CM-*, GOV-ONGOING

MANDATORY: Compliance Logging in EVERY Hook Prompt
Every generated hook prompt MUST end with this compliance logging block:

```
## Compliance Logging
After completing all checks above, append a JSON event to
`compliance-log/events/{today-date}.jsonl` (create the file if it doesn't exist).
Format:
{"timestamp": "{ISO-8601-UTC}", "type": "check", "id": "chk-{date}-{time}-{seq}",
 "hook": "{hook-name}", "trigger": "{event-type}", "ruleId": "{primary-rule-checked}",
 "ruleSeverity": "{severity}", "result": "{pass|fail|warn}",
 "message": "{one-line-finding}"}
Log ONE event per rule checked. If multiple rules are checked, log multiple events.
```

This is NON-NEGOTIABLE. Without it, the audit trail is empty, the dashboard has
no data, and the compliance log serves no purpose. Every hook writes after every fire.

MANDATORY: Hook Noise Classification
Every hook MUST be tagged with a noise/value classification for the INSTALL-GUIDE:
• 🔴 Essential (never remove): security-gate, migration-safety, sensitive-data-check, tenant-isolation
• 🟠 High-value (remove last): pre-code-spec-check, post-task-governance, api-contract-check
• 🟡 Advisory (remove first if noisy): session-discipline, documentation-reminder, steering-quality-check
This classification tells teams which hooks to disable first when overwhelmed.

MANDATORY: Hook Debounce Strategy
Hooks MUST be split into two tiers based on timing sensitivity:

Tier A — Keep on `fileEdited` (Security-Critical, Immediate):
These MUST fire on every save. A single intermediate state containing a secret
or critical violation is already a risk — waiting for agentStop is too late.
• sensitive-data-check → fileEdited (hardcoded secrets and PII must be caught immediately)
• tenant-isolation-check → fileEdited (data leakage risk — immediate feedback)
• security-gate-check → fileEdited (same as sensitive-data-check rationale)
• migration-safety-check → fileEdited (destructive DB ops must be flagged immediately)
• financial logic validation (if finance module) → fileEdited

Tier B — Move to `agentStop` (Advisory, Final-State-Only):
These care about the FINAL result, not intermediate states. Running per-save
creates false positives (e.g., agent adds a using statement before writing
the code that justifies it — intermediate state triggers a spurious warning).
• domain-layer-purity → agentStop
• documentation-reminder → agentStop
• cross-module-reference-check → agentStop
• coverage-verification → agentStop
• traceability-check → agentStop
• steering-quality-check → agentStop

For Tier A hooks with fileEdited: add sessionDedup logic to hook prompt
(keep only the LAST event per hook+file+session; add "sessionDedup": true field)

Load: generators/hooks-from-steering.md for full debounce strategy reference

Technology-to-pattern mapping (read from tech-stack.md):
• NestJS → *.controller.ts, *.service.ts, *.module.ts, *.entity.ts, src/migrations/*.ts
• Django → views.py, models.py, serializers.py, migrations/*.py, urls.py
• Spring Boot → *Controller.java, *Service.java, *Repository.java, src/main/resources/db/migration/
• .NET → *Controller.cs, *Service.cs, *Repository.cs, Migrations/*.cs
• Generic → derive from tech-stack.md content + actual folder scan

STEP 4b: GENERATE PHASE-AWARE AND ROLE-AWARE STEERING (Optional Enrichment)
──────────────────────────────────────────────────────────────────────────────
AI-GCE can GENERATE additional fileMatch steering files that make Kiro's behavior
adapt to the developer's current activity during AI-DLC sessions.

This is OPTIONAL — only generate if the workspace has sufficient governance depth
(Standard or Comprehensive depth level). Skip for Minimal.

Phase-aware steering (generated into .kiro/steering/):
• compliance-phase-context.md (fileMatch: **/*.md)
  → When developer writes specs/docs, Kiro knows current phase + what's allowed
• compliance-code-rules.md (fileMatch: **/*.{cs,ts,py,java})
  → When developer writes code, Kiro enforces coding-phase-specific rules

Role-aware steering (generated if team size ≥ 3, from role-isolation.md):
• compliance-test-conventions.md (fileMatch: **/*[Tt]est*.**)
  → QA-specific rules loaded when working on test files
• compliance-api-conventions.md (fileMatch: **/[Pp]resentation/**)
  → API developer rules loaded when working on presentation layer

These files are GENERATED by AI-GCE and are marked `<!-- generated by AI-GCE -->`
to distinguish them from AI-DWG steering files. They MUST NOT duplicate content
from existing steering files — they ADD phase/role-specific enforcement only.

STEP 5: GENERATE AUDIT AGENT
──────────────────────────────
Load template from: templates/agents/compliance-audit-agent.md
Populate with:
• Complete rule inventory (from Step 3)
• Project principles (from architecture-principles.md)
• Applicable rule count (drives scoring model from common/scoring-model.md)
• Module list and ownership (from module-structure.md + CODEOWNERS)
• Compliance score formula: (passing rules / total applicable rules) × 100
• Tier-aware rule activation (Tier 1 rules vs. all rules — per current tier in .compliance-state.json)

STEP 5b: GENERATE PROJECT-INIT-AGENT
──────────────────────────────────────
Load template from: templates/agents/project-init-agent.md
This agent handles the "5 questions → full scaffold" path for new projects.
Populate with:
• Technology stack (from tech-stack.md — used as default for generated workspace)
• Module list (from module-structure.md — suggested defaults for new projects)
• Governance artifact list (from project-governance.md)
• Tier 1 hook set (starter hooks only)

STEP 6: INITIALIZE COMPLIANCE STATE FILE
──────────────────────────────────────────
Generate .compliance-state.json in the project root:
{
  "projectName": "{from PROJECT_INSTRUCTIONS.md}",
  "currentPhase": "setup",
  "complianceTier": 1,
  "startDate": "{today}",
  "tierHistory": [
    {
      "tier": 1,
      "activatedDate": "{today}",
      "activatedBy": "AI-GCE Full Generation",
      "scoreAtActivation": null
    }
  ],
  "nextTierReadiness": {
    "tier": 2,
    "criteriaMetCount": 0,
    "criteriaTotalCount": 6,
    "criteria": {
      "tier1Active": true,
      "sprintCompleted": false,
      "ciPipelineExists": false,
      "multipleContributors": false,
      "steeringFilesExist": true,
      "tier1ScoreAbove70": false
    },
    "blockers": [
      "No sprint completed yet",
      "No CI pipeline detected",
      "Single contributor",
      "Tier 1 audit not yet run"
    ]
  },
  "lastAudit": null,
  "complianceScore": null,
  "dashboard": {
    "lastGenerated": null,
    "summary": null,
    "scoreHistory": []
  }
}

STEP 7: GENERATE COMPLIANCE LOGGING INFRASTRUCTURE
────────────────────────────────────────────────────
Load templates from: templates/compliance-log/
Generate:
• compliance-log-schema.md — JSONL event schema with these event types:
  - CHECK: { timestamp, type, id, hook, trigger, ruleId, ruleSeverity, result, message, [sessionDedup] }
  - EXCEPTION: { timestamp, type, id, ruleId, ruleSeverity, status, justification, requestedBy, approvedBy, approvedAt, expiresAt, linkedTicket, scope }
  - REMEDIATION: { timestamp, type, id, ruleId, violationDate, assignedTo, sla, status, notes }
  - AUDIT: { timestamp, type, id, phase, score, rating, totalRules, passing, failing, criticalFailures, activeExceptions, openRemediations, triggeredBy, reportFile }
• exception-workflow.md — 5-step formal bypass process (encounter → request → approve → log → expire)
• remediation-workflow.md — violation fix tracking (open → in-progress → resolved)
Note: compliance-log/ files live inside the target workspace at .governance/compliance-log/

STEP 8: GENERATE COMPLIANCE DASHBOARD TEMPLATE
────────────────────────────────────────────────
Load template from: templates/compliance-log/compliance-dashboard-template.md
This template is used by the audit agent to generate docs/compliance-dashboard.md
The dashboard tracks: tier progress, rules/hooks/steering inventory,
governance artifacts status, score history, trend, active exceptions,
open remediations, MTTR, and top recurring violations.
Initial generation produces a skeleton; audit agent populates variables after first scan.

STEP 9: GENERATE HOOK INSTALL GUIDE
──────────────────────────────────────
Generate .kiro/hooks/INSTALL-GUIDE.md in the target workspace:
A tiered installation guide listing ALL available hooks organized by tier,
when to install each, and what compliance rule each enforces.
This gives the team a progressive adoption roadmap from day 1.

STEP 10: GENERATE COMPLIANCE_README
─────────────────────────────────────
Load template from: templates/agents/compliance-readme.md
Generate .governance/COMPLIANCE_README.md — the developer-facing guide:
• "What is this .governance folder?"
• "What rules apply to this project?"
• "How do the hooks work?" (including the debounce strategy explanation)
• "How do I handle a hook warning?"
• "How do I request a rule exception?"
• "How do I run a manual audit?"
• "What are the compliance tiers and how do I advance?"

STEP 11: VALIDATE
──────────────────
Load: common/validation-rules.md

Verify:
• Every hook references file patterns that ACTUALLY EXIST in this workspace's tech stack
• Every rule traces back to a specific steering file section (or built-in baseline)
• No contradictions between rules
• Conditional rules generated ONLY where corresponding steering file exists
• Hook event types are valid Kiro hook event types
• Security-critical hooks use fileEdited; advisory hooks use agentStop
• Every hook prompt ends with the compliance logging block (non-negotiable)
• Every hook prompt includes phase-awareness check instruction
• .compliance-state.json generated with correct initial state
• COMPLIANCE_README accurately describes what was generated
• INSTALL-GUIDE.md present in .kiro/hooks/ with noise classification per hook
• CONTEXT BUDGET CHECK: If AI-GCE generated additional steering files (Step 4b),
  count total lines across ALL always-inclusion files in .kiro/steering/.
  If total > 300 lines: WARN and convert lowest-priority generated files to fileMatch.
  AI-GCE MUST NOT push the workspace over the 300-line always-inclusion budget.
• Phase-aware hooks correctly map rules to their applicable phase
• Hook prompts include "If all rules pass, confirm compliance silently" (DX principle)

STEP 12: OUTPUT — Present Summary
──────────────────────────────────
Present generation results:

"✅ AI-GCE GENERATION COMPLETE

📦 Compliance engine (Tier 1) derived for: {project name}
📁 Workspace: {workspace root}

📊 Summary:
   • Rule categories: {n}
   • Rules generated: {total count}
   • Hooks installed: {n} (always: {x}, conditional: {y})
   • Hook split: {a} security-critical (fileEdited), {b} advisory (agentStop)
   • Audit agent: configured ({applicable rule count} rules in scope)
   • Project-init agent: configured
   • Compliance state: initialized (.compliance-state.json — Tier 1)
   • Compliance dashboard: template ready (docs/compliance-dashboard.md)
   • Compliance log: initialized
   • Hook install guide: .kiro/hooks/INSTALL-GUIDE.md

📋 Conditional enforcement activated:
   • {rule category}: because {steering file} exists
   • ...

📋 Conditional enforcement SKIPPED:
   • {rule category}: because {steering file} does NOT exist
   • ...

🎯 Compliance tier status:
   Tier 1 ✅ Active (score target: 60-70%)
   Tier 2 ⬜ Not started (criteria: 0/6 met)
   Tier 3 ⬜ Not started

🔗 Next steps:
   1. Review .governance/COMPLIANCE_README.md — how compliance works in this project
   2. Run initial audit: 'Using AI-GCE, run a compliance audit' to establish Tier 1 score
   3. Review Tier 2 readiness criteria in .compliance-state.json
   4. If brownfield: follow .governance/incremental-adoption-plan.md for progressive enforcement
   5. Begin AI-DLC workflow — Tier 1 hooks are now active

The compliance engine (Tier 1) is live."
```

---

## MODE 2: RE-DERIVATION (Incremental Update)

### When Triggered

Mode 2 is triggered when the AI-DWG workspace changes — specifically when steering files are updated. This happens when:
- AI-DWG Delta Reconciliation was run (architecture change updated steering files)
- Team manually updated a steering file to reflect a new decision
- A conditional steering file was added (e.g., `multi-tenancy.md` was created)
- AI-DWG emits a downstream signal: "Steering files updated. Affected: {list}"

### Interaction Model

1. **Triggered by:** AI-DWG signal OR user: "Re-derive compliance for updated workspace"
2. **AI identifies** which steering files changed (from signal or user input)
3. **AI maps** changed steering files → affected rules + hooks
4. **AI re-generates** ONLY affected rules and hooks (leaves unaffected ones intact)
5. **AI presents** changes: "Updated {n} rules in {m} categories; {p} hooks modified. Reason: {change}"
6. **AI applies** the updates — merging with any manual rule customizations

### Re-Derivation Flow

```
STEP 1: IDENTIFY CHANGED STEERING FILES
─────────────────────────────────────────
From downstream signal: use the provided list directly
Without signal: ask user "Which steering files changed?" or compare timestamps

STEP 2: MAP CHANGES TO AFFECTED RULES + HOOKS
───────────────────────────────────────────────
Load: re-derivation/change-detection.md for full mapping table

Quick reference — steering file → affected artifacts:

| Steering File Changed | Affected Rules | Affected Hooks |
|----------------------|---------------|----------------|
| workspace-rules.md | architecture-compliance.md | post-task-governance.json |
| architecture-principles.md | architecture-compliance.md | post-task-governance.json |
| tech-stack.md | naming-conventions.md, devops-deployment.md | naming-check.json, coverage-check.json |
| security-rules.md | security-compliance.md | security-gate-check.json |
| api-standards.md | api-first-compliance.md | api-contract-check.json |
| module-structure.md | module-boundaries.md | module-boundary-check.json |
| testing-strategy.md | code-review-gates.md | coverage-check.json |
| database-rules.md | data-governance.md | migration-safety.json |
| naming-conventions.md | naming-conventions.md | naming-check.json |
| git-workflow.md | devops-deployment.md | pre-pr-checklist.json |
| multi-tenancy.md (new) | tenant-isolation.md (NEW) | tenant-isolation-check.json (NEW) |
| resilience-standards.md | resilience-compliance.md | (resilience gate hook) |
| observability-tracing.md | observability-compliance.md | (tracing hook) |
| event-sourcing.md (new) | event-sourcing-compliance.md (NEW) | (event-sourcing hook NEW) |
| feature-flags.md (new) | feature-flag-compliance.md (NEW) | (feature-flag hook NEW) |
| brownfield-patterns.md (new) | → Triggers Mode 3 flow, not Mode 2 | |

STEP 3: RE-GENERATE AFFECTED ARTIFACTS
────────────────────────────────────────
Load: re-derivation/selective-regeneration.md

For EACH affected rule file:
• Read the updated steering file
• Re-derive the affected rules
• Check for manually added rules (marked with `<!-- custom -->` tag)
• Preserve manually added rules — only update AP-derived rules
• If conflict between new derivation and manual addition → present to user

For EACH affected hook:
• Re-derive file patterns and prompt text from updated steering
• Preserve hook mode (askAgent vs. blocking) if manually set
• Update rule references to match updated rule IDs

STEP 4: PRESENT CHANGES
─────────────────────────
Present to user:

"🔄 COMPLIANCE RE-DERIVATION COMPLETE

Triggered by: {steering file changes — list}

Updated artifacts:
┌──────────────────────────────────────┬─────────────────────────────────────────┐
│ Artifact                             │ Change                                  │
├──────────────────────────────────────┼─────────────────────────────────────────┤
│ .governance/rules/{rule file}        │ {what changed in the rules}             │
│ .kiro/hooks/{hook file}              │ {what changed in the hook}              │
│ NEW: {file}                          │ {new steering file → new rule category} │
└──────────────────────────────────────┴─────────────────────────────────────────┘

{n} rules updated | {m} hooks updated | {p} new artifacts added

⚠️ Manual customizations preserved:
   • {custom rule}: kept as-is (marked as custom)"

STEP 5: LOG RE-DERIVATION EVENT
─────────────────────────────────
Append a REDERIVATION event to compliance-log/events/{today-date}.jsonl:
{"timestamp": "{ISO-8601-UTC}", "type": "rederivation", "id": "rdr-{date}-{time}-001",
 "trigger": "{steering file change list}", "rulesUpdated": {n},
 "hooksUpdated": {m}, "newArtifacts": {p}, "reason": "{brief description}"}

This ensures the team has a clear audit trail of WHEN enforcement changed and WHY.
Without this log, a developer whose hook behavior suddenly changes has no way to
understand what happened.

STEP 6: UPDATE COMPLIANCE_README
──────────────────────────────────
If new rule categories were added: update the "What rules apply" section
If new hooks were added: update the "How do the hooks work" section
Preserve team-added content in COMPLIANCE_README
```

---

## MODE 3: BROWNFIELD INCREMENTAL ADOPTION

### What Brownfield Means for Compliance

When a workspace has `brownfield-patterns.md` in its steering, it signals:
- The codebase predates AI-DWG governance
- Existing code may have violations of the rules that AI-GCE will derive
- Teams CANNOT be blocked on day 1 for violations that existed before governance was introduced

**Key principle:** The compliance engine enforces against NEW code immediately. It acknowledges existing violations as technical debt with a formal remediation SLA. Over time, the compliance score improves as legacy violations are resolved.

**Anti-pattern to avoid:** Generating the same hooks as Mode 1 but with looser thresholds. Brownfield mode is architecturally different — it operates with a baseline, a timeline, and a distinction between "new code violations" and "legacy violations."

### Interaction Model

1. **User invokes:** "Set up incremental compliance adoption" / "Brownfield baseline scan" / "Retrofit compliance"
2. **AI reads** workspace + `brownfield-patterns.md` for specific brownfield constraints
3. **AI runs** a baseline scan — identifies existing violations
4. **AI generates** the brownfield baseline document (acknowledged violations + SLAs)
5. **AI generates** the incremental adoption plan (enforcement timeline)
6. **AI generates** compliance rules and hooks configured for new-code-only enforcement
7. **AI generates** same artifacts as Mode 1, but with brownfield-adapted behavior
8. **AI presents** the baseline summary and adoption roadmap

### Brownfield Overlay Flow

```
STEP 1: READ WORKSPACE + BROWNFIELD SIGNALS
─────────────────────────────────────────────
Read all steering files (same as Mode 1 STEP 1)
ADDITIONALLY read:
• brownfield-patterns.md → understand characterization test requirements,
  strangler-fig boundaries, legacy API compatibility rules, data migration guardrails
• Existing codebase structure → identify which modules are LEGACY vs. NEW

From brownfield-patterns.md, determine:
• Which modules/folders are LEGACY (pre-governance code)
• Which modules/folders are NEW (post-governance code)
• Legacy API compatibility constraints
• Data migration guardrails in effect

STEP 2: RUN BASELINE SCAN
────────────────────────────
Perform a non-blocking catalog of current state:
For each rule category (that would be generated in Mode 1):
• Scan existing code patterns for rule violations
• Classify each violation: LEGACY (in existing code) vs. SCOPE UNKNOWN

Produce baseline catalog:

"📊 BROWNFIELD COMPLIANCE BASELINE

Scanned: {n} modules | {m} files
Project: {project name}

By rule category:
┌─────────────────────────┬──────────────┬─────────────────────────────────────┐
│ Rule Category           │ Status       │ Notes                               │
├─────────────────────────┼──────────────┼─────────────────────────────────────┤
│ Naming conventions      │ ⚠️ {n} gaps  │ {description of pattern variations} │
│ API contract-first      │ ✅ Compliant │ Existing endpoints documented        │
│ Module boundaries       │ ⚠️ {n} gaps  │ {description of cross-boundary deps} │
│ Security gates          │ ✅ Compliant │ Auth present on all routes           │
│ ...                     │ ...          │ ...                                 │
└─────────────────────────┴──────────────┴─────────────────────────────────────┘

Overall baseline score: {x}% compliant
New code will be enforced at: 100% from day 1
Legacy code remediation target: {date} (12-week default SLA)"

STEP 3: GENERATE BROWNFIELD BASELINE DOCUMENT
──────────────────────────────────────────────
Load: templates/compliance-log/brownfield-baseline.md

Generate .governance/brownfield-baseline.md:
• Summary of existing violations per category
• Designation: ACKNOWLEDGED LEGACY TECHNICAL DEBT
• Remediation SLA per category (default: 12 weeks from governance adoption date)
• Exception: security-critical violations get 2-week SLA regardless
• Sign-off line (team lead acknowledges the baseline)

This document transforms "violations" into "acknowledged technical debt with a plan."
Without it, the team would face hundreds of immediate blocks on day 1.

STEP 4: GENERATE INCREMENTAL ADOPTION PLAN
────────────────────────────────────────────
Load: templates/compliance-log/incremental-adoption-plan.md

Generate .governance/incremental-adoption-plan.md:

Phase 1 — Immediate (Week 0, day 1):
• New code MUST comply with all rules
• Hooks active for files CREATED after governance adoption
• Baseline violations documented and tracked

Phase 2 — Early Wins (Weeks 1-4):
• Resolve security-critical legacy violations (2-week SLA)
• Resolve naming convention violations in new modules
• Enable blocking mode for hooks on NEW code only

Phase 3 — Steady Progress (Weeks 5-8):
• Resolve high-priority legacy violations
• Extend blocking hooks to recently modified files
• First compliance score review

Phase 4 — Convergence (Weeks 9-12):
• Resolve remaining acknowledged violations
• Move all hooks to full enforcement
• Final compliance audit — target: 80%+ score
• Graduate from brownfield mode: full compliance engine active

STEP 5: GENERATE RULES WITH BROWNFIELD ANNOTATIONS
────────────────────────────────────────────────────
Same as Mode 1 STEP 3, with these additions:
• Each rule file includes a "Brownfield Note" section:
  "Existing violations acknowledged in .governance/brownfield-baseline.md.
   This rule enforces NEW code only until {remediation SLA date}."
• Rules reference the incremental-adoption-plan.md for timeline

STEP 6: GENERATE HOOKS WITH BROWNFIELD CONFIGURATION
──────────────────────────────────────────────────────
Same as Mode 1 STEP 4, with these critical differences:

For hooks watching CREATED files (fileCreated events):
→ Run at full enforcement immediately (new code = must comply)

For hooks watching EDITED files (fileEdited events):
→ Run in WARN mode for legacy module paths (don't block; inform)
→ Run in ENFORCE mode for new module paths (as defined by brownfield-patterns.md)

Brownfield hook configuration pattern:
Each hook prompt for legacy modules must include:
"[BROWNFIELD MODE] This file is in a legacy module. If this is a modification to
existing legacy code, note the violation in .governance/brownfield-baseline.md.
If this is new code added to a legacy module, it MUST comply with [rule reference]."

STEP 7: GENERATE REMAINING ARTIFACTS
──────────────────────────────────────
Same as Mode 1 STEPS 5-8 (audit agent, compliance log, COMPLIANCE_README)
Ensure COMPLIANCE_README includes a "Brownfield Adoption" section explaining:
• The baseline scan concept
• How the incremental adoption plan works
• How legacy violations are tracked
• How to graduate from brownfield mode to full enforcement

STEP 8: OUTPUT — Present Brownfield Summary
─────────────────────────────────────────────

"✅ AI-GCE BROWNFIELD ADOPTION INITIALIZED

📦 Compliance engine (incremental mode) for: {project name}
📁 Workspace: {workspace root}

📊 Baseline established:
   • Overall compliance score: {x}%
   • Categories fully compliant: {n}
   • Categories with legacy violations: {m}
   • Security violations (2-week SLA): {p}
   • General violations (12-week SLA): {q}

🔒 Immediate enforcement (new code):
   • {n} hooks active for newly created files
   • All rule categories enforced for NEW code from today

⏳ Incremental enforcement (legacy code):
   • Baseline documented: .governance/brownfield-baseline.md
   • Adoption plan: .governance/incremental-adoption-plan.md
   • Full compliance target: {date}

📋 Key files:
   • .governance/brownfield-baseline.md — acknowledged legacy violations
   • .governance/incremental-adoption-plan.md — enforcement timeline
   • .governance/COMPLIANCE_README.md — how to work with this compliance engine

🔗 Next steps:
   1. Review .governance/brownfield-baseline.md — acknowledge and sign off
   2. Read .governance/incremental-adoption-plan.md — understand the timeline
   3. Begin AI-DLC workflow — new code is enforced from day 1
   4. Run weekly compliance audit to track improvement score"
```

---

## CONDITIONAL GENERATION TABLE

AI-GCE generates ONLY what the workspace justifies. This prevents generating enforcement for patterns the architecture doesn't use.

| Workspace Signal | Action | What Gets Generated |
|-----------------|:------:|---------------------|
| `multi-tenancy.md` exists | ✅ Generate | Tenant isolation rules + `tenant-isolation-check.json` hook |
| `multi-tenancy.md` absent | ❌ Skip | No tenant isolation content |
| `api-versioning.md` exists | ✅ Generate | Breaking-change rules + version compliance enforcement |
| `api-versioning.md` absent | ❌ Skip | No API versioning content |
| `resilience-standards.md` exists | ✅ Generate | Resilience pattern rules + resilience gate hook |
| `resilience-standards.md` absent | ❌ Skip | No resilience content |
| `observability-tracing.md` exists | ✅ Generate | Tracing compliance rules + span instrumentation hook |
| `observability-tracing.md` absent | ❌ Skip | No tracing content |
| `performance-standards.md` exists | ✅ Generate | Performance budget rules + regression detection |
| `performance-standards.md` absent | ❌ Skip | No performance content |
| `workflow-engine.md` exists | ✅ Generate | Workflow state-machine compliance rules |
| `workflow-engine.md` absent | ❌ Skip | No workflow engine content |
| `frontend-standards.md` exists | ✅ Generate | Frontend pattern rules + accessibility enforcement hook |
| `frontend-standards.md` absent | ❌ Skip | No frontend content |
| `event-sourcing.md` exists | ✅ Generate | Event store rules + CQRS boundary enforcement + event-sourcing hook |
| `event-sourcing.md` absent | ❌ Skip | No event sourcing content |
| `feature-flags.md` exists | ✅ Generate | Flag lifecycle rules + rollout compliance enforcement |
| `feature-flags.md` absent | ❌ Skip | No feature flag content |
| `brownfield-patterns.md` exists | ✅ Use Mode 3 | Baseline scan + incremental adoption plan + brownfield-annotated rules |
| `brownfield-patterns.md` absent | ❌ Skip brownfield path | Standard Mode 1 full enforcement from day 1 |
| Module count ≥ 3 (from module-structure.md) | ✅ Generate | Module boundary rules + `module-boundary-check.json` at full depth |
| Single module (simple project) | ⚠️ Generate at minimal | Basic boundary check (hooks still present but lightweight) |

---

## MODE 4: TIER ACTIVATION (Compliance Tier Upgrade)

### When Triggered

Mode 4 is triggered when a project is ready to advance from its current compliance tier to the next. It is NOT a new derivation — it is a progressive activation of rules and hooks that were deferred at initial generation time.

**Trigger signals:**
- User says "activate tier 2" / "activate next tier" / "upgrade compliance"
- `.compliance-state.json` shows all `nextTierReadiness.criteria` as true
- PM runs the tier activation accelerator

### Interaction Model

1. **User invokes:** "Activate next compliance tier"
2. **AI reads** `.compliance-state.json` → determine current tier and next tier
3. **AI verifies** all readiness criteria for the next tier (checks actual workspace state)
4. **AI asks** tier-specific questions (2-4 per tier — see below)
5. **AI activates** new rules and hooks for this tier
6. **AI runs** compliance audit with newly activated rules
7. **AI presents** new score, gap report, and next actions

### Tier-Specific Questions

**Activating Tier 2 (3 questions):**
- What CI pipeline type is in use? (GitHub Actions / GitLab CI / Azure DevOps / Other)
- Are all team members listed in CODEOWNERS? (If no — prompt to update first)
- Which modules have active development? (Determines domain-specific rule activation)

**Activating Tier 3 (4 questions):**
- What is the release version/tag?
- Who are the external stakeholders for sign-off?
- Which compliance frameworks apply? (SOX / GDPR / ISO 27001 / None)
- Target deployment environment? (Cloud / On-Premise / Hybrid)

### Tier Activation Flow

```
STEP 1: READ CURRENT STATE
───────────────────────────
Read .compliance-state.json:
• Current tier (1, 2, or 3)
• Tier history
• Next tier readiness criteria and their status
• Last audit score

STEP 2: VERIFY READINESS CRITERIA
────────────────────────────────────
For each criterion in nextTierReadiness.criteria:
• Check actual workspace state (don't trust cached values in state file)
• Report: "Criterion X: ✅ Met / ❌ Not met — {reason}"
• If any criteria unmet: warn but allow PM to override (full activation mode)

STEP 3: ASK TIER-SPECIFIC QUESTIONS
──────────────────────────────────────
Ask the 2-4 questions specific to this tier upgrade.
Derive everything else from workspace state — no unnecessary questions.

STEP 4: ACTIVATE NEW RULES
────────────────────────────
Load rules that belong to this tier (tagged in rule files with tier number).
For Tier 2: governance-checklist, role-isolation, steering-governance, devops-deployment
For Tier 3: security-compliance, change-management, full phase-gates

STEP 5: INSTALL NEW HOOKS
───────────────────────────
Install hooks that belong to this tier.
For Tier 2: post-task-governance, segregation-check, security-gate-check,
            enforce-module-structure, cross-module-reference-check, 
            steering-quality-check, auto-run-tests
For Tier 3: change-readiness-gate, exception-expiry-check
            (periodic-audit-trigger already installed — now runs full scan)

STEP 6: RUN COMPLIANCE AUDIT WITH NEW RULES
─────────────────────────────────────────────
Run full audit with all activated rules (Tier 1 + newly activated Tier N).
Expected: score will dip as new rules expose new gaps — this is expected and healthy.

STEP 7: UPDATE STATE FILE
───────────────────────────
Update .compliance-state.json:
• Set complianceTier to new tier number
• Add tierHistory entry with date, activatedBy, scoreAtActivation
• Update nextTierReadiness for the NEXT tier
• Update complianceScore with new audit result

STEP 8: REGENERATE COMPLIANCE DASHBOARD
─────────────────────────────────────────
Regenerate docs/compliance-dashboard.md with new tier state:
• Tier progress bars updated
• New rules inventory showing newly activated rules
• New hooks roadmap showing what was installed and what's next
• Gap report for newly discovered violations
• Updated score history

STEP 9: OUTPUT — Tier Activation Summary
──────────────────────────────────────────
"⬆️ COMPLIANCE TIER {N} ACTIVATED

Active rules:    {list of newly activated rule categories}
Active hooks:    {list of newly installed hooks}
New audit score: {score}% ({rating}) — was {previous score}%
Score delta:     {+/- change} (dip is expected as new rules expose gaps)

Top gaps from new rules:
  🔴 {critical finding 1}
  🟠 {high finding 2}
  🟡 {important finding 3}

Next tier ({N+1}) readiness: {criteria met count}/{total} criteria
Blockers: {list}

Updated: .compliance-state.json | docs/compliance-dashboard.md"
```

---

## WHAT AI-GCE DOES NOT DO

- ❌ Require manual configuration — it READS the workspace and derives everything
- ❌ Hardcode any technology — NestJS, Django, .NET, Spring Boot: all derived from `tech-stack.md`
- ❌ Generate architecture/governance steering files — that is AI-DWG's job. Exception: AI-GCE MAY generate phase/role-aware ENFORCEMENT steering (Step 4b) — compliance-specific, fileMatch-only, marked `<!-- generated by AI-GCE -->`
- ❌ Make architecture decisions — those were made in AI-ADLC and encoded in AI-DWG
- ❌ Generate application code
- ❌ Run as an interactive lifecycle with approval gates (it is a generator, not a lifecycle)
- ❌ Activate all 310+ rules on Day 0 — it uses the 3-tier progressive adoption model
- ❌ Block day 1 on brownfield violations — it BASELINES existing violations and enforces NEW code first
- ❌ Overwrite manually customized rules during re-derivation — it merges, preserving `<!-- custom -->` tags
- ❌ Work without a workspace that has `.kiro/steering/` populated — it needs steering files to read
- ❌ Require full regeneration for small workspace changes — Mode 2 (re-derivation) handles incremental updates
- ❌ Fire advisory hooks on every intermediate file save — security-critical on `fileEdited`, advisory on `agentStop`

---

## RULE DERIVATION PATTERN

This shows how a steering file decision becomes a concrete, technology-specific rule and hook.

### Example: API Contract Enforcement (NestJS workspace)

**Input from `api-standards.md`:**
```markdown
| Aspect | Approach |
|--------|----------|
| Spec format | OpenAPI 3.1 |
| Generation | Auto-generated from NestJS decorators |
| Location | /api/docs |
```

**Input from `module-structure.md`:**
```markdown
| Module | Path |
|--------|------|
| Incident | src/modules/incident/ |
| Change | src/modules/change/ |
| Asset | src/modules/asset/ |
```

**AI-GCE derives:**

Rule file (`.governance/rules/api-first-compliance.md`):
```markdown
### API-01: Contract Before Implementation
Severity: 🟠 High
Derived From: .kiro/steering/api-standards.md → "OpenAPI 3.1 spec"
Rule: Every API endpoint MUST have an OpenAPI contract defined BEFORE
      controller implementation is written.
Verification:
- [ ] For each *.controller.ts in src/modules/*/presentation/ →
      a corresponding OpenAPI spec entry exists
File Patterns: src/modules/*/presentation/**/*.controller.ts
Anti-Pattern: Creating controller files before the API contract is reviewed
```

Hook file (`.kiro/hooks/api-contract-check.json`):
```json
{
  "name": "API Contract Check",
  "version": "1.0.0",
  "when": {
    "type": "fileCreated",
    "patterns": ["src/modules/*/presentation/**/*.controller.ts"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "A controller file was created. Verify an OpenAPI contract exists for this endpoint per rule API-01 in .governance/rules/api-first-compliance.md. If the corresponding spec does not define this endpoint, warn the developer to create the API contract first before implementing the controller."
  }
}
```

**If the workspace were Django instead of NestJS:** The same derivation logic reads `tech-stack.md` ("Django"), reads `api-standards.md` (same OpenAPI 3.1 spec), and generates:
- File pattern: `**/views.py` or `**/viewsets.py`
- Different file glob — same rule concept and compliance intent

**This is why AI-GCE has zero manual configuration.** The workspace tells it everything.

### Example: Role Segregation Enforcement (Non-Architectural)

**Input from `role-isolation.md`:**
```markdown
## Segregation of Duties
| Decision Type | Approved By |
|--------------|-------------|
| Code changes | Peer + CODEOWNER |
| Security-sensitive changes | Security role |
| Steering file changes | Architect / Tech Lead |
```

**Input from `CODEOWNERS`:**
```
src/Modules/Finance/**    @finance-reviewer
src/Modules/Procurement/**  @procurement-reviewer
```

**AI-GCE derives (from built-in baseline + steering enrichment):**

Rule file (`.governance/rules/role-isolation.md`):
```markdown
### GOV-ROLE-004: Session Owner ≠ Reviewer
Severity: 🔴 Critical
Tier: 2
Derived From: .kiro/steering/role-isolation.md → "Segregation of Duties" + Built-in Baseline
Rule: The person who wrote code (Session Owner) MUST NOT be the person who
      reviews/approves the PR. CODEOWNERS assigns a different reviewer per module.
Verification:
- [ ] PR author is never the PR approver
- [ ] CODEOWNERS file maps each module to a reviewer ≠ session owner
Anti-Pattern: Same person authoring and approving a PR
```

Hook file (`.kiro/hooks/segregation-check.json`):
```json
{
  "name": "Segregation of Duties Reminder",
  "version": "1.0.0",
  "when": { "type": "postTaskExecution" },
  "then": {
    "type": "askAgent",
    "prompt": "A task was completed. Verify segregation of duties: the person who wrote this code MUST NOT be the reviewer. Check CODEOWNERS for the affected module to confirm a different person is assigned as reviewer. If all rules pass, confirm compliance silently.\n\n## Compliance Logging\nAppend to compliance-log/events/{today}.jsonl:\n{\"timestamp\":\"{ISO-8601}\",\"type\":\"check\",\"hook\":\"segregation-check\",\"trigger\":\"postTaskExecution\",\"ruleId\":\"GOV-ROLE-004\",\"ruleSeverity\":\"critical\",\"result\":\"{pass|warn}\",\"message\":\"{finding}\"}"
  }
}
```

**This example shows:** Even without technology-specific file patterns, governance rules are concrete and enforceable. The "built-in baseline" rule (author ≠ approver) is ENRICHED by steering (specific CODEOWNERS mapping) to become project-specific.

---

## KEY PRINCIPLES

1. **Read before generating.** Never assume file patterns, module paths, or technology. Read `tech-stack.md` and `module-structure.md` first.

2. **Specificity beats generality.** A hook that watches `src/modules/incident/presentation/**/*.controller.ts` is infinitely more useful than one watching `**/*.ts`.

3. **Every architectural rule traces to a steering file.** Rules without a source can't be justified to the team. Governance rules may trace to built-in baseline OR steering file (both are valid sources).

4. **Warn before blocking.** All hooks start in `askAgent` mode. Teams adopt compliance gradually. Build trust before building blockers.

5. **Brownfield is not an edge case.** Most real projects have existing code. Mode 3 is a first-class path, not an afterthought.

6. **Preserve customizations.** Manual rule additions tagged `<!-- custom -->` survive re-derivation. Teams own their compliance engine after it's generated.

7. **The compliance engine must explain itself.** COMPLIANCE_README.md is mandatory — developers must understand why hooks exist and how to respond to them.

8. **Conditional means conditional.** Never generate enforcement for patterns the architecture doesn't use. A team that doesn't use multi-tenancy should never see a tenant-isolation hook.

9. **Re-derivation is not full regeneration.** When one steering file changes, only the affected rules and hooks update. The rest stay as-is, preserving any team customizations.

10. **Score what you measure.** The compliance audit agent tracks a score. That score must be meaningful — based on applicable rules only, not a fixed total.

11. **Silence is compliance.** If all rules pass, produce no output. Hooks that report "everything is fine" on every fire train developers to ignore them. Only speak when something is wrong.

12. **Phase-aware enforcement.** Rules have phases where they become applicable. Don't fire a change-management gate during Setup phase — that's noise, not governance. Check `.compliance-state.json` before enforcing.

13. **Every hook writes to the log.** No exceptions. The compliance log is the audit trail. A hook that fires but doesn't log is invisible to the audit agent, the dashboard, and external auditors.

14. **Respect the context budget.** AI-GCE generates steering files (Step 4b). The total always-inclusion budget is ≤300 lines. If AI-GCE's generated files push over that limit, convert them to fileMatch. The compliance engine must not degrade Kiro's performance.

---

## CHECKPOINT ENFORCEMENT

AI-GCE enforces these checkpoints before declaring completion:

| Checkpoint | Requirement | Failure Action |
|------------|-------------|---------------|
| Workspace marker found | `.kiro/steering/workspace-rules.md` exists | Stop; ask user for workspace path |
| Technology identified | `tech-stack.md` readable and has technology entry | Warn; use generic file patterns as fallback |
| Module paths confirmed | `module-structure.md` readable and has module paths | Warn; scan actual folder structure as fallback |
| Hooks use real paths | All hook file patterns match actual workspace structure | Fix before completing |
| Rules have sources | Every rule references a specific steering file | Flag untraced rules; request confirmation |
| No contradictions | Rules in one category don't contradict rules in another | Resolve or flag to user |
| COMPLIANCE_README generated | `.governance/COMPLIANCE_README.md` exists and is populated | Do not complete without this |
| Brownfield baseline present | If `brownfield-patterns.md` exists, `.governance/brownfield-baseline.md` must also exist | Trigger Mode 3 if missing |

---

## DIRECTORY STRUCTURE — AI-GCE OUTPUT

When AI-GCE completes, this structure exists in the user's workspace:

```
{project-root}/
├── .kiro/
│   ├── steering/                               ← Unchanged (AI-DWG output)
│   └── hooks/                                  ← GENERATED BY AI-GCE
│       ├── INSTALL-GUIDE.md                    ← Tier-based hook installation roadmap
│       ├── session-discipline.json             ← Spec-before-code (promptSubmit)
│       ├── pre-code-spec-check.json            ← Spec gate (preToolUse/write)
│       ├── api-contract-check.json             ← API contract before controller
│       ├── module-boundary-check.json          ← Cross-module import (agentStop)
│       ├── security-gate-check.json            ← Security enforcement (fileEdited) ← Tier A
│       ├── naming-check.json                   ← Naming conventions (agentStop)
│       ├── migration-safety.json               ← DB migration safety (fileEdited) ← Tier A
│       ├── coverage-check.json                 ← Test coverage (agentStop)
│       ├── post-task-governance.json           ← DoD check (postTaskExecution)
│       ├── pre-pr-checklist.json               ← PR quality gate (userTriggered)
│       ├── periodic-audit.json                 ← Full compliance scan (userTriggered)
│       ├── sensitive-data-check.json           ← PII detection (fileEdited) ← Tier A
│       ├── domain-layer-purity.json            ← DDD purity (agentStop)
│       ├── documentation-reminder.json         ← Docs update (agentStop)
│       ├── [tenant-isolation-check.json]       ← IF multi-tenancy (fileEdited) ← Tier A
│       ├── [resilience-gate.json]              ← IF resilience-standards.md
│       ├── [tracing-check.json]                ← IF observability-tracing.md (agentStop)
│       └── [event-sourcing-check.json]         ← IF event-sourcing.md
│
├── .compliance-state.json                      ← GENERATED BY AI-GCE
│                                                 Tier tracking, readiness criteria, score history
│
├── docs/
│   └── compliance-dashboard.md                ← GENERATED by audit agent (maintained ongoing)
│
└── .governance/                                ← GENERATED BY AI-GCE
    ├── COMPLIANCE_README.md                    ← How compliance works in THIS project
    │
    ├── rules/
    │   ├── phase-gates.md                      ← ALWAYS (Tier 1 basic → Tier 3 full)
    │   ├── session-governance.md               ← ALWAYS
    │   ├── architecture-compliance.md          ← ALWAYS
    │   ├── api-first-compliance.md             ← ALWAYS
    │   ├── security-compliance.md              ← ALWAYS (Tier 3: enriched with SOX/GDPR)
    │   ├── data-governance.md                  ← ALWAYS
    │   ├── module-boundaries.md                ← ALWAYS
    │   ├── naming-conventions.md               ← ALWAYS (Tier 1)
    │   ├── code-review-gates.md                ← ALWAYS
    │   ├── devops-deployment.md                ← Tier 2+
    │   ├── error-handling-compliance.md        ← ALWAYS
    │   ├── logging-compliance.md               ← ALWAYS
    │   ├── sensitive-data-protection.md        ← ALWAYS
    │   ├── domain-context-enforcement.md       ← ALWAYS
    │   ├── governance-checklist.md             ← Tier 2+
    │   ├── role-isolation.md                   ← Tier 2+
    │   ├── steering-governance.md              ← Tier 2+
    │   ├── change-management.md                ← Tier 3+
    │   ├── [tenant-isolation.md]               ← IF multi-tenancy.md exists
    │   ├── [api-versioning-compliance.md]      ← IF api-versioning.md exists
    │   ├── [resilience-compliance.md]          ← IF resilience-standards.md exists
    │   ├── [observability-compliance.md]       ← IF observability-tracing.md exists
    │   ├── [performance-compliance.md]         ← IF performance-standards.md exists
    │   ├── [workflow-compliance.md]            ← IF workflow-engine.md exists
    │   ├── [frontend-compliance.md]            ← IF frontend-standards.md exists
    │   ├── [event-sourcing-compliance.md]      ← IF event-sourcing.md exists
    │   └── [feature-flag-compliance.md]        ← IF feature-flags.md exists
    │
    ├── agents/
    │   ├── compliance-audit-agent.md           ← Full audit spec (9-step with dashboard)
    │   └── project-init-agent.md               ← Project scaffolding (5 questions)
    │
    ├── compliance-log/
    │   ├── compliance-log-schema.md            ← JSONL schema (CHECK/EXCEPTION/REMEDIATION/AUDIT)
    │   ├── exception-workflow.md               ← Formal 5-step bypass with expiry rules
    │   └── remediation-workflow.md             ← Violation resolution with SLAs
    │
    ├── [brownfield-baseline.md]                ← IF brownfield-patterns.md exists
    └── [incremental-adoption-plan.md]          ← IF brownfield-patterns.md exists
```

---

*AI-GCE v1.0.0 | Created By: Maheri | Inspired By: awslabs/aidlc-workflows (MIT-0)*
