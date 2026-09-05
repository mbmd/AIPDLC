<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Security Compliance — Derivation Logic

## Purpose

Derives security compliance rules from `security-rules.md` and `observability-sensitive.md`. This is a HYBRID category: built-in baseline provides universal security floor; steering enriches with project-specific security decisions.

---

## MANDATORY: Stage Sub-Role — Security Architect

During THIS activity, ALSO adopt the mindset of a **Security Architect**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Apply defense-in-depth thinking: baseline security is the floor, steering enrichment adds project-specific layers
- Treat every security rule as Tier A (immediate enforcement) unless explicitly advisory — security violations in intermediate state ARE dangerous
- Think in attack surfaces: endpoints without auth, secrets in code, unmasked PII — each is an exploitable vector
- Assign severity based on blast radius: auth bypass (🔴) > PII exposure (🔴) > CORS misconfiguration (🟠) > naming (🟡)
- Ensure file patterns for security hooks cover ALL entry points, not just controllers

### Anti-Patterns for This Activity
- Do NOT generate security rules with weak language ("should secure") — security is always MUST/NEVER
- Do NOT defer security hooks to agentStop — secrets in code are dangerous at every intermediate state
- Do NOT assume security-rules.md covers everything — built-in baseline applies regardless of steering content

### Quality Check
A good output from this activity sounds like:
- "SEC-BASELINE-01: No hardcoded secrets. Pattern: `**/*.ts`, `**/*.json`, `**/*.yaml`. Event: fileEdited (Tier A). sessionDedup: true. This fires immediately because a committed secret is exploitable from the moment it exists."
- "security-rules.md specifies RS256 → SEC-01 generated. HS256 in any JWT config is a Critical violation."

---

## Source Steering Files

| File | What to Extract |
|------|----------------|
| `security-rules.md` | Auth model, token strategy, RBAC, encryption, OWASP mitigations, audit logging |
| `observability-sensitive.md` | PII categories, masking rules, what NEVER to log, data classification |

## Built-in Baseline (Always Generated)

These rules exist regardless of steering content:

| Rule ID | Statement | Source |
|---------|-----------|--------|
| SEC-BASELINE-01 | No hardcoded secrets in source code (API keys, passwords, tokens, connection strings) | Built-in: Universal security |
| SEC-BASELINE-02 | Every API endpoint MUST have explicit auth declaration (`[Authorize]` or `[AllowAnonymous]`) | Built-in: No accidental exposure |
| SEC-BASELINE-03 | Credentials MUST be in environment variables or secret manager — never in committed files | Built-in: Secret management |

---

## Steering-Enriched Rules

### From `security-rules.md` → Auth Model Section

| Steering Content | Generated Rule |
|-----------------|---------------|
| "JWT Bearer tokens with RS256 signing" | SEC-01: All auth tokens MUST use RS256 signing (no HS256 in production) |
| "Role-based access: Admin, Manager, User" | SEC-02: Every endpoint MUST declare minimum required role |
| "Token expiry: 15 minutes access, 7 days refresh" | SEC-03: Access token TTL MUST NOT exceed 15 minutes |

### From `security-rules.md` → OWASP Section

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Input validation on all API endpoints" | SEC-10: All request DTOs MUST have validation rules |
| "SQL injection prevention: parameterized queries only" | SEC-11: NEVER use string concatenation for queries |
| "CORS: explicit origin whitelist" | SEC-12: CORS must list explicit origins (no wildcard `*` in production) |

> ⚠️ **`SEC-10/11/12` are produced but assigned to no hook.** `security-gate-check.json`'s prompt substantively checks input validation and query string-concatenation, but it does not **cite** these IDs, so those checks emit no attributable compliance event, and CORS (`SEC-12`) is checked by nothing. All three are deterministic and belong on a gate-fired sensor surface that does not exist yet. They are left produced-but-unassigned deliberately — assigning them to `security-gate-check` here would record enforcement that has not been designed.

### From `security-rules.md` → Data-Classification Section

Derived rules — they read the project's restricted-data patterns from steering, exactly like the rest of the `SEC-*` family. **If the steering names no restricted-data categories, emit NO rules** (the standing "no steering = no rule" principle); never hardcode a pattern list.

| Steering Content | Generated Rule |
|-----------------|---------------|
| "Personal / restricted data fields must be classified" | SEC-13: Every entity or model field holding personal or otherwise restricted data MUST carry an explicit sensitivity annotation. A field is never implicitly non-sensitive — an unannotated field holding restricted data is a violation, not a default. |
| "Restricted data encrypted at rest" | SEC-14: Every field annotated as restricted MUST also declare its at-rest protection — the encryption mechanism, or an explicit recorded exemption naming the compensating control. A restricted field with no at-rest declaration is a violation. |

> **`SEC-13`/`SEC-14` are fail-closed and they chain.** **Fail-closed:** each is phrased so that *absence is a violation, not a pass* — the check reports on an unannotated field rather than skipping it, which is the property that stops it returning a clean result on a completely unclassified schema (the same defect class as AI-TGE's silent degradation). **They chain:** `SEC-14` iterates over the fields `SEC-13` annotated, so `SEC-13` is authored first and `SEC-14` has nothing to evaluate without it. **`SEC-14` permits a recorded exemption via the existing `GOV-LOG-004` approval workflow** (encryption at rest has legitimate compensating-control exceptions); **`SEC-13` accepts no exemption** — a field either holds restricted data or it does not. Both are enforced by the **`pdlc-data-classification`** gate-fired sensor. Behaviour verified by TR-831.

### From `observability-sensitive.md`

| Steering Content | Generated Rule |
|-----------------|---------------|
| "NEVER log: passwords, tokens, credit card numbers, SSN" | SEC-20: Log sanitization MUST mask all PII categories |
| "Email addresses: mask middle portion" | SEC-21: Email masking format: `a***@domain.com` |
| "Financial amounts: OK to log; account numbers: NEVER" | SEC-22: Account numbers MUST be masked in all outputs |

---

## Tier Progression

| Tier | Security Rules Active |
|:----:|----------------------|
| 1 | SEC-BASELINE-01/02/03 + basic rules from security-rules.md (auth model, no secrets) |
| 2 | + Full SEC-* set from steering (OWASP, encryption, PII masking) |
| 3 | + SOX internal controls (if applicable), GDPR data rules (if applicable), full audit trail |

### Tier 3 Enrichment (SOX/GDPR — Conditional)

If `project-governance.md` or `scope-and-risks.md` mentions SOX, GDPR, PCI-DSS, or similar:
- Generate additional rules: SOX-01 through SOX-06, GDPR-01 through GDPR-06
- These are Tier 3 — only activated at pre-release
- Source: derived from security-rules.md compliance section + built-in framework knowledge

---

## Hook Mapping

| Hook | Event | Debounce | Rules Enforced |
|------|-------|:--------:|----------------|
| `security-gate-check.json` | fileEdited | Tier A 🔴 | `SEC-01`, `SEC-02`, `SEC-03`, `SEC-BASELINE-02` |
| `sensitive-data-check.json` | fileEdited | Tier A 🔴 | `SEC-BASELINE-01`, `SEC-20/21/22` |

Both hooks are 🔴 Essential — NEVER remove.

> **This mapping is the authoritative one for `security-gate-check`.** Three files disagreed on its rule set: the hook inventory said `SEC-001/003/010` (all mis-padded, and `SEC-010` was really `SEC-10`), and `knowledge-map-guide.md` said `SEC-01/03/10`. This generator **produces** these rules, so it wins — the set is `SEC-01/02/03 + SEC-BASELINE-02`. The other two files are corrected to match (`SEC-001/003/010` was fixed in `hooks-from-steering.md` at merged item 2 file 1; `knowledge-map-guide.md` is corrected below). `SEC-10` is **not** enforced by this hook — it is one of the produced-but-unassigned trio noted above.

---

## File Pattern Derivation

Security hooks watch presentation/controller files (where endpoints are defined):

| Technology | Pattern for security-gate-check |
|-----------|--------------------------------|
| NestJS | `src/modules/*/presentation/**/*.controller.ts` |
| Django | `**/views.py`, `**/viewsets.py` |
| ASP.NET | `src/Modules/*/Presentation/**/*Controller.cs` |
| Spring Boot | `src/main/java/**/controller/*Controller.java` |

Sensitive-data-check watches ALL code files:

| Technology | Pattern for sensitive-data-check |
|-----------|--------------------------------|
| NestJS | `**/*.ts`, `**/*.json`, `**/*.yaml` |
| Django | `**/*.py`, `**/*.json`, `**/*.yaml` |
| ASP.NET | `**/*.cs`, `**/*.json`, `**/*.yaml` |
| Spring Boot | `**/*.java`, `**/*.json`, `**/*.yaml`, `**/*.properties` |
