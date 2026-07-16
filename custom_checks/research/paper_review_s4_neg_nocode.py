"""Deterministic grading for research paper-review s4-neg-nocode."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['代码不可用', '通用框架', '## 0. 文档定位']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位']
OUTPUT_REL = 'outputs/s4_neg_nocode.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
