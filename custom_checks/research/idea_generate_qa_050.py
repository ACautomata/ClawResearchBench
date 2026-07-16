"""Deterministic grading for research idea-generate QA-050."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['Chain-of-Thought', 'Self-Consistency', 'Tree-of-Thought', 'ReAct', 'Quiet-STaR', 'DeepSeek-R1', 'reasoning cost', 'Pareto frontier', 'emergent reasoning', 'safety', 'multi-agent debate', 'search efficiency', 'no-human-demonstration', 'lineage']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
