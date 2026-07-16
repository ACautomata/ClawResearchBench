"""Deterministic grading for research idea-generate QA-019."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['object detection', 'KD', 'classification head', 'regression head', 'loss balancing', 'teacher-student', 'mAP', 'Faster R-CNN', 'logit', 'bounding box', 'weight schedule', 'task weight']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
