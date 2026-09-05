<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Data Governance — Derivation Logic

## Purpose

Derives data governance rules (DATA-*) from `database-rules.md`. 100% steering-derived for project-specific rules; built-in baseline provides migration safety floor.

---

## MANDATORY: Stage Sub-Role — Data Architect

During THIS activity, ALSO adopt the mindset of a **Data Architect**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in data safety: schema migrations are irreversible operations that can destroy production data
- Treat migration-safety as Tier A (immediate): a destructive migration is dangerous from the moment it's written
- Derive schema patterns from database-rules.md — DDD aggregates, ERD, document store each have different rules
- Ensure expand-contract is enforced for ALL breaking schema changes (no shortcuts to "just drop the column")
- Consider multi-tenancy implications: if tenant scoping exists, EVERY query must include tenant_id

### Anti-Patterns for This Activity
- Do NOT allow DROP TABLE/COLUMN without expand-contract process documented in the migration
- Do NOT assume database technology — derive from database-rules.md + docker-compose.yml confirmation
- Do NOT generate tenant-scoping rules unless multi-tenancy.md exists (conditional signal)

### Quality Check
A good output from this activity sounds like:
- "DATA-BASELINE-01: Every migration MUST have a rollback/down method. Enforced by migration-safety.json (fileEdited, Tier A 🔴). Pattern: `src/migrations/**/*.ts`. sessionDedup: true."
- "DATA-03: Expand-contract for breaking changes. Verification: any migration containing ALTER TABLE DROP COLUMN must reference a prior expand migration."

---

## Source: `database-rules.md`

| Section to Extract | Generated Rules |
|-------------------|----------------|
| Schema patterns | DATA-01: Schema follows stated pattern (DDD aggregates / ERD / document store) |
| Migration rules | DATA-02: Backward-compatible migrations only; DATA-03: Expand-contract for breaking changes |
| Tenant scoping (if multi-tenant) | DATA-04: Every query scoped to tenant_id |
| Caching strategy | DATA-05: Cache invalidation follows stated pattern |
| Naming conventions (tables/columns) | DATA-06: Table/column naming per stated convention |

## Built-in Baseline

| Rule ID | Statement |
|---------|-----------|
| DATA-BASELINE-01 | Every migration MUST have a rollback/down method |
| DATA-BASELINE-02 | No destructive schema operations (DROP TABLE/COLUMN) without expand-contract |

## Build-Method Routing — the `DATA-*` ownership boundary under `aidlc` (merged item 28)

> Resolves finding **F-C16** (the `migration-safety` double-classification) and settles ledger rows **A26**/**A31**. This is **not a judgement call** — enumerating the `DATA-*` family above shows it **splits by concern, then by mechanisability**. Under `buildProfile: aidlc`, each `DATA-*` rule routes to the surface its concern and checkability warrant; under the four non-`aidlc` methods the `migration-safety.json` hook is retained (no v2 sensor mechanism exists there). The rule set above is unchanged — this section only states *where each rule is enforced* per build method.

| `DATA-*` rule(s) | Concern | Under `aidlc` — routes to | Why |
|---|---|---|---|
| `DATA-BASELINE-01/02` + `DATA-02/03` | **Migration safety** (rollback present, expand-contract, no unguarded destructive op) | **`pdlc-migration-safety` gate-fired sensor** (built at merged item 24d, `common/gate-fired-sensors.md`) | All four are structural and deterministically checkable at a gate; the window test returns No (a migration is dangerous *when run*, not when written), so a gate-fired sensor suffices — no blocking hook needed under `aidlc` |
| `DATA-06` | **Table/column naming** | **v2's shipped linter** | It is a naming regex on tables/columns — exactly the class the motto sends to v2's own linter rather than a custom manifest (the same routing as `NC-*` naming rules) |
| `DATA-01`, `DATA-05` | **Schema pattern**, **cache-invalidation pattern** | **v2 memory rule** (`memory/`) | Neither is deterministically checkable — *"schema follows the stated pattern"* and *"cache invalidation follows the stated pattern"* are judgement calls, and v2 **rejects LLM-evaluated sensors at parse time**, so they cannot be sensors even in principle. They are behavioural constraints the build agent reads |
| `DATA-04` | **Tenant scoping** (every query scoped to `tenant_id`) | **⚠️ one small overlap to call** — routes to the existing conditional **`tenant-isolation-check`** rather than `pdlc-migration-safety` | `DATA-04` is a *tenant-isolation* concern, not a *migration* concern; a `tenant-isolation-check.json` hook already exists (conditional on `multi-tenancy.md`). `DATA-04` belongs with **that** check, not with the migration sensor — the one `DATA-*` rule that lands on a *third* surface |

**The boundary this closes (F-C16).** `migration-safety` was double-classified: its `DATA-*` rule family was routed to a sensor (A26 data-classification) while the hook was marked never-remove (A31). The classification is settled by **which concern each rule serves**: `pdlc-migration-safety` owns exactly the **migration** concern (`DATA-BASELINE-01/02` + `DATA-02/03`); `pdlc-data-classification` (A26, `SEC-13/14` field-level classification) owns **classification** — a *different* rule family entirely. The `DATA-*` rules that belong to neither (`DATA-01` schema, `DATA-05` cache, `DATA-06` naming) route to memory rules or v2's linter, and `DATA-04` tenant-scoping routes to the tenant-isolation check. No rule is orphaned and none is double-owned.

**Non-`aidlc` methods.** The `migration-safety.json` hook (below) is **retained** under `spec-driven-kiro` / `spec-driven-speckit` / `freestyle` / `manual` — v2's gate-fired sensor mechanism exists only under `aidlc`, so the four migration rules fall back to the hook there (the same 🔴 never-remove check, re-expressed onto a hook surface, `common/non-aidlc-blocking-hooks.md`). Moving the check between mechanisms per build method is adaptation, never removal (INV-L2-022) — the migration-safety capability is preserved under every build method.

## Hook: `migration-safety.json`

- **Event:** fileEdited (Tier A 🔴)
- **Pattern:** Migration files (derived from tech-stack — e.g., `Migrations/*.cs`, `src/migrations/*.ts`)
- **Checks:** DATA-BASELINE-01/02, DATA-02/03
- **Build-method note:** Retained under the non-`aidlc` methods; under `aidlc` these same four rules become the `pdlc-migration-safety` gate-fired sensor (see Build-Method Routing above).

## Tier: 1 (baseline) / 2 (full steering-derived set)
