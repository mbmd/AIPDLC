# AI-LENS Facet — AI-PILC

> **Loaded by the lens seam** when `Lens_Status.md` AI-LENS row = `AI-Powered` (or when no mode exists yet — PILC promotes the mode into the project spine).
> **Integration points:** `inception/` (Stage 1–3), `assessment/` (Stage 4–7), `justification/` (Stage 8).
> **Persona:** PMO Professional / Senior Project Manager (primary; sub-role `#persona-subrole-risk-analyst` for feasibility/risk, `#persona-subrole-financial-analyst` for cost/business case).

---

## Purpose

Promote the AI-LENS mode into the project's governance spine as a formal `Decision_Log` row, then assess the AI dimension across feasibility, cost, risk, and regulatory classification. PILC is where the idea-level posture becomes a project-level commitment with budget and risk implications.

---

## When This Facet Fires

1. **During inception (Stage 1–3):** promote the AI mode into the spine `Decision_Log` + update `Lens_Status.md`.
2. **During assessment (Stage 4–7):** AI-specific feasibility assessment.
3. **During justification (Stage 8):** AI-specific cost model, risk, and EU AI Act classification in the business case.

---

## Step 1: Mode Promotion (at Inception)

### If an Idea Brief with AI Posture exists (chain mode from ILC):

- Read the `aiPosture` from the Idea Brief.
- Promote it into the project's `Decision_Log.md` as a formal row:

```markdown
| PILC-{ABBREV}-D-{N} | PILC | {date} | AI-LENS mode set: AI-Powered ({sub-modes}) | Promoted from Idea Brief AI Posture: {posture} | No-AI / AI-Powered (multi-select) | AI-Powered: {sub-modes} | Idea Brief assessment + strategic alignment with {product vision} | {user} |
```

- **Dual-write:** also upsert `Lens_Status.md` (per `LENS_STATUS_MECHANISM.md` §4) — upsert the AI-LENS row: `| AI-LENS | AI-Powered | {sub-modes} | {date} | PILC-{ABBREV}-D-{N} | PILC |`. `Lens_Status.md` is the live current-mode SSOT the facets read; the `Decision_Log` row is the immutable history (INV-L3-033 — current mode = the `Lens_Status.md` row, never a Decision_Log scan).
- Create the spine and/or `Lens_Status.md` if absent (per `MANAGEMENT_FRAMEWORK_CONTRACT.md` §4: create-if-absent).
- ID format: `PILC-{ABBREV}-D-{N}` — scan for highest existing `N` in the Decision_Log, increment.

### If no Idea Brief (standalone / direct entry):

- Run the full Resolution Protocol (as defined in `AI_LENS_PROTOCOL.md` §2):
  - Ask: "No-AI, or AI-Powered? If AI-Powered, which stances? (Opportunity / Augmented / Native — multi-select)"
  - Record the choice as a `Decision_Log` row (same format as above, with Context = "Direct project initiation — no upstream idea") **+ upsert the `Lens_Status.md` AI-LENS row (same dual-write, per `LENS_STATUS_MECHANISM.md` §4)**.

### Inform & Proceed

After recording, inform:
```
AI Lens: AI-Powered — {sub-modes}, recorded as PILC-{ABBREV}-D-{N}.
Change anytime with _AILENS_.
```

---

## Step 2: AI Feasibility Assessment (at Assessment Stage)

When the assessment phase runs and the mode = `AI-Powered`, add an AI-specific feasibility dimension:

### Assessment Areas

| Area | Key questions | Output |
|------|--------------|--------|
| **Data availability** | Does the required training/grounding data exist? Is it accessible, clean, sufficient volume? | Ready / Partial / Gap |
| **Model availability** | Is there a suitable model (managed API / open-source / custom-trained)? | Available / Evaluate / Build-required |
| **Build vs. Buy** | Managed AI service (API) vs. self-hosted vs. fine-tuned vs. from-scratch? | Buy / Hybrid / Build |
| **Skills readiness** | Does the team have ML/AI engineering capability, or is it a gap? | Ready / Upskill / Hire |
| **Technical risk** | Non-deterministic output, latency sensitivity, scale requirements, integration complexity? | Low / Medium / High |

### Recording

Record the feasibility summary in the PIP's feasibility section under an `## AI Feasibility` heading:

```markdown
## AI Feasibility

| Dimension | Assessment | Notes |
|-----------|-----------|-------|
| Data availability | {Ready/Partial/Gap} | {detail} |
| Model availability | {Available/Evaluate/Build-required} | {detail} |
| Build vs. Buy | {Buy/Hybrid/Build} | {detail} |
| Skills readiness | {Ready/Upskill/Hire} | {detail} |
| Technical risk | {Low/Medium/High} | {detail} |

**Overall AI feasibility:** {Feasible / Feasible-with-conditions / Not-feasible}
```

If overall = `Not-feasible`, inform the user this creates a significant risk; they may choose to flip the mode to `No-AI` (append a new Decision_Log row).

---

## Step 3: AI Cost Model (at Justification Stage)

When building the business case and the mode = `AI-Powered`, add AI-specific cost dimensions:

### Cost Categories

| Category | What to capture |
|----------|-----------------|
| **Inference/runtime cost** | Token consumption, API call pricing, GPU hours (variable, usage-based) |
| **Training/fine-tuning cost** | One-time or periodic model training/fine-tuning costs |
| **Data infrastructure** | Vector DB hosting, embedding generation, data pipeline, storage |
| **Human-in-the-loop** | Review/moderation labor, quality assurance cost |
| **Monitoring/MLOps** | Drift detection, eval runs, model versioning infrastructure |

### Cost Model Type

Classify the overall cost model:
- `token-metered` — primarily API-call/token-based (managed LLM)
- `gpu-compute` — primarily GPU infrastructure (self-hosted models)
- `managed-api` — flat-rate or tiered managed service
- `hybrid` — combination of the above

### Recording

Add to the business case under `## AI Cost Analysis`:

```markdown
## AI Cost Analysis

**Cost model type:** {token-metered | gpu-compute | managed-api | hybrid}

| Category | Monthly estimate | Scaling factor | Notes |
|----------|-----------------|----------------|-------|
| Inference/runtime | {estimate} | per {unit} | {detail} |
| Data infrastructure | {estimate} | {fixed/variable} | {detail} |
| HITL labor | {estimate} | per {volume} | {detail} |
| MLOps/monitoring | {estimate} | {fixed} | {detail} |

**Key insight:** AI features introduce VARIABLE cost tied to usage volume — unlike traditional features where cost is primarily fixed (dev effort).
```

---

## Step 4: AI Risk Assessment (at Assessment Stage)

Add AI-specific risks to the risk register:

### AI Risk Categories

| Risk | Description | Typical controls |
|------|-------------|-----------------|
| **Model quality degradation** | Output quality drops over time (data drift, model staleness) | Monitoring, eval harness, retraining triggers |
| **Hallucination / confabulation** | Model generates plausible but false content | Grounding (RAG), output verification, HITL |
| **Bias and fairness** | Systematic discrimination in model outputs | Bias testing, diverse training data, fairness metrics |
| **Vendor lock-in** | Dependency on a single AI provider (API, model, platform) | Abstraction layer, fallback provider, open-source baseline |
| **Regulatory non-compliance** | AI usage violates EU AI Act or sector-specific regulations | Classification, transparency obligations, conformity assessment |
| **Security (prompt injection, data poisoning)** | Adversarial inputs manipulate model behavior | Input sanitization, output filtering, red-teaming |
| **Cost overrun** | Usage-based AI costs exceed budget at scale | Usage caps, alerting, architecture cost controls |

### Recording

Add each applicable risk to the project risk register with standard columns. Tag AI risks with `Category: AI` for downstream filtering.

**Overall AI risk level:** `low` | `medium` | `high` | `critical` (based on the highest-impact unmitigated AI risk).

---

## Step 5: EU AI Act Classification (at Assessment Stage)

For each AI feature candidate (from the Idea Brief's capability signal), classify the EU AI Act risk:

### Classification Guide

| Class | Criteria | Obligations |
|-------|----------|-------------|
| **Minimal** | AI used for non-critical internal tooling, creative assists, or low-stakes recommendations | Voluntary code of conduct only |
| **Limited** | AI interacts with humans (chatbots, content generation shown to users) | Transparency obligation — disclose that AI is in use |
| **High** | AI in critical domains (hiring, credit, law enforcement, education assessment, critical infrastructure) | Conformity assessment, risk management, human oversight, data governance, transparency, accuracy monitoring |
| **Unacceptable** | Social scoring, real-time biometric surveillance, manipulation of vulnerable groups | Prohibited — do not proceed |

### Recording

Add to the PIP feasibility section under `## EU AI Act Risk Classification`:

```markdown
## EU AI Act Risk Classification

| Feature (from Idea Brief) | Capability | Proposed class | Rationale | Key obligation |
|---------------------------|-----------|----------------|-----------|----------------|
| {feature description} | {capability} | {minimal/limited/high/unacceptable} | {one-line reasoning} | {primary obligation} |

**Highest class across features:** {class}
**Action required:** {none / transparency disclosure / conformity assessment / STOP — prohibited}
```

If any feature = `unacceptable`: flag immediately. The user must remove that feature or redesign it. Do not proceed with an unacceptable classification.

If any feature = `high`: note that AI-GCE's `AIG__` agent will later enforce the full obligation set during development.

---

## What This Facet Does NOT Do

- Does not identify individual AI features in the backlog (AI-POLC).
- Does not design AI interaction patterns (AI-UXD).
- Does not make architecture decisions (model choice, data pipeline) — that's AI-ADLC.
- Does not provision infrastructure (AI-DWG).
- Does not enforce compliance rules (AI-GCE) or run evaluations (AI-TGE).

---

*AI-LENS PILC Facet v1.0.0 | Integration: Inception (mode promotion) + Assessment (feasibility/risk/EU-AI-Act) + Justification (cost model) | Author: Maheri*
