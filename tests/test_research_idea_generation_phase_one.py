from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from harness.custom_checks import run_custom_checks
from harness.loader import load_scenario, scenarios_root
from harness.runner import _copy_workspace_files


SCENARIO_ROOT = scenarios_root() / "research"


def _grade(scenario_name: str, output: str | None) -> dict:
    scenario = load_scenario(SCENARIO_ROOT / scenario_name)
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        _copy_workspace_files(scenario, workspace)
        if output is not None:
            target = workspace / "recommended-ideas.md"
            target.write_text(output, encoding="utf-8")
        result = run_custom_checks(scenario, workspace, {"events": []}, [])
    assert result is not None
    return result


class ResearchIdeaGenerationPhaseOneTests(unittest.TestCase):
    def test_ig_002_grades_hard_rules_and_rejects_unsupported_claims(self) -> None:
        good = _grade(
            "idea_generation_ig_002_hard_rules.yaml",
            "TinyRec evidence: L2 normalization and Recall@20 = 0.18 on MovieLens-1M.\n"
            "Metric: Recall@20. Risk: normalization may hurt ranking. "
            "Validation: compare with the 0.15 MF baseline.\n",
        )
        bad = _grade(
            "idea_generation_ig_002_hard_rules.yaml",
            "TinyRec should probably achieve Recall@20 = 0.99.\n",
        )

        self.assertAlmostEqual(sum(item["score"] for item in good["checkpoints"].values()), 1.0)
        self.assertEqual(bad["checkpoints"]["hard_rule_coverage"]["score"], 0.0)
        self.assertEqual(bad["checkpoints"]["no_unsupported_language"]["score"], 0.0)
        self.assertEqual(bad["checkpoints"]["no_fabricated_numbers"]["score"], 0.0)

    def test_qa_001_uses_source_keyword_coverage(self) -> None:
        good = _grade(
            "idea_generate_qa_001_paper_only.yaml",
            "Three ideas combine trajectory matching and class-balanced sampling for a synthetic "
            "CIFAR-LT set. Track minority class accuracy and balanced accuracy by samples per class; "
            "control the distillation budget, majority class overfitting, and other overfitting risks.\n",
        )
        partial = _grade(
            "idea_generate_qa_001_paper_only.yaml",
            "trajectory matching with class-balanced sampling on a synthetic set; "
            "measure minority class accuracy and CIFAR-LT balanced accuracy.\n",
        )

        self.assertEqual(good["checkpoints"]["keyword_coverage"]["score"], 0.9)
        self.assertEqual(partial["checkpoints"]["keyword_coverage"]["score"], 0.54)

    def test_qa_002_enforces_backbone_constraint(self) -> None:
        good = _grade(
            "idea_generate_qa_002_paper_plus_code.yaml",
            "Use maximum concept matching in the existing CLIP inference scoring function. "
            "Tune calibration and threshold for fine-grained OOD cases; measure AUROC and FPR95 "
            "without changing the backbone.\n",
        )
        bad = _grade(
            "idea_generate_qa_002_paper_plus_code.yaml",
            "Retrain the backbone and replace the CLIP inference pipeline.\n",
        )

        self.assertEqual(good["checkpoints"]["constraint_following"]["score"], 0.1)
        self.assertEqual(bad["checkpoints"]["constraint_following"]["score"], 0.0)

    def test_qa_005_grades_resource_constraint_keywords(self) -> None:
        good = _grade(
            "idea_generate_qa_005_constraint_heavy.yaml",
            "Starting from FedAvg on the non-IID benchmark, use a single GPU for at most 8 hours. "
            "Test client personalization via regularization and local fine-tuning; compare "
            "communication rounds and worst-client accuracy.\n",
        )
        missing = _grade("idea_generate_qa_005_constraint_heavy.yaml", None)

        self.assertAlmostEqual(sum(item["score"] for item in good["checkpoints"].values()), 1.0)
        self.assertEqual(missing["checkpoints"]["output_exists"]["score"], 0.0)
        self.assertEqual(missing["checkpoints"]["keyword_coverage"]["score"], 0.0)


if __name__ == "__main__":
    unittest.main()
