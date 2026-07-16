"""Deterministic grading for research idea-generate QA-020."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['reward hacking', 'PPO', 'helpfulness', 'peak-then-decline', 'overoptimization', 'OOD reward', 'KL penalty', 'reward ensemble', 'early stopping', 'reward shaping', 'distribution shift', 'ground truth']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
