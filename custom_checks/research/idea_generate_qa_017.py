"""Deterministic grading for research idea-generate QA-017."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['transferability', 'black-box', 'surrogate ensemble', 'MI-FGSM', 'PGD', 'attack success rate', 'Lp norm', 'defense', 'gradient', 'momentum', 'decision boundary', 'query']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
