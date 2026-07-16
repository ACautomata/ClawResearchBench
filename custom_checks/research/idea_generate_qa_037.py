"""Deterministic grading for research idea-generate QA-037."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['missing modality', 'MIWAE', 'VAE', 'importance weighting', 'MNAR', 'MAR', 'multimodal', 'task-relevant imputation', 'shared semantics', 'audio-visual', 'informative missingness', 'cross-modal']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
