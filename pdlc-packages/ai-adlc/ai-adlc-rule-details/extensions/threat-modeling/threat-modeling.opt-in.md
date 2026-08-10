<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Opt-In: Threat Modeling (Deep)

## When This Extension Applies

Your system needs the deep threat-modeling extension (beyond the always-run Stage 8 STRIDE baseline) if:

- It is a high-security or regulated system where a light STRIDE checklist is not enough
- It handles highly sensitive assets, spans complex trust boundaries, or is an attractive attacker target
- Compliance requires a documented threat model with explicit risk ratings and mitigations
- You need attack trees, DREAD / OWASP Risk Rating scoring, and per-data-flow analysis

> **This extension layers on top of the baseline.** Stage 8 (`decisions/security-identity.md`, Step 6a) already runs a depth-scaled STRIDE pass for **every** project. Opt in here only when the system warrants heavier rigor.

## Opt-In Question

```
### Would you like to run a DEEP threat-modeling pass?

The always-run Stage 8 security stage already performs a STRIDE pass scaled to your
project depth. This extension adds heavyweight rigor on top for high-security systems:

- A full trust-boundary Data Flow Diagram (elements, flows, trust zones)
- STRIDE enumerated per element AND per data-flow crossing
- Attack trees for the highest-value threats (decomposed attack paths)
- Risk rating per threat (DREAD or OWASP Risk Rating) and residual-risk tracking
- Mitigation mapping handed to AI-GCE (compliance controls) and AI-TGE (security tests)

(a) Yes -- run the deep threat-modeling pass (high-security / regulated systems)
(b) No  -- the Stage 8 STRIDE baseline is sufficient for this system

Recommended for: systems handling regulated/sensitive data, high attacker value,
strict compliance, or multiple trust boundaries
Skip if: low-sensitivity system where the baseline STRIDE checklist covers the risk
```

If yes → load `threat-modeling.md`

## Relationship to Other Stages & Extensions

Threat Modeling (Deep) is a **security-analysis** extension at **Stage 8 (Security & Identity)**. It does not replace the baseline — it deepens it. Its output feeds:

- **ADRs** — major security decisions with long-term impact
- **AI-GCE** — mitigations become security-compliance rules/hooks in the generated workspace
- **AI-TGE** — threats and mitigations become derived security tests
- **AI-DWG** — informs the generated `security-rules.md` steering

Same **Security Architect** sub-role as the Stage 8 baseline. If not opted in, the Stage 8 baseline STRIDE pass still runs — this extension is never required for a valid security architecture.

## Status: ✅ Available (v1.1)
