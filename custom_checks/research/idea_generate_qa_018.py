"""Deterministic grading for research idea-generate QA-018."""

from custom_checks.research.idea_generate_rules import grade_keyword_output


KEYWORDS = ['fine-grained', 'alignment', 'CLIP', 'frozen backbone', 'contrastive loss', 'local-global', 'patch', 'grid', 'retrieval', 'attention', 'grounding', 'region']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_keyword_output(workspace_path, KEYWORDS)
