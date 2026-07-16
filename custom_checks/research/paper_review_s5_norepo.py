"""Deterministic grading for research paper-review s5-norepo."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['# 发给 claude-code 的完整任务提示词', '此处应填写代码仓库路径', '自行实现', '完成标准', '限制说明', '占位符']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s5_norepo.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
