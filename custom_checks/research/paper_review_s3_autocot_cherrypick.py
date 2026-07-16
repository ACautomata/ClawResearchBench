"""Deterministic grading for research paper-review s3-autocot-cherrypick."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['选择性', '算术', '符号', '2-3%']
MUST_NOT_CONTAIN = ['所有 benchmark 均等提升']
FIELDS = []
OUTPUT_REL = 'outputs/s3_autocot_cherrypick.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
