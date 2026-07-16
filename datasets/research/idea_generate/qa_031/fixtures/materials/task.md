研究主题：attention interpretability——attention weights 是否等于 feature importance？
论文 A（Attention is not Explanation, 2019）：通过在 attention weights 上施加对抗扰动（不改变预测），发现完全不同的 attention 分布可产生相同预测——即 attention weights 不可靠作为解释。
论文 B（Attention is not not Explanation, 2020）：反驳 A，声称只要正确选择'对抗扰动'的约束集——只扰动而不改变模型决策边界的先验——attention 就仍是可解释的。进一步声称 A 的扰动超出了合理范围。
张力：A 和 B 使用同一组实验（binary text classification on SNLI/MIMIC），但 B 的实验设置不同（adversarial objective 的 constraint 不同）。核心分歧：'什么算 fair perturbation'——这本身是一个方法论争议而非技术事实。
约束：只能做 controlled re-evaluation（不改模型），使用公开 text classification benchmark（SNLI/MIMIC/SST-2）。
