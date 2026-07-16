"""Deterministic grading for research paper-review s4-minimal."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['最小', '子集', '100', '单一自变量', 'P1', '自变量', '控制变量', '预期结果不成立']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s4_minimal.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
