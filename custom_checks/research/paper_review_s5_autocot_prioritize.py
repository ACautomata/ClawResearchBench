"""Deterministic grading for research paper-review s5-autocot-prioritize."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['# 发给 claude-code 的完整任务提示词', '优先级', '排序', '理由', '# 发给 claude-code 的完整任务提示词', '## 4. 优先实现的验证实验']
MUST_NOT_CONTAIN = []
FIELDS = ['# 发给 claude-code 的完整任务提示词', '## 4. 优先实现的验证实验']
OUTPUT_REL = 'outputs/s5_autocot_prioritize.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
