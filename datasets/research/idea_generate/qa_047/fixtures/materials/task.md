研究谱系：self-supervised contrastive learning for vision。
[2020] SimCLR — 对比学习+大batch(8192)，ImageNet linear eval 70.0%。projection head 很重要。
[2020] MoCo v2 — momentum encoder + memory bank 解耦 batch dependency。
[2020] BYOL — 完全不需要负样本！positive-only 学习，74.3%。
[2021] SimSiam — 连 momentum encoder 都不需要，stop-gradient 防 collapse。质疑 BYOL 的 momentum 是否必要。
[2021] DINO — 自监督 ViT attention map 自动产生语义分割——无需 pixel-level 监督。
[2022] MAE — 转向 mask-and-reconstruct 范式(generative)，证明对比学习不是唯一路径。
当前 uncovered gaps: (1) 简化路径在细粒度/长尾/医疗图像上是否同样有效？(2) 不同 SSL 方法在哪种下游任务上各自最优？(3) SSL 预训练的计算最优分配没有系统回答。
