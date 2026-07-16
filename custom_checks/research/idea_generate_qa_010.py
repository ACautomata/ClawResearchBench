"""Deterministic grading for research idea-generate QA-010."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['linear probing', 'fine-tuning', 'BYOL', 'SimCLR', 'evaluation protocol', 'ranking reversal', 'linear separability', 'transferability', 'checkpoint', 'protocol design']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
