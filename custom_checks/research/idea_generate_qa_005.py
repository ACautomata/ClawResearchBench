"""Deterministic grading for research idea-generate QA-005."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = (
    "FedAvg",
    "non-IID",
    "single GPU",
    "8 hours",
    "client",
    "communication rounds",
    "personalization",
    "regularization",
    "local fine-tuning",
    "worst-client",
)


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
