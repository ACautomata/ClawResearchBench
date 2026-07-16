"""Deterministic grading for research idea-generate QA-008."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['knowledge distillation', 'pruning', '10MB', 'accuracy retention', 'latency', 'temperature scaling', 'sparsity', 'iterative', 'MobileNet', 'edge deployment']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
