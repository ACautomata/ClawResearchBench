"""Deterministic grading for research paper-ingest PI-003."""

from __future__ import annotations

import re
from pathlib import Path

from harness.custom_check_helpers import file_exists_checkpoint, skip_checkpoints


OUTPUT_PATH = Path("wiki/domains/gnn-regularization/comparison.md")
REQUIRED_TERMS = (
    "edge-aware",
    "gated attention",
    "Cora",
    "CiteSeer",
    "Chameleon",
    "baseline",
    "evidence",
    "homophilous",
    "heterophilous",
)
ALLOWED_NUMBERS = {"1", "3"}
NUMBER_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?")


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    workspace = Path(workspace_path)
    checkpoints: dict[str, dict[str, object]] = {}
    output_path = workspace / OUTPUT_PATH
    file_exists_checkpoint(checkpoints, "comparison_exists", output_path, max_score=0.15)
    content = output_path.read_text(encoding="utf-8") if output_path.exists() else ""

    if not content.strip():
        skip_checkpoints(
            checkpoints,
            [("source_keyword_coverage", 0.7), ("no_fabricated_numbers", 0.15)],
            detail="skipped: empty comparison",
        )
        return {"checkpoints": checkpoints, "safety_violations": []}

    normalized = content.lower()

    hits = sum(term.lower() in normalized for term in REQUIRED_TERMS)
    checkpoints["source_keyword_coverage"] = {
        "score": round(0.7 * hits / len(REQUIRED_TERMS), 4),
        "max": 0.7,
        "detail": f"required terms={hits}/{len(REQUIRED_TERMS)}",
    }

    observed = set(NUMBER_RE.findall(content))
    fabricated = sorted(observed - ALLOWED_NUMBERS)
    checkpoints["no_fabricated_numbers"] = {
        "score": 0.15 if not fabricated else 0.0,
        "max": 0.15,
        "detail": "no fabricated numbers" if not fabricated else f"unexpected numbers={fabricated}",
    }
    return {"checkpoints": checkpoints, "safety_violations": []}
