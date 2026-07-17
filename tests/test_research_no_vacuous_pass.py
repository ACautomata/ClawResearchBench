from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from harness.loader import load_scenario, scenarios_root
from harness.runner import _copy_workspace_files
from harness.scoring import grade_scenario


RESEARCH_ROOT = scenarios_root() / "research"


def _research_yaml_names() -> list[str]:
    return sorted(path.name for path in RESEARCH_ROOT.glob("*.yaml"))


def _final_score(scenario_name: str, files: dict[str, str]) -> float:
    scenario = load_scenario(RESEARCH_ROOT / scenario_name)
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        _copy_workspace_files(scenario, workspace)
        for relative_path, content in files.items():
            target = workspace / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        breakdown = grade_scenario(scenario, workspace, {"events": []})
    return breakdown.final_score


class ResearchNoVacuousPassTests(unittest.TestCase):
    """An agent that writes no output must not pass any research scenario.

    Covers every research scenario (Phase 1 + Phase 2 + pipeline), exercised
    through the grade_scenario black-box seam — the test does not know or care
    whether a grader or a standalone produced the score.
    """

    def test_empty_output_never_passes_any_research_scenario(self) -> None:
        names = _research_yaml_names()
        self.assertGreater(len(names), 0, "no research scenarios discovered")
        for scenario_name in names:
            with self.subTest(scenario=scenario_name):
                scenario = load_scenario(RESEARCH_ROOT / scenario_name)
                score = _final_score(scenario_name, {})
                self.assertLess(
                    score,
                    scenario.pass_threshold,
                    f"{scenario_name} passed with no output at {score} "
                    f"(threshold {scenario.pass_threshold})",
                )


if __name__ == "__main__":
    unittest.main()
