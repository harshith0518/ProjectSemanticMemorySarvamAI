# Semantic-memory blueprint: storage, placement and caching audit

Verified 6 September 2026. Reviewed the latest `END_TO_END_DESIGN.md` and current primary documentation linked below. No product implementation, installation, model request or benchmark. An isolated executable storage-contract probe accompanies this research. This note supplies implementation contracts and contrary cases; it does not claim to have read entire commercial books or establish a universally best database.

## Decision: where semantic memory lives

The initial **memory service is a Python module inside the Kivi application process**. It owns import, admission, retrieve, inspect, correct and forget operations. The database stores its state; an LLM adapter helps interpret language. A CLI, persistent REPL and later HTTP/UI adapter can call the same service functions. “Service” here means an application boundary, not a required network daemon or microservice.

Use one local SQLite file for source records, accepted interpretations, user controls, relationships and derived search representations. An in-process worker processes durable jobs. On an ordinary one-shot CLI exit, queued jobs remain on disk but do not keep executing: document `process --resume`, an explicit drain option, or the persistent REPL/server lifecycle. Do not silently suggest work continues after its host process ends.

SQLite's stated strength is application-local storage with little administration. It permits many readers but a single concurrent writer. A server may safely use a local SQLite file behind an application API; clients must not share the file over a network filesystem. This fits the present assignment assumption, not every future hosted deployment. [SQLite appropriate uses](https://sqlite.org/whentouse.html)

## Four compatible representations

| Representation | Meaning for Kivi | Initial implementation |
|---|---|---|
| Tables | Durable structured records that can be filtered, joined and revised | SQLite tables with explicit indexed fields and extensible JSON/text |
| Maps | Fast lookup from a known key to an item | Ordinary indexes or an optional in-process dictionary, such as entity ID to display name |
| Graph | Entities connected by supported relationships | Entity/link tables plus bounded joins/recursive queries |
| Vectors | Numerical representations used to find similar meanings | Revision-labelled vector rows and optional exact scoring over a RAM matrix |

These are not competing memory types. A table can store graph edges or vectors; a map can index graph nodes. A drawing of nodes is a visualization, not evidence that graph storage is superior. SQLite explicitly documents recursive graph queries. Vector proximity is neither factual confidence nor an identity proof. [SQLite graph queries](https://sqlite.org/lang_with.html), [pgvector similarity search](https://github.com/pgvector/pgvector)

Keep query-critical fields explicit: user/scope, subject, predicate, category, status, temporal bounds, source revision and value type. Retain text for meaning and optional metadata for extensibility. Amounts need units/currency and dates need uncertainty; an opaque paragraph or untyped JSON-only schema makes exact filters and timelines unnecessarily difficult. The 12 proposed categories share a schema rather than creating 12 disconnected databases.

## Authority and retained interpretation

1. **Original records and explicit user controls:** preserve what was said and its provenance. Role, origin, attribution and modality determine what it can support. Assistant prose is available for conversation continuity but cannot automatically establish personal facts.
2. **Accepted interpretations and decisions:** persist admitted memories, evidence and revisions. They are derived but operationally durable: a new LLM run is not guaranteed to reproduce them. Human corrections must survive any index rebuild.
3. **Graph projections and indexes:** maintain links from accepted supporting assertions; avoid a second independently writable truth store. FTS and vectors can be rebuilt from current permitted inputs.
4. **Caches:** reuse computations under explicit dependency rules. Deleting a cache should affect speed, not erase the only evidence or accepted memory.

This adapts the primary-versus-derived-data distinction in Kleppmann's articles. It does not require Kafka, separate databases or putting LLM logic into SQL procedures. His materialized-view discussion also explains why precomputing a useful representation and placing it near the source can help while increasing maintenance obligations. [Kleppmann on logs and dual writes](https://martin.kleppmann.com/2015/05/27/logs-for-data-infrastructure.html), [derived data and materialized views](https://martin.kleppmann.com/2015/03/04/turning-the-database-inside-out.html)

## Minimal revision and transaction contract

Use logical revision counters, not wall-clock timestamps, for concurrency. Event time, record time and import time remain separate meaning-related metadata.

| Counter | Advances when | Purpose |
|---|---|---|
| Per-source revision | Source content/eligibility changes | Bind evidence spans and processing jobs to exact input |
| Per-memory revision | Interpretation, scope, status or support changes | Reject stale updates; retain history |
| Per-user `knowledge_rev` | Eligible evidence or admitted knowledge changes, including corrections/exclusions | Detect potentially stale retrieval/context, including newly arrived contradictory evidence |
| Per-user/encoder `index_rev` | The eligible vector/search representation changes or new vectors become ready | Validate RAM mirrors and cached retrieval coverage |
| Per-user `publication_seq` | A control or buffered answer is accepted | Order completed controls and response acceptance |

This is a proposed minimal scheme, not a library-provided guarantee. `knowledge_rev` can initially combine content and control generations; split them only when measurements justify the added complexity. Ordinary output logging should not increment knowledge revision unless it creates newly eligible evidence. A coarse counter may cause unnecessary retries during active ingestion; track that rate and batch/offline-process imports before increasing concurrency. If a counter changed, comparing only the originally cited rows is insufficient: new contrary evidence may have appeared. Refresh relevant retrieval or regenerate under a bounded retry policy.

Transaction sequence:

- **Receive:** save the source identity/revision and pending stage jobs together. Update its permitted lexical projection in the same transaction. Stable upstream IDs handle duplicate import; text hashes alone must not merge distinct real events.
- **Read:** gather one coherent snapshot of sources, memories, exclusions and versions. Close the transaction before LLM/embedding/network work.
- **Admit:** start a short write transaction, validate expected revisions and job attempt, then commit accepted memories, evidence, graph projections, FTS changes, decisions, knowledge revision and vector jobs together.
- **Index:** compute outside the transaction; commit only against current source/memory/projection revisions. Complete the job and advance index revision with its output. Obsolete vectors never count as ready.
- **Publish:** within one short transaction, check current controls/evidence, assign publication sequence, save the permitted response and terminal run state. Deliver the committed result afterward. A later forget can invalidate retained/displayed copies; network delivery is not an SQL transaction.

Give jobs unique input/stage/configuration identities and states such as pending, running, succeeded, failed and superseded. Claims need an attempt token if they can be reclaimed; a stale worker cannot commit merely because it once held a lease. Retry effects in SQLite can be idempotent; external API charges can repeat after an ambiguous timeout. Scope all relevant keys/joins by user and use parameterized SQL rather than model-generated mutation statements.

SQLite snapshot isolation does not make an existing read transaction observe later corrections. Start fresh validation transactions. Enable foreign keys on every connection, verify FTS synchronization with actual `MATCH` queries, configure bounded busy handling, and keep model work outside transactions. FTS5 external-content tables require application/trigger maintenance and an initial rebuild for existing rows. [SQLite isolation](https://sqlite.org/isolation.html), [SQLite pragmas](https://sqlite.org/pragma.html), [FTS5 external-content behavior](https://sqlite.org/fts5.html)

## Forgetting must cover original-source fallback

The most important missing concrete boundary is a shared **eligible-text projection**. Every retrieval path, full-history baseline, neighborhood expansion, extraction job and context assembler must read through it. Otherwise a forgotten memory can disappear from `memories` while its original full record or neighboring chunk immediately restores it.

The projection applies user/scope restrictions, source lifecycle and exclusions before exposing text. For span-level exclusions, omit or mask excluded spans while preserving a mapping to original offsets. Specify the offset unit, preferably Unicode code-point positions in the exact original field; offsets into normalized embeddings or UTF-8 bytes are different. Exclude a whole affected chunk/source temporarily if safe partial reconstruction is unavailable, then rebuild from surviving permitted text. Do not retain its old embedding or graph summary as a usable proxy.

Maintain separate evidence eligibility for assistant/tool records: tool observations can establish what the tool observed at a time, not arbitrary personal truths or fresh authority. A forget request that repeats the fact should not become a new eligible source of that fact. Review retained prompts, candidate quotes, aliases, cached inputs and generated traces as well as the primary tables.

Logical suppression from use, deletion from the application store and forensic erasure are different promises. Document external source files, exports, backups and provider retention separately. Never silently edit unrelated user-owned files. Opaque source/span exclusions prevent known-source reprocessing; they cannot identify every future paraphrase without broader semantic collection restrictions.

## Explicit cache policy

| Layer | Initial policy | Validity requirements |
|---|---|---|
| Document/memory vectors | Persist when dense retrieval is enabled | Source/memory/projection revision, encoder version, input hash, dimension and normalization; rebuild on mismatch |
| Encoder in RAM | Keep loaded for persistent REPL/server | Pinned model configuration; process lifetime; measure cold starts separately |
| Vector RAM mirror | Optional after measuring DB-load/scoring time | User, encoder and index revision; rebuild/swap coherently and check current eligibility before use |
| Query-encoding cache | Initially off; bounded exact-input cache if repetition helps | Actual encoder input, model/preprocessing version, user isolation policy and purge rules; no semantic equivalence guessing |
| Retrieval-result cache | Off initially | Query/working-context interpretation, scope, knowledge and index revisions, retrieval configuration, relative-time dependencies |
| Exact/semantic final-answer cache | Off | Too many mutable evidence, time, instruction and tool dependencies for the present benefit |
| Provider prompt cache | Do not assume support | Verify actual NVIDIA endpoint, eligibility, billing, retention and hit telemetry; use current context, never an old answer as if freshly derived |

**Can a cache in the same normal DB help? Yes, when it avoids an expensive computation.** A SQLite key-value table containing a query embedding can survive CLI restarts and avoid encoding it again. It does not avoid SQLite lookup or model-loading work on a miss, and its writes may compete with the single writer. An extra cache of an already cheap indexed SQL lookup may add more overhead than it removes. Avoid updating persistent `last_used` on every hit; expiry checks and batched statistics can avoid turning every read into a write. SQLite already has a page cache; it is distinct from cached model results. [SQLite page-cache controls](https://sqlite.org/pragma.html#pragma_cache_size)

Provider prompt caching reuses overlapping inference work; answer caching reuses a completed result. Huyen's public platform article distinguishes prompt, exact and semantic caches, but its historical provider examples are not proof of current NVIDIA support. [Huyen on caching](https://huyenchip.com/2024/07/25/genai-platform.html#step-4-reduce-latency-with-cache)

TTL permits staleness until expiry. Immediate correction/forget semantics need revision invalidation and authoritative checks, including after reconnect/restart. Redis documents tracking/invalidation costs and stale-data hazards when messages are missed. A network cache for a local SQLite workload needs measured benefit; it is not inherently faster. [Redis client-side invalidation](https://redis.io/docs/latest/develop/reference/client-side-caching/)

## Current library evidence and the strongest contrary case

- **LangMem:** its core transformation functions are storage-independent; higher-level stateful integration uses LangGraph stores. This supports separating interpretation logic from persistence. Its defaults and memory-importance heuristics still require product evaluation. [LangMem core concepts](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/)
- **Graphiti:** current README lists Neo4j, FalkorDB, Neptune and deprecated Kuzu; it also documents an embedded FalkorDB option. A graph alternative therefore does not always require a separate network process, though Windows/runtime compatibility must be tested. The README distinguishes OSS from Zep's proprietary hosted engine; hosted speed claims are not local benchmarks. [Graphiti](https://github.com/getzep/graphiti)
- **Mem0:** current v2-to-v3 migration docs remove external graph-store integration from OSS and place graph memory in Platform. OSS extraction is ADD-only; its hybrid BM25/entity signals rerank semantic candidates rather than expanding the candidate set. Older Mem0-plus-Neo4j diagrams do not describe the current documented OSS path. Pin the version before evaluating. [Mem0 migration guide](https://docs.mem0.ai/migration/oss-v2-to-v3)

The strongest argument against our own design is that **500 records may not justify comprehensive extraction or a rich assertion graph at all**. Full allowed history or hybrid source retrieval could deliver better coverage with fewer unsupported transformations and lower development cost. Keep these real baselines, retain user controls/provenance, and add only the memory structure that improves useful behavior. This challenges both a dedicated graph database and unnecessary complexity inside SQLite.

The strongest argument against SQLite is a different deployment requirement: multiple application hosts, significant concurrent writes, established hosted PostgreSQL infrastructure, database-level access controls or operational recovery requirements. PostgreSQL with pgvector keeps relations and vectors together. Its default Read Committed isolation differs from SQLite's serialized writes; moving databases requires revisiting snapshot/locking/retry assumptions, not merely changing a connection string. [PostgreSQL isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [pgvector](https://github.com/pgvector/pgvector)

## Change gates and remaining decisions

Adopt an alternative only after testing the same eligible corpus, queries, evidence and endpoint budget. Graph database tests must preserve the same edges to separate better extraction from engine effects. Approximate-vector tests must measure filtered nearest-neighbor recall and task evidence coverage. Cache replay must include realistic repetition, misses, invalidation and correction/forgetting, with net end-to-end savings.

Before development settles configuration: choose one-shot versus persistent command behavior; specify the eligible-text projection; fix revision/offset contracts; declare warm retrieval measurement boundaries; and pin tested dependency versions. The current proposal's 500 ms warm retrieval aspiration should explicitly include query encoding and context assembly or report them separately.

For SQLite deployment, keep the DB on local durable storage and use a verified backup procedure. WAL permits concurrent readers with one writer; prolonged reads impede checkpoints. Verify a runtime containing the documented WAL-reset fix (3.51.3 or an official backport). Use the backup API rather than copying only an active `.db` and losing uncheckpointed WAL state. These are operational checks, not reasons to add a distributed service. [SQLite WAL](https://sqlite.org/wal.html), [SQLite backup API](https://sqlite.org/backup.html)

Required integrity scenarios include stale admission/index commits, duplicate import, retry after commit, worker restart, partial-index coverage, forget during buffered generation, masked-source fallback, graph-projection agreement, RAM-mirror invalidation and scoped retrieval. Passing these establishes tested lifecycle behavior; answer usefulness and factual accuracy remain separate empirical questions.

## Isolated executable contract probe

The accompanying [stdlib Python probe](validation/atomic_memory_probe.py) models a subset of these contracts in fresh in-memory SQLite databases. Its [machine-readable results](validation/atomic_memory_results.json) report 12/12 cases passed using Python 3.12.14 and SQLite 3.53.1. It exercises actual FTS5 maintenance and SQL transactions, including rollback of memory/evidence/index/job changes, idempotency conflicts, composite ownership foreign keys, stale admission, held-input visibility, forgotten-span source fallback, stale vector/cache eligibility and atomic response publication/replay.

Three negative controls show why the contracts matter: reading the raw table bypasses held-input privacy; it also exposes a suppressed span; unchecked response persistence accepts an obsolete response. The span scenario includes mixed English/Hindi text to exercise original Unicode-code-point offsets, without claiming Hindi retrieval quality.

Adversarial review then added a case that initially failed: forgetting a span before a held source had a search document allowed later source release and private re-reading to restore that span. A common exclusion-aware projection helper fixed both routes. The [review record](validation/REVIEW.md) preserves the sequence: initial 10/10, new case 10/11 with the exact failure, then 11/11 after the repair. The regression case remains in the suite. A twelfth case subsequently verified the narrow code-issued token rebase for promotion of unchanged already-seen input: unrelated changes before/after promotion and altered projections reject. The final suite is 12/12.

This validates the small model implemented by the probe, not the unbuilt Kivi application. Interleavings are injected sequentially; real concurrency, disk/WAL failure, worker restart, graph/alias cleanup, model extraction, semantic judgments, MCP, network delivery, physical erasure and performance are not tested. Response dependencies are deliberately simplified to one source, with conservative invalidation. Full-system evaluation must still test the actual implementation.
