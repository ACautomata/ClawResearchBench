"""Deterministic grading for research paper-review seed-003."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['关键前提', '审稿式质疑', '高优先级', '中优先级', '研究空缺', '现有材料不足以确认', '较有证据支持', '合理推测', '## 0. 文档定位', '## 1. 方法机制、实验支撑与关键前提', '## 2. 核心贡献声明与审稿式质疑', '## 3. 潜在问题分析', '## 4. 验证候选问题与优先级', '## 5. 可能形成的研究空缺方向', '## 6. 简短结论']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '## 1. 方法机制、实验支撑与关键前提', '## 2. 核心贡献声明与审稿式质疑', '## 3. 潜在问题分析', '## 4. 验证候选问题与优先级', '## 5. 可能形成的研究空缺方向', '## 6. 简短结论']
OUTPUT_REL = 'outputs/seed_003.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
