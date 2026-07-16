研究主题：out-of-distribution generalization for vision transformers。
论文 A 摘要：ViT 在 ImageNet 上通过 patch-based attention 优于 CNN，但在 ImageNet-C（corruption）上精度下降 30%，远超 ResNet 的 15%。可能原因：patch embedding 对高频噪声更敏感。
论文 B 摘要：CNN 的 inductive bias（平移等变性、局部感受野）天然提供 OOD 鲁棒性，ViT 缺乏这些偏置，需要更多数据或更强的 augmentation。
约束：CIFAR-10-C/CIFAR-100-C 小规模验证，指标为 corruption error (CE) 和 relative robustness gap。
