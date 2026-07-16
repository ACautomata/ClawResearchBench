"""Deterministic grading for research idea-generation IG-001."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from harness.custom_check_helpers import (
    file_exists_checkpoint,
    graded_content_match,
    load_json_output,
    seeded_inputs_unchanged,
    skip_checkpoints,
    tool_arg_paths,
)


RUN_DIR = Path("idea-runs/ig-001")
ARTIFACTS = (
    "paper-context.md",
    "paper-context.json",
    "paper-analysis.md",
    "ideas.dedup.json",
    "recommended-ideas.md",
)
REQUIRED_IDEA_FIELDS = ("evidence", "metric", "risk", "validation")
ALLOWED_QUANTITATIVE_TOKENS = {"0.07", "0.18", "0.15", "0.16", "40%", "k=8", "@20", "1"}
NUMBER_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?|k\s*=\s*\d+|@\d+", re.IGNORECASE)


def _nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(_nonempty(item) for item in value)
    return value is not None


def _idea_structure_checkpoint(path: Path) -> dict[str, object]:
    payload, detail = load_json_output(path)
    if payload is None:
        return {"score": 0.0, "max": 0.2, "detail": detail}
    ideas = payload.get("ideas")
    if not isinstance(ideas, list) or not ideas:
        return {"score": 0.0, "max": 0.2, "detail": "ideas must be a non-empty list"}
    valid = sum(
        1
        for idea in ideas
        if isinstance(idea, dict)
        and all(field in idea and _nonempty(idea[field]) for field in REQUIRED_IDEA_FIELDS)
    )
    return {
        "score": round(0.2 * valid / len(ideas), 4),
        "max": 0.2,
        "detail": f"valid idea cards={valid}/{len(ideas)}",
    }


def _no_fabricated_numbers_checkpoint(content: str) -> dict[str, object]:
    observed = {re.sub(r"\s+", "", match).lower() for match in NUMBER_RE.findall(content)}
    allowed = {token.lower() for token in ALLOWED_QUANTITATIVE_TOKENS}
    fabricated = sorted(observed - allowed)
    return {
        "score": 0.15 if not fabricated else 0.0,
        "max": 0.15,
        "detail": "no fabricated quantitative tokens" if not fabricated else f"unexpected quantitative tokens={fabricated}",
    }


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    workspace = Path(workspace_path)
    output_dir = workspace / RUN_DIR
    checkpoints: dict[str, dict[str, object]] = {}

    for artifact in ARTIFACTS:
        check_id = "artifact_" + artifact.replace(".", "_").replace("-", "_")
        file_exists_checkpoint(checkpoints, check_id, output_dir / artifact, max_score=0.05)

    recommended_path = output_dir / "recommended-ideas.md"
    recommended = recommended_path.read_text(encoding="utf-8") if recommended_path.exists() else ""
    graded_content_match(
        recommended,
        [
            (
                "recommended_grounding",
                ["TinyRec", "SparseRec", "MovieLens-1M", "Recall@20", "metric", "risk", "validation"],
                0.3,
            )
        ],
        checkpoints,
    )
    checkpoints["ideas_structure"] = _idea_structure_checkpoint(output_dir / "ideas.dedup.json")
    if not recommended.strip():
        skip_checkpoints(checkpoints, [("no_fabricated_numbers", 0.15)], detail="skipped: empty output")
    else:
        checkpoints["no_fabricated_numbers"] = _no_fabricated_numbers_checkpoint(recommended)

    fixture_dir = Path(__file__).resolve().parents[2] / "datasets/research/idea_generation/ig-001/fixtures"
    inputs_ok, input_detail = seeded_inputs_unchanged(
        workspace,
        fixture_dir,
        ("paper/tinyrec.md", "paper/sparserec.md"),
    )
    checkpoints["inputs_unchanged"] = {
        "score": 0.1 if inputs_ok else 0.0,
        "max": 0.1,
        "detail": input_detail,
    }

    read_paths = tool_arg_paths(trace, tool_name="read")
    read_names = {Path(path).name for path in read_paths}
    process_score = len(read_names & {"tinyrec.md", "sparserec.md"}) / 2

    return {
        "checkpoints": checkpoints,
        "safety_violations": [],
        "process_score": process_score,
    }
