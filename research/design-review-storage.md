# Storage and consistency review for Hey Kivi

Reviewed 6 September 2026. Planning only: no application code, benchmarks, dependency installation, or model calls. Reviewed the current architecture proposal and storage/data-system notes, then checked the primary sources linked below. These are design judgments for roughly 500 source records and a two-day, CLI-first assignment, not proven performance results.

## Recommendation and vocabulary

Use one local SQLite database behind the memory service. Store original messages, supported memory assertions, evidence links, user control events, and processing state there. Add FTS5 and initially optional application-side exact vector scoring. Represent useful relationships with entity/edge tables; a graph is a data model before it is a database product. SQLite explicitly supports recursive graph queries. [SQLite use cases](https://sqlite.org/whentouse.html), [SQL graph traversal](https://sqlite.org/lang_with.html)

| Layer | Example | Authority and lifecycle |
|---|---|---|
| Original records | User utterance, raw/formatted transcript pair, assistant response, tool result | Preserve role, origin and source revision. A stored assistant claim is not evidence that the user actually did something. |
| Accepted memory | A scoped preference or promise with source spans | Durable, versioned interpretation. Corrections and admission decisions must be inspectable. |
| Relationship projection | User → sister → Riya | Supported by accepted assertions; do not create an independently editable second truth store. |
| Search representations | FTS tokens, document/memory vectors | Rebuildable from permitted current records. Embeddings help find evidence; they are not evidence or certainty. |
| Optional cache | Reused query encoding or retrieval result | A reusable result with an explicit validity key and eviction rule; never the only copy. |

The proposed 12 information categories can be labels/subtypes on shared assertion records. They do not require 12 databases or 12 disconnected search silos. Entity type, memory category, topic, time, scope and evidence are separate dimensions. Preserve unclassified original material for source retrieval.

Derived does not mean freely disposable: regenerate embeddings safely, but preserve accepted extraction results, human corrections and their versions for reproducibility. Re-running an LLM over the same source need not recreate identical interpretations. An explicit user correction is itself new authoritative input, not merely a cached model output.

## Tables, graph and vectors are compatible

For a small corpus, exact similarity over compatible normalized vectors is a strong starting candidate. The sentence-transformers documentation describes direct scoring for small corpora. Actual viable size and latency depend on hardware, embedding dimension, source expansion and concurrency; its illustrative corpus range is not a latency guarantee. For scale intuition only, 5,000 vectors × 384 dimensions × 4 bytes is 7.68 MB before metadata/model memory. [Sentence-transformers semantic search](https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html)

A graph engine becomes an experiment when a substantial workload needs variable-length constrained paths, graph algorithms, or rapidly changing relationship patterns that are difficult to maintain efficiently in SQL. It does not resolve entity ambiguity, temporal errors or unsupported extraction by itself. Neo4j's own documentation warns that broad variable-length paths can produce huge path sets; traversal still needs bounds and predicates. Compare identical entities, edges and evidence in SQL and the candidate graph engine before attributing an improvement to storage. [Neo4j variable-length paths](https://neo4j.com/docs/cypher-manual/current/patterns/variable-length-paths/)

Graphiti is a useful temporal-memory implementation to study: it combines episodes, entity/relationship facts, temporal validity and hybrid retrieval. Its repository distinguishes the open-source framework and external graph backend from Zep's managed proprietary engine. Hosted performance claims do not establish local Graphiti performance or compatibility with the selected model endpoint. [Graphiti repository](https://github.com/getzep/graphiti)

For a hosted service with independent concurrent writers or multiple application hosts, evaluate PostgreSQL plus pgvector. pgvector provides exact search by default and approximate indexes optionally. Approximate-neighbor recall means retrieval of mathematically nearest vectors, not correctness of memories or answers; filters and tenant partitioning require their own evaluation. [pgvector documentation](https://github.com/pgvector/pgvector)

## Commit and freshness contracts

1. **Input receipt:** one short transaction records a stable user/source/revision identity, original content, lexical indexing work and durable processing jobs. Content hashes detect unchanged input, but identical text from separate real events is not automatically one event.
2. **Explicit control:** requests to remember, correct or forget must durably commit the applicable control state before claiming completion. If interpretation is unresolved, acknowledge that limited outcome honestly. Ordinary opportunistic extraction may continue in the background. The current utterance stays available to the current answer even before extraction completes.
3. **Model work:** extraction and embedding calls happen outside transactions. Capture the relevant source, memory and exclusion versions beforehand. The LLM proposes typed changes; application code validates scope, evidence, revisions and permitted transitions.
4. **Admission:** in one transaction, commit accepted assertions, evidence, supported relationship projections, lifecycle changes, lexical index changes and queued vector work. FTS5 external-content tables require explicit synchronization, commonly triggers, and an initial rebuild when attaching to existing content. A normal SELECT passing is not proof that MATCH is consistent. [FTS5 external-content pitfalls](https://sqlite.org/fts5.html#external_content_table_pitfalls)
5. **Late results:** before writing a model result, compare captured versions to current versions inside the commit transaction. Reject stale work and commit job completion with its result. Unique stage/input/configuration keys prevent duplicated database effects; an ambiguous external timeout can still cause repeated API charges. [Kleppmann on dual writes](https://martin.kleppmann.com/2015/05/27/logs-for-data-infrastructure.html), [storage-enforced fencing principle](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
6. **Partial indexing:** lexical and original-source retrieval remain available. Dense results must reference current permitted revisions; missing vectors mean incomplete dense coverage, never permission to use obsolete vectors. A worker crash cannot leave a record permanently marked complete without its output.
7. **Answer publication:** fetch evidence, release the read transaction, generate a buffered answer, then validate against a fresh version before accepting/publishing it. SQLite snapshot reads do not automatically see concurrent corrections. Serialize the final acceptance step with user control writes; define the ordering contract instead of promising that a last-minute SELECT removes every possible race. A response accepted after a completed forget must exclude its removed evidence. Already transmitted text cannot be recalled; streaming requires cancellation and a separate, tested policy. [SQLite isolation](https://sqlite.org/isolation.html)

Keep database writes short and initially use one worker. Deletion must cover copied quotes, candidates, relation labels, generated context, vector rows and traces as applicable. Logical exclusion from future use is distinct from physical erasure of backups, provider requests or source files. Rebuild from surviving allowed evidence only. These are necessary application semantics, not features obtained automatically by choosing a graph database.

## Cache decision

Initially keep the embedding model loaded during a service session and precompute document vectors. A CLI process that exits after each question cannot preserve an in-process model across those invocations; benchmark that cold path or offer a persistent REPL/service later. The stored vector index persists either way.

Start without persistent answer caching. A short-term conversation window is working context, and “recent” does not mean “more true.” Add a bounded query-embedding cache only when repeated encodings materially contribute to measured latency. Key it by exact normalized input, preprocessing/model version and relevant isolation policy. Retrieval/answer caches additionally need user/scope, history and exclusion generation, index readiness, policy/model configuration, and any time/external-tool dependency. Time-dependent answers such as “what is due tomorrow?” cannot safely use only query text and corpus version.

TTL alone permits stale results until expiry. Redis documents both invalidation overhead and stale-data hazards when invalidation delivery fails. The Kivi design should retain a fresh authoritative version check, even when using cached candidates. Prefer a small in-process cache before adding a network cache to a local database workload. [Redis cache invalidation reference](https://redis.io/docs/latest/develop/reference/client-side-caching/)

## Measurable adoption and migration gates

Set the target laptop, expected concurrent activity, memory budget and p95 retrieval budget before comparing variants. Separate query encoding, DB/graph work, vector scoring, model generation and background processing lag; report cold and warm runs with sample counts.

| Proposed addition | Evidence required before adoption |
|---|---|
| Typed extraction | Better evidence coverage, supported answers or useful personalization than original-source retrieval/full-history baselines, after accounting for ingest cost and admission errors. |
| Graph expansion | Improvement on held-out multi-source relationship questions, with exact source support and no increased false identity merges. |
| Graph database | Same graph/evidence workload exceeds the SQL traversal budget after sensible indexes/bounds, and the candidate meets it with acceptable maintenance/setup cost. |
| Approximate vector index | Exact scanning exceeds the declared latency/memory budget at measured expansion; approximate recall and filtered evidence coverage remain acceptable. |
| PostgreSQL | Sustained write contention, busy failures, queue lag or required multi-host operation exceeds the agreed service contract. Row count alone is insufficient. |
| Cache | Replay of realistic repeated queries shows material end-to-end savings after lookup/invalidation overhead; correction, deletion, time and scope tests still pass. |

Before any user-facing memory claim, require deterministic integrity scenarios: repeat import; crash between source and worker stages; retry after commit; correction during extraction; forget during a buffered answer; restart during vector rebuild; relationship-projection consistency; and scope isolation. All expected invariants must pass. These checks establish lifecycle correctness, not answer accuracy, which needs a separate labeled evaluation.

The main gaps in the previous proposal are explicit control-write acknowledgment, graph projections having one authority, cold CLI process behavior, time-dependent cache validity, and a precisely stated answer-publication race contract. The overall one-database recommendation remains justified; no speedup or quality advantage has yet been measured.
