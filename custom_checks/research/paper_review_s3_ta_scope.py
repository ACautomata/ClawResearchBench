"""Deterministic grading for research paper-review s3-ta-scope."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['适用', '边界', '仅在', 'CLIP', 'shot', 'domain shift', '证据强度', '已验证范围', '未验证外推']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s3_ta_scope.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
