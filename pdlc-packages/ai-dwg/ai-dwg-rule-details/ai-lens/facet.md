# AI-LENS Facet — AI-DWG

> **Loaded by the lens seam** when `Lens_Status.md` AI-LENS row = `AI-Powered`.
> **Integration points:** `mapping/` (new transforms) + `templates/` (config/compose/steering).
> **Persona:** DevOps / Platform Engineer + Senior Architect (primary).

---

## Purpose

Provision AI/ML scaffolding into the generated development workspace **and act as the courier** — carry all AI-feature context across the DWG hinge so that AI-GCE (`AIG__`) and AI-TGE (`AIQ__`) have full context without reaching back to the planning workspace. DWG is the bridge between design-time and dev-time for AI features.

---

## Dual Role

| Role | What it does |
|------|-------------|
| **Provisioner** | Generates AI-specific files (deps, config, scaffolding, eval harness, prompt templates) |
| **Courier** | Carries the AI-feature context (tags + AC + architecture + EU-AI-Act class) into the generated workspace |

Both roles activate together; you cannot courier without provisioning, and vice versa.

---

## Guardrail

This facet operates within the DevOps/Platform Engineer's lane:
- Provision **infrastructure and scaffolding** for AI features.
- Courier **context** for downstream agents.
- DO NOT make architecture decisions (AI-ADLC already did that; DWG reads them).
- DO NOT design interaction patterns (AI-UXD already did that).
- DO NOT enforce governance rules (AI-GCE `AIG__` will consume the couriered context).

---

## When This Facet Fires

During workspace generation, when `aiFeature`-tagged items exist in the AP/PBP/UXP inputs:
1. **Scan inputs** for `aiFeature: true` artifacts.
2. **Generate AI scaffolding** based on the ADLC architecture decisions.
3. **Courier AI context** into a manifest inside the generated workspace.

---

## Step 1: Scan for AI Features

Read the 3 peer inputs (AP, PBP, UXP — subset-tolerant) and collect:
- All `aiFeatureId` values
- Per feature: `aiSubMode`, `aiCapability`, `aiAcceptanceCriteria[]` (from POLC)
- Per feature: architecture decisions — model strategy, data strategy, security controls (from ADLC ADRs)
- Per feature: `euAiActClass` (from PILC/PIP)
- Per feature: `aiInteractionModel`, `aiHitlLevel` (from UXD)

If zero AI features found: skip this facet entirely (no AI scaffolding generated).

---

## Step 2: Generate AI Scaffolding

Based on the architecture decisions (from ADLC ADRs), generate:

### 2.1 Dependencies

| Architecture decision | Generated dependencies |
|----------------------|----------------------|
| Managed API (OpenAI/Anthropic/Bedrock) | SDK client library + env config placeholders |
| Self-hosted model | Model-serving framework (vLLM, Ollama, TGI) + Docker config |
| Vector DB (Pinecone/Weaviate/pgvector/Qdrant) | Client library + connection config |
| Feature store | Client library + config |

Generate into `package.json` / `requirements.txt` / `pom.xml` (technology-adaptive per existing DWG logic).

### 2.2 Environment Configuration

Generate `.env.example` entries for AI services:
```env
# AI Services (AIF-{NNN}: {feature name})
AI_MODEL_PROVIDER={provider}
AI_MODEL_ENDPOINT={endpoint-placeholder}
AI_API_KEY={api-key-placeholder}
VECTOR_DB_URL={url-placeholder}
VECTOR_DB_API_KEY={key-placeholder}
AI_TOKEN_BUDGET_DAILY={budget}
```

### 2.3 Scaffolding Files

| File/Folder | Purpose | Generated when |
|-------------|---------|---------------|
| `prompts/` | Prompt template directory with versioned prompt files | Any generation/conversational/summarization feature |
| `eval/` | Evaluation harness directory (golden-set placeholder + eval script skeleton) | Any AI feature (TGE's `AIQ__` needs this) |
| `eval/golden-set.example.jsonl` | Example golden-set format for quality evaluation | Always |
| `src/ai/` or `lib/ai/` | AI client module skeleton (typed interface to the model) | Any managed-API or self-hosted feature |
| `docker-compose.ai.yml` | Local AI infrastructure (vector DB, local model server) | Self-hosted model or vector DB in architecture |
| `ai-config.json` | Central AI configuration (models, endpoints, budgets, feature flags) | Always (references `.env` values) |

### 2.4 AI-Specific Steering

Generate steering file for GCE to govern:
```markdown
---
generatedBy: AI-DWG
source: AI-LENS architecture decisions (ADLC ADRs)
ownership: generated
---

# AI Feature Governance — Steering

## Active AI Features
{list aiFeatureId + capability + sub-mode + EU-AI-Act class}

## Architectural Commitments
{per-feature: model strategy, data strategy, security controls}

## Responsible-AI Obligations
{per-feature: guardrails, bias testing cadence, HITL enforcement level}
```

---

## Step 3: Courier AI Context (Cross-Hinge)

Generate an **AI feature manifest** inside the workspace that carries ALL context downstream agents need:

### File: `{slug}-workspace/.ai-lens/manifest.json`

```json
{
  "aiLensVersion": "1.0.0",
  "generatedOn": "{ISO-date}",
  "generatedBy": "AI-DWG",
  "projectId": "{project-id}",
  "aiMode": "ai-powered",
  "aiSubModes": ["{sub-modes}"],
  "features": [
    {
      "aiFeatureId": "AIF-001",
      "aiSubMode": "{value}",
      "aiCapability": "{value}",
      "euAiActClass": "{value}",
      "acceptanceCriteria": ["{AC from POLC}"],
      "architecture": {
        "modelStrategy": "{from ADLC}",
        "dataStrategy": "{from ADLC}",
        "mlOpsStrategy": "{from ADLC}",
        "raiPosture": "{from ADLC}",
        "securityControls": ["{from ADLC}"],
        "costModel": "{from PILC}"
      },
      "ux": {
        "interactionModel": "{from UXD}",
        "hitlLevel": "{from UXD}",
        "disclosureType": "{from UXD}"
      }
    }
  ]
}
```

### Courier Principle

The manifest is the **single source of truth** for dev-side agents. `AIG__` and `AIQ__` read this manifest; they never reach back across the hinge to the planning workspace. Everything they need is here.

---

## Step 4: Mirror to `data-schema/`

Mirror the AI-feature fields into the generated workspace's `data-schema/` so DFE's `DAT__` can assemble the full lifecycle traceability JSON from the dev workspace:

- `aiFeatureIds[]` — list of all couriered feature IDs
- `aiScaffoldingGenerated: true`
- `aiContextCouriered: true`

---

## Sub-Mode Calibration

| Sub-mode | Scaffolding depth |
|----------|-------------------|
| `opportunity` | Minimal: API client + `.env` placeholder + basic `eval/` skeleton. No docker-compose, no prompts/ folder unless generation capability. |
| `augmented` | Full: all applicable scaffolding from Step 2. Complete eval harness. Full steering for GCE. |
| `native` | Full + additional: model-card template, RAI testing framework skeleton, EU AI Act compliance documentation scaffold. |

---

## What This Facet Does NOT Do

- Does not make architecture decisions (reads them from ADLC ADRs).
- Does not identify or tag AI features (reads from POLC).
- Does not enforce governance rules (generates steering for GCE; GCE enforces via `AIG__`).
- Does not evaluate quality (generates eval harness; TGE evaluates via `AIQ__`).
- Does not modify AI-DFE (mirrors fields into `data-schema/` for existing `DAT__`).

---

*AI-LENS DWG Facet v1.0.0 | Integration: Workspace generation (mapping + templates) | Author: Maheri*
