"""Deterministic grading for research paper-review scenarios.

Encodes the rule-able portion of each source QA's rubric: required keyword
coverage (``must_contain``), required section headings (``fields``), and
forbidden phrases (``must_not_contain``). Subjective ``key_behavior`` /
``violation_penalty`` prose is intentionally dropped (issue #2 decision B).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from harness.custom_check_helpers import file_exists_checkpoint, skip_checkpoints


def grade_paper_review(
    workspace_path: str,
    output_rel: str,
    must_contain: Iterable[str],
    *,
    must_not_contain: Iterable[str] = (),
    fields: Iterable[str] = (),
    keyword_max: float = 0.6,
    fields_max: float = 0.2,
    forbidden_max: float = 0.1,
    exists_max: float = 0.1,
) -> dict:
    workspace = Path(workspace_path)
    checkpoints: dict[str, dict[str, object]] = {}
    output_path = workspace / output_rel
    file_exists_checkpoint(checkpoints, "output_exists", output_path, max_score=exists_max)

    required = list(must_contain)
    section_fields = [f for f in fields if str(f).strip()]
    forbidden = list(must_not_contain)

    # Reallocate the fields budget to keyword coverage when no section
    # headings are specified, so the checkpoint max always sums to 1.0.
    effective_keyword_max = keyword_max + (fields_max if not section_fields else 0.0)
    effective_fields_max = fields_max if section_fields else 0.0

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
    hits = sum(token.lower() in normalized for token in required)
    checkpoints["keyword_coverage"] = {
        "score": round(effective_keyword_max * hits / len(required), 4) if required else 0.0,
        "max": effective_keyword_max,
        "detail": f"required keywords={hits}/{len(required)}",
    }

    if section_fields:
        field_hits = sum(str(f).strip() in content for f in section_fields)
        checkpoints["required_fields"] = {
            "score": round(effective_fields_max * field_hits / len(section_fields), 4),
            "max": effective_fields_max,
            "detail": f"section headings={field_hits}/{len(section_fields)}",
        }

    leaked = [phrase for phrase in forbidden if phrase.lower() in normalized]
    checkpoints["no_forbidden_phrases"] = {
        "score": forbidden_max if not leaked else 0.0,
        "max": forbidden_max,
        "detail": "no forbidden phrases" if not leaked else f"forbidden phrases present={leaked}",
    }
    return {"checkpoints": checkpoints, "safety_violations": []}
