# Semantic-memory blueprint: research and ontology review

Research cutoff and access date: **6 September 2026**. Independently reviewed `END_TO_END_DESIGN.md` against primary papers and current official repositories. This is a proposed blueprint, not implementation or measured performance. No models were called, dependencies installed, or application files changed. Repository links below were inspected on their moving default branches; implementation must pin actual commits and recheck contracts.

**Decision:** retain the local SQLite-backed memory service and independent source search. Refine its ontology into a small, versioned assertion model with 12 overlapping content labels, explicit attribution/modality, uncertain time, and evidence-backed relationships. Keep generated associations and summaries distinct from factual assertions. Recent work provides useful construction and retrieval mechanisms; none of the reviewed evidence establishes that a separate graph engine or a framework replacement is best for this corpus.

## Dated primary-source review

The four entries marked **new** are the only additional papers taken forward from this search. All were publicly submitted before the cutoff; none is presented as an independently reproduced Kivi result. Dates come from arXiv submission histories, not search-engine relative-age labels.

| Source and verified date/version | Mechanism worth borrowing | Avoid importing as an assumption |
|---|---|---|
| [Mem0](https://arxiv.org/html/2504.19413v1), 28 Apr 2025, v1 | Extract candidates, retrieve related prior memories, propose operations, then persist; compare a relational graph variant separately | A new contradictory sentence does not necessarily justify deleting old evidence. Model-chosen ADD/UPDATE/DELETE/NOOP is not a sufficient lifecycle contract. |
| [Zep](https://arxiv.org/html/2501.13956v1), 20 Jan 2025, v1 | Source episodes, evidence links, separate event-valid and system-recorded timelines | Do not infer an exact date from an ambiguous phrase or treat later ingestion as later truth. Paper results, current Graphiti OSS, and managed Zep are different artifacts. |
| [A-MEM](https://arxiv.org/html/2502.12110v11), first 17 Feb 2025; v11 8 Oct 2025; arXiv identifies NeurIPS 2025 | Context descriptions, optional tags, and associative links can improve discovery; revise generated indexing metadata as new context arrives | Similarity links are not asserted real-world relationships. Evolving a note's context is not permission to rewrite its supporting source or silently change its factual claim. |
| **New:** [Hindsight](https://arxiv.org/html/2512.12818v1), 14 Dec 2025, v1 preprint | Separate world facts, agent experiences, synthesized observations, and agent opinions; retain/recall/reflect are different operations | The agent's inferred opinions do not become the user's beliefs. Confidence scores are not calibrated truth probabilities. Do not turn every conversation into autonomous belief reinforcement. |
| **New:** [SimpleMem](https://arxiv.org/html/2601.02553v3), first 5 Jan 2026; v3 29 Jan 2026, preprint | Compact contextual units, lexical/dense/structured indexing, and retrieval scope chosen for the question | Its semantic-lossless framing is not a guarantee that compression preserves every future answer. Coreference and date normalization must be allowed to remain unresolved. |
| **New:** [APEX-MEM](https://arxiv.org/html/2604.14362v1), 15 Apr 2026, v1 preprint | Typed subject/property/value assertions anchored to events; preserve conflicting history and resolve appropriate evidence at query time | Its 35-class ontology and multi-tool graph agent are unnecessary defaults for 500 records. Its append-only comparison is cross-system indirect evidence, not an isolated causal proof. Explicit user correction/forget controls still need synchronous effects. |
| **New:** [LycheeMemory V2](https://arxiv.org/html/2608.12990v1), 13 Aug 2026, v1 preprint | Batch coherent dialogue segments into typed records with entities, time and source links; retain raw-turn retrieval alongside structured routes | Topic-boundary detection and extra query planning are costs to evaluate, not free improvements. Its LoCoMo/LongMemEval-S results do not establish Hindi/Hinglish ASR reliability. |

Mem0 and the four new papers evaluate conversational-memory benchmarks, with differing models, evidence granularity, retrieval budgets, judges, and preprocessing. This review borrows mechanisms and limitations rather than ranking their headline accuracy/latency figures. The existing evaluation protocol remains the way to decide whether they help Kivi.

## Current OSS changes the comparison

**Mem0:** inspected the current [memory service implementation](https://github.com/mem0ai/mem0/blob/main/mem0/memory/main.py). `_update_memory` updates the vector store and then records history through a separate database call; entity cleanup is deliberately non-fatal in the inspected path. That does not prove the whole library unsafe, but it does mean Kivi cannot assume this path supplies its atomic evidence/history/invalidation contract. Its entity matching also uses embedding similarity as one merge signal; do not adopt a global similarity threshold as proof that two people are identical. Borrow the operation pattern, and retain application-owned validation and transactions.

**Graphiti:** the current [repository](https://github.com/getzep/graphiti) supports prescribed and learned entity/edge types and hybrid retrieval. Its [EntityEdge implementation](https://github.com/getzep/graphiti/blob/main/graphiti_core/edges.py) includes source episode IDs and distinct `valid_at`, `invalid_at`, `expired_at`, and reference-time fields. These are useful modeling precedents. The README distinguishes Graphiti from managed Zep's proprietary Context Graph Engine; do not describe all current Zep deployments as simply hosted versions of an interchangeable OSS graph backend. No graph engine was installed or profiled here.

**A-MEM:** the current [official system repository](https://github.com/WujiangXu/A-mem-sys) and [memory_system.py](https://github.com/WujiangXu/A-mem-sys/blob/main/agentic_memory/memory_system.py) contain note metadata, related-note lookup, and LLM-driven note evolution. This is a useful associative retrieval experiment. For Kivi, write generated context/tags to versioned search representations and record semantic changes as separate attributed assertions with evidence. Do not use note evolution as the mechanism for explicit forgetting or identity resolution.

**Hindsight:** the current [OSS repository](https://github.com/vectorize-io/hindsight) offers PostgreSQL/pgvector, embedded pg0 packaging, and Windows support. Therefore, rejecting it because it necessarily requires a separately managed PostgreSQL server would be inaccurate. It also supplies four retrieval routes, fusion and reranking. It is a serious reusable comparator, but adoption brings its memory API, extraction, consolidation, storage and operational behavior into the application.

The official [Retain documentation](https://hindsight.vectorize.io/developer/retain) identifies a material tradeoff: a document producing zero memories is still stored, but ordinary recall/reflect cannot find it; its recommended recovery is reprocessing with broader extraction. It also describes background observation consolidation after retain. Kivi should preserve independent permitted-source search and measure that background work instead of counting only foreground calls. A stored source must remain discoverable even when no durable assertion was admitted.

**SimpleMem:** its current [repository](https://github.com/aiming-lab/SimpleMem) uses LanceDB and supports Python integration or an optional MCP/Docker server; it is not inherently a remote vector-server requirement. In the inspected [memory builder](https://github.com/aiming-lab/SimpleMem/blob/main/simplemem/core/memory_builder.py), windows trigger LLM extraction and storage, with up to three generation/parsing attempts. Exhausted exceptions return an empty list. Its extraction prompt also requires pronoun/relative-time disambiguation. For Kivi, count window processing and retries, preserve uncertain referents, and distinguish successful no-op from failed extraction. A library wrapper alone does not provide those semantics.

**Practical conclusion:** Hindsight and SimpleMem challenge the claim that all structured memory requires building everything from scratch. They do not remove Kivi's need for scoped evidence, original-source fallback, explicit controls, resumability, or measurable ingestion cost. Keep the service interface independent of a backend. Reconsider framework reuse if adapting those contracts demonstrably costs less than the small local service; do not reject it solely on repository size or accept it solely on benchmark rank.

## Logical service, storage engine, graph and map

The semantic-memory service decides what a statement means, who it concerns, its evidential status, how it changes, and what a current request may use. SQLite persists the records and transactions. FTS/vector indexes find candidate evidence. Entity/relationship tables express explicit connections. These can coexist in one implementation.

An embedding answers which representations are similar under an encoder. It does not establish that Riya owns a project, that two Ri(y)as are the same person, or that an old address is current. A graph edge records a named, scoped relationship; it still needs evidence and correct extraction. A dictionary keyed by entity ID helps direct lookup but needs multiple versioned assertions to represent uncertainty, concurrent roles, and history. A graph display or mind map is a view over this information, not another authority. SQL can perform bounded traversal over relationship tables. [SQLite recursive graph queries](https://sqlite.org/lang_with.html)

Maintain two distinct link classes:

- **Asserted relations:** subject, named predicate, object, evidence, modality and time. Example: Riya is the user's sister; Riya owns Project Cedar. These may support an answer if every necessary connection is eligible.
- **Associative retrieval links:** related topic, similar wording, or LLM-suggested connection between notes. These only propose more evidence to inspect. They cannot support ownership, identity, causality or authorization by themselves.

A bounded traversal should check user scope, relation type, direction, applicable time and evidence at every edge. General knowledge such as Paris being in France can help expand a query; keep its origin separate from the source proving the user's visit. For complete lists or counts, enumerate the eligible set and acknowledge extraction gaps; top-k similarity and a visually connected graph do not establish completeness.

## Stable schema axes

Use the shared `records`, `memories`, `memory_evidence`, entity/link and job groups already proposed. Add the following explicit semantics; this is a logical contract, not a request for a separate table for every field.

| Axis | Proposed representation and invariant |
|---|---|
| Identity and authority | Application-assigned user scope, memory/source ID and revision. Models cannot change ownership, source roles, permissions or schema versions. A remembered instruction is not live tool authorization. |
| Memory form | `semantic`, `episodic`, or `procedural` describes how the representation is used. An ordinary past exchange/attempt is eligible episodic material; importance is not part of the definition. One source may support linked representations of different forms. |
| Derivation | Direct attributed statement, observed tool result, inference, or summary. Inference/summary rows reference their actual dependencies and cannot become independent corroboration. This is separate from memory form. |
| Attribution | Source speaker/author, subject entity or unresolved mention, and reported/quoted speaker where needed. A user reporting another person's belief is different from personally endorsing it. |
| Assertion payload | Subject, predicate, object/value kind, and typed value or entity reference, plus necessary qualifiers. Retain a human-readable statement. Exactly one object representation is selected; amount/unit/currency remain explicit when applicable. |
| Modality and polarity | Preserve actual/described, desired, intended, proposed, conditional and hypothetical meaning; preserve negation independently. Retain condition text/dependencies. Do not force quoted conditional statements into a mutually exclusive single label. |
| Time | Original phrase, reference date/timezone, uncertain event/validity interval and precision, plus recorded/accepted sequence. Distinguish unknown endpoints from explicitly open intervals. Do not turn `June` into an invented year. |
| Lifecycle versus task state | Assertion lifecycle: active, superseded, retracted or conflicted. Task/project status is separate: open, blocked, completed or canceled. A completed task can be a currently valid memory. |
| Evidence | Source revision, field, exact offsets, and support/contradiction role. Every admitted personal assertion has source support; every inference has dependency links. Valid offsets alone do not prove entailment. |
| Content labels and topics | Many-to-many labels from the registry below; separate free-form topic tags. Neither determines truth, source ownership, retention permission or a mandatory retrieval partition. |
| Search representation | Text/vector/tag version, input hash, encoder/preprocessing version, and dependency revisions. Search artifacts are rebuildable; admitted interpretations and explicit controls are durable records. |

Start with a modest entity-type registry: person, organization, project/task, place, event, resource, concept, and other. Preserve original mentions and supported aliases. Leave identity unresolved rather than merging on name alone. Use a small canonical predicate registry for operations requiring structured queries; keep original relation phrasing and an extensible payload for other knowledge. Version registry additions through normal application changes, not autonomous DDL or LLM-edited policy.

For events with multiple participants or qualifiers, use an event entity/record and participant roles instead of collapsing everything into a binary edge. The assertion model can represent ordinary facts directly and refer to an event when time, participants, cause or outcome matters. Decisions should link to the stated reason, not an invented causal explanation. A user belief is a fact about that person's reported view; its embedded proposition need not be accepted as world truth.

Code can enforce references, scope, payload types, explicit null/unknown handling, allowed transitions, expected revisions and suppression. Semantic support, correct subject resolution, whether two assertions truly conflict, and whether a callback is appropriate remain model/human-evaluation questions. No fixed ontology eliminates those uncertainties.

## Proposed 12-label registry

These are the existing proposed content labels supplied for this design cycle, not twelve disjoint cognitive memory types. Preserve their deliberately overlapping meaning. A row may have several labels, and no label is required for original-source search.

| Label | Useful contents | Boundary that the schema must preserve |
|---|---|---|
| 1. Entities / attributes / capabilities | User's role, device ownership, another person's expertise | Stated skill is not independently verified proficiency; subject is explicit |
| 2. Relationships / roles | Sister, colleague, project owner, membership | Direction, identity, project context and validity; similarity is not identity |
| 3. Preferences / priorities | Preferred explanation style, tradeoffs, ranked wants | Explicit versus inferred, strength/context, current instructions and changes |
| 4. Constraints / requirements | Budget, deadline, access requirement, excluded option | Binding requirement versus preference; scope and expiration |
| 5. Routines / patterns | Recurring schedule or repeated behavior | Stated routine versus inferred pattern; exceptions and recurrence |
| 6. Goals / desired outcomes | Finish a portfolio, learn a language | Desired outcome does not imply a plan, deadline, commitment or authorization |
| 7. Plans / tasks / commitments | Tentative itinerary, assigned task, promise to send | Distinct subtype/modality, responsible actor, due time and execution state |
| 8. Decisions / stated reasons | Chosen venue and the user's explanation | Decision occurrence versus current choice; stated reason versus inferred cause |
| 9. Progress / blockers / open issues | Draft complete, waiting for Riya, unresolved question | Issue/task state separate from assertion lifecycle; uncertainty remains open |
| 10. Attributed beliefs / ideas / hypotheses | A person's view, speculative explanation, proposed idea | Attribution and epistemic status; never flatten hypothesis into established fact |
| 11. Personal vocabulary / concepts | An abbreviation, nickname, user's meaning of a term | Scope and competing senses; observed alias does not prove entity identity |
| 12. Resources / references | File, document, URL, source named in discussion | Pointer identity/version and provenance; mentioned is not fetched, endorsed or authorized for disclosure |

A resource can concern a goal; a commitment can follow a decision; a routine may reflect a preference. Classifying these into separate physical stores would make cross-category questions harder. Topic labels such as travel/work are additional facets. A procedural representation may be a reusable checklist or user-requested response rule; code/tool permissions remain owned by the harness. Do not silently compile a remembered sentence into executable behavior.

## Concrete treatment of the Jaipur example

For “Riya is my sister” and “Update my Jaipur trip's total hotel budget from INR 10,000 to INR 6,000,” retain separate assertions: the supported family relationship, the trip's earlier budget, and the new scoped budget. Label the budget as a constraint and possibly a plan-related item. Store numeric amount/currency and `total hotel budget`, rather than an unqualified `budget` attribute on the user.

Link the explicit change to its prior assertion and source. Keep historical meaning available while current queries select the revised state. The new amount does not prove the user booked a hotel, paid INR 6,000, or wants Kivi to send Riya anything. If another Riya is mentioned in work records, leave the identities separate until evidence resolves them. A generated trip summary references these assertions; it cannot erase their disagreement, supersession, or forgetting controls.

## Construction choices and experimental unknowns

Borrow segment/window batching as an **optional construction optimization**, especially from SimpleMem and LycheeMemory V2. Only group records with justified conversational continuity; adjacency across imported apps is insufficient. Keep current input and lexical source search immediately available, flush bounded pending segments on a declared timeout/size rule, and never delay explicit remember/correct/forget acknowledgment behind ordinary batching. Compare per-record versus bounded same-session batches on existing development cases before adopting semantic boundary detection or another LLM planner.

The following remain empirical and should use the existing small evaluation protocol, not a new architecture grid:

1. Does typed extraction add supported recall or useful personalization beyond source-only hybrid/full history, and what valid information does it miss?
2. Does one or two hops of **asserted** relationships improve multi-record questions after matching evidence budgets? Compare with those same edges disabled to isolate representation from extraction quality.
3. Do optional content labels improve browsing/retrieval after measuring label drift and overlap? Their stable schema role is already decided; their retrieval weight is not.
4. Does batching reduce actual extraction calls/tokens without harming names, negation, time, current-turn controls, or record-attributed provenance? Count retries and background consolidation.
5. Can the selected DeepSeek endpoint reliably preserve uncertainty and emit the schema in English/Hindi/Hinglish? Structured-output validity is a separate metric from semantic accuracy.
6. Would a pinned Hindsight or SimpleMem adapter satisfy source access, corrections, deletion, cost and laptop-operation requirements with less engineering? This remains open; neither was run here.

Do not add learned opinions, automatic summary evolution, or a graph server merely to claim coverage of modern memory research. The implementable blueprint is already rich enough: immutable permitted evidence, versioned attributed assertions, controlled state changes, separate semantic/episodic/procedural representations, optional overlapping labels, and lexical/vector/relationship retrieval over the same scoped store.
