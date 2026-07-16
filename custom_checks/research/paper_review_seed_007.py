"""Deterministic grading for research paper-review seed-007."""

from custom_checks.research.paper_review_rules import grade_paper_review


MUST_CONTAIN = ['## 0. 文档定位', 'CIFAR-10', 'CIFAR-100', 'TinyImageNet', 'FedAvg', 'FedProx', 'SCAFFOLD', 'FedDyn', '85.7%', 'lr=0.01', 'Dirichlet', '## 0. 文档定位', '## 2. 实验设置总览', '## 3. 主结果提取', '## 8. 值得关注的实验现象']
MUST_NOT_CONTAIN = []
FIELDS = ['## 0. 文档定位', '## 2. 实验设置总览', '## 3. 主结果提取', '## 8. 值得关注的实验现象']
OUTPUT_REL = 'outputs/seed_007.md'


def grade(workspace_path: str, trace: dict, tool_calls: list[dict]) -> dict:
    return grade_paper_review(
        workspace_path,
        OUTPUT_REL,
        MUST_CONTAIN,
        must_not_contain=MUST_NOT_CONTAIN,
        fields=FIELDS,
    )
