<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Rules / Knowledge Splitter — the transformation `memory-mapping` and `knowledge-routing` both invoke

> **Load this file** whenever the `aidlc/` emitter processes a canonical steering file (emitter steps 1 and 2). It is the single transformation that separates a steering file's **rules** from its **knowledge**; `memory-mapping.md` consumes the rules half, `knowledge-routing.md` consumes the knowledge half. Authority for the destinations: `common/aidlc-v2-output-contract.md` §2 (memory) + §3 (knowledge). (Compatibility design Proposal 2, addressing gaps G2 + G9.)

## Why a splitter

Every PDLC canonical steering file carries **two kinds of content in one document**:

- **Rules** — enforceable `MUST` / `MUST NOT` / `NEVER` statements. These are *constraints the agent obeys*.
- **Knowledge** — prose, tables, diagrams, reference material. This is *context the agent reads*.

v2 wants these in **different places**: rules become behavioural memory (`memory/project.md`), knowledge becomes per-agent reference (`knowledge/<agent>/`). A steering file dropped whole into either place is wrong in one of two ways — as memory it buries constraints under prose the agent must re-scan every turn; as knowledge it hides binding rules where nothing treats them as binding. The splitter is what makes each half land where it is treated correctly.

## The classification rule

Read the steering file statement by statement (a statement is a bullet, a sentence, or a table row):

| Statement shape | Portion | Destination |
|---|---|---|
| Contains `MUST` / `MUST NOT` / `NEVER` / `SHALL` / `REQUIRED` — a binary, checkable constraint | **Rule** | `memory/project.md` (or `memory/team.md` per the memory-mapping heading table) |
| Prose, a table of reference values, a diagram, an example, a rationale ("because…", "the system uses…") | **Knowledge** | `knowledge/<agent>/` per the routing table |
| A rule **with** its tightest supporting sentence | **Both** — the rule goes to memory; the supporting sentence may also go to knowledge if it carries reference value | split across both |

**The tie-breaker:** if a statement is *checkable* (an agent or a sensor could pass/fail against it), it is a rule. If it is *informative* (it tells the agent how something works but cannot be failed), it is knowledge. A "should" or "consider" is knowledge, not a rule — v2 memory rules are binary, matching AI-DWG's own prescriptive-output rule.

## Worked example — `security-rules.md`

| Source statement | Portion | Lands in |
|---|---|---|
| "The system uses OAuth 2.0 with PKCE flow for SPAs. Token rotation happens every 15 minutes." | Knowledge (reference — how auth works) | `knowledge/aidlc-devsecops-agent/` |
| "All endpoints MUST validate the Authorization header." | Rule (checkable constraint) | `memory/project.md ## Security` |
| "NEVER log token values." | Rule | `memory/project.md ## Security` |

The same source file feeds **both** targets — its rules to memory, its reference prose to the devsecops agent's knowledge directory. This is why `memory-mapping.md` and `knowledge-routing.md` are two consumers of one splitter pass, not two independent readers of the source.

## Invariants

1. **No statement is lost.** Every statement lands in at least one destination. A statement that is neither a clear rule nor clear knowledge defaults to **knowledge** (the safer side — misclassifying a rule as knowledge under-constrains but is visible; misclassifying knowledge as a rule creates a false binary check).
2. **No `should`/`consider` becomes a memory rule.** v2 memory rules are binary. Soft guidance is knowledge. This matches AI-DWG Rule 1 (prescriptive output: MUST/NEVER, no "should").
3. **The split runs once per source file** and feeds both consumers — never split the same file twice with divergent results.
4. **Front-matter is applied by the consumer**, not the splitter: memory gets `status:` + `pairing:` (memory-mapping); knowledge gets the provenance block (knowledge-routing).

## Relationship to the two consumers

| Consumer | Takes | Applies |
|---|---|---|
| `memory-mapping.md` | the **rules** portion | routes each rule to the frozen heading (team.md vs project.md) + phase files; adds `status:`/`pairing:` |
| `knowledge-routing.md` | the **knowledge** portion | routes each reference block to the correct agent directory; adds the provenance block |

The splitter is the shared front step; the two mapping files are the back steps. Together they are emitter steps 1–2.

---

*Developer-side design detail · AI-DWG `aidlc/` rules/knowledge splitter · © Mohammad Maheri*
