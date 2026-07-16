"""Deterministic grading for research paper-review s2-selfinstruct-data."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['## 0. 文档定位', '论文中未明确说明', '消融', '## 0. 文档定位', '## 3. 主结果提取', '## 4. 消融实验提取', '## 9. 证据充分性整理']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '## 3. 主结果提取', '## 4. 消融实验提取', '## 9. 证据充分性整理']
OUTPUT_REL = 'outputs/s2_selfinstruct_data.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
