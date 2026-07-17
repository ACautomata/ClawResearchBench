# Fork: target-agent gating (`fork/target-main`)

This branch diverges from upstream ClawProBench **specifically to target an
existing agent** (default `main` / 颍姗) and reuse its workspace, instead of
creating a throwaway `ocb6-<model>-<uuid>` agent per trial and wiping the
workspace.

It is consumed by `research-agent`'s benchmark CI, which clones this branch at
a pinned commit (it is **not** vendored into `research-agent`'s tree).

## The target-agent diff (re-apply on rebase)

The fork's entire purpose lives in these spots. If a rebase onto upstream
ClawProBench drops or changes them, re-apply:

- `harness/live_harness.py`
  - `OpenClawLiveHarness(target_agent=...)` + `_is_target_agent_mode()`.
  - `execute_turn`: in target mode the agent id is the given id, the agent pool
    is bypassed, `_create_agent` is skipped (its first step is
    `agents delete <id> --force` — it would destroy the target), and the
    unknown-agent recreate path is skipped.
  - `execute_turn` (target mode) stages scenario fixtures into the target's
    REAL workspace before running: `target_workspace_path()` resolves
    `agents.list[<target>].workspace` (expanded) with a state-dir fallback,
    `_stage_workspace_fixtures` merges (no wipe) the temp `workspace_path` into
    it, `execution_workspace` is pointed at it, and `LiveRunResult.workspace_path`
    reports it. Done before the `try` block so a missing target workspace fails
    fast. (`_agent_command` passes no `--workspace`, so the agent runs against
    its configured workspace - where fixtures must land.)
  - `_replace_workspace_contents` delegates to `_stage_workspace_fixtures`
    (merge, no wipe) in target mode.
  - `delete_agent` / `_delete_agent` gate the target id.
  - `read_primary_model()` reads `agents.defaults.model.primary` (spec #4 US8;
    per-agent `agents.list[].model` overrides are intentionally not consulted).
- `harness/runner.py`: `BenchmarkRunner(target_agent=...)` forwards to the harness.
  - Target-mode live trials: snapshot the target's real workspace before
    `execute_turn`, grade from `live_result.workspace_path` (the real workspace,
    not the temp dir), and roll the real workspace back to its pre-trial snapshot
    after grading via `_sync_workspace_to_snapshot` (merge + delete-extras; the
    target's own `SOUL.md`/`skills/` are preserved).
  - `_run_pending_scenarios`: live workers are clamped to 1 in target mode (the
    target agent is a shared singleton; replay parallelism is unaffected).
- `harness/reporter.py`: `reserve_report_path(slug=...)` is keyed by the agent id.
- `run.py`: `--agent` (default `main`), `--model` optional + auto-resolved from
  `agents.defaults.model.primary`, report slug = agent id. `--continue` drops a
  loaded report whose model differs from the requested one (reports are keyed by
  agent id, so a cross-model `result_<agent>_*.json` is not reused/overwritten).

## Safety invariants the fork guarantees for the target

1. Never `_create_agent` for the target (would force-delete it).
2. Never wipe the target workspace (stage/merge instead); after grading, only
   trial-staged artifacts roll back - the target's own `SOUL.md`/`skills/` persist.
3. Never `_delete_agent` on the target between trials.
4. Never turn isolation on for the target flow (target state == default state).
5. Never run live turns against the target concurrently (live workers clamped to 1).

Tests pinning these: `tests/test_live_harness.py::TargetAgentModeTests`,
`tests/test_runner.py` (target-mode live clamp + grade/restore),
`tests/test_cli.py` (`--agent` / `--model` / slug / cross-model `--continue`).

## Scope of this fork

Phase 1 (this branch): harness + CLI + reporter + tests only. Judge deletion,
old `benchmarks/_common/` retirement, the CI workflow, the bootstrap script, and
the PR renderer are separate, post-green PRs in `research-agent`. Scoring /
`custom_check` logic is unchanged.

Source of truth for the *why*: `research-agent` ADR-0002 + `CONTEXT.md`, and
spec issue `ACautomata/ClawResearchBench#4`.
