"""Deterministic grading for research idea-generate QA-026."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['subject-independent', 'data leakage', 'DEAP', 'EEG', 'emotion recognition', 'evaluation protocol', 'subject-wise', 'inflated accuracy', 'valance', 'LSTM', 'cross-subject', 'confound']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
