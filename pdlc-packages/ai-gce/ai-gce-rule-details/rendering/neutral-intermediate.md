<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Neutral Intermediate — one rule representation, rendered to hook OR sensor

> **Load this file** at the start of the rendering step, before `governance-rendering.md` wires per-platform adapters. It defines the **format-neutral intermediate** each mechanisable rule is expressed as, and the **two-axis** render that turns it into a platform hook or an AI-DLC v2 sensor. This is the **prerequisite for sensor emission** (merged item 25) — a sensor can only be rendered once the neutral intermediate exists. Design §8.5 ("Refactor needed"). Improvement — the AI-GCE neutral-format refactor.

## The problem this fixes

Today AI-GCE's generators render **directly to Kiro hook JSON**. That hardwires two decisions into the generator: (1) the output *format* (Kiro `.json`) and (2) the enforcement *mechanism* (a platform hook). Under `aidlc`, most checks must instead become **v2 sensors** — a different mechanism entirely. A generator that emits hook JSON directly cannot also emit a sensor; it would need a parallel code path per generator (the drift the single-resolution-point discipline exists to prevent).

**The fix:** generators emit a **format-neutral intermediate** — the rule, its check logic, and its file glob — and a **renderer** turns that intermediate into whichever form the two axes call for. One source, two possible mechanisms, many possible formats.

## The neutral intermediate — the shape a generator emits

Every **mechanisable** rule (a deterministic, file-or-gate-checkable constraint) is emitted as this platform-and-mechanism-neutral record, not as hook JSON:

```yaml
# neutral intermediate — one per mechanisable rule
id: SEC-01                       # the rule ID, from the OWNING generator (never invented here)
statement: "All endpoints MUST validate the Authorization header."
checkLogic: "grep for route handlers lacking an auth-guard decorator/middleware"
glob: "src/modules/*/presentation/**/*.controller.ts"   # derived from tech-stack + module-structure
class: security | data | architecture | naming | testing | api | governance
severity: blocking | advisory     # the rule's own severity (from its generator)
fireMoment: write | gate          # when the check should run (pre-write vs at an approval gate)
```

The intermediate carries **no** Kiro-specific field, **no** v2-manifest-specific field, and **no** decision about hook-vs-sensor. It is the pure statement of *what is checked, where, and how hard*. The rendering axes below decide the rest.

## The two render axes

The renderer reads the neutral intermediate and two manifest signals:

| Axis | Signal | Decides |
|---|---|---|
| **Mechanism** | the **strength→mechanism resolution point** (`common/strength-to-mechanism.md`, merged item 24a) — which reads `buildProfile` (via `build-method-resolution.md`) + the recorded enforcement strength + platform + this intermediate's `class`/`fireMoment` | **sensor** / **hook** / **prose rule** — sensor first, hook only where the write-to-gate window is unacceptable (secrets/PII) |
| **Format** | `platformTargets` (via `governance-rendering.md`) | *which* hook format — Kiro `.json`, Claude `settings.json`, CI gate, etc. |

The two axes are **orthogonal** and resolved by two different files — this file owns neither decision, it owns the **neutral source** they both render from:

```
generator  →  neutral intermediate (this file's shape)
                     │
      ┌──────────────┴───────────────┐
   mechanism = hook             mechanism = sensor   (buildProfile → build-method-resolution.md)
      │                              │
   format per platformTargets    v2 sensor manifest   (item 25 renders this from the intermediate)
   (governance-rendering.md)      (contract §4 field set)
```

## What renders to what

| Neutral intermediate | Under non-`aidlc` | Under `aidlc` |
|---|---|---|
| A **sensor-convertible** check (the 8 advisory-class rules + the gate-fired security set) | Rendered to a **platform hook** in the format `platformTargets` selects | Rendered to a **v2 sensor manifest** (item 25), fired on write or at a gate per `fireMoment` |
| The **secrets/PII** check | Blocking pre-write **hook** | **Still a hook** — only a hook stops a single write before it lands (the one genuine hook⇄sensor pair; build-method-resolution.md) |
| A **non-file-level** rule (session discipline, role isolation, sprint gov, phase gates) | AI-GCE rule/agent | **v2 prose rule** (`memory/`), not a sensor — not every intermediate becomes a sensor |

**Not every rule has a neutral intermediate.** Only **mechanisable** rules (deterministic, file-or-gate-checkable) do. A judgement rule (needs human reasoning) is not emitted as an intermediate — it stays a process agent or a prose rule. Emitting an intermediate for a non-mechanisable rule would imply a sensor could check it, which is false.

## Why this is the prerequisite for item 25

Item 25 (sensor manifests + wiring) renders v2 sensor manifests. A manifest is a rendering **of the neutral intermediate** into v2's field set (`id`, `kind: deterministic`, `command`, `default_severity`, `matches`, `fire_on`, contract §4). Without the neutral intermediate, item 25 would have to reverse-engineer a sensor out of hook JSON — parsing a Kiro-specific artifact back into a rule. The neutral intermediate is the clean source item 25 renders from; that is why item 23 comes first.

## The renderer preserves the check, never rewrites it

A rule's `checkLogic` and `glob` are **identical** whether rendered to a hook or a sensor — the same check, expressed in two mechanisms. The renderer never re-derives the check for one mechanism; if a hook checks "no auth-guard on this controller", the sensor checks exactly that. This is what makes the hook↔sensor switch a re-expression, not a re-implementation (the same "re-express, never re-derive" boundary the build-method dispatch and the observability read-and-persist both hold).

## Interaction with other files

| Related | Relationship |
|---|---|
| `generators/*` (the 24 rule-category generators) | Emit the neutral intermediate for their mechanisable rules — no longer render hook JSON directly |
| `common/build-method-resolution.md` | Owns the **mechanism** axis (hook vs sensor) — the renderer reads its resolved decision |
| `rendering/governance-rendering.md` | Owns the **format** axis (which platform hook format) — renders the hook side |
| `generators/hooks-from-steering.md` | Now renders the **hook** form *of the neutral intermediate* (rather than being the origin of hook JSON) |
| `common/gate-fired-sensors.md` (item 24d) | Defines the three `block`+`fireMoment: gate` security-class intermediates (auth presence, injection patterns, migration rollback) and carries the injection sensor script — the concrete gate-fired intermediates item 25 renders |
| `ai-dwg/…/buildmethod/aidlc/sensor-manifests.md` (item 25, AI-DWG side) | Renders the **sensor** form of this intermediate into v2's §4 field set (`id`/`kind: deterministic`/`command`/`default_severity`/`matches`/`fire_on`) + the pairing declaration + the executable check-script; the emitter re-expresses this intermediate's `checkLogic`+`glob`, never re-derives them |

## Output validation

- [ ] Each mechanisable rule is emitted as a neutral intermediate (id + statement + checkLogic + glob + class + severity + fireMoment), not as hook JSON directly.
- [ ] The intermediate carries no platform-specific and no mechanism-specific field.
- [ ] Mechanism axis resolved once via `build-method-resolution.md`; format axis via `governance-rendering.md` — never conflated.
- [ ] `checkLogic` + `glob` are identical across the hook and sensor renders of the same rule.
- [ ] Non-mechanisable (judgement) rules are NOT emitted as intermediates — they stay agents/prose.
- [ ] The secrets/PII check renders to a hook under every build method (never a sensor).

---

*Developer-side design detail · AI-GCE neutral-format intermediate · © Mohammad Maheri*
