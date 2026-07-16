"""Deterministic grading for research idea-generate QA-023."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['CheXpert', 'AUC drop', 'CutMix', 'anatomical', 'pathological validity', 'RandAugment', 'domain-agnostic', 'spurious feature', 'medical imaging', 'augmentation', 'plausibility', 'segmentation mask']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
