"""Deterministic grading for research paper-review s3-baseline."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['训练时间', '不对等', 'fair', '超参数搜索空间', 'SVD 参数化', '证据强度', '反事实设计', '资源不对称']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s3_baseline.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
