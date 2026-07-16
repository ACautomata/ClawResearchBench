请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/self-refine-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要（来自 S2 产出）
Self-Refine 依赖 LLM 同时充当三个角色：
1. Generator：生成初始输出
2. Feedback Provider：对输出质量提供自然语言反馈
3. Refiner：基于反馈精炼输出

核心依赖：同一个 LLM 必须具备足够的自我评估能力。论文在 GPT-3.5、GPT-4、PaLM-2 上验证，但未系统测试弱模型的自我评估能力。

关键数据：
- 迭代 1-2 轮增益最大，3-4 轮后边际递减
- 对话任务（SOTOPIA）上 Self-Refine 提升 >10%，但在某些代码任务上改善 <2%

## 上游 Wiki 摘要
Self-Refine (Madaan et al., 2023): 让单个 LLM 通过迭代自反馈和精炼持续改进输出，无需训练或外部模型。
