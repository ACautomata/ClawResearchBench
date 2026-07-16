"""Deterministic grading for research paper-review s2-autocot."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['## 0. 文档定位', '## 8. 值得关注的实验现象', '## 9. 证据充分性整理', '论文中未明确说明', '## 0. 文档定位', '## 1. 实验目标与作者想验证的核心结论', '## 2. 实验设置总览', '## 3. 主结果提取', '## 4. 消融实验提取', '## 5. 参数敏感性与稳定性分析', '## 6. 效率、复杂度与资源代价', '## 7. 鲁棒性、泛化性与补充实验', '## 8. 值得关注的实验现象', '## 9. 证据充分性整理', '## 11. 一段简短总结']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '## 1. 实验目标与作者想验证的核心结论', '## 2. 实验设置总览', '## 3. 主结果提取', '## 4. 消融实验提取', '## 5. 参数敏感性与稳定性分析', '## 6. 效率、复杂度与资源代价', '## 7. 鲁棒性、泛化性与补充实验', '## 8. 值得关注的实验现象', '## 9. 证据充分性整理', '## 11. 一段简短总结']
OUTPUT_REL = 'outputs/s2_autocot.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
