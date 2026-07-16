"""Shared deterministic grading for inline idea-generation rule scenarios."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from harness.custom_check_helpers import file_exists_checkpoint, skip_checkpoints


OUTPUT_PATH = Path("recommended-ideas.md")


def grade_keyword_output(
    workspace_path: str,
    keywords: Iterable[str],
    *,
    forbidden_phrases: Iterable[str] = (),
) -> dict:
    workspace = Path(workspace_path)
    checkpoints: dict[str, dict[str, object]] = {}
    output_path = workspace / OUTPUT_PATH
    file_exists_checkpoint(checkpoints, "output_exists", output_path, max_score=0.1)
    content = output_path.read_text(encoding="utf-8") if output_path.exists() else ""

    dependent = [("keyword_coverage", 0.8 if forbidden_phrases else 0.9)]
    if forbidden_phrases:
        dependent.append(("constraint_following", 0.1))

    if not content.strip():
        skip_checkpoints(checkpoints, dependent, detail="skipped: empty output")
        return {"checkpoints": checkpoints, "safety_violations": []}

    normalized = content.lower()
    required = list(keywords)
    hits = sum(keyword.lower() in normalized for keyword in required)
    coverage_max = 0.8 if forbidden_phrases else 0.9
    checkpoints["keyword_coverage"] = {
        "score": round(coverage_max * hits / len(required), 4) if required else 0.0,
        "max": coverage_max,
        "detail": f"source keywords={hits}/{len(required)}",
    }

    if forbidden_phrases:
        forbidden = [phrase for phrase in forbidden_phrases if phrase.lower() in normalized]
        checkpoints["constraint_following"] = {
            "score": 0.1 if not forbidden else 0.0,
            "max": 0.1,
            "detail": "constraints respected" if not forbidden else f"forbidden phrases={forbidden}",
        }

    return {"checkpoints": checkpoints, "safety_violations": []}
