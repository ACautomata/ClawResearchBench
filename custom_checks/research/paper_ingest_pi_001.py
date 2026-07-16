"""Deterministic grading for research paper-ingest PI-001."""

from __future__ import annotations

import re
from pathlib import Path

from harness.custom_check_helpers import file_exists_checkpoint, skip_checkpoints


PAGE_PATH = Path("wiki/domains/bench/papers/benchingest.md")
REQUIRED_FRONTMATTER = ("title:", "type: paper", "domain:", "evidence_level:", "created:", "updated:")


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    workspace = Path(workspace_path)
    checkpoints: dict[str, dict[str, object]] = {}
    page_path = workspace / PAGE_PATH
    index_path = workspace / "wiki/index.md"
    log_path = workspace / "wiki/log.md"

    file_exists_checkpoint(checkpoints, "paper_page_exists", page_path, max_score=0.1)
    file_exists_checkpoint(checkpoints, "index_exists", index_path, max_score=0.1)
    file_exists_checkpoint(checkpoints, "log_exists", log_path, max_score=0.1)

    if not page_path.exists():
        skip_checkpoints(
            checkpoints,
            [("frontmatter_complete", 0.25), ("all_sections_present", 0.25)],
            detail="skipped: paper page missing",
        )
        skip_checkpoints(checkpoints, [("index_updated", 0.1), ("log_updated", 0.1)])
        return {"checkpoints": checkpoints, "safety_violations": []}

    page = page_path.read_text(encoding="utf-8")
    normalized = page.lower()
    frontmatter_hits = sum(term in normalized for term in REQUIRED_FRONTMATTER)
    checkpoints["frontmatter_complete"] = {
        "score": round(0.25 * frontmatter_hits / len(REQUIRED_FRONTMATTER), 4),
        "max": 0.25,
        "detail": f"frontmatter fields={frontmatter_hits}/{len(REQUIRED_FRONTMATTER)}",
    }

    sections = {int(match) for match in re.findall(r"(?m)^##\s+(\d+)\.", page)}
    all_sections = sections == set(range(16)) and "## 15. 一句话总结" in page
    checkpoints["all_sections_present"] = {
        "score": 0.25 if all_sections else 0.0,
        "max": 0.25,
        "detail": f"numbered sections={sorted(sections)}",
    }

    index = index_path.read_text(encoding="utf-8").lower() if index_path.exists() else ""
    index_updated = "benchingest" in index
    checkpoints["index_updated"] = {
        "score": 0.1 if index_updated else 0.0,
        "max": 0.1,
        "detail": "index references BenchIngest" if index_updated else "index missing BenchIngest",
    }

    log = log_path.read_text(encoding="utf-8").lower() if log_path.exists() else ""
    log_updated = "benchingest" in log
    checkpoints["log_updated"] = {
        "score": 0.1 if log_updated else 0.0,
        "max": 0.1,
        "detail": "log references BenchIngest" if log_updated else "log missing BenchIngest",
    }
    return {"checkpoints": checkpoints, "safety_violations": []}
