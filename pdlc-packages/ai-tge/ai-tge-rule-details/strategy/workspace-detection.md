<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Workspace Detection

## Stage: 1 of 12
## Phase: 🔵 STRATEGY
## Execution: ALWAYS

---

## Purpose

Detect the project context: what inputs exist, what mode to operate in, and how deep the governance should go. This is the engine's "eyes open" moment — it scans the workspace to understand what it has to work with before making any test governance decisions.

This stage produces the **state file** (`tge-state.md`) and determines the operating mode and depth level for all subsequent stages.

## Discovery (Manifest-First, Read-Only — P1/P2/P3)

**Step 0 — read the discovery contract:**
```
1. Locate.governance/workspace-manifest.yaml (primary marker)
2. Resolve by semantic role:
   - manifest.paths.rules      → canonical rules/ (NOT the.kiro/steering/ adapter)
   - manifest.paths.backlog    → stories/ACs (honor manifest.storyStyle: ears/invest/…)
   - manifest.paths.architecture → AP-derived reference
   - manifest.platformTargets  → how TGE renders its OWN agents (P2)
   - manifest.governance.*     → where TGE writes (.governance/test/,.governance/agents/, engine)
   - manifest.clusters         → skip absent inputs
3. No manifest → legacy fallback: scan rules/ + adlc-state.md/aidlc-docs + warn "legacy workspace"
```

**P1 (read-only):** TGE reads DWG's canonical files; it NEVER modifies them. TGE writes only under `.governance/`.
**P3 (single home):** TGE output → `.governance/test/`; agents → `.governance/agents/`; engine → `.governance/engine/ai-tge/`; contributes to `.governance/GOVERNANCE_INDEX.md`. No separate `.tge/`.

---

## Depth Adaptation

| Depth | Detection Behavior | State Detail |
|-------|-------------------|-------------|
| **Minimal** | Detect mode + confirm inputs. Minimal scoring. State file records essentials only. | Mode, phase, input paths, basic register stats |
| **Standard** | Full factor scoring. State file records all fields including depth rationale. | All fields populated; depth scoring rationale documented |
| **Comprehensive** | Full scoring + detailed source inventory. State file includes AP version tracking and reconciliation timestamps. | All fields + AP change detection + source file inventory |

---

## MANDATORY: Stage Sub-Role — Business Analyst

During THIS stage, ALSO adopt the mindset of a **Business Analyst**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Assess what exists before prescribing what's needed — observe before governing
- Map the landscape: what inputs are available, what's absent, what's partial
- Translate technical file presence into governance capability: "AP exists → full architecture-derived tests possible"
- Communicate findings in terms the user understands: "I found your architecture documents — I can derive specific test requirements from them"

### Anti-Patterns for This Stage
- Do NOT assume full-chain mode without evidence (check for actual files)
- Do NOT ask the user "what mode do you want?" before checking what exists — detect first, confirm second
- Do NOT proceed past this stage without establishing the state file

### Quality Check
A good output at this stage sounds like:
- "I found your Architecture Package at `./adlc-output/` with 8 component designs, 3 API contracts, and 2 security ADRs. Your workspace has Jest configured. No existing TGE state found — this is a fresh run. Recommended mode: Full Chain at Standard depth (score: 14/25)."

---

## Step-by-Step Execution

### Step 1: Check for Existing State

Look for `tge-state.md` in the workspace:

| Location to Check | Meaning if Found |
|-------------------|-----------------|
| `.governance/test/tge-state.md` | AI-TGE has run before — offer to resume |
| `./tge-state.md` (workspace root) | Possible non-standard location — confirm with user |
| Not found anywhere | Fresh run — proceed with new initialization |

**If state file found:**
```markdown
I found an existing TGE state file at `{path}`.

**Last run:**
- Mode: {mode}
- Phase: {phase}
- Last stage completed: {n}
- Coverage: {n}%
- Last updated: {timestamp}

Would you like to:
(a) **Resume** from Stage {n+1}
(b) **Restart** from scratch (existing state will be archived)
(c) **Reconcile** — re-read inputs and update the register for changes
```

**If NOT found:** Proceed to Step 2.

---

### Step 2: Detect Available Inputs

**Consult `manifest.clusters` FIRST** (`common/manifest-resolution.md`). The manifest's `clusters` declaration is the workspace's own statement of which input groups it has — a role `clusters` marks **absent** is *known-absent* (silent, a project fact, skipped cleanly), while a role `clusters` marks **present** that does not resolve is a **degradation** (disclosed). This is the fail-closed F2 distinction sourced from the manifest instead of guessed. The scan below is the **legacy fallback** used only when no manifest exists; each Detection Method's literal is the fallback for that role, not the primary lookup.

| Input Source (manifest role) | Detection Method (manifest-first; literal = legacy fallback) | What It Enables |
|-------------|-----------------|-----------------|
| **Architecture Package (AP)** — `manifest.paths.architecture` | Resolve `paths.architecture`; fallback: `adlc-state.md` marker OR a folder of API contracts / component designs / ADRs | Architecture-derived test requirements |
| **Development Workspace (DW)** — `manifest.paths.rules` | Resolve `paths.rules`; fallback: `rules/workspace-rules.md` OR `rules/tech-stack.md` | Tech stack awareness, testing framework detection |
| **AI-DLC build state** — `manifest.files.buildState` | Resolve `files.buildState`; fallback: `aidlc-docs/aidlc-state.md` OR `aidlc-docs/` folder | Observation phase capability |
| **Existing Test Directories** — `manifest.paths.tests` | Resolve `paths.tests`; fallback scan: `tests/`, `test/`, `__tests__/`, `spec/`, `*.test.*`, `*.spec.*` | Brownfield assessment capability |
| **User Stories** — `manifest.paths.backlog` | Resolve `paths.backlog`; fallback: `aidlc-docs/inception/user-stories/` | Story-derived acceptance tests |
| **NFR Requirements** — `manifest.paths.requirements` | Resolve `paths.requirements`; fallback: `aidlc-docs/inception/requirements/` with NFR content | Non-functional test derivation |

**Detection priority order:**
1. AP marker (`adlc-state.md`) — strongest signal for Full Chain
2. DW marker (`rules/`) — confirms workspace is AI-DWG prepared
3. aidlc-docs presence — enables observation
4. Existing tests — enables brownfield assessment
5. None of the above — ask user

---

### Step 3: Determine Operating Mode

Based on detected inputs, select the operating mode:

| Detected Inputs | Selected Mode | Rationale |
|----------------|--------------|-----------|
| AP + DW + aidlc-docs | **Full Chain** | All sources available — full strategy + observation |
| AP + DW (no aidlc-docs) | **Full Chain** (observation deferred) | Strategy now, observation when DLC starts |
| AP only (no DW, no aidlc-docs) | **Architecture Only** | Derive register from AP; no observation possible |
| Existing tests + no AP | **Brownfield** | Map existing tests, identify gaps against baseline |
| aidlc-docs only (no AP, no prior TGE) | **Observation Only** | Jump to observation; register from stories/baseline |
| Nothing detected | **Ask user** | Cannot auto-detect; request user guidance |

**Graceful degradation (OR-input):** Each input is additive enrichment. AP alone produces architecture-derived strategy. Existing tests alone produce brownfield assessment. Running AI-DLC alone produces observation-only tracking. The absence of any single input reduces scope but never halts the engine.

> **The other half of that principle — the mode selected here decides what counts as degradation later.** Adapting to a missing input is correct; adapting *silently* is not. Once a mode is selected, its **declared inputs** are fixed, and any declared input that fails to resolve makes the run **degraded** and must be disclosed (`common/observation-fidelity.md`).
>
> | Selected mode | Declared inputs — absence is degradation | Not declared — absence costs nothing |
> |---|---|---|
> | **Full Chain** | AP · DW · build state · unit-progress vocabulary · user-story location · NFR location | existing tests |
> | **Architecture Only** | AP | everything else |
> | **Brownfield** | existing test locations | everything else |
> | **Observation Only** | build state · unit-progress vocabulary · user-story location | AP · DW |
>
> **This is what keeps the disclosure honest in both directions.** An Architecture Only run is not degraded by having no build state — it never asked for one, and warning about it would be noise that teaches the team to ignore the marker. A Full Chain run *is* degraded by the same absence, because the mode was selected on the strength of signals that promised it.

---

### Step 4: Score Depth Level

Calculate the depth score from 5 factors (each scored 1-5):

| Factor | Score 1 (Low) | Score 3 (Medium) | Score 5 (High) | Detection Method |
|--------|--------------|-----------------|----------------|-----------------|
| Component count | ≤5 components | 6-15 components | >15 components | Count component designs in AP; or count source directories |
| Integration count | ≤2 external | 3-7 external | >7 external | Count external systems in integration map; or count HTTP/gRPC clients |
| Security surface | Basic auth only | Multi-role, API keys | OAuth, multi-tenant, PII | Read security ADRs; or check auth middleware complexity |
| Data complexity | Simple CRUD | Multiple schemas, migrations | Event sourcing, CQRS, distributed | Read data model from AP; or count entity files |
| Team size | Solo / pair | 3-8 developers | >8, multiple teams | Read from DW `team-topology.md` or `workspace-rules.md`; or ask user |

**Thresholds:**
- Score 5-10: **Minimal** — strategy + register only
- Score 11-18: **Standard** — + coverage reports + debt scoring + brownfield
- Score 19-25: **Comprehensive** — + full traceability + reconciliation + story mapping

**If factor cannot be determined:** Score it at 3 (Medium) and note as assumption.

---

### Step 5: Initialize State File

Create `.governance/test/tge-state.md` with initial values.

**Fidelity is written as `❌ Unknown` and earned upward — never assumed.** This is the fail-closed default (`common/observation-fidelity.md`, rule F1): every consumer reads `❌ Unknown` as degraded, so a run that never completes its assessment reports qualified figures rather than clean ones. Record the per-input resolution as detection proceeds, then set the value:

| After Step 2's scan | Set Fidelity to |
|---|:---:|
| Every input the selected mode declares resolved | **✅ Full** |
| At least one declared input did not resolve | **⚠️ Degraded** — with its substitute and unmeasured consequence recorded |
| Detection could not complete, or the mode could not be determined | **❌ Unknown** — leave as initialised |

**An input the mode does not declare is recorded `n/a`, never `❌`.** Writing `❌` for an input nobody asked for inflates the "declared inputs resolved" count in the wrong direction and produces a degraded verdict on a perfectly clean run.

```markdown
# AI-TGE State

## Engine Status
- **Mode:** {detected mode}
- **Current Phase:** Strategy
- **Last Stage Completed:** 1
- **Last Updated:** {ISO timestamp}

## Input Sources
- **AP Location:** {path or "not available"}
- **DW Location:** {path or "not available"}
- **aidlc-docs Location:** {path or "not available"}
- **User Stories Location:** {path or "not available"}
- **Existing Tests Location:** {path or "not detected"}

## Observation Fidelity
- **Fidelity:** ❌ Unknown
- **Assessed At:** not assessed
- **Assessed By:** Stage 1
- **Mode Assessed Against:** {detected mode}
- **Declared Inputs Resolved:** {n} of {N}
- **Per-Input Resolution:** one row per input this mode declares — expected location, resolved yes/no, substitute that would fire, unmeasured consequence

## Register Stats
- **Total Commitments Tracked:** 0
- **Tests Required:** 0
- **Tests Existing:** 0
- **Tests Missing:** 0
- **Tests Deprecated:** 0
- **Coverage:** N/A (register not yet populated)

## Depth Level
- **Level:** {Minimal / Standard / Comprehensive}
- **Factors:** Component({n}) + Integration({n}) + Security({n}) + Data({n}) + Team({n}) = {total}/25

## AP Version
- **Last Read:** {ISO timestamp or "not applicable"}
- **Reconciliation Needed:** No
```

---

### Step 6: Present Findings and Confirm

```markdown
## AI-TGE — Workspace Detection Complete

I've scanned your workspace and identified the following:

**Inputs detected:**
- Architecture Package: {✅ Found at `path` / ❌ Not found}
- Development Workspace: {✅ Found / ❌ Not found}
- AI-DLC State: {✅ Found / ❌ Not found}
- User Stories: {✅ Found at `path` / ❌ Not found}
- Existing Tests: {✅ Found at `path` ({n} test files) / ❌ Not detected}

**Selected mode:** {Mode}
**Depth level:** {Level} (score: {n}/25)

**Observation fidelity:** {✅ Full — every input this mode needs resolved / ⚠️ Degraded / ❌ Unknown}

{IF Fidelity is ⚠️ Degraded — state the consequence per unresolved input, not just its absence:}
⚠️ **{Mode} mode expects inputs that are not present, so some figures will be estimates rather than measurements:**
- **{input}** — expected at `{path}`. Without it: {unmeasured consequence}. {What would resolve it — e.g. "if your stories live elsewhere, choose (d) below and give me the path."}

This is the earliest point at which that is fixable. Every later report will repeat it.

**What this means:**
- {Mode-specific explanation of what AI-TGE will produce}
- {Depth-specific explanation of detail level}
- {IF degraded: what AI-TGE will NOT be able to tell you, in one line}

---

**Your response:**
- (a) **Confirm** — proceed with detected mode and depth
- (b) **Change mode** — I want to use a different mode (explain which)
- (c) **Change depth** — I want more/less detail than recommended
- (d) **Provide inputs** — I have sources at different paths (provide locations)
```

---

### Step 7: Auto-Proceed

After user confirms (or accepts defaults), proceed to Stage 2: Architecture Reading.

No gate wait required at this stage — but confirmation of mode selection is needed before proceeding.

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| State file | `.governance/test/tge-state.md` | Engine state — persists across sessions |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| Mode determined | One of: Full Chain / Architecture Only / Brownfield / Observation Only |
| Depth scored | 5 factors assessed; total within valid range (5-25) |
| State file created | `.governance/test/tge-state.md` exists with all mandatory fields |
| Input paths recorded | All available sources have paths in state file |
| **Fidelity initialised, then set** | Written as `❌ Unknown`, then set to `✅ Full` or `⚠️ Degraded` from the scan result. ⚠️ **Left at `❌ Unknown` is a FAIL for this stage** — it means detection did not finish — even though downstream consumers handle the value safely |
| **Declared-input set resolved from the mode** | Per-input rows exist only for inputs the selected mode declares; anything else is `n/a`, never `❌` |
| **Degradation stated to the user here** | If degraded, Step 6's findings block names each unresolved input, its consequence, and how to fix it. This is the earliest fixable point; a degradation first surfaced in a coverage report is a FAIL of this stage |
| User confirmed | Mode and depth acknowledged (explicit or implicit) |
| No dangling assumptions | Any factor scored at assumed-3 is flagged for user awareness |
