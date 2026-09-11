# Visual guide: references and evidence limits

Sources checked: **11 September 2026**. This is an AI-assisted planning reference register, not an implementation or evaluation report.

Generated from `tools/visual_guide_sources.py` by `python tools/build_visual_guide.py`. Edit the source data and regenerate the PDF and this register together.

The PDF links to primary technical sources where they support the mechanism shown, the assignment where it defines requirements, and project documents where a rule is our design choice. Public sources were revisited for this revision; newly added explanations are supporting references, not a claim that every source originally determined our decisions. Provider documentation does not establish account access, quality or cost. No live-model or application result is claimed.

## Assignment brief

Source: **Kivi_Golden_Goose_Task_Final.pdf**, seven pages, supplied in the parent planning workspace at `../reference/Kivi_Golden_Goose_Task_Final.pdf` relative to the repository root. This is a local source, not bundled in this repository and not assigned an invented public URL. Page numbers below are physical PDF pages, starting at 1.

SHA-256: `9c30ac90c80b77118438c05e72c9539d166c38fd8f949ce8cb140bba6550937a`.

| Locator | What the brief supports |
| --- | --- |
| Page 2, introductory definition | Durable understanding of preferences, facts and continuing user context. |
| Page 3, Begin with the use case | "Semantic memory may make factual, episodic, and preference-level understanding possible." The applicant chooses which forms matter for the product. |
| Page 4, Build the complete experience / Build the system beneath it | Ordinary-user UI; transcript replay is allowed; real backend state, persistence, retrieval and model decisions; relate factual, episodic and preference-level understanding to the chosen product. |
| Pages 4-5, Prove it yourself | Approximately 500 development records with raw/formatted content and metadata; inspect the complete pipeline, provenance, behavior and measurements. These are observations, not 500 evaluation questions. |
| Page 5, Our evaluation | Reviewers examine learned facts, preferences and episodes on their own corpus. |
| Page 6, Our evaluation / submission requirements | Recover distributed information, support answers with original interactions, avoid unsupported answers, and provide reproducible project artifacts. |

**Scope interpretation:** Kivi includes useful reported episodes alongside reusable facts and scoped preferences. Automatic procedural learning is deferred by our plan, not prohibited by the brief. Content categories do not require separate databases. The narrower terminology in the LangChain source explains the categories; it does not override the assignment's broader product term.

## Page-by-page reference map

Each page has three clickable source cards. The cards identify the type of support; this register records the limits. Page 12 intentionally cites our own Private requirements and tests, because an external framework does not guarantee our proposed privacy contract.

### Page 01: The whole plan, one visual language

- **BRIEF**: [Assignment scope: pp. 3-5](#brief_scope) - Includes factual, episodic and preference-level understanding; choose a useful product scope.
- **PROJECT DECISION**: [Kivi implementation plan](#plan) - Proposed milestones, scope cuts, approval boundaries and the minimum complete reviewer journey.
- **PROJECT DECISION**: [Kivi requirements and open choices](#decisions) - Defines eligible evidence, Normal/Private, Correct/Forget and proposed implementation choices.

### Page 02: Semantic memory: assignment scope + terminology

- **BRIEF**: [Assignment scope: pp. 3-5](#brief_scope) - Includes factual, episodic and preference-level understanding; choose a useful product scope.
- **PRIMARY SOURCE**: [LangChain memory concepts](#langchain) - Separates facts, experiences and instructions; explains thread state, stores and memory writing.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 03: One backend, several ways to use it

- **PRIMARY SOURCE**: [Docker Compose startup ordering](#docker) - Explains dependency ordering, healthy-service conditions and successful one-shot completion.
- **PRIMARY SOURCE**: [FastAPI application containers](#fastapi) - Explains building and running a FastAPI application in a container image.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 04: A memory needs an evidence trail

- **PRIMARY SOURCE**: [W3C PROV: evidence and derivation](#prov) - Provides concepts for tracing entities, activities, attribution and derived information.
- **BRIEF**: [Assignment evaluation: pp. 4-6](#brief_evaluation) - Corpus, complete-pipeline evaluation, provenance, supported answers and abstention (pp. 4-6).
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 05: Keep time and certainty separate

- **PRIMARY SOURCE**: [Bitemporal history](#fowler) - Distinguishes when information applies from when a system records or learns about it.
- **PRIMARY SOURCE**: [W3C PROV: evidence and derivation](#prov) - Provides concepts for tracing entities, activities, attribution and derived information.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 06: Learning is a guarded pipeline

- **PRIMARY SOURCE**: [LangChain memory concepts](#langchain) - Separates facts, experiences and instructions; explains thread state, stores and memory writing.
- **PRIMARY SOURCE**: [PostgreSQL explicit locking](#locking) - Documents transaction locks used to serialize shared policy validation and state changes.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 07: The same new sentence can mean different things

- **PRIMARY SOURCE**: [Bitemporal history](#fowler) - Distinguishes when information applies from when a system records or learns about it.
- **PRIMARY SOURCE**: [W3C PROV: evidence and derivation](#prov) - Provides concepts for tracing entities, activities, attribution and derived information.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 08: Decide whether personal retrieval is needed

- **PRIMARY SOURCE**: [LangChain memory concepts](#langchain) - Separates facts, experiences and instructions; explains thread state, stores and memory writing.
- **PROJECT DECISION**: [Kivi requirements and open choices](#decisions) - Defines eligible evidence, Normal/Private, Correct/Forget and proposed implementation choices.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 09: Retrieve candidates, then rank useful evidence

- **PRIMARY SOURCE**: [Reciprocal Rank Fusion paper](#rrf) - Combines candidate rankings using reciprocal rank contributions; motivates the k=60 example.
- **PRIMARY SOURCE**: [pgvector: exact and hybrid search](#pgvector) - Documents exact/approximate vectors and full-text hybrid search with fusion or reranking.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 10: Watch three memories support one useful draft

- **PRIMARY SOURCE**: [Anthropic contextual retrieval](#anthropic) - Explains preserving chunk context and combining lexical, dense and reranking mechanisms.
- **PRIMARY SOURCE**: [W3C PROV: evidence and derivation](#prov) - Provides concepts for tracing entities, activities, attribution and derived information.
- **SYNTHETIC EXAMPLE**: [Synthetic Atlas / Mira fixtures](#example) - Illustrates changed plans, scoped preferences, reported actions, uncertainty and exact sources.

### Page 11: Give each model a bounded role

- **PRIMARY SOURCE**: [NVIDIA DeepSeek dated endpoint](#deepseek) - Documents the candidate hosted DeepSeek endpoint for the selected main-model role.
- **PRIMARY SOURCE**: [Nemotron Lightning model card](#lightning) - Describes a candidate model for bounded typed proposals, including its sparse architecture.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 12: Private is a boundary before personal state

- **PROJECT DECISION**: [Kivi requirements and open choices](#decisions) - Defines eligible evidence, Normal/Private, Correct/Forget and proposed implementation choices.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.
- **PROJECT DECISION**: [Kivi evaluation gates and race tests](#evaluation) - Defines real-DB races, Private checks, repeated live cases, ablations and proposed quality gates.

### Page 13: Forgetting must follow every dependency

- **PRIMARY SOURCE**: [W3C PROV: evidence and derivation](#prov) - Provides concepts for tracing entities, activities, attribution and derived information.
- **PRIMARY SOURCE**: [PostgreSQL explicit locking](#locking) - Documents transaction locks used to serialize shared policy validation and state changes.
- **PROJECT DECISION**: [Kivi requirements and open choices](#decisions) - Defines eligible evidence, Normal/Private, Correct/Forget and proposed implementation choices.

### Page 14: A shared guard defeats stale work

- **PRIMARY SOURCE**: [PostgreSQL explicit locking](#locking) - Documents transaction locks used to serialize shared policy validation and state changes.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.
- **PROJECT DECISION**: [Kivi evaluation gates and race tests](#evaluation) - Defines real-DB races, Private checks, repeated live cases, ablations and proposed quality gates.

### Page 15: Diagnose feedback before changing memory

- **PRIMARY SOURCE**: [Self-Refine: feedback and revision](#selfrefine) - Studies iterative feedback and refinement of model outputs without additional model training.
- **PRIMARY SOURCE**: [Reflexion: verbal feedback memory](#reflexion) - Studies agents using linguistic feedback and stored reflections to improve later attempts.
- **PROJECT DECISION**: [Kivi architecture and model proposals](#architecture) - Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

### Page 16: Prove usefulness with controlled comparisons

- **PRIMARY SOURCE**: [LongMemEval benchmark repository](#longmemeval) - Offers long-term memory tasks covering extraction, updates, temporal reasoning and abstention.
- **PRIMARY SOURCE**: [IR textbook: precision and recall](#irbook) - Defines precision and recall for retrieved sets relative to judged relevance.
- **BRIEF**: [Assignment evaluation: pp. 4-6](#brief_evaluation) - Corpus, complete-pipeline evaluation, provenance, supported answers and abstention (pp. 4-6).

### Page 17: Every extra mechanism must earn its place

- **PRIMARY SOURCE**: [pgvector: exact and hybrid search](#pgvector) - Documents exact/approximate vectors and full-text hybrid search with fusion or reranking.
- **PRIMARY SOURCE**: [Docker Compose startup ordering](#docker) - Explains dependency ordering, healthy-service conditions and successful one-shot completion.
- **PROJECT DECISION**: [Kivi requirements and open choices](#decisions) - Defines eligible evidence, Normal/Private, Correct/Forget and proposed implementation choices.

### Page 18: Understand here, implement from the same plan

- **BRIEF**: [Assignment product requirements: p. 4](#brief_product) - Requires an ordinary-user interface connected to actual state, persistence, retrieval and models.
- **PROJECT DECISION**: [Kivi implementation plan](#plan) - Proposed milestones, scope cuts, approval boundaries and the minimum complete reviewer journey.
- **PROJECT DECISION**: [Kivi current status and next action](#tracker) - Tracks completed, ongoing and pending work plus test, commit, push and verification workflow.

## Source details

<a id="brief_scope"></a>
### Assignment scope: pp. 3-5

**BRIEF** - [Open reference](https://github.com/harshith0518/ProjectSemanticMemorySarvamAI/blob/dev/docs/visual-guide-references.md#assignment-brief)

**Supports:** Includes factual, episodic and preference-level understanding; choose a useful product scope.

**Limits:** The supplied Golden Goose brief, p. 3 under 'Begin with the use case', explicitly includes factual, episodic and preference-level understanding. Page 4 repeats that scope; p. 5 lists learned facts, preferences and episodes for review. The brief's broad product use of semantic memory is not the narrower cognitive taxonomy. Deferring automatic procedural learning is a project choice, not a brief prohibition. The PDF is in the parent planning workspace; this link points to its locator, not a public copy.

<a id="brief_product"></a>
### Assignment product requirements: p. 4

**BRIEF** - [Open reference](https://github.com/harshith0518/ProjectSemanticMemorySarvamAI/blob/dev/docs/visual-guide-references.md#assignment-brief)

**Supports:** Requires an ordinary-user interface connected to actual state, persistence, retrieval and models.

**Limits:** Page 4, 'Build the complete experience' and 'Build the system beneath it', requires a real end-to-end product. Transcript replay is allowed; ASR and production Kivi integration are unnecessary. A CLI, static guide or architectural proposal alone is insufficient. These are assignment requirements, not achieved milestones. The linked locator identifies the locally supplied brief.

<a id="brief_evaluation"></a>
### Assignment evaluation: pp. 4-6

**BRIEF** - [Open reference](https://github.com/harshith0518/ProjectSemanticMemorySarvamAI/blob/dev/docs/visual-guide-references.md#assignment-brief)

**Supports:** Corpus, complete-pipeline evaluation, provenance, supported answers and abstention (pp. 4-6).

**Limits:** Page 4 starts the approximately 500-record development requirement; p. 5 specifies raw/formatted variants, reproducible evaluation, inspectable sources and a separate reviewer corpus; p. 6 requires distributed recovery, supported answers and refusal to invent missing answers. The brief does not prescribe the project's 90% target, three repeats, schema or model shortlist. No product evaluation result follows from these requirements.

<a id="plan"></a>
### Kivi implementation plan

**PROJECT DECISION** - [Open reference](https://github.com/harshith0518/ProjectSemanticMemorySarvamAI/blob/dev/PLAN.md)

**Supports:** Proposed milestones, scope cuts, approval boundaries and the minimum complete reviewer journey.

**Limits:** This project plan explains intended build order and acceptance gates. Work budgets are estimates, not delivery guarantees. The plan does not establish implementation, completed Part One submissions or approval of every later change. The linked GitHub dev-branch document can evolve after this diagram snapshot.

<a id="decisions"></a>
### Kivi requirements and open choices

**PROJECT DECISION** - [Open reference](https://github.com/harshith0518/ProjectSemanticMemorySarvamAI/blob/dev/DECISIONS.md)

**Supports:** Defines eligible evidence, Normal/Private, Correct/Forget and proposed implementation choices.

**Limits:** This is the authoritative project distinction between agreed requirements and proposed architecture. Private and Forget are application promises to implement and test; external libraries do not establish them. Normal source retention and selective memory formation are different decisions. Source support does not guarantee real-world truth.

<a id="architecture"></a>
### Kivi architecture and model proposals

**PROJECT DECISION** - [Open reference](https://github.com/harshith0518/ProjectSemanticMemorySarvamAI/blob/dev/ARCHITECTURE.md)

**Supports:** Defines proposed records, pipelines, model boundaries, full shortlist and concurrency guards.

**Limits:** The architecture is proposed, not implemented or benchmarked. It supplies Kivi-specific choices absent from external sources, including temporal reconciliation, typed model proposals, response publication and Private accounting. The main-model role is selected; endpoint access, smaller-model quality, cost and retention still need verification. Code owns authorization and database writes.

<a id="evaluation"></a>
### Kivi evaluation gates and race tests

**PROJECT DECISION** - [Open reference](https://github.com/harshith0518/ProjectSemanticMemorySarvamAI/blob/dev/EVALUATION.md)

**Supports:** Defines real-DB races, Private checks, repeated live cases, ablations and proposed quality gates.

**Limits:** The 90% blind-success target, three live repeats and question counts are project acceptance choices, not benchmark standards or achieved results. Deterministic doubles exercise application contracts; they do not measure extraction quality. Live runs, failure reporting and semantic support review remain necessary. Private tests use synthetic content and must inspect actual data paths.

<a id="tracker"></a>
### Kivi current status and next action

**PROJECT DECISION** - [Open reference](https://github.com/harshith0518/ProjectSemanticMemorySarvamAI/blob/dev/todo.md)

**Supports:** Tracks completed, ongoing and pending work plus test, commit, push and verification workflow.

**Limits:** The tracker is the evolving project status, not independent validation. Environment probes and documentation checks do not establish a running product. AI-assisted Part One reference drafts do not establish independent submissions. At this guide's planning snapshot S03 bootstrap remains subject to scope approval; recurring pushes of approved milestones are authorized.

<a id="langchain"></a>
### LangChain memory concepts

**PRIMARY SOURCE** - [Open reference](https://docs.langchain.com/oss/python/concepts/memory)

**Supports:** Separates facts, experiences and instructions; explains thread state, stores and memory writing.

**Limits:** The 'Long-term memory' table gives the narrower semantic/episodic/procedural taxonomy. It does not override the assignment's broader semantic-memory scope, require three databases or mandate LangGraph for Kivi. Persistent thread checkpoints are distinct from cross-thread memory. Its examples do not prove Kivi's privacy, reconciliation or retrieval quality.

<a id="prov"></a>
### W3C PROV: evidence and derivation

**PRIMARY SOURCE** - [Open reference](https://www.w3.org/TR/prov-overview/)

**Supports:** Provides concepts for tracing entities, activities, attribution and derived information.

**Limits:** PROV supplies a provenance vocabulary, not evidence that a statement is true. An existing source ID or derivation edge does not prove semantic entailment, trustworthy authorship or correct extraction. Kivi's span schema and invalidation protocol are application choices; using PROV concepts does not implement them automatically.

<a id="fowler"></a>
### Bitemporal history

**PRIMARY SOURCE** - [Open reference](https://martinfowler.com/articles/bitemporal-history.html)

**Supports:** Distinguishes when information applies from when a system records or learns about it.

**Limits:** This article explains temporal modeling, not an automatic truth-resolution algorithm. Capture, ingestion, event and validity times may differ; an unknown effective date cannot be inferred merely from ingestion order. A launch date is a claim value, not automatically its validity start. Kivi's successor and correction rules remain proposed application logic.

<a id="locking"></a>
### PostgreSQL explicit locking

**PRIMARY SOURCE** - [Open reference](https://www.postgresql.org/docs/current/explicit-locking.html)

**Supports:** Documents transaction locks used to serialize shared policy validation and state changes.

**Limits:** PostgreSQL documents locking primitives, not the complete Kivi Forget protocol. All relevant writers must use the same guard, recheck revisions inside the protected transaction and coordinate invalidation. Retrieval and response publication need their own defined revocation boundary. Verify with separate real database connections; already released response bytes cannot be recalled.

<a id="docker"></a>
### Docker Compose startup ordering

**PRIMARY SOURCE** - [Open reference](https://docs.docker.com/compose/how-tos/startup-order/)

**Supports:** Explains dependency ordering, healthy-service conditions and successful one-shot completion.

**Limits:** Starting a container is not proof the service is ready. Health and completion conditions can support a database-to-migration-to-application sequence, but migrations, volume isolation and failure behavior require implementation and checks. This guide does not establish that Kivi's Compose stack or project database exists.

<a id="fastapi"></a>
### FastAPI application containers

**PRIMARY SOURCE** - [Open reference](https://fastapi.tiangolo.com/deployment/docker/)

**Supports:** Explains building and running a FastAPI application in a container image.

**Limits:** Container deployment guidance supports the proposed packaging method. It does not prescribe Kivi's shared API/CLI/worker services, guarantee isolation or supply memory semantics. Dependency and image versions must be pinned and tested during approved bootstrap; the guide is not proof of a working backend.

<a id="rrf"></a>
### Reciprocal Rank Fusion paper

**PRIMARY SOURCE** - [Open reference](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)

**Supports:** Combines candidate rankings using reciprocal rank contributions; motivates the k=60 example.

**Limits:** RRF fuses ranked lists; its score is not a probability of truth or relevance. The diagram's k=60 and one-based ranks define the illustrated calculation, not a locally tuned optimum. A missing candidate contributes nothing from that list. Permission, exclusion and time checks remain mandatory; retrieval effectiveness must be measured on Kivi's questions.

<a id="pgvector"></a>
### pgvector: exact and hybrid search

**PRIMARY SOURCE** - [Open reference](https://github.com/pgvector/pgvector)

**Supports:** Documents exact/approximate vectors and full-text hybrid search with fusion or reranking.

**Limits:** pgvector is a retrieval component, not a memory-management system. PostgreSQL full-text ranking is not automatically BM25. Approximate indexes may miss candidates; exact search is a proposed starting point, not a measured latency guarantee. Five hundred observations may create more than five hundred claims or chunks. Indexes do not replace canonical evidence or exclusion checks.

<a id="anthropic"></a>
### Anthropic contextual retrieval

**PRIMARY SOURCE** - [Open reference](https://www.anthropic.com/engineering/contextual-retrieval)

**Supports:** Explains preserving chunk context and combining lexical, dense and reranking mechanisms.

**Limits:** Anthropic's engineering experiments motivate retrieval mechanisms, not a verified Kivi architecture or expected improvement. Contextualization may add model cost and can introduce unsupported interpretation. The Atlas example is synthetic and separate. Preserve original passages and evaluate any contextualized representation rather than transferring reported benchmark gains.

<a id="example"></a>
### Synthetic Atlas / Mira fixtures

**SYNTHETIC EXAMPLE** - [Open reference](https://github.com/harshith0518/ProjectSemanticMemorySarvamAI/blob/dev/README.md#using-the-visual-guide)

**Supports:** Illustrates changed plans, scoped preferences, reported actions, uncertainty and exact sources.

**Limits:** The eight source records live at ../reference-examples/sample-dictations.jsonl in the parent planning workspace, with separate evaluator-only labels. They are not bundled application data at this checkpoint and are not external validation. The README gives their location. Preserve raw/formatted variants as one observation; never ingest the evaluator labels. Illustrated outcomes are expectations, not measured model results.

<a id="deepseek"></a>
### NVIDIA DeepSeek dated endpoint

**PRIMARY SOURCE** - [Open reference](https://build.nvidia.com/deepseek-ai/deepseek-v4-pro-0813)

**Supports:** Documents the candidate hosted DeepSeek endpoint for the selected main-model role.

**Limits:** A listed endpoint does not establish account access, quotas, acceptable retention, schema enforcement or Kivi task quality. Verify configured and returned model IDs, cost and no-training settings before live calls. The user's main-model role choice is recorded in project architecture; endpoint availability can change after this check.

<a id="lightning"></a>
### Nemotron Lightning model card

**PRIMARY SOURCE** - [Open reference](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16)

**Supports:** Describes a candidate model for bounded typed proposals, including its sparse architecture.

**Limits:** The model card does not prove hosted endpoint behavior, multilingual extraction faithfulness or Kivi cost savings. Total parameters and active parameters are different; active count is not the required local memory footprint. Tools and structured-output training do not guarantee valid, supported proposals. The full untested shortlist and provider boundaries are project architecture choices.

<a id="selfrefine"></a>
### Self-Refine: feedback and revision

**PRIMARY SOURCE** - [Open reference](https://arxiv.org/abs/2303.17651)

**Supports:** Studies iterative feedback and refinement of model outputs without additional model training.

**Limits:** Self-generated critique is not guaranteed correct and may preserve or amplify an error. This paper does not prove autonomous root-cause diagnosis, factual memory correction or safe procedural learning for Kivi. Kivi proposes inspecting observable evidence and repairing the demonstrated failing layer with a bounded retry and regression case.

<a id="reflexion"></a>
### Reflexion: verbal feedback memory

**PRIMARY SOURCE** - [Open reference](https://arxiv.org/abs/2303.11366)

**Supports:** Studies agents using linguistic feedback and stored reflections to improve later attempts.

**Limits:** Reflexion is not a guarantee that an agent learns the right lesson or updates model weights. Reported experiments do not validate Kivi's user-feedback loop. A disliked reply is not automatically a corrected fact or universal preference. Automatic prompt or skill rewriting is deferred; supported, scoped changes remain controlled application operations.

<a id="longmemeval"></a>
### LongMemEval benchmark repository

**PRIMARY SOURCE** - [Open reference](https://github.com/xiaowu0162/LongMemEval)

**Supports:** Offers long-term memory tasks covering extraction, updates, temporal reasoning and abstention.

**Limits:** Benchmark task families inform challenge design; the repository does not provide a Kivi result. Public benchmark questions are not the assignment's approximately 500 source observations. The project's three repeats, blind question count and 90% success gate are separate choices. Do not equate a vendor's benchmark score with local product performance.

<a id="irbook"></a>
### IR textbook: precision and recall

**PRIMARY SOURCE** - [Open reference](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-unranked-retrieval-sets-1.html)

**Supports:** Defines precision and recall for retrieved sets relative to judged relevance.

**Limits:** Retrieval relevance metrics require an explicit ground-truth set and do not alone measure factual support, task completion, correct temporal interpretation or privacy. Kivi should report evidence coverage and supported task success separately. Small samples and incomplete labels limit the conclusions; all reported values must come from actual evaluation runs.
