# Hey Kivi memory: proposed evaluation and promotion protocol

Reviewed 6 September 2026 against `ARCHITECTURE_PROPOSAL.md`, `07-evaluation.md`, `14-ml-system-design.md`, and `PRODUCT_QUESTIONS.md`. This note proposes one protocol to replace the conflicting 60- and 80-question planning defaults. Nothing below has been measured, implemented, or approved as a final product target. No application code, installations, or model calls were used for this review.

**Recommendation:** build the first complete CLI around source retrieval and evidence-linked answers; evaluate typed memory as an addition. Carry the winning service into the UI. Five hundred transcript records are a corpus size, not 500 independent tests and not proof that full-history prompting is infeasible. Establish actual token counts first. The proposed category labels below are evaluation capabilities, not a selected memory taxonomy.

## 1. What the external evidence supports

- **LongMemEval:** its 500 questions cover extraction, multiple-session reasoning, temporal reasoning, knowledge updates, and abstention. It distinguishes indexing, retrieval, and reading, and reports retrieval separately from answer quality. These are useful diagnostic boundaries for Kivi; its generated conversational histories do not validate noisy multilingual transcripts. [Paper, ICLR 2025](https://arxiv.org/html/2410.10813v2)
- **Check the evaluator, not only a headline score.** LongMemEval's upstream QA grader tolerates off-by-one durations and accepts old information alongside the updated answer. Kivi's local rubric should instead require the supported time/state and reject incompatible facts presented as simultaneously current. Any later benchmark-compatible score must be separately labeled. [Official QA evaluator](https://github.com/xiaowu0162/LongMemEval/blob/main/src/evaluation/evaluate_qa.py)
- **LoCoMo:** generated, human-verified long conversations motivate linked-event, temporal, and evidence-retrieval probes. Its current repository release contains ten conversations; this is a different evaluation unit from Kivi's 500 records. Pin the actual dataset revision if used. The public project page and final paper give different length summaries, so do not mix their statistics. [Final ACL paper](https://aclanthology.org/2024.acl-long.747/), [Official data/code](https://github.com/snap-research/locomo)
- **Do not copy LoCoMo's local scoring shortcuts.** Its upstream QA code uses token F1 and defaults retrieval recall to 1 when the expected context information is absent. For Kivi, missing retrieval traces mean **not measured**. Use reviewed meaning and evidence, especially across scripts, negation, and aliases. [Official evaluator](https://github.com/snap-research/locomo/blob/main/task_eval/evaluation.py)
- **System design:** start with observable user outcomes, constraints, simple baselines, and incremental components; keep error diagnosis separate from model selection. [Huyen's author-published system-design guide](https://huyenchip.com/machine-learning-systems-design/design-a-machine-learning-system.html) Performance indicators should describe the user journey and capture typical and tail behavior, with a small number of operational targets. [Google SRE: implementing SLOs](https://sre.google/workbook/implementing-slos/)

The exact suite sizes, budgets, and gates below are local engineering proposals, not thresholds established by these sources. Running the complete public benchmarks is optional follow-up, not a prerequisite for this small prototype.

## 2. Freeze the data and the questions separately

Create a manifest for the approximately 500 records: stable user/source/revision IDs; raw/formatted pairing; source timestamps and timezones where supplied; import order; actual tokenizer lengths; languages/scripts; duplicates; missing fields; and material ASR/formatter disagreements. The pair is one observation, not independent corroboration. Preserve the original words; do not invent metadata to make a test answerable.

Author **80 human-reviewed probes: 30 development, 50 sealed**. Use one primary capability per probe, with overlapping difficulty tags:

| Primary capability | Development | Sealed | What success requires |
|---|---:|---:|---|
| Direct recall and attribution | 6 | 10 | Correct person, modality, names, numbers, and evidence |
| Combining records and complete evidence | 4 | 8 | All necessary connections; complete sets/counts when requested |
| Time, corrections, and changed state | 8 | 12 | Correct cutoff, order, historical/current distinction |
| Unknown, ambiguous, or conflicting information | 6 | 10 | Supported partial answer, focused clarification, or abstention |
| Contextual assistance and instruction priority | 6 | 10 | Useful adaptation or draft, relevant disclosure, current request respected |
| **Total** | **30** | **50** | **40 sealed answerable probes; 10 with insufficient/conflicting evidence** |

Keep the last group answerable: for some requests, correct behavior is a useful general answer without a personal callback. Mark memory use as required, optional, or inappropriate in its rubric. A correct contextual answer need not announce the remembered detail.

Split **whole narrative/scenario and template blocks**, including paraphrases and perturbations, before tuning. A feasible target is six development blocks and ten sealed blocks, five probes per block; distribute capabilities across blocks, not one capability per story. If naturally occurring records cannot support that structure, retain whole blocks, record the changed counts before sealing, and report reduced coverage. Shared background profile records can remain in the corpus, but tuning examples must not expose a sealed episode's answers. A single-user local holdout establishes local scenario generalization only. Duplicate and temporal leakage are distinct concerns. [Huyen's sampling/leakage exercises](https://huyenchip.com/ml-interviews-book/contents/7.2-sampling-and-creating-training-data.html)

Each probe records query text/time/timezone, permitted source revisions, supporting spans and acceptable alternative evidence sets, required claims, forbidden claims, answerability, expected response behavior, capability tags, and scenario ID. Keep probe questions, rubrics, and gold answers outside ingestion. A reviewer checks every gold label against both transcript variants; a second reviewer checks all ambiguity/multilingual cases and 20 randomly selected probes. If only one reviewer is available, disclose it and adjudicate their uncertainty before scoring. Do not use the answering model to certify its own gold labels.

Aim for at least 20 probes involving Hindi, Romanized Hindi, or code switching, including eight cross-language query/source probes. Include attribution, same-name ambiguity, quoted speech, plans versus completed events, negation, and ambiguous `kal`. These are overlapping tags, not a factorial test matrix. Missing natural coverage gets a separately labeled, hand-authored stress fixture; it does not inflate the natural-corpus score.

**Replay time correctly.** Store `available_at` separately from event time. At a query cutoff, ingest only permitted sources/revisions available by then; extraction context, entity links, indexes, and summaries must obey the same cutoff. A late-imported old event must not override a newer state simply because it arrived last. A future correction cannot improve an earlier answer. If availability metadata is absent, use a declared replay sequence and disclose that chronology is simulated. Never infer availability from event date alone.

## 3. Four primary systems, tested in stages

| System | Evidence supplied to the common answer service |
|---|---|
| F: full history | All permitted raw/formatted source pairs at the cutoff, when they fit |
| L: lexical sources | Lexical retrieval over original records, with original spans/context |
| H: hybrid sources | The same sources, lexical plus multilingual dense retrieval and rank fusion |
| T: typed memory plus sources | H plus attributed typed assertions and their original evidence; source fallback remains available |

Hold answer model/version, instructions, response limit, corpus cutoff, and scope fixed. For L/H/T, start with a **4,096-token total evidence budget**, including memory text, source excerpts, and source metadata. Deduplicate source evidence. A typed assertion and its supporting transcript cannot count as two independent supporting observations. Log Recall@5/10 on source IDs and actual evidence coverage **after** packing into the token budget; a retrieved ID with its decisive span omitted is not evidence delivered to the reader.

F gets the full permitted history when its token count plus the fixed prompt, query, reserved output, and a 1,024-token safety margin fit the verified model limit. Do not force F into the retrieval budget. Mark non-fitting probes unavailable for F, never silently truncate and call that full history. Report comparisons on the common fitting subset and all-probe coverage separately. All systems enforce correction, deletion, and user scope; F is not exempt from lifecycle controls.

Run the four systems on development first. Choose the strongest simpler alternative from F/L/H using the declared quality/operational gates; freeze it and one candidate for the 50 sealed probes. Retain F as a third sealed comparator only if it was not selected and its development result makes it a plausible deployment choice. Missing or unbuilt T is not a failed experiment; report the source system and the deferred question honestly.

Use no-memory and gold-source reader inputs on **12 development probes each** as diagnostic controls. Gold-source input locates generation failures; it is not an achievable retrieval system. Evaluate dense-only retrieval without extra answer calls when diagnosing H. Graph expansion, reranking, summaries, or cache are optional **development-only, one-component experiments** responding to an observed failure. Do not run a full architecture grid. A graph experiment initially means bounded relation expansion; it does not require a graph database.

## 4. Diagnose the whole path without one misleading score

Independently label eligible assertions in **50 source records**, grouped 20 development/30 sealed, reusing the probe scenarios plus some no-memory-worthy records. Report exact counts if fewer records support this. Score all candidates from those records against independently written labels, not against the extractor's candidate list alone. Record admitted-assertion precision, eligible-assertion recall, wrong subject/modality, invented detail, bad merge, and incorrect update. Evidence-span validity is a separate programmatic check, not proof of entailment.

For answers, make the primary score **fully supported task success**: all required claims/actions are satisfied, materially wrong additions are absent, attribution/time are right, and required personal-history claims have valid supporting evidence. Then report these diagnostics:

- Retrieval: source Recall@5/10, all-required-evidence rate, and delivered-span coverage; accept alternate valid evidence sets. Complete-list questions need coverage of the complete permitted set, not one matching record.
- Answering: strict correctness, claim-level citation support/completeness, and right-answer/wrong-source failures. A structured record ID check is necessary but insufficient.
- Answerability: false assertions on the ten insufficient/conflicted probes, false abstention/needless clarification on the 40 answerable probes, and correct-answer rate alongside answered coverage. Report partial success separately.
- State: the 12 temporal/update probes' current/historical accuracy and stale-current assertions. Unsupported exact dates fail; explicitly justified ranges may pass a range rubric.
- Personalization: blind paired preference for useful adaptation versus the simpler system; irrelevant callbacks, invented preferences, and inappropriate disclosure. Do not reward merely mentioning more memories.

Human review is primary at this size. If an automatic judge is later added, pin its model and rubric, blind candidate identity, and manually inspect every disagreement and every critical error. Record error location as source/gold ambiguity, extraction, retrieval, evidence packing, reading, lifecycle, or action control. Do not use hidden chain-of-thought as an evaluation artifact. Planning, tool execution, and efficiency can fail independently. [Huyen's agent evaluation discussion](https://huyenchip.com/2025/01/07/agents.html#agent-failure-modes-and-evaluation)

Show numerator/denominator and paired wins/losses. Estimate uncertainty by resampling whole scenario blocks, not individual correlated paraphrases. With ten sealed blocks, intervals remain coarse. Do not claim population-level language or user reliability from small slices. Fixing a sealed failure converts that suite into regression material; obtain a fresh holdout before claiming a new generalization result.

## 5. Twelve critical service checks, separate from semantic QA

Use deterministic staged outputs and tool simulators to control ordering and faults. These verify the service contracts; the 80 probes independently test whether models understand the language. No real send, booking, or external write is needed.

| Check | Required result |
|---|---|
| 1. Repeat import | Same source revision is idempotent; distinct identical utterances remain distinct events |
| 2. Interrupt/restart | Committed state survives; incomplete jobs resume without duplicate accepted memories |
| 3. Correction during extraction | Old candidate cannot commit over the corrected source revision |
| 4. Late old information | Older event arrival does not erase the supported newer state; historical answer remains possible |
| 5. Forget/delete during extraction or embedding | Delayed work cannot recreate excluded content or obsolete vectors |
| 6. Delete/correct during answering | Fresh evidence-generation check prevents release of stale/deleted material; buffer generated output until validation for the first implementation |
| 7. Forgetting across artifacts | Search, memory, aliases, candidates, mixed-source summaries, traces, and any cache obey deletion policy; rebuild excludes forgotten evidence |
| 8. User scope | User A's identifiers or model-suggested scope cannot read/write user B's records |
| 9. Instructions inside transcripts | Source text cannot edit policy, widen scope, forge authorization, or execute a tool |
| 10. Ambiguous or canceled action | Missing recipient/target/time and skipped clarification do not cause an external write |
| 11. Authorization and changed arguments | Only the currently authorized operation/arguments execute; changes or revocation invalidate a prepared action |
| 12. Tool retry and truthful status | Timeout/unknown provider outcome is not success; no blind duplicate write; proposed/authorized/attempted/succeeded/failed remain distinct |

Run each check when its component is introduced and after relevant changes. The source baseline already needs applicable scope/deletion/answer checks. A component not implemented is marked out of scope, not passed. Re-run these through the HTTP boundary before UI delivery. UI tests also verify that a canceled request does not surface a late stale result. Deletion cannot retract text already delivered or erase external originals/provider retention; the UI must describe the actual boundary.

## 6. Bounded run plan and operating budgets

The proposed initial assessment uses **at most 320 reader invocations**: 120 primary development runs, 24 diagnostic runs, up to 150 sealed comparisons, and 20 additional stability runs. For stability, repeat ten difficult development probes twice beyond their first run, before freezing; do not repeatedly rerun the sealed suite looking for a better outcome. Optional architecture experiments replace work within this cap or get a separately recorded follow-up budget. Extraction is one versioned materialization per compared extractor configuration, not one re-extraction per question; temporal snapshots may reuse only artifacts computed from the permitted prefix.

Preflight the corpus to determine extraction job count and exact estimated token demand. Configure one initial request plus at most one retry per transient model failure, output-token limits, concurrency, deadlines, and a total token/currency cap before live evaluation. A starting reader limit is 2,048 generated tokens including reasoning where the endpoint counts it; cap the visible answer near 512 tokens. If the selected endpoint cannot expose or enforce a limit, record the limitation and its accounting behavior. Failed and retried calls consume the run budget. Do not silently truncate source records to fit extraction; split or mark them pending with an explicit error.

Record ingest wall time/throughput, pending/failed coverage, extraction/embedding calls, database/index bytes, and peak local memory. On queries, separate scope/retrieval, query embedding, evidence preparation, model/network, and final validation; include first-visible-token time and total completion time. Report cold startup separately; warm measurements use at least the 50 sealed requests per finalist. Give p50/p95, sample count, max, timeout/error count, and cache state. Include failed request durations rather than reporting successful calls alone; report successes separately too. Do not claim p99 from this sample.

**Proposed prototype budgets to ratify after development profiling, before sealing:** local warm retrieval p95 <= 500 ms; complete ordinary Hey Kivi answer p50 <= 5 s and p95 <= 15 s; hard request deadline 30 s with explicit retry/failure behavior; no more than one ordinary reader call per query. These are desired service targets, not NVIDIA/DeepSeek measurements or guarantees. Batch ingestion is resumable; do not block source recall until every embedding/extraction finishes. Show processing coverage and label degraded retrieval. If the endpoint cannot meet the desired budget, revise the product scope/target openly before the sealed run rather than claiming it passed.

Report billed or estimated cost with provider/model/date and token categories. Free credits and quota do not make compute usage zero. If price is unavailable, report unknown monetary cost plus tokens/calls. Compare total cost as `ingestion + Q * query_cost` at Q=10, 100, and 1,000; state the intended reuse horizon. Include evaluation/judging and retry costs separately. Any cache test reports cold/miss/hit latency and hit rate under an explicit workload; repeated identical prompts are not an assumed production hit rate. Cache invalidation must pass checks 5-8 before its speed result is relevant.

## 7. Proposed promotion gates

These are **predeclared local acceptance proposals**, not achieved results or statistical reliability guarantees.

| Promotion | Proposed gate |
|---|---|
| First CLI path ready for comparison | All 500 intended sources are accounted for as imported/rejected with reason; IDs, provenance, and applicable critical checks pass; run manifest and source inspection work |
| Add typed memory to the answer path | On the 30 sealed extraction records, admitted precision >=95% and eligible recall >=80%, with zero critical wrong-person or invented-authorization writes; source fallback remains functional |
| Candidate ready for UI integration | At least 34/40 answerable probes have fully supported success; at least 9/10 insufficient/conflicted probes use the correct fallback; at most 2/40 false abstentions/needless clarifications; all 12 applicable service checks pass; zero cross-user disclosure, deleted-content release, unauthorized write, or false tool-success claim |
| Use extra complexity by default | Meets the above gate and either gains at least three net fully supported successes out of 50 against the simpler finalist, or preserves its successes while reducing measured p95 latency or intended-horizon total cost by >=20%; no new critical failure and no lower temporal/update success. Report uncertainty; a small local gain does not establish universal superiority |
| Final UI/backend demonstration | Same service and frozen configuration; repeat representative journeys for cited recall, changed-state answer, correction, forgetting, ambiguity, and a canceled/prepared action. All six succeed; citations open the correct surviving evidence, state persists across restart, statuses are truthful, and measured client latency meets the declared budget |

If evidence is insufficient to distinguish candidates, keep the simpler system and document the unresolved tradeoff. If a small category contains a failure, inspect it even when the aggregate gate passes. If a gate fails, report the failure and scope limitation; do not move the threshold after seeing sealed labels. Graphs, summaries, cache, and an adaptive tool loop remain optional until a specific measured problem justifies them. A CLI-only result does not satisfy the eventual requirement for a usable interface and backend together.
