"""Deterministic grading for research paper-review s6-cross-new."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['数字不一致', '3.7%', '4.1%', 'P3', '跳过', '阻塞下游', '留待后续工作', '证据强度', '偏差', '修复建议']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s6_cross_new.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
