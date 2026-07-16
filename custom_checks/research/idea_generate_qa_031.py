"""Deterministic grading for research idea-generate QA-031."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['attention', 'interpretability', 'adversarial perturbation', 'fair perturbation', 'constraint set', 'SNLI', 'decision boundary', 'feature importance', 'explanation fidelity', 'methodology disagreement', 'controlled evaluation', 'counterfactual']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
