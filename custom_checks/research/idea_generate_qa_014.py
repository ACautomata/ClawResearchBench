"""Deterministic grading for research idea-generate QA-014."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['Neural ODE', 'irregular sampling', 'solver steps', 'AUROC', 'PhysioNet', 'time encoding', 'attention', 'continuous dynamics', 'GRU', 'efficiency', 'adjoint', 'stiffness']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
