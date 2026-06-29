---
inclusion: manual
---
<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# PRIORITY: This workflow OVERRIDES all other built-in workflows when activated by key `_ILC_` or when the user requests idea capture, evaluation, or go/no-go decisions

# Activate via the explicit key `_ILC_`, OR when the user has a new idea for a project or feature — then ALWAYS follow this workflow FIRST. See "Activation & Multi-Package Isolation" below before asserting priority in a shared workspace.

---

## AI-ILC: AI-Driven Idea Life Cycle

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**Purpose:** Guide a user from a raw idea through a governed pipeline to a defensible go/no-go decision — with a clean, context-rich handoff to the appropriate next step (new project via AI-PILC, feature backlog via AI-POLC, or change request back to AI-PILC change management). When AI-FLO (router) is available, it dispatches; otherwise AI-ILC hands off directly to the target.

**Methodology Alignment:** Stage-gate innovation process / Portfolio management best practices / Lean validation
**Interaction Model:** Human-in-the-loop at every stage gate; adaptive depth per idea complexity.

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

    AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG ──► AI-DLC v1 (build) ¹
    Own it      Design UX   Design it   Prepare it       ▲
                                                         │
                        AI-POLC ⇄ AI-DLC v1 (back-and-forth)┘
                AI-DLC v1 ⇢ AI-UXD+AI-POLC (feedback)

    AI-GCE  +  AI-TGE  ──── alongside AI-DLC v1 (continuous quality) ────►
    Guard it   Test it

╚═════════════════════════════════════════════════════════════════════════╝
  ¹ AI-DLC v1 = Amazon's open-source build lifecycle (not ours; we feed it).
```

| Layer | Package | Type | Input | Output |
|-------|---------|------|-------|--------|
| Portfolio | **AI-ILC** ² | Interactive workflow (lifecycle) | Raw idea | Approved Idea Brief / Feature Brief |
| Portfolio | **AI-PILC** | Interactive workflow (lifecycle) | Raw requirement | Project Initiation Package (PIP) |
| Portfolio | **AI-PPM** ³ | Adaptive portfolio engine | Multiple PIPs + Approved Idea Briefs | Portfolio register + cross-project prioritization & governance |
| Edge | **AI-FLO** ³ | Router / orchestration engine | Any package output marker | Routing decision + handoff to next package/layer |
| Project | **AI-POLC** ³ | Interactive workflow (lifecycle) | PIP | Product Backlog Package (PBP) |
| Project | **AI-UXD** ³ | Interactive workflow (lifecycle) | PIP + PBP | UX Design Package (UXP): personas/journeys, IA, user flows, design system + tokens, accessibility baseline |
| Project | **AI-ADLC** | Interactive workflow (lifecycle) | PIP + PBP + UXP | Architecture Package (AP) |
| Project | **AI-DWG** | One-time generator | AP + PBP + UXP | Ready-to-code development workspace (DW) |
| Project | **AI-GCE** | Adaptive governance engine | DW (AI-DWG output) | Compliance enforcement layer |
| Project | **AI-TGE** | Test governance engine | DW / build artifacts | Test governance & quality layer |
| Project | **AI-DLC v1** ¹ | Interactive workflow (lifecycle) | DW + GCE + User Stories (from AI-POLC) | Working Software |

> ¹ **AI-DLC v1** ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)) is NOT our product. Our chain produces the workspace AI-DLC v1 consumes.
> ² **AI-ILC** is an **optional pre-stage** (the funnel before the funnel). The chain still works without it for users who start at AI-PILC. `⇢` denotes the optional link.
> ³ All packages in this table are **built**. AI-PPM (portfolio engine), AI-FLO (router), AI-POLC (product ownership lifecycle), and AI-UXD (UX design lifecycle) were the last four — completed June 2026. Within the Project layer, **AI-POLC, AI-UXD, and AI-ADLC run sequentially** (POLC→UXD→ADLC) — each feeds the next, culminating at AI-DWG which receives all three outputs (AP + PBP + UXP). **AI-GCE and AI-TGE run alongside AI-DLC v1** as continuous quality engines; **AI-POLC ⇄ AI-DLC v1** exchange backlog/acceptance throughout delivery; and **AI-DLC v1 runtime feedback flows back to both AI-UXD and AI-POLC**. Feedback loops (ADLC→POLC cost/risk, ADLC→UXD constraints) provide iterative refinement without changing the forward sequence.

AI-ILC is the optional front door of the family. Its output (Approved Idea Brief, Change Request Brief, or Feature Brief) routes via AI-FLO (when available) to the appropriate successor: AI-PILC for new projects and significant changes, AI-POLC for features/backlog items, or AI-DLC v1 as a fallback for small features.

---

## Activation & Multi-Package Isolation

**Explicit activation key:** `_ILC_`
Type `_ILC_` in any prompt to activate this workflow. An explicit key is treated as a **direct user order to switch** — it wins over keyword matching and every sibling package immediately.

**Active-package status key:** `_ACTIVE_`
Type `_ACTIVE_` at any time and the assistant reports which AI-* package is currently active (and its state-marker status). This is a read-only check — it changes nothing and never triggers a switch.

**Keyword activation (fallback):** This workflow also activates when the user requests **idea capture, evaluation, or a go/no-go decision** specifically — shaping a raw idea into an approved brief. It does NOT claim generic "initiation", "design", "backlog", "governance", or "workspace" requests — those belong to sibling packages.

**Switching rule — NON-NEGOTIABLE: a package switch NEVER happens without a direct user order or explicit confirmation.**
1. **Direct order:** the user types an explicit activation key (`_ILC_`, or a sibling `_XXX_` key). Treat this as the order — switch immediately, no confirmation needed.
2. **Otherwise, check for an active sibling:** scan for any sibling `*-state.md` (e.g. `pilc-state.md`, `adlc-state.md`, `polc-state.md`, `uxd-state.md`) whose status is not "complete". If one exists, that package is active — do NOT take over. Ask first: "AI-PILC is active — switch to AI-ILC? (yes / no)" and proceed only on explicit confirmation.
3. **Ambiguity:** if a request could match more than one installed package by keyword, ask which workflow to run rather than guessing.
4. **Announce every switch:** on any switch (via key or confirmation), the **FIRST line of that response MUST name the now-active package** — e.g. `Active package: AI-ILC`.
5. This package's own marker is `ilc-state.md`; sibling packages extend it the same courtesy when it is active.

---

## Adaptive Workflow Principle

The workflow adapts to the idea, not the other way around.

The AI model intelligently assesses what depth is needed based on:

1. Idea clarity and maturity (vague notion vs. well-formed concept)
2. Idea scale (small feature vs. new strategic initiative)
3. Organizational context (single team vs. cross-enterprise)
4. Risk profile (low-stakes improvement vs. high-investment bet)

**Depth Levels:**
- **Minimal** — Idea is clear, scope is small, risk is low → streamlined evaluation, fast go/no-go
- **Standard** — Normal complexity, some shaping needed → full pipeline with structured scoring
- **Comprehensive** — High stakes, ambiguous, or multi-stakeholder → detailed analysis, multiple evaluation dimensions, explicit value articulation

---

## MANDATORY: Dynamic Stage-Based Persona Selection

AI-ILC does NOT use a single fixed persona. Each stage is authored in the voice of the expert who owns it, with a specialist sub-role lens layered on top.

> **Note for users:** The lead persona at most stages is `#persona-product-manager`, which serves as BOTH the Product Manager and **Innovation Manager** role. The persona file is titled "Product Manager / Innovation Manager" and explicitly covers idea pipeline management, structured evaluation, go/no-go decisions, prioritization, and portfolio-funnel awareness. If your organization calls this role "Innovation Manager," "Portfolio Manager," or "Idea Owner" — it's the same persona, fully covered.

### Stage → Lead Persona Map

| Stage | Lead Persona | Sub-Role Layered | Why |
|-------|-------------|-----------------|-----|
| **Capture** | `#persona-product-manager` | — | Fast, low-ceremony — no specialist lens needed |
| **Shape** | `#persona-product-manager` | `#persona-subrole-business-analyst` | Requirements decomposition, ambiguity detection, gap identification |
| **Evaluate** | `#persona-product-manager` | `#persona-subrole-financial-analyst` | Value scoring, cost-of-not-doing, investment framing |
| **Scope** | `#persona-process-designer` | `#persona-subrole-resource-planner` | WBS-like boundary setting, effort estimation, dependencies |
| **Approve** | `#persona-product-manager` | `#persona-subrole-risk-analyst` | Risk-aware go/no-go: challenge assumptions, assess feasibility risks |
| **Route & Handoff** | `#persona-product-manager` | `#persona-subrole-change-manager` | Impact assessment (big vs. small change), stakeholder/adoption lens |

### Domain Detection (Additional Supporting Lens)

When the idea's **subject domain** emerges during shaping, the sub-role above may be supplemented or swapped for a domain-specific sub-role at the Approve and Route stages (capped at primary + one sub-role per the loading guide):

| Idea subject | Sub-role to prefer | Primary fallback |
|---|---|---|
| Architecture, system boundaries, decomposition | `#persona-subrole-systems-engineer` | `#persona-cto-architect` |
| Security, identity, trust boundaries | `#persona-subrole-security-architect` | `#persona-cto-architect` |
| Data modelling, schema, storage | `#persona-subrole-data-architect` | `#persona-cto-architect` |
| API / integration design | `#persona-subrole-api-designer` | `#persona-cto-architect` |
| CI/CD, workspace, repo structure | `#persona-subrole-workspace-architect` | `#persona-devops-platform-engineer` |
| Governance, compliance, hooks | `#persona-subrole-audit-specialist` | `#persona-compliance-governance` |
| Test strategy, QA, validation | _(no sub-role)_ | `#persona-qa-test-engineer` |
| Licensing, IP, commercial strategy | _(no sub-role)_ | `#persona-ip-licensing-counsel` |
| Project management, PMO governance | `#persona-subrole-change-manager` | `#persona-pmo-project-manager` |

**Resolution rule:** Lead = stage default; Sub-role = stage-specific (table above) OR idea's domain (when more relevant at Approve/Route); capped at primary + one sub-role. See `.kiro/steering/persona-loading-guide.md` → "Dynamic / Stage-Based Selection" for full resolution logic.

---

## MANDATORY: Rule Details Loading

CRITICAL: When performing any stage, you MUST read and use relevant content from rule detail files. Check these paths in order and use the first one that exists:

- `.ai-ilc/ai-ilc-rule-details/` (if user ran AI-assisted setup)
- `.kiro/ai-ilc-rule-details/` (Kiro IDE setup)
- `ai-ilc-rule-details/` (standalone setup)

All subsequent rule detail file references are relative to whichever rule details directory was resolved above.

**Common Rules:** ALWAYS load common rules at workflow start:

- Load `common/process-overview.md` for workflow overview
- Load `common/session-continuity.md` for session resumption guidance
- Load `common/question-format-guide.md` for question formatting rules
- Load `common/content-validation.md` for content validation requirements
- Reference these throughout workflow execution

---

## MANDATORY: Welcome Message

CRITICAL: When starting ANY idea-management request, display the welcome message.

1. Load the welcome message from `common/welcome-message.md`
2. Display the complete message to the user
3. This should only be done ONCE at the start of a new workflow
4. Do NOT load this file in subsequent interactions

---

## MANDATORY: State Management

The workflow maintains state across sessions via `{output_root}/ilc-state.md`.

At workflow start:
1. Check if `ilc-state.md` exists in the output directory
2. If YES → load state, confirm position with user, resume from last completed stage
3. If NO → fresh start; create state file after Capture stage begins

State file tracks:
- Current stage
- Completed stages with timestamps
- Idea identity (name, proposed type, domain)
- Evaluation score (once scored)
- Routing decision (once approved)
- Pending decisions
- Depth level

**CRITICAL:** Update state file immediately after EVERY stage completion.

---

## MANDATORY: Registers

The workflow creates and maintains two registers:

1. **Idea Register** — Every idea submitted to this pipeline (status, score, decision, dates)
2. **Decision Log** — Every go/no-go decision, routing decision, and park/reject rationale

**Rules:**
- Registers are created at first use (during Capture stage)
- Entries are added in real-time as they arise (not batched)
- Each entry is sequentially numbered and never deleted
- Registers live in `{output_root}/` (flat — shared across all ideas)

---

## MANDATORY: Output Folder Structure

AI-ILC organizes output so a workspace with many ideas stays navigable, **without** encoding status in folder names (which would force files to move as status changes and break successor detection). The structure follows two principles:

1. **Shared artifacts stay flat** at `pdlc-ws/ideas/` — the state marker, the Idea Register, and the governance spine. These are cross-idea and never move.
2. **Per-idea artifacts live in a per-idea subfolder** keyed by the idea's **stable Register ID** (never by status). Status is read from the Idea Register (its status-sectioned tables) and from each artifact's `Status` field — not from the folder.

### Fixed Output Root — `pdlc-ws/ideas/`

**The output root is ALWAYS `pdlc-ws/ideas/` relative to the workspace root.** This is a deterministic, non-negotiable path — the user is NOT asked where to place output. This aligns with `OUTPUT_AND_STATE_CONTRACT.md` §4, which designates `pdlc-ws/ideas/` as the pre-project, multi-idea funnel area.

**Rationale:** removing path-selection authority from the user eliminates ambiguity in successor detection, ensures consistent workspace topology across all AI-ILC installations, and aligns with the Always-On Rule (§3 of the multi-project contract — no layout variance, no adaptive activation, no user-customizable root).

**Brownfield exception:** if the workspace already contains AI-ILC output in a non-standard location (older flat layout), detect it on first run and inform the user: "Existing ILC output found at `{path}`. AI-ILC now uses `pdlc-ws/ideas/` as the standard location. I'll continue operating in `pdlc-ws/ideas/` — you may migrate existing artifacts at your convenience." Never force-move existing files.

```
pdlc-ws/ideas/                                    ← FIXED output root (workspace-root-relative)
├── ilc-state.md                          ← shared marker (one active idea at a time)
├── Idea_Register.md                      ← shared funnel view (status at a glance)
├── management_framework/                 ← shared governance spine (flat, per contract)
│   ├── MANAGEMENT_FRAMEWORK.md
│   ├── Decision_Log.md
│   └── Lessons_Learned.md
└── {NNN}-{idea-slug}/                    ← per-idea subfolder, keyed by zero-padded Register ID
    ├── Idea_Statement.md                 ← working doc (Shape)
    ├── {NNN}-{idea-slug}_Approved_Idea_Brief.md   ← (or _Change_Request_Brief / _Feature_Brief)
    └── {NNN}-{idea-slug}_GoNoGo_Decision_Record.md
```

**Naming rules:**
- `{NNN}` = the idea's Register ID, zero-padded to 3 digits (`001`, `002`, …). This is a **stable domain key** — the one folder partition the family allows (it never encodes mutable status; cf. the `{Project ID}/` partition pattern).
- `{idea-slug}` = the idea name lower-cased, spaces → hyphens, punctuation stripped.
- The subfolder is created at Capture (Stage 1) and **never renamed** for the life of the idea — even when the idea is parked, rejected, or routed. Status changes update the Register and the artifacts' `Status` field, not the folder.

**Successor detection is preserved:** successors still scan for `ilc-state.md` at `pdlc-ws/ideas/`. The state file's **`Brief File`** field carries the **relative path** to the brief inside the per-idea subfolder (e.g. `001-fleet-tracking/001-fleet-tracking_Approved_Idea_Brief.md`), and the Idea Register stores each idea's **Folder** path. Consumers resolve the brief from the marker — they never guess the folder.

**Provenance:** per `NAMING_AND_OWNERSHIP.md` §5.2, per-idea artifacts carry front-matter (`generatedBy: AI-ILC`, `ownership: user`) and a `Status` field so classification lives in metadata, not in the path.

---

## MANDATORY: Question Format

When asking questions at any stage, follow the structured format:

```
### Q-{nn}: {Question Title}

**Context:** {Why this question matters}

**Options:**
- (a) {Option A description}
- (b) {Option B description}
- (c) {Option C description}

**Recommended:** Option {x}
**Rationale:** {Why this is recommended}

**Your Decision:** _[awaiting input]_
```

- Always provide a recommended answer with rationale
- User can accept recommendation, choose another option, or propose alternative
- Log all decisions in Decision Log immediately upon confirmation

---

## MANDATORY: Two-Source Evaluation Model

The Evaluate stage uses a **two-source model**:

1. **Default baseline rubric** (built into the package) — provides universal evaluation criteria that work for any idea in any domain. Ships as the standard scoring model. If the enterprise provides no customization, this rubric still produces a meaningful score.

2. **Enterprise customization** (optional override) — the enterprise can provide their own scoring criteria, weights, or thresholds. When present, enterprise criteria **override** baseline defaults on a per-criterion basis. When absent, baseline stands alone.

**Resolution logic:**
- Enterprise provides custom criteria → use custom (overrides baseline)
- Enterprise is silent on a criterion → use baseline default
- No enterprise customization at all → full baseline rubric (still functional)

---

## MANDATORY: Chain Contract

AI-ILC is contract-aware — it knows it is an optional pre-stage in the AI-* chain.

### I Read (Predecessor: None)

AI-ILC is the optional first entry point. It accepts raw ideas in any format:
- Verbal description ("I have this idea...")
- One-liner or subject line
- Document (brief, proposal, email, feature request)
- Existing backlog item to elevate/evaluate

No input marker file. No predecessor package.

### I Produce (Successors: AI-PILC / AI-POLC / AI-FLO / AI-DLC v1)

| Aspect | Specification |
|--------|--------------|
| **Successors** | AI-PILC (new project OR change management) / AI-POLC (feature → product backlog) / AI-FLO (router dispatch, when available) / AI-DLC v1 (small feature fallback) / AI-PPM (portfolio awareness, informational) |
| **Marker file** | `ilc-state.md` |
| **Output location** | `pdlc-ws/ideas/` (fixed, workspace-root-relative; shared artifacts flat; per-idea artifacts under `{NNN}-{idea-slug}/`) |

**Guaranteed output (relative to marker):**

| File | Always Present? | Purpose |
|------|:---------------:|---------|
| `ilc-state.md` | ✅ Always | State + routing decision + completion status (flat at root) |
| Idea Register entry | ✅ Always | Idea tracked in portfolio funnel (flat at root) |
| Decision Log entry | ✅ Always | Go/no-go rationale recorded (in `management_framework/`) |
| `{NNN}-{slug}/*_Approved_Idea_Brief.md` | ⚠️ Conditional | When route = `new-project` (→ AI-PILC) |
| `{NNN}-{slug}/*_Change_Request_Brief.md` | ⚠️ Conditional | When route = `change-request` (→ AI-PILC change management) |
| `{NNN}-{slug}/*_Feature_Brief.md` | ⚠️ Conditional | When route = `feature` (→ AI-POLC / fallback AI-DLC v1) |
| `{NNN}-{slug}/*_GoNoGo_Decision_Record.md` | ✅ Always | Formal decision with rationale (approve/park/reject) |

> Per-idea artifacts live in the idea's `{NNN}-{slug}/` subfolder (see "MANDATORY: Output Folder Structure"). The exact relative path to the brief is recorded in the state file's `Brief File` field, so successors resolve it from the marker rather than guessing the folder.

**State file fields successors read:**
- `Status`: Must be `Routed` for handoff (terminal success state — set when the brief is produced)
- `Route`: `new-project` / `change-request` / `feature` / `portfolio-inform`
- `Brief File`: relative path to the brief inside the per-idea subfolder (e.g. `001-{slug}/001-{slug}_Approved_Idea_Brief.md`)
- `Depth Level`: Indicates richness of brief content
- `Idea Name`: Used as starting context by successor
- `Project ID`: If routing to an existing project, carries the target project's ID (for AI-PPM correlation)

**Successor detection (forward-compatible):**
- **`Route = new-project`:** AI-FLO dispatches to AI-PILC (if AI-FLO available) → fallback: AI-PILC directly reads `ilc-state.md` and consumes `Approved_Idea_Brief.md` via Mode E intake
- **`Route = change-request`:** AI-PILC consumes `Change_Request_Brief.md` and routes through its change management registers
- **`Route = feature`:** AI-POLC consumes `Feature_Brief.md` into the Product Backlog Package (if AI-POLC available) → fallback: AI-DLC v1 backlog receives `Feature_Brief.md` directly
- **`Route = portfolio-inform`:** AI-PPM is notified of the new project/feature for portfolio register awareness (if AI-PPM available) → fallback: informational only (no action if AI-PPM absent)

> **Forward-compatibility:** AI-FLO, AI-POLC, and AI-PPM are all built. When installed in a workspace, AI-FLO acts as the preferred dispatch layer and AI-POLC as the preferred feature intake. In workspaces where they are not yet installed, routing falls through to the direct successor (AI-PILC for projects, AI-DLC v1 for features). The `Route` field in `ilc-state.md` carries the *intent*; the consuming package resolves the *target* based on what's available.

### Contract Principles

| Principle | Implementation |
|-----------|---------------|
| **Detection by marker** | Successors scan for `ilc-state.md`, not for a specific folder name |
| **Fixed output root** | Output always goes to `pdlc-ws/ideas/` (workspace-root-relative); eliminates path ambiguity for successors |
| **Graceful standalone** | Every successor works without AI-ILC (all accept raw input directly) |
| **Additive to AI-PILC** | AI-PILC keeps ALL existing intake modes; "AI-ILC brief" and "AI-ILC change request" are additional optional inputs |
| **Forward-compatible routing** | Route values target packages that may not exist yet; fallback logic ensures handoff always succeeds |
| **Single-project context** | v1.0 operates within one project per workspace |
| **AI-ADLC is never a direct target** | If architecture needs rework, that flows THROUGH AI-PILC change management → AI-ADLC (not directly from AI-ILC) |
| **AI-POLC preferred for features** | Feature ideas go to AI-POLC (product backlog owner) when available; AI-DLC v1 is the fallback (OR-input) |

### Portfolio Connector (v1.0 = informational awareness)

When a new project is approved, AI-ILC emits `Route = new-project` + optionally `portfolio-inform`. If AI-PPM is available, it reads the approved idea brief and registers the new project in the portfolio. If AI-PPM is absent, the `portfolio-inform` route is a no-op (informational intent, no blocking). Multi-project routing (finding and selecting from multiple projects) is a **v1.1+ capability** that will consume the AI-FLO router.

### Downstream Signal

AI-ILC does not implement downstream signaling. The brief is a one-time handoff — once the idea is approved and routed, the successor consumes the brief as static input. If the user revisits and modifies the idea after the successor has started, they must re-initiate from the updated brief.

---

# WORKFLOW STAGES

---

## Stage 1: Capture (ALWAYS EXECUTE)

**Lead persona:** Product/Innovation Manager
**Purpose:** Log the raw idea fast — before it's lost or loses context.

1. Check for existing `ilc-state.md` — if found, load and offer to resume
2. If fresh start:
   a. Ask user: "What's the idea?" (accept any format: verbal, one-liner, document)
   b. Create `pdlc-ws/ideas/` folder if it doesn't exist
   c. Create `ilc-state.md` with initial configuration
   d. Create/update Idea Register (add new entry: status = Captured)
3. Capture the raw idea verbatim (preserve the user's language)
4. Auto-detect:
   - Idea scale signal: small feature / medium initiative / large strategic
   - Idea clarity: vague notion / partially formed / well-articulated
   - Recommended depth level: Minimal / Standard / Comprehensive
5. Present capture summary:

```
✅ Idea captured: "{idea_title}"
📊 Scale signal: {small/medium/large}
🔍 Clarity: {vague/partial/well-articulated}
📐 Recommended depth: {Minimal/Standard/Comprehensive}
📁 Output: pdlc-ws/ideas/{NNN}-{idea-slug}/

Ready to shape this idea. Continue? [Yes / Adjust depth / Stop here]
```

6. **Gate:** User confirms → proceed to Stage 2

**Detail file:** `idea-lifecycle/capture.md`

---

## Stage 2: Shape (ALWAYS EXECUTE — Adaptive Depth)

**Lead persona:** `#persona-product-manager` · **Sub-role:** `#persona-subrole-business-analyst`
**Purpose:** Turn a vague notion into a structured problem/solution statement.

**Depth adaptation:**
- Minimal: 3 quick questions (problem, who benefits, rough size)
- Standard: Full structured shaping (problem, current state, desired state, capabilities, boundaries)
- Comprehensive: Deep shaping with prior art analysis, stakeholder mapping, and dependency identification

1. Load `idea-lifecycle/shape.md` for detailed steps
2. Guide the user through structured shaping questions:
   - What problem does this solve? (precise problem statement)
   - Who benefits and how? (target persona + value)
   - What would it do? (key capabilities — 3-5 bullets)
   - What would it NOT do? (explicit boundaries)
   - Where does it sit? (context: standalone, part of an existing system, new initiative)
3. Detect the idea's **domain** → activate supporting persona for subsequent stages
4. Produce a structured **Idea Statement** (internal working document — not the final brief)
5. Present to user for review and iteration
6. Update state file: Stage 2 complete, domain identified
7. Update Idea Register: status = Shaped

**Gate:** User approves shaped idea → proceed to Stage 3

**Detail file:** `idea-lifecycle/shape.md`

---

## Stage 3: Evaluate (ALWAYS EXECUTE — Adaptive Depth)

**Lead persona:** `#persona-product-manager` · **Sub-role:** `#persona-subrole-financial-analyst`
**Purpose:** Score the idea consistently and articulate its strategic value.

**Depth adaptation:**
- Minimal: Quick 7-criterion score + 1-line rationale per criterion
- Standard: Full scoring + 4-dimension value analysis
- Comprehensive: Full scoring + value analysis + competitive positioning + cost-of-delay analysis

1. Load `idea-lifecycle/evaluate.md` for detailed steps
2. Score against the evaluation rubric (7 criteria, 1-5 each):
   - Problem Clarity
   - User Need
   - Strategic Fit (replaces "Family Fit" for standalone use)
   - Differentiation
   - Feasibility
   - Reusability / Breadth of applicability
   - Chain Value / Ecosystem contribution
3. Apply decision thresholds:
   - 30-35: Strong Proceed
   - 25-29: Proceed
   - 20-24: Conditional (needs rework)
   - 15-19: Park
   - 7-14: Reject
4. Check automatic blockers:
   - Any criterion = 1 → must be addressed
   - Both "Strategic Fit" AND "Differentiation" ≤ 2 → reject consideration
   - "Feasibility" ≤ 2 → technically unachievable
5. If score meets threshold (≥ 25), produce **Value Analysis**:
   - Value to the User
   - Value to the Organization / Ecosystem
   - Value Differentiators
   - Cost of NOT doing this
6. Present score + value analysis to user
7. Update state file: Stage 3 complete, score recorded
8. Update Idea Register: status = Evaluated, score = {n}/35

**Gate:** User confirms evaluation outcome (Proceed / Park / Reject) → if Proceed, continue to Stage 4. If Park/Reject, log decision and close.

**Detail file:** `idea-lifecycle/evaluate.md`

---

## Stage 4: Scope (CONDITIONAL — Execute if Evaluate = Proceed)

**Lead persona:** `#persona-process-designer` · **Sub-role:** `#persona-subrole-resource-planner`
**Purpose:** Define what's in vs. out for the initiative, and estimate rough effort.

**Depth adaptation:**
- Minimal: In/out list + t-shirt size effort estimate
- Standard: Structured scope with v1.0 vs. later, dependencies, and risks
- Comprehensive: Detailed scope with phased delivery, resource implications, and explicit trade-offs

1. Load `idea-lifecycle/scope.md` for detailed steps
2. Define scope:
   - Included (what MUST be in the first version)
   - Deferred (explicitly out for now — with rationale)
   - Dependencies (what must exist or be true)
   - Risks (what could go wrong)
3. Estimate effort:
   - T-shirt size (S / M / L / XL)
   - Rough timeline (if applicable)
4. Present scope to user for agreement
5. Update state file: Stage 4 complete
6. Update Idea Register: status = Scoped

**Gate:** User agrees on scope → proceed to Stage 5

**Detail file:** `idea-lifecycle/scope.md`

---

## Stage 5: Approve (CONDITIONAL — Execute if Scoped)

**Lead persona:** `#persona-product-manager` · **Sub-role:** `#persona-subrole-risk-analyst`
**Purpose:** Explicit go/no-go decision with recorded rationale.

1. Load `idea-lifecycle/approve.md` for detailed steps
2. Present the approval summary:
   - Idea name + one-line description
   - Score: {n}/35 ({band})
   - Scope summary (in/out/effort)
   - Value proposition (from Value Analysis)
   - Key risks
   - Recommended decision
3. Ask for explicit decision:
   - **APPROVE** — proceed to routing and handoff
   - **PARK** — valid idea, not now (record revisit date)
   - **REJECT** — doesn't fit (record rationale)
4. Produce **Go/No-Go Decision Record** (always, regardless of outcome):
   - Decision, rationale, date, decision-maker
   - Score summary
   - Conditions (if any)
5. Log decision in Decision Log
6. Update state file: Stage 5 complete, decision recorded
7. Update Idea Register: status = Approved / Parked / Rejected

**Gate:** If Approved → proceed to Stage 6. If Parked/Rejected → workflow ends (clean close with audit trail).

**Detail file:** `idea-lifecycle/approve.md`

---

## Stage 6: Route & Handoff (CONDITIONAL — Execute if Approved)

**Lead persona:** `#persona-product-manager` · **Sub-role:** `#persona-subrole-change-manager`
**Purpose:** Determine where this approved idea goes, and produce the right brief for that destination.

1. Load `idea-lifecycle/route-handoff.md` for detailed steps
2. Determine routing (impact-driven):

| Question | Answer | Route | Preferred Target | Fallback (if target absent) |
|----------|--------|-------|------------------|-----------------------------|
| Does a project exist for this idea? | **No** — it's a new initiative | `new-project` | AI-FLO → AI-PILC | AI-PILC directly |
| Does a project exist? | **Yes** — and the idea is a **BIG** change (impacts scope, success criteria, or architecture) | `change-request` | AI-PILC change management | *(always available)* |
| Does a project exist? | **Yes** — and the idea is a **SMALL** change (no project-level impact) | `feature` | AI-POLC (Product Backlog Package) | AI-DLC v1 backlog |

3. For the "project exists" path, perform a **lightweight impact assessment** (not a full feasibility study — AI-PILC handles the deep analysis):
   - Does this change the project's stated objectives or success criteria?
   - Does this alter the architecture significantly (new components, changed contracts, security model changes)?
   - Does this require budget/resource re-allocation beyond the current plan?
   - If ANY answer is "yes" → BIG change → route = `change-request`
   - If ALL answers are "no" → SMALL change → route = `feature`
4. **Portfolio awareness:** If route = `new-project`, additionally set `portfolio-inform` flag so AI-PPM (if available) registers the new project in the portfolio. This is informational — it does not block the primary route.
5. Ask user to confirm routing decision
6. Produce the appropriate brief:

> **Key design decision: forward-compatible routing.** Routes declare intent for packages that don't exist yet, with graceful fallback to existing packages. No package breaks if AI-FLO/AI-POLC/AI-PPM are absent — the route value carries the *intent*; the consuming layer resolves the *target* based on what's available in the workspace.

   - **`new-project` route:** Generate `{NNN}-{slug}/{NNN}-{slug}_Approved_Idea_Brief.md` (enriched raw requirement shaped for AI-PILC's intake Mode E)
   - **`change-request` route:** Generate `{NNN}-{slug}/{NNN}-{slug}_Change_Request_Brief.md` (shaped for AI-PILC's change management registers — includes impact assessment results)
   - **`feature` route:** Generate `{NNN}-{slug}/{NNN}-{slug}_Feature_Brief.md` (shaped for AI-POLC product backlog intake; fallback: AI-DLC v1 backlog — clear, bounded, ready to elaborate)
6. The brief carries forward ALL context from shaping + evaluation + scope — no information loss at handoff
7. Update state file:
   - Status = Routed (terminal — workflow complete)
   - Route = {new-project / change-request / feature}
   - Portfolio Inform = {true / false}
   - Brief file = {relative path under the idea folder}
   - Target Project ID = {project_id, if routing to an existing project; else "new"}
8. Update Idea Register: status = Routed, route = {destination}
9. Log routing decision in Decision Log
10. Present completion message:

```
🎉 AI-ILC WORKFLOW COMPLETE

📋 Idea: "{idea_name}"
✅ Decision: APPROVED
🔀 Route: {destination}
📄 Brief: {brief_filename}

{Route-specific next-step guidance:}
- New Project → "Run AI-PILC on {brief} to initiate the project."
- Change Request → "Submit {brief} to AI-PILC change management for the existing project."
- Feature Backlog → "Add {brief} to the project's AI-DLC v1 backlog for implementation."

Idea Register and Decision Log updated. Audit trail complete.
```

**Detail file:** `idea-lifecycle/route-handoff.md`

---

# KEY PRINCIPLES

1. **Every idea deserves a fair hearing.** The pipeline exists to evaluate, not to dismiss. Even rejected ideas get a recorded rationale.
2. **Go/No-Go is always explicit.** Never let an idea drift into limbo. It is Approved, Parked (with a revisit date), or Rejected (with rationale). All three are valid, governed outcomes.
3. **Context carries forward.** The brief handed to the successor contains everything learned during shaping, evaluation, and scoping. No "cold start" for the next step.
4. **The user decides, the AI advises.** Every gate presents a recommendation with rationale — but the user makes the call.
5. **Audit trail from day one.** Every score, every decision, every routing choice is logged. This is governance, not a suggestion box.
6. **Standalone is first-class.** This package delivers full value without the rest of the AI-* family. The chain integration is a bonus, not a requirement.
7. **Dynamic expertise.** The right persona leads each stage; the idea's domain pulls in the right support. No one-size-fits-all voice.
8. **Parked is not dead.** Parked ideas have a revisit date and stay in the register. They re-enter the pipeline when conditions change.

### Provenance Requirement (contracts/NAMING_AND_OWNERSHIP.md §5.2/§5.3)

All output files generated by this package MUST include provenance front-matter:

**For `.md` artifacts:**
```yaml
---
generatedBy: AI-ILC
generatedVersion: {version}
source: {upstream-doc-path}
generatedOn: {ISO-date}
ownership: generated | hybrid | user
---
```

Templates use `{placeholder}` syntax for these fields. See Naming & Ownership Contract §5.2–§5.3 for full schema and ownership values.

---

# CONDITIONAL GENERATION MAP

| Output | Always / Conditional | Trigger |
|--------|:--------------------:|---------|
| `ilc-state.md` | ✅ Always | Created at Capture |
| Idea Register entry | ✅ Always | Created at Capture |
| Decision Log entry | ✅ Always | Created at Approve |
| `{NNN}-{slug}/*_GoNoGo_Decision_Record.md` | ✅ Always | Created at Approve (even for Park/Reject) |
| `{NNN}-{slug}/*_Approved_Idea_Brief.md` | ⚠️ Conditional | Only when Route = new-project |
| `{NNN}-{slug}/*_Change_Request_Brief.md` | ⚠️ Conditional | Only when Route = change-request (big change to existing project) |
| `{NNN}-{slug}/*_Feature_Brief.md` | ⚠️ Conditional | Only when Route = feature (small change, no project impact) |

---

# DIRECTORY STRUCTURE — What the Workflow Outputs

```
pdlc-ws/ideas/                                      ← FIXED output root (workspace-root-relative)
├── ilc-state.md                            ← State + routing + completion (shared marker, flat)
├── Idea_Register.md                        ← All ideas in this pipeline (portfolio funnel, flat)
├── management_framework/                   ← Shared governance spine (flat)
│   ├── MANAGEMENT_FRAMEWORK.md
│   ├── Decision_Log.md                     ← All go/no-go decisions + routing
│   └── Lessons_Learned.md
└── {NNN}-{idea-slug}/                      ← Per-idea subfolder (keyed by stable Register ID)
    ├── Idea_Statement.md                   ← Working doc (Shape)
    ├── {NNN}-{idea-slug}_GoNoGo_Decision_Record.md   ← Formal decision artifact (always)
    ├── {NNN}-{idea-slug}_Approved_Idea_Brief.md      ← IF route = new-project
    ├── {NNN}-{idea-slug}_Change_Request_Brief.md     ← IF route = change-request (big change)
    └── {NNN}-{idea-slug}_Feature_Brief.md            ← IF route = feature (small change)
```

> Folder is keyed by the **stable** Register ID — never renamed for status changes. Status is tracked in the Idea Register (status-sectioned tables) and each artifact's `Status` field, not in the folder name. The shared marker, register, and spine stay flat so successors detect them at `pdlc-ws/ideas/`.

---

# POST-WORKFLOW: Agent Installation

After the AI-ILC workflow completes its first full run in a workspace, install the governance agent so the user can validate future idea briefs independently.

### Agent Artifacts to Install

| Artifact | Destination | Action |
|----------|-------------|--------|
| `idea-quality-agent.md` | `.kiro/agents/` | Copy from `templates/agents/` |
| Shortcut rules block | `.kiro/steering/workspace-rules.md` | Append `<!-- BEGIN AI-ILC AGENT SHORTCUTS -->` block (or replace if exists) |
| Agent registry entries | `.governance/AGENT_REGISTRY.md` | Create file if absent; append AI-ILC entries if exists |
| Agent guide section | `.governance/AGENT-GUIDE.md` | Create file if absent; append AI-ILC section if exists |

### Installation Logic

1. **Agent file:** Copy `templates/agents/idea-quality-agent.md` to `.kiro/agents/idea-quality-agent.md`. Populate `{version}` with current AI-ILC version and `{ISO-date}` with today's date.

2. **Shortcut block:** Check `.kiro/steering/workspace-rules.md` for `<!-- BEGIN AI-ILC AGENT SHORTCUTS -->` marker:
   - If found → replace the block (between BEGIN and END markers)
   - If not found → append the block from `templates/agents/shortcut-rules-block.md`

3. **Agent registry:** Check for `.governance/AGENT_REGISTRY.md`:
   - If absent → create with header + AI-ILC row: `| ILC-AG-01 | idea-quality-agent | Audit | IQC__ | 1 | AI-ILC | Active |`
   - If exists → append AI-ILC row (between `<!-- custom -->` markers if team rows exist)

4. **Agent guide:** Check for `.governance/AGENT-GUIDE.md`:
   - If absent → create with header + AI-ILC section from `templates/agents/agent-guide.md`
   - If exists → append AI-ILC section (between `<!-- BEGIN AI-ILC AGENT GUIDE SECTION -->` markers)

### When to Install

- **First run only.** If `.kiro/agents/idea-quality-agent.md` already exists, skip installation (agent already present from a prior run).
- **Re-derivation safe.** If the agent file exists but the version differs, update it (replace file, preserve any `<!-- custom -->` blocks if present).

---

*Last Updated: 2026-06-12 | Version 1.0.0*


---

## Gate Contract

> Conforms to `GATE_PROTOCOL.md` protocolVersion 1.2.0 · interfaceVersion 1.0

### Gate-Out — What AI-ILC GUARANTEES When Complete

```yaml
emits-type: idea-decision@1
visibility: internal
marker: ilc-state.md
payloadRoot: pdlc-ws/projects/{projectId}/ilc/
guarantees:
  - status == complete
  - ideaId
  - projectId
  - decisionOutcome           # approved | rejected | deferred | merged
  - ideaBrief                 # Approved Idea Brief / Feature Brief / CR Brief present
  - lifecycleDisposition      # new-project | feature | change-request
```

### Gate-In — What AI-ILC REQUIRES to Start

```yaml
consumes:
  - type: capability-input@^1       # satisfiable externally (e.g., EAFLC capability roadmap)
    optional:  [capabilityContext, strategicAlignment]
on-missing-all: standalone    # accepts raw idea from user (P4)
strictness-default: warn
```

> No type-specific mandatory payload — AI-ILC starts from a raw idea. Universal floor (status==complete + id) enforced by marker integrity (GATE_PROTOCOL §18).

### Visibility Note

- `idea-decision` is `internal` — consumed only by AI-PILC, AI-POLC, and AI-PPM within PDLC.
- `capability-input` is the **external seam-in** — declared in `FAMILY_INTERFACE.md` Tier 1.
