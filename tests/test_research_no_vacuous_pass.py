from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from harness.loader import load_scenario, scenarios_root
from harness.runner import _copy_workspace_files
from harness.scoring import grade_scenario


RESEARCH_ROOT = scenarios_root() / "research"

# (scenario file, empty-output fixture path) for each Phase 1 research scenario.
# An agent that writes nothing must not pass any of them.
EMPTY_OUTPUT_CASES = [
    ("idea_generation_ig_001_full_flow.yaml", {}),
    ("idea_generation_ig_002_hard_rules.yaml", {"recommended-ideas.md": ""}),
    ("idea_generate_qa_001_paper_only.yaml", {}),
    ("idea_generate_qa_002_paper_plus_code.yaml", {}),
    ("idea_generate_qa_005_constraint_heavy.yaml", {}),
    ("paper_ingest_pi_001_ingest.yaml", {}),
    ("paper_ingest_pi_002_missing_info.yaml", {}),
    ("paper_ingest_pi_003_consistency.yaml", {}),
]


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
    def test_empty_or_missing_output_never_passes(self) -> None:
        for scenario_name, files in EMPTY_OUTPUT_CASES:
            with self.subTest(scenario=scenario_name):
                scenario = load_scenario(RESEARCH_ROOT / scenario_name)
                score = _final_score(scenario_name, files)
                self.assertLess(
                    score,
                    scenario.pass_threshold,
                    f"{scenario_name} passed with empty/missing output at {score} "
                    f"(threshold {scenario.pass_threshold})",
                )


if __name__ == "__main__":
    unittest.main()
