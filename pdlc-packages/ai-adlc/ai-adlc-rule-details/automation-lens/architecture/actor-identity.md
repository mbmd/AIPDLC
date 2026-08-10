# Automation Architecture — Actor Identity & Authorization

> **Sub-module of** `automation-lens/facet.md`. Loaded on demand when designing the automation's identity and permissions.
> **Sub-role:** `#persona-subrole-security-architect`

---

## The premise

An automation is an actor in your system. It authenticates, it is authorized, it takes actions attributed to something. **Deciding what that something is, is a security-architecture decision** — not an implementation detail to be settled by whoever writes the deployment script.

The default failure mode: the automation runs with an over-privileged shared account, and nobody can tell whether an action was taken by the automation, a developer, or an attacker who found the credential.

---

## 1. Identity Model Selection

| Model | Mechanism | Use when | Risk |
|-------|-----------|----------|------|
| **Service account** | Dedicated non-human account with scoped permissions | Default for most automation | Credential must be stored and rotated |
| **Managed identity** | Platform-issued identity, no stored credential (cloud IAM roles, workload identity) | The automation runs on a platform that supports it | **Preferred** — no credential to leak |
| **API key** | Static key for an external system | Calling a third-party API that offers only keys | Static secret; rotation is manual and often skipped |
| **Delegated user (OBO)** | Acts on behalf of a specific human | The action must be legally/auditably attributed to a person | Complexity; token lifetime management |

### Choosing

1. **Does the platform offer a managed/workload identity?** → Use it. No stored credential is the strongest position.
2. **Must the action be attributed to a specific human** (regulatory, approval semantics, or the action is legally the user's)? → Delegated user.
3. **Calling an external system with only key-based auth?** → API key, vault-stored, with a documented rotation schedule.
4. **Otherwise** → dedicated service account.

**Design requirement:** name the identity explicitly in `requires.roles`. `roles: [ticket-router-service-account]` — not `roles: [system]`.

---

## 2. Least Privilege

**The rule:** the automation's permissions must be the minimum set required by its declared `provides.writes` and `requires.data`.

### Derivation

Build the permission set mechanically from the declarations:

| Declaration | Permission granted |
|-------------|-------------------|
| `requires.data: [ticket, agent]` | READ on ticket, agent |
| `provides.writes: [ticket.assignee]` | UPDATE on ticket.assignee **only** — not the whole ticket, if the platform supports field-level control |
| `requires.auth: [crm-api]` | The specific CRM scopes needed, not full access |
| `provides.emits: [ticket.assigned]` | PUBLISH on that topic only |

**Design requirements:**
- **No wildcard permissions.** `ticket:*` is not least privilege.
- **No inherited admin.** An automation must never run under an admin/root identity "for now."
- **Field-level scoping where available** — if the automation only sets `assignee`, it should not be able to change `status` or delete the record.
- **Separate identities for separate automations.** Sharing one account across five automations means the blast radius of any credential compromise is all five, and audit attribution is lost.
- **Document the permission set in the AP** — a table of identity → resource → operation.

---

## 3. Segregation of Duties (SoD)

**Mandatory for `controlled` control class** (SOX-style regulated processes); recommended wherever an approval step exists.

### The requirement

The identity that **initiates** an action must not be the identity that **approves** it. An automation that can both create a payment and approve it has defeated the control.

### Design patterns

| Pattern | How |
|---------|-----|
| **Split identities** | Automation A (initiator) and Automation B (approver) are distinct identities with non-overlapping permissions |
| **Human approval gate** | The automation initiates; a human identity approves (Attended mode) |
| **Dual control (four-eyes)** | Two distinct approvers required; the automation can be at most one of them |
| **Automation cannot approve** | The automation prepares and submits; approval permission is never granted to any automation identity |

**Design requirements:**
- For `controlled` class: **state explicitly which identity does what**, and prove no single identity holds both initiate and approve.
- The SoD boundary must be enforced by **permissions**, not by application logic. Logic can be bypassed; a missing permission cannot.
- `ATG__` (AI-GCE) will verify SoD in the implementation — the design must make the boundary checkable.

---

## 4. Credential Management

For any model that involves a stored secret (service account with password/key, API key):

| Concern | Requirement |
|---------|-------------|
| **Storage** | A secrets manager / vault. **Never** in code, config files, environment files committed to the repo, or CI variables in plain text. |
| **Rotation** | Define the interval and the mechanism. A rotation policy with no automated mechanism will not happen. |
| **Access** | Who/what can read the secret? Log every access. |
| **Scope** | One secret per automation per environment. Never share across environments. |
| **Revocation** | How fast can it be revoked if compromised? Document the procedure. |

**Design requirement:** if the chosen model requires a stored credential, the ADR must state the vault, the rotation interval, the rotation mechanism, and the revocation procedure. "We'll put it in the vault" is not a design.

---

## 5. Attribution & Non-Repudiation

Every automated action must be attributable in the audit trail (`audit-observability.md`).

**Design requirements:**
- The audit record names **the automation identity** and the `automationFeatureId` — not just "system."
- For delegated-user identities: record **both** the automation and the human on whose behalf it acted.
- The trigger is recorded — what caused this action (event id, schedule, human trigger).
- **An action must never be attributable to a human who did not perform it.** If an automation runs under a developer's personal account, the audit trail is falsified. This is a common and serious defect.

---

## 6. Authorization Checks at Runtime

Beyond identity permissions, the automation may need **business-level** authorization:

- Is this automation permitted to act on **this specific record**? (tenant isolation, data-boundary rules)
- Does the target entity's state permit this action? (don't assign a closed ticket)
- Is the automation currently enabled for this scope? (per-tenant activation)

**Design requirements:**
- **Multi-tenant automations must enforce tenant boundaries explicitly.** An automation with cross-tenant read access is a data-leak vector; scope every query.
- Authorization failures are **not retryable** (`reliability.md` §2) and must surface as business exceptions, not silent skips.

---

## 7. Identity Requirements by Control Class

| Control class | Identity requirements |
|---------------|----------------------|
| **Informational** | Read-only identity; least privilege on reads |
| **Operational** | Dedicated identity; least privilege; audit attribution; credential in vault |
| **Controlled** | All of the above + **SoD enforced by permissions** + dual-control on activation + rotation automated + access to the credential itself logged and reviewed |
| **Safety-critical** | All of the above + separate identity per environment with no production access from lower environments + break-glass procedure documented + periodic permission review with sign-off |

---

## 8. Handoff to Layer 3

AI-DWG provisions:
- The identity **placeholder** (never the actual credential — DWG generates config slots, not secrets)
- The vault reference / IAM role binding
- The permission manifest for review
- The `requires.auth` slots confirmed (DWG's provisioning-readiness check)

`ATG__` (AI-GCE) verifies in the implementation: least privilege honored, no wildcard grants, SoD intact for `controlled`+, no credentials in source, attribution correct in audit records.

---

## Anti-patterns

- **Shared "automation" account for everything** — no attribution, maximum blast radius.
- **Running under a developer's personal identity** — falsifies the audit trail; breaks when they leave.
- **Admin permissions "temporarily"** — it is never temporary.
- **Wildcard grants** — `resource:*` defeats the purpose of scoping.
- **Credential in an environment variable in the repo** — the most common leak path.
- **Automation that can both initiate and approve** — the control exists on paper only.
- **No rotation mechanism** — a rotation policy nobody can execute is not a control.
- **Cross-tenant read access in a multi-tenant automation** — one bug becomes a breach.

---

*Automation Architecture Sub-Module — Actor Identity & Authorization | v1.0.0*
