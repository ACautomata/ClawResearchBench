请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/tree-of-thoughts-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要（来自 S2 产出）
ToT 仅在以下条件验证：
- 模型：GPT-4 和 GPT-3.5-turbo，未在 LLaMA、PaLM、Claude 上测试
- 任务：Game of 24、Creative Writing（2步BFS）、Mini Crosswords（DFS），未在编程、数据分析、事实QA上测试
- 搜索：仅 BFS 和 DFS，未探索 A* 或 MCTS
- 成本：GPT-4 Game of 24 约 $74/100题

论文声称 ToT 是通用的问题求解框架（'a general framework'）。

## 上游 Wiki 摘要
Tree of Thoughts (Yao et al., NeurIPS 2023): 将经典树搜索算法与 LLM 的语义级思维生成和自我评估结合。
