# AI-LENS Facet — AI-UXD

> **Loaded by the lens seam** when `Lens_Status.md` AI-LENS row = `AI-Powered`.
> **Integration points:** `define/` (Phase 2) + `design/` (Phase 3) + `validate/` (Phase 4).
> **Persona:** UX Designer / Design System Lead (primary; no sub-role override).

---

## Purpose

Design how users **interact with** each AI feature — the experience layer that makes AI visible, controllable, and trustworthy. For every `aiFeature`-tagged item arriving from AI-POLC, this facet produces interaction patterns, transparency/disclosure affordances, HITL controls, and design-system additions that become part of the UX Design Package (UXP).

---

## Guardrail

This facet operates strictly within the UX Designer's lane:
- Design **how the user experiences** the AI feature (patterns, disclosure, controls).
- DO NOT prescribe model choice, data pipelines, or serving infrastructure (AI-ADLC).
- DO NOT write acceptance criteria (AI-POLC already did that).
- DO NOT enforce governance rules (AI-GCE) or design test strategies (AI-TGE).

---

## When This Facet Fires

1. **During define (Phase 2):** for each `aiFeature`-tagged item, identify the interaction model and HITL requirements.
2. **During design (Phase 3):** produce the AI interaction patterns + design-system components.
3. **During validate (Phase 4):** validate accessibility of AI output + user trust/comprehension.

---

## Step 1: Consume Upstream Tags (Entry)

Read the PBP (from AI-POLC) and identify all `aiFeature: true` items:
- For each tagged epic/story, note: `aiFeatureId`, `aiSubMode`, `aiCapability`, and the AI acceptance criteria (especially HITL level, confidence handling, fallback behavior).
- Group by feature (`aiFeatureId`) for the design pass.

---

## Step 2: Determine Interaction Model (at Define)

For each AI feature, select the primary interaction model:

| Pattern | Description | Best for |
|---------|-------------|----------|
| `suggestion-panel` | AI output displayed in a dedicated side/bottom panel; user reviews and accepts/edits/rejects | Recommendation, generation, summarization |
| `inline-assist` | AI output appears inline within the user's workflow (autocomplete, inline suggestion) | Generation, extraction, prediction |
| `conversational` | Multi-turn dialogue interface (chat, agentic) | Conversational, planning, semantic-search |
| `ambient` | AI operates in the background; surfaces results only when relevant (notifications, alerts) | Anomaly-detection, moderation, monitoring |
| `augmented-control` | User's existing control gains AI-powered enhancement (smart sort, auto-categorize) | Classification, optimization, personalization |
| `dashboard-insight` | AI-derived insights presented in a read-only analytical view | Prediction, causal-inference, simulation |

### Recording

For each AI feature, record in the UXP artifact:

```yaml
---
aiFeatureId: AIF-{NNN}
aiInteractionModel: {pattern from above}
---
```

Present to the user for confirmation: "For {feature}, proposing `{pattern}` because {one-sentence rationale}. Confirm?"

---

## Step 3: Design Transparency & Disclosure (at Define/Design)

Every AI feature that outputs content to the user requires a transparency affordance. This satisfies both UX trust principles and EU AI Act transparency obligations (limited/high risk classes).

### Disclosure Types

| Type | Implementation | Use when |
|------|---------------|----------|
| `badge` | Visual indicator ("AI" badge, icon, or label) adjacent to the AI-generated content | AI output is presented alongside human-authored content and the user must distinguish them |
| `inline-label` | Short text disclaimer within the content area (e.g. "AI-generated suggestion") | AI output is the primary content of a component or panel |
| `system-notice` | One-time or session-level notice that AI is in use (e.g. banner, tooltip on first use) | The AI operates ambiently; per-item badging is impractical |
| `none` | No explicit disclosure (internal tooling, non-user-facing AI) | AI output never reaches an end user (e.g. internal classification for routing) |

### Recording

```yaml
aiDisclosureType: {badge | inline-label | system-notice | none}
```

### Design Rules

- If EU AI Act class = `limited` or `high`: disclosure is **mandatory** (not "none").
- If the AI output is editable by the user: clearly mark the boundary between AI-suggested and user-modified content.
- Disclosure must be perceivable by screen readers (not purely visual — use ARIA labels or visually hidden text).

---

## Step 4: Design HITL Controls (at Design)

For each AI feature, define the human-in-the-loop control level based on the POLC acceptance criteria:

### HITL Levels

| Level | UX behavior | User action required |
|-------|-------------|---------------------|
| `review-before-action` | AI produces output; nothing happens until the user explicitly approves/sends/applies | User reviews, optionally edits, then confirms |
| `edit-after` | AI applies its output immediately but presents it as editable/reversible | User can undo, edit, or override within a time window |
| `monitor-only` | AI operates autonomously; user can observe a log/feed of actions taken | User monitors; intervenes only on exceptions |
| `autonomous` | AI operates with no user-visible control surface (fully delegated) | None (override via settings only) |

### Recording

```yaml
aiHitlLevel: {review-before-action | edit-after | monitor-only | autonomous}
```

### Design Obligations per Level

| Level | Required UX elements |
|-------|---------------------|
| `review-before-action` | Preview of AI output + explicit "Apply" / "Discard" buttons + optional edit surface |
| `edit-after` | Undo affordance + change-highlight + audit trail (what AI did vs. what user changed) |
| `monitor-only` | Activity feed / log + "Pause AI" toggle + exception alert surface |
| `autonomous` | Settings page with AI autonomy controls + periodic summary report |

---

## Step 5: Design Confidence & Fallback UX (at Design)

For each AI feature, design how confidence levels are communicated and what the fallback experience is:

### Confidence Display

| Approach | Implementation |
|----------|---------------|
| **Numeric** | Show confidence % or score (e.g. "85% match") — use for power users, analytical contexts |
| **Qualitative** | Show confidence band (High / Medium / Low) via color, icon, or text — use for general users |
| **Implicit** | Order by confidence (highest first) without showing the score — use for recommendation/ranking |
| **Hidden** | Don't show confidence at all — use when HITL is `autonomous` or all outputs are above threshold |

### Fallback States

Design the UX for each failure mode from POLC's acceptance criteria:

| State | UX requirement |
|-------|---------------|
| **No result** (model returns nothing above threshold) | Empty state with explanation ("No suggestions available for this context") |
| **Service unavailable** (API/model down) | Graceful degradation — hide AI panel, show non-AI alternative, no error blocking the workflow |
| **Low confidence** (below display threshold) | Either hide the suggestion or show with reduced prominence + disclaimer |
| **Timeout** (latency exceeds bound) | Loading state → timeout message → fallback to non-AI path |

---

## Step 6: Design-System Additions (at Design)

For AI features, identify new design-system components needed:

### Common AI Design-System Components

| Component | Purpose | When needed |
|-----------|---------|-------------|
| **AI Badge** | Marks AI-generated content | Any feature with disclosure type = `badge` |
| **Confidence Indicator** | Displays confidence level (bar, dot, label) | Any feature showing confidence to users |
| **Feedback Control** | Thumbs up/down, rating, correction input | Any feature where user feedback improves the model |
| **AI Loading State** | Skeleton/spinner specific to AI generation (may take longer than traditional loads) | Any feature with latency > 1s |
| **Suggestion Card** | Standard container for AI suggestions (with accept/reject/edit) | Suggestion-panel interaction model |
| **AI Empty State** | Explains why no AI output is available | Any feature with a fallback state |

### Recording

List new components in the UXP's design-system section with specifications (size, color token, a11y, states).

---

## Step 7: Accessibility Validation (at Validate)

For each AI feature's UX:

- [ ] AI disclosure is perceivable by screen readers (ARIA labels, not just color/icon)
- [ ] HITL controls are keyboard-accessible
- [ ] Confidence indicators have text alternatives
- [ ] Fallback states are announced to assistive technology
- [ ] AI-generated content is distinguishable in high-contrast mode
- [ ] Loading states communicate wait to screen-reader users (aria-live, role="status")
- [ ] Feedback controls have clear labels and focus management

---

## Output Summary

For each AI feature, the UXP gains:

```markdown
## AI Interaction Design — {feature name} (AIF-{NNN})

- **Interaction model:** {pattern}
- **Disclosure type:** {type}
- **HITL level:** {level}
- **Confidence display:** {approach}
- **Fallback behavior:** {summary}
- **New design-system components:** {list}
- **Accessibility notes:** {any special considerations}
```

---

## What This Facet Does NOT Do

- Does not identify or tag AI features (AI-POLC already did that).
- Does not design model architecture, data pipelines, or MLOps (AI-ADLC).
- Does not write acceptance criteria (reads them from POLC).
- Does not generate workspace scaffolding (AI-DWG).
- Does not enforce governance (AI-GCE) or evaluate quality (AI-TGE).

---

*AI-LENS UXD Facet v1.0.0 | Integration: Define (interaction model + disclosure) + Design (HITL + confidence + fallback + design-system) + Validate (a11y) | Author: Maheri*
