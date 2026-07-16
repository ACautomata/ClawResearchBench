"""Deterministic grading for research idea-generate QA-025."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['hit rate', 'virtual screening', 'data leakage', 'temporal split', 'docking baseline', 'blinding', 'false positive', 'proprietary', 'unverifiable', 'wet lab', 'kinase', 'assay']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
