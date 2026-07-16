请阅读 Wiki 条目（16-section 结构化论文信息）：materials/wiki/tip-adapter-wiki.md

---

以下为上游阶段产出的摘要信息：

## 上游实验提取摘要（来自 S2 产出）
Tip-Adapter 的适用边界：
- 仅在 CLIP 视觉编码器（ViT-B/32, ViT-B/16, ResNet-50）上验证
- 11 个数据集涵盖通用分类（ImageNet）、细粒度（CUB, Flowers）、纹理（DTD）等
- 超参 α=1.0, β=5.5 对所有数据集固定，未在 per-task 最优值上进行对比
- 微调版本 Tip-Adapter-F 仅需 20 epoch，论文声称 5 分钟即可完成

论文声称 Tip-Adapter 是'通用的少样本分类适配方法'。

未验证的场景：大 shot 数（>128）、domain shift 极大时（仅有 ImageNet→ImageNetV2/Sketch 两个目标域）、非 CLIP backbone 上。
