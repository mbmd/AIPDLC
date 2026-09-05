# Interaction Between AI-GCE Governance and AI-DLC Sensors

**Purpose:** Compares the AI-Driven Governance & Compliance Engine (AI-GCE) with **AI-DLC** (AI-Driven Development Life Cycle — Amazon's open-source build lifecycle) **v2's sensor system** — what each one is, what each can and cannot do, where they overlap, and how they run together in a PDLC-generated AI-DLC workspace. The short answer: they are **complementary layers, not competitors**, and a workspace that uses AI-DLC benefits from both at once.

> **Read this if** you are building with AI-DLC v2 and want to understand why AI-GCE still runs alongside it, what AI-GCE's rules turn into inside an AI-DLC workspace, and which governance concerns AI-DLC's own sensors do not cover.
>
> This is the *comparison* companion to [`INTERACTION_BETWEEN_THE_PDLC_CHAIN_AND_AIDLC.md`](INTERACTION_BETWEEN_THE_PDLC_CHAIN_AND_AIDLC.md), which explains the broader chain→AI-DLC handoff. Start there for the overall picture; use this one for the AI-GCE-vs-sensors detail.

---

## The Two Things Being Compared

| | AI-GCE | AI-DLC v2 sensors |
|---|--------|-------------------|
| **What it is** | A full governance **engine** — it reads your workspace and derives an entire compliance layer (rules, checks, an audit log, a compliance score, and process agents) | A single **check mechanism** — one sensor manifest describes one deterministic check that runs when an AI-DLC stage writes a file |
| **Scope** | The whole project lifecycle, from day one through production | Per-stage output — a sensor fires when a stage produces a file |
| **How its checks come to exist** | **Derived automatically** from your architecture and steering — you don't hand-write them | Each sensor is authored or scaffolded individually; there is no automatic derivation from your design |
| **What it produces** | Rules + checks + an audit trail + a rolling compliance score + a dashboard + governance agents | One audit row and one detail record per fire |
| **How aware it is of your project** | Deeply — it reads your technology stack, module structure, and phase, and tailors checks accordingly | Generically — the check logic lives in the sensor's script; the manifest itself is just metadata |

A useful mental image: **AI-GCE is the orchestra conductor; sensors are individual instruments.** AI-GCE arranges a whole governance layer; each sensor plays one precise, single-purpose note. They operate at different scales and solve different problems.

---

## Do They Stop the Build? — The Enforcement Model, Stated Carefully

This is the single most misunderstood part of the comparison, so it is worth being exact.

### AI-GCE: registers findings by default; does not stop your work

**AI-GCE's normal behaviour is to detect a problem and record a finding — it does not halt the build.** When a check fails, AI-GCE writes a timestamped compliance event (`pass` / `fail` / `warn`) and surfaces it to you; the write still lands and work proceeds, and you correct it on the next turn. When everything passes, AI-GCE is silent. This is true for **every** AI-GCE concern — architecture, naming, API contracts, module boundaries, data governance, domain context, logging, session discipline, role isolation, and phase gates.

There is **exactly one** exception: a **pre-write blocking check for secrets and PII only**. Because a secret written to disk can be committed, pushed, and mirrored irreversibly before any later check could react, this one check can refuse the write before it lands. It is **opt-in** — the default secrets check is advisory like everything else, and the blocking variant is produced only when (1) you have set the enforcement strength for secrets/PII to *block* **and** (2) your platform supports a pre-write blocking hook. Even when it blocks, it still records the finding. Everything else AI-GCE does is register-and-report.

### AI-DLC sensors: report on write; can block only at an approval gate

An AI-DLC sensor has two ways of firing:

- **Write-fired** (the common case): the sensor runs when a stage writes a file and **reports** a pass/fail result inline in AI-DLC's flow. It does not stop the write.
- **Gate-fired**: the sensor is bound to an AI-DLC **approval gate**, and the gate opens only if the sensor passes. This *can* block — but at the granularity of a **phase transition**, not an individual file write.

### The honest bottom line on "who can stop what"

- Neither system freely halts your work; both are built around *report-and-correct*, which is the right default for an AI-assisted build.
- The **only** thing that stops a *single file write before it lands* is AI-GCE's opt-in secrets/PII hook — and only on a platform that supports it.
- The **only** thing that blocks a *phase transition* is an AI-DLC gate-fired sensor.
- These are different granularities guarding different risks. They do not overlap, and neither makes the other redundant.

---

## What Maps Where — AI-GCE's Rules Inside an AI-DLC Workspace

When AI-DWG generates an AI-DLC workspace, AI-GCE's governance does not disappear — it is expressed through whichever mechanism fits each rule. Roughly:

- **About one third** of AI-GCE's rules become **AI-DLC sensor manifests** — the deterministic, file-content checks.
- **About half** become **behavioural rules** in AI-DLC's own `memory/` files — the constraints an AI-DLC agent reads before it works.
- **About one fifth** have **no AI-DLC equivalent at all** and remain AI-GCE-exclusive value running alongside.

### Rules that become AI-DLC sensors (deterministic, file-content checks)

| AI-GCE rule area | Becomes an AI-DLC sensor because… |
|------------------|-----------------------------------|
| Security patterns (e.g. no hardcoded secrets, auth present) | These are pattern-matchable in file content |
| Architecture conformance (import direction, forbidden dependencies) | Layer and dependency rules can be checked deterministically |
| Naming conventions | File/class/method naming is a regex check |
| Test-coverage threshold | Coverage above a threshold is a numeric check *(owned by AI-TGE, not AI-GCE)* |
| API-contract compliance | Endpoint naming and response-envelope structure are checkable |

### Rules that become AI-DLC behavioural rules (not sensors)

| AI-GCE rule area | Why a sensor can't express it | Where it lands in AI-DLC |
|------------------|-------------------------------|--------------------------|
| Session discipline (e.g. spec before code) | It's about the *order* of actions, not the content of one file | A written rule the agent reads |
| Role isolation (e.g. architect doesn't write code) | It's a cross-concern behaviour, not a file check | A written rule the agent reads |
| Phase gates | It governs lifecycle transitions, not file content | Phase-scoped rules |
| Team topology / module ownership | It's organizational, not code-level | A team-level written rule |

### AI-GCE capabilities with no AI-DLC equivalent (they remain AI-GCE-only)

- **A rolling compliance score** and dashboard (an aggregated view over time — sensors only pass/fail per fire).
- **Progressive enforcement tiers** that ratchet up as the project matures (day-one light, tightening over sprints).
- **Periodic full-workspace audits** (sensors only check the file being written right now).
- **Human-triggered process agents** for governance moments (sensors are fully automated).
- **Brownfield baselining** that grandfathers existing issues and enforces only new code.

---

## What Each Does That the Other Cannot

### What AI-GCE offers that sensors do not

| Capability | Why sensors can't provide it |
|-----------|------------------------------|
| **Automatic derivation** — checks generated from your architecture and steering | Each sensor is authored individually; there is no derive-from-design step |
| **Breadth** — 15+ governance categories (security, architecture, API, naming, testing, CI/CD, session, roles, data, team topology, boundaries, scoring, phase gates, audit, observability) | Sensors are a small set of deterministic file-content check types |
| **A rolling compliance score + dashboard** | Sensors have no aggregation layer — each fire is a standalone pass/fail |
| **Progressive tiers** — enforcement tightens over time | Sensors are binary on/off per stage import |
| **Full-workspace periodic audits** | Sensors only check files being written now |
| **Pre-write blocking for the one irreversible case** (secrets/PII, opt-in) | Sensors fire after the write, or at a gate — neither intercepts a single write before it lands |
| **Human process agents** at governance milestones | Sensors are fully automated with no human-trigger concept |
| **Brownfield baselining** | Sensors treat every file equally, with no legacy-vs-new distinction |

### What sensors offer that AI-GCE does not

| Capability | Why AI-GCE doesn't provide it |
|-----------|-------------------------------|
| **Learning-loop integration** — a correction at a gate can become a new sensor automatically | AI-GCE re-derives from steering; it doesn't turn a single correction into a permanent new check on its own |
| **Per-stage binding** — fine-grained control over which check fires on which AI-DLC stage | AI-GCE checks fire by file pattern or event, not by AI-DLC workflow stage |
| **Start-up validation** — an unknown sensor id makes the workflow fail to start | An AI-GCE hook can fail silently if misconfigured |
| **Upgrade-safety** — project-tier sensors survive AI-DLC framework upgrades automatically | AI-GCE re-derivation can overwrite non-custom content |
| **Native inline feedback** — sensor results appear directly in AI-DLC's own flow and audit trail | AI-GCE runs as a companion layer beside AI-DLC, not inside its stage output |

---

## Verdict: Complementary Layers That Coexist

In a PDLC-generated AI-DLC workspace, AI-GCE and AI-DLC sensors run **in parallel, without conflict**:

- They read from the **same canonical rules** that AI-DWG writes once — neither is a copy of the other, and the same constraint is never duplicated across surfaces.
- They **own separate outputs**: AI-GCE keeps its own compliance records; sensors write into AI-DLC's audit trail.
- They cover **different ground**: sensors give fast, automated, inline feedback on deterministic file checks *within* AI-DLC's workflow; AI-GCE provides the broader governance — scoring, tiers, periodic audits, process agents, and the one pre-write secrets guard — *around* it.

Neither replaces the other. A team using AI-DLC gets the best result from **both**: sensors for immediate in-flow checks, and AI-GCE for the lifecycle-wide governance that sensors were never designed to do.

---

## Two Axes That Decide What Enforcement You Get

One practical note that prevents a common mix-up: what enforcement mechanisms are available in a given workspace depends on **two independent things**, not one.

| Axis | Set by | Decides |
|------|--------|---------|
| **Harness** — the IDE/agent shell you run in (e.g. Kiro, Claude Code, Cursor, generic) | `platformTargets` in the workspace manifest | Whether **hooks** are available, and in what format |
| **Build method** — how the work is structured | `buildProfile` in the workspace manifest | Whether **AI-DLC sensors** are available (they exist when `buildProfile: aidlc`) |

Sensors are available whenever the build method is AI-DLC, on any harness. Hooks are available whenever the harness supports them, regardless of build method. So a workspace on a hook-capable harness *and* using AI-DLC gets **both** hooks and sensors; a workspace on a harness with no hook support but using AI-DLC still gets sensors (they are portable), and so on. The two axes are orthogonal — read them separately.

---

## Related Documents

| Document | What it adds |
|----------|--------------|
| [`INTERACTION_BETWEEN_THE_PDLC_CHAIN_AND_AIDLC.md`](INTERACTION_BETWEEN_THE_PDLC_CHAIN_AND_AIDLC.md) | The broader picture — how the whole PDLC chain feeds AI-DLC, where AI-DWG sources each piece, and how AI-GCE and AI-TGE run alongside AI-DLC |
| [`HOW_AIDLC_V2_SUPPORT_WORKS.md`](HOW_AIDLC_V2_SUPPORT_WORKS.md) | The mechanics of the AI-DLC v2 build method — the `aidlc/` tree, sensor manifests, and the `buildProfile` switch |
| [`HOW_GCE_DERIVATION_PIPELINE_WORKS.md`](HOW_GCE_DERIVATION_PIPELINE_WORKS.md) | How AI-GCE derives its rules, hooks, and agents from workspace steering |
| [`HOW_GCE_COMPLIANCE_AUDIT_WORKS.md`](HOW_GCE_COMPLIANCE_AUDIT_WORKS.md) | How AI-GCE runs audits, scores compliance, and tracks violations |
| [`HOW_HOOK_GENERATION_WORKS.md`](HOW_HOOK_GENERATION_WORKS.md) | How AI-GCE turns rules into hooks, including the debounce classes |
| [`HOW_TIERED_GOVERNANCE_WORKS.md`](HOW_TIERED_GOVERNANCE_WORKS.md) | The progressive-tier model that is AI-GCE-exclusive |
| [`HOW_TGE_TEST_GOVERNANCE_WORKS.md`](HOW_TGE_TEST_GOVERNANCE_WORKS.md) | How AI-TGE governs test coverage, including the test-coverage sensor |

---

*Knowledge Document | Interaction | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
