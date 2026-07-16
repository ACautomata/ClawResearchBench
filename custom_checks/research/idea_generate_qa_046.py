"""Deterministic grading for research idea-generate QA-046."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['Adapter', 'Prefix Tuning', 'LoRA', 'IA3', 'QLoRA', 'DoRA', 'multi-task PEFT', 'rank theory', 'method combination', 'continual PEFT', 'reparameterization', 'parameter efficiency', 'lineage', 'composability']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
