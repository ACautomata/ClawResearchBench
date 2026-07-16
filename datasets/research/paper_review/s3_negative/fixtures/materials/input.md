请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/adalora-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要
AdaLoRA 的负面/中性结果：
- 高 budget (2M+): AdaLoRA 与 LoRA 差距消失
- CNN/DailyMail: 几乎持平（差距 <0.5 ROUGE），2.20% budget 下 LoRA 略高 0.03
- 训练时间: 2-3x LoRA
- 仅两种 backbone 上测试，无 decoder-only 实验

论文声称的全貌：摘要中写 'AdaLoRA 在所有任务和所有预算水平下一致优于 LoRA'。
