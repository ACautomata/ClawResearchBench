"""Deterministic grading for research paper-review s4-reflexion-minimal."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['单变量', '控制', '最小', '隔离', '## 0. 文档定位', '## 3. 核心验证实验设计']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '## 3. 核心验证实验设计']
OUTPUT_REL = 'outputs/s4_reflexion_minimal.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
