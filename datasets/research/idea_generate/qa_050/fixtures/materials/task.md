研究谱系：LLM reasoning enhancement。
[2022] Chain-of-Thought (Wei et al.) — GSM8K accuracy 从 18% 跃升至 58%。reasoning 仅从 prompting 涌现。
[2022] Self-Consistency (Wang et al.) — 多条 CoT + 投票，GSM8K 提升到 74%。
[2023] Tree-of-Thought (Yao et al.) — 线性链→搜索树，允许回溯。Game of 24 从 CoT 4%→74%。
[2023] ReAct (Yao et al.) — reasoning 与 tool use 交错：思考→调用工具→反思→再思考。
[2024] Quiet-STaR (Zelikman et al.) — 每个 token 位置并行生成内部思考，REINFORCE 优化。模型自己学会'何时该思考'。
[2025] DeepSeek-R1 (DeepSeek-AI) — pure RL 训练 LLM 产生 long chain-of-thought。reasoning 从 RL reward 自发涌现。
当前 uncovered gaps: (1) CoT→Tree-of-Thought→ReAct 增加了搜索成本(O(L)→O(B^D))，效率 vs accuracy 的 Pareto frontier 未系统研究；(2) Quiet-STaR 和 R1 证明'reasoning 可以不需要 human CoT 数据'，但自发涌现 reasoning 的可控性和安全性完全未探索；(3) multi-agent debate reasoning 在数学之外的领域效果未知。
