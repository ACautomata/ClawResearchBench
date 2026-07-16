"""Deterministic grading for research idea-generate QA-012."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['low-rank', 'input-conditioning', 'activation rescaling', 'task taxonomy', 'interaction effect', 'discriminating experiment', 'competing hypothesis', 'LongRangeQA', 'CodeXGLUE', 'MMLU-Pro', 'LoRA', 'Prefix Tuning', 'IA3', 'task feature', 'rank reversal']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
