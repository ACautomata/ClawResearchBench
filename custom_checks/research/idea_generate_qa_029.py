"""Deterministic grading for research idea-generate QA-029."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['MCU', 'ARM Cortex-M4', '200KB', 'keyword spotting', 'MFCC', 'Speech Commands v2', 'int8 quantization', 'BC-ResNet', 'TFLite Micro', 'power budget', 'accuracy decay', 'feature extraction']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
