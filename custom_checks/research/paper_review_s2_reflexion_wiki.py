"""Deterministic grading for research paper-review s2-reflexion-wiki."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['## 0. 文档定位', 'Reflexion', 'HumanEval', 'ALFWorld']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s2_reflexion_wiki.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
