"""Deterministic grading for research paper-review s3-tot-scope."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['适用', '边界', '仅在', 'GPT-4', '成本', '搜索算法', '证据强度', '已验证范围', '未验证外推']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s3_tot_scope.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
