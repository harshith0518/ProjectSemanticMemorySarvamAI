# Hey Kivi — consolidated architecture and project plan

Updated: 6 September 2026. Document revision: **1.1, conversation consolidation**. Technical baseline: the reviewed v1 memory design. Status: **ready for product refinement and implementation; application not built**.

This is the single starting reference for continuing the Golden Goose project. It consolidates the decisions, explanations, constraints and unresolved choices from this conversation, the assignment brief, and the saved research. It supersedes older planning notes where they differ. Research files remain supporting evidence, not additional competing plans. A finalized starting contract is not a claim that the system is optimal or already works.

**Status language:** “user choice” records an explicit preference; “baseline” is our current engineering plan; “candidate/proposed” needs validation or a product decision; “implemented” is reserved for code that exists. At this point, only a research-only SQLite contract probe exists. The product CLI, migrations, corpus, model integration, semantic evaluation and final interface do not exist yet.

**Reading route:** product and scope in section 0; tech stack in section 2; categories and storage in sections 3–4; input-to-output behavior in sections 6–9; caching in section 10; import/configuration/tools in section 11; evaluation in section 12; submission and next decisions in sections 15–17. The core plan is contained here; following research links is optional for deeper justification.

## 0. Product intent, assignment scope and user behavior

### 0.1 What we are building and why

The user chose **Golden Goose**, with **semantic memory for Hey Kivi** as the central engineering problem, after initially comparing it with the backend/phonetic-memory assignment. The motivation was broader learning and a more rewarding complete product. The earlier recommendation to choose backend is superseded. An initial two-day ambition makes scope discipline important; it is not a verified remaining deadline. Eligibility for multiple hiring tracks is separate from this technical plan and is not established by this document.

The recurring need expressed in the conversation is to recover useful past information without repeating or manually searching it, then use that information in the current request. The proposed abilities are:

| Ability | Ordinary request | What makes it useful |
|---|---|---|
| Recover | “What did I promise to send Riya?” | Finds evidence even when the user does not remember the original wording |
| Connect and understand changes | “What changed about our Jaipur plan?” | Combines records while separating earlier plans, current information and unresolved questions |
| Apply relevant context | “Prepare a short checklist using our budget and preferences.” | Turns recall into a useful answer or draft |
| Inspect and control, across all three | “Where did that come from?” / “That changed.” / “Forget it.” | Makes assistance understandable and correctable |

“Best memory,” low latency, good architecture and an attractive interface are quality goals. The first concrete user journey still needs to be selected and refined. The examples here explain technical behavior; they are not the applicant's Part One positioning statement or vision.

An **ability** is an outcome for the person; a **tool** is an executable operation; a **skill** is a reusable way to combine operations. Summarizing, comparing and drafting can be model behavior over retrieved evidence. They do not require three separate tools, a plugin marketplace, a roles hierarchy or a separate skills framework.

### 0.2 Kivi, Sarvam and the two modes

Sarvam is the company; Kivi is its voice-first computing product. The assignment describes regular dictation and direct Hey Kivi requests. Our submission is a separate working demonstration of the chosen memory experience, with its own backend and interface.

| Boundary | Regular dictation | Hey Kivi in this project |
|---|---|---|
| User intention | Write what the person says | Understand a request and help complete it |
| Personalization | Names/terminology, spelling, style and formatting | Relevant history, preferences, decisions, episodes and constraints |
| Memory role | Can supply historical observations for later learning | Retrieves and applies relevant understanding |
| Content behavior | Preserve intended content; do not insert unsolicited personal history | Answer, explain, prepare a draft or execute an authorized implemented tool |

Phonetic memory concerns how personal words should be recognized/written. Semantic memory concerns durable meaning and context. We are not implementing a phonetic-learning or speech-recognition pipeline in this scope. Raw ASR and formatted text are inputs to our history system; their difference alone does not prove a preferred spelling or a personal fact.

The brief's long-term direction permits dictation to become a tool inside Hey Kivi. It does not require us to recreate the entire current Kivi product. Public sources reviewed earlier showed dictation, vocabulary/style behavior and selected-text assistance. A native app walkthrough and a built-in chat/project workspace were **not verified**. Our memory design does not depend on such a workspace existing. Application name is not project identity. [Kivi public product page](https://heykivi.ai/)

### 0.3 What the assignment actually requires

The authoritative source is the [Golden Goose brief](../Kivi_Golden_Goose_Task_Final.pdf), pages 2–7. The user's learning notes PDF was reviewed against it and is not a replacement specification.

- Part One asks for the applicant's independently formed and written position, at most 100 words, and vision, at most 600 words, preserved before Part Two. It explicitly excludes generative AI from arriving at or writing that position. Completion of those documents has not been established here. This AI-assisted technical plan must not be represented as independently authored Part One work, and prior AI use must be described honestly.
- Part Two requires one real end-to-end product with a normal-user interface and backend. **CLI first is our development sequence; CLI alone is not the final submission.** A notebook, static mockup or architectural proposal is insufficient.
- No speech recognition or production Kivi integration is required. Import/replay text records containing raw ASR output, formatted output and available metadata. A typed Hey Kivi question is sufficient input.
- Create or obtain **approximately 500 history records**, then evaluate the complete pipeline. This is not a requirement for 500 test cases. Reviewers later import a separate approximately 500-record corpus from one user.
- Questions may ask anything reasonably stated in or derivable from that history, including multiple-record and temporal reasoning. Narrow tool scope does not justify hard-coding a narrow list of answerable questions.
- Missing metadata, languages, project IDs and exact future evaluator questions are unknown. Preserve missingness. English/Hindi/Hinglish coverage is our proposed test scope, not a guaranteed hidden-corpus format.
- A local web/desktop application is acceptable. Deployment and Docker are optional. The exact clean-checkout review path and generated results are required; section 15 lists the deliverables.

The proposed review arrangement is a local application/database connected to the hosted model API. Local storage does not mean offline model processing: eligible context is sent to the configured provider. One LLM key can be enough when embeddings run locally; account quota, prices and endpoint support must be checked during development.

### 0.4 Personalization, uncertainty and user control

The person should not have to classify memories, approve every extraction, merge graph nodes or maintain technical settings. Kivi organizes routinely; the person can inspect, correct, override and forget through ordinary language and simple controls. A developer inspection view is an additional review surface.

Current explicit instructions take precedence over applicable remembered preferences for this request. Using an old preference must not silently make it a new universal rule. A retrieved memory is used only when it helps the current task; it need not be announced. For example, a brevity preference can shape an answer without a personal callback.

| Situation | Proposed user-facing behavior |
|---|---|
| Enough evidence | Answer directly and make sources inspectable |
| Uncertain detail is unnecessary | Omit that detail and complete the supported portion |
| Two interpretations are useful to show | Explain the alternatives; a reversible draft may use a clearly labeled assumption |
| Missing detail materially changes the answer | Ask one focused question and give a supported partial answer when possible |
| Action lacks a material recipient, path, time or authority | Prepare what can be prepared; hold the dependent effect |
| History does not support an answer | Explain what is unknown; do not invent an answer |
| User skips clarification | Preserve uncertainty and take the supported fallback; skipping is not confirmation |

Background learning does not interrupt the user for every ambiguity. Preserve unresolved mentions and revisit them when a request needs the distinction. A model's self-reported confidence percentage is not a calibrated decision threshold. [Clarification research](https://aclanthology.org/2025.findings-naacl.306/)

Useful boundary examples from the discussion:

- “I visited Paris” supports a visit, not enjoyment, a year, a preference for France or an intention to return.
- “I want to visit Paris” is an intention; “my sister visited Paris” concerns the sister; a fictional draft is not a personal event.
- A postponed trip does not automatically prove an associated meeting was rescheduled. A manager's identity does not automatically establish who must review an unrelated document.
- Remembering a document's location does not establish access to its contents. An old “send this” dictation is historical evidence, not current execution authority.

Exact onboarding language, retention/no-personalization controls and which of these behaviors lead the final UI remain product-refinement work. The technical correction/forgetting boundaries below are already part of the baseline.

## 1. Where semantic memory is

**Semantic memory is the `MemoryService` subsystem and its durable knowledge records. SQLite is its initial storage engine.** It is a separate logical component inside the application, not a mandatory separate server or database.

```mermaid
flowchart TD
  U[CLI first; user interface later] --> R[Request coordinator]
  R <--> L[DeepSeek model adapter]
  R <--> M
  R <--> T[Controlled tool executor]
  subgraph M[MemoryService — the semantic-memory subsystem]
    A[Admission: interpret and validate knowledge]
    B[Knowledge: facts, episodes, evidence and revisions]
    C[Relationships: entities, aliases and links]
    D[Recall: keyword, vector and relationship retrieval]
    E[Controls: remember, correct, forget and inspect]
    A --> B
    B --> C
    C --> D
    E --> B
  end
  M <--> DB[(One SQLite database)]
  W[One learning worker] --> M
  W <--> L
  DB --- S[Original history and permitted text projections]
  DB --- I[Search indexes and persisted vectors]
  D <--> RAM[Loaded encoder and optional revision-checked RAM views]
```

The model interprets language. The memory service preserves and retrieves attributed knowledge. The coordinator controls request order. The tool executor performs permitted effects and records observations. A table, graph, map and vector are compatible representations with different jobs:

| Representation | Use in v1 |
|---|---|
| Relational tables | Durable sources, memories, evidence, controls, jobs and operation outcomes |
| Graph | Supported entity-to-entity links stored in tables; bounded traversal |
| Map/dictionary | Optional fast lookup by known ID/key during a running process; reconstructed from the database |
| Vectors | Meaning-based retrieval candidates derived from permitted text; stored in SQLite and scored locally |
| Working context | The current request, relevant conversation and retrieved evidence assembled for one run |
| Cache | Reusable computation with explicit validity rules; never the sole copy of knowledge |

This boundary follows the distinction between memory content and retrieval technique; semantic memory is not synonymous with semantic search. [LangChain memory concepts](https://docs.langchain.com/oss/python/concepts/memory)

## 2. Locked starting choices and measured alternatives

“Locked” means the current starting choice, subject to an explicit evidence-backed revision. It does not mean installed, benchmarked or impossible to change.

| Layer | Technology / approach | Decision status |
|---|---|---|
| Application language | Python; 3.12 is the available development-runtime family | Baseline; packaged runtime/version pin still needed |
| Request orchestration | Small custom coordinator, `MemoryService`, one durable worker and tool registry | Baseline; no full agent framework selected |
| Durable storage | SQLite through standard-library `sqlite3`, parameterized SQL and versioned migrations | Baseline; product schema/migrations not implemented |
| Exact-text search | SQLite FTS5 | Baseline; available in the research runtime |
| Meaning-based search | `sentence-transformers` + local embeddings + NumPy exact scoring | Planned separable extension; benchmark before default use |
| Embedding model | `intfloat/multilingual-e5-small`; compare `BAAI/bge-m3` only if useful | Candidates; no local accuracy/speed result yet |
| Language model | NVIDIA-hosted DeepSeek via a configurable adapter | User choice of provider/model family; exact model ID and behavior pending |
| Model/API client | HTTPX, with explicit timeouts, bounded retries and usage capture | Baseline |
| Data and model-output contracts | Pydantic plus application validation | Baseline; schema validation does not establish factual truth |
| CLI / persistent session | Standard-library `argparse` and a REPL | Baseline; CLI not yet written |
| Relationships | Entity/alias/edge tables in SQLite | Baseline representation; bounded expansion measured separately |
| Reuse / cache | Persist document vectors; retain loaded encoder; optional checked RAM views | Baseline policy; answer/result caching disabled initially |
| Tool connectivity | Narrow local tool adapter first; MCP adapter when a chosen use case needs it | Local artifact is the first proposed effect; MCP integration deferred |
| Evaluation | Custom corpus replay, evidence/rubric scoring, metrics and integrity checks | Planned; product test runner/library not selected |
| Final UI and HTTP/application adapter | Usable web or desktop client calling the same core | Required later; frameworks **not selected** |
| Packaging and review | Reproducible local setup with hosted LLM access | Proposed primary arrangement; Docker/hosting optional |

FastAPI, React, pytest, Redis, Neo4j and a hosted memory framework are not silently implied dependencies. The final UI framework and API adapter will be selected with the user journey; adding them must not create a second memory implementation.

Start with one Python application process, one SQLite file on local storage, and one worker. Use Python `sqlite3`, FTS5, Pydantic for validated contracts, HTTPX for the provider adapter, and standard `argparse` for the first CLI. Dense retrieval is a separable feature using `sentence-transformers`, a pinned multilingual encoder and NumPy exact scoring. E5-small is the first encoder candidate, with BGE-M3 a larger comparator. Pin exact dependency/model revisions during development after compatibility checks; these libraries are not all installed yet. [Pydantic validation](https://docs.pydantic.dev/latest/), [HTTPX timeouts](https://www.python-httpx.org/timeouts/), [E5-small](https://huggingface.co/intfloat/multilingual-e5-small)

Use NVIDIA-hosted DeepSeek behind a provider interface; credentials arrive during product development. Verify actual model name, context length, structured-output behavior, reasoning-token limits and tool support. Endpoint compatibility does not guarantee all features. Keys stay outside memory and traces.

Retain full-history and source-only retrieval as real baselines. Start implementing with source storage and lexical retrieval; selectively add typed memory and vectors. The semantic service includes controls, provenance and durable interpretation even if a simple source route wins some query classes.

Do not add a graph server, dedicated vector server, Redis, autonomous reflection, recursive summary tree or workflow platform in v1. Reconsider PostgreSQL/pgvector for multi-host or substantial concurrent-writing requirements; a graph engine for a measured traversal limitation; and approximate vector indexing for a measured exact-scan bottleneck. SQLite supports graph queries and many readers with one writer. A future database migration must revisit isolation/retry contracts. [SQLite use cases](https://sqlite.org/whentouse.html), [SQL graph traversal](https://sqlite.org/lang_with.html), [pgvector](https://github.com/pgvector/pgvector)

## 3. Categorization without disconnected silos

Every memory has independent axes. The model cannot infer scope or authority from a category alone.

| Axis | Values/contract |
|---|---|
| Memory form | Semantic knowledge, episodic experience, or a user-authorized reusable procedure |
| Content category | One primary label from the registry below; optional secondary labels |
| Subject and attribution | Who the claim concerns, who stated it, and whether it reports a user, third party or tool observation |
| Derivation | Direct attributed statement, tool observation, inference or summary; derived items retain dependencies and are not independent corroboration |
| Modality and polarity | Separate actuality/intention/commitment, conditional context and positive/negative proposition; preserve nested attribution rather than forcing everything into one label |
| Topic | Overlapping labels such as travel, family and work; not a retrieval access boundary |
| Scope | Person, project, trip, task, conversation or time-limited applicability; missing scope stays unresolved |
| Time | Event/validity time, source/capture time and availability/import time remain distinct |
| Evidence and lifecycle | Supporting exact spans; active, disputed, superseded, excluded; revision history |

The twelve categories are **labels on records in shared memory tables**. They are not twelve databases, twelve required tables or twelve isolated search routes. A single message can support multiple atomic memories, each with one primary category and optional secondary labels.

| # | Category | Contents / example | Boundary to preserve |
|---|---|---|---|
| 1 | Entities, attributes and stated capabilities | People, organizations, equipment, location, skills: “I use Windows.” | A claimed capability is attributed; the system has not independently tested it |
| 2 | Relationships and roles | Family, teams, ownership and responsibilities: “Riya is my sister.” | A shared name does not identify a person; roles apply within supported scope |
| 3 | Preferences and priorities | Likes, dislikes, response style, stated tradeoffs: “I prefer short updates.” | Preserve preference strength and context; do not silently turn a preference into a hard requirement |
| 4 | Constraints and requirements | Budgets, limits, necessary conditions: “Total hotel budget is INR 6,000.” | Preserve units and trip scope; total is not per night |
| 5 | Routines and recurring patterns | Usual activities or timing: “I review expenses on Sundays.” | A few observed instances do not prove a routine or an automatic reminder |
| 6 | Goals and desired outcomes | Aspirations or intended outcomes: “I want to learn Python.” | A goal is not a scheduled task or a promise |
| 7 | Plans, tasks and commitments | Tentative plans, intended actions, assignments, promises, with distinct subtypes | “Might visit,” “plan to visit” and “promised to book” do not establish completion |
| 8 | Decisions and explicitly stated reasons | Chosen option and supplied rationale: “We chose SQLite for local setup.” | Do not invent reasons or treat an unaccepted suggestion as a decision |
| 9 | Progress, blockers and open issues | Work state, dependencies, pending questions | A task being completed is distinct from a memory being superseded |
| 10 | Attributed beliefs, ideas and hypotheses | “Riya suspects the deadline will change.” | Record who believes what; belief is not confirmation of its proposition |
| 11 | Personal vocabulary and concepts | “Phoenix means our migration project.” | Meaning/reference resolution differs from phonetic spelling correction |
| 12 | Resources and references | Files, links, documents, useful artifacts and locations | A remembered reference does not establish current contents or permission to open it |

The registry and predicate rules are versioned application policy. The LLM may select categories and suggest overlapping topics such as travel/work/family. It may not rewrite the schema, SQL, policy or permissions. Optional secondary-label storage can be normalized or use validated JSON; that physical encoding is a migration-level choice, not twelve separate stores. Extend the registry only for a demonstrated recurring need; unfamiliar permitted text stays searchable without forced classification.

These are overlapping product labels, not a scientifically exhaustive partition. “Facts” is an umbrella. An attributed belief is knowledge that someone holds a belief, not proof that its proposition is true. A date does not automatically make a memory episodic. Unclassified permitted source material remains searchable. Categories are extraction/browsing aids; the system never routes a question exclusively to one category.

For example, a source stating “For the Jaipur trip, our total hotel budget is INR 6,000” supports a semantic constraint with trip scope, currency INR and total-budget meaning. It does not establish a nightly budget or a general spending limit. Represent the amount structurally while retaining the original phrase and evidence. A procedural instruction mentioned inside a document remains document content unless the user actually authorizes it as Kivi behavior.

Semantic knowledge, episodic experiences and authorized reusable procedures are independent **memory forms**. An episode may be an ordinary meeting, visit or attempted task. Working memory is the temporary context for the current request. The assignment uses semantic memory broadly enough to discuss factual, episodic and preference-level understanding; our schema retains the distinctions. Topics and recency do not form a mandatory hierarchy or a retrieval access boundary. [CoALA memory framework](https://arxiv.org/html/2309.02427v3#S4.SS1)

## 4. Durable schema and authority

The tables below are a logical implementation contract, not executed SQL DDL. Field nullability, check constraints, physical indexes, supported predicate definitions and exact migration files still need implementation and tests. Their authority, evidence, revision and scope rules must be preserved during that work.

All primary/foreign keys that cross user data include trusted `user_id`. User scope is supplied by the application, never the model. IDs are opaque. Use parameterized SQL. Enable foreign keys on every connection. Revisions are logical integers; they are not timestamps.

| Table/group | Required logical fields and constraints |
|---|---|
| `owner_state` | `user_id` PK; `knowledge_rev`, `index_rev`, `publication_seq` |
| `record_revisions`, `record_heads` | Composite key `(user_id, record_id, revision)`; role/origin, kind, exact raw/formatted fields or message text, source metadata, availability, visibility, content digest. A head pointer defines the current source revision; historical access explicitly selects a permitted revision. |
| `memory_revisions` | Composite key `(user_id, memory_id, revision)`; form/category, subject or unresolved mention, speaker/reporter/belief-holder attribution, derivation/dependencies, predicate, one typed object/value with units, scope, modality, polarity/condition, qualified time, assertion state, prior-revision links |
| `memory_heads` | Current revision pointer per memory identity; current does not mean universally true or applicable |
| `evidence` | Composite FKs to exact memory and source revisions; field, start/end offsets, support/contradiction role |
| `entities`, `aliases`, identity decisions, `edges` | User-scoped identities; alias and identity decisions retain source/memory support and revisions. Edges reference supporting memory revisions and preserve attribution, modality, polarity, time and scope. A shared alias alone does not merge identities. |
| `exclusions`, permitted projections | Targeted source/field/spans or broader explicitly selected scope; revision and allowed-text representation/mapping |
| `search_documents`, FTS5, `embeddings` | Subject revision, permitted-projection digest, encoder/config version, vector dimension/normalization, readiness. Only current allowed representations are eligible. |
| `jobs`, `memory_decisions` | Stage/input/config identity; held/queued/running/terminal state, attempt fencing token, expected revisions, candidate decisions and concise reasons |
| `runs`, `run_attempts`, `operations`, `responses` | Logical request key/digest, active attempt and run revision/status, retained attempt outcomes, exact effect arguments/authority, observed receipts, answer dependencies and acceptance sequence |

**Storage example.** One input says: “Riya is my sister. For our Jaipur trip, the total hotel budget is INR 6,000. For this trip, I prefer quiet hotels.” Store that original once, then accept separate supported assertions:

| Illustrative memory | Primary category | Typed meaning and scope | Evidence |
|---|---|---|---|
| M1 | Relationships and roles | User has sister Riya | Exact relationship phrase in the source |
| M2 | Constraints and requirements | Jaipur trip: total hotel budget, amount 6000, currency INR | Exact budget phrase in the source |
| M3 | Preferences and priorities | Quiet hotel preferred for this trip | Exact preference phrase in the source |

These are rows/revisions in the same memory store. Supported entity links connect the records; search documents and vectors help find them. The model sees a relevant evidence bundle, not unrestricted database access. M1–M3 are illustrative IDs, not existing data. The ambiguous word “our” does not itself establish that Riya is a trip participant.

Evidence offsets use zero-based Unicode code-point positions, end-exclusive, into the exact named original field. Normalization/transliteration/embedding chunks need mappings; their offsets cannot silently replace original offsets. Raw ASR and formatted text are paired representations of one observation, not independent corroboration. Preserve a material disagreement rather than selecting the more fluent version.

Ordinary source retrieval uses `record_heads` and the current permitted projection. An explicit historical revision or temporal replay must still pass today's exclusions and the evaluation's availability cutoff. Older source revisions cannot accidentally appear as extra corroborating records. Alias/identity support disappearing invalidates the decision and its dependent projections; rebuild conservatively from surviving evidence rather than keeping an irreversible merged identity.

Time has an original phrase, reference time/timezone when available, precision, and each interval bound marked `known`, `unknown` or `open`. A missing/unknown endpoint is not evidence of unrestricted validity. Task status such as completed/cancelled is a typed property distinct from assertion status such as active/superseded. A completed task can be a valid active assertion.

Use a small versioned predicate registry with subject/object types, units and cardinality within explicit scope and time. For example, a trip's total hotel budget can be single-valued for that trip and interval; preferences can be multi-valued. A second value becomes a replacement only when the supported change/correction establishes matching scope and temporal meaning. Otherwise retain alternatives/conflict. Unknown predicates/scopes do not trigger automatic overwrite. Keep the original statement alongside typed values.

For “Riya believes Ajay does not manage Project X,” preserve the reported belief holder and negative proposition. Do not project an unqualified positive management edge. Facts involving several participants may use an event entity with participant roles. Similarity/LLM-suggested associations, if later retained, are explicitly discovery hints and cannot serve as evidence-backed factual edges.

Original inputs and accepted user controls are durable evidence of what was expressed. Accepted memory interpretations are also retained and versioned: re-running an LLM need not reproduce them. Edges are projections of supported assertions. Search representations are rebuildable. Assistant output is conversation history, not independent proof of personal events. Tool evidence establishes what was observed at that operation/time, not arbitrary personal truths or fresh permission.

`knowledge_rev` advances whenever eligible evidence, admitted knowledge or controls change. `index_rev` advances when a ready search representation changes. `publication_seq` orders committed controls and accepted responses. Ordinary assistant-output logging does not automatically change knowledge. Per-source and per-memory revisions localize updates; a coarse knowledge revision provides a conservative response freshness check.

An ordinary correction can preserve source/history and supersede a current interpretation. A genuine real-world change and correction of an earlier mistake have different temporal meaning. Do not resolve ambiguous changes solely from last import time or embedding similarity. Multi-valued relationships/preferences may coexist; avoid a global uniqueness rule that forces one value per category.

## 5. One permitted-text boundary

Every model-facing history read uses `read_evidence`/`eligible_text`: lexical search results, vector candidate expansion, full-history baselines, source inspection, neighboring context, extraction and summaries. Raw-table access is not exposed as an agent tool.

The boundary checks trusted scope, source visibility/revision, exclusions and supported time constraints. It masks/omits excluded spans and returns a mapping to surviving original spans. If safe partial reconstruction is unavailable, exclude the entire affected chunk/record until rebuilt. Never use its old embedding to recover excluded meaning.

For live requests, the original source begins as `turn_private`: only the current run can use it. Its learning job is held. Before a forget is applied, the current run may read its current input; after controls, even private-current reads apply exclusions. A validated disposition releases only the surviving projection for general history/learning, never a fresh copy of raw text. A forget request repeating the targeted information must not become a new eligible source of it. Failed or unresolved control handling leaves learning held rather than silently promoting the source.

`forget` blocks future memory/model use of the selected information and known supporting spans; disclose whether original history is retained. `delete_source` removes the specified in-application source content and affected derivatives. Rebuild mixed-source memories only from surviving permitted evidence. Purge or suppress dependent prompts, candidate quotes, aliases, internal artifacts and retained answer copies within the selected boundary. Operation replay and `get_run` use the current projection too. User-owned exports, source files, backups and provider retention are separate boundaries; do not silently edit unrelated files or promise recognition of arbitrary future paraphrases.

## 6. MemoryService API

These names define the implementation contract; they are not existing commands or functions.

| Method | Input | Output |
|---|---|---|
| `import_history` | Trusted context, source envelope, stable import key | Source receipt and per-stage readiness; no external execution |
| `accept_turn` | Trusted context, request key, exact input | Run ID/revision; private source; held learning job |
| `retrieve` | Query specification, scope, time, evidence budget | Candidates, original spans, completeness/readiness and store-issued freshness token |
| `read_evidence` | Source refs/spans and trusted context | Current permitted text plus original-span mapping |
| `inspect_memory` | Memory ID/revision | Interpretation, evidence, decisions, history and control state |
| `apply_controls` | Ordered compatible controls, operation key, target revisions | Code-issued committed/no-op/conflict/needs-input/rejected/failed receipt |
| `delete_source` | Explicit source-deletion instruction, selected source IDs/revisions, trusted context and operation key | Use-block receipt, exact deletion scope, source-retention/purge status and affected dependencies; implemented through the same validated control transaction |
| `admit_candidates` | Job/attempt token, candidates, captured dependencies | Per-candidate decisions and committed memory/index-job revisions |
| `process_pending` | Bounded stage/source set and configuration | Durable progress, watermark, pending/no-op/failed counts |
| `get_run`, `resume_run`, `cancel_run` | Run ID/revision and any new authorized input | Current eligible result, actual operation state or cancellation intent |
| `accept_response` | Buffered answer, dependencies, actual action receipts | Committed answer/sequence or stale/cancelled/rejected outcome |

An idempotency key identifies one logical request/effect. Same key plus identical canonical payload returns its current receipt; same key plus a changed payload returns conflict. The application assigns operation IDs and freshness tokens. The model cannot invent success receipts, authoritative versions or a different user scope.

## 7. Model contract and exact request path

The provider adapter validates one versioned proposal:

```text
TurnProposal(version=1)
  controls: list[Remember | Correct | Forget | DeleteSource]
  next: Answer | Retrieve | ProposeAction | Clarify | Abstain

Each control: target references, scoped change, current-request evidence,
              change-vs-correction meaning where applicable.
Answer: provisional text, personal-claim evidence references, status.
Retrieve: registered read operation, bounded arguments, missing evidence.
ProposeAction: registered tool, proposed arguments, supporting references.
Clarify: missing field, question, permitted partial fallback.
```

`next` is one discriminated choice. The model cannot declare a tool succeeded or a memory was committed. The service produces receipts after actual state transitions. Validate syntax, unknown fields/operations, ownership, references and legal transitions. Quote/span validity does not prove factual entailment or detect a control the model failed to propose; those need semantic evaluation. Provide explicit correction/forget CLI/UI controls as a less ambiguous path.

1. **Accept:** persist the run, private current source and held learning job. Explicit CLI controls with IDs can bypass language interpretation.
2. **Read:** gather a coherent snapshot from both memory and original-source routes. Add the current input and relevant recent conversation. Close read transactions before model calls.
3. **Interpret:** make the first answer-model call. No mandatory separate classifier and no comprehensive extraction before every answer.
4. **Control:** validate detected controls and apply a compatible batch atomically. If unresolved, conflicting or failed, block dependent effects and any saved-success claim. Independent drafting can use current input with an honest unsaved/partial status.
5. **Release permitted learning:** commit the current source's allowed projection and release its job only after controls resolve. If forgotten text is mentioned in the request, it remains excluded. Current input was already available privately to this run. The service returns a disposition receipt with knowledge revision before/after and the promoted projection digest. It may rebase the answer's freshness token only if the before revision exactly matches the captured token, the sole change is promotion of text already present in that run's context, its permitted digest is unchanged, and no control or intervening write changed meaning. Recheck the after revision at publication. Any unrelated change before/after release or altered projection requires normal refresh. The model cannot request this exception.
6. **Continue:** if changed evidence invalidates the provisional result, refresh retrieval and regenerate. Otherwise process its answer/read/action choice. Repeated controls return their existing receipt. Tool observations re-enter the model as observations.
7. **Publish:** buffer the final answer. In a short transaction, check fresh knowledge/run/permission state, accept the output, assign sequence and persist the terminal run outcome together. A changed knowledge revision can represent new contradictory evidence even when cited rows are unchanged; refresh under a bounded retry policy. No second raw content copy is written after acceptance.
8. **Deliver/replay:** return the committed result through the ordered output path. Retrieval on reconnect or idempotent replay must obey current suppression. Acceptance is ordered against controls; it does not make network delivery atomic or retract previously received bytes.

Initial circuit breakers: four answer-model attempts including repair/retries, six follow-up read operations beyond initial retrieval, one external effect, and a 30-second ordinary-request deadline. One ordinary supported answer targets one model call. Permit at most one eligible transient retry per call within the total budget. On exhaustion, return an observed partial/error status; do not make an unbounded final attempt. These limits are development defaults, not endpoint guarantees.

### 7.1 Two entry paths, one memory service

```text
Historical record: raw ASR + formatted text + available metadata
  -> validated import and original-source persistence
  -> permitted source search becomes available
  -> durable worker proposes / validates / admits useful memories
  -> evidence, supported links and search representations become ready

Current typed Hey Kivi request
  -> private input + held learning job
  -> permitted history/memory retrieval + current input
  -> model proposal
  -> application commits controls / resolves allowed source release
  -> further retrieval or authorized tool effect only if needed
  -> freshness check + response acceptance
  -> output text, sources and actual artifact/outcome
```

Imported history is not a live instruction. A current input is available to its own answer before background extraction completes. Ordinary learning stays off the answer's critical path, but its costs are still recorded. An explicit “remember/correct/forget” must succeed before Kivi claims that it was saved or removed.

### 7.2 Illustrative complete journey and failures

1. Import sources establishing the Jaipur trip's total hotel budget as INR 6,000 and the user's trip-specific quiet-hotel preference. Inspect the original sources and accepted memories.
2. Ask for a hotel-selection checklist. Retrieve both constraints/preferences with evidence and prepare a useful draft; do not invent actual hotel availability or a completed booking.
3. Say “Change the total hotel budget for that Jaipur trip to INR 8,000.” Resolve the same trip, commit the supported change, preserve the earlier value as historical, and acknowledge only after commit.
4. Ask the current budget and the earlier budget. Answer INR 8,000 and INR 6,000 respectively, with their sources and time/status qualifications.
5. Optionally request saving the checklist to a designated local path. Use current authority, verify the resulting artifact and report its observed status. Memory saving and a filesystem effect are separate outcomes; one can succeed while the other fails.
6. Inspect why the budget affected the answer, then request forgetting that budget. The selected information and known supporting spans stop being used through memories, original-source fallback, stale jobs, indexes and retained answer replay. Distinguish this from deleting the original source itself.

If “that trip” matches multiple trips, preserve the ambiguity and ask only for the distinction needed. If persistence fails, an independent draft can still use the current message with an explicit unsaved status. If an effect times out after dispatch, show unknown outcome and reconcile; do not blindly duplicate it. This journey is a contract illustration, not a prepared-only demo or finalized product narrative.

## 8. Atomic operations and durable recovery

Atomic means the related database changes commit together or none do. It does not mean the whole request, model API, database and file system share one transaction.

| Operation | Changes checked/committed together |
|---|---|
| Accept input | Request-key/digest check; source/run identity; visibility; held or queued job |
| Apply controls | Validate the complete compatible batch and expected targets; memory revisions/heads; exclusions; permitted-source projection; affected indexes/links; receipt and knowledge revision |
| Resolve live-source disposition | Allowed remaining source text, readiness, released/remaining held job and knowledge revision; combine with controls where possible |
| Admit background memories | Current job attempt/lease and captured source/knowledge/target revisions; candidate decisions, memory/evidence/edge/FTS changes; follow-up vector jobs |
| Complete vector work | Current allowed projection/encoder/revision; vector row and job outcome; index revision |
| Prepare effect | Exact target/arguments, authorization reference, operation key and expected target version |
| Admit dispatch | Recheck applicable controls/authority; compare-and-set ready to dispatched; record attempt identity |
| Observe effect | Actual receipt/status, operation state and permitted tool observation |
| Accept response | Fresh knowledge/run/cancellation checks, answer dependencies, response content, terminal run status and publication sequence |

Use short transactions and bounded busy/retry behavior. No model call, embedding computation or external tool effect happens inside a DB transaction. A worker reclaim increments an attempt token; a delayed prior attempt cannot commit. Enqueue jobs in the same transaction as the state requiring them. Do not describe retried external calls as exactly-once execution. [SQLite isolation](https://sqlite.org/isolation.html), [Kleppmann on dual writes](https://martin.kleppmann.com/2015/05/27/logs-for-data-infrastructure.html), [Temporal Activity execution](https://docs.temporal.io/activity-definition)

Keep states separate:

```text
Run: accepted -> running -> waiting_input -> running
     running -> completed | partial | failed | cancelled | outcome_unknown
     accepted/running/waiting_input -> cancelled when stoppage is established
Explicit resume of a failed attempt -> linked new attempt: accepted -> running
     prior attempt stays terminal; committed operation receipts stay authoritative

Learning: held -> queued -> running -> succeeded | no_op | excluded
          running -> retry_wait -> queued; exhausted -> failed
          stale completion -> discard or queue a new revision

Effect: proposed -> ready | waiting_approval | rejected
        waiting_approval -> ready only after matching authorization
        proposed/waiting_approval/ready -> cancelled | rejected
        ready -> dispatched -> succeeded | failed | unknown
        unknown -> reconciling -> succeeded | failed | unknown
```

Crash after a local commit: replay the receipt. Crash after external dispatch but before recording completion: preserve unknown outcome and reconcile. Cancellation after dispatch expresses intent, not guaranteed rollback. Deletion after response acceptance invalidates retained copies according to policy; already delivered text has a separate boundary.

`resume_run` after terminal failure creates a linked attempt under the logical request and atomically updates its active-attempt pointer; it does not rewrite the prior terminal attempt. The new attempt has an explicit fresh bounded call/deadline budget, while cumulative usage remains recorded. Reuse committed operation receipts and reconcile any unknown dispatched effect before further execution. Changed effect payloads need a new operation identity and fresh authority check. A waiting-input continuation retains its attempt's call budget; user-wait time is reported separately from active execution time.

FTS updates must be tested with actual `MATCH` queries. Enable WAL only on suitable local storage, use a runtime containing its documented fixes, and use SQLite's backup API for active databases. The available research runtime is Python 3.12.14 / SQLite 3.53.1 with FTS5; this does not establish the future packaged application's configuration. [SQLite WAL](https://sqlite.org/wal.html), [FTS5](https://sqlite.org/fts5.html), [backup API](https://sqlite.org/backup.html)

## 9. Learning and retrieval details

The learner works on permitted source units. Begin with individual short records and justified adjacent context. Batch coherent segments only when context/cost measurements justify it; never batch across unknown speaker/session boundaries or hold explicit user controls for a consolidation window. Distinguish successful empty extraction from a parse/provider failure. An unresolved name, date or pronoun remains unresolved; compression must not manufacture specificity.

Extract attributed candidates, retrieve related existing assertions, then validate and admit. Outcomes are add, supported change/correction, link independent evidence, duplicate/no-op, conflict/unresolved or rejection. Preserve conflicting history. Only explicit controls can request forgetting; ordinary model disagreement is not permission to erase original evidence.

Admission policy is versioned and inspectable. Preserve useful reported facts, preferences, plans, decisions and experiences when supported. Do not turn greetings, repetitions, boilerplate, fictional/quoted passages, assistant-generated drafts, ambiguous ASR differences or unsupported interpretations into unqualified user facts. A quotation can still be useful knowledge about who said what. Unknown attribution or time stays unknown; it is not fixed by rewriting a sentence more fluently. Deliberately skipping derived memory leaves permitted source retrieval available. The exact product policy for unusually sensitive data still needs a stated user experience rather than a blanket promise to remember everything.

Record prompt, admission-policy, category/predicate-registry, model, encoder, preprocessing and retrieval-configuration versions/hashes with jobs and evaluation manifests. Changes to accepted interpretations are explicit versioned operations, not silent consequences of loading a new prompt. Prompts instruct the model; code enforces scope, schemas, allowed operations and atomic transitions. Store concise evidence-linked decision reasons, not hidden chain-of-thought.

Retrieval starts with four candidate lists when dense is enabled: source lexical, source vector, memory lexical and memory vector. Prototype defaults are top 20 per list, reciprocal rank fusion with k=60, and at most 40 fused candidates before packing. Deduplicate source variants and overlapping evidence. These are tunable retrieval budgets, not optimum values or confidence thresholds. Graph expansion can add one supported hop with at most 20 entities/40 evidence references; retain a truncation indicator. Adjust only on development data. [Hybrid retrieval](https://www.anthropic.com/engineering/contextual-retrieval)

For direct recall, inspect original supporting spans. For multi-source questions, retrieve bridge evidence through links or a bounded further read. For counts, complete lists and change histories, use structured enumeration plus source fallback for extraction gaps; a top-k list cannot establish completeness. Page such reads (initially 100 records per page) through the same eligibility boundary and report incomplete coverage when limits prevent enumeration. Coherent late records and current corrections remain temporally distinguishable.

Start with a 4,096-token evidence budget including memory text, source excerpts and metadata. Preserve decisive spans during packing. Use the actual tokenizer and reserve model output/context overhead. E5 inputs use the model's documented prefixes and token limits. Exact vector scoring means no approximate-neighbor candidate loss under that function, not perfect semantic retrieval. Hindi/Hinglish, negation and names require their own tests. [Sentence-transformers semantic search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)

Return an evidence bundle with source/memory revisions, scores, supported spans, conflicts, coverage/truncation, per-stage readiness and a store-issued freshness token. An answer's personal claims need permitted evidence. General world knowledge and external tool information remain distinguishable. Useful personalization can silently shape a response; merely mentioning a remembered fact is not a success metric.

## 10. Exact cache policy

| Layer | v1 policy | Validity/invalidation |
|---|---|---|
| Persisted document/memory embeddings | Enable with dense retrieval | User, record/memory revision, permitted-projection digest, encoder revision/preprocessing, dimension/normalization |
| Loaded encoder | Keep in RAM during a persistent process | Model configuration and process lifetime |
| RAM vector/map view | Optional optimization; retain correctness without it | User and index/knowledge revision as applicable; rebuild/swap coherently; recheck eligibility |
| Query-embedding cache | Off initially; possible bounded cache later | Exact actual encoder input, user, encoder/preprocessing revision; purge retained query text under controls |
| Retrieval-result cache | Off initially | Would need query interpretation/working context, user/scope, knowledge/index revisions, time and retrieval configuration |
| Exact or semantic answer cache | Off | Would also need instructions, evidence, model and tool/external dependencies |
| Provider prompt cache | No assumption of support | Verify actual NVIDIA capability, retention, billing and hit telemetry |

Storing embeddings in SQLite is precomputation/index persistence. Loading the encoder once avoids cold-start work. Those supply useful reuse without a cache of old final answers.

A cache inside SQLite can help if it avoids expensive computation; for example, a repeated query encoding can survive CLI restarts. It does not automatically improve an already cheap indexed DB lookup. Avoid turning every cache hit into a DB write for `last_used`. Measure net hit/miss/lookup/invalidation costs under realistic repetition. Relative-time questions can change without a knowledge mutation. TTL is insufficient for immediate correction/forget semantics. SQLite already has a page cache, distinct from cached model results. [SQLite page cache](https://sqlite.org/pragma.html#pragma_cache_size), [Huyen on cache types](https://huyenchip.com/2024/07/25/genai-platform.html#step-4-reduce-latency-with-cache)

## 11. Tools, CLI lifecycle and later interface

Use a small tool registry and application-validated arguments. Existing authorization is reused within scope; missing authority or material target details are resolved before dispatch. First effect: create/update a user-requested local artifact under a designated directory, with expected path/version and observable result. Do not automatically execute a remembered intention. An external read can disclose its query, so tool scope includes outgoing content.

MCP is an adapter protocol. Its tool annotations cannot independently grant authority, and negotiated task support cannot be assumed for every server. A timeout or expired remote task is not proof of no effect. Persist receipts and reconcile unknown outcomes before any retry that could duplicate work. [MCP tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools), [MCP tasks](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/tasks)

Planned CLI surface: `init`, `import`, `process --resume`, `ask`, `chat`, `resume <run_id>`, `cancel <run_id>`, `inspect`, `correct`, `forget`, `delete-source`, `status`, `evaluate`, and `reset`. All call the same service contracts. `chat` is a persistent REPL that can retain the encoder and worker. In one-shot `ask`, input and pending jobs persist, but ordinary learning stops when the process exits; show pending status and use `process --resume` for eligible queued work. It reports held jobs separately and cannot resolve their control interpretation by extraction. `resume <run_id>` routes a failed/unresolved live turn back through the coordinator with any needed clarification; only its valid disposition releases learning. Explicit controls still commit synchronously. No invisible daemon is implied.

Proposed module layout, not yet created:

```text
kivi/
  cli.py                 # argparse client / persistent REPL
  coordinator.py         # request state and bounded proposal loop
  contracts.py           # Pydantic proposal/receipt/evidence contracts
  prompts/               # versioned extraction/answer policy; no authority from source text
  memory/
    service.py           # public memory operations
    admission.py         # extraction proposals and lifecycle decisions
    evidence.py          # one permitted-text projection boundary
    retrieval.py         # lexical/dense/link retrieval and packing
    controls.py          # remember/correct/forget
  storage/
    repository.py        # scoped parameterized SQL and atomic operations
    migrations/          # versioned schema changes
  models/
    language.py          # NVIDIA/DeepSeek adapter
    embeddings.py        # pinned local encoder
  jobs.py                # durable learning/index work
  tools.py               # narrow registry/adapters and effect ledger
  evaluation/            # replay, fixtures, rubrics, metrics
```

The final UI will call this service through an application boundary and provide evidence, controls, processing state and actual outcomes. Frontend choice and detailed user journeys follow this blueprint; CLI-only remains an intermediate milestone.

The first artifact tool should show its target and operation, validate a designated-directory boundary and expected existing version, and return the actual path/content digest or error. Use readback/reconciliation for an uncertain write. A remembered preference never grants filesystem, email or calendar authority. Calendar, email, browser/web search, reminders and general MCP connectors remain optional, use-case-driven extensions; no scheduler or external account integration is assumed.

### 11.1 Import and configuration contract to finalize in development

The baseline requires a documented, versioned import format that a reviewer can map their logs into. JSONL is the proposed first encoding. The following is a **draft logical envelope**, not an implemented parser contract:

| Field | Planned meaning |
|---|---|
| `schema_version` | Explicit format version |
| `record_id`, `revision` | Stable upstream identity/revision; generated importer mapping must be reproducible if absent |
| `raw_asr`, `formatted_text` | Exact paired text fields; preserve Unicode and material disagreement |
| `captured_at`, `timezone`, `available_at` | Optional supplied time context; distinguish capture and availability |
| `app`, `conversation_id`, `project_id` | Optional supplied scope/context; absence does not block unrelated recall |
| `metadata` | Original additional fields, kept as untrusted data |

Trusted user scope comes from the application/import invocation, not a model or arbitrary row field. Define required/null/malformed behavior in the actual import schema before corpus generation. The expected assignment pair should be validated; incomplete local stress fixtures need explicit handling, not invented text. Preserve distinct real events even if text is identical. Stable ID/revision plus payload governs repeat import; content hashes detect changes and do not define event identity alone. Account for every row as accepted, duplicate, pending or rejected with reason. Reimport must not silently bypass an exclusion or recreate a deleted source; define suppression/tombstone behavior and explicit restoration separately.

Proposed environment-variable names to preserve or explicitly revise when `.env.example` is implemented:

| Name | Purpose / status |
|---|---|
| `NVIDIA_API_KEY` | Secret supplied by the user during development, not in chat, source data, traces or Git |
| `KIVI_LLM_BASE_URL` | Configurable provider endpoint; verify the actual NVIDIA deployment |
| `KIVI_LLM_MODEL` | Exact verified model ID; not selected yet |
| `KIVI_DB_PATH` | Local application-owned SQLite path |
| `KIVI_EMBEDDING_MODEL` | Encoder identifier; pin a model revision in the run configuration |

Timeouts, output/reasoning limits, concurrency, retry ceilings, embedding settings and total usage budgets belong in versioned configuration. The actual SDK/request shape, structured-output support, context/tokenizer behavior, rates and account limits require a live preflight. No free/unlimited quota or provider caching is promised. No API key is needed to continue refining this plan.

Pin Python, package and model revisions during implementation, and record model-download size/startup needs in `RUN.md`. Compare a cold one-shot process with a warm REPL/service; their encoder costs differ. Exact install/start/reset commands must be tested against real code before they are documented as working commands.

## 12. Evaluation, review loops and stopping rule

Create or obtain the **planned approximately 500 history records**. Neither that corpus nor the evaluation has been built. The current proposed protocol is **80 reviewed questions: 30 development / 50 sealed**, with whole narrative/template blocks separated. Separately audit 50 source records, split 20 development / 30 sealed, for extraction and exercise critical lifecycle/action invariants. Readiness, permitted history and time cutoffs apply to every baseline. The [earlier detailed evaluation review](research/design-review-evaluation.md) supplies rationale; this section governs where scheduling or contract details differ.

### 12.1 Data, question coverage and honest labels

The corpus manifest records IDs/revisions, raw/formatted pairing, actual token lengths, languages/scripts, timestamp/timezone/availability coverage, duplicate events, missing metadata and ASR/formatter disagreements. Generated histories should contain coherent recurring people/events and realistic distractors. Do not shape the corpus around memorized demonstration questions or use generated gold answers without checking their supporting records.

| Primary capability | Development | Sealed |
|---|---:|---:|
| Direct recall and attribution | 6 | 10 |
| Combining records and evidence completeness | 4 | 8 |
| Time, corrections and changed state | 8 | 12 |
| Unknown, ambiguous or conflicting information | 6 | 10 |
| Contextual assistance and current instruction priority | 6 | 10 |
| Total | 30 | 50 |

The sealed target has 40 answerable cases and 10 insufficient/conflicting cases. Treat English, Hindi in Devanagari, Romanized Hindi/Hinglish, code switching and cross-language query/source pairs as overlapping slices. Proposed coverage is at least 20 multilingual/mixed-language questions including eight cross-language pairs, with names, negation, dates and ambiguous “kal.” Missing coverage remains visible; separately labeled authored stress fixtures do not inflate natural-data results. An English interface is a starting proposal, separate from multilingual text handling.

Each question records query time/timezone, available source revisions, acceptable supporting spans/evidence sets, required and forbidden claims, answerability, expected behavior and scenario ID. Separate whole narratives/templates and their paraphrases before tuning. Keep question text, rubrics and gold answers outside memory ingestion. Human review checks source support; the answering model cannot certify its own gold. Disclose single-reviewer limitations; ideally independently review ambiguous/multilingual cases and a sample of other questions.

Temporal replay uses only sources available by the query cutoff. An old event imported later must not overwrite newer state based solely on import order. If availability is absent, use a declared simulated order; never fabricate real chronology. Derived links, extractions, summaries and indexes obey the same cutoff and current exclusions.

### 12.2 Baselines, metrics and release proposals

Compare full allowed history where it fits, lexical original-source retrieval, hybrid original-source retrieval and hybrid with typed memory. Give full history its actual full context and report fitting subsets; do not artificially truncate it into a weak baseline. Measure supported task success, evidence coverage, current/historical correctness, false abstention, inappropriate personalization, tool outcomes, latency, tokens and ingestion-plus-query cost. Public benchmark scores are not evidence of Kivi performance. [LongMemEval](https://github.com/xiaowu0162/LongMemEval)

Hold the answer model, instructions, scope and cutoff constant between systems. For retrieval systems, use the same initial evidence-token budget and deduplicate observations. Score evidence delivered after packing, not merely source IDs that appeared earlier in a ranking. Missing retrieval traces mean unmeasured, not perfect retrieval. Full-history fit includes prompt/query, output reservation and a proposed 1,024-token safety margin against the verified context limit.

Primary quality measure: **fully supported task success**—required claims/actions satisfied, no material unsupported additions, correct subject/time/modality, and actual evidence for personal-history claims. Report these separately:

| Stage | What to inspect |
|---|---|
| Extraction | Admitted precision, eligible recall, wrong subject, invented details, bad merges/updates, unresolved and no-op decisions |
| Retrieval | Source Recall@5/10, all-required-evidence coverage, decisive-span coverage after packing, truncation/readiness |
| Answering | Claim support, citation completeness, correct answer with wrong source, current versus historical accuracy |
| Abstention | False assertions when history is insufficient; needless clarification/abstention on answerable cases |
| Personalization | Useful adaptation, current instruction priority, unnecessary callbacks or invented preferences |
| Tools | Actual effect and permission/target correctness; truthful partial/failed/unknown status |
| Operations | Ingestion throughput/lag, cold/warm query latency, retries/errors, DB/index growth, model RAM, calls/tokens/cost |

Human judgment is primary for this small suite. If an automatic judge is used, version its model/rubric, hide candidate identity where possible, and inspect disagreements and critical errors. Record concise decision reasons and observed traces, not private model reasoning. Show counts and denominators and paired wins/losses. Any uncertainty estimate must respect shared scenario blocks; small language slices do not establish population reliability.

Proposed final acceptance thresholds inherited from the review are listed here so they cannot disappear into another file. **They are not achieved results or user-approved performance promises.** Ratify them before opening sealed results; use corresponding development measurements for tuning. Sealed measurements assess the frozen candidate, not a new round of tuning.

| Proposed gate | Initial threshold to ratify |
|---|---|
| Import accounting | Every intended source accounted for, with inspectable status/provenance and applicable integrity checks passing |
| Typed extraction | On audited sealed sources, at least 95% admitted precision and 80% eligible recall; zero critical wrong-person or invented-authorization writes |
| Supported task quality | At least 34/40 answerable cases fully supported; at least 9/10 insufficient/conflicting cases use the correct fallback; at most 2/40 needless abstentions/clarifications |
| Critical integrity | Zero cross-user disclosure, excluded-content release, unauthorized write or false tool-success claim in applicable tested scenarios |
| Added complexity | At least three net additional supported successes out of 50, or preserved successes with at least 20% lower measured p95 latency or intended-horizon total cost; no new critical failure or weaker temporal performance |
| Final experience | Recall, changed-state answer, correction, forgetting, ambiguity and prepared/cancelled-action journeys work through the actual UI/backend with persistent state and truthful outcomes |

These sample-based gates cannot prove absence of errors. If results do not distinguish alternatives, keep the simpler design and disclose uncertainty. If an unimplemented optional component has no test, mark it unimplemented rather than passed.

Use paired development failures to select one component experiment at a time. Freeze the strongest simpler comparator and the memory candidate before the 50 sealed questions. A maximum of 320 reader attempts is the proposed initial budget; the earlier worst-case 314-call schedule leaves inadequate retry space, so use two sealed finalists by default and trim optional diagnostics before the run. Count actual attempts, not questions; do not skip difficult cases when the budget runs out. Extraction, embeddings and judging have separately declared budgets.

The two-finalist schedule starts at 120 development comparisons plus 100 sealed comparisons. With all optional diagnostics (24 no-memory/gold-source calls) and stability checks (20) included and one attempt per comparison, 264 attempts are planned, leaving 56 of the 320 for additional calls/retries. Fewer optional checks leave more reserve; multi-call requests consume it. Preflight token/currency limits may require fewer optional diagnostics. A budget-exhausted run is incomplete and must be reported as such; gold-source diagnostics never count as achievable retrieval performance. A proposed starting generation cap is 2,048 tokens including reasoning where enforceable, with visible answers near 512 tokens; verify provider accounting first.

Prototype targets to ratify during preflight, before sealing: warm local retrieval p95 <= 500 ms **including query encoding, DB/vector work and evidence packing**; report those subcomponents separately. Ordinary full response p50 <= 5 s / p95 <= 15 s, request deadline 30 s. These are desired targets, not measured promises. Report cold starts, failures, sample counts, processing lag, database/model RAM, calls/tokens and unknown prices honestly.

Report end-to-end latency including failed requests, with successful-only timing separately. Buffered answers mean time to first visible output includes validation. Do not claim p99 from a tiny sample. Report ingestion plus query cost at declared reuse horizons, initially Q=10/100/1,000 queries; free credits do not make token usage zero. Unknown monetary pricing remains unknown. Include retry/evaluation/judging costs separately.

### 12.3 Product integrity suite, distinct from the research probe

Implement tests for repeated import with distinct identical events; restart/resume; correction during extraction; late old information; forgetting during extraction/embedding; correction or deletion during answering; dependent artifact/alias/cache suppression; cross-user scope; instructions inside history; skipped or cancelled actions; changed authorization/arguments; and unknown tool outcomes without blind retries. Include the held-source and own-source freshness cases discovered in the research probe.

These checks use controlled faults and staged outputs, then exercise the real application boundaries as they are built. The final HTTP/UI path must preserve the same rules, including suppression of cancelled late results. **The 12 already passing research checks are not the same thing as this planned product integrity suite.** Real concurrency, disk recovery, model interpretation and selected tool integration still require appropriate implementation tests.

### 12.4 Review loops and stopping rule

Design review loop: research -> explicit contracts -> independent adversarial review -> revise -> isolated contract probes -> final cross-check. Stop architectural review when no unresolved blocking contract contradiction remains and unmeasured choices have explicit experiments/change gates. This cannot establish an absolute best system before product measurements.

Implementation loop: build the smallest end-to-end path -> exercise invariants and development questions -> diagnose extraction/retrieval/packing/model/action failures -> change one justified component -> rerun affected checks. Once required checks and declared targets pass, freeze and run the sealed comparison. Later changes influenced by sealed failures need fresh held-out cases for a new generalization claim.

Do not add a graph database or cache because it is fashionable. Adopt it only when it fixes a measured relevant limitation with acceptable correctness, cost, latency and maintenance. If typed extraction does not help a class of questions, preserve its simpler source route rather than expanding the ontology to hide the failure.

## 13. Research inspirations and why this is not a framework transplant

Primary sources checked through 6 September 2026 support mechanisms, not a universal winner. The following newer papers are treated as research evidence requiring local replication; current repository behavior was checked separately.

| Source | Specific inspiration and boundary |
|---|---|
| [Graphiti / Zep](https://github.com/getzep/graphiti) | Source-backed entities/relationships and temporal validity. Borrow the model; do not equate an OSS backend with managed Zep performance. |
| [A-MEM](https://arxiv.org/html/2502.12110v11) | Optional associative links and generated retrieval context. An association is a discovery hint rather than proof of a real relationship. |
| [Hindsight, Dec 2025](https://arxiv.org/html/2512.12818v1) | Explicit retain/recall/reflect operations and separation of evidence from synthesized observations. No autonomous belief reinforcement is required in v1. |
| [SimpleMem, Jan 2026](https://arxiv.org/html/2601.02553v3) | Compact context-aware units and multiple retrieval representations. Its compression framing does not guarantee preservation of all future answers. |
| [APEX-MEM, Apr 2026](https://arxiv.org/html/2604.14362v1) | Typed temporal assertions and preserved conflicting history. Explicit user controls still require immediate effects. |
| [LycheeMemory V2, Aug 2026](https://arxiv.org/html/2608.12990v1) | Coherent segment batching as an optional way to reduce construction calls, subject to provenance/latency tests. |
| [LangMem](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/) | Separate memory transformations from the backing store; a checkpoint or library alone is not the entire memory contract. |

Current implementation details matter. [Mem0's migration guide](https://docs.mem0.ai/migration/oss-v2-to-v3) documents ADD-only OSS extraction and moves external graph-store integration to Platform. [Hindsight's retain guide](https://hindsight.vectorize.io/developer/retain) states that raw documents producing zero memories are not discoverable through ordinary recall/reflect; our independent source search deliberately preserves that route. Hindsight now has an embedded deployment option, and SimpleMem uses embedded LanceDB, so neither is rejected on the false premise that every alternative requires a remote server.

The inspected [SimpleMem builder](https://github.com/aiming-lab/SimpleMem/blob/main/simplemem/core/memory_builder.py) returns an empty list after exhausted parsing failures and asks for forced reference/date disambiguation. Our contracts distinguish failed extraction from a genuine no-op and retain unresolved names/dates. These specific differences explain why importing a framework unchanged would not finish this assignment's lifecycle requirements. A future adapter remains possible if it demonstrably reduces engineering cost while meeting the same contracts.

System-design grounding includes [DDIA's official book resources](https://dataintensive.net/), Kleppmann's cited public articles on durable and derived data, [Huyen's public Agents section from AI Engineering](https://huyenchip.com/2025/01/07/agents.html), and her [ML system-design guide](https://huyenchip.com/machine-learning-systems-design/design-a-machine-learning-system.html). These supplied relevant principles and accessible sections; this research does not claim entire commercial books were read.

The wider competitor study informed product questions rather than a runtime dependency decision:

| Reference group | Lesson retained | Limit on what we infer |
|---|---|---|
| Wispr Flow, Superwhisper, other dictation tools | Context-sensitive terminology and faithful composition; avoid needless settings work | Dictionary/style features do not by themselves establish history reasoning |
| ChatGPT, Claude, Gemini memory experiences | Low-effort continuity, understandable control and scoped use of history | Public behavior does not disclose a complete internal storage architecture |
| Granola and other history/meeting assistants | Useful questions with inspectable source context | A narrow capture surface differs from all supplied Kivi dictations |
| Glean, Copilot, connected knowledge tools | Access boundaries and evidence across sources | Remembered references do not grant connector access or authority |
| Mem0, LangMem, Graphiti, A-MEM, Hindsight, SimpleMem | Reusable extraction, temporal representations, storage-independent transformations and retrieval ideas | Match versions and inspect source behavior; a framework does not automatically meet our lifecycle contract |
| Letta/MemGPT, RAPTOR, Cognee, Supermemory | Context selection, hierarchy and richer memory systems worth understanding | No need to adopt a whole agent platform, summary tree or extra database without measured benefit |

The [initial competitor report](RESEARCH_SEMANTIC_MEMORY.md) and [15-topic research dossier](research/README.md) retain source details. Their historical rankings, feature counts and early implementation sketches are not settled claims in this plan. No comparable local competitor benchmark was run, and no exhaustive market-gap claim is justified. Current product/repository details are dated research observations and must be rechecked before relying on a changed dependency or feature.

Detailed audits: [memory/ontology](research/blueprint-research-memory.md), [storage/cache](research/blueprint-research-storage.md), [workflow contracts](research/blueprint-research-workflow.md).

## 14. Completed review, validation and next boundary

Three independent researchers reviewed the integrated contracts and then checked the corrections. The closed findings include attribution/polarity in graph projections, unknown temporal bounds, scoped predicate cardinality, alias/identity provenance, current source heads, live-source promotion freshness, explicit source deletion, approval/cancellation transitions and linked retry attempts.

The [isolated SQLite probe](research/validation/atomic_memory_probe.py) uses actual in-memory SQL transactions, foreign keys and FTS5 triggers with controlled sequential interleavings. Initial ten checks passed. A new held-source-forget case failed; projection unification fixed it. An additional source-promotion/freshness case tested the controlled one-call exception. Final result, independently rerun by the primary agent: **12/12 passed**, Python 3.12.14 / SQLite 3.53.1. [Machine-readable results](research/validation/atomic_memory_results.json), [failure/fix review history](research/validation/REVIEW.md).

The probe does not test real concurrency, disk-crash recovery, LLM interpretation, factual accuracy, graph/alias cleanup, MCP execution or performance. It is an executable design model, not the product or its production test suite. The future application must exercise the same contracts independently.

The next stage is user-point-of-view refinement: define the default experience for recalling changed information, preparing a useful personalized result, and inspecting/correcting/forgetting memory; specify ambiguity and partial-success behavior. Then implement the CLI against these contracts, starting with source import/inspection and a complete cited-answer path. Model credentials, endpoint/encoder validation, actual migrations and product tests belong to that development stage. The final assignment also needs the normal-user interface after the CLI milestone.

The conversation consolidation adds an independent assignment-alignment audit, technical-contract audit and research-decision audit. They found missing submission/product context and an incorrect claim that the corpus already existed; those are corrected here. No application was built, no new model benchmark was run, and the unchanged research probe was not rerun merely to edit documentation.

## 15. Submission and reviewer completion checklist

The following are **required deliverables or review-path work**, not claims of completion. All must be checked against the final implementation.

- [ ] Applicant's independently authored positioning statement (<=100 words) and vision (<=600 words), with honest provenance and the brief's required ordering.
- [ ] One GitHub repository containing complete source code, a working normal-user interface and connected backend.
- [ ] Actual database schema and versioned migrations, with reproducible seed data.
- [ ] Approximately 500 transcript-like development records containing raw ASR, formatted text and useful available metadata.
- [ ] Runnable full-pipeline evaluation, reviewed cases/rubrics, generated results, failures and limitations.
- [ ] Inspectable original inputs, accepted/retrieved/changed/rejected memories, supporting sources, resulting behavior and concise decision reasons.
- [ ] Latency, database growth, model usage and cost accounting where relevant.
- [ ] `README.md` explaining product, architecture, use cases, limitations, measured results and AI use.
- [ ] `RUN.md` beginning with the primary review arrangement; no undocumented dashboard work or setup repair required.
- [ ] Exact runtime/package/model requirements, every environment variable and an `.env.example` without private credentials.
- [ ] Tested commands for dependency installation, database creation/migration/seeding and every process startup.
- [ ] Exact URL/window/interface to open and primary interactions to try.
- [ ] Exact evaluation command and where generated results can be inspected.
- [ ] Exact procedure to import a different corpus, process it, inspect database/memory state and operate Hey Kivi.
- [ ] Exact procedure to reset the system; application data reset must have a clear boundary and not remove unrelated files.
- [ ] A clean-checkout test of start, import, process, use, inspect, evaluate and reset using the declared method.
- [ ] Submission form includes repository URL and exact final commit SHA; hosted URL only if using a hosted primary review method.

Deployment, Docker, native speech capture, production Kivi integration and a broad MCP catalog are optional. A reviewer can supply documented credentials and translate their data into the documented import format. They will not infer missing steps or repair the application. Choose reproducibility over an impressive-looking deployment arrangement.

## 16. Build order, open decisions and scope control

### 16.1 Next development stages

| Stage | Work | Exit evidence |
|---|---|---|
| 0. Product refinement | Confirm the leading user journey, useful outcome, mode boundary, uncertainty/controls experience and final review arrangement; account for Part One status | Small coherent behavior specification; each selected capability has a user purpose |
| 1. Durable source foundation | Pin runtime/dependencies, implement import contract/schema/migrations, source inspection, jobs, policy versions and relevant exclusion/scope rules | Reproducible import accounting, persistence, reset and applicable integrity checks |
| 2. Complete CLI answer path | Coordinator, provider preflight, lexical source retrieval, evidence bundle, cited response, errors/status/usage | Real typed question produces a supported answer or honest fallback through actual persisted state |
| 3. Memory and retrieval comparison | Typed admission, the 12 labels, revisions/controls, source fallback; add local dense retrieval as a separately measured increment | Development evidence shows what memory and embeddings improve; corrections/forgetting work through every path |
| 4. Useful output and evaluation preparation | One justified artifact capability; reviewed corpus/questions; paired development comparisons; failure diagnosis and candidate configuration | Truthful action/partial status and relevant integrity checks; sealed questions remain unopened |
| 5. Complete user interface | Select/build UI and adapter around the same service; source inspection and natural controls; real loading/error/cancel behavior | Representative ordinary journeys and UI/backend integrity checks pass; freeze the final pipeline/configuration |
| 6. Final evaluation and submission rehearsal | Run the sealed comparison on the frozen pipeline; record honest results; complete documents/schema/migrations/seed/runbook; rehearse a fresh checkout | Reviewer can start, operate, import, inspect, evaluate and reset the submitted commit; sealed-informed fixes require a new holdout for a fresh generalization claim |

These are dependency stages, not a promise of a particular number of hours. Some UI work can proceed once service contracts and the user journey are stable. Build the applicable correction, scope, exclusion and trace rules with the first source path rather than postponing all correctness until a later feature stage. Final interface and new-corpus import remain essential even if optional memory enhancements are cut.

### 16.2 Open decisions and the evidence that resolves them

| Open item | Current position | How to resolve it |
|---|---|---|
| First recurring user journey | Recover/connect/apply context are candidate abilities | Select one meaningful task and review its normal, ambiguous, changed and forgotten states |
| Applicant's Part One status | Not established in the inspected artifacts | Applicant handles the brief's independent-thinking/writing requirement; disclose actual AI use |
| Final UI and application adapter | Required; framework undecided | Choose after the journey; use one shared service and a reproducible local review path |
| Detailed memory admission/retention UX | Selective learning and explicit controls established | Define useful versus ignored information, sensitive-data behavior and any no-personalization experience |
| Exact import/schema/config contract | Logical fields and proposed names specified here | Freeze validated schema and migrations before generating the final corpus |
| NVIDIA/DeepSeek deployment | Provider family chosen; credentials later | Verify actual model ID, output contract, limits, usage accounting, failure behavior and latency |
| Embedding default | E5-small first candidate; BGE-M3 comparator | English/Hindi/Hinglish tests, cold/warm RAM/latency and retrieval coverage |
| Typed memory / graph contribution | Baseline schema supports them | Paired development analysis; admit default answer-path complexity only when it earns its cost |
| Retrieval/quality/usage targets | Explicit proposals in sections 7, 9 and 12 | Ratify during development preflight, before sealed evaluation |
| Test tooling and packaging | Custom evaluation required; tools/versions unpinned | Pick compatible small tooling and prove the clean-checkout procedure |

No API key is requested during this consolidation. No unresolved choice justifies silently presenting a proposed framework, threshold or command as already implemented.

### 16.3 What to cut first if scope is too large

Defer a graph server, Redis, approximate indexing, query/answer caches, recursive summaries, rerankers, autonomous reflection, separate skills/roles infrastructure, broad external integrations and optional benchmark grids before cutting source coverage, evidence, correction/forgetting, useful user behavior, evaluation or the final UI. A source-only route that outperforms extraction on a question class is a valid route in the product.

Readiness today means the memory architecture is concrete enough to implement and interrogate. It does not mean the product position, interface, model quality, speed or submission readiness has been proven. The next useful evidence comes from the smallest complete working journey and its evaluation, rather than another unbounded research cycle.

## 17. Conversation decision register and fresh-start handoff

This consolidation reviewed all three pages of retrievable turns in this task, the latest visible conversation, the official assignment extract and the saved planning/research artifacts. It is a decision record, not a verbatim transcript. Tool outputs and every historical feature list are not duplicated; relevant conclusions and their limitations are retained. The inspected sources are listed below so a future review can distinguish evidence from proposals.

| Conversation topic / earlier idea | Current resolution | Where to resume |
|---|---|---|
| Backend versus Golden Goose | User chose Golden Goose; no parallel phonetic product is in this build | Section 0 |
| Kivi versus Sarvam; dictation versus assistant | Company/product and mode boundaries retained; no full Kivi clone or ASR required | Section 0.2 |
| “Any question” | Any reasonable supported/derivable history question; no guessing or fixed-demo restriction | Sections 0.3, 9, 12 |
| User control without administration | Natural correction/forget/why, automatic routine organization, inspectable evidence | Sections 0.4, 5–8 |
| Direct input versus speech; language | Imported paired text plus typed requests; multilingual testing proposed, no hidden-language guarantee | Sections 0.3, 11.1, 12.1 |
| LLM API key / provider | NVIDIA-hosted DeepSeek chosen; key and exact deployment later; local embeddings separate | Sections 2, 11.1 |
| Abilities, tools, skills and harness | Observable recover/connect/apply abilities; small custom orchestration; narrow tools | Sections 0.1, 6–8, 11 |
| Broad semantic categories | Twelve overlapping content labels, independent forms/topics/time/attribution, shared storage | Sections 3–4 |
| Separate semantic database | Logical MemoryService over one SQLite file; exact table groups specified | Sections 1, 4 |
| Graph, map, hierarchy and recency | Supported relationships in SQL; optional RAM maps; recency helps ranking without excluding old evidence | Sections 1, 3, 9–10 |
| Cache inside the database | Persisted vectors/loaded encoder useful; query cache measured later; final-answer cache off | Section 10 |
| Input → extract everything → answer | Current path retrieves and proposes; controls commit synchronously, ordinary learning is durable background work | Sections 7–9 |
| Uncertainty and implicit France/Paris recall | Selective clarification and appropriate personalization; no invented preference/identity/time | Section 0.4 |
| External work through MCP | Connectivity adapter only; current authority, observed outcomes and reconciliation remain our responsibility | Sections 8, 11 |
| Sources as truth / memory as disposable index | Sources record what was expressed; accepted interpretations and user controls are durable too; search projections are rebuildable | Sections 4–5 |
| Research and competitor choices | Mechanisms borrowed; no mandatory memory framework, private architecture guess or unreplicated performance ranking | Section 13 |
| Evaluation count and old schedules | About 500 records; proposed 80 questions, 50-source audit, separate integrity suite; two sealed finalists by default | Section 12 |
| Atomicity and validation | Reviewed contracts and research-only 12/12 checks retained; product/concurrency/model tests still pending | Sections 8, 14 |
| Founder pitch / “ready to go” | Defensible implementation plan; no claim of a working app or measured advantage | Sections 14–16 |
| Fresh start | Read this file, refine user POV and unresolved choices, then implement the smallest complete CLI path | Sections 15–16 |

Supporting material: [official assignment](../Kivi_Golden_Goose_Task_Final.pdf); [five product questions](research/PRODUCT_QUESTIONS.md); [research index](research/README.md); [earlier end-to-end explanation](research/END_TO_END_DESIGN.md); [earlier architecture proposal](research/ARCHITECTURE_PROPOSAL.md); [evaluation review](research/design-review-evaluation.md); and [probe validation history](research/validation/REVIEW.md). Earlier generic `records`/`memories` table names, six-type category sketches, immediate publication of live input, 60-question examples and historical framework descriptions do not override the current revisioned contracts.

For a fresh planning session: treat this file as the baseline, preserve explicit user choices and correctness rules, propose changes with a user benefit and measurable tradeoff, update the decision/status tables when a choice changes, and never turn an unmeasured proposal into a claim of completion. The immediate task is product refinement followed by CLI development—not recreating the research from scratch.
