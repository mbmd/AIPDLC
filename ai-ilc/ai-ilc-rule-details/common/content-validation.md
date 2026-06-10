# AI-ILC — Content Validation

**Purpose:** Quality rules for all artifacts AI-ILC produces. Every output must pass these checks before being finalized and presented to the user.

---

## Validation Checklist (Apply to Every Output)

Before presenting any artifact to the user, verify:

### Completeness
- [ ] All required sections present (per the relevant template)
- [ ] No `{placeholder}` values left unfilled (unless marked `_[TBD]_` for user's later input)
- [ ] All referenced decisions exist in the Decision Log
- [ ] State file is current (reflects this stage's completion)

### Accuracy
- [ ] All claims trace back to user-provided input or documented decisions
- [ ] No invented scope, features, or requirements — only what the user stated or confirmed
- [ ] Score rationale references actual content from shaping (not generic statements)
- [ ] Routing decision is supported by the impact assessment answers

### Consistency
- [ ] Idea name matches across all artifacts (state file, register, briefs, decisions)
- [ ] Depth level matches what was agreed at capture (or explicitly adjusted at a gate)
- [ ] No contradiction between evaluation findings and scope decisions
- [ ] Decision Log numbering is sequential with no gaps

### Formatting
- [ ] Markdown renders correctly (headers, tables, lists)
- [ ] Tables have consistent column alignment
- [ ] No broken links or file references
- [ ] Question numbers follow Q-{nn} convention
- [ ] Decision numbers follow D-{nn} convention

### Tone & Voice
- [ ] Content matches the stage's assigned persona voice (see persona map in core-workflow)
- [ ] Professional but accessible — not academic, not casual
- [ ] Value-first framing (lead with what matters, details follow)
- [ ] Actionable language ("do X" rather than "it is recommended that X be done")

---

## File Naming Convention

All output files follow this pattern:

```
{Idea_Name}_{Artifact_Type}.md
```

| Artifact | Filename Pattern | Example |
|----------|-----------------|---------|
| State file | `ilc-state.md` | `ilc-state.md` (fixed name) |
| Idea Register | `Idea_Register.md` | `Idea_Register.md` (fixed name) |
| Decision Log | `Decision_Log.md` | `Decision_Log.md` (fixed name) |
| Go/No-Go Record | `{Idea_Name}_GoNoGo_Decision_Record.md` | `Mobile_App_GoNoGo_Decision_Record.md` |
| Approved Idea Brief | `{Idea_Name}_Approved_Idea_Brief.md` | `Mobile_App_Approved_Idea_Brief.md` |
| Change Request Brief | `{Idea_Name}_Change_Request_Brief.md` | `Mobile_App_Change_Request_Brief.md` |
| Feature Brief | `{Idea_Name}_Feature_Brief.md` | `Mobile_App_Feature_Brief.md` |

**Idea Name rules:**
- Use PascalCase with underscores for spaces: `Mobile_App`, `Payment_Gateway`, `Compliance_Dashboard`
- No special characters, no spaces in filenames
- Keep it short but recognizable (3-4 words max)
- Derived from the idea title confirmed at Capture

---

## Content Rules by Artifact

### Idea Register Entry
- One row per idea — never split an idea across rows
- Status must be a valid value from the state transition table
- Score column stays empty until Evaluate completes
- Route column stays empty until Route & Handoff completes

### Decision Log Entry
- Every entry has: ID, date, question reference, decision, rationale
- Rationale is mandatory — never log a bare decision without "why"
- Include who decided (user confirmed vs. AI recommended + user accepted)

### Go/No-Go Decision Record
- Must be produced for ALL outcomes (approve, park, reject) — not just approvals
- Includes: idea summary, score, key risks, decision, rationale, conditions (if any), next step
- Parked ideas must have a revisit date
- Rejected ideas must have a clear "why not" that someone else could read and understand

### Briefs (Approved Idea / Change Request / Feature)
- Must carry forward ALL context from shaping + evaluation + scope
- Zero information loss at handoff — the successor never starts cold
- Must be self-contained: readable without needing to open the state file or register
- Must explicitly state the routing destination and why

---

## Depth-Specific Quality Expectations

| Depth | Content Length | Detail Level | Iteration |
|-------|:-------------:|:------------:|:---------:|
| **Minimal** | Concise (1-2 pages per brief) | Essentials only — problem, value, scope, decision | Single pass (present once, user approves) |
| **Standard** | Moderate (2-4 pages per brief) | Full structured content with rationale at each section | One iteration (present, collect feedback, finalize) |
| **Comprehensive** | Detailed (4-6 pages per brief) | Deep analysis, multiple perspectives, explicit trade-offs | Multiple iterations (draft → feedback → revise → finalize) |

---

## Validation Failure Handling

If any check fails:

1. **Do NOT present the artifact to the user yet**
2. Fix the issue silently (if it's a formatting or consistency error the AI can resolve)
3. If it requires user input to resolve (e.g., missing decision), ask the specific question
4. Re-validate after fix
5. Only present when all checks pass

**Never ship an incomplete artifact with "I'll fix this later."** Every output is final when presented.

---

## Cross-Reference Integrity

When an artifact references another artifact or decision:

| Reference Type | Validation Rule |
|----------------|----------------|
| "As decided in Q-03..." | Verify Q-03 exists in the Decision Log with that answer |
| "Score: 28/35" | Verify the score in the state file matches |
| "Per the scope definition..." | Verify scope was actually defined (Stage 4 completed) |
| "Route: New Project" | Verify ilc-state.md Route field matches |
| "See Idea Register" | Verify the idea has an entry with matching status |

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Produce content the user didn't ask for | AI-ILC is governed, not generative-at-will |
| Fill in `_[TBD]_` fields without asking | Those are explicitly user-provided-later markers |
| Use vague rationale ("it seems good") | Every rationale must reference specific evidence |
| Leave the state file stale | State must always reflect the latest completed stage |
| Produce briefs with generic/boilerplate sections | Every section must be specific to THIS idea |
| Ignore depth level | Minimal ≠ shorter Standard; it's a genuinely different interaction model |

---

*Version: 1.0.0 | Part of AI-ILC — AI-Driven Idea Life Cycle*
