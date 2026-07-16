"""Deterministic grading for research paper-review s4-neg-impossible."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['不可能', '无法设计', '## 0. 文档定位']
MUST_NOT_CONTAIN = ['可以设计', '建议使用']
FIELDS = ['## 0. 文档定位']
OUTPUT_REL = 'outputs/s4_neg_impossible.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
