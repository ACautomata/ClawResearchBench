#!/usr/bin/env python3
"""Generate Phase 2 research scenarios from source qa.jsonl -- FULL scope.

Ports ALL 162 licensing-relevant QAs into ClawProBench as incubating
scenarios: idea-generate 47 + paper-review 112 + paper-review-pipeline 3.

Workspace fixture layout for each scenario::

  fixtures/
    materials/
      input.md            # full input_material text (paths normalized)
      wiki/*.md           # referenced wiki entries (copied from source)
      *_full.md / *_full_text.txt   # referenced full-text papers
      fle/*_fulltext.md   # ICLR/OpenReview full texts (copied)

This script does NOT touch any ClawProBench harness code.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

SRC = Path("/Users/junran/Documents/research-agent/benchmarks")
DST = Path("/Users/junran/Documents/ClawResearchBench")

SCENARIOS = DST / "scenarios" / "research"
DATASETS = DST / "datasets" / "research"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def sanitize(qa_id: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", qa_id.lower()).strip("_")


def _normalize_paths(text: str) -> str:
    """Replace source-absolute material refs with workspace-relative paths."""
    return re.sub(
        r"benchmarks?/paper-review/materials/",
        "materials/",
        text,
    )


def _copy_ref(rel_ref: str, src_root: Path, dst_materials: Path) -> None:
    """Copy one referenced file into the fixture's materials/ tree."""
    src_file = src_root / rel_ref
    # The ref might be relative to paper-review/materials/ or just a filename.
    if not src_file.exists():
        # Try with 'paper-review' prefix stripped.
        alt = src_root / Path(rel_ref).name
        if alt.exists():
            src_file = alt
        else:
            return  # e.g. nonexistent-* negative-test files
    dst_file = dst_materials / rel_ref
    dst_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_file, dst_file)


# ---------------------------------------------------------------------------
# YAML writer
# ---------------------------------------------------------------------------

def _write_yaml(path: Path, *, scenario_id: str, name: str, custom_check: str,
                custom_check_config: dict, seed_dir: str, prompt: str, category: str,
                timeout: int, difficulty: str = "medium") -> None:
    """Write a scenario YAML file using the yaml module so volatile prompt
    content is safely escaped regardless of internal colons / quotes.

    Emits YAML + fixture material only; no per-scenario .py wrapper is produced.
    Per-scenario grading config rides on the scenario as ``custom_check_config``
    and is consumed by the family grader named in ``custom_check``.
    """
    import yaml as _yaml
    data: dict = {
        "id": scenario_id,
        "name": name,
        "execution_mode": "live",
        "dimension": "research",
        "difficulty": difficulty,
        "benchmark_group": "intelligence",
        "benchmark_status": "incubating",
        "benchmark_core": False,
        "signal_source": "workspace_live",
        "weight": 1.0,
        "timeout_seconds": timeout,
        "optimal_steps": 6,
        "pass_threshold": 0.5,
        "tags": ["research", category.replace("research_", "").replace("_", "-"), "closed-world"],
        "prompt": "当前工作区已经放好了只读输入文件。\n\n" + prompt,
        "tools": [],
        "expected_tools": [],
        "ideal_tool_sequence": [],
        "custom_check": custom_check,
        "custom_check_config": custom_check_config,
        "workspace_seed_dir": seed_dir,
        "description": name,
        "objective": "Complete the research task grounded only in the seeded input material.",
        "prerequisites": [
            "The workspace is writable.",
            "Input material is present in materials/.",
        ],
        "steps": [
            "Read the seeded input material under materials/.",
            "Complete the requested analysis.",
            "Write the required output file(s).",
        ],
        "expected_outcome": "A grounded research artifact matching the deterministic rubric.",
        "scoring_criteria": [
            "Output file(s) exist.",
            "Required keywords and section headings are present.",
            "No forbidden phrases appear.",
        ],
        "time_limit": timeout,
    }
    path.write_text(_yaml.dump(data, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


# ---------------------------------------------------------------------------
# idea-generate (47 remaining)
# ---------------------------------------------------------------------------

def gen_idea_generate(qa: dict) -> None:
    sid = sanitize(qa["qa_id"])
    gold = qa.get("gold_answer") or {}
    keywords = [str(k) for k in (gold.get("must_contain") or []) if str(k).strip()]
    if not keywords:
        return

    fixture_dir = DATASETS / "idea_generate" / sid / "fixtures"
    (fixture_dir / "materials").mkdir(parents=True, exist_ok=True)
    (fixture_dir / "materials" / "task.md").write_text(
        qa.get("input_material", "") + "\n", encoding="utf-8",
    )

    seed_dir = f"../../datasets/research/idea_generate/{sid}/fixtures"
    prompt = (
        "请阅读 materials/task.md 中的研究材料，据此生成研究创意"
        "并创建 recommended-ideas.md。每个 idea 需说明依据、方法变化、"
        "评估指标、最小验证实验和风险，遵守材料中的约束。"
    )
    _write_yaml(SCENARIOS / f"idea_generate_{sid}.yaml",
                scenario_id=f"research_idea_generate_{sid}",
                name=f"Idea Generate {qa['qa_id']}",
                custom_check="research/idea_generate_grader.py",
                custom_check_config={"keywords": keywords},
                seed_dir=seed_dir, prompt=prompt,
                category="research_idea_generation", timeout=240)


# ---------------------------------------------------------------------------
# paper-review (112, including third-party)
# ---------------------------------------------------------------------------

MATERIALS_SRC_DIR = SRC / "paper-review" / "materials"

# Recognised file-reference patterns that appear in input_material.
REF_RE = re.compile(r"benchmarks?/paper-review/materials/([A-Za-z0-9_./\-]+\.(?:md|txt|json))")

# Skill-name patterns (Chinese) to strip from questions for prompt rewriting.
SKILL_NAMES = {
    "paper-experiment-deep-extractor": "提取论文中的实验信息",
    "paper-pipeline-quality-auditor": "审计文档中的质量问题",
    "paper-problem-analyzer": "分析论文中识别出的问题",
    "paper-validation-designer": "设计验证实验方案",
    "paper-codex-prompt-generator": "生成可执行验证的代码提示",
    "paper-report-compiler": "编写综合审阅报告",
}


def _rewrite_question(question: str) -> str:
    """Strip skill-name invocations and replace with task descriptions."""
    result = question
    for skill, desc in SKILL_NAMES.items():
        # "请执行 paper-experiment-deep-extractor，基于..."
        result = re.sub(rf"请执行\s*{re.escape(skill)}\s*[,，]?\s*", f"{desc}：", result)
        result = re.sub(rf"请执行\s*{re.escape(skill)}\s*。?\s*", f"{desc}。", result)
    return result


def gen_paper_review(qa: dict) -> None:
    sid = sanitize(qa["qa_id"])
    gold = qa.get("gold_answer") or {}
    must_contain = [str(k) for k in (gold.get("must_contain") or []) if str(k).strip()]
    must_not_contain = [str(k) for k in (gold.get("must_not_contain") or []) if str(k).strip()]
    fields = [str(k) for k in (gold.get("fields") or []) if str(k).strip()]
    if not must_contain and not fields:
        # Purely agent-judged QA with no deterministic gold beyond existence.
        # Still generate the scenario with an output-existence-only check.
        must_contain = []
        fields = []

    fixture_dir = DATASETS / "paper_review" / sid / "fixtures"
    mat_dir = fixture_dir / "materials"
    mat_dir.mkdir(parents=True, exist_ok=True)

    raw_input = qa.get("input_material", "")
    # Copy referenced files into the fixture.
    for ref in REF_RE.findall(raw_input):
        _copy_ref(ref, MATERIALS_SRC_DIR, mat_dir)

    normalized = _normalize_paths(raw_input)
    (mat_dir / "input.md").write_text(normalized + "\n", encoding="utf-8")

    output_rel = f"outputs/{sid}.md"
    seed_dir = f"../../datasets/research/paper_review/{sid}/fixtures"
    rewritten = _rewrite_question(qa.get("question", ""))
    prompt = (
        f"请阅读 materials/input.md 中的材料，按要求完成分析任务。\n\n"
        f"任务说明：{rewritten}\n\n"
        f"将完整 Markdown 结果写入 `{output_rel}`。\n"
        f"基于材料中的证据进行分析，不得编造材料中不存在的数据或结论。"
    )
    _write_yaml(SCENARIOS / f"paper_review_{sid}.yaml",
                scenario_id=f"research_paper_review_{sid}",
                name=f"Paper Review {qa['qa_id']}",
                custom_check="research/paper_review_grader.py",
                custom_check_config={
                    "output": output_rel,
                    "must_contain": must_contain,
                    "must_not_contain": must_not_contain,
                    "fields": fields,
                },
                seed_dir=seed_dir, prompt=prompt,
                category="research_paper_review", timeout=300,
                difficulty="hard")


# ---------------------------------------------------------------------------
# paper-review-pipeline (PRP-001..003, rules-judged, fedaux materials)
# ---------------------------------------------------------------------------

def gen_pipeline() -> None:
    for line in (SRC / "paper-review-pipeline" / "qa.jsonl").read_text().splitlines():
        qa = json.loads(line)
        sid = sanitize(qa["qa_id"])  # prp_001, prp_002, prp_003
        gold = qa.get("gold_answer") or {}
        must_contain = [str(k) for k in (gold.get("must_contain") or []) if str(k).strip()]
        expected = qa.get("expected_artifacts") or []

        fixture_dir = DATASETS / "paper_review_pipeline" / sid / "fixtures"
        mat_dir = fixture_dir / "materials"
        mat_dir.mkdir(parents=True, exist_ok=True)

        # Stage fedaux materials.
        for name in ("fedaux_experiment_deep_extraction.md", "fedaux_full_text.txt",
                      "fedaux_text.txt"):
            src = MATERIALS_SRC_DIR / name
            if src.exists():
                shutil.copy2(src, mat_dir / name)

        (mat_dir / "input.md").write_text(
            "FedAux 论文材料已放置在 materials/ 目录中：\n"
            "- fedaux_full_text.txt — 论文全文\n"
            "- fedaux_experiment_deep_extraction.md — 实验提取\n"
            "- fedaux_text.txt — 文本版本\n",
            encoding="utf-8",
        )

        # Build output file list and prompt.
        outputs = [f.replace("workspace-paper-review/outputs/bench-<run>/",
                              f"outputs/{sid}/")
                   for f in expected]
        (fixture_dir / "outputs" / sid).mkdir(parents=True, exist_ok=True)

        prompt = (
            "请阅读 materials/ 中的 FedAux 论文材料，完成以下 pipeline 任务。\n\n"
            f"任务：{_rewrite_question(qa.get('question', ''))}\n\n"
            "将结果写入以下文件：\n"
            + "\n".join(f"- `{o}`" for o in outputs) + "\n\n"
            "基于材料中的证据进行分析，不得编造材料中不存在的数据或结论。"
        )
        seed_dir = f"../../datasets/research/paper_review_pipeline/{sid}/fixtures"

        _write_yaml(SCENARIOS / f"paper_review_pipeline_{sid}.yaml",
                    scenario_id=f"research_paper_review_pipeline_{sid}",
                    name=f"Pipeline {qa['qa_id']}",
                    custom_check="research/paper_review_grader.py",
                    custom_check_config={
                        "outputs": outputs,
                        "keywords": must_contain,
                    },
                    seed_dir=seed_dir, prompt=prompt,
                    category="research_paper_review_pipeline", timeout=360,
                    difficulty="hard")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> int:
    done_idea = {"QA-001", "QA-002", "QA-005"}
    n_idea = n_pr = 0
    for line in (SRC / "idea-generate" / "qa.jsonl").read_text().splitlines():
        qa = json.loads(line)
        if qa["qa_id"] in done_idea:
            continue
        gen_idea_generate(qa)
        n_idea += 1
    for line in (SRC / "paper-review" / "qa.jsonl").read_text().splitlines():
        qa = json.loads(line)
        gen_paper_review(qa)
        n_pr += 1
    gen_pipeline()
    print(f"generated idea-generate: {n_idea}, paper-review: {n_pr}, pipeline: 3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
