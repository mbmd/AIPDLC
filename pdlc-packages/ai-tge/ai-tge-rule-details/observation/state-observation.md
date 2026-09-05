<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# State Observation

## Stage: 7 of 12
## Phase: 🟢 OBSERVATION
## Execution: ALWAYS (in Observation Phase)

---

## Purpose

Read the AI-DLC build state — resolved via `manifest.files.buildState` (`common/manifest-resolution.md`), with `aidlc-docs/aidlc-state.md` as the legacy fallback — to identify newly completed units and stages. For each completed unit, check whether its required tests now exist in the source code. Update the register with current existence status. This is the engine's continuous monitoring heartbeat.

This stage runs every time AI-TGE is invoked during the Observation phase — it's the entry point for tracking build progress against test obligations.

---

## Depth Adaptation

| Depth | Observation Scope | Update Detail |
|-------|------------------|--------------|
| **Minimal** | Check aidlc-state for completed units. Verify test file existence (filename match only). Update register status. | Binary: test file exists / doesn't exist |
| **Standard** | Check completed units + read test file names/describe blocks. Match to specific register entries. Track new tests written since last observation. | Per-entry status update + delta report |
| **Comprehensive** | Full scan: completed units + test content analysis + assertion verification. Detect partial coverage (test exists but doesn't cover all assertions). Track test quality, not just existence. | Detailed verification + partial coverage flags + quality notes |

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS stage, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in terms of state changes and events — what changed since last observation?
- Focus on detecting WHAT'S NEW: new test files, new test blocks, new code completions
- Be efficient: don't rescan everything if state file shows only 1 unit completed since last check
- Report deltas, not full state: "Since last observation, 3 tests were added, covering 2 Critical gaps"

### Anti-Patterns for This Stage
- Do NOT block on this stage — observation is continuous, never gated
- Do NOT report full register status every time — only report changes
- Do NOT modify test files — observation is read-only
- Do NOT re-score risks here — that's Stage 12 (Debt Reassessment)

### Quality Check
A good output at this stage sounds like:
- "Observation cycle complete. 2 units completed since last check (UserService Code Gen, OrderService Build-and-Test). 4 new test files detected. Register updated: 6 entries moved from Missing → Exists. 2 Critical gaps remain (SEC-001: auth bypass, DATA-003: transaction integrity)."

A good **degraded** output at this stage sounds like:
- "Observation cycle complete — DEGRADED. The build state was not found at its expected location, so unit completion was inferred from file modification timestamps rather than read. 4 changed test files detected; whether they correspond to completed units is unverified. Register updated: 6 entries moved from Missing → Exists on filename match. Coverage now 71% ⚠️ — treat as a lower bound, since a completed unit whose files were not touched is invisible to this cycle."

**Note what the degraded example does NOT do.** It does not refuse to report, and it does not hedge every sentence. It reports the same facts, names the substitute once, and qualifies the specific figures the substitute affects. A degraded run is still useful — it is only dishonest when it is silent.

---

## Step-by-Step Execution

### Step 1: Read AI-DLC Build State

Resolve the build state through the **build-engine layout descriptor** (`common/manifest-resolution.md` → "Build-Engine Layout Descriptor"), which gives — per build method — the `stateFile` location AND the `progressVocabulary` (for `aidlc`, the Construction slugs `functional-design`, `nfr-requirements`, `nfr-design`, `infrastructure-design`, `code-generation`, `build-and-test`, `ci-pipeline`). The legacy `aidlc-docs/aidlc-state.md` literal is the fallback of last resort only. When the descriptor cannot resolve, this is the disclosed `⚠️ Degraded` read handled below — never a silent read of the literal or a timestamp heuristic:

| State Field | What It Tells Us |
|-------------|-----------------|
| Units completed | Which features/components have been built |
| Current stage per unit | Code Gen → Build-and-Test → Review → Complete |
| Stories completed | Which user stories are now accepted |
| Last build timestamp | When the last code was produced |

**Extract:** List of units/features completed SINCE last TGE observation (compare timestamps with `tge-state.md → Last Updated`).

#### Step 1a: If the build state does not resolve — split by cause BEFORE proceeding

These two look identical at the filesystem and are **not** the same finding. Classify first (`common/observation-fidelity.md`, fail-closed rule F2):

| Cause | Which modes | Fidelity | Behaviour |
|---|---|:---:|---|
| **This mode does not declare a build state** — there is no build engine to observe | Architecture Only · Brownfield | unaffected — record `n/a` | Observe test-file existence only. **Silent.** Nothing was substituted, because nothing was expected. |
| **This mode declares a build state and it did not resolve** | Full Chain · Observation Only | **⚠️ Degraded** | Proceed on the substitute below **and disclose it.** |

**MANDATORY when degraded — record all four facts before deriving any figure:**

| Fact | Value |
|---|---|
| **Input** | Build state |
| **Expected at** | `aidlc-docs/aidlc-state.md` |
| **Substitute used** | Scan for test files changed since the last observation; use file modification timestamps as a proxy for build progress |
| **Unmeasured consequence** | Unit completion is **inferred from file timestamps, not read**. A completed unit whose files were not touched is invisible; a touched file that completes nothing registers as progress. |

Write these into `tge-state.md → Observation Fidelity` (Step 6), carry them into the coverage report (Stage 9), and state them in this stage's report (Step 7) — **all three destinations, not one.**

**NEVER present a timestamp-derived delta as a build-progress delta without the marker.** The substitute answers a different question — *which files changed* rather than *which units completed* — and the two agree only by coincidence.

#### Step 1b: The unit-progress vocabulary is a second declared input, and it fails differently

It is a **token set, not a path**, so it fails when `aidlc-state.md` **is** present but its per-unit stage names are not the expected set. A path-existence check passes and the observation is still wrong — which is why this input needs its own classification rather than riding on Step 1a's.

| Cause | Fidelity | Behaviour |
|---|:---:|---|
| The state file's per-unit stage names match the expected vocabulary | unaffected | Read per-unit stage position normally |
| The state file resolved, but its per-unit stage names are an unrecognised set | **⚠️ Degraded** | Treat every completion as generic. Record: substitute = *completions treated as generic*; unmeasured = *per-unit stage position unavailable, so stage-conditional register updates cannot fire* |

---

#### Step 1c: Under `aidlc` — read v2's traceability outcome, do NOT re-run it

When the build method is `aidlc` and v2's `traceability` / `upstream-coverage` sensors are present, AI-TGE **reads v2's computed traceability outcome and persists the derived status into its register entries** — it does **not** re-run the traceability check itself (`common/traceability-ownership.md`, merged item 27). Re-running a check v2 already ran double-counts the outcome, the same failure the observability read-and-persist boundary (AI-GCE item 21) established. A register entry whose traceability v2 has computed is marked from v2's result (`source: aidlc-traceability-sensor`), not re-derived by a second scan. The register is still **kept** — AI-TGE owns it under every build method; only the *computation* of traceability moves to v2 under `aidlc`. If v2's outcome does not resolve, that is a disclosed **degraded** read (Step 1a's fidelity discipline), never a silent re-run. Under the four non-`aidlc` methods no v2 sensors exist, so AI-TGE computes traceability itself, as normal.

---

### Step 2: Identify Register Entries Affected

For each newly completed unit, find its register entries:

```markdown
## Affected Register Entries

Unit completed: {unit_name}
Components involved: {component list}

| Register Entry | Level | Type | Previous Status | Action Needed |
|:-------------:|:-----:|:----:|:---------------:|:--------------|
| API-001 | Integration | Contract | Missing | Check for test existence |
| BL-003 | Unit | Business Logic | Missing | Check for test existence |
| BASE-API-01 | Integration | Contract | Missing | Check for test existence |
```

---

### Step 3: Scan for Test Existence

For each affected register entry, check whether a matching test now exists:

**Scanning approach (by depth):**

| Depth | Method |
|-------|--------|
| Minimal | Check if test file for the component exists (e.g., `user-service.test.ts` exists) |
| Standard | Read test file names and describe/it blocks; match to register entry test names |
| Comprehensive | Read test content; verify assertions match what the register requires |

**Matching criteria (same as Stage 4 brownfield):**
- Exact name match (High confidence)
- Semantic match (Medium confidence)
- Component + type match (Low confidence)

---

### Step 4: Update Register Status

For each entry checked:

| Finding | New Status | Register Update |
|---------|:----------:|----------------|
| Matching test found (High confidence) | `Exists` | Add verification note: `Verified: {file_path} ({timestamp})` |
| Matching test found (Medium confidence) | `Exists (unverified)` | Add note: `Possible match: {file_path} — verify manually` |
| No test found | `Missing` (unchanged) | No change; remains in debt scorecard |
| Test found but failing | `Failing` | Add note: `Test exists but failing: {file_path}` |

---

### Step 5: Calculate Delta

```markdown
## Observation Delta — {ISO timestamp}

**Period:** {last observation timestamp} → {now}
**Derived from:** {the build state file / ⚠️ the file-modification-time substitute — DEGRADED}
**Units completed:** {n} {⚠️ inferred, not read — if degraded}
**Register entries checked:** {n}

### Changes This Cycle

| Metric | Before | After | Delta |
|--------|:------:|:-----:|:-----:|
| Tests Existing | {n} | {n} | +{n} |
| Tests Missing | {n} | {n} | -{n} |
| Tests Failing | {n} | {n} | {±n} |
| Coverage % | {n}% | {n}% | +{n}%{⚠️ if degraded} |

### Entries Moved to Exists
| ID | Test Name | Component | Was Bucket |
|:--:|-----------|-----------|:----------:|
| {id} | {name} | {comp} | {🔴🟠🟡🟢} |

### Critical/High Gaps Remaining
| ID | Test Name | Component | Score |
|:--:|-----------|-----------|:-----:|
| {id} | {name} | {comp} | {score} |
```

---

### Step 6: Update State File

```markdown
# Updates to tge-state.md

- **Last Stage Completed:** 7 (or latest observation stage reached)
- **Last Updated:** {ISO timestamp}
- **Observation Fidelity:** {✅ Full / ⚠️ Degraded} — **written BEFORE the register stats below**
  - Assessed At: {ISO timestamp} · Assessed By: Stage 7 · Mode Assessed Against: {mode}
  - Declared Inputs Resolved: {n} of {N}
  - Per-Input Resolution: one row per declared input, carrying its expected location, whether it resolved, the substitute used, and the unmeasured consequence
- **Observation History:** append this cycle's row **including its Fidelity value** — the current-state block above is overwritten each cycle, so a degraded cycle is only recoverable from this history
- **Register Stats:** (recalculated from register)
  - Tests Required: {N}
  - Tests Existing: {n}
  - Tests Missing: {n}
  - Tests Failing: {n}
  - Tests Deprecated: {n}
  - Coverage: {n}%

**Order matters.** Fidelity is written first because every stat below it may be derived from a substitute. A run that writes stats and then fails before recording fidelity leaves the value at `❌ Unknown`, which every consumer reads as degraded — the safe direction. Writing stats first and fidelity last would leave a stale `✅ Full` vouching for figures it never saw.
```

---

### Step 7: Report (Non-Blocking)

Present observation results without requiring user action:

```markdown
{IF Fidelity is ⚠️ Degraded or ❌ Unknown — this block comes FIRST, before any figure:}
## ⚠️ Observation: State Check Complete — DEGRADED

⚠️ **DEGRADED OBSERVATION — the figures below are incomplete.**
{n} of {N} declared inputs for {mode} mode did not resolve:
- **{input}** — expected at `{path}`; substituted with {substitute}

**Therefore unmeasured:** {unmeasured consequence}
{IF Fidelity is ❌ Unknown:} Fidelity was not assessed for this cycle, so it is reported as degraded.

Per-input detail: `.governance/test/tge-state.md` → Observation Fidelity.

---

{OTHERWISE:}
## 🟢 Observation: State Check Complete

**Since last check:** {n} units completed{⚠️ inferred, not read — if degraded}, {n} new tests detected
**Register updated:** {n} entries moved Missing → Exists
**Current coverage:** {n}%{⚠️ if degraded} (was {n}%)

{IF Critical gaps remain:}
⚠️ **Critical gaps remaining:** {n}
- {id}: {name} (Score: {score})

{IF all Critical resolved:}
✅ All Critical-risk tests now exist.

{IF no changes:}
ℹ️ No new completions detected since last observation.
```

**No gate.** Observation is continuous — inform the user and proceed to next applicable stage.

---

## Trigger Conditions

This stage executes when:
1. User invokes AI-TGE during Observation phase ("check coverage", "update register")
2. Session starts and state file shows Observation phase active
3. User explicitly requests "observe" or "what's the coverage now?"
4. After any other observation stage completes (as the re-entry point)

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Updated Test Register | `.governance/test/test-register.md` | Status field updated for checked entries |
| Updated state file | `.governance/test/tge-state.md` | Stats recalculated; timestamp updated |
| Observation log (Comprehensive) | `.governance/test/observation-log.md` | Append-only history of observation cycles |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| **Build state resolution classified** | Resolved — **or** classified by cause per Step 1a (`not declared by this mode` versus `declared and unresolved`). ⚠️ **"Or fallback" is NOT a pass.** A substitute satisfies this row only when its use is recorded; running on the substitute silently is a FAIL |
| **Vocabulary resolution classified** | Per-unit stage names checked against the expected set per Step 1b. A resolved *path* is not a resolved *vocabulary* |
| **Traceability read-and-persist (aidlc only)** | Under `aidlc`, v2's traceability outcome is **read and persisted** into the register (`source: aidlc-traceability-sensor`), never re-run (Step 1c, `common/traceability-ownership.md`). The register is kept. An unresolved v2 outcome is a disclosed degraded read, not a silent re-run. N/A under the four non-`aidlc` methods |
| **Fidelity recorded** | `tge-state.md → Observation Fidelity` holds a value other than `❌ Unknown`, written **before** any figure was derived from it |
| **Degradation disclosed in all three destinations** | If fidelity is not `✅ Full`: the coverage report artifact, the state file, **and** this stage's report each say so. Two of three is a FAIL |
| **Cycle recorded in history** | Observation History row appended, carrying this cycle's fidelity value |
| Affected entries identified | All register entries for completed units checked |
| Status updated | Each checked entry reflects current test existence |
| Coverage recalculated | % reflects updated status counts |
| State file updated | Timestamp and stats current |
| Delta reported | User informed of changes (if any) |
| Non-blocking | No user action required to continue |
