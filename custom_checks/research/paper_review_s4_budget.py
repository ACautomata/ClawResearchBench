"""Deterministic grading for research paper-review s4-budget."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['预算', '$500', '选中', '砍掉', '成本', '自变量', '控制变量', '砍掉理由']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s4_budget.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
