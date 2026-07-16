"""Deterministic grading for research idea-generate QA-034."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['RandAugment', 'time series', 'channel-wise', 'warping', 'causality', 'physical constraint', 'UEA archive', 'magnitude', 'magnitude adaptation', 'cross-channel', 'time causal', 'domain gap']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
