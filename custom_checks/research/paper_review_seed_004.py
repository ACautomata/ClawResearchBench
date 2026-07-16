"""Deterministic grading for research paper-review seed-004."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['自变量', '控制变量', '观测指标', '预期可能出现的结果', '实验成本判断', '最小可执行版本', '如果问题成立', '如果问题不成立', '高优先级', '中优先级', '## 0. 文档定位', '## 1. 验证目标总览', '## 2. 实验设计原则', '## 3. 核心验证实验设计', '## 4. 可选补充实验', '## 5. 实验优先级排序', '## 6. 最值得优先执行的 3 个实验', '## 7. 这些实验可能支撑的后续研究方向', '## 8. 简短总结', '## 9. 输出要求说明']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '## 1. 验证目标总览', '## 2. 实验设计原则', '## 3. 核心验证实验设计', '## 4. 可选补充实验', '## 5. 实验优先级排序', '## 6. 最值得优先执行的 3 个实验', '## 7. 这些实验可能支撑的后续研究方向', '## 8. 简短总结', '## 9. 输出要求说明']
OUTPUT_REL = 'outputs/seed_004.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
