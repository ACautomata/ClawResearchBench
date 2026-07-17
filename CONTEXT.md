# CONTEXT

Ubiquitous terms for this repository. Use these as defined; don't drift to
synonyms. Architecture decisions live in `docs/adr/`.

## research grader

A **data-driven, per-family grading module** under `custom_checks/research/`
(`idea_generate_grader.py`, `paper_review_grader.py`). One grader serves every
scenario in a family: the per-scenario rubric (keywords, required headings,
forbidden phrases, output paths) is carried as data on the scenario, not baked
into a copied file. This is distinct from a *per-scenario wrapper* — the
~165 shallow `grade_keyword_output(...) / grade_paper_review(...)` pass-through
`.py` files that previously duplicated one wrapper per scenario and were
collapsed in issue #5. The 5 genuinely deep standalone checks
(`idea_generation_ig_001/002`, `paper_ingest_pi_001/002/003`) are not graders
and are preserved as-is.

## custom_check_config

The **scenario-level grading-config passthrough**: a free-form dict field on
`Scenario` (`scenario.custom_check_config`), populated from YAML and read
opaqely by the loader. The loader does not validate its shape — the grader that
owns a family defines its own keys (`keywords` / `forbidden_phrases` for
idea-generate; `output` / `must_contain` / `must_not_contain` / `fields` for
single-output paper-review; `outputs` / `keywords` for multi-output pipeline)
and fails fast on a missing key. This keeps "add a scenario = add a YAML line"
true and avoids a harness schema change for every new scoring shape.

## dimension: research

The **research axis** of the weighted `Dimension` enum, at weight **0.0** while
the research benchmark is `incubating` (see ADR-0001). It isolates the 170
incubating research scenarios from `synthesis`/`tool_use` so they neither pollute
those dimensions nor contribute to any aggregate score, while remaining visible
via `--dimension research`. Promoting research to `active` requires assigning a
deliberate non-zero weight.
