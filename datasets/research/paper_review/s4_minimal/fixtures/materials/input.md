请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/react-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游 Wiki 摘要
ReAct (ICLR 2023): LLM agent 交替 thought+action。

## 上游问题分析摘要（S3 产出）
最高优问题 P1: ReAct Hallucination 0% 是否来自 Wikipedia API 外部信息，而非 reasoning+acting 机制本身？

要求：只验证 P1，用最小数据集（Fever 的 100 条子集），最小 API 调用次数（<20 次）。
