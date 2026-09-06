# 06 — Clarification and abstention

Kivi should preserve the flow of capturing memories and clarify only when an unresolved distinction matters to the current request. A history of 500 dictations provides context, but its size does not establish that a particular answer is supported. The user's dislike of frequent mandatory questions makes interruption cost an explicit design constraint.

Zhang and Choi evaluate clarification as a tradeoff between task improvement and interaction cost, accounting for dominant interpretations and user preferences. Their experiments cover QA, translation, and inference; they do not validate a personal-memory policy. The transferable lesson is to estimate whether a question would improve the result, rather than treating every ambiguity as a reason to interrupt. [Clarify When Necessary, NAACL Findings 2025](https://aclanthology.org/2025.findings-naacl.306/).

Testoni and Fernández find that model uncertainty poorly predicts human clarification behavior in a collaborative drawing task; their uncertainty-guided questions improve task success. This supports evaluating questions by their effect on Kivi's task, while cautioning against copying human question frequency or transferring that paper's task-specific thresholds. [Asking the Right Question at the Right Time, EACL 2024](https://aclanthology.org/2024.eacl-long.16/).

Amershi et al.'s guidelines recommend timing interruptions to context, allowing dismissal and correction, and narrowing service when uncertain. These are interaction guidelines, not evidence that any particular clarification rate works for dictation. [Guidelines for Human-AI Interaction, CHI 2019](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf).

The following is a proposed Kivi policy, to validate on actual use:

1. **Materiality:** Would plausible interpretations change the substantive answer, person, date, remembered relationship, or requested action? If they lead to the same useful result, proceed. Do not ask merely to fill an empty field.
2. **Risk:** What happens if Kivi chooses incorrectly, and how readily can the result be corrected? An uncertain label can remain unresolved. A wrong recipient or destructive edit requires resolution before that dependent action; independent useful work can continue.
3. **Evidence sufficiency:** Retrieve relevant original dictations and check attribution, time, and contradictions. Distinguish unclear user intent from a clear question with missing evidence. Asking the user to restate the question cannot supply an absent memory.
4. **Question value:** Ask only if the user can resolve the decisive gap and doing so materially improves the outcome. Prefer one short, specific question with candidate choices when available and an explicit skip path. Avoid model-generated confidence percentages or universal numerical cutoffs; tune decisions against observed errors and interruption burden.

At ingestion, save the original dictation without a compulsory clarification step. Preserve uncertain mentions and competing interpretations without silently promoting them into established facts. Offer correction when the user opens a memory or when the uncertainty becomes relevant; do not repeatedly surface ignored suggestions.

At retrieval, give the supported portion with source references. For optional disambiguation, show both candidates: “I found two dinners with Amit; here are both.” If evidence is missing, say “I don't have a recorded date,” and offer an optional way to add it. If clarification is skipped, return the scoped answer or abstain from the unsupported claim. Silence never confirms an interpretation.

Evaluate answer correctness, unsupported claims, avoidable interruptions, question usefulness, skipped-question outcomes, and correction effort together. A low question rate alone is not success.
