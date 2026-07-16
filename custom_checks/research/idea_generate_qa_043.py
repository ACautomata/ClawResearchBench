"""Deterministic grading for research idea-generate QA-043."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['Hinton', 'FitNet', 'CRD', 'ReviewKD', 'MaskedKD', 'cross-architecture', 'imperfect teacher', 'OOD distillation', 'lineage', 'incremental', 'paradigm', 'gap', 'Venn diagram', 'uncovered', 'delta']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
