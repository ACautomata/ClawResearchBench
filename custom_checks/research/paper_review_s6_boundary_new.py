"""Deterministic grading for research paper-review s6-boundary-new."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['越界', 'S2', 'S3', 'S4', '阶段边界', '精度退化', '2.3%', '约2%', '预期结果', '结论化表达', '阻塞下游', '修复建议']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s6_boundary_new.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
