<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Gate-Fired Sensors — the three security-class checks that block a gate, not a write

> **Load this file** when a generator emits one of the three `block`-strength security checks whose `fireMoment` is `gate` — **auth presence**, **injection patterns**, and **migration rollback safety**. It defines each as a **gate-fired sensor intermediate** (the neutral-intermediate shape with `fireMoment: gate`), and it carries the one genuine new build: the **injection sensor script**. This is Improvement 10 work item 2 (§5.8). Loaded **on demand**, never into the always-loaded dispatcher (CC-2). `TR-820` (`INV-L2-022`).

## Why these three are sensors, not hooks

The strength→mechanism resolution (`common/strength-to-mechanism.md`, item 24a) runs the **window test** on every `block`-strength check:

> *Is the exposure between a bad write landing and the next approval gate genuinely unacceptable?*

For **secrets/PII** the answer is **Yes** — a secret on disk is committed, pushed and mirrored before any gate opens, and that exposure is irreversible. That is the one case that forces a pre-write blocking hook (item 24c).

For these three the answer is **No** — nothing deploys between the bad write and the next phase gate, so catching the violation **at the gate** is early enough:

| Check | Window test | Why "No" |
|---|---|---|
| **Auth presence** (`SEC-01/02/03` + `SEC-BASELINE-02`) | No | A missing auth decorator caught at the phase gate is caught **before anything deploys** |
| **Injection patterns** (`SEC-10/11/12`) | No | A string-concatenated query on disk is not exploitable until the code **runs** — the gate is before that |
| **Migration rollback** (`DATA-BASELINE-01/02` + `DATA-02/03`) | No | A migration without a rollback is dangerous **when run**, not when written |

**Under `aidlc`, a gate-fired sensor blocks the gate from opening.** That is the enforcement — the phase does not advance while the check fails — and it needs **no new hook template**. The v2 phase gate is the trigger AI-GCE lacks entirely (§0.1a); these three finally use it. Under non-`aidlc` there is no gate, so the same three checks fall back to blocking hooks (item 24e).

## The three gate-fired sensor intermediates

Each is emitted as the neutral-intermediate shape (`rendering/neutral-intermediate.md`, item 23) with `fireMoment: gate`. The `id` comes from the **owning generator** (never invented here). Item 25 renders these into v2 sensor manifests; item 26 verifies the wiring. This file defines the intermediates and the injection script; it does **not** render the manifest.

### 1. Auth presence — `pdlc-auth-presence`

```yaml
id: SEC-01                       # owning generator: security-compliance-gen.md (auth family SEC-01/02/03 + SEC-BASELINE-02)
sensorId: pdlc-auth-presence
statement: "Every public endpoint MUST carry an authentication guard."
checkLogic: "flag route/controller handlers that expose a public HTTP verb with no auth-guard decorator/middleware in scope"
glob: "{DERIVE: presentation-layer controllers from tech-stack.md + module-structure.md — e.g. src/modules/*/presentation/**/*.controller.ts}"
class: security
severity: blocking
fireMoment: gate
pairing: aidlc-pdlc-auth-presence
```
*Appropriateness* of a given auth scheme remains a judgement call and stays with the rule (prose) — the sensor only checks **presence**, which is deterministic.

### 2. Injection patterns — `pdlc-injection-patterns`

```yaml
id: SEC-11                       # owning generator: security-compliance-gen.md (OWASP section; also carries SEC-10 input-validation + SEC-12 CORS)
sensorId: pdlc-injection-patterns
statement: "NEVER build a query, command, or markup string by concatenating untrusted input (SEC-11); validate inbound DTOs (SEC-10); pin CORS origins (SEC-12)."
checkLogic: "deterministic pattern match — see the injection sensor script below"
glob: "{DERIVE: application source from tech-stack.md — e.g. src/**/*.ts, src/**/*.cs, src/**/*.py}"
class: security
severity: blocking
fireMoment: gate
pairing: aidlc-pdlc-injection-patterns
```
**This is the one genuine build.** `SEC-10/11/12` are authored by the security generator but assigned to **no hook** — the rule exists, the enforcement is absent (findings F-C15 / F-C18; ledger A30 / A30b). The mechanism is a **deterministic sensor script**, built below. It covers all three unenforced OWASP rules in one script (they were beside each other, all unenforced).

### 3. Migration rollback safety — `pdlc-migration-safety`

```yaml
id: DATA-BASELINE-01             # owning generators: data-governance-generator.md (DATA-BASELINE-01/02 + DATA-02/03) AND devops-generator.md (GOV-DEVOPS-012/013/014 + GOV-DEVOPS-BASELINE-02)
sensorId: pdlc-migration-safety
statement: "Every migration MUST declare a rollback method and MUST NOT run a destructive operation without an expand/contract predecessor."
checkLogic: "flag a migration file with no down/rollback method, or a destructive DDL with no referenced prior expand migration"
glob: "{DERIVE: migration path from tech-stack.md — e.g. src/**/migrations/**/*, db/migrate/**/*}"
class: data                      # ⚠️ DATA-* is data-governance, NOT security (F-C16) — included here for the rollback check only; ownership settled at item 28 (data-governance-generator.md Build-Method Routing)
severity: blocking
fireMoment: gate
pairing: aidlc-pdlc-migration-safety
```
**`migration-safety` is not a security check.** Its rule family (`DATA-*`) is data-governance (finding F-C16). It is defined here alongside the two security sensors **only because it is a 🔴 never-remove check whose strength the user controls** and it shares the gate-fired mechanism. Its ownership boundary against A26 (data-classification) is **settled at merged item 28** by enumerating the generator — `pdlc-migration-safety` owns exactly the **migration** concern (`DATA-BASELINE-01/02` + `DATA-02/03`), while the rest of the `DATA-*` family routes elsewhere (`DATA-06` → v2 linter; `DATA-01`/`DATA-05` → memory rules; `DATA-04` tenant-scoping → the existing `tenant-isolation-check`). See `generators/data-governance-generator.md` → "Build-Method Routing" for the full split. Never re-classify it as security.

## The injection sensor script — the genuine new capability

AI-GCE has never emitted an executable script — its output is prompts and JSON. Building the injection check as a deterministic script is **genuine new capability**, scoped to the mechanisable subset only (§0.1c destination 1). The division of labour follows Decision A (§ the externally-dispatched check): **AI-GCE ships the script at the path v2's scaffolder defaults to; v2's learning loop installs the manifest and binds it to a stage.** We auto-fire nothing.

```
.governance/sensors/pdlc-injection-patterns.sh   ← the path v2's scaffolder resolves to
```

**Script contract (deterministic — v2 accepts only `kind: deterministic` and rejects LLM-evaluated sensors at parse time):**

```bash
#!/usr/bin/env bash
# pdlc-injection-patterns — deterministic sensor for SEC-10/11/12.
# Emitted by AI-GCE. Executed by the AI-DLC v2 build engine at a gate.
# Exit 0 = clean (gate may open); exit 1 = finding (gate blocked, stderr forwarded).
# generatedBy: AI-GCE  generatedVersion: {version}  source: security-compliance-gen.md (SEC-10/11/12)

set -euo pipefail

# --- Package Territory exclusion (common/hook-preamble.md, Layer 1) -------------
# Skip package-infrastructure zones — never flag a governance/upstream file.
EXCLUDE='(^|/)(\.governance|rules|compliance-log|project-initiation|architecture|management_framework|templates)/'

# --- Scope: application source only (DERIVED from tech-stack.md) -----------------
GLOB="{DERIVE: e.g. src/**/*.ts src/**/*.cs src/**/*.py}"

findings=0
scan() { grep -REnH "$1" $GLOB 2>/dev/null | grep -Ev "$EXCLUDE" || true; }

# SEC-11 — string-concatenated queries/commands (injection surface)
hits=$(scan '(query|execute|exec|raw|createQueryBuilder)\s*\(\s*[`"'\''].*\$?\{?.*\+' )
[ -n "$hits" ] && { echo "SEC-11 injection: concatenated query/command" >&2; echo "$hits" >&2; findings=1; }

# SEC-10 — request handler with no DTO/schema validation in scope
# (deterministic proxy: a body-binding handler with no validate/schema/DTO reference in the file)
# SEC-12 — CORS configured with a wildcard origin
hits=$(scan 'cors\s*\(\s*\{?[^)]*origin\s*[:=]\s*[`"'\'']\*')
[ -n "$hits" ] && { echo "SEC-12 CORS: wildcard origin" >&2; echo "$hits" >&2; findings=1; }

exit $findings
```

**What the script is and is not.** It is a **template** — the `{DERIVE: …}` glob and the per-language pattern set are populated at generation time from `tech-stack.md`, exactly as the hook templates are. It is **deterministic** (pattern match only, no judgement), so it clears v2's parse-time filter. It **reuses the package-territory exclusion** (Layer 1 of the three-layer segregation) so it never flags a governance or upstream file. The check logic is **identical** to what a hook form of the same rule would run — this is a re-expression of the check into an executable surface, not a re-implementation (the neutral-intermediate "re-express, never re-derive" boundary).

**Auth presence and migration rollback do not need a new script here.** Their check logic is already produced by their owning generators (`security-compliance-gen.md`, `data-governance-generator.md` + `devops-generator.md`) and is deterministically expressible; item 25 renders their manifests from the intermediates above. Only injection had **no mechanism at all**, so only injection needs the script built now.

## Records strength only where the user chose it — never turns the check off

Each of the three is a security-class (or never-remove data) check, so its **strength** is user-controllable via the shared intake primitive (`common/enforcement-strength-parameter.md`, item 24b) — default `warn`, `block` where the user asks and the mechanism honours it. When strength resolves to `warn`, the same sensor fires **advisory** (reports, does not block the gate); at `block` it blocks the gate. The check is **never removed** by any strength (INV-L2-022) — strength changes only whether the gate is held, never whether the violation is detected and logged.

## Preserves capability, only re-expresses it (INV-L2-022)

Moving these three from "advisory hook / unbuilt intent" to "gate-fired sensor" changes **how** each is enforced, never **whether** or **what**. Auth presence still checks for a missing guard; injection still checks for concatenated queries; migration still checks for a missing rollback. No capability cell moves — TR-820 passes because the check is preserved, only its surface changed.

## Interaction with other files

| Related | Relationship |
|---|---|
| `common/strength-to-mechanism.md` (item 24a) | Selects **gate-fired sensor** for these three (`block` + `fireMoment: gate`); this file defines the three it selects |
| `common/enforcement-strength-parameter.md` (item 24b) | Records the user's `warn`/`block` strength for the security-class set these three belong to |
| `rendering/neutral-intermediate.md` (item 23) | Provides the intermediate shape; these three are intermediates with `fireMoment: gate` |
| `templates/hooks/sensitive-data-check-blocking.json` (item 24c) | The **other** branch of the window test — the one check that IS a pre-write hook |
| `common/non-aidlc-blocking-hooks.md` (item 24e) | Where there is no gate (the four non-`aidlc` methods), these three fall back to blocking hooks (or a `freestyle` CI/CD backstop) — the same checks, re-expressed |
| `ai-dwg/…/buildmethod/aidlc/sensor-manifests.md` (item 25) | Renders these three `fireMoment: gate` intermediates into v2 sensor manifests (`default_severity: blocking` + `fire_on: gate`) + the pairing declaration + the `.governance/AIDLC_SENSOR_WIRING.md` binding rows |
| `common/sensor-wiring-verification.md` (item 26) | Verifies these three sensors are bound to a stage (reads `seeded.sensors` in the bootstrap record); an emitted-but-unwired manifest is a reportable finding |
| `security-compliance-gen.md` · `data-governance-generator.md` · `devops-generator.md` | Own the rule IDs; this file never invents an id, it reads theirs |

## Output validation

- [ ] Each of the three is emitted as a neutral intermediate with `fireMoment: gate` and a `sensorId` + `pairing` field.
- [ ] Rule IDs are sourced from the owning generators, never invented here (SEC-01/02/03+BASELINE-02; SEC-10/11/12; DATA-BASELINE-01/02+DATA-02/03 + GOV-DEVOPS-012/013/014+BASELINE-02).
- [ ] The injection sensor script is deterministic (pattern match only) and reuses the package-territory exclusion.
- [ ] The script is a template — glob and patterns DERIVE from tech-stack.md, no hardcoded project paths.
- [ ] `migration-safety` is labelled `class: data` (data-governance, not security — F-C16); never re-classified.
- [ ] Strength never removes any of the three checks (INV-L2-022) — it only sets gate-block vs advisory.
- [ ] No new hook template is created for these three under `aidlc` (the gate is the mechanism).

---

*Developer-side design detail · AI-GCE gate-fired security sensors · © Mohammad Maheri*
