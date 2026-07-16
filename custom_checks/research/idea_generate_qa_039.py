"""Deterministic grading for research idea-generate QA-039."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['heterophily', 'depth degradation', 'neighbor aggregation', 'negative signal', 'LINKX', 'GCN', 'Roman-Empire', 'MPNN assumption', 'feature vs topology', 'homophily assumption', 'adaptive depth', 'message passing']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
