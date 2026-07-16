"""Deterministic grading for research idea-generate QA-009."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['CPU-only', '2 hours', 'catastrophic forgetting', 'replay buffer', 'regularization', 'forgetting rate', 'CIFAR-100', 'sequential tasks', 'finetuning baseline', 'training time budget']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
