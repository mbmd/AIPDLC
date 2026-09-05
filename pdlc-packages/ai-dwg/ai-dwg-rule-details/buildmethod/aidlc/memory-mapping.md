<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Memory Mapping — canonical `rules/` → `memory/{team,project}.md` + `memory/phases/`

> **Load this file** during step 1 of the `aidlc/` emitter. It maps AI-DWG's canonical steering into v2's behavioural-rule files at the frozen paths and headings. Authority for paths/headings/front-matter: `common/aidlc-v2-output-contract.md` §2.

## The two memory files, and what separates them

| File | Holds | Test |
|---|---|---|
| `memory/team.md` | Practices that **outlive this one project** — branching model, review cadence, code style, testing posture | "Would this still be true on the team's *next* project?" → team |
| `memory/project.md` | This project's **specialization** — its security constraints, architecture rules, domain terminology, accessibility target | "Is this specific to *this* system?" → project |

`memory/org.md` is **never written** — v2 supplies org-level defaults, and writing it would collide with framework territory.

## The frozen heading set → source mapping

Content is plain prose under level-two headings. Emit only the headings for which the present inputs supply content (conditional — an empty heading is not written).

| Heading | File | Source in PDLC canonical `rules/` |
|---|---|---|
| `## Way of Working` | `team.md` | AI-ADLC git workflow + AI-DWG contributing/team-agreement + AI-POLC definition of done |
| `## Code Style` | `team.md` | AI-ADLC technology stack + naming conventions |
| `## Testing Posture` | `team.md` | AI-ADLC quality attributes, or AI-TGE `## Testing Posture` when active |
| `## Deployment` | `team.md` | AI-ADLC infrastructure decisions + AI-DWG CI/CD mapping |
| `## Walking Skeleton` | `team.md` | AI-ADLC delivery strategy (vertical-slice vs horizontal-layer + reference module) |
| `## Security` | `project.md` | AI-ADLC security & identity architecture (rules portion) |
| `## Architecture` | `project.md` | AI-ADLC architecture principles + module structure |
| `## Accessibility` | `project.md` | AI-UXD accessibility baseline |
| `## Domain Language` | `project.md` | AI-ADLC ubiquitous language / domain context |

> **`team.md` is the one exception to conditional-heading emission.** For `project.md`, an empty heading is not written. For **`team.md`**, all five Practices-Discovery sections (`Way of Working`, `Walking Skeleton`, `Testing Posture`, `Deployment`, `Code Style`) are **always emitted as a complete unit** so v2's Stage 2.2 recognises a populated file and fast-affirms it. The completeness contract, the section-replace-safety rationale, and the affirm-me marker for thin sections are owned by **`practices-preseeding.md`** (merged item 14) — this mapping supplies the per-heading sources; that file governs the always-five obligation. `Walking Skeleton` therefore lives in `team.md` (a durable practice), not `project.md`.

## The rules-vs-knowledge split

Each source steering file carries **both** reference prose and enforceable rules. The **rules/knowledge split is performed once** by `rules-knowledge-splitter.md` (the shared front step of emitter steps 1–2); this mapping consumes its **rules portion** (MUST / MUST NOT / NEVER statements + their tightest supporting sentence) and routes each to the frozen heading. The reference prose goes to `knowledge/` (see `knowledge-routing.md`, the other consumer of the same splitter pass).

**Example** — `security-rules.md`:
- → `knowledge/aidlc-devsecops-agent/` (reference): "The system uses OAuth 2.0 with PKCE for SPAs; tokens rotate every 15 minutes."
- → `memory/project.md ## Security` (rule): "All endpoints MUST validate the Authorization header. NEVER log token values."

## Phase files — routed by the phase-vocabulary mapping

`memory/phases/{ideation,inception,construction,operation}.md` receive the `PG-*` phase-gate rules **per the phase-vocabulary mapping authored in AI-GCE's `phase-gates-generator.md`** (merged item 7). The emitter does not re-derive that mapping — it reads it. Summary of the routing it applies:

| Phase file | Receives |
|---|---|
| `ideation.md` | No AI-GCE gate rules — **emitted with a stated reason, never blank** (a zero-byte file reads as a failed generation) |
| `inception.md` | `PG-INCEP-*` |
| `construction.md` | `PG-DOM/APP/PRES/TEST-*` (build half) **+** `PG-CONST-*` (integration) — **grouped and labelled by originating phase** so a reader can tell why a cross-module gate sits beside a DTO gate |
| `operation.md` | `PG-INTEG-*` + `CM-*` |

Setup (`PG-SETUP-*`) and Foundation (`PG-FOUND-*`) rules go to **no phase file** — they are already-satisfied preconditions recorded in the bootstrap record + behavioural rules in `memory/team.md` (§0.1 principle 4: not dropped, re-formed). *(The actual phase-file emission — the four files, honouring the three emission traps — is owned by `phase-rules.md` (merged item 16); this table is the routing summary, that file is the emission step.)*

## Front-matter — mandatory on every rule file

```yaml
---
status: active                    # active | deprecated | draft
pairing: feedforward-only         # or the sensor id that verifies this file's rules
---
```

`pairing:` is **not optional for us** even though v2 marks it so: an unpaired rule shows as a coverage gap on v2's first health check, making a fresh workspace look broken. `feedforward-only` honestly declares no automated check exists for that file. Where a `memory/` rule *is* covered by an emitted sensor (contract §4), name that sensor's id instead.

## Additive-chain discipline

v2 resolves rules through five layers (org → team → project → phase → stage), **nothing overridden**. So a `project.md` rule sits *alongside* an org default, never replacing it. Write only what is genuinely this project's; do not restate framework defaults (don't write "use trunk-based development" if the org layer says so) — that keeps v2's overlap-contradiction advisory quiet.

---

*Developer-side design detail · AI-DWG `aidlc/` memory mapping · © Mohammad Maheri*
