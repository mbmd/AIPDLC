<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Strength → Mechanism — the one place that turns "how hard" into "which surface"

> **Load this file** when a generator needs to know how a check is enforced. It is the **single resolution point** for the split the motto names: **the user picks the enforcement *strength*, the engine picks the *mechanism*.** Generators **ask** this file; they do **not** branch on strength individually. This is Improvement 10 work item 4 (§5.5). Loaded **on demand**, never into the always-loaded dispatcher (self-cap, CC-2). `TR-819` (`INV-L2-022`).

## The split — strength vs mechanism

Two different decisions were previously entangled in a single broken setup question ("warn mode or blocking mode?" — asked, then ignored, with no template behind either answer):

| | Who decides | Values |
|---|---|---|
| **Strength** — *how hard* a violation is treated | **the user** (recorded once, via the shared intake primitive) | `warn` (advisory) · `block` (stop the work) |
| **Mechanism** — *which surface* delivers the check | **the engine** (this file) | `sensor` · `hook` · `prose rule` |

The user never picks a mechanism, and the engine never overrides the user's strength. This file is the seam between them.

## The motto — reach for a sensor first

> *Fewer hooks, more sensors, as far as possible.* The engine reaches for a **sensor first** and a **hook only where the write-to-gate exposure window is genuinely unacceptable.*

So `block` does **not** mean "a blocking hook". Under `aidlc`, a `block`-strength check is delivered by a **gate-fired sensor** (it blocks the gate from opening) wherever catching the violation at the next gate is early enough — which it is for everything except a check that must stop a **single write before it lands**. Only that last case needs a hook.

## The resolution — inputs → mechanism

The resolution reads four inputs and returns one mechanism:

| Input | Source |
|---|---|
| **strength** | the user's recorded enforcement-strength parameter (`warn`/`block`) — recorded by `common/enforcement-strength-parameter.md` (item 24b) via the shared intake primitive; security-class checks only, default `warn` |
| **buildProfile** | `common/build-method-resolution.md` (the mechanism axis) |
| **harness / platform** | `platformTargets` (does this platform support hooks at all?) |
| **rule class + fireMoment** | the rule's neutral intermediate (`class`, `fireMoment` — item 23) |

**The resolution table:**

| strength | under `aidlc` | under non-`aidlc` |
|---|---|---|
| `warn` | **sensor** (advisory) where the check is sensor-convertible; else **prose rule** | **hook** (advisory) in the platform's format; else prose |
| `block`, `fireMoment: gate` | **gate-fired sensor** (blocks the gate opening) — no hook needed | **blocking hook** (item 24e), where the platform supports it; else CI gate |
| `block`, `fireMoment: write` **and** the write-to-gate window is unacceptable (only the secrets/PII class) | **blocking pre-write hook** (item 24c) — the one genuine hook⇄sensor pair | **blocking pre-write hook** |
| non-mechanisable (judgement) rule | **prose rule** (`memory/`) + process agent — strength is advisory-only, a judgement check cannot block deterministically | AI-GCE rule + process agent |

**The one case that forces a hook under `aidlc`:** `block` strength **and** `fireMoment: write` **and** the exposure between the write and the next gate is unacceptable. That is the **secrets/PII** class only — a secret written to disk is already leaked by the time a gate fires. Everything else at `block` strength is a gate-fired sensor.

**The two secrets/PII templates (merged item 24c).** Secrets/PII ships in two variants, selected by the resolved strength: `templates/hooks/sensitive-data-check.json` (advisory `askAgent`, `fileEdited`) when strength resolves to `warn`, and `templates/hooks/sensitive-data-check-blocking.json` (blocking `PreToolUse`, exit 2) when strength resolves to `block` **and** the platform supports pre-write blocking. The two carry **identical check logic** — only the action type and trigger differ (the re-expression boundary). Where the platform cannot block pre-write, the advisory variant is emitted and `PLATFORM_NOTES.md` discloses the limitation (P2 of the enforcement-strength parameter).

## Generators ask, they do not branch

Every generator that emits a mechanisable rule (via the neutral intermediate, item 23) calls this resolution rather than deciding hook-vs-sensor itself. This is the single-resolution-point discipline items 6 and 19 established, applied to the strength→mechanism question: one place answers "which surface delivers this check?", so the answer cannot drift across the 24 generators.

## Rides the shared intake primitive (CC-1) — no bespoke gate

The **strength** input is recorded through the **shared project-parameter intake primitive** (Cross-Design Reconciliation CC-1: "ask once → record to state → inform thereafter"), the same primitive `buildProfile` and the other project parameters use. This file does **not** add a fifth bespoke setup gate; it reads the recorded strength parameter (populated by item 24b) alongside the other inputs.

## Preserves capability, only re-expresses it (INV-L2-022)

Switching a check between sensor / hook / prose changes **how** it is enforced, never **whether** it is enforced or **what** it checks — the `enforcementSurface` guarantee is conditional on the mechanism but the check itself is preserved (INV-L2-022, item 9). A `warn`-strength check still logs; a `block`-strength check still stops the work; the mechanism is the only variable. No capability is dropped by any resolution outcome.

## Interaction with other files

| Related | Relationship |
|---|---|
| `common/build-method-resolution.md` | Provides the `buildProfile` mechanism axis; this file adds the strength axis on top |
| `rendering/neutral-intermediate.md` | Provides `class` + `fireMoment` + `severity`; the resolved mechanism tells the renderer which form to emit |
| (item 24b) enforcement-strength parameter | Populates the `strength` input via the shared intake primitive |
| `common/gate-fired-sensors.md` (item 24d) | Defines the three `block`+`fireMoment: gate` security-class checks this resolution routes to gate-fired sensors (auth presence, injection patterns, migration rollback), and carries the injection sensor script |
| `common/non-aidlc-blocking-hooks.md` (item 24e) | Supplies the **blocking hook** variants this resolution selects for a `block` security-class check under a hook-capable non-`aidlc` method (and the `freestyle` CI/CD-backstop fallback) |
| (item 24c) secrets/PII blocking hook | The other concrete mechanism this resolution selects between |

---

*Developer-side design detail · AI-GCE strength→mechanism resolution · © Mohammad Maheri*
