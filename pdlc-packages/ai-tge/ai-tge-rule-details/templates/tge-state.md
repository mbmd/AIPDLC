<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# TGE State File — Template

---
generatedBy: AI-TGE
generatedVersion: {version}
source: engine-runtime
generatedOn: {ISO-date}
ownership: generated
---

# AI-TGE State

> **MARKER FILE** — This file's existence signals that AI-TGE has been initialized in this workspace.
> Location: `.governance/test/tge-state.md`

---

## Engine Status

| Field | Value |
|-------|-------|
| **Mode** | {Full Chain / Architecture Only / Brownfield / Observation Only} |
| **Current Phase** | {Strategy / Observation / Complete} |
| **Last Stage Completed** | {1-12} |
| **Last Updated** | {ISO timestamp} |
| **Engine Version** | AI-TGE v{version} |
| **Initialized** | {ISO timestamp — first creation} |

---

## Input Sources

| Source | Path | Status |
|--------|------|:------:|
| **Architecture Package (AP)** | {path or "not available"} | {✅ Detected / ❌ Not available} |
| **Development Workspace (DW)** | {path or "not available"} | {✅ Detected / ❌ Not available} |
| **aidlc-docs** | {path or "not available"} | {✅ Detected / ❌ Not available} |
| **User Stories** | {path or "not available"} | {✅ Detected / ❌ Not available} |
| **Existing Tests** | {path or "not detected"} | {✅ Detected / ❌ Not detected} |

> **Detection only.** A `❌ Not available` row above is not a finding on its own — what each absence *costs* is recorded in Observation Fidelity below.

---

## Observation Fidelity

| Field | Value |
|-------|-------|
| **Fidelity** | {✅ Full / ⚠️ Degraded / ❌ Unknown} |
| **Assessed At** | {ISO timestamp or "not assessed"} |
| **Assessed By** | Stage {1 / 7} |
| **Mode Assessed Against** | {Full Chain / Architecture Only / Brownfield / Observation Only} |
| **Declared Inputs Resolved** | {n} of {N} |

### Per-Input Resolution

| Input | Expected At | Resolved | Substitute Used | Unmeasured Consequence |
|-------|-------------|:-------:|-----------------|------------------------|
| **Build state** | {path or "not declared by this mode"} | {✅ / ❌ / n/a} | {— / modification-time heuristic} | {— / unit completion is inferred from file timestamps, not read} |
| **Unit-progress vocabulary** | {source or "not declared by this mode"} | {✅ / ❌ / n/a} | {— / completions treated as generic} | {— / per-unit stage position unavailable} |
| **User-story location** | {path or "not declared by this mode"} | {✅ / ❌ / n/a} | {— / Stage 8 skipped} | {— / story-derived acceptance coverage is zero, not complete} |
| **NFR location** | {path or "not declared by this mode"} | {✅ / ❌ / n/a} | {— / story-carried NFR extraction skipped} | {— / NFR coverage reflects the Architecture Package only} |

> **`❌ Unknown` is read as `⚠️ Degraded` by every consumer** — an unassessed run is never treated as a clean one. Fidelity is reset to `❌ Unknown` on every session resume and earns `✅ Full` only by a fresh assessment that resolves every input this mode declares. Definition, both fail-closed rules, and the disclosure obligation: `common/observation-fidelity.md`.

---

## Register Stats

| Metric | Count |
|--------|:-----:|
| **Total Commitments Tracked** | {N} |
| **Tests Required (active)** | {N} |
| **Tests Existing** | {n} |
| **Tests Missing** | {n} |
| **Tests Failing** | {n} |
| **Tests Deprecated** | {n} |
| **Tests Overridden** | {n} |
| **Coverage** | {n}% |

---

## Risk Summary

| Bucket | Count |
|--------|:-----:|
| 🔴 Critical | {n} |
| 🟠 High | {n} |
| 🟡 Medium | {n} |
| 🟢 Low | {n} |
| **Total scored** | {N} |

---

## Depth Level

| Field | Value |
|-------|-------|
| **Level** | {Minimal / Standard / Comprehensive} |
| **Total Score** | {n}/25 |
| **Component Count** | {n} (scored {1-5}) |
| **Integration Count** | {n} (scored {1-5}) |
| **Security Surface** | {description} (scored {1-5}) |
| **Data Complexity** | {description} (scored {1-5}) |
| **Team Size** | {description} (scored {1-5}) |

---

## AP Version Tracking

| Field | Value |
|-------|-------|
| **Last Read** | {ISO timestamp or "not applicable"} |
| **AP Marker Location** | {path to adlc-state.md or "N/A"} |
| **Reconciliation Needed** | {Yes / No} |
| **Last Reconciliation** | {ISO timestamp or "never"} |
| **Changes Pending** | {n or 0} |

---

## Observation History

| Cycle | Date | Fidelity | Tests Added | Tests Deprecated | Coverage Before | Coverage After |
|:-----:|:----:|:--------:|:-----------:|:----------------:|:--------------:|:--------------:|
| 1 | {date} | {✅ / ⚠️ / ❌} | {n} | {n} | {n}% | {n}% |
| 2 | {date} | {✅ / ⚠️ / ❌} | {n} | {n} | {n}% | {n}% |

> **Why fidelity is recorded per cycle.** The current-state block above is overwritten each cycle, so without this column a degraded cycle becomes invisible the moment the next one runs. Any trend read across these rows MUST be qualified if any contributing cycle was not `✅ Full` — a coverage jump between a degraded cycle and a full one measures the change in *observation*, not the change in *tests*.

---

## Session Continuity

| Field | Value |
|-------|-------|
| **Last Session** | {date or "current"} |
| **Pending Actions** | {list or "none"} |
| **Deferred Decisions** | {list or "none"} |
| **Next Expected Stage** | {stage number and name} |

---

## Output Artifacts

| Artifact | Path | Last Modified |
|----------|------|:------------:|
| Test Strategy | `.governance/test/test-strategy.md` | {date or "not generated"} |
| Test Register | `.governance/test/test-register.md` | {date or "not generated"} |
| Coverage Report | `.governance/test/coverage-report.md` | {date or "not generated"} |
| Debt Scorecard | `.governance/test/debt-scorecard.md` | {date or "not generated"} |
| Defect Log | `.governance/test/defect-log.md` | {date or "not generated"} |

---

*AI-TGE v{version} | State file — auto-maintained by engine*
