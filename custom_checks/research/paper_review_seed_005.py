"""Deterministic grading for research paper-review seed-005."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['# 发给 claude-code 的完整任务提示词', '最小侵入', '复用', '此处应填写代码仓库路径', '结果保存', '不重构', '配置化', '# 发给 claude-code 的完整任务提示词', '## 1. 任务背景', '## 2. 可用输入材料', '## 3. 当前论文方法与验证目标', '## 4. 优先实现的验证实验', '## 5. 总体实现要求', '## 6. 建议优先查看的代码位置', '## 7. 交付内容', '## 8. 完成标准', '## 9. claude-code 完成后的汇报格式', '## 10. 一句话目标总结']
MUST_NOT_CONTAIN = []
FIELDS = ['# 发给 claude-code 的完整任务提示词', '## 1. 任务背景', '## 2. 可用输入材料', '## 3. 当前论文方法与验证目标', '## 4. 优先实现的验证实验', '## 5. 总体实现要求', '## 6. 建议优先查看的代码位置', '## 7. 交付内容', '## 8. 完成标准', '## 9. claude-code 完成后的汇报格式', '## 10. 一句话目标总结']
OUTPUT_REL = 'outputs/seed_005.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
