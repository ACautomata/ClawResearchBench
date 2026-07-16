"""Deterministic grading for research idea-generate QA-035."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['code refactoring', 'style transfer', 'AST', 'functional equivalence', 'BLEU', 'content preservation', 'test case', 'adversarial style', 'differentiable compiler', 'syntax constraint', 'Styleformer', 'Python']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
