"""Deterministic grading for research idea-generate QA-041."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['batch size', 'contrastive learning', 'negative samples', 'BYOL', 'SimCLR', 'negative-free', 'long-tailed', 'representation collapse', 'gradient statistics', 'MoCo', 'tail class', 'positive-only']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
