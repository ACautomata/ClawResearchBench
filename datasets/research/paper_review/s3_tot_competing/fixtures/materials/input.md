请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/tree-of-thoughts-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要（来自 S2 产出）
ToT 在三个任务上的核心结果：
- Game of 24：ToT (b=5) 74% vs CoT 4% vs CoT-SC (k=100) 9%
- Creative Writing：ToT 7.56 vs CoT 6.93（GPT-4 1-10 评分）
- Mini Crosswords：ToT Letter 78%, Word 60%, Game 4/20 vs CoT Letter 40.6%, Word 15.6%, Game 1/20

ToT 使用 BFS（Game of 24, Creative Writing）和 DFS（Mini Crosswords）两种搜索策略。GPT-4 API 成本约 $206（2023年5月价格）。

## 上游 Wiki 摘要
Tree of Thoughts (Yao et al., NeurIPS 2023): 将经典树搜索算法（BFS/DFS）与 LLM 的语义级思维生成和自我评估结合，使 LLM 能进行深思熟虑的决策。
