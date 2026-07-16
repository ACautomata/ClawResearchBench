"""Deterministic grading for research paper-review s3-vpt-cherrypick."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['选择性', '叙事', '强调', '弱化', '## 0. 文档定位', '## 1. 方法机制、实验支撑与关键前提', '## 2. 核心贡献声明与审稿式质疑', '## 6. 简短结论']
MUST_NOT_CONTAIN = ['选择性报告不影响结论']
FIELDS = ['## 0. 文档定位', '## 1. 方法机制、实验支撑与关键前提', '## 2. 核心贡献声明与审稿式质疑', '## 6. 简短结论']
OUTPUT_REL = 'outputs/s3_vpt_cherrypick.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
