"""Deterministic grading for research idea-generate QA-048."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['FGSM', 'PGD', 'TRADES', 'AWP', 'perceptual attack', 'Denoised Smoothing', 'clean-robust tradeoff', 'fairness', 'certified radius', 'meta-attack', 'LPIPS', 'loss landscape', 'ImageNet-scale', 'lineage']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
