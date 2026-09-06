# Five product questions: evidence and discussion notes

Research checked 5 September 2026. These are research notes and feedback on the user's ideas, not the applicant's Part One positioning statement or vision. The assignment asks for those documents to be formed and written independently. No application code is being built in this planning stage; the user will provide an NVIDIA API key during development.

## 1. Why would someone return to Kivi?

The user's stated aim is to recover useful information from prior interactions and bring it into a current Hey Kivi request, while keeping ordinary dictation faithful to what was said.

That is a useful direction, but “remember almost everything in the best way” does not identify a recurring task or a measurable outcome. Distinguish three things: capturing permitted source history, selectively deriving reusable memories, and selecting only relevant context for a response. More stored memories do not automatically improve answers.

**Current Kivi interface, verified scope:** the public product page shows dictation inside other applications, corrected vocabulary, app-specific personas, and Hey Kivi actions on selected text. Sarvam's announcement describes cross-application voice computing. Neither source establishes a ChatGPT-style project workspace, folders of chats, or a built-in project knowledge base. This is absence of public confirmation, not proof that no such interface exists in a beta build. We did not install or operate the native app. [Kivi](https://heykivi.ai/), [Sarvam announcement](https://www.sarvam.ai/epoch/summary)

Memory remains useful without chat projects: the same project or person can recur across email, Slack, notes, and other dictations. App name alone is not a project identifier. Missing project metadata must remain missing; inferred project associations should have evidence and be reversible. Project IDs can be optional scope metadata in our application, not a prerequisite for recall.

## 2. Which two or three abilities solve it?

“Good semantic memory,” “personalization,” and “good architecture” are quality goals and mechanisms. Candidate observable abilities in the user's own examples are: recovering prior information, combining scattered evidence or changes, and adapting a current answer or draft using relevant known context. Interface quality should help people accomplish and verify these tasks.

Reasoning quality is not exclusively model-dependent. Model capability matters, but retrieving the right records, selecting evidence, separating plans from events, preserving dates, and deciding when to abstain determine what the model can reliably reason over. This is a system-quality problem. Simple measurable workflows are a sensible starting point; autonomous loops add cost and additional failure opportunities. [Anthropic's agent engineering guidance](https://www.anthropic.com/engineering/building-effective-agents)

## 3. What must it remember?

A database is the storage component of a memory system. The system also needs admission, representation, retrieval, revision, forgetting, context selection, and evaluation.

Useful candidate representations include evidence-linked facts, explicit preferences, episodes, people/projects/places, and relationships. Each assertion needs attribution, time where supported, provenance, and epistemic status: stated, inferred, hypothetical, quoted, corrected, or uncertain. Raw ASR and formatted text belong to the same underlying interaction; they are not two independent witnesses. Neither variant is automatically perfect.

The user's proposed LLM-generated categories can be optional multi-label tags. Keep the core record schema stable so records remain searchable even if the LLM labels similar topics differently. A policy Markdown file can explain admission rules to the LLM, but programmatic validation, transactions, scope enforcement, and tests must enforce invariants. Database architecture is considered separately in the memory recommendation.

## 4. When should it ask for clarification?

Published work separates deciding whether clarification is necessary from choosing the question and then using the answer. Human-AI design research also calls for easy correction, dismissibility, relevant information, and reduced scope under uncertainty. These findings support selective clarification; they do not provide a universal confidence threshold for Kivi. [Clarify When Necessary](https://arxiv.org/abs/2311.09469), [EACL 2024 uncertainty-guided clarification](https://aclanthology.org/2024.eacl-long.16/), [CHI 2019 design guidelines](https://www.microsoft.com/en-us/research/articles/guidelines-for-human-ai-interaction-eighteen-best-practices-for-human-centered-ai-design/)

Proposed policy to test:

| Situation | Response |
|---|---|
| Sufficient relevant evidence | Answer and make sources inspectable; no clarification |
| Uncertain detail is unnecessary | Omit it and complete the supported portion |
| Two interpretations can be described briefly | Show both alternatives, or a labeled assumption for a reversible draft |
| Missing detail materially changes an answer | Ask one concise question, with a supported partial answer if possible |
| Missing recipient, time, or target for an external action | Prepare the action; do not execute until necessary information and authorization are available |
| History has no supporting evidence | Say what is missing; do not ask a question solely to avoid admitting lack of knowledge |

During background ingestion, retain ambiguous source evidence without repeatedly interrupting the person. Revisit an ambiguity when it matters to a request. If the person skips clarification, preserve the uncertainty and take the supported fallback; skipping is not confirmation. Do not treat an LLM's self-reported confidence number as a calibrated probability.

## 5. Personal recall and external actions

The user's France example concerns implicit personalization: retrieving a relevant past visit even when the current question does not explicitly request memory search. It does not, by itself, require external action.

Suppose a source explicitly says “I visited Paris in June.” A response may use that fact as a relevant reference point, with provenance. It may not infer that the user loved Paris, prefers France, visited this year, or wants to travel again. “I want to visit Paris” supports a plan or interest, not a completed visit. “My sister visited Paris” belongs to the sister. General geographical knowledge that Paris is in France should be distinguished from the personal evidence that establishes the visit.

Retrieval is not sufficient justification to mention a memory. Apply a relevance and appropriateness check: does using the memory help fulfill this request? Often the better personalization is adapting depth or skipping known basics, rather than announcing remembered details. General answers remain possible without inserting a personal memory into every response.

The eventual application can recall, draft, and act. Keep read operations and external writes separate: remembering a past request does not authorize a new send, booking, or file write. Tool records should distinguish proposed, authorized, attempted, succeeded, and failed operations. [Chip Huyen's author-published agent chapter](https://huyenchip.com/2025/01/07/agents.html)

## NVIDIA / DeepSeek preference

The user selected an NVIDIA-hosted DeepSeek model and will provide credentials later. NVIDIA's current catalog explicitly offers a free prototype endpoint, and the associated documentation describes it as a trial service. This confirms prototype access, not an unlimited quota or production availability guarantee. The actual account limit and latency remain untested. Keep base URL, model ID, timeouts, retry limits, and token usage configurable. A chat model does not automatically provide an embedding endpoint; choose and verify embeddings separately. [NVIDIA catalog](https://build.nvidia.com/deepseek-ai/deepseek-v4-pro-0813), [NVIDIA reference](https://docs.api.nvidia.com/nim/reference/deepseek-ai-deepseek-v4-pro-0813)
