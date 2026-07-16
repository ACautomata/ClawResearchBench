"""Deterministic grading for research idea-generate QA-024."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['low-confidence', 'classical baseline', 'MNIST 3vs6', 'binary trivial', 'circuit depth', 'noise model', 'scaling', 'quantum advantage', 'no evidence', 'reproducibility', '8-qubit', 'missing metrics']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
