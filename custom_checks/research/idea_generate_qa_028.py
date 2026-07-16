"""Deterministic grading for research idea-generate QA-028."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['Raspberry Pi', '50MB', '100ms latency', '1 hour training', 'anomaly detection', 'NAB', 'F1 score', 'LSTM-AE', 'model compression', 'feature engineering', 'memory budget', 'inference time']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
