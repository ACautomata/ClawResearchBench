"""Deterministic grading for research idea-generate QA-015."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['disentanglement', 'reconstruction trade-off', 'causal graph', 'beta-VAE', 'MIG', 'dSprites', 'latent space', 'regularization', 'causal prior', 'identifiability', 'spurious', 'intervention']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
