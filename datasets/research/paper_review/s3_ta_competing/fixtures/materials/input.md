请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/tip-adapter-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要（来自 S2 产出）
Tip-Adapter 的核心声称：
1. Training-free：无需 SGD 训练即可提升 CLIP 少样本分类
2. Cache model：从训练集构造 key-value cache，通过特征检索注入知识
3. 性能：在 ImageNet 16-shot 上 Tip-Adapter-F 超越 CoOp、CLIP-Adapter 等需训练方法

关键数据：
- Tip-Adapter (training-free): ImageNet 16-shot 约 68%
- Tip-Adapter-F (fine-tuned): ImageNet 16-shot 约 73%（仅需 20 epoch，5分钟）
- 超参 α (residual ratio) 和 β (sharpness) 对所有数据集固定

## 上游 Wiki 摘要
Tip-Adapter (Zhang et al., 2022): 通过构建少样本训练集的 key-value cache model 实现无需训练的 CLIP 适配。
