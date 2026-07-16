"""Deterministic grading for research idea-generate QA-021."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['DARTS', 'zero-cost proxy', 'search cost', 'NAS-Bench', 'Spearman', 'random baseline', 'p-value', 'architecture ranking', 'search space', 'proxy quality', 'correlation collapse', 'efficiency']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
