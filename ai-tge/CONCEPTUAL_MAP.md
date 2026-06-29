# AI-TGE Conceptual Map

> **What this file is:** A navigational guide to AI-TGE's internal structure. It answers "where does each test governance concern live?" and helps you find the right file.

---

## How to Read This

AI-TGE is a **test governance engine** that runs alongside AI-DLC v1 as a continuous quality companion. It reads the development workspace (same input as AI-GCE) and derives test governance rules, coverage requirements, and quality gates specific to the project's architecture and methodology.

**Key principle:** AI-TGE governs HOW testing is done (strategy, coverage, methodology). It does NOT execute tests — it ensures the testing discipline is followed.

---

## Concern → Location Map

### Core Orchestration

| Concern | File | Purpose |
|---------|------|---------|
| Master engine logic | `ai-tge-rules/core-engine.md` | Modes, two-source model, derivation flow, chain contract |
| Family position | `ai-tge-rules/core-engine.md` → Family table | AI-TGE runs alongside AI-DLC v1 (continuous quality) |

### Cross-Cutting Rules

| Concern | File | Purpose |
|---------|------|---------|
| Process overview | `common/process-overview.md` | High-level map of TGE's derivation process |
| Session continuity | `common/session-continuity.md` | State preservation across sessions |
| Question format | `common/question-format-guide.md` | Structured question formatting |
| Content validation | `common/content-validation.md` | Output quality checks |
| Test taxonomy | `common/test-taxonomy.md` | Classification of test types and their governance rules |
| Two-source model | `common/two-source-model.md` | Steering-derived + built-in baseline (L25) |
| Welcome message | `common/welcome-message.md` | One-time workflow greeting |

### Strategy Phase (Stage Details)

| Stage | File | Purpose |
|:-----:|------|---------|
| 1 | `strategy/workspace-detection.md` | Detect inputs, select mode, score depth, init state |
| 2 | `strategy/architecture-reading.md` | Read AP/DW/codebase, produce commitment inventory |
| 3 | `strategy/test-requirement-derivation.md` | Two-source derivation → test register |
| 4 | `strategy/brownfield-assessment.md` | Scan existing tests, map to register, identify gaps |
| 5 | `strategy/test-strategy-generation.md` | Produce test strategy (pyramid, tools, goals, gates) |
| 6 | `strategy/risk-scoring.md` | Score missing tests, produce debt scorecard |

### Observation Phase (Stage Details)

| Stage | File | Purpose |
|:-----:|------|---------|
| 7 | `observation/state-observation.md` | Read DLC state, check test existence, update register |
| 8 | `observation/story-acceptance-mapping.md` | Map acceptance criteria → register entries |
| 9 | `observation/coverage-reporting.md` | Multi-view coverage report generation |
| 10 | `observation/architecture-reconciliation.md` | Detect AP changes, propose register updates |
| 11 | `observation/defect-logging.md` | Structured defect capture with governance linkage |
| 12 | `observation/debt-reassessment.md` | Re-score risks, update priorities, track trend |

### Output Templates

| Template | Purpose |
|----------|---------|
| `templates/test-strategy.md` | Test strategy document template |
| `templates/test-register.md` | Master test register template |
| `templates/coverage-report.md` | Multi-view coverage report template |
| `templates/debt-scorecard.md` | Prioritized debt list template |
| `templates/defect-log.md` | Structured defect tracking template |
| `templates/tge-state.md` | Engine state/marker file template |
| `templates/management-framework.md` | Governance spine template (TGE-* entries, L45) |
| `templates/quality-dashboard-template.md` | Test quality dashboard for project monitoring |

---

## Cross-Cutting Mechanisms

| Mechanism | Where Defined | How It Works |
|-----------|--------------|--------------|
| **Two-source model (L25)** | `common/two-source-model.md` | Steering-derived test rules + universal baseline (test before merge, coverage gates) |
| **Continuous companion** | `core-engine.md` | Runs alongside AI-DLC v1, not as a one-shot |
| **Governance spine (L45)** | `templates/management-framework.md` | Appends TGE-* entries (test-governance decisions, override acceptances) |
| **Project ID correlation** | `core-engine.md` | Reads Project ID from workspace-rules.md for audit trail |
| **Tier-progressive** | `core-engine.md` | Same 3-tier model as AI-GCE (Day 0 → Sprint 2+ → Pre-Release) |

---

## Common Questions

### "What's the difference between AI-TGE and AI-GCE?"
→ AI-GCE governs code/process compliance (architecture, sessions, roles, PRs). AI-TGE governs testing discipline (coverage, strategy, quality gates). They run in parallel alongside AI-DLC v1 — complementary, not overlapping.

### "Where are the test rules defined?"
→ `core-engine.md` contains the derivation logic. The actual rules are generated into the destination workspace based on steering files (testing-strategy.md, tech-stack.md).

### "Does AI-TGE generate hooks?"
→ Yes — coverage-check hooks, test-before-merge gates. Same hook classification model as AI-GCE (security-critical on fileEdited, advisory on agentStop).

### "How does AI-TGE read project context?"
→ Same input as AI-GCE: the AI-DWG development workspace (.kiro/steering/ files). Specifically reads `testing-strategy.md`, `tech-stack.md`, and `module-structure.md`.

### "What agents does AI-TGE ship?"
→ `test-governance-agent` (TGV__) and `coverage-review-agent` (CVR__) — IDs `TGE-AG-01` and `TGE-AG-02`. Both built and located in `templates/agents/`.

---

*Created: 2026-06-12 | Lesson 30 compliance*

---

## AI-DFE Data Interface (`ai-tge-rule-details/data-schema/`)

This package ships a machine-readable data interface consumed by **AI-DFE** (the family data fabric). AI-DFE reads these files to gather this package's output into `{family}-ws/data/tge-data.json`.

| File | Purpose |
|------|---------|
| `tge-data.schema.json` | JSON Schema — the shape AI-DFE produces for this package |
| `SOURCE_MAP.md` | Declares where this package's raw output lives + field extraction rules |
| `SCHEMA_README.md` | Human documentation of the schema, fields, and consumers |

> These files do not change this package's runtime behavior — they are a read-only contract for the data fabric. See AI-DFE for how the data surface is gathered, shaped, and distributed.
