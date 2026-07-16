from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harness.custom_checks import run_custom_checks
from harness.loader import load_scenario, scenarios_root
from harness.runner import _copy_workspace_files


SCENARIO_PATH = scenarios_root() / "research" / "idea_generation_ig_001_full_flow.yaml"


def _trace(*events: dict) -> dict:
    return {"events": list(events)}


class ResearchIdeaGenerationIg001Tests(unittest.TestCase):
    def test_known_good_workspace_earns_full_custom_check_score(self) -> None:
        scenario = load_scenario(SCENARIO_PATH)
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            _copy_workspace_files(scenario, workspace)
            run_dir = workspace / "idea-runs" / "ig-001"
            run_dir.mkdir(parents=True)
            (run_dir / "paper-context.md").write_text(
                "TinyRec and SparseRec are evaluated on MovieLens-1M.\n",
                encoding="utf-8",
            )
            (run_dir / "paper-context.json").write_text(
                json.dumps({"papers": ["TinyRec", "SparseRec"]}),
                encoding="utf-8",
            )
            (run_dir / "paper-analysis.md").write_text(
                "TinyRec improves Recall@20 while SparseRec reduces FLOPs.\n",
                encoding="utf-8",
            )
            (run_dir / "ideas.dedup.json").write_text(
                json.dumps(
                    {
                        "ideas": [
                            {
                                "title": "Sparse TinyRec",
                                "evidence": ["TinyRec", "SparseRec"],
                                "metric": "Recall@20",
                                "risk": "Sparse routing may reduce recall",
                                "validation": "Compare on MovieLens-1M",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "recommended-ideas.md").write_text(
                "# Sparse TinyRec\n"
                "Evidence: combine TinyRec and SparseRec on MovieLens-1M.\n"
                "Metric: Recall@20.\n"
                "Risk: sparse routing may reduce recall.\n"
                "Validation: compare against the reported 0.18 and 0.16 results "
                "while checking the 40% FLOPs reduction.\n",
                encoding="utf-8",
            )
            trace = _trace(
                {"type": "tool_call", "tool": "read", "args": {"path": "paper/tinyrec.md"}},
                {"type": "tool_call", "tool": "read", "args": {"path": "paper/sparserec.md"}},
                {
                    "type": "tool_call",
                    "tool": "write",
                    "args": {"path": "idea-runs/ig-001/recommended-ideas.md"},
                },
            )

            result = run_custom_checks(scenario, workspace, trace, [])

        self.assertIsNotNone(result)
        checkpoints = result["checkpoints"]
        self.assertAlmostEqual(sum(item["score"] for item in checkpoints.values()), 1.0)
        self.assertAlmostEqual(sum(item["max"] for item in checkpoints.values()), 1.0)
        self.assertEqual(result["process_score"], 1.0)

    def test_incomplete_fabricated_workspace_loses_required_checkpoints(self) -> None:
        scenario = load_scenario(SCENARIO_PATH)
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            _copy_workspace_files(scenario, workspace)
            run_dir = workspace / "idea-runs" / "ig-001"
            run_dir.mkdir(parents=True)
            (run_dir / "recommended-ideas.md").write_text(
                "TinyRec should reach Recall@20 = 0.99. Metric: Recall@20.\n",
                encoding="utf-8",
            )

            result = run_custom_checks(scenario, workspace, _trace(), [])

        self.assertIsNotNone(result)
        checkpoints = result["checkpoints"]
        self.assertEqual(checkpoints["artifact_paper_context_md"]["score"], 0.0)
        self.assertEqual(checkpoints["artifact_ideas_dedup_json"]["score"], 0.0)
        self.assertEqual(checkpoints["recommended_grounding"]["score"], 0.0)
        self.assertEqual(checkpoints["no_fabricated_numbers"]["score"], 0.0)
        self.assertEqual(result["process_score"], 0.0)


if __name__ == "__main__":
    unittest.main()
