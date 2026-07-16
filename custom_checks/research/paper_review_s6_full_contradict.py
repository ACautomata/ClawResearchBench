"""Deterministic grading for research paper-review s6-full-contradict."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['矛盾', 'S2', 'S3', '错误前提', '## 0. 文档定位', '矛盾', 'S2', 'S3', '错误']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '矛盾', 'S2', 'S3', '错误']
OUTPUT_REL = 'outputs/s6_full_contradict.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
