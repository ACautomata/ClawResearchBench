请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/react-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要（来自 S2 产出）
ReAct 在 ALFWorld 上的完整结果：

| Task | Best-of-6 | Average | 差距 |
|------|----------|---------|------|
| Pick | 92 | 65 | 27 |
| Clean | 58 | 39 | 19 |
| Heat | 96 | 83 | 13 |
| Cool | 86 | 76 | 10 |
| Look | 78 | 55 | 23 |
| Pick 2 | 41 | 24 | 17 |
| All | 71 | 57 | 14 |

论文摘要和结论中只引用了 Best-of-6 的 71% 作为主要结果。Average 57% 仅在表格中出现。

## 上游 Wiki 摘要
ReAct (Yao et al., ICLR 2023): 提出 Reasoning + Acting 交替的 LLM agent 框架，在 HotpotQA、Fever、ALFWorld、WebShop 四个 benchmark 上评估。
