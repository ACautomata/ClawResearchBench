"""Deterministic grading for research idea-generate QA-033."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['early stopping', 'weight decay', 'rank correlation', 'overparameterization', 'ViT', 'equivalence breakdown', 'ImageNet', 'optimization trajectory', 'generalization bound', 'effective learning rate', 'model scale', 'complementary']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
