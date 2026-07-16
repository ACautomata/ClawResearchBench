"""Deterministic grading for research paper-review seed-006."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['论文中未明确说明', '## 0. 元信息', '## 15. 一句话总结', 'edge-aware', '## 0. 元信息', '## 4. 方法总览', '## 6. 关键公式与机制说明', '## 8. 实验设置', '## 15. 一句话总结']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 元信息', '## 4. 方法总览', '## 6. 关键公式与机制说明', '## 8. 实验设置', '## 15. 一句话总结']
OUTPUT_REL = 'outputs/seed_006.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
