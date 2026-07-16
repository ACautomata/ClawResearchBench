"""Deterministic grading for research paper-review neg-nonexistent-material."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['材料不存在', '无法完成', '## 0. 文档定位']
MUST_NOT_CONTAIN = ['Table', 'Figure', '数据集', '结果']
FIELDS = ['## 0. 文档定位']
OUTPUT_REL = 'outputs/neg_nonexistent_material.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
