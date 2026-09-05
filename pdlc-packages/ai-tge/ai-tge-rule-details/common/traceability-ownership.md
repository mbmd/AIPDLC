<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Traceability Ownership — AI-TGE keeps the register; under `aidlc` it reads-and-persists v2's outcome

> **Load this file** when AI-TGE runs under a workspace where AI-DLC v2 is the build engine (`buildProfile: aidlc`) and v2's own `traceability` / `upstream-coverage` sensors are present. It settles who owns the requirement-to-test traceability check when both AI-TGE's register and v2's sensors exist. This is merged item 27 (Decision G, resolved to **G3 + read-and-persist**); ledger rows B1/B7. `TR-820`.

## The overlap this resolves

AI-TGE's core output is a **Test Register** — a requirement-to-test map (the `coverageMatrix`, Rule 7: *"did we test what we designed?"*) built in Stage 3 and maintained through Observation (Stages 7/8/10). AI-DLC v2 **also** ships `traceability` and `upstream-coverage` sensors that compute an overlapping thing: whether each requirement has a test. Two systems, two ID schemes, the same question — unreconciled. The question item 27 answers: **when both exist, who owns the traceability check?**

## Why the two rejected options were never available

Decision G had three options; two were foreclosed before the choice was made:

| Option | Verdict | Why |
|---|---|---|
| **G1 — Drop AI-TGE's register; defer entirely to v2's sensors** | ❌ **Prohibited** | The register is how AI-TGE works under **all five** build methods; v2's traceability sensors exist **only** under `aidlc`. Dropping the register would remove requirement-to-test traceability for the other four build methods (`spec-driven-kiro`, `spec-driven-speckit`, `freestyle`, `manual`) — that is **capability removal**, which §0.1 principle 4 forbids. A capability cannot be deleted because *one* build method happens to supply an alternative |
| **G2 — Keep the register AND re-run the traceability check ourselves under `aidlc`** | ❌ **Contradicts precedent** | Re-running a check v2 already ran **double-counts** the outcome — the exact failure the observability read-and-persist boundary (merged item 21) established: where v2 computes something, AI-TGE reads and persists it rather than re-executing. Applying that precedent here, re-running traceability is not an option |
| **G3 — Keep the register; under `aidlc`, read v2's computed traceability outcome and persist it** | ✅ **Taken** | The register survives (no capability removed under any build method), and under `aidlc` AI-TGE does not re-run — it reads v2's outcome into its own register, the same read-and-persist seam as the observability spine |

## The resolution — keep the register, read-and-persist under `aidlc`

**AI-TGE keeps its Test Register under every build method.** It is the single source of the requirement-to-test map, and it is how traceability is delivered under the four non-`aidlc` methods where v2's sensors do not exist.

**Under `aidlc`, where v2's `traceability` / `upstream-coverage` sensors run**, AI-TGE does **not** re-run the traceability check. Instead, at its Observation heartbeat (Stage 7), it **reads v2's computed traceability outcome and persists the derived status into its own register entries** — the same "read the engine's outcome, persist the derived event, do not re-execute" seam that `ai-gce/…/common/observability-read-and-persist.md` (item 21) established for the compliance spine. A register entry whose traceability v2 has already computed is marked from v2's result (`source: aidlc-traceability-sensor`), not re-derived by a second scan.

| Build method | Who computes traceability | AI-TGE's register |
|---|---|---|
| `aidlc` | v2's `traceability` / `upstream-coverage` sensors | **Kept** — reads v2's outcome and persists it into register entries (read-and-persist, no re-run) |
| `spec-driven-kiro` · `spec-driven-speckit` · `freestyle` · `manual` | AI-TGE (no v2 sensors exist here) | **Kept** — AI-TGE computes and maintains it directly, as today |

## No traceability sensor id is frozen — the ID schemes stay separate

The frozen output contract (§4) freezes `pdlc-test-coverage` (coverage ownership is settled: AI-TGE) but deliberately **does not freeze a traceability sensor id**. Traceability ownership stays with **AI-TGE's own register ID schemes** (the `coverageMatrix` / register-entry IDs), and v2 keeps **its** sensor IDs. AI-TGE does not mint a `pdlc-traceability` manifest, and it does not adopt v2's sensor IDs into its register — it reads v2's *outcome* and records it against its *own* entry IDs. The two schemes coexist; the read-and-persist seam is the bridge, not a shared ID space. This is why the sensor-manifest registry (item 25) has ten AI-GCE manifests + `pdlc-test-coverage` but **no** `pdlc-traceability`.

## Preserves capability, only relocates who computes it (INV-L2-022)

Requirement-to-test traceability is delivered under every build method — the capability is never dropped (that is what makes G1 prohibited). Under `aidlc` the *computation* moves to v2's sensor and AI-TGE *reads* the result; under the other four methods AI-TGE computes it itself. The register — the persistent artifact and the ID scheme — is unchanged in both cases. No capability cell moves: TR-820 passes because traceability (B1) and the register/coverage relationship (B7) are preserved, only the compute-vs-read split differs by build method.

## Interaction with other files

| Related | Relationship |
|---|---|
| `observation/state-observation.md` (Stage 7) | The Observation heartbeat where, under `aidlc`, AI-TGE reads v2's traceability outcome and persists it into the register |
| `common/observation-fidelity.md` | The read-and-persist under `aidlc` is a declared input like any other — if v2's traceability outcome does not resolve, that is a disclosed degraded read, not a silent re-run |
| `common/process-overview.md` | Carries the delivery-method-invariance boundary (scope invariant, observation mechanism not) — this file adds the traceability compute-owner split on top |
| `ai-gce/…/common/observability-read-and-persist.md` (item 21) | The precedent this mirrors — read the engine's outcome, persist the derived record, never re-run |
| `ai-dwg/…/common/aidlc-v2-output-contract.md` §4 | Freezes `pdlc-test-coverage` but **not** a traceability sensor id — the contract basis for keeping the ID schemes separate |

## Output validation

- [ ] AI-TGE keeps its Test Register under **all five** build methods (dropping it is prohibited — G1, §0.1 principle 4).
- [ ] Under `aidlc`, traceability is **read from v2's sensor outcome and persisted**, never re-run (G2 rejected; item 21 precedent).
- [ ] Under the four non-`aidlc` methods, AI-TGE computes traceability itself (no v2 sensors exist there).
- [ ] No `pdlc-traceability` sensor id is minted; AI-TGE's register ID schemes and v2's sensor IDs stay separate.
- [ ] A read of v2's outcome that fails to resolve is a disclosed degraded read (observation-fidelity), not a silent re-run.
- [ ] The capability (requirement-to-test traceability) is preserved under every build method (INV-L2-022).

---

*Developer-side design detail · AI-TGE traceability ownership boundary · © Mohammad Maheri*
