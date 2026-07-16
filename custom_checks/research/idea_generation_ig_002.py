"""Deterministic grading for research idea-generation IG-002."""

from __future__ import annotations

import re
from pathlib import Path

from harness.custom_check_helpers import file_exists_checkpoint, graded_content_match, skip_checkpoints


OUTPUT_PATH = Path("recommended-ideas.md")
ALLOWED_QUANTITATIVE_TOKENS = {"0.07", "0.18", "0.15", "0.16", "40%", "k=8", "@20", "1"}
NUMBER_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?|k\s*=\s*\d+|@\d+", re.IGNORECASE)
UNSUPPORTED_PHRASES = ("should be", "probably", "应该会", "可能会")


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    workspace = Path(workspace_path)
    checkpoints: dict[str, dict[str, object]] = {}
    output_path = workspace / OUTPUT_PATH
    file_exists_checkpoint(checkpoints, "output_exists", output_path, max_score=0.1)
    content = output_path.read_text(encoding="utf-8") if output_path.exists() else ""

    graded_content_match(
        content,
        [("hard_rule_coverage", ["TinyRec", "evidence", "metric", "risk", "validation"], 0.5)],
        checkpoints,
    )

    if not content.strip():
        skip_checkpoints(
            checkpoints,
            [("no_unsupported_language", 0.2), ("no_fabricated_numbers", 0.2)],
            detail="skipped: empty output",
        )
        return {"checkpoints": checkpoints, "safety_violations": []}

    normalized = content.lower()
    unsupported = [phrase for phrase in UNSUPPORTED_PHRASES if phrase.lower() in normalized]
    checkpoints["no_unsupported_language"] = {
        "score": 0.2 if not unsupported else 0.0,
        "max": 0.2,
        "detail": "no unsupported language" if not unsupported else f"unsupported phrases={unsupported}",
    }

    observed = {re.sub(r"\s+", "", token).lower() for token in NUMBER_RE.findall(content)}
    fabricated = sorted(observed - {token.lower() for token in ALLOWED_QUANTITATIVE_TOKENS})
    checkpoints["no_fabricated_numbers"] = {
        "score": 0.2 if not fabricated else 0.0,
        "max": 0.2,
        "detail": "no fabricated quantitative tokens" if not fabricated else f"unexpected quantitative tokens={fabricated}",
    }
    return {"checkpoints": checkpoints, "safety_violations": []}
