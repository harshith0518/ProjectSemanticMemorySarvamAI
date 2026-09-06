# Golden Goose: complete architecture and build status

Status snapshot: 6 September 2026. Based on `ARCHITECTURE.md`, revision 1.1. This is a map of the planned system, not implemented application behavior.

**DONE** = planning/research artifact exists. **PROBE** = isolated experiment exists. **BUILD** = specified, but product implementation remains. **OPEN** = decision or measurement remains. **DEFER** = optional, outside the starting build. The probe's 12/12 results are not application, semantic-quality, concurrency, or performance results.

```mermaid
flowchart TB
  subgraph STATUS["0 · WHAT EXISTS TODAY"]
    DOCS["DONE · Canonical architecture + research<br/>9 memory/application areas · 12 category labels<br/>Storage, lifecycle, retrieval and evaluation contracts"]
    PROBE["PROBE · Isolated SQLite experiment: 12/12<br/>SQL rollback, scope, idempotency, stale work,<br/>held input, forgetting, replay, publication freshness<br/>No working product or real model benchmark"]
    OPEN["OPEN · First user journey and admission/retention UX<br/>Part One documents not found in inspected folder<br/>UI/API framework · exact model · embedding default<br/>Quality, latency and usage targets unmeasured"]
  end

  subgraph INPUT["1 · APPLICATION ENTRY POINTS — BUILD"]
    HIST["Historical corpus / replay<br/>Approximately 500 development records<br/>Raw ASR + formatted text = ONE observation<br/>Available timestamps, app and other metadata"]
    UI["Normal-user web or desktop interface<br/>Typed Hey Kivi request · source inspection<br/>Remember / correct / forget / delete controls<br/>Loading, ambiguity, cancellation and failures"]
    CLI["Intermediate CLI / persistent REPL<br/>init · import · process · ask/chat · inspect<br/>correct · forget · delete-source · status<br/>resume/cancel · evaluate · reset"]
    IMPORT["Validate versioned import envelope<br/>Trusted user scope; stable record ID + revision<br/>Preserve Unicode, missing data and ASR disagreement<br/>Account for accepted / duplicate / pending / rejected rows"]
    INGEST["Atomic import<br/>Persist original source revision + head<br/>Create permitted source search and durable jobs<br/>Reimport respects exclusions/deletion tombstones"]
    HIST --> IMPORT --> INGEST
    UI -.-|"alternative clients"| CLI
  end

  subgraph LIVE["2 · LIVE REQUEST COORDINATOR — BUILD · UI and CLI share the same service"]
    L1["1. Accept request atomically<br/>Request key + payload digest → run/attempt<br/>Current source is PRIVATE to this run<br/>Learning job starts HELD"]
    L2["2. Retrieve coherent evidence<br/>Permitted sources + memories + recent context<br/>Current input usable immediately by its own run<br/>Capture store-issued freshness token"]
    L3["3. Interpret through model adapter<br/>Versioned proposal: controls + one next choice<br/>Answer / retrieve / action / clarify / abstain<br/>No mandatory separate classifier"]
    L4["4. Resolve current controls first<br/>Validate references, scope and legal changes<br/>Commit compatible controls atomically<br/>Failed/unresolved controls hold dependent effects"]
    L5["5. Release permitted current source<br/>Only surviving permitted text becomes shared<br/>Release learning job after controls resolve<br/>Repeated forgotten text must not be relearned<br/>Freshness rebase: identical already-seen current text only;<br/>no intervening control/knowledge change; recheck at publication"]
    L6["6. Continue within bounded budget<br/>Refresh/regenerate if controls changed meaning<br/>Further evidence read or authorized tool if needed<br/>Clarify / supported partial answer / abstain"]
    L7["7. Accept buffered response atomically<br/>Check knowledge, run, permission and cancellation<br/>Store answer + terminal state + publication sequence<br/>Stale result → bounded refresh or honest failure"]
    L8["8. Deliver or replay accepted result<br/>Answer + supporting sources + actual outcome<br/>Replay respects CURRENT exclusions<br/>Already delivered bytes cannot be retracted"]
    LIMIT["Proposed request limits — unmeasured<br/>4 answer-model attempts incl. repairs/retries<br/>6 follow-up reads · 1 external effect<br/>30-second ordinary-request deadline"]
    UI --> L1
    CLI --> L1
    L1 --> L2 --> L3 --> L4
    L4 -->|"resolved"| L5 --> L6 --> L7 --> L8
    L4 -->|"unresolved / failed"| HOLD["Keep learning HELD<br/>No dependent action or saved-success claim<br/>Ask for needed input, fail honestly,<br/>or provide an independent unsaved draft"]
    HOLD -->|"resume with needed input"| L3
    HOLD -->|"independent partial / error; learning stays held"| L7
    L6 -->|"more evidence / tool observation"| L3
    L7 -->|"stale; retry budget remains"| L2
    LIMIT -.- L6
  end

  subgraph MEMORY["3 · MEMORYSERVICE — BUILD · Logical subsystem inside the same application"]
    subgraph LEARN["A · MEMORY EXTRACTION AND ADMISSION"]
      JOB["One durable learning worker<br/>Read permitted source + justified adjacent context<br/>Held → queued → running → terminal/retry<br/>Attempt token fences stale completions"]
      EXTRACT["Model proposes atomic, attributed candidates<br/>Who said what, about whom, when and in what scope<br/>Preserve quotes, negation, intent and uncertainty<br/>Parse failure differs from successful empty extraction"]
      ADMIT["Retrieve related assertions; validate candidates<br/>Evidence spans · predicate/type/units · source revisions<br/>Policy, subject, time, scope and dependencies<br/>Valid JSON/span alone does not prove support"]
      OUTCOMES["Admission outcome<br/>Add · supported change/correction · link evidence<br/>Duplicate/no-op · conflict/unresolved · reject<br/>Rejection still leaves permitted source searchable"]
      EXTRACT --> ADMIT --> OUTCOMES
    end

    subgraph REPRESENT["B · REPRESENTATION, ENTITIES AND TEMPORAL UNDERSTANDING"]
      ASSERT["Versioned memory assertion<br/>Form + category + typed predicate/value + units<br/>Subject/speaker/attribution + derivation/dependencies<br/>Scope + polarity/modality + evidence + lifecycle"]
      CATS["12 overlapping labels in SHARED tables<br/>Entities · relationships · preferences · constraints<br/>Routines · goals · plans/tasks/commitments · decisions<br/>Progress/blockers · beliefs/ideas · vocabulary · resources"]
      TIME["Preserve time and identity meaning<br/>Event/validity ≠ capture ≠ availability/import time<br/>Unknown date/scope remains unknown<br/>Same name does not automatically merge people"]
      CHANGE["Supported updates preserve history<br/>Correction of mistake ≠ real-world change<br/>New import does not automatically replace current truth<br/>Task completion ≠ assertion supersession"]
      ASSERT --- CATS
      ASSERT --- TIME
      TIME --- CHANGE
      OUTCOMES -->|"accepted supported writes only"| ASSERT
    end

    subgraph CONTROLS["C · CORRECTION, FORGETTING AND USER CONTROL"]
      CTRL["Validate current remember/correct/forget/delete intent<br/>Resolve target + expected revision + trusted scope<br/>Explicit controls may bypass language interpretation<br/>Application creates committed/no-op/conflict receipt"]
      CORRECT["Remember / correct<br/>Commit supported assertion or revised interpretation<br/>Retain evidence and qualified historical values<br/>Invalidate affected indexes and answer dependencies"]
      FORGET["Forget<br/>Block selected knowledge and known supporting spans<br/>Suppress source fallback, vectors, aliases, derived artifacts<br/>and retained answer/replay content; rebuild surviving support"]
      DELETE["Delete source<br/>Also remove selected in-app original source content<br/>Report exact use-block / purge / retention status<br/>Exports, backups and provider retention are separate"]
      CTRL --> CORRECT
      CTRL --> FORGET
      CTRL --> DELETE
    end

    subgraph EVIDENCE["D · ONE PERMITTED-TEXT BOUNDARY"]
      ELIGIBLE["read_evidence / eligible_text<br/>Trusted user + source head/revision + visibility<br/>Exclusions + time/availability cutoff<br/>Return allowed text + original-span mapping"]
      RULE["Applies to EVERY history read<br/>Extraction · source/vector expansion · full-history baseline<br/>Inspection · neighboring context · summaries · replay<br/>After controls, even private-current re-reads apply exclusions"]
      SPAN["Evidence points to exact original field/revision<br/>Zero-based Unicode code-point offsets; end-exclusive<br/>Normalized chunks require original-offset mapping<br/>No safe partial projection → suppress affected chunk"]
      ELIGIBLE --- RULE
      ELIGIBLE --- SPAN
    end

    subgraph RETRIEVE["E · RETRIEVAL AND EVIDENCE SELECTION"]
      SEARCH["Candidate retrieval<br/>Source keyword + memory keyword using FTS5<br/>Optional source vector + memory vector search<br/>E5-small first candidate; BGE-M3 comparison remains open"]
      FUSE["Deduplicate and fuse candidates<br/>Proposed top 20 per list; RRF k=60; up to 40 fused<br/>Optional supported one-hop relation expansion<br/>20 entities / 40 evidence references; mark truncation"]
      COMPLETE["Recover distributed and complete evidence<br/>Read original decisive spans and bridge sources<br/>Counts/lists/change histories use paged enumeration<br/>Source fallback covers missed extraction; report gaps"]
      PACK["Pack evidence bundle<br/>Proposed 4,096-token evidence budget<br/>Source/memory revisions, spans, scores, conflicts<br/>Coverage/readiness + store-issued freshness token"]
      FUSE --> COMPLETE --> PACK
    end

    subgraph APPLY["F · CONTEXT APPLICATION, PERSONALIZATION AND UNCERTAINTY"]
      USE["Use memory only when relevant to current request<br/>Current instruction overrides remembered preference<br/>Supported recall, comparison, draft or checklist<br/>Personal claims require inspectable evidence"]
      UNCERTAIN["Choose supported behavior<br/>Enough evidence → answer; unnecessary unknown → omit<br/>Material ambiguity → one focused question / partial answer<br/>Absent evidence → abstain; skipped question ≠ confirmation"]
      USE --> UNCERTAIN
    end
  end

  subgraph STORAGE["4 · ONE LOCAL SQLITE DATABASE — BUILD · Schema below is a logical contract, not migrations"]
    DB[("SQLite · scoped relational tables<br/>Short transactions · parameterized SQL<br/>Foreign keys on each connection<br/>FTS5 + separately ready persisted vectors")]
    TABLES["Durable table groups<br/>owner_state: knowledge_rev / index_rev / publication_seq<br/>record_revisions + record_heads; memory_revisions + memory_heads<br/>evidence; entities/aliases/identity decisions/edges<br/>exclusions/permitted projections; search_documents/FTS/embeddings<br/>jobs/memory_decisions; runs/attempts/operations/responses"]
    INDEX["Rebuildable search representations<br/>Current permitted projection + source/memory revision<br/>Encoder/config revision, digest, dimension, normalization<br/>Lexical can work while vectors remain pending"]
    CACHE["Reuse policy<br/>Persist vectors; keep encoder loaded in persistent process<br/>Optional revision-checked RAM vector/map views<br/>Query, retrieval-result and answer caches initially OFF"]
    RECOVERY["Durability and recovery contracts<br/>State change + job enqueue commit together<br/>Same key/payload replays receipt; changed payload conflicts<br/>No LLM, encoding or external effect inside DB transaction<br/>Resume uses linked attempt; stale worker cannot commit"]
    DB --- TABLES
    DB --> INDEX --- CACHE
    DB --- RECOVERY
  end

  subgraph MODEL["5 · LANGUAGE / EMBEDDING ADAPTERS — BUILD; EXACT CONFIGURATION OPEN"]
    LLM["NVIDIA-hosted DeepSeek adapter<br/>HTTPX + validated versioned proposals<br/>Verify model ID, output/tool support and context limit<br/>Bounded timeout/retry; record tokens, latency and cost"]
    EMB["Local multilingual encoder candidate<br/>sentence-transformers + NumPy exact scoring<br/>Pin model revision, prefixes, tokenizer and dimensions<br/>Measure English / Hindi / Hinglish; cold and warm behavior"]
    CONFIG["Configuration and versioning<br/>NVIDIA_API_KEY; KIVI_LLM_BASE_URL; KIVI_LLM_MODEL<br/>KIVI_DB_PATH; KIVI_EMBEDDING_MODEL<br/>Pin runtime/dependencies, prompts, policies and retrieval config<br/>Secrets excluded from source data, traces and Git"]
    LLM --- CONFIG
    EMB --- CONFIG
  end

  subgraph TOOLS["6 · APPLICATION TOOLS — BUILD · First proposed effect: requested local artifact"]
    PREP["Prepare exact operation<br/>Registered tool + validated args + current authority<br/>Check designated directory, target and existing version<br/>Remembered intentions never authorize a new effect"]
    DISPATCH["Persist operation and admit dispatch<br/>Proposed → ready / waiting approval / rejected<br/>Recheck current authority/cancellation before dispatch<br/>No external exactly-once guarantee"]
    RECEIPT["Observe actual outcome<br/>Succeeded / failed / unknown + receipt/readback<br/>Unknown → reconcile before any repeat effect<br/>Cancellation after dispatch does not promise rollback"]
    PREP --> DISPATCH --> RECEIPT
  end

  subgraph PROOF["7 · OBSERVABILITY, EVALUATION AND REVIEW — BUILD"]
    TRACE["Inspectable decision trace<br/>Original input → candidate/admission decision → evidence<br/>Retrieved / changed / rejected memory → final behavior<br/>Versions, readiness, calls/tokens, latency, failures and cost<br/>Concise reasons; no private model chain-of-thought"]
    DATA["Create approximately 500 transcript records<br/>Recurring entities/events, distractors, missing metadata<br/>ASR disagreements, changes, ambiguity and multilingual cases<br/>Separate narratives/templates and keep gold labels out of ingestion"]
    EVAL["Proposed evaluation protocol<br/>80 reviewed questions: 30 development + 50 sealed<br/>50-source extraction audit: 20 development + 30 sealed<br/>Full-history / source lexical / source hybrid / typed memory<br/>Freeze candidate before sealed comparison"]
    QUALITY["Measure actual task quality<br/>Admission precision/recall; evidence and citation support<br/>Wrong person/time, unsupported claims, false abstention<br/>Useful personalization, observed effects, latency/DB growth/cost<br/>Thresholds are proposals, not achieved results"]
    INTEGRITY["Real application integrity suite still required<br/>Concurrent changes; disk restart/crash; stale jobs/results<br/>Forgetting in every path; alias/artifact/replay cleanup<br/>Cross-user scope; hostile history; duplicate/unknown effects<br/>Research probe does not replace these tests"]
    SUBMIT["Reviewer-ready submission<br/>User-authored Part One; complete code + normal-user UI/backend<br/>Schema/migrations, seed/corpus, generated evaluation results<br/>README + AI-use disclosure; RUN.md; environment example<br/>Fresh-checkout install/start/import/process/inspect/evaluate/reset<br/>One GitHub repository + exact final commit SHA"]
    DATA --> EVAL --> QUALITY --> SUBMIT
    TRACE --> EVAL
    INTEGRITY --> SUBMIT
  end

  DEFER["DEFER unless measured benefit / chosen use case<br/>Graph/vector servers · Redis · approximate indexing<br/>Answer caches · rerankers · recursive summaries · autonomous reflection<br/>Broad MCP/email/calendar/browser/reminder integrations<br/>Native speech recognition, production Kivi integration, hosting and Docker are optional"]

  DOCS -.-> OPEN
  DOCS -.-> IMPORT
  PROBE -.-> INTEGRITY
  OPEN -.-> UI
  INGEST --> DB
  INGEST --> JOB
  L5 -->|"only permitted released jobs"| JOB
  JOB --> ELIGIBLE
  ELIGIBLE -->|"permitted extraction content"| EXTRACT
  EXTRACT -.->|"model call"| LLM
  L3 -.->|"model call"| LLM
  OUTCOMES -->|"all decisions logged; accepted writes atomic"| DB
  ASSERT --> DB
  L2 --> SEARCH
  INDEX --> SEARCH
  DB --> ELIGIBLE
  SEARCH --> ELIGIBLE
  ELIGIBLE -->|"eligible retrieval candidates"| FUSE
  COMPLETE --> ELIGIBLE
  PACK -->|"evidence for interpretation"| L3
  L4 --> CTRL
  CORRECT --> DB
  FORGET --> DB
  DELETE --> DB
  CTRL -->|"actual control receipt"| L4
  INDEX -.->|"encoding work"| EMB
  L6 --> USE
  L6 -->|"bounded follow-up retrieval"| SEARCH
  UNCERTAIN --> L7
  L6 -->|"action proposed"| PREP
  RECEIPT -->|"observed result"| L6
  L1 -->|"persist run and private input"| DB
  L5 -->|"atomic projection promotion + job release"| DB
  L7 -->|"atomic publication"| DB
  L8 -->|"sources, controls, outcome"| UI
  L8 --> CLI
  L8 --> TRACE
  DB -->|"metadata only; content uses evidence gate"| TRACE
  ELIGIBLE -->|"permitted trace content"| TRACE
  RECEIPT --> TRACE
  DOCS -.-> DEFER

  classDef done fill:#E8F3E9,stroke:#39804B,color:#163D22;
  classDef probe fill:#E2F1F4,stroke:#28758A,color:#123D48;
  classDef build fill:#FFF3DA,stroke:#B48022,color:#49350E;
  classDef open fill:#F0E7F7,stroke:#8652A0,color:#432551;
  classDef deferred fill:#ECEFF1,stroke:#7B858B,color:#39454C;
  class DOCS done;
  class PROBE probe;
  class OPEN,LLM,EMB,CONFIG open;
  class DEFER deferred;
  class HIST,UI,CLI,IMPORT,INGEST,L1,L2,L3,L4,L5,L6,L7,L8,LIMIT,HOLD,JOB,EXTRACT,ADMIT,OUTCOMES,ASSERT,CATS,TIME,CHANGE,CTRL,CORRECT,FORGET,DELETE,ELIGIBLE,RULE,SPAN,SEARCH,FUSE,COMPLETE,PACK,USE,UNCERTAIN,DB,TABLES,INDEX,CACHE,RECOVERY,PREP,DISPATCH,RECEIPT,TRACE,DATA,EVAL,QUALITY,INTEGRITY,SUBMIT build;
```

Implementation order: resolve the leading journey and Part One status → durable import/source foundation → complete cited-answer path → selective memory and retrieval comparison → useful output/evaluation preparation → final interface → sealed evaluation and clean-checkout rehearsal.

Important qualifications: UI and CLI are alternative clients; the UI does not run through the CLI. Local storage still sends eligible context to the configured hosted model. The only freshness-token rebase exception is a trusted receipt for promotion of identical current text already seen by the current run, with no intervening knowledge/control change; otherwise refresh. Partial source suppression is use blocking, not physical erasure. The 12 category labels do not imply 12 databases.
