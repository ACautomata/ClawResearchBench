"""Deterministic grading for research idea-generate QA-044."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['GAT', 'GATv2', 'SuperGAT', 'Graph Transformer', 'NodeFormer', 'SGFormer', 'heterophilic', 'temporal graphs', 'scalability', 'interpretability', 'dynamic attention', 'positional encoding', 'lineage', 'O(N)']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
