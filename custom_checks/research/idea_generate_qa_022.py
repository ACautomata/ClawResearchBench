"""Deterministic grading for research idea-generate QA-022."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['SimSiam', 'predictor depth', 'collapse', 't-SNE', 'dimensional collapse', 'stop-gradient', 'negative-free', 'projector', 'linear probing', 'rank', 'degeneration', 'regularization']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
