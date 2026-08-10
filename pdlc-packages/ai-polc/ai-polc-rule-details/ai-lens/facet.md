# AI-LENS Facet — AI-POLC

> **Loaded by the lens seam** when `Lens_Status.md` AI-LENS row = `AI-Powered`.
> **Integration points:** `strategy/epic-decomposition.md` (Stage 5, Step 5.7+) and `tier2/story-elaboration.md`.
> **Persona:** Product Manager / Product Ownership Lead (primary; no sub-role override).

---

## Purpose

Identify which epics and stories in the Product Backlog Package (PBP) are AI features, classify each into its sub-mode, apply the `aiFeature` tag, and author product-level AI acceptance criteria. This is the **origin point** where AI features enter the backlog as first-class tagged items; downstream packages (UXD, ADLC, DWG, GCE, TGE) key off these tags.

---

## Guardrail

This facet operates strictly within the Product Manager's lane:
- Identify **what** is an AI feature and **why** (product value, user need).
- Define **what good looks like** (acceptance criteria from the user's perspective).
- DO NOT prescribe **how** it is built (no model choice, no serving topology, no data pipeline, no MLOps). That is AI-ADLC's responsibility.

---

## When This Facet Fires

1. **During epic decomposition (Stage 5):** after epics are identified and before prioritization, scan each epic for AI-opportunity signals.
2. **During story elaboration (Tier 2, if active):** when elaborating stories from an AI-tagged epic, carry the `aiFeatureId` forward and write story-level AI acceptance criteria.

---

## Step 1: AI-Opportunity Scan

For each epic (or story, in Tier 2), scan for signals that the feature involves or could benefit from AI:

### Signal Indicators

| Signal category | Examples |
|-----------------|----------|
| **Explicit AI intent** | "use ML to…", "AI-powered…", "intelligent…", "predictive…", "automated recommendation…" |
| **Data-pattern opportunity** | Large datasets mentioned, pattern recognition needed, historical data leverage, personalization requirement |
| **Cognitive task** | Summarization, classification, extraction from unstructured data, natural-language understanding |
| **Non-deterministic output** | "suggest", "rank by relevance", "generate", "draft", "similar to" |
| **Human-judgment augmentation** | "assist the agent", "flag anomalies", "prioritize automatically", "score risk" |

### Scan Behavior

- Read the epic/story description, acceptance criteria, and any context notes.
- Match against the signal indicators above.
- For each match, note which AI capability from the taxonomy (below) it maps to.
- If zero signals detected: skip this epic/story (it is not an AI feature). Move to the next.
- If signals detected: proceed to Step 2.

---

## Step 2: Propose Classification

For each detected AI opportunity, propose:

1. **That it IS an AI feature** (explain the signal in one sentence).
2. **Which sub-mode** from the active palette applies to THIS feature:
   - `opportunity` — AI would add value but the feature can exist without it
   - `augmented` — the feature is deliberately designed around AI enhancement
   - `native` — the feature fundamentally cannot exist without AI/ML

3. **Which primary capability** from the AI-Opportunity Taxonomy:

| # | Capability | Use when… |
|---|------------|-----------|
| 1 | `classification` | The feature categorizes inputs into predefined labels |
| 2 | `prediction` | The feature forecasts future values or outcomes |
| 3 | `recommendation` | The feature suggests items, actions, or content |
| 4 | `generation` | The feature produces text, images, code, or artifacts |
| 5 | `summarization` | The feature condenses content into key points |
| 6 | `semantic-search` | The feature retrieves information by meaning (incl. RAG) |
| 7 | `personalization` | The feature adapts to individual user context |
| 8 | `anomaly-detection` | The feature identifies outliers or unusual patterns |
| 9 | `extraction` | The feature pulls structured data from unstructured sources |
| 10 | `conversational` | The feature involves interactive dialogue or agentic behavior |
| 11 | `optimization` | The feature finds optimal solutions or rankings |
| 12 | `clustering` | The feature groups similar items without predefined labels |
| 13 | `translation` | The feature converts content between languages |
| 14 | `transcription` | The feature converts speech/audio into text |
| 15 | `planning` | The feature decomposes goals into ordered steps or actions |
| 16 | `moderation` | The feature detects policy-violating or inappropriate content |
| 17 | `causal-inference` | The feature identifies cause-effect relationships (not just correlation) |
| 18 | `simulation` | The feature models system behavior under "what-if" conditions |
| 19 | `verification` | The feature checks content/claims against rules or ground truth |
| 20 | `entity-resolution` | The feature determines if records refer to the same real entity |
| 21 | `speech-synthesis` | The feature converts text into spoken audio |

### Presentation Format

```
AI Feature Detected:
  Epic/Story: {epic-id} — {title}
  Signal: "{quoted text or paraphrase from the requirement}"
  Proposed sub-mode: {opportunity | augmented | native}
  Proposed capability: {taxonomy value}
  Rationale: {one sentence explaining why this classification}

Confirm? (yes / change sub-mode / change capability / not AI)
```

Wait for user confirmation before proceeding. The user may:
- Confirm as proposed
- Change the sub-mode or capability
- Reject (mark as not-AI — skip tagging)

---

## Step 3: Apply the `aiFeature` Tag

On user confirmation, apply the tag to the epic/story front-matter:

```yaml
---
aiFeature: true
aiSubMode: {confirmed value}
aiCapability: {confirmed value}
aiFeatureId: AIF-{NNN}
---
```

### Minting `aiFeatureId`

- Scan all existing `AIF-*` tags across the project's backlog artifacts.
- Take the highest `{NNN}` found.
- Assign `{NNN} + 1` (or `001` if none exist).
- One `aiFeatureId` per feature; if the same feature spans multiple stories, they share the ID (the epic holds the canonical tag; stories inherit via `derivedFrom`).

---

## Step 4: Write AI Acceptance Criteria

For each confirmed AI feature, write **product-level** acceptance criteria that define "what good looks like" from the user's perspective. These are constraints the architecture and test strategy must satisfy, but they do NOT prescribe implementation.

### Required AI Acceptance Criteria Categories

| Category | What it defines | Example |
|----------|-----------------|---------|
| **Quality threshold** | Minimum acceptable quality for the AI output | "Suggested replies are rated acceptable by support agents ≥ 85% of the time" |
| **Confidence handling** | What happens at different confidence levels | "Below 70% confidence, do not show suggestion; between 70-90%, show with disclaimer" |
| **Fallback behavior** | What happens when AI fails or is unavailable | "If suggestion service is down, hide the panel entirely; do not block the agent workflow" |
| **Human-in-the-loop** | Required human oversight level | "Agent must review and optionally edit before any AI-drafted reply is sent to the customer" |
| **Response time** | Latency/performance expectation | "Suggestion appears within 3 seconds of ticket load" |
| **Safety/boundary** | What the AI must NOT do | "Never reference internal pricing, never invent a refund policy, never disclose PII from other tickets" |

### Writing Rules

- Write from the **user's perspective** (what they experience), not the system's perspective (how it's built).
- Use measurable thresholds where possible (percentages, seconds, counts).
- Every criterion must be **testable** — AI-TGE will later derive eval harnesses from these.
- Do NOT mention model names, frameworks, APIs, or architecture patterns (that's ADLC's job).
- Place criteria in the epic/story body under a `## AI Acceptance Criteria` heading (or as an `aiAcceptanceCriteria` array in front-matter for machine extraction).

### Format

```markdown
## AI Acceptance Criteria

- **Quality:** {threshold statement}
- **Confidence:** {confidence-handling rule}
- **Fallback:** {degradation behavior}
- **HITL:** {human oversight requirement}
- **Latency:** {response time bound}
- **Safety:** {boundary constraints}
```

Not every category applies to every feature. Include only those relevant; minimum 3 categories per AI feature.

---

## Step 5: Prioritization Impact

After tagging, note the prioritization impact of the sub-mode:

| Sub-mode | Priority signal |
|----------|-----------------|
| `opportunity` | No priority change; treat as a value-add enhancement |
| `augmented` | Elevate priority weight — this is a deliberate strategic investment |
| `native` | The feature is non-negotiable (it IS the AI); priority = must-have for its epic |

Inform the user of the priority signal so they can factor it into the prioritization model (Stage 5 scoring). Do not auto-override scores.

---

## Step 6: Inform Downstream

After all AI features in this batch are tagged:

1. **Summary line:** "AI Lens: {N} features tagged across {M} epics — {list of aiFeatureIds}."
2. **Downstream signal:** these tags will be consumed by:
   - AI-UXD (interaction design per tagged feature)
   - AI-ADLC (architecture per tagged feature — model, data, MLOps, RAI, cost, security)
   - AI-DWG (provisioning + courier)
   - AI-GCE `AIG__` (governance)
   - AI-TGE `AIQ__` (eval + drift)
3. **DFE derivation:** `aiFeatureId` + `aiSubMode` + `aiCapability` + `aiAcceptanceCriteria` are exposed via POLC's `data-schema/` for the cross-lifecycle traceability JSON.

---

## Tier 2 Behavior (Story Elaboration)

When Tier 2 is active and the user elaborates stories from an AI-tagged epic:

- Each story inherits the epic's `aiFeatureId` (via `derivedFrom`).
- Each story MAY carry `aiFeature: true` in its own front-matter if it is a distinct AI unit; otherwise, the epic-level tag is sufficient.
- Write story-level AI acceptance criteria where they differ from the epic level (e.g., a specific story handles the fallback UX; another handles the confidence display).
- Stories that are NOT AI-related within an AI-tagged epic do NOT get the tag (e.g., an admin settings story in a recommendation epic).

---

## What This Facet Does NOT Do

- Does not prescribe model choice, serving strategy, data pipeline, or MLOps approach (AI-ADLC).
- Does not design interaction patterns, disclosure UX, or HITL controls (AI-UXD).
- Does not generate workspace scaffolding (AI-DWG).
- Does not enforce governance rules or run compliance checks (AI-GCE `AIG__`).
- Does not evaluate quality or detect drift (AI-TGE `AIQ__`).
- Does not modify AI-DFE (shared fabric; used as-is).

---

*AI-LENS POLC Facet v1.0.0 | Integration: Stage 5 (epic-decomposition) + Tier 2 (story-elaboration) | Author: Maheri*
