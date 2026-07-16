"""Deterministic grading for research paper-review s5-neg-oversized."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['# 发给 claude-code 的完整任务提示词', '规模', '不确定', '# 发给 claude-code 的完整任务提示词', '## 1. 任务背景']
MUST_NOT_CONTAIN = []
FIELDS = ['# 发给 claude-code 的完整任务提示词', '## 1. 任务背景']
OUTPUT_REL = 'outputs/s5_neg_oversized.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
