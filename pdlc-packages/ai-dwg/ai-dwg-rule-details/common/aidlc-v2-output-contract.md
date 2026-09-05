<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-DLC v2 Output Contract (FROZEN) — the `aidlc/` build-method surface

> **Load this file** whenever generating under the AI-DLC build method (`buildProfile: aidlc`), or when AI-GCE / AI-TGE need to know the exact shape AI-DWG emits for AI-DLC v2. This is the **frozen interface** the three packages build against — the equivalent, for the AI-DLC build method, of the frozen interface the spec-driven method already has.

**Status: FROZEN.** Changes here require contract-change deliberation — update this file first, then propagate to AI-DWG, AI-GCE, and AI-TGE together. This file is the committed form of the compatibility design's §18 (build item P0 / merged item 9).

> **Why this is a separate contract file.** The general `common/output-contract.md` covers what AI-DWG *always* emits (the workspace + steering + docs). This file covers the **conditional** surface emitted **only when `buildProfile: aidlc`** — the `aidlc/` tree, sensor manifests, and the bootstrap record. Keeping it separate stops the always-on contract from implying the `aidlc/` tree is unconditional.

---

## 1. The detection marker — how a consumer knows this contract applies

A consumer reads the workspace manifest at `.governance/workspace-manifest.yaml` and checks one field:

```yaml
buildProfile: aidlc
```

**If and only if** that field reads `aidlc`, everything below is present and this contract applies. The five valid values are `aidlc`, `spec-driven-kiro`, `spec-driven-speckit`, `freestyle`, `manual`; the field is mandatory.

**No new manifest field is introduced.** Consumers dispatch on the two fields that already exist — `platformTargets` for platform capability, `buildProfile` for build method. A third combined field would collapse two independent axes.

---

## 2. Behavioural rules — file and section structure

**Files AI-DWG writes** (under `aidlc/spaces/<space>/`):

| File | Contains |
|---|---|
| `memory/team.md` | Practices that outlive this one project — branching model, review cadence, code style, testing posture |
| `memory/project.md` | This project's specialization — security constraints, architecture rules, domain terminology, accessibility target |
| `memory/phases/ideation.md` | Rules for every Ideation-phase stage |
| `memory/phases/inception.md` | Rules for every Inception-phase stage |
| `memory/phases/construction.md` | Rules for every Construction-phase stage |
| `memory/phases/operation.md` | Rules for every Operation-phase stage |

**File AI-DWG never writes:** `memory/org.md` (v2 supplies org-level defaults).

**Section headings — frozen set.** Plain prose under level-two headings:

| Heading | Source in PDLC | File |
|---|---|---|
| `## Way of Working` | AI-ADLC git workflow + AI-DWG contributing/team-agreement + AI-POLC definition of done | `team.md` |
| `## Code Style` | AI-ADLC technology stack + naming conventions | `team.md` |
| `## Testing Posture` | AI-ADLC quality attributes, or AI-TGE when active | `team.md` |
| `## Deployment` | AI-ADLC infrastructure decisions + AI-DWG CI/CD mapping | `team.md` |
| `## Security` | AI-ADLC security and identity architecture | `project.md` |
| `## Architecture` | AI-ADLC architecture principles + module structure | `project.md` |
| `## Accessibility` | AI-UXD accessibility baseline | `project.md` |
| `## Domain Language` | AI-ADLC ubiquitous language / domain context | `project.md` |
| `## Walking Skeleton` | Optional override only — v2 supplies a default at org level | `project.md` |

**Front-matter on every rule file:**

```yaml
---
status: active                    # active | deprecated | draft
pairing: feedforward-only         # or the id of the sensor that verifies this file's rules
---
```

**`pairing:` is mandatory for us** even though v2 marks it optional: v2's health check reports any unpaired rule as a coverage gap, so omitting it makes a freshly generated workspace look broken on its first health check. `feedforward-only` is the honest declaration that no automated check exists for that file.

**Two surrounding-system behaviours AI-DWG must respect:**

1. **The rules chain is strictly additive** — organization → team → project → phase → stage, nothing overridden. A project rule sits alongside an org default; it does not replace it.
2. **Overlapping headings are reported as possible contradictions.** Keep seeded content specific to this project; do not restate framework defaults (don't write "use trunk-based development" if the org layer already says so).

**Ownership after generation.** These files are `hybrid`: the team edits them, and v2's learning loop appends dated entries to `project.md`/`team.md` at approval gates. AI-DWG reconciliation (Mode 2) treats both as team-modified and preserves additions.

---

## 3. Per-agent knowledge — routing table

**Routing is the contract; filenames are not.** v2 loads any `.md` in an agent directory. The binding decision is *which directory*.

| Agent directory | What AI-DWG routes here | Upstream source |
|---|---|---|
| `aidlc-shared/` | Project identity, domain context, naming conventions, git workflow | AI-ADLC + AI-DWG |
| `aidlc-product-agent/` | Product vision, roadmap, personas, user journeys, epics, elaborated stories, scope and risks | AI-POLC + AI-UXD |
| `aidlc-architect-agent/` | Technology stack, architecture principles, module structure, C4 views, ADRs, data architecture, integration patterns | AI-ADLC |
| `aidlc-developer-agent/` | API standards, database conventions, error handling | AI-ADLC |
| `aidlc-design-agent/` | Design system, tokens, frontend standards, accessibility baseline, navigation, content guidelines, theming | AI-UXD |
| `aidlc-quality-agent/` | Testing strategy, coverage expectations, performance standards | AI-ADLC, or AI-TGE when active |
| `aidlc-devsecops-agent/` | Security architecture, authN/authZ model | AI-ADLC |
| `aidlc-operations-agent/` | Observability and logging standards | AI-ADLC |
| `aidlc-pipeline-deploy-agent/` | CI/CD standards, deployment gates | AI-ADLC + AI-DWG |
| `aidlc-delivery-agent/` | Definition of done, definition of ready, planning cadence | AI-POLC |
| `aidlc-compliance-agent/` | Data classification, regulatory requirements | AI-ADLC, only when compliance content exists |
| `aidlc-aws-platform-agent/` | Cloud account structure, service constraints | AI-ADLC, only when cloud specifics exist |

**Conditional emission rule.** A directory is created only when there is content for it — an empty agent directory would be indistinguishable from v2's own empty-at-bootstrap state.

**Front-matter on every knowledge file:** the standard PDLC provenance block (`generatedBy: AI-DWG`, `generatedVersion`, `source`, `generatedOn`, `ownership: generated`).

---

## 4. Sensor manifests — full field contract

**Location:** `<project>/{platform-dir}/sensors/aidlc-<id>.md` — project tier, never inside v2's shipped framework directory (v2 rejects that).

**Naming — a hard contract with a silent failure mode.** The compiler discovers manifests by a pattern requiring the `aidlc-` prefix, and `id:` must equal the filename minus that prefix. A file without the prefix is **silently skipped** — no error, no warning. (This is why `INV-L1-014` guards the three-way reconciliation.)

> **♻️ Rule IDs reconciled with merged item 2 (2026-09-01).** The source-rule-category IDs below use the **item-2-corrected** citations verified against their owning generators (F-I13 / `INV-L5-051`). The compatibility design's §18.4 still carried the pre-correction IDs (`SEC-006`+`LOG-*`, `SEC-001/003/010`, `DATA-012/013/014`); those are stale and are corrected here — this is the "fold the gate-out corrections into the freeze" that makes the contract right the first time rather than corrected after the fact.

| Filename AI-DWG writes | Required `id:` value | Source rule category (owning generator) | Owner |
|---|---|---|---|
| `aidlc-pdlc-architecture.md` | `pdlc-architecture` | `ARCH-*` (architecture-compliance-gen) | AI-GCE |
| `aidlc-pdlc-api-contract.md` | `pdlc-api-contract` | `GOV-API-001` (api-compliance-generator) | AI-GCE |
| `aidlc-pdlc-module-boundary.md` | `pdlc-module-boundary` | `MOD-01/02/03` (module-boundary-generator) | AI-GCE |
| `aidlc-pdlc-data-classification.md` | `pdlc-data-classification` | `SEC-13/14` field-level classification (security-compliance-gen) — *(renamed from `pdlc-data-governance`; classification is a `SEC-*` concern, F-C17)* | AI-GCE |
| `aidlc-pdlc-domain-context.md` | `pdlc-domain-context` | `DOM-*` — section headings + ubiquitous-language term usage (domain-context-generator) | AI-GCE |
| `aidlc-pdlc-domain-purity.md` | `pdlc-domain-purity` | `MOD-02` + `DOM-01` + `DOM-05` — no infrastructure imports in the domain layer. A **different check** from `pdlc-domain-context`; both required | AI-GCE |
| `aidlc-pdlc-sensitive-data.md` | `pdlc-sensitive-data` | `SEC-BASELINE-01` + `SEC-20/21/22` (security-compliance-gen) — *(was `SEC-006`+`LOG-*`, corrected item 2)* | AI-GCE — **paired** with the hook |
| `aidlc-pdlc-auth-presence.md` | `pdlc-auth-presence` | `SEC-01/02/03` + `SEC-BASELINE-02` — auth *presence* only; appropriateness stays with the rule *(was `SEC-001/003/010`, corrected item 2)* | AI-GCE — gate-fired sensor |
| `aidlc-pdlc-migration-safety.md` | `pdlc-migration-safety` | `DATA-BASELINE-01/02` + `DATA-02/03` (data-governance-generator) **+ `GOV-DEVOPS-012/013/014` + `GOV-DEVOPS-BASELINE-02`** (devops-generator) — rollback method present *(was `DATA-012/013/014`, corrected item 2; two owning generators, ledger A31)* | AI-GCE — gate-fired sensor |
| `aidlc-pdlc-a11y.md` | `pdlc-a11y` | AI-UXD accessibility baseline (not an AI-GCE generator) | AI-GCE |
| `aidlc-pdlc-test-coverage.md` | `pdlc-test-coverage` | Coverage threshold | **AI-TGE**, not AI-GCE |

> **No traceability sensor id is frozen** — that ownership is settled at merged item 27 (G3 + read-and-persist), and AI-TGE keeps its own register with its own ID schemes. `pdlc-test-coverage` is safe to freeze because coverage ownership is settled (AI-TGE).

**Front-matter fields:** `id` ✅ · `kind: deterministic` ✅ (only accepted value) · `command` ✅ (an invocation **prefix**, not a full command line — v2's dispatcher appends `--stage`, plus `--output-path`/`--file-path`) · `default_severity` ✅ (`advisory` default; `blocking` only with `fire_on: gate`) · `description` ✅ · `fire_on` (`write` default / `gate`) · `matches` (glob — a write-fired manifest with no glob never fires; must not be empty) · `category` · `input_schema` · `output_schema` · `timeout_seconds` (30 code / 5 document).

**The `command` field cannot pass its own flags** — so the brownfield baseline date is read by the script from `.governance/baseline-manifest.yaml`, not declared in the manifest.

**Wiring — what makes a manifest run.** A manifest carries no stage-targeting field. Each **stage** declares which sensors it imports; the compiler throws on an unknown id. **A manifest no stage imports never fires.** AI-DWG emits `.governance/AIDLC_SENSOR_WIRING.md` listing, per sensor, the stage that should import it and the exact line to add — AI-DWG does not perform the edit. **AI-GCE verifies the wiring landed** (§7a Clause 3).

---

## 5. Code knowledge base — the seeded set

**Location:** `aidlc/spaces/<space>/codekb/<repo>/<canonical-name>.md` — keyed per repository, shared across all work items.

| Canonical artifact | Seeded | Source |
|---|:---:|---|
| `business-overview` | ✅ | AI-POLC product vision + scope and risks |
| `architecture` | ✅ | AI-ADLC C4 context and container views |
| `code-structure` | ✅ | AI-DWG's generated source scaffold + canonical module-structure rules |
| `component-inventory` | ✅ | AI-ADLC C4 level-3 component design |
| `technology-stack` | ✅ | AI-ADLC technology-stack decision record |
| `dependencies` | ✅ | AI-ADLC integration architecture |
| `api-documentation` | ✅ | AI-ADLC API architecture |
| `code-quality-assessment` | ⛔ | Records a real code scan — must **never** be fabricated |
| `reverse-engineering-timestamp` | ⛔ | Records **when** a scan ran — a fabricated value can cause v2 to skip a needed scan |

**Conditions:** greenfield only, and only when AI-ADLC is among the present upstream packages. On brownfield, nothing is seeded and v2's Reverse Engineering stage runs against real code.

---

## 6. Bootstrap record — schema

**Location:** `.governance/aidlc-bootstrap.yaml` — inside AI-DWG's governance area, never inside `aidlc/`. AI-DLC v2 does **not** read this file (it has no bootstrap concept); its readers are the human, AI-GCE, and AI-TGE.

```yaml
# .governance/aidlc-bootstrap.yaml
# Generated by AI-DWG — DO NOT EDIT MANUALLY
---
bootstrapVersion: 1
generatedBy: AI-DWG
generatedVersion: {version}
generatedOn: {ISO-8601 timestamp}
projectId: PRJ-{ABBREV}-{YYYY}-{NNN}

recommended_scope: classic          # v2 STOCK scope — 26 of 33 stages, skips all 7 Ideation stages
recommended_depth: standard         # v2 SCOPE DEPTH (report verbosity) — minimal | standard | comprehensive
recommended_test_strategy: standard # v2 TEST VOLUME — minimal | standard | comprehensive; from AI-TGE's advice when active, else inherited from recommended_depth
tge_governance_depth: standard      # AI-TGE's OWN test-governance depth (engine output detail + which of its 12 stages run); present only when AI-TGE active; INDEPENDENT of recommended_test_strategy — same names, different concepts, never derived from each other (merged item 22 / §8.6)

project_type: greenfield            # greenfield | brownfield

pdlc_chain_completeness:
  ilc:  complete | partial | absent
  pilc: complete | partial | absent
  polc: complete | partial | absent
  uxd:  complete | partial | absent
  adlc: complete | partial | absent
  dwg:  complete

seeded:
  memory:    true
  phases:    true
  knowledge: true
  documents: true
  codekb:    true                   # greenfield only — false on brownfield
  sensors:   manifests-only         # manifests-only | wired | none

waivers:
  peerCoverage: full                # full | partial
  enforcementCoverage: full         # full | advisory-only
```

**`sensors: manifests-only`** tells AI-GCE manifests exist but stage wiring has not been applied — it reports on that rather than assuming the checks are live. Becomes `wired` once the team applies the wiring and AI-GCE confirms it. **Only stock v2 scopes are ever recommended** — never a custom one.

---

## 7. What AI-GCE derives from this contract

| AI-GCE behaviour | Driven by |
|---|---|
| Render the sensor-convertible checks as sensors rather than platform hooks | `buildProfile: aidlc` |
| Keep the secrets/PII check as a pre-write blocking hook | Always — only a hook stops a write before it lands (the one genuine pair) |
| Express the non-file-level items (session discipline, role isolation, sprint governance, phase gates) as prose rules | The heading set in §2 + the phase-vocabulary mapping |
| Resolve hook file format | `platformTargets` |
| Verify sensor wiring was applied | `seeded.sensors` in the bootstrap record |
| Skip generating its own compliance log and process agents | `buildProfile: aidlc` — v2 has native audit shards and its own learning loop |
| Read the brownfield baseline date for sensor scripts | `.governance/baseline-manifest.yaml` |

---

## 7a. Three cross-engine clauses (added at design §18.7a)

### Clause 1 — The `aidlc/` tree is explicitly excluded from drift detection

`aidlc/spaces/<space>/memory/project.md` has **three writers**: AI-DWG (seeds it), v2's learning loop (appends confirmed corrections), and AI-GCE drift detection (currently ignores it). AI-GCE's behaviour is correct but **correct by accident** — the file simply is not on its governed-element list. **The clause:** the `aidlc/` tree is a **generated-then-team-owned** surface, deliberately excluded from drift detection. Drift covers divergence from the *design baseline* (architecture, data, infrastructure, UX, product) — never the rules-and-knowledge surface v2 and the team co-author. Guarded by `INV-L3-041`.

### Clause 2 — AI-GCE's hand-over contract carries a conditional enforcement-surface guarantee

**♻️ This is the item-2 gate-out correction folded into the freeze.** AI-GCE's gate-out declared `hookDefinitions` **unconditionally**; under `aidlc` some become sensors and the guarantee becomes false. The corrected gate-out:

```yaml
# AI-GCE Gate-Out (extended) — INV-L2-022
emits-type: governance-engine@1        # UNCHANGED — no new capability type
visibility: internal
guarantees:
  - status == complete
  - projectId
  - complianceChecks
  - auditScoring
  - driftDetection
  - enforcementSurface       # NEW — which mechanism is present: hooks | sensors | both | docs-only
  - hookDefinitions          # NOW CONDITIONAL — present when enforcementSurface includes hooks
```

A consumer reads `enforcementSurface` to learn what it can rely on, instead of assuming. *(No consumer today reads `hookDefinitions` unconditionally — the capability is `visibility: internal` and AI-DWG already declares the same field conditionally — so this is a minor bump, not a breaking change; see §V.3 of the merged build order.)*

### Clause 3 — Sensor-wiring verification is AI-GCE's responsibility

AI-DWG emits the manifests and the wiring instruction file but does **not** edit v2's stage files. A manifest no stage imports **never fires, silently**. **AI-GCE verifies the wiring landed** — an emitted manifest with no importing stage is a reportable finding, not a silent pass. It reads `seeded.sensors` (§6) to know whether wiring is expected. *(Preferred install path: v2's own learning loop performs the install, so AI-GCE normally verifies that v2 did it.)*

---

## 8. What AI-TGE derives from this contract

| AI-TGE behaviour | Driven by |
|---|---|
| Write the testing strategy as reference material | `knowledge/aidlc-quality-agent/` per §3 |
| Write coverage MUST statements as rules | `memory/team.md ## Testing Posture` per §2 |
| Own the test-coverage sensor manifest | §4 — **AI-TGE owns this one, not AI-GCE** (settles coverage only, not traceability — merged item 27) |
| Record its engine depth and v2's test strategy as **two independent fields** | see below |

**Depth vs test strategy — two independent fields, neither derived from the other** (merged item 22): AI-TGE's **engine depth** controls how much detail the engine produces + which of its twelve stages run (auto-scored from five complexity factors); v2's **test strategy** controls test *volume*. They share three level names and mean different things — a team could want AI-TGE Comprehensive with v2 Minimal. Labelling requirement: qualify as **"test-governance depth"** vs **"test volume strategy"** in any workspace that also runs AI-DLC.

### 8a. AI-TGE's output root — frozen

| What | Frozen path |
|---|---|
| AI-TGE artifacts root | `.governance/test/` |
| Lens findings — AI-LENS facet | `.governance/test/ai-lens/` |
| Lens findings — Automation-Lens facet | `.governance/test/automation-lens/` |
| Agent specifications | `.governance/agents/` (shared with AI-GCE) |

**`.tge/` is the retired path** (migrated at merged item 4; `INV-L2-023`). AI-TGE's gate-out payload-root contradiction is corrected at merged item 11 (its gate-out is the wrong one; every stage body writes `.governance/test/`).

---

*Developer-side frozen contract · AI-DWG · committed from compatibility design §18 at merged item 9 · © Mohammad Maheri*
