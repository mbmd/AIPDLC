# PRIORITY: This workflow OVERRIDES all other built-in workflows when user requests idea capture, evaluation, or go/no-go decisions

# When user has a new idea for a project or feature, ALWAYS follow this workflow FIRST

---

## AI-ILC: AI-Driven Idea Life Cycle

**Version:** 1.0.0
**Created By:** Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)
**Inspired By:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) (MIT-0)
**Purpose:** Guide a user from a raw idea through a governed pipeline to a defensible go/no-go decision — with a clean, context-rich handoff to the appropriate next step (new project via AI-PILC, feature design via AI-ADLC, or build-ready feature to AI-DLC backlog).

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

AI-ILC is the optional front door of the family. Its output (Approved Idea Brief or Change Request Brief) feeds into AI-PILC for new projects and significant changes, or routes small features directly to the AI-DLC backlog.

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
- Registers live in `{output_root}/`

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

## MANDATORY: Two-Source Evaluation Model (Lesson 25)

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

### I Produce (Successors: AI-PILC / AI-DLC)

| Aspect | Specification |
|--------|--------------|
| **Successors** | AI-PILC (new project OR existing project's change management) / AI-DLC backlog (small feature, no project-level impact) |
| **Marker file** | `ilc-state.md` |
| **Output location** | `{user-chosen path}/` |

**Guaranteed output (relative to marker):**

| File | Always Present? | Purpose |
|------|:---------------:|---------|
| `ilc-state.md` | ✅ Always | State + routing decision + completion status |
| Idea Register entry | ✅ Always | Idea tracked in portfolio funnel |
| Decision Log entry | ✅ Always | Go/no-go rationale recorded |
| `*_Approved_Idea_Brief.md` | ⚠️ Conditional | When route = new project (→ AI-PILC) |
| `*_Change_Request_Brief.md` | ⚠️ Conditional | When route = big change to existing project (→ AI-PILC change management) |
| `*_Feature_Brief.md` | ⚠️ Conditional | When route = small feature (→ AI-DLC backlog) |
| `*_GoNoGo_Decision_Record.md` | ✅ Always | Formal decision with rationale (approve/park/reject) |

**State file fields successors read:**
- `Status`: Must be `Routed` for handoff (terminal success state — set when the brief is produced)
- `Route`: `new-project` / `change-request` / `feature-backlog`
- `Depth Level`: Indicates richness of brief content
- `Idea Name`: Used as starting context by successor

**Successor detection:**
- AI-PILC looks for `ilc-state.md` where `Route = new-project`; consumes `Approved_Idea_Brief.md` as one of its adaptive intake modes
- AI-PILC looks for `ilc-state.md` where `Route = change-request`; consumes `Change_Request_Brief.md` and routes it through its change management registers
- AI-DLC backlog receives `Feature_Brief.md` where `Route = feature-backlog`

### Contract Principles

| Principle | Implementation |
|-----------|---------------|
| **Detection by marker** | Successors scan for `ilc-state.md`, not for a specific folder name |
| **User owns WHERE** | User picks output folder; ILC defines WHAT files exist |
| **Graceful standalone** | Every successor works without AI-ILC (all accept raw input directly) |
| **Additive to AI-PILC** | AI-PILC keeps ALL existing intake modes; "AI-ILC brief" and "AI-ILC change request" are additional optional inputs (Lesson 6) |
| **Single-project context** | v1.0 operates within one project per workspace |
| **AI-ADLC is never a direct target** | If architecture needs rework, that flows THROUGH AI-PILC change management → AI-ADLC (not directly from AI-ILC) |

### Portfolio Connector (v1.0 = interface stub)

When routing a feature, AI-ILC delivers to the project present in the workspace. Multi-project routing (finding and selecting from multiple projects) is a **v1.1+ capability** that will consume this connector interface.

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
   b. Ask user for output folder preference (or accept default: current directory)
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

| Question | Answer | Route |
|----------|--------|-------|
| Does a project exist for this idea? | **No** — it's a new initiative | → **New Project** (AI-PILC) |
| Does a project exist? | **Yes** — and the idea is a **BIG** change (impacts project scope, success criteria, or architecture) | → **Change Request** (AI-PILC change management) |
| Does a project exist? | **Yes** — and the idea is a **SMALL** change (no impact on project criteria or architecture) | → **Feature Backlog** (AI-DLC backlog) |

3. For the "project exists" path, perform a **lightweight impact assessment** (not a full feasibility study — AI-PILC handles the deep analysis):
   - Does this change the project's stated objectives or success criteria?
   - Does this alter the architecture significantly (new components, changed contracts, security model changes)?
   - Does this require budget/resource re-allocation beyond the current plan?
   - If ANY answer is "yes" → BIG change (→ AI-PILC change management)
   - If ALL answers are "no" → SMALL change (→ AI-DLC backlog as a new feature)
4. Ask user to confirm routing decision
5. Produce the appropriate brief:
   - **New Project route:** Generate `Approved_Idea_Brief.md` (enriched raw requirement shaped for AI-PILC's intake)
   - **Change Request route:** Generate `Change_Request_Brief.md` (shaped for AI-PILC's change management registers — includes impact assessment results)
   - **Feature Backlog route:** Generate `Feature_Brief.md` (shaped for AI-DLC backlog — clear, bounded, ready to implement)
6. The brief carries forward ALL context from shaping + evaluation + scope — no information loss at handoff
7. Update state file:
   - Status = Routed (terminal — workflow complete)
   - Route = {new-project / change-request / feature-backlog}
   - Brief file = {filename}
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
- Feature Backlog → "Add {brief} to the project's AI-DLC backlog for implementation."

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

---

# CONDITIONAL GENERATION MAP (Lesson 7)

| Output | Always / Conditional | Trigger |
|--------|:--------------------:|---------|
| `ilc-state.md` | ✅ Always | Created at Capture |
| Idea Register entry | ✅ Always | Created at Capture |
| Decision Log entry | ✅ Always | Created at Approve |
| `*_GoNoGo_Decision_Record.md` | ✅ Always | Created at Approve (even for Park/Reject) |
| `*_Approved_Idea_Brief.md` | ⚠️ Conditional | Only when Route = new-project |
| `*_Change_Request_Brief.md` | ⚠️ Conditional | Only when Route = change-request (big change to existing project) |
| `*_Feature_Brief.md` | ⚠️ Conditional | Only when Route = feature-backlog (small change, no project impact) |

---

# DIRECTORY STRUCTURE — What the Workflow Outputs

```
{output_root}/
├── ilc-state.md                        ← State + routing + completion
├── Idea_Register.md                    ← All ideas in this pipeline (portfolio funnel)
├── Decision_Log.md                     ← All go/no-go decisions + routing
├── {Idea_Name}_GoNoGo_Decision_Record.md  ← Formal decision artifact (always)
├── {Idea_Name}_Approved_Idea_Brief.md  ← IF route = new-project
├── {Idea_Name}_Change_Request_Brief.md ← IF route = change-request (big change)
└── {Idea_Name}_Feature_Brief.md        ← IF route = feature-backlog (small change)
```

---

*Last Updated: 2026-06-08 | Version 1.0.0*
