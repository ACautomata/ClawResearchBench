"""Deterministic grading for research paper-review s6-full-normal."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['pipeline', 'S2', 'S3', 'S4', 'S5', '## 0. 文档定位', 'S2', 'S3', 'S4', 'S5']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', 'S2', 'S3', 'S4', 'S5']
OUTPUT_REL = 'outputs/s6_full_normal.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
