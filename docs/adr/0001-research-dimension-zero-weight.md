# ADR-0001: Research dimension carries weight 0.0 while incubating

- **Status:** Accepted
- **Date:** 2026-07-17
- **Supersedes:** none
- **Related:** issue #5 (Deepen research benchmark)

## Context

The `research` benchmark is `benchmark_status: incubating` and `benchmark_core:
false`. Its 170 scenarios were previously tagged `dimension: synthesis` (and a
few `dimension: tool_use`), so a `--benchmark-status all` sweep folded
idea-generation / paper-review work into the weighted `synthesis` (0.15) and
`tool_use` (0.20) axes, perturbing every aggregate score with unfinished,
incubating material.

Issue #5 gives research its own `Dimension.RESEARCH` axis. The load-bearing
question is what weight to assign it. `DIMENSION_WEIGHTS` is multiplied into the
overall score, so any non-zero value would let incubating content move the
active ranking the moment someone runs a `--benchmark-status all` sweep; a zero
value means research is reported per-dimension (for visibility) but contributes
nothing to any aggregate.

## Decision

`Dimension.RESEARCH` is registered at weight **0.0**. The weights table still
sums to 1.00. Per-dimension detail for `research` is still reported so the
incubating capability remains observable in isolation (`--dimension research`).

Because research is `incubating` / `benchmark_core: false`, it is already
excluded from the `core` / `intelligence` / `full` (active-only) profiles. The
0.0 weight is the second guard: it ensures incubating content also cannot perturb
a `--benchmark-status all` overall.

## Consequences

- Research scenarios are fully isolated: they neither enter active profiles nor
  move any aggregate score, yet remain visible via `--dimension research` and
  per-dimension reporting.
- **Transitioning research to `active` requires a deliberate, non-zero weight
  assignment** (and a `benchmark_core` decision). It cannot silently enter the
  ranking — a future maintainer flipping `benchmark_status` to `active` must also
  edit `DIMENSION_WEIGHTS` and record the reasoning (reopen or extend this ADR).
- A 0.0-weighted axis is unusual; this ADR exists so a future architecture
  review does not re-litigate "why is research weight zero?" without the
  incubating-context reasoning.
