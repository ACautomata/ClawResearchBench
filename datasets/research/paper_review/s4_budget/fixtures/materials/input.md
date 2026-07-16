请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/adalora-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游 Wiki 摘要
AdaLoRA (ICLR 2023): 自适应 budget 分配的 PEFT 方法。DeBERTaV3-base + BART-large。

## 上游问题分析摘要（S3 产出）
高优先级验证问题：
P1: SVD 参数化 vs 自适应分配的独立贡献分离
P2: 不同 seed 下重要性排序是否一致（稳定性）
P3: decoder-only 架构上是否仍然有效
P4: 训练 2-3x 的成本是否被公平比较
P5: 重要性指标在不同任务类型上是否需要切换

预算约束：OpenAI API 使用限制 $500。GPT-4 每次评估约 $0.03-0.06。估计每个完整消融实验需要 20-50 次 API 调用。每个完整验证实验估计成本 $20-100。
