<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Sensor Manifests — emission + the wiring instruction file

> **Load this file** during step 5 of the `aidlc/` emitter. Authority: `common/aidlc-v2-output-contract.md` §4. **Completed at merged item 25** — establishes the emitter call site, the naming contract, the tool-scoped seam, and the wiring-file responsibility (below), plus the per-manifest field population, the executable check-script emission, and the pairing declarations (the "Rendering a manifest FROM the neutral intermediate" section). Depends on merged item 23 (the neutral-format intermediate this renders from) and item 24a (the strength→mechanism resolution that decides which checks become sensors).

## Location — the one tool-scoped output

`<project>/{platform-dir}/sensors/aidlc-<id>.md` — **project tier**, never inside v2's shipped framework directory (v2 rejects that). This is the **only** part of the `aidlc/` tree that is tool-scoped: the emitter calls the active platform adapter as a **path-resolution service** to learn where `{platform-dir}` is for this platform (the seam described in `buildmethod-model.md`). Everything else in the tree is tool-neutral.

## Naming — a hard contract with a SILENT failure mode

The v2 compiler discovers manifests by a pattern requiring the `aidlc-` prefix, and the `id:` field must equal the filename **minus that prefix**. A file without the prefix is **silently skipped — no error, no warning**. This is why `INV-L1-014` guards the three-way reconciliation (filename ↔ `id:` ↔ the frozen registry), and why TR-819 is P1-BLOCKER: a naming drift ships a workspace where a governance check silently never runs.

## The manifest set — frozen registry (contract §4, item-2-corrected IDs)

The emitter writes exactly the manifests in the frozen registry, with the `id:` values fixed there. The owning generators + corrected rule IDs are in the contract; the emitter does not re-derive them. (The set includes `pdlc-architecture`, `pdlc-api-contract`, `pdlc-module-boundary`, `pdlc-data-classification`, `pdlc-domain-context`, `pdlc-domain-purity`, `pdlc-sensitive-data`, `pdlc-auth-presence`, `pdlc-migration-safety`, `pdlc-a11y` — AI-GCE-owned — and `pdlc-test-coverage` — AI-TGE-owned.)

## Wiring — what makes a manifest actually fire

A manifest is a **pure capability descriptor** with no stage-targeting field. Each **stage** declares which sensors it imports; the v2 compiler resolves those declarations and throws on an unknown id. **A manifest no stage imports never fires.** So the emitter ALSO writes:

- `.governance/AIDLC_SENSOR_WIRING.md` — lists, per emitted sensor, the stage that should import it and the exact line to add.

**AI-DWG does NOT perform the stage-file edit** (it does not own v2's stage files). The preferred path is v2's own learning loop applying the wiring; failing that, a human applies it from the instruction file. **AI-GCE verifies the wiring landed** (contract §7a Clause 3) — an emitted manifest with no importing stage is a reportable finding, not a silent pass. The bootstrap record's `seeded.sensors` starts at `manifests-only` and becomes `wired` once AI-GCE confirms.

## The `command` field is an invocation prefix

v2's dispatcher appends runtime arguments itself (`--stage <slug>`, then `--output-path`/`--file-path`). A manifest **cannot** pass its own flags — so the brownfield baseline date is read by the check script from `.governance/baseline-manifest.yaml`, never declared in the manifest.

---

## Rendering a manifest FROM the neutral intermediate (merged item 25)

Each manifest is a **render of AI-GCE's neutral intermediate** (`ai-gce/…/rendering/neutral-intermediate.md`, merged item 23) into v2's §4 field set — the sensor render of the same source the hook render draws from. The emitter never re-derives the check; it re-expresses the intermediate's `checkLogic` + `glob` into the manifest's `command` + `matches`. This is the same "re-express, never re-derive" boundary the whole build holds. The mechanism decision (is this check a sensor at all, and gate- or write-fired?) is already made by AI-GCE's `common/strength-to-mechanism.md` (merged item 24a) — the emitter reads the resolved mechanism, it does not decide it.

### Field population — intermediate → §4 front-matter

| Manifest field | Populated from | Rule |
|---|---|---|
| `id` | the frozen registry (contract §4) | Never invented — equals filename minus `aidlc-`. `INV-L1-014` guards the three-way match |
| `kind` | fixed | Always `deterministic` — the only value v2 accepts (it rejects LLM-evaluated sensors at parse time) |
| `command` | the intermediate's `checkLogic`, resolved to the executable check-script path | An **invocation prefix** (e.g. `bash .governance/sensors/<id>.sh`) — no flags; v2's dispatcher appends `--stage`/`--file-path`/`--output-path` |
| `matches` | the intermediate's `glob` (DERIVED from `tech-stack.md` + `module-structure.md`) | A write-fired manifest with an empty `matches` **never fires** — must not be empty. Gate-fired manifests may omit it |
| `fire_on` | the intermediate's `fireMoment` | `write` (default) or `gate` — the three gate-fired security sensors (item 24d) carry `gate` |
| `default_severity` | the resolved strength + `fire_on` | `advisory` default; `blocking` **only** with `fire_on: gate` (a write-fired sensor cannot block — that is the secrets/PII pre-write hook's job, item 24c) |
| `description` | the intermediate's `statement` | One line, human-readable |
| `category` | the intermediate's `class` | `security` / `data` / `architecture` / … |
| `input_schema` / `output_schema` | the check's I/O shape | Per v2's schema convention |
| `timeout_seconds` | check target | 30 for a code check, 5 for a document check |

### The pairing declaration (depends on item 24a)

Every mechanisable rule AI-GCE emits to `memory/` carries a `pairing:` field — either `pairing: aidlc-pdlc-<id>` (the sensor that verifies it) or `pairing: feedforward-only` (no automated check exists). The manifest and the rule name **the same `aidlc-pdlc-<id>`**, so v2's health check can report any rule whose named sensor is not bound as a **visible coverage gap** rather than a silent orphan. The three gate-fired sensors' pairings (`aidlc-pdlc-auth-presence`, `aidlc-pdlc-injection-patterns`, `aidlc-pdlc-migration-safety`) come straight from `ai-gce/…/common/gate-fired-sensors.md` (item 24d); the emitter reads them, it does not mint them.

### The executable check-script emission (division of labour)

For a manifest whose `command` points at a project-tier script, the emitter also writes that script at the path v2's scaffolder defaults to (`.governance/sensors/<id>.sh`). The scripts are **deterministic** (pattern match / structural check only — no judgement, so they clear v2's parse-time filter) and are **templates**: the glob and per-language patterns DERIVE from `tech-stack.md`. Most check bodies already exist in their owning AI-GCE generators; the **injection** script is the one AI-GCE authored fresh (item 24d, `pdlc-injection-patterns.sh`, covering `SEC-10/11/12`). AI-DWG emits the manifest + copies the script to the resolved path; **v2's own learning loop installs the binding**. We auto-fire nothing — v2 decides when the check runs.

> **Why this honours "no automation in v1" rather than overturning it.** AI-GCE never owns a running event loop; it ships a **declaration** (the manifest + the `pairing:`) and a **script**. The check appears inside v2's own flow, at a gate, with v2's confirmation and audit row. Sensor coverage builds over time — v2's adoption model — rather than existing on day one.

## Wiring — what makes a manifest actually fire (the instruction file, populated)

The emitter writes `.governance/AIDLC_SENSOR_WIRING.md` — one row per emitted sensor:

| Column | Content |
|---|---|
| `sensor id` | `aidlc-pdlc-<id>` |
| `target stage` | the v2 stage that should import it (from the sensor's `fire_on` + its `category` — e.g. a `gate`-fired auth sensor binds at the phase gate stage; a write-fired architecture sensor binds at the construction write stage) |
| `exact import line` | the literal line to add to that stage's `imports:` (or equivalent) declaration |
| `applied?` | left `☐` — v2's learning loop (preferred) or a human ticks it once the binding lands |

**AI-DWG lists the wiring; it does NOT edit v2's stage files** (it does not own them). A manifest no stage imports **never fires, silently** — so AI-GCE **verifies** the wiring landed at merged item 26 (reads the bootstrap record's `seeded.sensors`, contract §7a Clause 3); an emitted manifest with no importing stage is a **reportable finding**, not a silent pass. The bootstrap `seeded.sensors` starts at `manifests-only` and becomes `wired` once AI-GCE confirms.

## Output validation

- [ ] Every manifest in the frozen registry (contract §4) is emitted with `id` = filename minus `aidlc-` (INV-L1-014 three-way match).
- [ ] `kind: deterministic` on every manifest; no LLM-evaluated sensor.
- [ ] `command` is an invocation prefix (no flags); write-fired manifests carry a non-empty `matches`.
- [ ] `default_severity: blocking` appears ONLY with `fire_on: gate` (the three gate-fired security sensors).
- [ ] Each manifest and its paired `memory/` rule name the same `aidlc-pdlc-<id>` (or the rule carries `pairing: feedforward-only`).
- [ ] The injection check script (`pdlc-injection-patterns.sh`, item 24d) is emitted at the resolved project-tier path; `command` points at it.
- [ ] `.governance/AIDLC_SENSOR_WIRING.md` lists every emitted sensor with its target stage + exact import line; AI-DWG does not edit any stage file.
- [ ] `checkLogic` + `glob` in each manifest match the neutral intermediate exactly (re-expression, not re-derivation).

---

*Developer-side design detail · AI-DWG `aidlc/` sensor manifests · © Mohammad Maheri*
