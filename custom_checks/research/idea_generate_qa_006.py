"""Deterministic grading for research idea-generate QA-006."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['oversmoothing', 'residual connection', 'split protocol', 'train/test leakage', 'representation similarity', 'controlled re-evaluation', 'layer-wise', 'Cora', 'node classification', 'depth']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
