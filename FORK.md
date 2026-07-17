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
  - `BenchmarkRunner.__init__` rejects target-agent mode combined with isolated
    state (non-default `--openclaw-profile`/`--openclaw-state-dir`/`--openclaw-config-path`)
    via `_uses_isolated_state()` - a fresh isolated state has no target workspace
    and target mode never runs `agents add`. Pointing `--openclaw-config-path` at
    颉姗's real default config is allowed (returns False).
  - `run_with_resume` rejects an explicit `--model` that differs from the target's
    configured `agents.defaults.model.primary`: `_agent_command` has no `--model`
    flag so the agent runs its configured model; a mismatch would mislabel
    pricing/report/resume.
  - Target-mode live trials: snapshot the target's real workspace before
    `execute_turn`, clear stale scenario-owned paths (`_clear_scenario_owned_target_paths`
    - `file_exists`/`file_contains` check paths + fixture dests + seed-dir entries;
    traversal-guarded, never touches `SOUL.md`/`skills/`) BEFORE the snapshot so it
    is a clean baseline, grade from `live_result.workspace_path` (the real
    workspace, not the temp dir), and roll the real workspace back to the snapshot
    after grading via `_sync_workspace_to_snapshot` (merge + delete-extras).
  - `_run_pending_scenarios`: live workers are clamped to 1 in target mode (the
    target agent is a shared singleton; replay parallelism is unaffected).
- `harness/reporter.py`: `reserve_report_path(slug=...)` is keyed by the agent id.
- `run.py`: `--agent` (default `main`), `--model` optional + auto-resolved from
  `agents.defaults.model.primary`, report slug = agent id. `--continue` drops a
  loaded report whose model differs from the requested one (reports are keyed by
  agent id, so a cross-model `result_<agent>_*.json` is not reused/overwritten).

## Safety invariants the fork guarantees for the target

1. Never `_create_agent` for the target (would force-delete it).
2. Never wipe the target workspace (stage/merge instead); stale scenario-owned
   outputs are cleared before the pre-trial snapshot, and after grading only
   trial-staged artifacts roll back - the target's own `SOUL.md`/`skills/` persist.
3. Never `_delete_agent` on the target between trials.
4. Never turn isolation on for the target flow (rejected at runner init if
   state/config resolve outside the default).
5. Never run live turns against the target concurrently (live workers clamped to 1).
6. Never run the target under a model other than the one recorded (explicit
   `--model` mismatching the configured primary is rejected at `run_with_resume`).

Tests pinning these: `tests/test_live_harness.py::TargetAgentModeTests`,
`tests/test_runner.py` (target-mode live clamp + grade/restore + stale-clear +
isolated-state/model-mismatch rejection),
`tests/test_cli.py` (`--agent` / `--model` / slug / cross-model `--continue`).

## Scope of this fork

Phase 1 (this branch): harness + CLI + reporter + tests only. Judge deletion,
old `benchmarks/_common/` retirement, the CI workflow, the bootstrap script, and
the PR renderer are separate, post-green PRs in `research-agent`. Scoring /
`custom_check` logic is unchanged.

Source of truth for the *why*: `research-agent` ADR-0002 + `CONTEXT.md`, and
spec issue `ACautomata/ClawResearchBench#4`.
