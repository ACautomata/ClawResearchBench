"""Deterministic grading for research paper-review-pipeline PRP-003."""

from pathlib import Path
from harness.custom_check_helpers import file_exists_checkpoint, skip_checkpoints


OUTPUTS = ['outputs/prp_003/fedaux-experiment.md']
KEYWORDS = ['## 0. 文档定位', '## 1. 实验目标', '## 2. 实验设置总览', '## 3. 主结果提取', '## 11. 一段简短总结', 'FedAux', 'FedAvg', 'FedProx', 'SCAFFOLD', 'Dirichlet', 'Cora', 'PubMed']


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
