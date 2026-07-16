"""Deterministic grading for research idea-generate QA-007."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['prompt template', 'exemplar selection', 'domain gap', 'clinical notes', 'label imbalance', '1000 calls', 'no fine-tune', 'rare disease', 'feasibility', 'adaptation']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
