"""Deterministic grading for research paper-review neg-truncated-input."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['材料不完整', '无法获取', '未提供', '## 0. 文档定位', '## 9. 证据充分性整理']
MUST_NOT_CONTAIN = ['Table 1', 'Table 2']
FIELDS = ['## 0. 文档定位', '## 9. 证据充分性整理']
OUTPUT_REL = 'outputs/neg_truncated_input.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
