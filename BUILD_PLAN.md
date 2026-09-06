# Kivi build plan, evaluation and reviewer handoff

**6 September 2026: application unbuilt.** [ARCHITECTURE.md](ARCHITECTURE.md) governs technical contracts; [RESEARCH.md](RESEARCH.md) preserves rationale; [README.md](README.md) is the entry point. This plan consolidates product behavior, implementation, evaluation, validation history and submission work.

**Next:** specify one recurring journey, then build persistent import → cited answer → correction/forget with evaluation fixtures. CLI/UI/backend/migrations/importer/model integration/~500-record corpus/product evaluation remain unbuilt. Only the isolated sequential SQLite probe has recorded 12/12 results; limits below. Planning coverage is not a product completion percentage.

Mentor route: [single flowchart](KIVI_COMPLETE_FLOW.svg), [process SVG gallery](mentor-svg/index.html), [navigable guide](ARCHITECTURE_GUIDE.html). Images explain proposed behavior, not working features.
## 1. Product scope and assignment obligations

Golden Goose is the selected assignment; the earlier backend/phonetic alternative is superseded. The value sought is to recover past information, connect distributed evidence/changes, and apply relevant context to a current answer or draft. Select one recurring task; “best memory” is a quality goal. Jaipur examples illustrate behavior, not a finalized product position. An earlier two-day ambition is historical, not a verified remaining deadline.

Regular Kivi preserves intended dictation with vocabulary/spelling/style/formatting assistance; it must not inject unsolicited personal history. Our demo imports raw ASR + formatted text + available metadata, accepts typed Hey Kivi questions, and implements semantic memory over the same SQLite file as normal product/source state. No ASR, phonetic learner or production Kivi integration is required. Public research did not verify native-app use or a built-in chat/project workspace; app name is not project identity.

**Part One remains the applicant’s responsibility:** actually use Kivi/study other products, independently form and write the position (≤100 words) and vision (≤600 words), and preserve them before Part Two as required by the brief. The brief excludes generative AI from arriving at or writing that position. Completion is not established; this AI-assisted plan does not replace it. Disclose actual AI use; do not generate Part One during implementation.

Required Part Two outcomes:

- One genuine product with a normal-user interface and persisted backend; CLI first is an intermediate milestone, not sufficient final delivery.
- Define what is learned/ignored/never assumed, how factual/episodic/preference knowledge is represented and controlled, and demonstrate its effect on later behavior.
- Answer any reasonable question stated in or derivable from history, including temporal/distributed evidence; narrow tools cannot justify a fixed demo-question list.
- Inspect original sources, created/retrieved/changed/rejected memories, evidence, resulting behavior and concise reasons; support simple correction/forgetting.
- Prepare approximately **500 paired history records**, evaluate the whole pipeline, and support a reviewer’s different approximately 500-record single-user corpus. This is not 500 questions.
- Deliver source/UI/backend/schema/migrations/seed/corpus/results and reproducible start/import/process/ask/inspect/evaluate/reset instructions.

Missing metadata, languages, project IDs and evaluator questions are unknown; preserve missingness. English/Hindi/Hinglish coverage is a proposed test scope, not a hidden-corpus guarantee. A local application with hosted NVIDIA/DeepSeek access is the proposed review arrangement: local storage does not mean offline processing. Hosting, Docker, speech capture and broad integrations are optional.
## 2. Specify the first useful journey

Write a small behavior specification before choosing a UI framework: returning user, recurring task, useful output, relevant history, inspection/control and normal/ambiguous/changed/forgotten/interrupted/failed states. Define sensitive-data, retention and no-personalization behavior explicitly.

| State | Acceptance behavior |
|---|---|
| Recover | A promise to Riya is recalled with correct person and source, or the evidence gap is stated. |
| Connect changes | A Jaipur comparison combines relevant earlier/later records, separating current state, history and conflict; import order alone cannot restore an old value. |
| Apply | A checklist uses relevant current budget/scoped preference. Present explicit instructions override memory; a one-off instruction is not automatically permanent. |
| Inspect | Show interpretation and exact supporting source revision/field/span; raw/formatted variants are one observation. |
| Correct | Distinguish an extraction mistake from real-world change. Claim saved success only after the actual committed receipt. |
| Forget/delete | Forget blocks selected information, known support and derivatives across future reads/fallback/replay. Delete-source additionally removes selected in-app originals. Repeating forgotten information in the control request cannot teach it again. Exports/backups/providers/already delivered text have separate boundaries. |
| Uncertainty | Ask one focused question only for a material missing distinction; otherwise omit, give supported alternatives/partial answer or label a reversible assumption. Skipping is not confirmation. Lack of evidence is an honest gap, not an invitation to invent. |
| Action/failure | Show target/operation; execute only within current authority and complete material arguments. Report actual success/failure/unknown. Preserve partial work, suppress late cancelled answers, reconcile uncertain effects before retry; cancellation after dispatch does not promise rollback. |

Memory must help the task; a general answer or silent adaptation can be correct. A visit does not imply enjoyment, date, preference or intent to return; someone else’s visit and a fictional draft are not personal events. A postponed trip does not prove its meeting moved. A document path does not prove content access. Historical instructions never grant current authority. Users should not classify memories or merge nodes; background ambiguity waits until relevant, and model confidence percentages are not calibrated decision thresholds.
## 3. Work packages and implementation sequence

Stages are dependencies, not promised hours. Include scope, exclusions, control receipts and traces from the first source path. The exact schema/transaction/freshness/module contracts remain in [ARCHITECTURE.md](ARCHITECTURE.md); every client uses one implementation.

| Stage | Build and exit evidence |
|---|---|
| 0. Behavior | Select the journey, outcome, mode/control/uncertainty UX and review arrangement; account for Part One. Expected results are explicit in each state. |
| 1. Source foundation | Pin runtime/dependencies; import contract, migrations, stable revisions/heads, permitted projections, jobs/policy versions, inspection/FTS5 and bounded reset. Small reviewed fixture survives restart; reimport is accounted for; applicable integrity checks pass. |
| 2. Real CLI answer | Coordinator + provider preflight + lexical sources + evidence packing + cited answer/unknown/clarification + explicit controls + status/usage. A real persisted query works; correction changes its next answer; forget blocks fallback/replay; receipts, calls and latency are visible. |
| 3. Measured memory | Selective background admission, 12 labels, scoped entities/aliases/time, dependencies and controls; add dense retrieval separately. Compare development outcomes; source fallback works despite extraction misses; stale work cannot bypass controls. |
| 4. Useful output/evaluation | One justified artifact tool, reviewed corpus/questions, paired development comparisons and fault diagnosis. Truthful operation/partial outcomes, passing affected checks; sealed cases unopened. |
| 5. Complete UI | Choose interface/API around the same core; evidence, natural controls, processing, error/ambiguity/cancellation states. Real UI/backend journeys pass; freeze pipeline/models/policies/configuration and comparator. |
| 6. Assess/rehearse | Run sealed comparison, retain failures/limits, package source/data/results/runbook, rehearse unfamiliar corpus from clean checkout. Reviewer can start/import/process/ask/inspect/evaluate/reset; sealed-informed changes need a new holdout for fresh generalization claims. |

Detailed implementation responsibilities, module layout, planned CLI commands, import fields and environment names are in ARCHITECTURE §§7–11. Keep these acceptance requirements explicit:

- One shared MemoryService/coordinator serves CLI and final UI; short atomic writes, trusted scope, evidence/receipt validation, durable jobs and stale-attempt fencing. Source fallback is independent of successful extraction; qualified entities/time and complete-list evidence must survive every route.
- Live input begins private/held; model proposes, controls commit, surviving input is released, bounded continuation follows, and freshness/cancellation gates final persistence/delivery/replay. Ordinary learning stays off the answer critical path.
- Freeze versioned import required/null/malformed/identity/revision behavior before corpus creation. Preserve Unicode, raw/formatted disagreement and missing metadata. Account every row; distinct identical events remain distinct; reimport respects exclusions/tombstones, with restoration explicit.
- CLI is planned, not executable. One-shot exit leaves persisted eligible jobs/status for explicit resume; held jobs need coordinator resolution. REPL may keep worker/encoder warm; no invisible daemon.
- Verify exact NVIDIA/DeepSeek deployment, context/tokenizer/output/tool support, accounting/account limits, retries/deadlines and package/model pins. Credentials stay outside source/history/traces/Git; document cold/warm startup/download needs. No free/unlimited quota is promised.
- Python/sqlite3/FTS5/Pydantic/HTTPX/argparse are baseline choices; local E5-small/sentence-transformers/NumPy is a measured option, BGE-M3 a comparator. UI/API/test framework remains undecided. First proposed effect: requested local artifact with designated-directory/expected-version/authority validation and observable receipt; reconcile unknown writes. MCP is an optional adapter, never authority.
Cut graph servers, Redis, approximate indexing, query/answer caches, recursive summaries, rerankers, autonomous reflection, roles/skills frameworks, broad integrations and optional experiment grids before source coverage, evidence, controls, evaluation or final UI. Keep a simpler source route where it performs better.
## 4. Evaluation protocol: prove useful behavior without leakage

All counts, budgets and thresholds are **proposals, not achieved results or assignment-prescribed targets**. Ratify on development/preflight before opening sealed labels. Use two sealed finalists by default; the older near-cap 314-attempt schedule is superseded.

### Data and leakage controls

Create approximately 500 coherent paired records with recurring people/events, distractors, changes, duplicates, missing metadata and ASR/formatter disagreements. Manifest IDs/revisions, raw/formatted pairing, actual token lengths, languages/scripts, capture/timezone/availability and import order. Do not shape history around demo questions or trust unchecked generated gold.

Propose **80 reviewed questions: 30 development / 50 sealed**, plus an independent **50-source extraction audit: 20 development / 30 sealed**, including no-memory-worthy sources. Score eligible assertions against independent labels, not only extractor proposals.

| Primary capability | Development | Sealed |
|---|---:|---:|
| Direct recall/attribution | 6 | 10 |
| Combining records/complete evidence | 4 | 8 |
| Time/corrections/changed state | 8 | 12 |
| Unknown/ambiguous/conflicting information | 6 | 10 |
| Contextual assistance/current instruction priority | 6 | 10 |
| **Total** | **30** | **50: 40 answerable, 10 insufficient/conflicting** |

Split whole narrative/scenario/template blocks including paraphrases/perturbations before tuning. Initial structure: six development and ten sealed blocks of five questions, capabilities distributed across stories. If natural data requires different counts, declare reduced coverage before sealing. Shared background records may remain without exposing sealed episode answers. A single-user holdout supports local scenario generalization, not population reliability.

Every question records text, query time/timezone, permitted source revisions, acceptable supporting spans/evidence sets, required/forbidden claims, answerability, expected behavior, tags and scenario ID. Contextual rubrics mark memory required/optional/inappropriate; a general answer or silent adaptation can succeed. Keep questions, rubrics and gold out of ingestion. Review every label against both transcript variants; ideally a second reviewer checks all ambiguous/multilingual cases and 20 random questions. Disclose single-reviewer limits and settle uncertainty before scoring. The answer model cannot certify its gold.

Target ≥20 multilingual/mixed questions including eight cross-language pairs: Devanagari Hindi, Romanized Hindi/Hinglish, code switching, names, negation, dates and ambiguous “kal.” These are overlapping slices, not a factorial grid or hidden-language guarantee. Missing natural coverage gets separately labeled authored stress fixtures, not inflated natural-data scores. English UI choice is separate from multilingual handling.

Temporal replay admits only permitted revisions available by the query cutoff; extraction context, links, summaries and indexes obey it too. Event/validity, capture and availability differ. Future corrections cannot improve earlier answers; late old events cannot become current by import order. Without availability metadata, declare simulated replay order rather than invent chronology.

### Comparable systems and diagnostics

| System | Common answer service receives |
|---|---|
| F: full history | All permitted raw/formatted source pairs at cutoff, where they actually fit |
| L: lexical sources | Original-source keyword retrieval with spans/context |
| H: hybrid sources | L plus multilingual dense candidates and rank fusion |
| T: typed memory + sources | H plus attributed assertions and original evidence; source fallback stays available |

Hold answer model/version, instructions, output limit, scope and cutoff constant. L/H/T begin with **4,096 total evidence tokens**, including memories/excerpts/metadata. Deduplicate observations; memory plus supporting transcript is not two witnesses. Score source Recall@5/10 and all-required/decisive-span coverage **after packing**; retrieved IDs without decisive text are not delivered evidence. Missing traces mean unmeasured, not perfect recall.

F receives full allowed history if it + prompt/query + reserved output + proposed **1,024-token safety margin** fit the verified context window. Do not force F into the retrieval budget or silently truncate. All systems obey controls. Report F’s fitting comparison subset and unavailable coverage separately.

Run four implemented systems on development. Freeze the strongest simpler F/L/H alternative and one memory candidate before the 50 sealed questions. Unbuilt T is untested, not a failed experiment. A third plausible full-history comparator needs an explicit pre-sealed budget revision. Retain source routes where extraction adds no value.

Optional diagnostics: **12 development no-memory calls + 12 gold-source calls**; gold-source locates reading failures, not achievable retrieval performance. Dense-only retrieval can be diagnosed without additional answer calls. Graph expansion/reranking/summaries/cache are development-only, one-component experiments justified by observed failures, not a full architecture grid. A graph experiment starts with bounded supported SQL expansion, not a graph server.

### Metrics and judgment

Primary score: **fully supported task success**—all required claims/actions, no material unsupported addition, correct subject/time/modality and valid evidence for required personal claims. Fluency, matching answer text or valid IDs alone are insufficient.

| Layer | Measures |
|---|---|
| Import | Intended/accepted/duplicate/pending/rejected counts, provenance, missingness/ambiguity and readiness |
| Extraction | Admitted precision/eligible recall, wrong subject/modality, invented detail, bad merges/updates, unresolved/no-op outcomes; span validity separately from entailment |
| Retrieval/packing | Source Recall@5/10, complete required evidence and decisive delivered spans, alternate valid sets, truncation/readiness; list/count questions need complete set coverage |
| Answer | Supported success, claim/citation completeness, right-answer/wrong-source, current/historical accuracy and stale-current assertions; unsupported exact dates fail, justified ranges may pass their rubric |
| Abstention | False assertions on insufficient/conflicting cases, needless abstention/clarification on answerable cases, answered coverage and partial success |
| Personalization | Useful blind paired adaptation versus simpler system, instruction priority, invented preference/irrelevant callback/inappropriate disclosure; no reward for merely mentioning memory |
| Tools | Actual effect, target/permission and truthful proposed/authorized/attempted/succeeded/failed/unknown status |
| Operations | Ingestion throughput/lag/readiness, cold/warm latency, retries/errors, DB/index growth, model RAM, calls/tokens/cost |

Human review is primary. Any automatic judge has a pinned model/rubric, blinded candidate identity where possible, and manual inspection of every disagreement/critical error. Record observed traces and concise reasons, not hidden chain-of-thought. Diagnose source/gold ambiguity, extraction, retrieval, packing, reader, lifecycle and action separately. Public benchmark scores, token-F1 shortcuts and permissive conflicting-date scoring do not establish Kivi quality.

Report counts/denominators and paired wins/losses. Resample whole scenario blocks, not correlated paraphrases; ten sealed blocks and small language slices give coarse evidence. Inspect subgroup failures despite aggregate success. Sealed-informed fixes turn those cases into regression material; use fresh holdout for a new generalization claim.

### Proposed gates and bounded run

| Gate to ratify before sealing | Initial threshold |
|---|---|
| Import | Every intended source accounted for, inspectable status/provenance/manifest, applicable integrity checks pass |
| Typed extraction | On 30 sealed sources: ≥95% admitted precision, ≥80% eligible recall; zero critical wrong-person/invented-authorization writes |
| Supported task quality | ≥34/40 answerable successes; ≥9/10 correct insufficient/conflict fallbacks; ≤2/40 needless abstentions/clarifications |
| Critical integrity | Zero cross-user disclosure, excluded-content release, unauthorized write or false tool success in applicable tested scenarios |
| Added default complexity | ≥3 net supported successes out of 50, or preserved successes with ≥20% lower measured p95 latency or intended-horizon total cost; no new critical failure/weaker temporal performance |
| Final UI | Cited recall, changed-state answer, correction, forgetting, ambiguity and prepared/cancelled-action journeys succeed through real UI/backend; correct surviving sources, persistence, truthful outcomes and declared client latency |

These sample gates are not reliability guarantees. Select/integrate on development; sealed assessment evaluates the frozen final pipeline. If indistinguishable, prefer simpler and disclose uncertainty. Unimplemented/untested optional components never pass. Do not move thresholds after sealed results.

**Reader cap: 320 actual attempts.** Four systems ×30 development =120; two finalists ×50 sealed =100. Optional 24 diagnostics +20 stability repeats yield **264 planned attempts, 56 reserve**. Repeat ten difficult development questions twice beyond first run before freezing; never rerun sealed cases seeking a better result. Multi-call requests, failures and retries consume the cap. Trim optional diagnostics first; do not drop difficult questions. Budget exhaustion means incomplete. Declare separate extraction/embedding/judging budgets; materialize each extraction configuration once with only permitted replay-prefix context.

Preflight extraction jobs/tokens, concurrency/deadlines and total token/currency ceilings. Starting transient policy: initial request + at most one retry within all budgets. Proposed generation cap **2,048 tokens including reasoning where enforceable**, visible answers near 512. Verify endpoint accounting and disclose unenforceable caps. Split oversized extraction records safely or mark pending; never silently truncate.

Unmeasured prototype targets: warm local retrieval p95 **≤500 ms including query encoding, DB/vector work and packing**; ordinary full answer p50 **≤5 s**, p95 **≤15 s**; ordinary deadline **30 s**. Aim for one ordinary reader call; bounded continuations follow architecture limits. Revise infeasible targets openly during development before sealing.

Measure cold one-shot startup versus warm REPL/service; warm sample includes ≥50 sealed requests per finalist. Separate encoding/retrieval/packing/model-network/final validation. Buffered answers include validation in first-visible time. Include failed requests in end-to-end timing, show successful-only separately, p50/p95, count/max/errors/timeouts/cache state; no p99 claim from this sample. Source recall works while optional learning/dense work is pending; display degraded coverage and ingestion lag.

Cost reports identify provider/model/date/token categories. Compare **ingestion + Q × query cost** at **Q=10/100/1,000** and declared reuse horizon; separate retries/evaluation/judging. Free credits do not erase usage; unknown monetary prices remain unknown with calls/tokens reported. Future cache experiments require explicit workload, cold/miss/hit latency and hit rate plus passing invalidation checks before speed matters.
## 5. Real product integrity suite

Use deterministic staged outputs, fault injection and tool simulators as each component arrives; semantic understanding is evaluated separately. Run applicable checks on the source baseline immediately and repeat affected checks through the final HTTP/UI boundary. Absent components are unimplemented/out of scope, never passed.

| Scenario | Required result |
|---|---|
| Repeat import | Same revision/payload idempotent; distinct identical utterances remain separate; exclusions/tombstones survive. |
| Interrupt/restart | Committed disk state survives; eligible jobs resume without duplicate memories; extraction cannot release held work. |
| Correction during extraction | Obsolete source/control revision candidates cannot overwrite corrected state. |
| Late old information | Arrival order cannot replace supported newer state; historical answers remain possible. |
| Forget/delete during extraction/embedding | Late candidates/vector writes cannot recreate excluded information or obsolete meaning. |
| Control during answering | Freshness check rejects stale/deleted evidence before atomic response/sequence publication; buffer output. |
| Dependent cleanup | Source fallback, memories, aliases/edges, candidates, mixed-source artifacts, traces, replay and caches obey exclusions; rebuild only surviving evidence. |
| User scope | Guessed IDs, model scope, imports/evidence links/retrieval cannot cross owners. |
| Hostile history | Source instructions cannot change policy, scope, authority or dispatch tools. |
| Ambiguous/skipped/cancelled action | Missing material target/time/recipient and skipped clarification block the effect; cancelled late results stay suppressed. |
| Changed authority/arguments | Current authorized operation/arguments and expected target/version govern dispatch; changes/revocation invalidate prepared work. |
| Unknown outcome | Timeout/expired task proves neither success nor absence of effect; reconcile before retry and retain truthful partial/unknown state. |
| Forget while held | Private reread, later publication, FTS and full-source fallback all obey current projection; repeated forgotten text is not relearned. |
| Own-source promotion | Only trusted-code promotion of identical already-seen input may rebase a matching snapshot; unrelated changes or altered/excluded text reject. |

Exercise real rollback/idempotency: same operation key/payload replays receipt; changed payload conflicts. Sources/jobs and memory/evidence/index/job/revision changes commit together; worker attempt tokens fence stale completion; linked run retries retain receipts. Separately test actual threads/processes, disk crash/WAL recovery, provider failures, graph/alias dependencies and selected artifact integration. Deletion cannot retract delivered text or erase external originals/providers; UI wording must match the boundary.
## 6. What the existing SQLite probe establishes

[Probe source](research/validation/atomic_memory_probe.py) and [recorded results](research/validation/atomic_memory_results.json): **12/12 passed**, Python 3.12.14 / SQLite 3.53.1; fresh in-memory DBs, foreign keys, actual transactions and FTS5 triggers with controlled **sequential** interleavings. This is an executable design model, not application code or a benchmark.

Cases: `atomic_admission_rollback`, `operation_idempotency`, `cross_user_scope`, `stale_extraction_fencing`, `held_input_visibility`, `forgotten_span_projection`, `stale_vector_cache_and_mirror`, `stale_publication_rejection`, `response_replay_after_forget`, `partial_index_and_atomic_publication`, `forget_before_held_source_release`, `own_source_promotion_rebase`. The linked JSON preserves each exact check and negative controls.

History: initial 10/10 passed; adversarial case 11 exposed forgotten text returning through private-current-input, source FTS and full-source fallback when no search document existed at forgetting time. Shared `projected_source_text` fixed rereads/release independently of index presence: 11/11 passed, original text retained, demonstrating use suppression rather than physical erasure. Case 12 checked the narrow trusted-receipt promotion/freshness exception. Raw-table bypasses and unchecked publication in negative controls demonstrate why every read/publication boundary matters.

**Not tested:** actual concurrency, disk crash/WAL, network delivery/provider retries/MCP; LLM extraction/entailment/control detection/answers; embedding quality/speed (synthetic vectors only); arbitrary-paraphrase forgetting, physical erasure, backups/provider retention or alias/graph cleanup. Response dependencies use one source and conservative invalidation. The product must implement/test contracts independently; documentation consolidation adds no validation claim.
## 7. Submission and clean-checkout review

Keep the repository portable: relative artifact links, versioned source/configuration and explicit dependencies; no machine-specific credentials, undocumented local services or assumption that the original desktop path exists. The current README can explain the planning artifacts and probe. Add real install/run commands only when implemented and tested. At application delivery, a `RUN.md` must begin with the declared primary review arrangement.

- [ ] Applicant-authored Part One position/vision with required limits, ordering and honest provenance.
- [ ] One GitHub repository with complete application source, usable normal-user interface and connected backend.
- [ ] Actual schema/versioned migrations and reproducible seed data; approximately 500 paired transcript records plus corpus manifest.
- [ ] Runnable full-pipeline evaluation, reviewed questions/rubrics, generated results, paired comparisons, observed failures and limitations.
- [ ] Inspectable original inputs, accepted/retrieved/changed/rejected memories, supporting sources, resulting behavior and concise decision reasons.
- [ ] Latency, DB/index growth, model calls/tokens and relevant cost accounting with dates/configuration and validation limits.
- [ ] README describing product, architecture, use cases, measured results, limitations and AI use.
- [ ] Tested `RUN.md`, exact Python/package/model pins, model download/startup requirements, every environment variable and a secret-free `.env.example`.
- [ ] Commands for dependency installation, DB create/migrate/seed, each process startup and exact URL/window/interface to open.
- [ ] Primary interactions to try; exact unfamiliar-corpus import format, processing/resume, inspection and Hey Kivi procedure.
- [ ] Exact evaluation command, result locations and explanation of scope/holdout status.
- [ ] Explicit application-owned reset boundary and tested reset command that cannot remove unrelated files.
- [ ] Clean-checkout rehearsal against the submitted commit: install → start fresh → import unfamiliar fixture → process → ask → inspect → correct/forget → evaluate → reset; no hidden manual repair.
- [ ] Submission form includes repository URL and exact final commit SHA, plus hosted URL only for a hosted primary review method.

A reviewer may supply documented credentials and translate their logs to the documented format. They will not infer missing setup or repair the application. Deployment/Docker are optional; reproducible local setup is sufficient. A published architecture repository is useful for continuing work on another system, but it is not the completed product submission.

## 8. Open decisions, mentor feedback and stopping rule

| Still open | Resolution evidence |
|---|---|
| First recurring journey | Which repeated task justifies remembering? Specify normal/changed/ambiguous/forgotten outcomes and unacceptable failures. |
| Preparation/Part One | Applicant verifies product use and independent writing/order; disclose actual AI use. |
| UI/API and retention UX | Choose around a useful journey and shared core. Define automatic/ignored/uncertain/sensitive examples, retention/no-personalization and controls understandable without database administration. |
| Import/schema/configuration | Freeze validated fields/migrations before corpus creation; unfamiliar logs must import without invented metadata or repair. |
| NVIDIA/DeepSeek deployment | Verify exact ID, output/tool support, limits, retries, usage, account access and latency. |
| Embeddings/typed memory/relationships | Measure benefit over source baselines, multilingual evidence coverage and cold/warm RAM/cost/latency; require support for identity merges/state changes. |
| Artifact and recovery scope | Select the one output that earns adding an effect; define essential recovery guarantees. |
| Targets/test tools/packaging | Ratify proposed quality/retrieval/usage targets on development before sealing; pin compatible tooling and prove a clean checkout. |

Mentor feedback should identify the smallest valuable journey, unacceptable failures, and three observations that justify expanding the first slice. Discuss whether the user can verify/correct without maintaining the memory system, which questions need exhaustive evidence, what gain earns complexity and what should be cut. Use the [build/feedback image](mentor-svg/images/15-build-order-and-mentor-feedback.svg), [reviewer image](mentor-svg/images/14-reviewer-setup-and-submission.svg) and [evaluation image](mentor-svg/images/13-corpus-evaluation-and-quality.svg).

Stop architecture review when blocking contract contradictions are resolved and uncertain choices have explicit experiments/change gates. Implement smallest complete path → applicable integrity/development cases → diagnose failing layer → one justified change → affected checks. Once required checks/declared targets pass, freeze and assess sealed cases; sealed-informed fixes need a new holdout for fresh generalization claims. If alternatives are indistinguishable, keep the simpler one and disclose uncertainty.

For a new chat/machine, read README, the single SVG and this plan; use ARCHITECTURE for contracts and RESEARCH for rationale. Preserve user choices and validation limits, inspect actual code before claiming progress, and resume at the first incomplete dependency instead of restarting research or treating diagrams as a product.