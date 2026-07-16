研究主题：data augmentation vs architecture for small datasets。
论文 A（CutMix, 2019）：声称对于 CIFAR-100 with limited data（只用 20% 训练集），强 augmentation（CutMix+AutoAugment）比专门设计的小数据架构（如 PyramidNet+ShakeDrop）更有效——CutMix 提升 4.2%，而架构改进仅提升 2.1%。
论文 B（Rethinking Data Augmentation, 2021）：在相同设置下复现，发现当 training budget 从 300 epochs 增加到 1200 epochs 时，结论反转——架构改进（PyramidNet+ShakeDrop+EMA）提升 6.8%，而 CutMix 的边际收益降至 1.3%。即 augmentation 的优势来自 implicit regularization via longer effective training。
张力：A 和 B 对'什么更有效'给出相反结论，根本原因是 training budget 不同。
约束：只能在 CIFAR-100/Stanford Cars/FGVC-Aircraft 上验证，使用公开代码。
