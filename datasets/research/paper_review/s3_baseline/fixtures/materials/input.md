请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/adalora-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要
AdaLoRA vs LoRA 对比的关键数据：
- AdaLoRA 每步训练开销：forward/backward 比 LoRA 增加约 11-16%（Table 15 自报）；wall-clock 时间约 2-3x LoRA（wiki 分析推断，因需额外重要性评分计算和更长的收敛步数）
- AdaLoRA 使用 SVD 参数化（PΛQ），LoRA 使用 BA 分解
- AdaLoRA 额外优化目标：正交正则化 + triplet loss
- LoRA 仅 task loss
- 超参数搜索空间：AdaLoRA 约5-6维，LoRA 约2维
- 论文声称：在相同总参数预算下 AdaLoRA 优于 LoRA

## 上游 Wiki 摘要
AdaLoRA (Zhang et al., ICLR 2023): 基于重要性评分的自适应 budget 分配的 PEFT 方法。
