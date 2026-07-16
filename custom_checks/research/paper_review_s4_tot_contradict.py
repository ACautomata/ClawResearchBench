"""Deterministic grading for research paper-review s4-tot-contradict."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['矛盾', '区分', 'H1', 'H2', '## 0. 文档定位', '## 1. 验证目标总览', '## 3. 核心验证实验设计']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '## 1. 验证目标总览', '## 3. 核心验证实验设计']
OUTPUT_REL = 'outputs/s4_tot_contradict.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
