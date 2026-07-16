"""Deterministic grading for research paper-review s6-cross-drift."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['不一致', 'claim', '优先级', '## 0. 文档定位', '不一致', '证据', '修复']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '不一致', '证据', '修复']
OUTPUT_REL = 'outputs/s6_cross_drift.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
