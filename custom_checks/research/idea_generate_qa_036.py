"""Deterministic grading for research idea-generate QA-036."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['DiffPool', 'point cloud', 'downsampling', 'SE(3)', 'k-NN graph', 'density', 'assignment matrix', 'invariance', 'ModelNet40', 'PointNet++', 'farthest point', 'geometric']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
