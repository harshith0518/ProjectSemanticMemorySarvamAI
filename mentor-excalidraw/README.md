# Golden Goose — editable mentor board

Start with [the compact overview](Golden-Goose-Compact-Overview.excalidraw). Use [the full six-frame board](Golden-Goose-Mentor-Board.excalidraw) when a question needs a deeper explanation. The [.json copy](Golden-Goose-Mentor-Board.json) contains exactly the same full scene.

These are native Excalidraw shapes, text, arrows, groups and frames, rather than a flattened picture. Open a `.excalidraw` file using Excalidraw's **Open** control. Keep your edited version as a new file. The [offline visual preview](index.html) lets you browse the same six areas without loading an editor or installing anything.

The file structure follows the [official Excalidraw JSON format](https://docs.excalidraw.com/docs/codebase/json-schema). The generated scenes were checked for valid JSON, frame containment, IDs, groups and arrow references; all six visual previews were rendered and reviewed. Native editor import was not exercised end to end in this environment, so this is structural and visual validation rather than an editor compatibility certification.

## A short mentor walkthrough

1. **00 — Two modes.** Regular Kivi preserves the user's intended dictation; its paired transcript can become historical input. Hey Kivi uses relevant evidence for a present request. Native speech recognition and phonetic learning are outside this submission.
2. **01 — One database.** General application records and semantic-memory records share SQLite. MemoryService adds interpretation, evidence, scope/time, controls and retrieval. Vectors are an optional search representation, not the definition of memory.
3. **02 — CRUD.** Create supported claims; read sources plus memories; update qualified interpretations; forget selected meaning or explicitly delete its source. Related changes commit together, and the application reports actual receipts.
4. **03 — Special safeguards.** Source fallback, qualified meaning, one exclusion boundary, held live input, short transactions, operation identities, stale-worker rejection, fresh answers and actual tool outcomes.
5. **04 — Technology rationale.** Each technology has a job, a reason for choosing it, its current decision status and a limitation. This distinguishes the user's model-family choice from baseline engineering choices and optional experiments.
6. **05 — Next work.** Choose one worthwhile journey; build persistent source search and a real cited-answer path with controls; add measured memory; finish the interface, evaluation and review setup.

For a five-minute opening, explain only 00. Use the same Jaipur-budget example for later questions. Ask the mentor to challenge usefulness, memory policy, ambiguity handling, trust-breaking failures and the evidence needed to justify optional complexity.

## Status and sources

This is a reviewed technical plan. The application, CLI, migrations, importer, live model integration, approximately 500-record corpus and product evaluation remain unbuilt. The only recorded executable evidence is the isolated SQLite contract experiment with 12/12 checks; it is not a semantic, concurrency or performance result.

The [canonical architecture snapshot](reference/ARCHITECTURE.md) governs abbreviated wording. Its internal research links refer to the original project repository. The [assignment brief](reference/Kivi_Golden_Goose_Task_Final.pdf) defines required outcomes. This AI-assisted board does not replace the applicant's independently formed and written Part One position and vision.

## Updating the source

`build_board.py` creates both scene extensions, the overview and six SVG previews. `technology-content.json` contains the complete compact rationale rows. The generator uses Python, Pillow and the declared Windows Arial path to measure text. `verify_board.py` checks the exported documentation and makes the portable ZIP. These are documentation utilities, not Kivi implementation.

Regenerating replaces the generated files. Preserve mentor edits in a separately named `.excalidraw` file before regenerating.
