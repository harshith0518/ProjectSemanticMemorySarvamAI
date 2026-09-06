# Golden Goose — mentor SVG pack

Start with **00**, then open only the mechanism being discussed. All 16 SVGs are standalone vector images with real selectable text, explicit status, sources and numbered process steps. No JavaScript, hosted fonts or HTML foreignObject elements are required by the SVGs.

These explain the current technical plan. The application, corpus, live model integration and product evaluation remain unbuilt. The only executed validation is an isolated SQLite contract experiment with 12/12 passing checks; it is not evidence of semantic or production reliability.

[Open the visual index](index.html) · [Problem-statement coverage](coverage.md) · [Canonical architecture snapshot](reference/ARCHITECTURE.md)

| # | Image |
|---|---|
| 00 | [Golden Goose — overall architecture](images/00-overall-architecture.svg) |
| 01 | [The assignment and the user experience](images/01-assignment-and-user-journey.svg) |
| 02 | [Import history without losing its meaning](images/02-import-and-source-evidence.svg) |
| 03 | [Learn useful memories from evidence](images/03-memory-extraction-and-admission.svg) |
| 04 | [What a memory contains and how it is stored](images/04-memory-schema-and-categories.svg) |
| 05 | [Keep people, time and changes distinct](images/05-entities-time-and-updates.svg) |
| 06 | [Find evidence sufficient for the question](images/06-retrieval-and-evidence.svg) |
| 07 | [From a live request to a trustworthy response](images/07-live-request-lifecycle.svg) |
| 08 | [Apply context and handle uncertainty](images/08-personalization-and-uncertainty.svg) |
| 09 | [Remember, correct, forget and inspect](images/09-controls-and-forgetting.svg) |
| 10 | [Language reasoning, validated tools and observed outcomes](images/10-models-and-tools.svg) |
| 11 | [Durable state, background work and safe recovery](images/11-persistence-and-recovery.svg) |
| 12 | [Make memory understandable in the application](images/12-interface-and-explainability.svg) |
| 13 | [Prove quality with a reproducible evaluation](images/13-corpus-evaluation-and-quality.svg) |
| 14 | [Make the complete product reproducible](images/14-reviewer-setup-and-submission.svg) |
| 15 | [From reviewed plan to a complete product](images/15-build-order-and-mentor-feedback.svg) |

## Suggested mentor discussion

1. Use 00 and 01 to explain the problem, intended utility and mode boundaries. The leading recurring task is still open.
2. Use 02–06 for what is remembered, evidence, representation, change and retrieval.
3. Use 07–12 for live behavior, control, tool authority, reliability and user experience.
4. Use 13–15 to challenge the proof, reproducibility, scope and next build milestones.

The applicant must form and write the brief's Part One position (≤100 words) and vision (≤600 words) independently and preserve them before Part Two. This AI-assisted technical pack does not replace those documents.

The coverage checklist links the problem statement to the images. The included canonical architecture snapshot governs any abbreviated diagram wording. All examples are illustrations, not a finalized product narrative or real user facts. These SVGs zoom without losing quality; open an individual image to read the details or place it directly in a slide or document.

## Editing and regeneration

The three `*-panels.json` files hold the content. `build_svgs.py` generates the images and index using Python plus Pillow for font measurement. It is documentation tooling, not product implementation. Run it from any directory using its absolute path; the original generator uses Arial from the declared Windows font paths.
