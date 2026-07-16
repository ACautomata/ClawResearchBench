"""Deterministic grading for research paper-review s4-vpt-budget."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['预算', '优先级', '最小', '自变量', '## 0. 文档定位', '## 1. 验证目标总览', '## 3. 核心验证实验设计', '## 5. 实验优先级排序']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '## 1. 验证目标总览', '## 3. 核心验证实验设计', '## 5. 实验优先级排序']
OUTPUT_REL = 'outputs/s4_vpt_budget.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
