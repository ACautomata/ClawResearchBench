from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from harness.custom_checks import run_custom_checks
from harness.loader import load_scenario, scenarios_root
from harness.runner import _copy_workspace_files
from harness.scoring import grade_scenario


ROOT = scenarios_root() / "research"


def _final(rel_yaml: str, files: dict[str, str]) -> float:
    s = load_scenario(ROOT / rel_yaml)
    with tempfile.TemporaryDirectory() as d:
        w = Path(d)
        _copy_workspace_files(s, w)
        for rp, c in files.items():
            p = w / rp
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(c, encoding="utf-8")
        return grade_scenario(s, w, {"events": []}).final_score


class ResearchPhase2SampleTests(unittest.TestCase):
    """Sample-based smoke tests for generated Phase 2 scenarios."""

    # ---------- idea-generate (keyword-coverage) ----------

    def test_ideagen_rules_empty_fails(self) -> None:
        s = _final("idea_generate_qa_011.yaml", {})
        self.assertLess(s, 0.5)

    def test_ideagen_rules_known_good_passes(self) -> None:
        s = _final("idea_generate_qa_011.yaml",
                   {"recommended-ideas.md": (
                       "default assumption about problematization and causal spurious "
                       "correlation. OOD fidelity, generalization gap, distribution shift, "
                       "template memorization from GNNExplainer and PGExplainer using "
                       "counterfactual intervention.\n")})
        self.assertGreater(s, 0.5)

    # ---------- paper-review inline (must_contain + fields) ----------

    def test_pr_inline_empty_fails(self) -> None:
        s = _final("paper_review_s6_boundary_new.yaml", {})
        self.assertLess(s, 0.5)

    def test_pr_inline_known_good_passes(self) -> None:
        content = (
            "## 0. 越界\n"
            "S2 到 S3 阶段边界问题：2.3% 精度退化写成约2%，"
            "阻塞下游修复建议；区分预期结果与结论化表达。\n"
        )
        s = _final("paper_review_s6_boundary_new.yaml",
                   {"outputs/s6_boundary_new.md": content})
        self.assertGreater(s, 0.5)

    # ---------- paper-review synth-wiki (edgereg-gnn fixture) ----------

    def test_pr_synth_incomplete_empty_fails(self) -> None:
        s = _final("paper_review_s2_incomplete.yaml", {})
        self.assertLess(s, 0.5)

    def test_pr_synth_incomplete_known_good_passes(self) -> None:
        content = "\n".join(f"## {i}. section" for i in range(12))
        content += "\nEdgeReg-GNN edge-aware 正则化 Cora 83.2% CiteSeer 72.1% 论文中未明确说明\n"
        s = _final("paper_review_s2_incomplete.yaml",
                   {"outputs/s2_incomplete.md": content})
        self.assertGreater(s, 0.5)

    # ---------- paper-review full-text ref (react_full.md, third-party) ----------

    def test_pr_thirdparty_empty_fails(self) -> None:
        s = _final("paper_review_s2_nonstandard.yaml", {})
        self.assertLess(s, 0.5)

    # ---------- pipeline (PRP multi-output) ----------

    def test_pipeline_empty_fails(self) -> None:
        s = _final("paper_review_pipeline_prp_002.yaml", {})
        self.assertLess(s, 0.5)


class ResearchNoVacuousPassPhase2Tests(unittest.TestCase):
    """Spot-check vacuous-pass prevention across representative families."""

    def _assert_empty_fails(self, yaml_name: str, empty: dict = {}) -> None:
        s = load_scenario(ROOT / yaml_name)
        self.assertLess(_final(yaml_name, empty), s.pass_threshold,
                        f"{yaml_name} passed with empty output")

    def test_ideagen_sample_empty(self) -> None:
        self._assert_empty_fails("idea_generate_qa_030.yaml", {})

    def test_pr_sample_empty(self) -> None:
        self._assert_empty_fails("paper_review_s6_boundary_new.yaml", {})

    def test_pr_thirdparty_sample_empty(self) -> None:
        self._assert_empty_fails("paper_review_s2_nonstandard.yaml", {})


if __name__ == "__main__":
    unittest.main()
