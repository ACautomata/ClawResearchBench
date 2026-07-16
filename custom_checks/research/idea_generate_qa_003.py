"""Deterministic grading for research idea-generate QA-003."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['chain quality', 'filtering', 'mix ratio', 'accuracy', 'output length', 'diversity', 'noise', 'teacher', 'data selection', 'reasoning path']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
