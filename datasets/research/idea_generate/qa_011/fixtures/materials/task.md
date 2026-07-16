研究主题：graph neural network explainability。
论文 A：GNNExplainer 通过边掩码学习子图解释，默认假设是'重要子图 = 对预测影响最大的子图'。
论文 B：PGExplainer 参数化解释生成，默认假设是'解释可泛化到新图，不依赖逐图重训'。
反例证据：最新 benchmark (Synthetic-XG) 发现两种方法在分布外图上的解释保真度均下降 40%+，说明默认假设可能不成立——'最大影响子图'未必是'因果相关子图'，'可泛化解释'在分布偏移时退化为'记忆化模板'。
约束：只能做 ≤500 个节点的图（CPU），指标为 explanation fidelity 和 OOD generalization gap。
