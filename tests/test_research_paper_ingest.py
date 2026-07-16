from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from harness.custom_checks import run_custom_checks
from harness.loader import load_scenario, scenarios_root
from harness.runner import _copy_workspace_files


RESEARCH_SCENARIOS = scenarios_root() / "research"


def _run_check(scenario_name: str, files: dict[str, str]) -> dict:
    scenario = load_scenario(RESEARCH_SCENARIOS / scenario_name)
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        _copy_workspace_files(scenario, workspace)
        for relative_path, content in files.items():
            target = workspace / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        result = run_custom_checks(scenario, workspace, {"events": []}, [])
    assert result is not None
    return result


def _sections() -> str:
    return "\n".join(f"## {index}. Section {index}" for index in range(16))


class ResearchPaperIngestTests(unittest.TestCase):
    def test_pi_001_grades_complete_wiki_ingest(self) -> None:
        page = (
            "---\ntitle: BenchIngest\ntype: paper\ndomain: bench\n"
            "evidence_level: synthetic\ncreated: 2026-07-17\nupdated: 2026-07-17\n---\n"
            + _sections()
            + "\n## 15. 一句话总结\nSynthetic pipeline note.\n"
        )
        good = _run_check(
            "paper_ingest_pi_001_ingest.yaml",
            {
                "wiki/domains/bench/papers/benchingest.md": page,
                "wiki/index.md": "bench/papers/benchingest.md\n",
                "wiki/log.md": "2026-07-17 ingested BenchIngest\n",
            },
        )
        bad = _run_check(
            "paper_ingest_pi_001_ingest.yaml",
            {"wiki/domains/bench/papers/benchingest.md": "# BenchIngest\n"},
        )

        self.assertAlmostEqual(sum(item["score"] for item in good["checkpoints"].values()), 1.0)
        self.assertEqual(bad["checkpoints"]["all_sections_present"]["score"], 0.0)
        self.assertEqual(bad["checkpoints"]["index_updated"]["score"], 0.0)
        self.assertEqual(bad["checkpoints"]["log_updated"]["score"], 0.0)

    def test_pi_002_grades_missing_information_handling(self) -> None:
        page = (
            "---\ntitle: edge-aware regularization\ntype: paper\ndomain: gnn\n"
            "evidence_level: abstract\ncreated: 2026-07-17\nupdated: 2026-07-17\n---\n"
            + _sections()
            + "\n论文中未明确说明。\n## 15. 一句话总结\n"
            "Edge-aware regularization encourages smooth predictions across connected nodes.\n"
        )
        good = _run_check(
            "paper_ingest_pi_002_missing_info.yaml",
            {"wiki/domains/bench/papers/edge-reg.md": page},
        )
        bad = _run_check(
            "paper_ingest_pi_002_missing_info.yaml",
            {"wiki/domains/bench/papers/edge-reg.md": "可能是一个 GNN 方法。\n"},
        )

        self.assertAlmostEqual(sum(item["score"] for item in good["checkpoints"].values()), 1.0)
        self.assertEqual(bad["checkpoints"]["all_sections_present"]["score"], 0.0)
        self.assertEqual(bad["checkpoints"]["missing_information_explicit"]["score"], 0.0)

    def test_pi_003_grades_cross_paper_comparison(self) -> None:
        good = _run_check(
            "paper_ingest_pi_003_consistency.yaml",
            {
                "wiki/domains/gnn-regularization/comparison.md": (
                    "# Comparison\n"
                    "edge-aware evaluates homophilous Cora and CiteSeer against a GCN baseline, "
                    "with evidence of a 1-3% gain. gated attention instead evaluates the "
                    "heterophilous Chameleon setting; this evidence is not directly comparable.\n"
                )
            },
        )
        bad = _run_check(
            "paper_ingest_pi_003_consistency.yaml",
            {
                "wiki/domains/gnn-regularization/comparison.md": (
                    "edge-aware beats gated attention by 25% on every dataset.\n"
                )
            },
        )

        self.assertAlmostEqual(sum(item["score"] for item in good["checkpoints"].values()), 1.0)
        self.assertLess(bad["checkpoints"]["source_keyword_coverage"]["score"], 0.7)
        self.assertEqual(bad["checkpoints"]["no_fabricated_numbers"]["score"], 0.0)


if __name__ == "__main__":
    unittest.main()
