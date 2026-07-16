"""Deterministic grading for research idea-generate QA-042."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['ImageNet', 'medical imaging', 'texture bias', 'shape-based', 'CheXpert', 'pretraining', 'random init', 'volumetric', '2D vs 3D', 'domain gap', 'RadImageNet', 'task-specific pretraining']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
