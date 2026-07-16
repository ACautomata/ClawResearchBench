"""Deterministic grading for research idea-generate QA-045."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['DDPM', 'DDIM', 'DPM-Solver', 'Progressive Distillation', 'Consistency Models', 'LCM', 'sampling steps', 'FID', 'single-step', 'ODE solver', 'distillation', 'conditioned tradeoff', 'safety', 'lineage']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
