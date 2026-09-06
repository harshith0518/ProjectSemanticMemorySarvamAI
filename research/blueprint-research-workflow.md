# Blueprint research: service contracts and durable request execution

Reviewed 6 September 2026 against `END_TO_END_DESIGN.md`, `design-review-harness.md`, `design-review-evaluation.md`, and the earlier harness notes. Planning only: proposed contracts, no application implementation, installation, API calls, or measured results. This reads selected public author material and documentation, not entire commercial books.

## Decision and research basis

Keep one Python process, SQLite, and one worker initially. Separate the request coordinator, memory service, model adapter, and tool executor through ordinary interfaces. A durable jobs/operations ledger supplies the limited recovery needed for this prototype; adding Temporal or LangGraph is not necessary simply because the system contains an LLM.

The workflow/agent distinction remains useful: fixed orchestration handles invariants, while the model can select further evidence within a bounded loop. Anthropic's newer Managed Agents article reinforces separating durable session state from the replaceable model loop and execution tools. Apply that interface separation locally; its cloud infrastructure and performance figures do not transfer to Kivi. [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), [Managed Agents architecture](https://www.anthropic.com/engineering/managed-agents)

Durability does not establish exactly-once external effects. Temporal explicitly describes Activities executing more than once when completion is not recorded; idempotent effects and recorded outcomes remain application responsibilities. LangGraph separately identifies run checkpoints and cross-run stores: a checkpoint is not a complete semantic-memory implementation. [Temporal Activity definitions](https://docs.temporal.io/activity-definition), [Temporal workflow recovery](https://docs.temporal.io/workflow-execution), [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)

## 1. Stable service boundary

Names below are contract notation, not implemented Python functions. `Context` comes from the trusted application boundary and supplies user identity, permitted scope, request ID and actor kind. Models cannot choose these values. Every mutation accepts an operation key plus a canonical payload fingerprint; repeating a key with different arguments returns `IDEMPOTENCY_CONFLICT`.

| Contract | Required request data | Required result |
|---|---|---|
| `accept_turn` | Context, client request key, current text, session, supplied timestamp/timezone | Run/source IDs, accepted sequence, persistence status, ordinary-learning job state |
| `import_records` | Context, stable upstream IDs/revisions, raw/formatted pair, metadata | Per-record imported/no-op/rejected outcome, reasons, source revisions and jobs |
| `search` | Context, query, optional topic/entity/time filters, evidence budget | Evidence bundle, current/conflicted/historical status, scope/cutoff, source revisions, truncation and readiness |
| `read_evidence` | Context, permitted source references and bounded span/window | Exact eligible source text, offsets, provenance, revision and access status |
| `inspect_memory` | Context, memory ID | Current allowed revision, history, evidence, decisions and lifecycle status |
| `apply_controls` | Context, run/operation key, ordered normalized controls, expected target revisions | Committed/no-op/needs-input/conflict/rejected/failed receipt; affected IDs; new generations; whether dependent output must refresh |
| `admit_candidates` | Worker context, job/attempt ID, source/extractor versions, candidates, expected control/target revisions | Per-candidate accepted/duplicate/updated/conflicted/rejected/no-op decisions; committed revisions and follow-up jobs |
| `get_processing_status` | Context, import/run or source set | Ready/pending/failed/excluded counts separately for lexical, extraction and dense stages |
| `process_pending` | Worker context, bounded source set/stage/configuration | Durable progress and terminal/pending errors; runnable both from CLI and background worker |
| `get_run` / `resume_run` | Context, run ID, expected run revision, optional clarification/approval response | Current status or resumed state; eligible retained answer; action receipts; processing/error details |
| `cancel_run` | Context, run ID, expected revision | Cancellation intent and actual stoppage status; dispatched effects remain separately tracked |
| `accept_response` | Coordinator context, run revision, buffered answer, evidence dependencies, action receipts | Accepted response/sequence or stale/cancelled/rejected; no second unvalidated content copy |

Keep `apply_controls` and `admit_candidates` separate. Explicit user controls and model-derived background interpretations have different authority. Neither accepts raw SQL. Search results use a `FreshnessToken` identifying user scope, control/exclusion generation, source high-water mark and relevant source/memory revisions. The canonical store owns these values; the model cannot mint a fresh token.

No generic public `delete_anything` or `update_memory_json` tool is needed. Model-accessible read tools can wrap `search`, `read_evidence`, and a bounded timeline operation; mutations pass through dedicated validated service contracts.

## 2. Model proposals versus authoritative events

Use one versioned structured envelope per model response:

```text
TurnProposal
  schema_version
  controls[]: Remember | Correct | Forget
  next: Answer | Read | ProposeAction | Clarify | Abstain

Answer: text, claims/evidence_refs, answer_status
Read: named_operation, bounded_arguments, evidence_gap
ProposeAction: registered_tool, proposed_arguments, relevant_evidence_refs
Clarify: question, missing_field, optional_safe_fallback
Abstain: reason_code, optional_supported_partial_answer

Control proposal: type, target_refs, scope, replacement_or_exclusion,
                  current_request_evidence, change_vs_correction
```

`controls` plus `next` handles "correct my budget and prepare a draft" in one call. `next` is a discriminated union: the model cannot ambiguously request final publication and unexecuted work simultaneously. `Answer` is provisional until all detected controls succeed and its dependencies remain valid. A `ProposeAction` does not authorize or execute the action. The initial scope supports one external effect per request; compound external workflows are a later feature.

The coordinator, not the model, emits `TurnAccepted`, `ControlApplied`, `ControlNeedsInput`, `ReadCompleted`, `ActionPrepared`, `ActionDispatched`, `ActionObserved`, `ResponseAccepted`, and failure events. These events contain observable state and concise reason codes; hidden chain-of-thought is not required. A model-supplied `ToolSucceeded` or `MemoryApplied` field is invalid protocol output.

For model errors, permit one structured repair or transient retry within the request's total budget. Reject unknown operations/fields and invalid references. A valid source span still does not prove semantic entailment or reveal a correction the model failed to detect. The model adapter should normalize supported native tool/structured output into this protocol; verify the chosen DeepSeek endpoint rather than assuming every compatibility feature works.

## 3. Exact request loop and call bounds

1. Accept input and create the run transactionally. Direct CLI/UI controls with explicit targets call `apply_controls` without a model.
2. Perform scoped initial retrieval; include the current message and relevant working context. Existing knowledge can be stale relative to explicit information in this message.
3. Make one answer-model call returning `TurnProposal`. No mandatory preceding classifier or comprehensive extractor.
4. Validate and apply detected controls first. If a control is unresolved or fails, block dependent actions and success acknowledgments. Keep independent useful preparation possible with an honest partial result.
5. If `next` remains valid, answer or execute its bounded read/action path. If a control changed material evidence, refresh retrieval and regenerate as necessary. Already committed controls return their receipt on repeated proposals.
6. Accept the buffered response only after fresh dependency, exclusion, run-cancellation and action-state checks. Persist the answer and terminal outcome in the same short acceptance transaction, then return through the ordered publication path.

Suggested starting circuit breakers: at most four total answer-model attempts per request, including repairs and retries; six follow-up read operations beyond initial retrieval; one external effect; one retry per eligible transient provider call; and a 30-second ordinary request deadline. These are local defaults to verify before sealing, not vendor guarantees. A tool whose work legitimately continues beyond the response deadline returns an observed pending/unknown state rather than being described as failed or completed. Deadline expiry does not itself cancel an external effect.

An ordinary supported answer targets one model call. Background extraction has a separate budget and usage ledger. Additional evidence and action results consume additional calls. If the budget expires without a valid buffered answer, return a deterministic partial/error response from observed receipts; do not invent a final success or start an unbounded last attempt.

## 4. Learning readiness, CLI and UI

Historical import uses persisted jobs directly. For live turns, create the learning job initially as `held_for_controls`: ordinary extraction must not race a current remember/correct/forget decision. Release it after the first valid proposal's controls resolve or a safely finalized request establishes its permitted remaining content. A model failure leaves it held/retryable; do not silently extract a possible forget request. If a control mentions the forgotten information, its source and copied traces must obey that exclusion too.

This hold does not delay the current answer's access to its own message. It also does not guarantee natural-language control detection: missed-control probes remain necessary. Until admitted for history use, a live source stays available only to its current request; it should not enter unrelated long-term source fallback prematurely.

The CLI's `process --resume` drains the same durable job functions to a specified watermark and reports failed/pending items. The UI can return an accepted run ID immediately, display processing state, and poll or subscribe to service events. HTTP disconnect is not an instruction to repeat input or silently cancel an already dispatched action. Resubmitting the same request key retrieves the existing run.

Keep final answer text buffered initially. UI progress can show processing stages without exposing unaccepted answer content. Reconnection must call `get_run`, which rechecks current access/exclusion state; after forgetting, even idempotent response replay returns a redacted/suppressed retained result instead of the original text.

## 5. State machines and atomic operations

Avoid a single overloaded status field. Keep overall run status separate from operation outcomes:

```text
Run:
  accepted -> running -> waiting_input -> running
  running -> completed | partial | failed | cancelled | outcome_unknown

Learning job:
  held_for_controls -> queued -> running -> succeeded | no_op | excluded
  running -> retry_wait -> queued
  running -> failed              # bounded attempts exhausted
  stale completion -> discard/requeue against a new expected revision

Action:
  proposed -> waiting_approval | ready | rejected
  ready -> dispatched -> succeeded | failed | unknown
  unknown -> reconciling -> succeeded | failed | unknown
  proposed/waiting_approval/ready -> cancelled
  after dispatch: cancellation_requested is an intent, not proof of rollback
```

`outcome_unknown` can terminate the conversational run while the distinct operation remains reconcilable. `waiting_input` is not a failure or authorization; resumption checks the run and prepared-argument revision. No request resumes forever simply because new context exists.

Recommended atomic DB operations:

| Transaction | Together inside the short transaction |
|---|---|
| Input acceptance | Deduplication key/payload check, source and run creation, source visibility, held/queued job |
| Control batch | Validate every target/revision; commit the normalized compatible batch or none; revisions/exclusions, source eligibility, projections/index cleanup, audit receipt and generation increment |
| Candidate admission | Check lease/attempt/source/control versions; accepted memory/evidence/link/FTS changes, decisions and embedding jobs |
| Embedding completion | Verify expected revision/configuration/exclusions; vector write and job completion |
| Action preparation | Persist exact arguments, authorization reference, target version and stable operation key |
| Dispatch admission | Recheck controls/authorization/target version; compare-and-set ready to dispatched; record attempt/correlation ID |
| Action observation | Persist verified result and operation state, tool-source record, optional learning job from permitted tool evidence |
| Response acceptance | Fresh eligibility/run checks; answer, acceptance sequence and terminal run outcome |

Perform model calls, embedding computation, and external effects outside DB transactions. For a compatible multi-control batch, validate the whole batch before changing anything; conflicting instructions need resolution. This is a narrow local transaction, not an atomic promise spanning a tool effect. Logs and derived indexes can remain synchronized here without a distributed streaming platform. [Kleppmann's database/dataflow explanation](https://martin.kleppmann.com/2015/03/04/turning-the-database-inside-out.html)

The dispatch-admission commit is an explicit ordering boundary. A later cancellation cannot guarantee prevention of an effect already dispatched. Likewise, response acceptance is ordered against control commits but cannot retract network bytes already delivered. Failed persistence must not be followed by an unrecorded irreversible action.

## 6. Failure semantics for controls and tools

**Correction:** a stale target revision returns conflict and fresh target data, rather than overwriting another correction. Preserve genuine historical change separately from correcting erroneous evidence. A storage failure leaves the old durable state unchanged; the current message can still inform an independent draft, accompanied by an honest unsaved-update status.

**Forgetting:** return separate fields for `use_block_committed`, exact affected scope, `source_retained`, and `purge_status`. If immediate exclusion commits but slow derivative cleanup remains, say use is blocked and cleanup is pending. Never claim full removal while copies remain inside the promised deletion boundary. For this small SQLite prototype, prefer completing database-content/index cleanup in the control transaction. External originals, exported user files and provider retention remain explicitly separate boundaries. If exclusion cannot commit, report failure and do not continue a dependent operation using the targeted material.

**External action:** a transport timeout, process crash after dispatch, or missing response is `unknown`, not known failure. Reconcile by provider receipt/idempotency key or verified readback before retry. Local operation IDs do not create remote idempotence. A stable destination/path plus expected digest supports reconciliation for the first local-artifact capability; do not overwrite changed content merely to make a retry succeed.

MCP task support is negotiated and remains experimental in the checked 2025-11-25 specification. Where supported, retain the remote task ID and poll interval, fetch the result, and map observed states into the operation ledger. Do not assume every tool supports tasks. Task TTL expiration or a missing task ID does not prove no side effect occurred. MCP tool result validation and authorization remain necessary independently of task polling. [MCP tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks), [MCP tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)

## 7. Evaluation convergence and additional probes

Retain the existing 80-probe, 30-development/50-sealed protocol and its declared gates; this note does not introduce another competing question count. Separate planning, tool choice/arguments, execution, and efficiency failures, as Huyen recommends. Define the product's errors and constraints before adjusting architecture. [Huyen: agent failure modes](https://huyenchip.com/2025/01/07/agents.html#agent-failure-modes-and-evaluation), [Huyen: system-design process](https://huyenchip.com/machine-learning-systems-design/design-a-machine-learning-system.html)

Add these deterministic acceptance probes to the relevant service checks, not as replacements for language-understanding evaluation:

1. Same operation key/same payload repeats its committed result; changed payload returns conflict.
2. Response retry/reconnection after forget cannot re-emit the original retained answer.
3. Live-turn learning cannot run before a detected forget/correction resolves; the control's own text cannot recreate forgotten material.
4. One proposal contains correction plus action: the action dispatches only against the committed correction. Failed correction blocks the dependent effect.
5. An incompatible multi-control batch changes nothing; valid prior independent operations remain accurately reported.
6. Two corrections race on one revision: one wins; the stale operation conflicts rather than silently overwriting.
7. Crash after control commit/before response: resume returns the control receipt without applying it twice.
8. Crash after external effect/before observation: outcome stays unknown until reconciliation; no automatic duplicate.
9. Fake model success fields, malformed union output, changed tool arguments after approval, or an unknown tool are rejected.
10. Stale worker/lease completion after a newer attempt or exclusion cannot commit.
11. Cancel/disconnect/reconnect cannot publish a late canceled answer; cancellation after dispatch remains honest about effects.
12. Budget exhaustion and unavailable models produce a truthful partial/failure result with all attempted calls counted.

Before sealing, stop optional architecture exploration once required service invariants pass, the candidate meets the declared development quality/latency targets, and remaining errors have no demonstrated component-level fix worth its cost. Permit only bounded experiments tied to observed failures; inconclusive results select the simpler implementation. Freeze prompts, models, corpus, extraction materialization and numerical gates before the sealed run. Fixing sealed failures turns that suite into regression material, requiring a fresh holdout for a new generalization claim.

Budget warning: the existing maximum plan consumes 314 of 320 reader attempts before most multi-call/retry overhead. Profile actual calls on development first. Omit the optional third sealed comparator or reduce optional development work before exhausting the cap; do not skip difficult sealed cases. If the study remains incomplete, report incomplete results rather than relaxing the gate.

After the locked evaluation, rerun only checks affected by subsequent changes plus required end-to-end UI journeys. Passing tests is a stopping condition for that iteration, not proof of universal correctness. The final product still needs its normal-user interface, evidence inspection, controls, repeatable evaluation and reviewer instructions; optional agent autonomy must not displace those requirements.
