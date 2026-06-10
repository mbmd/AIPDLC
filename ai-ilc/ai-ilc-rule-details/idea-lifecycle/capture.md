# Stage 1: Capture

**Lead persona:** `#persona-product-manager`
**Sub-role:** None (fast, low-ceremony stage)
**Execution:** ALWAYS
**Purpose:** Log the raw idea fast — before it's lost or loses context.

---

## Why This Stage Exists

Ideas are perishable. The longer between "someone thought of it" and "it's written down in a structured place," the more context bleeds away. Capture is deliberately fast and low-friction — 2 minutes max. Structure comes later (Shape). Right now we just need: what is it, who said it, and where does it go.

---

## Depth Adaptation

| Depth | Capture Behavior |
|-------|-----------------|
| **Minimal** | Accept idea as-is; auto-detect signals; confirm with one question |
| **Standard** | Accept idea; ask 1-2 clarifying questions to improve signal detection |
| **Comprehensive** | Accept idea; ask for additional context (trigger, who benefits, rough scale) before confirming |

---

## Step-by-Step Execution

### Step 1: Check for Existing State

1. Look for `ilc-state.md` in the workspace/output directory
2. If found:
   - Load state file
   - Check status:
     - If terminal (Routed / Rejected): inform user previous idea is complete; offer to start new
     - If active (any non-terminal status): offer to resume (per `session-continuity.md`)
     - If Parked: offer to revisit or start new
3. If NOT found: proceed to Step 2 (fresh start)

### Step 2: Receive the Raw Idea

Accept the idea in ANY format the user provides:
- Verbal description ("I have this idea for...")
- One-liner ("What about a tool that does X?")
- Pasted document (brief, proposal, feature request, email)
- Backlog item being elevated for evaluation

**Do NOT restructure yet.** Capture the user's exact words/content. Shaping happens in Stage 2.

### Step 3: Auto-Detect Signals

From the raw input, detect:

| Signal | Detection Method | Values |
|--------|-----------------|--------|
| **Scale** | Scope language, stakeholder breadth, time horizon | Small feature / Medium initiative / Large strategic |
| **Clarity** | Specificity, problem/solution articulation, concreteness | Vague notion / Partially formed / Well-articulated |
| **Domain** | Subject matter keywords | architecture / governance / devops / testing / licensing / pmo / general |

### Step 4: Recommend Depth

Based on signals:

| Scale + Clarity | Recommended Depth |
|----------------|-------------------|
| Small + Well-articulated | Minimal |
| Small + Vague | Standard |
| Medium + any clarity | Standard |
| Large + any clarity | Comprehensive |

### Step 5: Configuration Questions

```markdown
### Q-01: Output Location

**Context:** Where should AI-ILC store its output files for this idea?

**Options:**
- (a) Current directory (default)
- (b) A specific folder path: ___
- (c) Let me decide later

**Recommended:** (a) Current directory
**Rationale:** Keeps things simple; you can always move files later.

**Your Decision:** _[awaiting input]_
```

```markdown
### Q-02: Depth Level

**Context:** Based on what you've shared, this idea appears to be {scale} in scale and {clarity} in clarity.

**Options:**
- (a) Minimal — fast pipeline, essentials only
- (b) Standard — full evaluation with structured scoring
- (c) Comprehensive — deep analysis, multiple perspectives

**Recommended:** ({recommended}) — {rationale based on signals}
**Rationale:** {explanation}

**Your Decision:** _[awaiting input]_
```

### Step 6: Create State File

Create `ilc-state.md` with:
- Idea Name: derived from user's input (short title — confirm with user if ambiguous)
- Status: Captured
- Current Stage: 1
- Depth Level: as confirmed
- Domain Detected: from auto-detection
- Route: pending
- Created: current date
- All other fields: pending

### Step 7: Register the Idea

Add entry to `Idea_Register.md`:
- ID: next sequential number
- Name: idea title
- Status: Captured
- Score: —
- Decision: —
- Route: —
- Created: current date

If `Idea_Register.md` doesn't exist, create it from template `templates/idea-register.md`.

### Step 8: Present Capture Summary

```
✅ Idea captured: "{idea_title}"
📊 Scale signal: {small/medium/large}
🔍 Clarity: {vague/partial/well-articulated}
🧭 Domain detected: {domain}
📐 Depth: {Minimal/Standard/Comprehensive}
📁 Output: {location}

Idea registered as #{id} in the pipeline.

Ready to shape this idea — turning it into a structured problem statement.
Continue to Shape? [Yes / Adjust depth / Adjust name / Stop here]
```

---

## Gate

**Condition to proceed:** User confirms the capture summary.

**Acceptable user responses:**
- "Yes" / "Continue" / "Shape it" → proceed to Stage 2
- "Adjust depth to {X}" → update state, re-confirm, then proceed
- "Adjust name to {Y}" → update state + register, re-confirm, then proceed
- "Stop here" → state remains Captured; user can resume later

**Post-gate actions:**
1. Log D-01 in Decision Log: "Idea captured and confirmed. Depth: {level}. Title: {name}."
2. Update state file: Current Stage = 2 (ready for Shape)

---

## Transition Message

```
───────────────────────────────────────────────────────
Moving to Stage 2: SHAPE

I'll now ask structured questions to turn your raw idea
into a clear problem/solution statement. This is where
we figure out WHAT the idea actually is.

Activating: Business Analyst lens (ambiguity detection,
requirements structuring)
───────────────────────────────────────────────────────
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| User provides multiple ideas at once | Capture the first; note the others as "pending capture" in state file Pending Decisions; process one at a time |
| Idea is identical to a previously-rejected one | Flag it: "This resembles idea #{X} which was rejected because {reason}. Do you want to proceed anyway (new context) or acknowledge the duplicate?" |
| User provides a fully-formed proposal (already shaped) | Still run Capture (log it), but signal that Shape may be fast: "This looks well-articulated — shaping may go quickly." |
| User doesn't know what to call the idea | Offer a working title derived from the problem space; mark as "title TBD — will refine in Shape" |

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*
