"""Deterministic grading for research idea-generate QA-001."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = (
    "trajectory matching",
    "class-balanced sampling",
    "synthetic",
    "minority class accuracy",
    "CIFAR-LT",
    "balanced accuracy",
    "majority class",
    "samples per class",
    "overfitting",
    "distillation budget",
)


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
