<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-* Family — Project-Parameter Intake Contract

**Version:** 1.0.0
**Date:** 2026-09-03
**Author:** Maheri
**Authored under:** `#persona-process-designer` (lead) + `#persona-product-manager` (support)
**Status:** ADOPTED
**Governs:** the single "ask-once → record → inform" intake surface for project-wide parameters (CC-1 in `CROSS_DESIGN_RECONCILIATION_PLAN.md`)
**Consumed by (contributors):** AI-POLC / AI-PILC (`deliveryMethod` — the live reference); *pending:* AI-LENS (`aiMode`), Flow-Variant (`variant`), Family-Flow (`familyFlow`), Question-Persistence (`questionMode`)

---

## 1. Purpose

Define **one** interface, across the whole AI-* family, by which a project-wide **parameter** — a setting several packages need but the user should only ever be asked once — is **elicited**, **recorded**, and **inherited** without re-elicitation.

Before this contract, four in-flight designs each planned their own Stage-1 question gate (AI-LENS mode, Flow-Variant selection, Question-Persistence mode, Delivery-Method elicitation). A project would accumulate four separately-designed "ask the user once" mechanisms, each storing its answer its own way. This contract is the **single shared surface** those parameters plug into; each design contributes **one parameter row**, not a whole gate.

> **This is a shared CONTRACT, not a new package** — same stance as `DRIFT_INTAKE_CONTRACT.md`, `TRACEABILITY_CONTRACT.md`, and `MANAGEMENT_FRAMEWORK_CONTRACT.md`. Project-parameter intake is a cross-cutting discipline every contributing package honors; no package "owns" another's parameter.

> **Not a new storage tier.** This contract does **not** create a new file. It formalizes a pattern that is already live for one parameter — the delivery-method fields in `OUTPUT_AND_STATE_CONTRACT.md` §10.1 ("captured once and inherited family-wide via the state markers, never re-elicited downstream"). It generalizes that proven convention so the other parameters use the same track, and it names the storage authority for each parameter (§4) — the state file for most, the governance spine for the AI-LENS mode.

---

## 2. Governing Principle

> **Ask once, at first touch. Record to the owning authority. Every downstream reader inherits; nobody re-asks.**
>
> A parameter is **not** collected up-front in a batch interrogation. It is resolved lazily — the **first** package that genuinely needs it runs the resolution protocol (§3): it checks whether the value is already recorded; if present, it uses it; if absent, it asks the user once, records it, and proceeds. Every package thereafter reads the recorded value and never asks again. A change is an **explicit, user-initiated** re-record (via the parameter's own toggle where one exists), not a re-prompt.

This is the input-side mirror of the family's Draft-First output discipline (`GATE_PROTOCOL.md` §21): the recorded value is the medium of exchange, not the chat.

---

## 3. The Resolution Protocol (`project-intake@1.0`)

Uniform for every parameter. A contributing package, at the first stage where the parameter matters, runs:

```
resolve(parameter):
  1. READ the parameter from its recorded authority (§4).
  2. IF present  -> use the recorded value; DO NOT ask. (proceed)
  3. IF absent   -> ASK the user ONCE (the parameter's elicitation prompt),
                    RECORD the answer to the parameter's authority,
                    (optionally) confirm back a one-line summary + a "change it?" affordance,
                    then proceed.
  4. A later change is a user-initiated re-record (toggle / new decision row),
     NEVER an automatic re-prompt.
```

**Properties every contributor honors:**

- **Ask-once.** The prompt fires at most once per project unless the user explicitly changes the value.
- **Lazy.** Resolution happens at first touch, not in an up-front batch. A parameter never asked is simply never needed by any package that ran.
- **Non-linear-entry safe.** Whichever package runs first (even standalone, out of chain order) performs the elicitation and records it (create-if-absent). Later packages detect-and-adopt.
- **Optional.** A parameter with a defined default may be left unset; absence resolves to the default (e.g. `questionMode` defaults to `prompt`; `deliveryMethod` absent = manual/AI-assisted, no `buildProfile`).
- **Additive (safe).** Recording a parameter never renames an existing marker; it adds a field/row.

---

## 4. Registered Parameters

Each contributing design registers exactly **one** parameter here: its key, allowed values, who elicits it, and **where the value is recorded** (its storage authority). The value's authority is the single writer; downstream packages read it.

| Parameter | Allowed values | Elicited by (first-touch) | Recorded authority | Inherited by | Status |
|-----------|----------------|---------------------------|--------------------|--------------|--------|
| `deliveryMethod` (+ `aiTool`, `teamAIMaturity`, `buildProfile`) | `manual` / `ai-assisted` / `ai-driven` / `hybrid` (+ tool name; maturity; `spec-driven`/`aidlc`/`freestyle` or omitted) | AI-PILC (`pilc-state.md`, at inception) or AI-POLC (`polc-state.md` → `## Velocity Model`, when PILC absent) | **State file** — `OUTPUT_AND_STATE_CONTRACT.md` §10.1 (per-project `*-state.md` markers) | AI-POLC (velocity model + dual-track timing); AI-DWG (projects `buildProfile` into `.governance/workspace-manifest.yaml`); AI-GCE (reads `buildProfile` for governance depth) | 🟢 **LIVE — reference implementation** |
| `aiMode` | `No-AI` / `AI-Powered` (+ sub-mode palette: Opportunity / Augmented / Native) | AI-LENS lens seam (first lens-aware node — ILC posture or PILC) | **Governance spine** — `Decision_Log` AI-mode row (`PILC-{ABBREV}-D-{N}`); current mode = latest row (AI-LENS design §3.2) | every lens-aware package (reads latest AI-mode row; No-AI = zero facet load) | 🟠 **Registered — CC-1 adoption DEFERRED.** AI-LENS keeps its own §4 Resolution Protocol for now (owner directive, 2026-07-15: "keep it here until everything works properly"). Its protocol is already an `project-intake@1.0`-conformant instance; formal consolidation onto this contract is a later step. |
| `deliveryMethod` elicitation ⟶ intake gate | (see `deliveryMethod` row) | AI-POLC (live build) | State file (§10.1) | (see above) | 🟡 **Wiring in progress** — the live Delivery-Method build (`02-in-progress/delivery-method-timing/`) is the **first design to consume this contract's resolution protocol** for its elicitation step instead of a bespoke gate. |
| `questionMode` | `prompt` (default) / `worksheet` | any package's Q&A phase (first stage that asks a question) | **State file** — `*-state.md` `Q&A Mode` field (Question-Persistence §3.6) | every package's Q&A phase (governs how questions are recorded) | 🟠 **Registered — pending build** (Question-Persistence WS-2, `01-not-started/`). Its ask-once contract is the model this primitive generalizes. |
| `variant` | per-package variant set (e.g. fast-track PILC, migration ADLC) | the package offering the variant, at entry | **State file** — `*-state.md` `variant` field (CC-5b boundary: *within* a package) | that package's stage routing | 🟠 **Registered — pending build + CC-5b boundary ratification** (`01-not-started/flow-authoring/`). |
| `familyFlow` | family-level alternate path (e.g. skip-UXD, start-at-PILC) | the first package under an alternate family flow | **State file** — `familyFlow` field (CC-5b boundary: *between* packages) | AI-FLO routing + each package's predecessor detection | 🟠 **Registered — pending build + CC-5b boundary ratification** (`01-not-started/flow-authoring/`). |

> **Storage note.** Most parameters live in the per-project state file (`OUTPUT_AND_STATE_CONTRACT.md` §10, Tier 2). The **AI-LENS `aiMode` is the deliberate exception** — it is a governance decision (reversible, audited), so its authority is the spine `Decision_Log`, not a state field. The resolution protocol (§3) is identical either way; only the READ/RECORD target differs per the authority column. This contract does not move any parameter's storage; it names each authority so there is one writer per parameter (no contention).

> **`variant` vs `familyFlow` (CC-5b).** These two are distinct parameters pinned to distinct fields precisely so they never collide: `variant` = the path *within* a package; `familyFlow` = the path *between* packages. Ratifying that boundary into the two `flow-authoring/` designs is tracked as D2 in the reconciliation plan and is a prerequisite to building either.

---

## 5. Contributing a New Parameter

To add a project-wide parameter, a design MUST:

1. **Register one row in §4** — key, allowed values, elicitor, recorded authority, inheritors, status. Do **not** invent a second intake gate.
2. **Pick an authority** — the per-project state file (default) or the governance spine (only for audited, reversible governance decisions, like `aiMode`). One writer only.
3. **Implement the resolution protocol (§3) verbatim** at the first stage the parameter matters — check → use-if-present → ask-once-and-record-if-absent → never re-prompt.
4. **Define a default** where the parameter is optional, so absence resolves without a prompt.
5. **Provide a change path** (a toggle/new decision row) if the value is user-reversible — a change is an explicit re-record, never an auto re-prompt.
6. **Stay additive:** add a field/row; never rename an existing marker.

---

## 6. Conformance Checklist

Every contributing package MUST:

- [ ] Register its parameter as **one row** in §4 — never build a parallel intake gate
- [ ] Resolve via the §3 protocol: **read first**, use-if-present, **ask-once-and-record** only if absent
- [ ] Read/write only its parameter's **declared authority** (§4) — one writer per parameter, no contention
- [ ] Elicit **lazily**, at first touch — never batch-interrogate the user up-front
- [ ] Be **non-linear-entry safe** — whichever package runs first elicits + records (create-if-absent); the rest detect-and-adopt
- [ ] Honor the parameter's **default** when optional (absence ⇒ default, no prompt)
- [ ] Treat a value change as a **user-initiated re-record**, never an automatic re-prompt
- [ ] Reference this contract (`project-intake@1.0`) from the design that owns the parameter

---

## 7. Relationship to Sibling Contracts

| Sibling contract | Relationship |
|------------------|--------------|
| `OUTPUT_AND_STATE_CONTRACT.md` §10.1 | **Storage authority** for state-file parameters (`deliveryMethod` and its companions). This contract generalizes §10.1's "capture once, inherit family-wide, never re-elicit" pattern into the family-wide intake primitive; §10.1 is the first (live) registered parameter. A companion note in §10.1 records that it is now one entry in this shared intake set. |
| `MANAGEMENT_FRAMEWORK_CONTRACT.md` §4 | **Storage authority** for the `aiMode` parameter (the spine `Decision_Log` row), under §4's create-if-absent/append contribution model. |
| `AI_LENS_DESIGN.md` §3/§4 | AI-LENS's own Resolution Protocol is a conformant `project-intake@1.0` instance kept in place for now (CC-1 adoption deferred); when consolidated, AI-LENS §4 collapses to "consume the primitive; contribute the `aiMode` row." |
| `GATE_PROTOCOL.md` §21 | The input-side mirror of Draft-First: the recorded parameter (not the chat) is the medium of exchange. Question-Persistence's `questionMode` governs how the Q&A phase itself is recorded. |

---

*Shared contract for the AI-* PDLC Family. Defines the single "ask-once → record → inform" intake surface for project-wide parameters (CC-1). Storage stays where each parameter's authority already lives (state file per `OUTPUT_AND_STATE_CONTRACT.md` §10.1, or the spine `Decision_Log` for the AI-LENS mode); this contract unifies the resolution protocol and registers the contributors. First live parameter: `deliveryMethod`.*
