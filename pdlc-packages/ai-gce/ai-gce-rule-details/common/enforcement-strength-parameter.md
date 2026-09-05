<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Enforcement-Strength Parameter — the setup question, made real

> **Load this file** when AI-GCE records the enforcement strength at setup. It makes the existing (asked-but-ignored) *"warn mode or blocking mode?"* question **real** and populates the `strength` input that `common/strength-to-mechanism.md` (merged item 24a) reads. Improvement 10 · the retired Decision F. Constraints `P1`–`P4` below. `TR-824` · `TR-827`.

## The broken promise this fixes

AI-GCE **already asks** the user *"should hooks start in warn mode or blocking mode?"* at setup — and then **does the same thing regardless**, because every one of its hook templates is advisory and there is **no template behind either answer**. That is a broken promise, not an open policy question. Item 24b makes the answer load-bearing: the recorded strength flows into the strength→mechanism resolution point, which selects a mechanism that can actually honour it.

## The four constraints (P1–P4)

The parameter is deliberately narrow. It obeys four constraints, all from the retired Decision F:

| # | Constraint | Why |
|---|---|---|
| **P1** | **Security-class checks only.** The strength dial is offered for the security-class set, **not** for every rule. | Most rules have a settled enforcement posture (advisory, or gate-fired under `aidlc`); only the security class has a genuine warn-vs-block choice worth exposing. A per-rule dial for all 300+ rules would be noise. |
| **P2** | **Asked only where the answer can be honoured.** If the active platform + build method cannot deliver a `block` (e.g. an advisory-only harness with no hook and no gate), the question is **not asked** — the parameter defaults and the workspace discloses the limitation. | Offering a choice the engine cannot honour is the same broken promise in a new place. Ask only where both answers are deliverable. |
| **P3** | **Defaults to `warn`.** Absent an explicit `block`, the recorded strength is `warn`. | AI-GCE's own principle: "warn before blocking; all hooks start in warn mode." Blocking is opt-in, never the silent default. |
| **P4** | **Rides the shared project-parameter intake primitive** (CC-1: ask once → record to state → inform thereafter). It does **not** add a bespoke setup gate. | `buildProfile` and the other project parameters already use this primitive; the enforcement strength is another such parameter. A fifth bespoke gate would be the reinvention CC-1 exists to prevent. |

## The security-class set — what the dial applies to

| Check | Rule IDs | Class |
|---|---|---|
| **secrets/PII** (`sensitive-data-check`) | `SEC-BASELINE-01` + `SEC-20/21/22` | security |
| **auth presence** (`security-gate-check`) | `SEC-01/02/03` + `SEC-BASELINE-02` | security |
| **injection patterns** | `SEC-10/11/12` (rules exist, enforcement was absent — F-C15/F-C18; ✅ built as the injection sensor script at item 24d, `common/gate-fired-sensors.md`) | security |
| **migration rollback** (`migration-safety`) | `DATA-BASELINE-01/02` + `DATA-02/03` + `GOV-DEVOPS-*` | **data-governance, NOT security** |

> **`migration-safety` is included in the strength dial but is NOT a security check** (F-C16 — it enforces `DATA-*` via the data-governance generator, not the security generator). It is included **only** because it is a 🔴 never-remove check whose enforcement strength the user should also control — its *ownership* stays data-governance (resolved cleanly at item 28). Including it here is a strength-control decision, not a re-classification.

## What the recorded value drives — it does NOT pick the mechanism

The parameter records **strength** (`warn` / `block`) and nothing more. It does **not** choose hook-vs-sensor — that is `strength-to-mechanism.md`'s job (item 24a). The separation is the whole point of the retired Decision F: **the user picks the strength; the engine picks the mechanism.** So `block` recorded here becomes, at resolution time, a gate-fired sensor under `aidlc` for auth/injection/migration-rollback and a pre-write blocking hook only for secrets/PII (the one unacceptable-window case).

## Recording shape

Stored via the shared intake primitive into the workspace state — one entry per security-class check (or a single default when the user accepts the default for all):

```yaml
# recorded via the shared project-parameter intake primitive (CC-1)
enforcement_strength:
  secrets-pii:        block | warn      # default warn
  auth-presence:      block | warn      # default warn; asked only if the platform/build-method can block
  injection:          block | warn      # default warn
  migration-rollback: block | warn      # default warn
```

Where P2 suppresses the question (the answer cannot be honoured), the entry records `warn` and the workspace's `PLATFORM_NOTES.md` discloses that blocking was unavailable on this platform/build-method.

## Preserves the check regardless of strength (INV-L2-022)

`warn` and `block` differ only in what happens *on a violation* — both still **run** the check and **log** the outcome. Strength never turns a check off; it never changes what is governed. No capability is added or removed by the parameter (INV-L2-022, the conditional `enforcementSurface`).

## Interaction with other files

| Related | Relationship |
|---|---|
| `common/strength-to-mechanism.md` | **The consumer** — reads the recorded `enforcement_strength` as its strength input (item 24a) |
| `common/build-method-resolution.md` | Provides `buildProfile`, which P2 uses to decide whether `block` is deliverable |
| `common/gate-fired-sensors.md` (item 24d) | Defines the three gate-fired sensors (auth presence, injection patterns, migration rollback) a recorded `block` resolves to under `aidlc`, and carries the injection sensor script |
| `common/non-aidlc-blocking-hooks.md` (item 24e) | Supplies the blocking-hook variants a recorded `block` resolves to under a hook-capable non-`aidlc` method (and the `freestyle` CI/CD-backstop fallback, disclosed per P2) |
| (item 24c) secrets/PII blocking hook | The other concrete mechanism a recorded `block` resolves to |

---

*Developer-side design detail · AI-GCE enforcement-strength parameter · © Mohammad Maheri*
