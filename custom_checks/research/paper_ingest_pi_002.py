"""Deterministic grading for research paper-ingest PI-002."""

from __future__ import annotations

import re
from pathlib import Path

from harness.custom_check_helpers import file_exists_checkpoint, graded_content_match, skip_checkpoints


PAGE_PATH = Path("wiki/domains/bench/papers/edge-reg.md")
REQUIRED_FRONTMATTER = ("title:", "type: paper", "domain:", "evidence_level:", "created:", "updated:")
FORBIDDEN_GUESSES = ("可能是", "应该是")


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    workspace = Path(workspace_path)
    checkpoints: dict[str, dict[str, object]] = {}
    page_path = workspace / PAGE_PATH
    file_exists_checkpoint(checkpoints, "paper_page_exists", page_path, max_score=0.1)

    if not page_path.exists():
        skip_checkpoints(
            checkpoints,
            [
                ("frontmatter_complete", 0.2),
                ("all_sections_present", 0.3),
                ("source_grounding", 0.2),
                ("missing_information_explicit", 0.2),
            ],
            detail="skipped: paper page missing",
        )
        return {"checkpoints": checkpoints, "safety_violations": []}

    page = page_path.read_text(encoding="utf-8")
    normalized = page.lower()

    frontmatter_hits = sum(term in normalized for term in REQUIRED_FRONTMATTER)
    checkpoints["frontmatter_complete"] = {
        "score": round(0.2 * frontmatter_hits / len(REQUIRED_FRONTMATTER), 4),
        "max": 0.2,
        "detail": f"frontmatter fields={frontmatter_hits}/{len(REQUIRED_FRONTMATTER)}",
    }

    sections = {int(match) for match in re.findall(r"(?m)^##\s+(\d+)\.", page)}
    all_sections = sections == set(range(16)) and "## 15. 一句话总结" in page
    checkpoints["all_sections_present"] = {
        "score": 0.3 if all_sections else 0.0,
        "max": 0.3,
        "detail": f"numbered sections={sorted(sections)}",
    }

    graded_content_match(
        page,
        [("source_grounding", ["edge-aware", "论文中未明确说明"], 0.2)],
        checkpoints,
    )
    missing_explicit = "论文中未明确说明" in page and not any(term in page for term in FORBIDDEN_GUESSES)
    checkpoints["missing_information_explicit"] = {
        "score": 0.2 if missing_explicit else 0.0,
        "max": 0.2,
        "detail": "missing information marked without guesses" if missing_explicit else "missing marker absent or guessing language present",
    }
    return {"checkpoints": checkpoints, "safety_violations": []}
