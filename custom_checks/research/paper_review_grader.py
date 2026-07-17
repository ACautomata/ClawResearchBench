"""Deep per-family grader for research paper-review scenarios.

Serves the 112 ``paper_review_*`` single-output scenarios plus the 3
``paper_review_pipeline_prp_*`` multi-output (pipeline) scenarios. Each scenario
carries its rubric as data in ``custom_check_config`` rather than as a copied
``.py`` wrapper, so a new scenario is one YAML entry, not a new file. Absorbs
the logic previously in ``paper_review_rules.grade_paper_review`` and the inline
multi-output pipeline check.

Config shapes (the grader owns its shape and fails fast on a missing key):

* single-output: ``output`` (relative path) + ``must_contain`` + ``must_not_contain``
  + ``fields``.
* multi-output pipeline: ``outputs`` (list of relative paths) + ``keywords``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from harness.custom_check_helpers import file_exists_checkpoint, skip_checkpoints


def _grade_single(workspace: Path, config: dict) -> dict:
    output_rel = config["output"]  # fail-fast: every single-output scenario declares its output path
    must_contain = list(config.get("must_contain") or [])
    must_not_contain = list(config.get("must_not_contain") or [])
    fields = [str(f).strip() for f in (config.get("fields") or []) if str(f).strip()]

    checkpoints: dict[str, dict[str, object]] = {}
    output_path = workspace / output_rel
    file_exists_checkpoint(checkpoints, "output_exists", output_path, max_score=0.1)

    keyword_max, fields_max, forbidden_max = 0.6, 0.2, 0.1
    # Reallocate the fields budget to keyword coverage when no section headings are
    # specified, so the checkpoint max always sums to 1.0.
    effective_keyword_max = keyword_max + (fields_max if not fields else 0.0)
    effective_fields_max = fields_max if fields else 0.0

    if not output_path.exists():
        skip_checkpoints(
            checkpoints,
            [
                ("keyword_coverage", effective_keyword_max),
                ("required_fields", effective_fields_max),
                ("no_forbidden_phrases", forbidden_max),
            ],
            detail="skipped: output missing",
        )
        return {"checkpoints": checkpoints, "safety_violations": []}

    content = output_path.read_text(encoding="utf-8")
    if not content.strip():
        skip_checkpoints(
            checkpoints,
            [
                ("keyword_coverage", effective_keyword_max),
                ("required_fields", effective_fields_max),
                ("no_forbidden_phrases", forbidden_max),
            ],
            detail="skipped: empty output",
        )
        return {"checkpoints": checkpoints, "safety_violations": []}

    normalized = content.lower()
    hits = sum(token.lower() in normalized for token in must_contain)
    checkpoints["keyword_coverage"] = {
        "score": round(effective_keyword_max * hits / len(must_contain), 4) if must_contain else 0.0,
        "max": effective_keyword_max,
        "detail": f"required keywords={hits}/{len(must_contain)}",
    }

    if fields:
        field_hits = sum(str(f).strip() in content for f in fields)
        checkpoints["required_fields"] = {
            "score": round(effective_fields_max * field_hits / len(fields), 4),
            "max": effective_fields_max,
            "detail": f"section headings={field_hits}/{len(fields)}",
        }

    leaked = [phrase for phrase in must_not_contain if phrase.lower() in normalized]
    checkpoints["no_forbidden_phrases"] = {
        "score": forbidden_max if not leaked else 0.0,
        "max": forbidden_max,
        "detail": "no forbidden phrases" if not leaked else f"forbidden phrases present={leaked}",
    }
    return {"checkpoints": checkpoints, "safety_violations": []}


def _grade_multi(workspace: Path, config: dict) -> dict:
    outputs = config["outputs"]  # fail-fast: every pipeline scenario declares its output list
    keywords = list(config.get("keywords") or [])

    checkpoints: dict[str, dict[str, object]] = {}
    n = len(outputs) or 1
    for rel in outputs:
        p = workspace / rel
        cid = "output_" + rel.replace(".", "_").replace("/", "_")
        file_exists_checkpoint(checkpoints, cid, p, max_score=round(0.05 * n, 4))

    combined = ""
    for rel in outputs:
        p = workspace / rel
        if p.exists():
            combined += p.read_text(encoding="utf-8") + "\n"

    if not combined.strip():
        skip_checkpoints(checkpoints, [("keyword_coverage", 0.6)])
        return {"checkpoints": checkpoints, "safety_violations": []}

    hits = sum(kw.lower() in combined.lower() for kw in keywords)
    checkpoints["keyword_coverage"] = {
        "score": round(0.6 * hits / len(keywords), 4) if keywords else 0.0,
        "max": 0.6,
        "detail": f"keywords={hits}/{len(keywords)}",
    }
    return {"checkpoints": checkpoints, "safety_violations": []}


def grade(workspace_path: str, trace: dict, tool_calls: list[dict], scenario: Any) -> dict:
    config = scenario.custom_check_config
    workspace = Path(workspace_path)
    if config.get("outputs"):
        return _grade_multi(workspace, config)
    return _grade_single(workspace, config)
