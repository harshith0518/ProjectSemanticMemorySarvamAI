# 05 — Evidence-grounded implicit personalization

Kivi should retrieve personal context even when the user does not explicitly request recall, then independently decide whether using it improves this answer. Retrieval relevance is broader than permission to mention a memory. The recommendations below are product-design inferences; these benchmarks do not establish what users find comfortable.

## What the evidence supports

- **LaMP** evaluates seven personalized classification/generation tasks and finds benefits from retrieving relevant profile items. Its approaches include lexical, semantic, and temporal retrieval. This supports selective profile augmentation, not inserting personal anecdotes into every factual answer. [Authors’ paper and repository](https://github.com/lamp-benchmark/lamp)
- **LongMemEval** explicitly tests using user information for personalized responses; evidence can be conveyed incidentally during another task. It also tests updated facts and abstention when information is absent. Thus “remember only when asked” misses a tested capability, while unsupported inference remains an error. [Paper, §3.2](https://arxiv.org/html/2410.10813v2)
- **PrefEval** separates preference inference, memory, and following across explicit/implicit preferences. Its evaluation distinguishes preference violation, hallucinated preferences, acknowledgment, and helpfulness. It therefore supports measuring faithful application separately from merely mentioning a remembered fact. [Paper and evaluation rubrics](https://arxiv.org/html/2502.09597v1)
- **PersonaMem** tests current preferences and transfer into new scenarios. Retrieval helps in its evaluated settings, but transferring preferences and generating new suggestions remain challenging. Its synthetic histories and response-selection evaluation are not direct evidence of user acceptance of spontaneous callbacks. [Paper, §§2–4](https://arxiv.org/html/2504.14225v1)

## Kivi policy options

1. **Restrained:** use memories when they materially change advice, constraints, explanations, or requested recall; omit decorative callbacks.
2. **Contextual companion — recommended for this brief:** additionally allow one short, grounded callback when a strong entity/event connection makes an open-ended conversation more relevant. A general France discussion can naturally connect to the user's Paris visit without an explicit memory request. Answer the current question first. “What is France’s capital?” normally needs no trip anecdote.
3. **Frequent callbacks:** surface associations whenever available. This risks repetition, distraction, and an intrusive feeling; validate with users before choosing it.

For all options, “I visited Paris” supports a visit, **not** liking Paris, French food, museums, or wanting to return. Preserve evidence, speaker, date, and fact-versus-inference status. Never convert assistant speculation into a user preference. Apply current corrections, avoid unrelated sensitive disclosures, and honor “do not personalize.”

Use optional, multiple topic/entity tags as retrieval hints and browsing facets. Do not make a single category hierarchy a mandatory gate: a Paris work trip crosses geography, travel, and employment; food preferences may matter to travel recommendations. Keep a global retrieval fallback and rank by question-specific usefulness. This is an architecture recommendation, not a benchmark-proven superiority claim.

## Acceptance tests

- France overview + Paris-visit evidence: appropriate grounded callback in companion mode; no invented sentiment.
- Capital question or unrelated arithmetic: correct concise answer; no gratuitous recall.
- French restaurant suggestions + explicit vegetarian preference: apply it without needing a reminder.
- Same suggestion + only Paris-visit evidence: no invented cuisine preference.
- Corrected preference, ambiguous Paris identity, third-party visit, deleted memory: no stale or misattributed personalization.
- Cross-topic evidence: retrieve despite missing/wrong category tags.

Score supported-memory recall, unsupported personal claims, unnecessary mentions, preference compliance, and task helpfulness separately; include human judgments of usefulness and intrusiveness.
