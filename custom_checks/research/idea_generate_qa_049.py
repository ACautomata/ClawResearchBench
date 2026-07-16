"""Deterministic grading for research idea-generate QA-049."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['FedAvg', 'FedProx', 'Per-FedAvg', 'Ditto', 'FedRep', 'pFedBayes', 'non-IID', 'personalization', 'meta-learning', 'privacy-personalization tradeoff', 'multi-modal FL', 'concept drift', 'representation sharing', 'lineage']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
