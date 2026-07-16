"""Deterministic grading for research idea-generate QA-004."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['low-confidence', 'evidence-weak', 'baseline reproduction', 'missing', 'spectroscopy', 'open question', 'dataset name', 'metric value', 'statistical significance', 'generalization']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
