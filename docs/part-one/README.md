# Part One source notes

[user-notes.txt](user-notes.txt) preserves the substantive notes supplied by the applicant in this project conversation on 11 September 2026, beginning “Kivi - by sarvam” and ending “Part - 2 :-”. Wording and spelling are retained; paragraph whitespace and file line endings are normalized. The surrounding request to search earlier chats is not part of the notes.

These are **source notes, not two finalized Part One submissions**. They combine a glossary, scope, output expectations and five Part One questions/answers. Subsequently, the applicant explicitly requested two drafts in chat. Those assistant-written drafts are preserved below as AI-assisted reference material; they do not establish independent authorship or complete the submission requirement.

## Earlier conversation checked

At the applicant's request, the recent turns of **Explain Sarvam AI products** and **Document product features and plan** were inspected. The former contains an assistant-authored five-question recap in turn `01a0878f-6b19-7a12-a35f-fda7b91cacb3` (task `01a084d5-e7bd-7371-90e0-5ddb9a7ae111`). That response explicitly labels itself an AI-assisted recap and says Part One is not complete. The latter contains AI-assisted scope discussion. This bounded inspection did not identify two finalized applicant-authored submissions; it was not an exhaustive search of every earlier turn.

The latest notes are attributed as **user-supplied**. Similarity to the earlier discussion neither proves independent authorship nor establishes that all supplied wording was written by the assistant. Preserve this distinction rather than certifying an origin we cannot establish.

## Mechanical check

Count convention: Python `str.split()` over UTF-8 text. Hyphenated terms stay one token; standalone punctuation counts as a token. Counts are reproducible editorial checks, not an official scoring convention.

| Material | Count |
| --- | ---: |
| Entire notes file | 813 |
| Content after `Part - 1 :-` and before `Part - 2 :-`, including its five questions | 317 |

The Part One subsection is below 600 by this convention. That alone does not make it a finalized vision document or supply the separate positioning statement of at most 100 words.

The assignment brief, page 3, asks for a positioning statement of at most 100 words and a vision document of at most 600 words, independently formed and written by the applicant, with both preserved before Part Two. The source brief is held in the parent planning workspace as `reference/Kivi_Golden_Goose_Task_Final.pdf`; it is not bundled in this repository.

## Remaining applicant work

Provide the two final independently written documents. Preserve their actual submission dates and provenance; do not backdate them or describe prior AI-assisted discussion as independent writing. Their absence need not stop machine-readiness checks, but the Part One submission gate remains open.

The notes' competitor comparisons and language-quality claims are reproduced as supplied, not verified findings. The implementation continues to follow the explicit decisions in [DECISIONS.md](../../DECISIONS.md); these draft notes do not silently change scope. For evaluation traces, record observable operations, evidence, usage and concise decision summaries, not claimed access to a model's hidden reasoning.

## AI-assisted drafts supplied in chat

Preserved on 11 September 2026 at the applicant's request for continuity. These are the exact draft bodies previously supplied by the assistant, with paragraph spacing normalized. They are **AI-assisted reference drafts, not independently written applicant submissions**. The counts below use the same whitespace-token convention described above. Keep S01 open; do not infer approval of implementation scope from this drafting request.

### Positioning draft — 83 words

Kivi is a personal assistant that remembers useful context from a user’s previous conversations and dictations, so they do not have to explain the same things again. Its core experience, Hey Kivi, uses supported facts, preferences and changes to answer questions and prepare relevant drafts. Regular Dictation focuses on the text the user intends to write. Users can inspect sources, correct mistaken understanding, forget information or use Private mode. The value is practical personalization that saves effort while keeping the user in control.

### Vision draft — 378 words

Kivi should become an assistant that develops useful understanding of a person’s work and applies it when they need help. The value is in reducing repeated explanations, searching through old conversations and manually assembling information for everyday writing.

The product has two experiences. Regular Dictation focuses on capturing the text the user intends to write, with appropriate grammar, spelling and formatting. Hey Kivi handles questions and requests that benefit from remembered context. Dictations can contribute useful information to memory without remembered facts being silently inserted into ordinary dictated text.

For example, a user may mention that Atlas is now planned for 21 September, explain why the date changed, and separately record that Mira prefers three-bullet Atlas updates. Later, “Hey Kivi, draft an update for Mira” should bring these details together, preserve the date’s status as a plan and show the supporting sources. Producing the draft must not imply that it was sent.

Semantic memory should preserve selected facts, preferences and changes that could help with future tasks. Each memory needs enough context to explain whom it concerns, where it applies, when it is relevant and what supports it. Questions, quotations, tentative plans and temporary instructions need different treatment. Conflicting information should remain visibly uncertain until there is evidence to resolve it. A correction to Kivi’s interpretation must be distinguished from a real change in the user’s situation.

Users should be able to inspect what Kivi remembers and its sources, correct mistakes and ask it to forget information. Forgetting should prevent that information from being reused or relearned from the same supporting material. Private interactions should use only the current input and explicitly supplied temporary context, without reading saved personal information or retaining the interaction in the application.

For this assignment, the priority is a working semantic memory experience built around imported transcripts, persistent storage, useful assistance and essential memory controls. A small interface should make the complete journey understandable. Richer dictation interfaces and conversation organization can follow. Support for Indian languages and English is a direction to evaluate, with limitations reported honestly.

Success means Kivi makes later tasks easier while remaining accurate, understandable and correctable. We should demonstrate this through unfamiliar inputs, changing information, ambiguity and user feedback, and measure useful task completion, unsupported claims, latency and cost.
