<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Build-Method Resolution — the single point where AI-GCE reads `buildProfile`

> **Load this file** at the start of Mode 1 (Full Generation) and Mode 2 (Re-Derivation), before any generator runs. It is the **one** place AI-GCE reads the build method and decides how generation adapts. No generator re-reads `buildProfile`; every generator that needs to vary reads the resolved decision from here. Authority for the `aidlc` column: the FROZEN `ai-dwg/…/common/aidlc-v2-output-contract.md` §7 (AI-GCE builds against that contract).

## Why a single resolution point

AI-GCE has **24 rule-category generators**. The build method affects several of them (whether a check renders as a hook or a v2 sensor, whether the compliance log and process agents are generated at all, how enforcement is expressed). If each generator read `buildProfile` and decided for itself, the decision would be made 24 times and would drift the first time one generator was edited without the others. So the read happens **once, here**, and the generators consult the resolved decision — the same single-source discipline AI-TGE applies with `common/manifest-resolution.md` (item 6) and the phase mapping applies by reading AI-GCE's own `phase-gates-generator.md` rather than re-deriving it (items 7/16).

**Greenfield note:** before this file, **0 of 24 rule-category generators** dispatched on `buildProfile` — AI-GCE generated the same enforcement surface regardless of build method. This file is that dispatch, added in one place rather than sprinkled across the generators.

**Two existing readers already consume `buildProfile`** — `drift/drift-detection-engine.md` (detection *depth*) and `drift/gate-integration.md` (gate *strictness*). They are **not** a second and third resolution point: they read the same single `buildProfile` value and apply it to a different concern (drift/gate cadence, not the enforcement surface). This file owns the **generation-surface** resolution (hook vs sensor, compliance-log/agent emission, enforcement surface); the two drift/gate files own the **drift-cadence** resolution. All three read one value from one manifest field — the single-source rule is about the *value*, and it has exactly one source. Where their defaults must agree, they agree: a missing manifest is `Standard`/established behaviour in the drift files and `manual`/established behaviour here — both decline to assume `aidlc`.

## Where the value comes from

Read `buildProfile` from `.governance/workspace-manifest.yaml` (the manifest-driven discovery AI-GCE already uses — core-engine P2). It is a **5-value** field:

| `buildProfile` | Meaning |
|---|---|
| `aidlc` | The workspace feeds AI-DLC v2 — v2 owns the lifecycle, its native audit + learning loop are present |
| `spec-driven-speckit` | GitHub SpecKit build method |
| `spec-driven-kiro` | Kiro-native spec workflow |
| `freestyle` | No prescribed build method — a rules doc only |
| `manual` | Names the previously-implicit unset state |

If the manifest is absent (legacy fallback), treat as `manual` and warn — never guess `aidlc`, because the `aidlc` adaptations assume v2 is present and would suppress governance a non-v2 workspace needs.

## The resolved decisions — how generation adapts per value

The only value that changes generation today is `aidlc`; the other four leave AI-GCE's established behaviour intact. Each row below is the **resolved decision** a generator reads (the `aidlc` column is exactly the frozen contract §7 derivation, restated here as the single read-point):

| Generation decision | `aidlc` | `spec-driven-speckit` / `spec-driven-kiro` / `freestyle` / `manual` |
|---|---|---|
| Sensor-convertible checks (auth, injection, migration-rollback, etc.) | Render as **v2 sensors** (manifest + wiring), not platform hooks | Render as **platform hooks** (established behaviour) |
| The secrets/PII check | **Blocking pre-write hook, always** — only a hook stops a write before it lands (the one genuine hook⇄sensor pair) | Blocking pre-write hook (established behaviour) |
| Non-file-level items (session discipline, role isolation, sprint governance, phase gates) | Express as **v2 prose rules** (per the §2 heading set + the phase-vocabulary mapping) | Express as AI-GCE's own rules/agents (established behaviour) |
| Compliance log + process agents | **Not generated as a *primary* audit** for what v2 audits natively — but the observability **spine is kept in full** (score / trend / drift / dashboard / permanent JSONL); see `observability-read-and-persist.md` | **Generated** (established behaviour) |
| A check that runs as a **v2 sensor** | **Read-and-persist** — AI-GCE reads v2's audit outcome and persists the derived compliance event, does **not** re-run the check (would double-count). Audit-event mapping in `observability-read-and-persist.md` (ledger A9) | **Re-run** — the check fires as an AI-GCE hook and logs directly (no v2 sensor exists) |
| Hook file format | Resolved from `platformTargets` (unchanged by build method) | Resolved from `platformTargets` |
| Sensor-wiring verification | **Verify** `seeded.sensors` in `.governance/aidlc-bootstrap.yaml` landed (§7a Clause 3) — procedure in `common/sensor-wiring-verification.md` (item 26): an emitted manifest with no importing stage is a reportable finding, never a silent pass | N/A (no sensors emitted) |
| Enforcement surface guarantee | `enforcementSurface` conditional (`sensors` / `both` / `docs-only`) — `hookDefinitions` no longer unconditional (INV-L2-022) | `enforcementSurface: hooks` (the established unconditional case) |
| Three-tier progressive **gating** (Day 0 / Sprint 2+ / Pre-Release activation) | **Suspended** — v2 owns the lifecycle cadence; AI-GCE does not gate tier advancement | **Active** — the established progressive-enforcement gating (Mode 4 Tier Activation) |
| Three-tier **assessment** (coverage % + which band the workspace is in) | **Retained as advisory reporting** — the band is still computed and reported, it just no longer gates | **Retained** — drives both the report *and* the gate |

**The one thing that never varies:** the *governance content* — the rules themselves, derived from the workspace — is the same regardless of build method. `buildProfile` changes only **how** a rule is enforced (hook vs sensor vs prose) and **whether** AI-GCE emits its own audit surface (redundant under `aidlc`). It never changes **what** is governed. This is the boundary that keeps the dispatch safe: no rule is dropped because of the build method, only re-expressed.

> **`buildProfile` is one of two axes into the mechanism decision.** This file resolves the **build-method** axis; the **strength** axis (the user's `warn`/`block` choice) is resolved in `common/strength-to-mechanism.md` (merged item 24a), which reads `buildProfile` *from here* plus the recorded strength, the platform, and the rule's class/fireMoment, and returns the concrete mechanism (sensor / hook / prose). Generators ask that resolution point; they never branch on strength themselves.

## Tier gating vs tier assessment under `aidlc` — split, not dropped

AI-GCE's three-tier progressive-compliance model does **two** things that are easy to conflate: it **gates** (holds a team at Tier 1 until it is ready to activate Tier 2, etc. — Mode 4 Tier Activation) and it **assesses** (computes a coverage % and reports which band — Day 0 / Sprint 2+ / Pre-Release — the workspace sits in). Under `buildProfile: aidlc` these two are split:

- **Gating is suspended.** AI-DLC v2 owns the lifecycle cadence — it decides when a project moves between phases. A second, independent tier gate from AI-GCE would fight v2's cadence (two engines each holding the project at a different readiness bar). So under `aidlc`, AI-GCE does **not** gate tier advancement; Mode 4's *hold* behaviour is inactive.
- **Assessment is retained.** The coverage % and the band are **still computed and still reported** — as advisory information, not a gate. A team on v2 still learns "you are at ~78%, Sprint-2+ band" from AI-GCE's report; that number simply no longer blocks anything.

**Why split rather than drop (ledger row A13).** The tier *assessment* is a preserved AI-GCE capability — dropping it would lose the coverage visibility teams rely on. Only the *gating* teeth are removed under `aidlc`, and only because v2 already owns cadence. This is the same "re-express / re-scope, never drop" boundary the build-method dispatch itself honours: the capability survives, its enforcement authority is what changes. Under every non-`aidlc` build method, both gating and assessment stay exactly as before.

**Interaction with `enforcementSurface`.** Suspended gating does not touch the enforcement surface: sensors/hooks/prose are still emitted per the rows above. Gating governed *when* a tier's rules switch on; suspending it under `aidlc` means all applicable rules are available from the start (v2 sequences their relevance through its own phases), reported against the band rather than gated by it.

## What generators do with this

A generator that has no build-method variance (most of the 24) ignores this file entirely — it generates as it always has. A generator that *does* vary (the enforcement-surface generators — hooks-from-steering, security-compliance, cicd-gates, compliance-log-gov, agents-from-steering) reads the relevant resolved decision above and branches once. It does **not** re-read `buildProfile` or re-derive the mapping.

## Degradation

A build method this file does not recognise (a future sixth value) degrades to the non-`aidlc` column (established hook/agent behaviour) **and** discloses the unknown value in the generation summary — never silently assumes `aidlc`. Suppressing AI-GCE's own audit surface for an unrecognised build method would remove governance with nothing proven to replace it.

---

*Developer-side design detail · AI-GCE build-method resolution · © Mohammad Maheri*
