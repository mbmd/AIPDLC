<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Domain Storytelling

**Extension ID:** domain-storytelling
**Version:** 1.1.0
**Rule Prefix:** DST
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 4 (System Context) / Stage 5 (Container Design — decomposition)
- **Secondary Stages:** Stage 12 (Component Design)

Domain Storytelling is a **discovery technique**, not a design-pattern rule set. Domain experts narrate scenarios as pictographic sentences — **actor → activity → work object** — numbered in sequence and annotated with rules and pain points. It reveals actors, work objects, and boundaries *before* structural design, and it **feeds** the tactical extensions rather than replacing them:

- **DDD Tactical** (`ddd-tactical`) — work objects → candidate aggregates/entities (DDD-01); story clusters → Context Map (DDD-08); captured terms → ubiquitous language (DDD-11).
- **Security & Identity** (Stage 8) — actors → the role/identity model.

Domain Storytelling and **Event Storming** are alternative discovery lenses selected via the shared discovery-method selector (see `domain-storytelling.opt-in.md`). They can run together (narrative first, event flow second) or independently. If no tactical extension is active, a domain story still stands alone as a decomposition aid whose candidate contexts reconcile with the Stage 5 containers.

---

## MANDATORY: Extension Sub-Role — Domain Modeller (Domain Storytelling Facilitator)

When this extension is active, ALSO adopt the mindset of a **Domain Modeller facilitating a Domain Storytelling workshop**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension for the duration of Domain Storytelling rule enforcement. (This is the same **Domain Modeller** sub-role used by DDD Tactical and Event Storming, applied to narrative discovery.)

### Behavioral Shifts
- Follow one concrete scenario end-to-end — "show me exactly how this went the last time" — before generalizing
- Draw the sentence, don't abstract it — actor → activity → work object, in the domain's own words
- Keep it linear and numbered — the sequence IS the model; resist branching until the main flow is clear
- Separate as-is from to-be explicitly — never blur how it works today with how it should work

### Anti-Patterns for This Extension
- Do NOT jump to entities, tables, or aggregates before the story reads as a coherent narrative ("nouns first")
- Do NOT merge multiple scenarios into one tangled diagram — one story = one scope + one granularity
- Do NOT silently "fix" the process while capturing the as-is story — capture pain points as annotations instead
- Do NOT let the story become a deliverable in itself — its only value is what it feeds downstream

### Quality Check
A good output with this extension sounds like:
- "3 domain stories (2 as-is, 1 to-be) at coarse granularity; 7 actors → role model; 9 work objects → candidate aggregates handed to DDD Tactical; 2 story-cluster boundaries → candidate contexts reconciled with Stage 5 containers; ubiquitous-language glossary started; 4 pain-point annotations (1 → ADR)..."

---

## Rules

### Rule DST-01: Pictographic Grammar (Actor → Activity → Work Object)

**Statement:** Each sentence in a domain story follows the grammar **actor → activity → work object** (optionally → recipient actor). Actors are roles or systems; activities are verbs in the domain's language; work objects are the things acted upon.

**Verification:**
- [ ] Every sentence has an identified actor (a role or system, never a named individual)
- [ ] Activities are domain verbs (e.g., "submits", "approves"), not technical operations ("calls API")
- [ ] Work objects are named in the domain's language (e.g., "ticket", "invoice")
- [ ] Sentences read as natural narrative when spoken aloud

**Anti-Pattern:** Writing data-flow or system-call sentences ("Service A sends JSON to Service B") instead of a business narrative — modeling the solution, not the domain.

**ADR Trigger:** No — actors feed DST-06; work objects feed DST-07.

---

### Rule DST-02: Numbered Sequence

**Statement:** The sentences of a domain story are numbered in the order they happen. The sequence is the backbone of the model; the numbers make the flow unambiguous and referenceable.

**Verification:**
- [ ] Every sentence carries a sequence number
- [ ] Numbering reflects actual temporal/causal order
- [ ] Alternative or exception paths are shown as clearly-labeled branches (e.g., 3a/3b), not forced into the main line
- [ ] The story has a clear start and end point

**Anti-Pattern:** An unnumbered cloud of sentences from which no flow can be read.

**ADR Trigger:** No

---

### Rule DST-03: Scope and Granularity Declared

**Statement:** Every domain story declares its **scope** (which slice of the domain it covers) and its **granularity** (coarse-grained overview vs. fine-grained detail). One story holds one scope at one granularity.

**Verification:**
- [ ] Scope is stated (what the story does and does NOT cover)
- [ ] Granularity is labeled (coarse / fine)
- [ ] The story does not mix a high-level overview with deep detail in the same diagram
- [ ] Multiple related stories are listed with their scope/granularity so the set is navigable

**Anti-Pattern:** A single sprawling story that tries to cover the whole domain at every level of detail at once.

**ADR Trigger:** No

---

### Rule DST-04: As-Is vs. To-Be Labeled

**Statement:** Each story is explicitly labeled as **as-is** (how the domain works today) or **to-be** (how it should work). The two are never blurred within one story.

**Verification:**
- [ ] Every story is tagged as-is or to-be
- [ ] As-is stories capture reality including its pain, not an idealized version
- [ ] To-be stories reference the as-is they evolve from (where one exists)
- [ ] Changes between as-is and to-be are traceable (what the to-be adds/removes)

**Anti-Pattern:** Quietly modeling the desired process as if it were the current one, hiding the change the project actually requires.

**ADR Trigger:** No

---

### Rule DST-05: Rules and Pain Points Captured as Annotations

**Statement:** Business rules, constraints, and pain points surfaced while telling the story are captured as **annotations** on the relevant sentence — not resolved on the spot and not omitted.

**Verification:**
- [ ] Business rules governing an activity are annotated at that sentence
- [ ] Pain points / bottlenecks are marked (they motivate to-be stories and hotspot-style follow-ups)
- [ ] Assumptions are recorded rather than silently baked in
- [ ] Each annotation has a type (rule / pain / assumption / question)

**Anti-Pattern:** Debating a rule to a premature conclusion mid-workshop, or losing it entirely, instead of annotating and moving on.

**ADR Trigger:** Yes — when a captured rule or pain point resolves into a decision between 2+ viable architectural options with long-term impact.

---

### Rule DST-06: Actors → Role Model

**Statement:** The distinct actors across all stories are consolidated into a candidate **role model** — the seed of the authorization and identity design.

**Verification:**
- [ ] All actors are consolidated into a de-duplicated role list
- [ ] Human roles are distinguished from system actors
- [ ] Each role's activities (what it does across the stories) are noted
- [ ] The role list is reconciled with the Security & Identity role model (Stage 8) and, where present, AI-UXD personas

**Anti-Pattern:** Capturing actors in each story but never consolidating them, so the role/permission model has no basis.

**ADR Trigger:** No — actors reconcile with the Stage 8 role model.

---

### Rule DST-07: Work Objects → Candidate Entities/Aggregates

**Statement:** The work objects across the stories are collected as **candidate entities/aggregates**. Domain Storytelling *identifies* them; their boundary and invariant design is owned by DDD Tactical.

**Verification:**
- [ ] Work objects are consolidated into a candidate entity/aggregate list, named in the ubiquitous language
- [ ] Work objects that always change together are noted as aggregate candidates
- [ ] Candidates are handed to DDD-01 for boundary/invariant design — this rule does NOT finalize internals
- [ ] Work objects that cross story-cluster boundaries are flagged (candidates for shared kernel / integration)

**Anti-Pattern:** Finalizing entity attributes, relationships, or persistence during storytelling — pre-empting DDD Tactical and the data-architecture stage.

**ADR Trigger:** No — aggregate-boundary ADRs are raised under DDD-01 when a boundary is contested.

---

### Rule DST-08: Story-Cluster Boundaries → Candidate Contexts

**Statement:** Groups of stories that share a language and a set of work objects form candidate **bounded contexts**. Boundaries fall where the language shifts (the same term means something different) or where a different set of actors/work objects takes over. These candidates reconcile with the Stage 5 container decomposition.

**Verification:**
- [ ] Candidate bounded contexts are drawn around cohesive story clusters
- [ ] Boundaries are placed where the ubiquitous language changes meaning
- [ ] Each candidate context has a name and a one-line responsibility
- [ ] Candidate contexts are reconciled with Stage 5 containers (1:1, or the mismatch is explained)

**Anti-Pattern:** Drawing context boundaries along org-chart or technical lines instead of language and story cohesion.

**ADR Trigger:** Yes — when a candidate bounded-context boundary is non-obvious/contested, or when it drives the container decomposition.

---

### Rule DST-09: Ubiquitous-Language Glossary

**Statement:** The exact words used for actors, activities, and work objects during storytelling *are* the ubiquitous language and must be captured into a glossary as they are agreed, per candidate context.

**Verification:**
- [ ] A glossary is captured during (not after) the workshop
- [ ] Terms are recorded per candidate context (the same term may differ across contexts)
- [ ] Actor/activity/work-object names in the stories match the glossary
- [ ] Disputed terms are annotated (DST-05) rather than silently reconciled

**Anti-Pattern:** Translating the domain experts' words into technical jargon on the diagram, losing the domain language at the moment it was available.

**ADR Trigger:** No — the glossary hands off to DDD-11 (Ubiquitous Language Enforcement).

---

### Rule DST-10: Hand-Off Completeness

**Statement:** At stage completion, every element of every story must be routed to its downstream home; nothing is orphaned. A domain story exists to feed the design, not to decorate the wall.

**Verification:**
- [ ] Every actor maps to the role model (DST-06 / Stage 8)
- [ ] Every work object maps to a candidate entity/aggregate (DST-07 / DDD-01)
- [ ] Every story cluster maps to a candidate context (DST-08 / DDD-08 / Stage 5)
- [ ] Ubiquitous-language terms are in the glossary (DST-09 / DDD-11)
- [ ] Every annotation has a disposition (→ ADR / → Issue / → Assumption / resolved)
- [ ] Business-level activities implying product capabilities are noted for AI-POLC epic identification — informational and upstream only (AI-ADLC does not own that hand-off)

**Anti-Pattern:** A rich set of domain stories that never feeds the architecture — the "dead artifact" anti-pattern.

**ADR Trigger:** No

---

## Verification Checklist (Stage Completion)

Before completing a stage with Domain Storytelling rules active, verify:

- [ ] Each story uses the actor → activity → work object grammar (DST-01) and is numbered (DST-02)
- [ ] Each story declares scope + granularity (DST-03) and is labeled as-is or to-be (DST-04)
- [ ] Rules and pain points are captured as typed annotations (DST-05)
- [ ] Actors are consolidated into a candidate role model (DST-06)
- [ ] Work objects are collected as candidate entities/aggregates and handed to DDD-01 (DST-07)
- [ ] Story-cluster boundaries → candidate contexts, reconciled with Stage 5 containers (DST-08)
- [ ] Ubiquitous-language glossary started, per context (DST-09)
- [ ] Every story element is routed to a downstream home; no orphans (DST-10)

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| DST-05 | A captured rule/pain point resolves into a decision between 2+ viable architectural options with long-term impact |
| DST-08 | A candidate bounded-context boundary is non-obvious/contested, or it drives the container decomposition |

---

## Templates

### Domain Story

One numbered narrative for a single scope + granularity. Label as-is or to-be.

```
# Domain Story: {name}   ·   Scope: {slice}   ·   Granularity: {coarse|fine}   ·   {AS-IS | TO-BE}

| # | Actor | Activity | Work Object | → Recipient | Annotation (rule / pain / assumption / question) |
|--:|-------|----------|-------------|-------------|--------------------------------------------------|
| 1 | Customer | submits | Support Ticket | → Help Desk | rule: priority set from contract tier |
| 2 | Help Desk Agent | triages | Support Ticket | — | pain: no view of customer history |
| 3 | System | routes | Support Ticket | → Specialist Queue | rule: routing by product area |
| … | | | | | |
```

> Optional: render the numbered flow as a Mermaid sequence or flow diagram per `common/diagram-standards.md`. The table is authoritative; the diagram is an aid.

### Annotation Log

```
| ID | Story · Sentence | Rule / Pain / Assumption / Question | Disposition |
|----|------------------|-------------------------------------|-------------|
| AN-01 | {story} · #2 | pain: agent lacks customer history | → to-be story / → ADR-{NNN} / → Issue |
```

### Tag → Artifact Hand-Off Map

The routing contract — every story element lands in one of these homes.

```
| Domain Storytelling element | Downstream home | Rule / artifact |
|-----------------------------|-----------------|-----------------|
| Actor | Role/identity model · UXD personas | DST-06 · Stage 8 · AI-UXD |
| Work Object | Candidate entity/aggregate | DST-07 · DDD-01 |
| Story cluster | Candidate bounded context · containers | DST-08 · DDD-08 · Stage 5 |
| Ubiquitous language | Glossary per context | DST-09 · DDD-11 |
| Annotation (rule/pain/assumption/question) | ADR · Issue register · Assumption · to-be story | DST-05 · Architecture Workbook |
```
