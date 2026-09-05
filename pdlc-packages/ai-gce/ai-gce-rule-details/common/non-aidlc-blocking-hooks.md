<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Non-`aidlc` Blocking Hooks — where there is no gate, "enforce" means a blocking hook

> **Load this file** when the resolved `buildProfile` is **not** `aidlc` and a security-class check has resolved to `block` strength. Under `aidlc` a `block` check is a gate-fired sensor (`common/gate-fired-sensors.md`, item 24d) — but the four non-`aidlc` build methods have **no phase gate**, so the sensor mechanism does not exist there. This file defines how the same `block` strength is honoured under those methods: a **blocking hook** where the harness supports one, a **CI/CD backstop** where it does not. This is Improvement 10 work item 3 (§5.8). Loaded **on demand**, never into the always-loaded dispatcher (CC-2). `TR-820` (`INV-L2-022`).

## Why this file exists — the gate is an `aidlc`-only mechanism

Item 24d routes three security-class checks (auth presence, injection patterns, migration rollback) to **gate-fired sensors**: under `aidlc` a failing sensor holds the phase gate shut, and that *is* the enforcement. But the phase gate is a **v2 mechanism** — it exists only under `buildProfile: aidlc`. Under the other four build methods there is no gate to hold, so the gate-fired sensor has nothing to fire against. The check still has to be enforceable at `block` strength (the user asked for it, and the strength must be honoured wherever it can be — P2 of the enforcement-strength parameter). The only surface left that can stop bad code under a non-gate build method is a **blocking hook**.

This is the non-`aidlc` half of the resolution table in `common/strength-to-mechanism.md`: the row that reads *"`block`, `fireMoment: gate` → blocking hook (item 24e), where the platform supports it; else CI gate"*.

## The mechanism per build method

The design's harness table settles which surface each method uses:

| build method | advisory (`warn`) | blocking (`block`) |
|---|---|---|
| `aidlc` | write-fired sensor | **gate-fired sensor** (item 24d) — a hook only for secrets/PII |
| `spec-driven-kiro` | advisory hook | **blocking hook** — no sensor mechanism exists under this method |
| `spec-driven-speckit` | advisory hook | **blocking hook** — same |
| `manual` | advisory hook | **blocking hook** — same |
| `freestyle` | rules doc | **CI/CD backstop** — the harness question does not arise (no hook lifecycle) |

**`spec-driven-kiro` / `spec-driven-speckit` / `manual`** run in a harness with a pre-write hook lifecycle, so a `block`-strength security check becomes a **blocking hook** (a `PreToolUse`/pre-write hook that exits non-zero on a violation). **`freestyle`** has no hook lifecycle at all — there is no harness to host a hook — so a `block`-strength check is delivered by a **CI/CD backstop** (a pipeline gate) instead, and the workspace's `PLATFORM_NOTES.md` records that pre-write blocking was unavailable (P2).

## Scoped to the security-class set — never a blocking hook for a style rule

The blocking-hook variants are built **only** for the security-class set (the same P1 scope as the enforcement-strength parameter):

| Check | Rule IDs | Non-`aidlc` blocking variant |
|---|---|---|
| **secrets/PII** | `SEC-BASELINE-01` + `SEC-20/21/22` | ✅ **Already built** — `templates/hooks/sensitive-data-check-blocking.json` (item 24c). It is a pre-write hook under *every* build method, `aidlc` included, because its exposure window is unacceptable regardless of gate. Nothing new here. |
| **auth presence** | `SEC-01/02/03` + `SEC-BASELINE-02` | **Blocking hook variant** of `security-gate-check` — the same check the `aidlc` gate-fired sensor `pdlc-auth-presence` runs, re-expressed as a blocking hook |
| **injection patterns** | `SEC-10/11/12` | **Blocking hook variant** wrapping the **same injection check** — under non-`aidlc` the deterministic pattern match built at item 24d runs inside a blocking hook instead of a gate-fired sensor |
| **migration rollback** | `DATA-BASELINE-01/02` + `DATA-02/03` + `GOV-DEVOPS-*` | **Blocking hook variant** of `migration-safety` — `class: data`, included in the security-strength set only because the user controls its strength (F-C16; ownership stays data-governance, settled at item 28 — see `generators/data-governance-generator.md` "Build-Method Routing") |

A blocking hook for a naming-convention or a style rule is out of scope — a style violation that blocks a write is exactly the noise P1 exists to prevent. Only the security-class set gets a blocking variant.

## The check is identical — only the surface changes (the re-expression boundary)

A non-`aidlc` blocking hook for auth/injection/migration runs the **same `checkLogic` and `glob`** as the `aidlc` gate-fired sensor for that check — the neutral intermediate (`rendering/neutral-intermediate.md`, item 23) is the single source both render from. The blocking hook is the **hook render** of the intermediate; the gate-fired sensor is the **sensor render**. Neither re-derives the check. For injection specifically, the deterministic script built at item 24d is the check body in both cases: under `aidlc` the build engine runs it at a gate; under a non-`aidlc` harness the blocking hook runs the same script pre-write and exits non-zero on a finding. This is the same "re-express, never re-derive" boundary items 19/21/23 hold.

Each blocking-hook variant carries the **package-territory preamble** (`common/hook-preamble.md`, Layer 2) and logs on every fire, block included (Rule 5) — identical to every other AI-GCE hook.

## Resolved by the single resolution point — generators still do not branch

A generator emitting one of these four security-class checks calls `common/strength-to-mechanism.md`, which reads `buildProfile` + platform and returns the mechanism. Under a non-`aidlc` build method with `block` strength and a hook-capable harness, that resolution returns **blocking hook** and this file supplies the variant. The generator never contains a `buildProfile == 'aidlc' ? sensor : hook` branch — the resolution point owns the decision (the single-resolution-point discipline of items 6/19/24a).

## Preserves capability, only re-expresses it (INV-L2-022)

The auth/injection/migration checks are the same capability whether delivered as a gate-fired sensor (under `aidlc`), a blocking hook (under a hook-capable non-`aidlc` method), or a CI/CD backstop (under `freestyle`). No check is dropped when the build method changes — only the surface that delivers it. TR-820 passes because no capability cell moves; the mechanism column is conditional on `buildProfile`, the check is not.

## Interaction with other files

| Related | Relationship |
|---|---|
| `common/strength-to-mechanism.md` (item 24a) | Selects **blocking hook** for a `block` security-class check under a hook-capable non-`aidlc` method; this file supplies the variant |
| `common/gate-fired-sensors.md` (item 24d) | The `aidlc` counterpart — the same three checks as gate-fired sensors; this file is their non-gate fallback |
| `templates/hooks/sensitive-data-check-blocking.json` (item 24c) | The secrets/PII blocking hook — already a pre-write hook under every method, so it needs no non-`aidlc` variant |
| `common/enforcement-strength-parameter.md` (item 24b) | P1 (security-class only) + P2 (asked only where honourable — `freestyle` falls to CI/CD, disclosed in `PLATFORM_NOTES.md`) scope this file |
| `rendering/neutral-intermediate.md` (item 23) | The single source both the blocking hook and the gate-fired sensor render from — identical `checkLogic` + `glob` |
| `common/hook-preamble.md` | The package-territory preamble every blocking-hook variant carries |

## Output validation

- [ ] Blocking-hook variants are built ONLY for the security-class set (auth, injection, migration; secrets/PII already covered by item 24c).
- [ ] `spec-driven-kiro` / `spec-driven-speckit` / `manual` → blocking hook; `freestyle` → CI/CD backstop (no hook lifecycle).
- [ ] Each variant runs the SAME `checkLogic` + `glob` as the `aidlc` gate-fired sensor for that check (re-expression, not re-implementation).
- [ ] The injection variant runs the deterministic script built at item 24d, pre-write, exiting non-zero on a finding.
- [ ] Each variant carries the package-territory preamble and logs on block (Rule 5).
- [ ] Where blocking is not deliverable (`freestyle`), `PLATFORM_NOTES.md` discloses the fallback (P2).
- [ ] No blocking-hook variant is built for a non-security-class (style/naming) rule.

---

*Developer-side design detail · AI-GCE non-`aidlc` blocking-hook variants · © Mohammad Maheri*
