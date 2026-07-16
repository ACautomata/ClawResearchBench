"""Deterministic grading for research idea-generate QA-032."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['CutMix', 'small dataset', 'training budget', 'epochs', 'architecture vs augmentation', 'CIFAR-100', 'implicit regularization', 'ShakeDrop', 'conclusion reversal', 'interaction effect', 'compute tradeoff', 'data regime']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
