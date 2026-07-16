研究主题：early stopping vs explicit regularization for deep learning generalization。
论文 A（2019）：在 387 个 CIFAR-10 训练配置的元分析中，发现 early stopping 与 weight decay/L2 的效果几乎完全重叠（rank correlation 0.91）——即 early stopping 和显式正则化在功能上等价，选其一即可。
论文 B（2022）：在更大规模（ImageNet-level）和更现代架构（ViT/Swin）上重复分析，发现 early stopping 和 weight decay 的 rank correlation 降至 0.62——在过参数化模型中，early stopping 主要影响优化轨迹而非泛化边界；weight decay 的作用机制完全不同（控制 effective learning rate × weight norm）。
张力：小规模实验结论在大规模/现代架构上不成立；两个方法的等价性取决于模型过参数化程度。
约束：不能从头训练大型模型，但可以使用公开 pretrained checkpoint 做 fine-tuning 分析。
