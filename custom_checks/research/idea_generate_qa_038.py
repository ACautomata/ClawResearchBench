"""Deterministic grading for research idea-generate QA-038."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['more data assumption', 'low-resource', 'synthetic data harm', 'language typology', 'SOV vs SVO', 'data quality vs quantity', 'MasakhaNER', 'FLORES', 'annotation bias', 'problematization', 'language-specific', 'data curation']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
