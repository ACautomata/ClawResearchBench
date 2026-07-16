"""Deterministic grading for research idea-generate QA-047."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['SimCLR', 'MoCo', 'BYOL', 'SimSiam', 'DINO', 'MAE', 'negative-free', 'projection head', 'stop-gradient', 'momentum encoder', 'generative vs contrastive', 'compute allocation', 'downstream specificity', 'lineage']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
