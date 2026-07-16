"""Deterministic grading for research idea-generate QA-016."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['functional correctness', 'test execution', 'pass@k', 'CodeBERTScore', 'HumanEval', 'semantic similarity', 'scoring function', 'test case', 'execution feedback', 'Spearman', 'coverage', 'oracle']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
