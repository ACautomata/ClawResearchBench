"""Deterministic grading for research idea-generate QA-013."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['patch embedding', 'high-frequency', 'inductive bias', 'corruption error', 'robustness gap', 'ViT', 'CNN', 'augmentation', 'OOD', 'Fourier', 'regularization', 'attention']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
