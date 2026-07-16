请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/react-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要
ReAct 论文 Table 2：在 Fever 上，CoT hallucination 率 56%，ReAct 降至 0%。论文将此归因于 reasoning + acting 协同。

同期数据：
- ReAct reasoning error 47%（CoT 仅 16%）
- ReAct 的 Wikipedia API 搜索错误占失败案例的 23%
- Fever 是事实验证任务，Wikipedia API 搜索接口能精准命中相关页面

## 上游 Wiki 摘要
ReAct (Yao et al., ICLR 2023): LLM agent 交替输出 thought 和 action。Action 调用 Wikipedia API。
