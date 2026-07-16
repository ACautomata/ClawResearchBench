"""Deterministic grading for research paper-review s3-sr-dependency."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['外部依赖', '自我评估', '归因', '弱模型', '退化', '证据强度', '区分实验', '依赖充分性']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s3_sr_dependency.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
