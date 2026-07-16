"""Deterministic grading for research paper-review s3-tot-competing."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['竞争性假设', 'GPT-4', '搜索', 'CoT', '可检验', '证据强度', '因果链', '可检验预测']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s3_tot_competing.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
