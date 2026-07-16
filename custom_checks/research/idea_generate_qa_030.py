"""Deterministic grading for research idea-generate QA-030."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['30fps', '33ms latency', 'GTX 1660', 'UCF-101', 'TSM', 'MobileNet', 'VideoMAE', 'temporal', 'batch=1', 'action recognition', 'real-time', 'temporal redundancy']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
