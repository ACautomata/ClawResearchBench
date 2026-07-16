"""Deterministic grading for research idea-generate QA-027."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['prompt template', 'non-native', 'TOEFL', 'rater bias', 'language background', 'fairness', 'BERT baseline', 'inter-rater', 'reproducibility', 'essay scoring', 'confound', 'stratification']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
