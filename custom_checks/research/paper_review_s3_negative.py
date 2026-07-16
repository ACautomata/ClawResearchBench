"""Deterministic grading for research paper-review s3-negative."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['负向', '退化', '持平', '高 budget', 'CNN/DailyMail', '平衡', '证据强度', '证据分布', '叙事匹配']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s3_negative.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
