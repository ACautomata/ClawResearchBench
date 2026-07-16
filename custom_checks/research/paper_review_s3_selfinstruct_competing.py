"""Deterministic grading for research paper-review s3-selfinstruct-competing."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['H1', 'H2', 'H3', '竞争性', '替代', '## 0. 文档定位', '## 2. 核心贡献声明与审稿式质疑', '## 3. 潜在问题分析']
MUST_NOT_CONTAIN = ['论文自身的解释已足够']
FIELDS = ['## 0. 文档定位', '## 2. 核心贡献声明与审稿式质疑', '## 3. 潜在问题分析']
OUTPUT_REL = 'outputs/s3_selfinstruct_competing.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
