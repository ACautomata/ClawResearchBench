"""Deterministic grading for research idea-generate QA-040."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['attention sink', 'Long Range Arena', 'Pathfinder', 'S4', 'SSM', 'static pattern', 'spatial reasoning', 'self-attention failure', 'diluted attention', 'long-range dependency', 'attention collapse', 'selective mechanism']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
