"""Deterministic grading for research paper-review s6-boundary-s2-s3."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['边界', '越界', '阶段', '## 0. 文档定位', '边界', '越界', '阶段', '严重']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '边界', '越界', '阶段', '严重']
OUTPUT_REL = 'outputs/s6_boundary_s2_s3.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
