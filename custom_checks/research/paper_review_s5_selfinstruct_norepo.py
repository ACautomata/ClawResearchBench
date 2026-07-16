"""Deterministic grading for research paper-review s5-selfinstruct-norepo."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['# 发给 claude-code 的完整任务提示词', '此处应填写代码仓库路径', '占位符', '# 发给 claude-code 的完整任务提示词', '## 6. 建议优先查看的代码位置']
MUST_NOT_CONTAIN = ['model.py', 'data.py', 'train.py']
FIELDS = ['# 发给 claude-code 的完整任务提示词', '## 6. 建议优先查看的代码位置']
OUTPUT_REL = 'outputs/s5_selfinstruct_norepo.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
