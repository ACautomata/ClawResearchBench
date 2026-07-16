"""Deterministic grading for research paper-review-pipeline PRP-002."""

from pathlib import Path
from harness.custom_check_helpers import file_exists_checkpoint, skip_checkpoints


OUTPUTS = ['outputs/prp_002/fedaux-problem.md', 'outputs/prp_002/fedaux-validation.md']
KEYWORDS = ['## 0. 文档定位', '## 6. 简短结论', '## 9. 输出要求说明', '高优先级', '中优先级', '自变量', '控制变量', '观测指标', '如果问题成立', '如果问题不成立']


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    workspace = Path(workspace_path)
    checkpoints: dict[str, dict[str, object]] = {}
    n = len(OUTPUTS) or 1
    for rel in OUTPUTS:
        p = workspace / rel
        cid = 'output_' + rel.replace('.', '_').replace('/', '_')
        file_exists_checkpoint(checkpoints, cid, p, max_score=round(0.05 * n, 4))
    combined = ''
    for rel in OUTPUTS:
        p = workspace / rel
        if p.exists():
            combined += p.read_text(encoding='utf-8') + '\n'
    if not combined.strip():
        skip_checkpoints(checkpoints, [('keyword_coverage', 0.6)])
        return {'checkpoints': checkpoints, 'safety_violations': []}
    hits = sum(kw.lower() in combined.lower() for kw in KEYWORDS)
    checkpoints['keyword_coverage'] = {
        'score': round(0.6 * hits / len(KEYWORDS), 4) if KEYWORDS else 0.0,
        'max': 0.6,
        'detail': f'keywords={hits}/{len(KEYWORDS)}',
    }
    return {'checkpoints': checkpoints, 'safety_violations': []}
