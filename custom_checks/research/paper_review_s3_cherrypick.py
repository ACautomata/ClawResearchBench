"""Deterministic grading for research paper-review s3-cherrypick."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['选择性报告', 'Best-of-6', 'Average', '14个百分点', '71%', '57%', '叙事偏差', '证据强度', '反事实设计', '叙事修正']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s3_cherrypick.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
