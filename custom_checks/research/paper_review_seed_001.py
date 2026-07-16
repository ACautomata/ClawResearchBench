"""Deterministic grading for research paper-review seed-001."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['## 0. 元信息', '## 15. 一句话总结', 'FedAux', 'federated', 'auxiliary', '论文中未明确说明', '## 0. 元信息', '## 1. 研究背景', '## 2. 任务定义', '## 3. 论文要解决的核心问题', '## 4. 方法总览', '## 5. 方法关键模块', '## 6. 关键公式与机制说明', '## 7. 训练与推理流程', '## 8. 实验设置', '## 9. 主要实验结果', '## 10. 论文贡献总结', '## 11. 方法特点总结', '## 12. 术语与概念表', '## 13. 可复现信息', '## 14. 适合后续研究时重点关注的内容', '## 15. 一句话总结']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 元信息', '## 1. 研究背景', '## 2. 任务定义', '## 3. 论文要解决的核心问题', '## 4. 方法总览', '## 5. 方法关键模块', '## 6. 关键公式与机制说明', '## 7. 训练与推理流程', '## 8. 实验设置', '## 9. 主要实验结果', '## 10. 论文贡献总结', '## 11. 方法特点总结', '## 12. 术语与概念表', '## 13. 可复现信息', '## 14. 适合后续研究时重点关注的内容', '## 15. 一句话总结']
OUTPUT_REL = 'outputs/seed_001.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
