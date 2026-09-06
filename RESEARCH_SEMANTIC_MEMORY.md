# Golden Goose: semantic-memory landscape

Researched on 5 September 2026.

Follow-up: the [15-part research dossier](research/README.md) and [architecture proposal](research/ARCHITECTURE_PROPOSAL.md) contain more detailed source/code verification and supersede this initial survey where product versions or implementation recommendations differ.

> This is external research, not Part One of the assignment. The brief requires the applicant to form and write the product position independently, without generative AI, and to preserve it before designing the interface or choosing the architecture. Do not copy this document into Part One.

## Decision check

Choosing Golden Goose is coherent if the goal is to show product judgment, backend engineering, evaluation design, and a small usable interface in one submission. It can be more rewarding than the backend-only task, but it also carries more failure modes. The two-day version must have a narrow product promise and unusually strong evaluation discipline.

The brief does not ask for a generic chatbot with vector search. It asks for a working product that:

- imports about 500 transcript-like records containing raw ASR, formatted text, and metadata;
- decides what to learn, ignore, revise, or reject;
- answers questions that require facts, preferences, episodes, time, and evidence across dictations;
- abstains when the history cannot support an answer;
- exposes provenance and the reason for memory decisions;
- reports retrieval and end-to-end latency, database growth, model use, and cost; and
- survives a second, unseen corpus of about 500 dictations from one user.

That makes semantic memory the center of the challenge. Phonetic memory is already part of Kivi's product surface, but on its own it cannot satisfy cross-dictation questions or evidence-backed recall.

## Kivi's current public baseline

Kivi is Sarvam AI's voice interface for a computer. It turns speech into polished text or actions across applications, supports more than 22 Indian languages and code-switching, remembers corrected names and jargon, applies app-specific writing personas, and can operate on selected text. Sarvam supplies the wider speech and language stack; Kivi is one product built on that stack. Sources: [Kivi product page](https://heykivi.ai/), [Sarvam Epoch summary](https://www.sarvam.ai/epoch/summary), and [Sarvam model documentation](https://docs.sarvam.ai/api/getting-started/models).

The assignment asks what Kivi could become once its history is useful beyond better transcription. That places it at the intersection of three markets:

1. universal voice dictation;
2. personal assistants with long-term memory; and
3. searchable personal or workplace history.

No single competitor covers all three especially well.

## Commercial competitors

The weaknesses below are comparisons with the Golden Goose problem, based on public product documentation. They are not claims about undisclosed internal systems.

| Product | Relevant features | Main strength and uniqueness | Weakness or open gap for this task |
|---|---|---|---|
| **Wispr Flow** | Dictation in any app; filler removal; backtracking; automatic punctuation and lists; personal and team dictionaries; snippets; app-aware styles; developer syntax/file awareness; 100+ languages | Probably the closest direct comparison for polished universal dictation. Its automatic dictionary updates turn user corrections into immediate future accuracy. | Its public product story is primarily about producing better text now. A personal dictionary and style profile do not by themselves answer evidence-backed questions over months of activity. [Official features](https://wisprflow.ai/features) |
| **Superwhisper** | Local or cloud speech models; per-workflow modes; custom prompts; app, selection, and clipboard context; vocabulary and deterministic replacements; history; system-audio and speaker capture | High user control. Local transcription and replace rules provide privacy and predictable corrections; custom modes make it a flexible power-user tool. | Personalization is configuration-heavy. Its documented memory primitives are history, vocabulary, and context rather than a governed store of evolving facts and episodes. [Modes](https://superwhisper.com/docs/modes/modes), [vocabulary](https://superwhisper.com/docs/get-started/interface-vocabulary), [context](https://superwhisper.com/docs/common-issues/context) |
| **ChatGPT Memory** | Saved memories; reference to past chats; automatic updates to useful context; project-only memory; temporary chats; review, correction, and deletion; source indications | Strong mainstream model for implicit personalization plus explicit user control. Project and temporary scopes are understandable privacy boundaries. | Memory is summarized and selective, so it can lose event detail. Its source indicator may not expose every influence, and complete deletion can require removing source chats/files as well as saved memory. [Official Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq) |
| **Claude Memory** | Topic-based memories; automatic and explicit remembering; editable memory; past-chat citations; search across chats; project boundaries; incognito chats; exclusions for some sensitive details | Topic-based memory is legible, and citations make recalled context easier to verify. Separate project memories reduce accidental context mixing. | It remembers conversations with Claude, not a continuous cross-application voice history. Topic summaries can still compress away fine-grained evidence. [Official help](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context) |
| **Gemini Personal Intelligence** | Past-chat personalization; connected Gmail, Calendar, Drive, Docs, Photos, Contacts, Search, Maps, Shopping, and YouTube data where eligible; per-chat personalization controls; temporary chats | The widest consumer data surface here. It can combine communication, plans, places, media, and files to answer personal questions or take actions. | Availability depends on account, region, feature, and connected services. Controls span both conversation deletion and connection settings, which increases mental overhead. [Connected apps](https://support.google.com/gemini/answer/16598406), [past-chat personalization](https://support.google.com/gemini/answer/16598469) |
| **Microsoft 365 Copilot** | Work profile and inferred memories; asks before saving inferred information; explicit remember/edit/delete; Work IQ/Graph grounding; external connectors; permission-respecting enterprise search and citations | Strongest enterprise model for memory inside existing access controls. Work artifacts and organization permissions already form a governed context layer. | It depends on the Microsoft 365 tenant and its data. It is a work-memory system rather than a simple personal record of everything a user dictated. [Memory management](https://support.microsoft.com/en-us/microsoft-365-copilot/manage-copilot-memory-in-microsoft-365-copilot), [Copilot connectors](https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors) |
| **Glean** | Permission-aware enterprise search; personalization from role, activity, and work context; ongoing-project awareness; connected workplace sources; sensitive-attribute exclusions | Excellent at finding organization knowledge without crossing source permissions. Personalization is grounded in a company's existing information system. | Its value rises with connector coverage and enterprise administration. It does not target private, raw dictation as the primary source of longitudinal memory. [Memory and personalization](https://docs.glean.com/user-guide/assistant/memory-personalization), [end-user guide](https://docs.glean.com/user-guide/about/end-user-quick-start-guide) |
| **Granola** | Meeting capture; AI-enhanced notes; chat over one, selected, folder, or all meetings; cross-meeting patterns; action items; reusable recipes; uploaded-file context | Very clear evidence boundary: answers come from meetings and uploaded files. This makes recall useful and easier to explain. | Granola explicitly does not know about emails, offline tasks, or personal to-do items unless supplied. Basic-plan history is limited. It is strong episodic meeting memory, not a universal activity stream. [Chat with meetings](https://docs.granola.ai/help-center/getting-more-from-your-notes/chatting-with-your-meetings) |
| **Notion AI** | Workspace and connected-app search; meeting notes; web search; pages and database creation/editing; agent actions inside the workspace | Memory and action share the same workspace, so recalled information can immediately become a document, task, or database update. | It only sees content inside Notion or configured connections. Its basic unit is a work artifact, rather than a user's evolving personal state extracted from dictation. [Official FAQ](https://www.notion.com/help/notion-ai-faqs) |

## Ten competitor patterns worth understanding

These are the strongest recurring features across the market:

1. **Correction-to-dictionary learning** — one correction improves future spellings and jargon.
2. **Application-aware style** — messages, email, documents, and code receive different formatting.
3. **Immediate screen context** — selected text, clipboard, and the active app disambiguate the current dictation.
4. **Stable and dynamic profile separation** — durable preferences are kept apart from temporary projects or recent activity.
5. **Temporal revision** — a new address or preference supersedes the old one without erasing history.
6. **Scoped memory** — workspaces, projects, temporary chats, and incognito modes prevent context leakage.
7. **Inspectable memory** — users can see, edit, delete, or explicitly teach remembered information.
8. **Evidence links** — answers point back to chats, meetings, files, or events that support them.
9. **Permission-aware retrieval** — the answer cannot reveal data the current user is not allowed to read.
10. **Cross-record synthesis** — the system combines several events to explain a trend, decision, relationship, or unfinished commitment.

Kivi already publicly demonstrates patterns 1-3. Golden Goose is mostly about proving patterns 4-10 over dictation history, with abstention and operational measurements.

## Open-source building blocks

| Project | Public architecture | Strength and uniqueness | Weakness or risk | Two-day fit |
|---|---|---|---|---|
| **Mem0** | LLM-based memory extraction and updates; user/session/agent scopes; vector or hybrid retrieval; library, self-hosted server, and managed platform | Fastest general-purpose route to add per-user memory; simple API; Apache-2.0; useful evaluation code | Its abstraction can hide why a fact was added or changed unless extra audit records are built. Managed features and benchmark behavior are not necessarily identical to the base library. | **Good for a spike**, provided every decision and source is recorded outside the library. [Repository](https://github.com/mem0ai/mem0) |
| **Graphiti** | Raw episodes become entities and relationship edges; facts have validity windows; hybrid semantic, BM25, and graph retrieval; every fact retains episode provenance | Best fit for changing truths, event time, and multi-record relationships. Old facts are invalidated instead of destroyed. Apache-2.0. | Requires a graph backend and surrounding user/thread/API/UI code. Entity resolution and graph debugging add significant scope. | **High risk in two days** unless used only for one temporal-memory experiment. [Repository](https://github.com/getzep/graphiti) |
| **LangMem** | Memory tools in the request path or a background extractor/consolidator; storage-agnostic API; native LangGraph store integration | Small, controllable primitives. Supports explicit schemas and lets the application retain ownership of persistence and audit logic. MIT. | It is a toolkit, not an end-to-end memory product. The team must still design memory policy, durable storage, retrieval, provenance, evaluation, and UI. | **Good if the team wants control** and already knows LangGraph. [Repository](https://github.com/langchain-ai/langmem) |
| **Letta** | Stateful agents with editable core memory blocks plus archival/searchable memory; newer tooling can keep agent-owned memory in a Git-backed filesystem | Memory is inspectable and versioned; the agent can reorganize and improve its own context over time. Apache-2.0. | It is an agent platform. Self-editing memory is harder to evaluate deterministically, and much of the platform is outside this assignment's transcript-to-answer core. | **Poor fit for the first submission**, useful as design inspiration. [Repository](https://github.com/letta-ai/letta), [memory docs](https://github.com/letta-ai/letta-docs-md/blob/main/configuration/memory/index.md) |
| **Cognee** | Ingestion pipeline builds a self-hosted knowledge graph plus vector index and ontology; session cache can sync into permanent graph; `remember`, `recall`, `forget`, and `improve` operations | Broad ingestion, graph reasoning, traceability, tenant isolation, and local development backends. Apache-2.0. | Many moving parts and model calls; defaults favor quality over latency. The full feature set makes failure attribution harder during a short assignment. | **High risk in two days**, better for a later comparison. [Repository](https://github.com/topoteretes/cognee) |
| **Supermemory** | Fact extraction; static/dynamic user profile; contradiction and expiry handling; hybrid memory plus RAG; connectors and multimodal ingestion; hosted and local paths | Most batteries-included public feature set and a convenient profile-plus-search API. MIT. | Many performance and benchmark claims are vendor-reported. Hosted and local behavior must be verified separately, and it may obscure the decisions the evaluator wants to inspect. | **Good for a baseline**, weaker as the only implementation. [Repository](https://github.com/supermemoryai/supermemory) |
| **LongMemEval** | A benchmark rather than a memory layer; 500 questions testing information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention | Its categories align unusually well with the Golden Goose hidden-corpus evaluation and can inspire adversarial test cases. | It uses chat histories rather than noisy raw/formatted dictation pairs, so its data cannot substitute for the assignment corpus. | **Excellent evaluation reference.** [Repository](https://github.com/xiaowu0162/LongMemEval), [ICLR paper](https://openreview.net/pdf?id=pZiyCaVuti) |

## The architecture patterns underneath the products

The credible systems vary in implementation, but most contain these logical layers:

```text
raw interaction ledger
        |
        v
candidate extraction -----> rejection / ignore log
        |
        v
normalized memories: facts | preferences | episodes | entities
        |
        +----> time, confidence, status, source IDs, revision links
        |
        v
hybrid retrieval: lexical + semantic + metadata/time filters
        |
        v
evidence selection -> answer or abstain -> citations and decision trace
```

The raw ledger is the safety net. Extracted memories are a lossy index, not the source of truth. The answer path should be able to fall back to source records, and every derived item should carry source IDs. This is the main difference between a trustworthy semantic-memory product and a vector database containing summaries.

Four common implementation families are:

| Family | Shape | Advantage | Failure mode |
|---|---|---|---|
| Event RAG | Chunk every record, embed, retrieve top-k, answer | Simple and preserves source text | Weak updates, contradictions, preferences, and multi-step questions |
| Profile memory | Maintain one structured user profile and retrieve it | Fast and compact for stable facts/preferences | Rewrites can silently remove evidence; episodes fit poorly |
| Memory documents | Store many typed facts/preferences/episodes with source and lifecycle metadata | Auditable, easy to filter, and relatively simple | Requires deduplication, contradiction policy, and query planning |
| Temporal graph | Entities and relations with event/valid time plus source episodes | Strong time and relationship reasoning | Highest ingestion, operations, and debugging cost |

For this assignment, architecture quality will be judged less by sophistication of the database and more by whether failures are visible and reproducible. A smaller system with explicit decisions can outperform a larger framework that returns impressive answers without explaining them.

## The unresolved opportunity shown by the landscape

Competitors are good at one of these jobs:

- producing clean text from speech;
- remembering a short user profile;
- searching a bounded corpus such as meetings or work documents; or
- providing infrastructure for an agent developer.

The weakly served area is a user-controlled memory derived from everyday voice activity that distinguishes durable facts from temporary episodes, revises itself over time, and can prove every answer from original interactions. The difficult product questions remain:

- Which statements are safe and useful to remember without an explicit command?
- How should the system distinguish what the user said, what the system inferred, and what is currently true?
- When should a newer statement supersede an older one?
- How much evidence is enough for a preference or pattern?
- What should be forgotten automatically, and what requires user action?
- How should the product show uncertainty without making ordinary recall feel technical?

Those questions are more differentiating than the choice of vector database.

## Practical decision for the next step

The Golden Goose choice is worthwhile, with one gate: complete and commit the applicant's own Part One before choosing the product behavior or technical stack. After that snapshot exists, the research suggests comparing only three implementation directions against the chosen position:

1. a transparent custom memory-document store with hybrid retrieval;
2. the same product backed by Mem0 or LangMem to save extraction plumbing; or
3. a limited Graphiti experiment if temporal relationships are central enough to justify the risk.

Do not begin with a full Letta, Cognee, or temporal-graph platform unless Part One clearly demands it. The assignment rewards an end-to-end, inspectable product on unseen data; broad infrastructure would consume the time needed for evaluation, provenance, and a usable interface.

## Source-quality note

Product features came from vendor documentation and therefore describe intended behavior. Benchmark scores in vendor repositories are useful hypotheses, not neutral comparisons. Any adopted open-source framework should be run against the same local corpus, queries, model, and scoring rules before its claims influence the final architecture.
