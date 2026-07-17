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
  - `_replace_workspace_contents` delegates to `_stage_workspace_fixtures`
    (merge, no wipe) in target mode.
  - `delete_agent` / `_delete_agent` gate the target id.
  - `read_primary_model()` reads `agents.defaults.model.primary`.
- `harness/runner.py`: `BenchmarkRunner(target_agent=...)` forwards to the harness.
- `harness/reporter.py`: `reserve_report_path(slug=...)` is keyed by the agent id.
- `run.py`: `--agent` (default `main`), `--model` optional + auto-resolved from
  `agents.defaults.model.primary`, report slug = agent id.

## Safety invariants the fork guarantees for the target

1. Never `_create_agent` for the target (would force-delete it).
2. Never wipe the target workspace (stage/merge instead).
3. Never `_delete_agent` on the target between trials.
4. Never turn isolation on for the target flow (target state == default state).

Tests pinning these: `tests/test_live_harness.py::TargetAgentModeTests`,
`tests/test_cli.py` (`--agent` / `--model` / slug).

## Scope of this fork

Phase 1 (this branch): harness + CLI + reporter + tests only. Judge deletion,
old `benchmarks/_common/` retirement, the CI workflow, the bootstrap script, and
the PR renderer are separate, post-green PRs in `research-agent`. Scoring /
`custom_check` logic is unchanged.

Source of truth for the *why*: `research-agent` ADR-0002 + `CONTEXT.md`, and
spec issue `ACautomata/ClawResearchBench#4`.
