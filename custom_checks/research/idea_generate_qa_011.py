"""Deterministic grading for research idea-generate QA-011."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['default assumption', 'problematization', 'causal', 'spurious correlation', 'OOD fidelity', 'generalization gap', 'distribution shift', 'template memorization', 'GNNExplainer', 'PGExplainer', 'counterfactual', 'intervention']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
