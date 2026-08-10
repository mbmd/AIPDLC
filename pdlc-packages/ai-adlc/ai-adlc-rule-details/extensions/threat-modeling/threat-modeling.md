<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Threat Modeling (Deep)

**Extension ID:** threat-modeling
**Version:** 1.1.0
**Rule Prefix:** THM
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 8 (Security & Identity Architecture)

Threat Modeling (Deep) is a **security-analysis extension** that layers heavyweight rigor on top of the **always-run Stage 8 STRIDE baseline** (`decisions/security-identity.md`, Step 6a). The baseline runs a depth-scaled STRIDE pass for every project; this extension adds a full trust-boundary DFD, per-element and per-flow STRIDE, attack trees, and formal risk rating for high-security systems. Its output **feeds** ADRs, AI-GCE (compliance controls), and AI-TGE (security tests) — it does not replace the baseline.

When this extension is NOT opted in, the Stage 8 baseline STRIDE pass still runs. This extension is never required for a valid security architecture — it is for systems whose risk warrants the extra depth.

---

## MANDATORY: Extension Sub-Role — Security Architect (Adversarial Depth)

When this extension is active, deepen the **Security Architect** sub-role already active at Stage 8 into an **adversarial** stance. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS an attacker's-eye dimension for the duration of deep threat-modeling.

### Behavioral Shifts
- Think like the attacker — start from the asset and reason backward: what is the shortest path to compromise it?
- Trust nothing implicitly — every data flow that crosses a trust boundary is a candidate attack surface
- Prefer decomposition over intuition — draw the DFD and enumerate; do not rely on "we've covered the obvious ones"
- Quantify, then prioritize — rate every threat so mitigation effort goes where residual risk is highest

### Anti-Patterns for This Extension
- Do NOT enumerate threats you have no intention of rating or mitigating — a threat with no disposition is theater
- Do NOT stop at STRIDE categories without tracing concrete attack paths for the high-value assets
- Do NOT treat the threat model as one-and-done — it is invalidated whenever the trust boundaries change
- Do NOT let compliance checkboxes substitute for genuine adversarial analysis

### Quality Check
A good output with this extension sounds like:
- "Trust-boundary DFD with 4 zones and 11 crossing flows; STRIDE per element + per flow → 34 threats; attack trees for the 3 highest-value assets; each threat DREAD-rated; 6 high/critical threats with mitigations mapped to GCE controls + TGE tests; 2 residual risks formally accepted with rationale; 3 ADRs..."

---

## Rules

### Rule THM-01: Trust-Boundary Data Flow Diagram

**Statement:** Decompose the system into a Data Flow Diagram — external entities, processes, data stores, data flows — and draw the **trust boundaries** (zones where the level of trust changes). The DFD is the foundation; every subsequent rule references it.

**Verification:**
- [ ] The DFD identifies external entities, processes, data stores, and data flows
- [ ] Trust boundaries are drawn where trust changes (internet↔app, app↔data, tenant↔platform, etc.)
- [ ] Elements are traceable to the containers/components from Stage 5
- [ ] Every data flow that crosses a trust boundary is marked

**Anti-Pattern:** Enumerating threats against a vague mental model with no explicit DFD or trust boundaries.

**ADR Trigger:** No

---

### Rule THM-02: STRIDE Per Element

**Statement:** Apply STRIDE (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) to **each element** of the DFD, using the element-type applicability (e.g., data stores → Tampering/Information disclosure/Repudiation; processes → all six).

**Verification:**
- [ ] Each DFD element has been walked through the applicable STRIDE categories
- [ ] Threats are specific to the element (not generic restatements of the category)
- [ ] Element-type applicability is respected (not every category applies to every element type)
- [ ] Identified threats are recorded in the threat register with a unique ID

**Anti-Pattern:** Listing the six STRIDE words once for the whole system instead of applying them per element.

**ADR Trigger:** No

---

### Rule THM-03: Attack Trees for High-Value Threats

**Statement:** For the highest-value assets/threats, build **attack trees** — decompose the attacker's goal into the sub-goals and steps that achieve it — to reveal the cheapest/most-likely attack paths and the best interdiction points.

**Verification:**
- [ ] Attack trees exist for the highest-value assets (crown jewels)
- [ ] Each tree's root is an attacker goal; children are AND/OR-decomposed sub-goals
- [ ] Leaf nodes are concrete, assessable attack steps
- [ ] The cheapest/most-likely path is identified and used to prioritize mitigation

**Anti-Pattern:** Building attack trees for trivial threats while leaving the crown-jewel assets analyzed only at STRIDE-category level.

**ADR Trigger:** No

---

### Rule THM-04: Per-Flow Analysis Across Trust Boundaries

**Statement:** Every data flow that crosses a trust boundary (THM-01) must be analyzed for the threats introduced by the crossing — authentication of both ends, integrity/confidentiality in transit, and validation at the receiving side.

**Verification:**
- [ ] Each boundary-crossing flow has an authentication mechanism for both ends
- [ ] In-transit integrity and confidentiality are specified per flow
- [ ] Input validation / output encoding at the receiving side is specified
- [ ] Flows lacking a control are flagged as threats with a disposition (THM-06)

**Anti-Pattern:** Securing the perimeter but leaving internal trust-boundary crossings (service-to-service, app-to-data) implicitly trusted.

**ADR Trigger:** No

---

### Rule THM-05: Risk Rating (DREAD or OWASP Risk Rating)

**Statement:** Every identified threat is rated with a consistent method — **DREAD** or the **OWASP Risk Rating** (likelihood × impact) — to produce a comparable residual-risk score that drives prioritization.

**Verification:**
- [ ] A single rating method is chosen and applied consistently to all threats
- [ ] Each threat has a score with the factors shown (not just a bare number)
- [ ] Threats are ranked; high/critical threats are clearly separated from low
- [ ] Residual risk (after planned mitigation) is distinguished from inherent risk

**Anti-Pattern:** Rating threats by gut feel or inconsistently, so the priority order cannot be defended.

**ADR Trigger:** No

---

### Rule THM-06: Mitigation or Accepted-Risk per Threat

**Statement:** Every identified threat must have a disposition — a **mitigation** (control), a **transfer**, or an **explicitly accepted risk** with a documented rationale and owner. No threat is left undispositioned.

**Verification:**
- [ ] Every threat has a disposition (mitigate / transfer / accept)
- [ ] Mitigations name a concrete control (not "add security")
- [ ] Accepted risks have a rationale, an owner, and (where relevant) a review date
- [ ] High/critical threats are not silently accepted — acceptance at that level is escalated

**Anti-Pattern:** A long threat list with mitigations only for the easy ones, leaving the hard/high threats undispositioned.

**ADR Trigger:** No — escalated to THM-07 when the mitigation choice has long-term impact.

---

### Rule THM-07: Major Security Decisions → ADR

**Statement:** Any mitigation or accepted-risk decision that involves 2+ viable options with long-term architectural impact must be recorded as an ADR.

**Verification:**
- [ ] Significant security decisions have an ADR (context, options, decision, consequences)
- [ ] Accepted high/critical risks are recorded as ADRs (not just log entries)
- [ ] The ADR is listed in the state ADR register
- [ ] The ADR references the threat ID(s) and risk rating it addresses

**Anti-Pattern:** Making a structural security trade-off (e.g., accepting a DoS exposure for cost reasons) with no recorded rationale.

**ADR Trigger:** Yes — this rule *is* the ADR trigger for deep threat-modeling decisions.

---

### Rule THM-08: Map Mitigations to Downstream Controls (AI-GCE + AI-TGE)

**Statement:** Each mitigation must be mapped to the downstream artifact that will enforce or verify it — a compliance control/hook for **AI-GCE**, and/or a security test for **AI-TGE** — so the threat model drives the built guardrails, not just the design doc.

**Verification:**
- [ ] Each mitigation names its enforcement home (GCE rule/hook) and/or verification home (TGE security test)
- [ ] Mitigations requiring runtime enforcement are flagged for AI-GCE
- [ ] Mitigations requiring test coverage are flagged for AI-TGE
- [ ] Mitigations with no downstream home are re-examined (is it actually enforceable?)

**Anti-Pattern:** A mitigation list that never becomes a control or a test — security theater that the build cannot honor.

**ADR Trigger:** No

---

### Rule THM-09: Re-Run on Change

**Statement:** The threat model is invalidated whenever the containers, data flows, or trust boundaries change. Such a change must trigger a re-run of the affected portion of the model.

**Verification:**
- [ ] The threat model records the architecture version (containers/flows) it was built against
- [ ] A change to trust boundaries or boundary-crossing flows is flagged for re-modeling
- [ ] Re-runs update the register and re-rate affected threats
- [ ] The reconciliation pass (when a UXP/PBP or revised AP appears) includes a threat-model check

**Anti-Pattern:** Treating the threat model as a one-time deliverable that silently rots as the architecture evolves.

**ADR Trigger:** No

---

### Rule THM-10: Hand-Off Completeness

**Statement:** At stage completion, every threat must be routed to its downstream home; nothing is orphaned. The deep threat model exists to drive controls, tests, and ADRs.

**Verification:**
- [ ] Every high/critical threat has a tracked disposition (THM-06)
- [ ] Every mitigation maps to a GCE control and/or TGE test (THM-08)
- [ ] Every long-term security decision / accepted high-risk has an ADR (THM-07)
- [ ] The threat register (with ratings + dispositions) is included in the Security & Identity Architecture document and referenced from `adlc-state.md`

**Anti-Pattern:** A thorough threat model that never feeds the workspace guardrails or the test suite — a "dead artifact."

**ADR Trigger:** No

---

## Verification Checklist (Stage Completion)

Before completing Stage 8 with Threat Modeling (Deep) active, verify:

- [ ] Trust-boundary DFD built; boundary-crossing flows marked (THM-01)
- [ ] STRIDE applied per element (THM-02); attack trees for crown-jewel assets (THM-03)
- [ ] Per-flow analysis across every trust boundary (THM-04)
- [ ] Every threat risk-rated with a consistent method (THM-05)
- [ ] Every threat has a disposition; high/critical not silently accepted (THM-06)
- [ ] Major decisions / accepted high-risks recorded as ADRs (THM-07)
- [ ] Mitigations mapped to AI-GCE controls and/or AI-TGE tests (THM-08)
- [ ] Model records the architecture version it was built against (THM-09)
- [ ] Every threat routed downstream; register in the security doc + `adlc-state.md` (THM-10)

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| THM-07 | Any mitigation or accepted-risk decision with 2+ viable options and long-term architectural impact |
| THM-06 | (escalates to THM-07) A high/critical threat is deliberately accepted rather than mitigated |

---

## Templates

### Trust-Boundary DFD (tabular)

```
Trust zones: {Internet} | {Application} | {Data} | {Platform/Admin}

| Element | Type (entity/process/store/flow) | Zone | Crosses boundary? | Notes |
|---------|----------------------------------|------|:-----------------:|-------|
| {Browser} | external entity | Internet | — | untrusted |
| {API gateway} | process | Application | Internet → App | authN enforced here |
| {Primary DB} | data store | Data | App → Data | encryption at rest |
```

### Threat Register (STRIDE + rating + disposition)

```
| ID | Element / Flow | STRIDE | Threat | Rating (DREAD/OWASP) | Disposition (mitigate/transfer/accept) | Control → GCE | Test → TGE | ADR |
|----|----------------|--------|--------|:--------------------:|-----------------------------------------|---------------|-----------|-----|
| TM-01 | API gateway | Spoofing | forged token | H (8.4) | mitigate: OIDC + sig verify | authn-rule | token-forgery test | ADR-{NNN} |
| TM-02 | Primary DB | Info disclosure | PII over-exposure | H (7.9) | mitigate: column encryption + least-privilege | data-access-rule | rbac-scope test | — |
```

### Attack Tree (indented)

```
GOAL: Exfiltrate customer PII
├── OR: Compromise the database directly
│   ├── AND: Obtain DB credentials + reach the DB network
│   └── Exploit an unpatched DB CVE
└── OR: Abuse the application layer
    ├── SQL injection via {endpoint}
    └── Broken access control → query another tenant's data
```

### Tag → Artifact Hand-Off Map

```
| Threat-model element | Downstream home | Rule / artifact |
|----------------------|-----------------|-----------------|
| Mitigation (enforceable) | AI-GCE compliance rule/hook | THM-08 |
| Mitigation (verifiable) | AI-TGE security test | THM-08 |
| Major decision / accepted high-risk | ADR | THM-07 |
| Threat register | Security & Identity doc · adlc-state.md | THM-10 |
| Trust-boundary change | Re-run trigger (reconciliation) | THM-09 |
```
