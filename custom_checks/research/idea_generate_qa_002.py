"""Deterministic grading for research idea-generate QA-002."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = (
    "scoring function",
    "CLIP",
    "FPR95",
    "AUROC",
    "concept matching",
    "fine-grained",
    "backbone",
    "inference",
    "calibration",
    "threshold",
)
FORBIDDEN_PHRASES = ("retrain the backbone", "重新训练 backbone", "fine-tune the backbone")


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS, forbidden_phrases=FORBIDDEN_PHRASES)
