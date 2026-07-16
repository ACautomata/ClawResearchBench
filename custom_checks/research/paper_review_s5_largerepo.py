"""Deterministic grading for research paper-review s5-largerepo."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['adalora.py', 'run_glue.py', 'SVDLinear', 'RankAllocator', '建议优先查看的代码位置', '行号', '完成标准']
MUST_NOT_CONTAIN = []
FIELDS = []
OUTPUT_REL = 'outputs/s5_largerepo.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
