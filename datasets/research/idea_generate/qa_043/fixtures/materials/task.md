研究谱系：knowledge distillation。
[2015] Hinton et al. — 提出 KD 基础范式：teacher soft label + temperature scaling。CIFAR-100 提升 3-5%。
[2017] FitNet — 加入中间层 feature map 匹配（hint-based）。
[2019] CRD — 用对比学习取代直接 feature matching。ImageNet 上 KD gain 从 2.1% 扩大到 3.8%。
[2021] ReviewKD — 跨层连接（student shallow→teacher deep）。
[2023] MaskedKD — 随机 mask teacher features for student prediction。
当前 uncovered gaps: (1) 所有 KD 方法都在同架构验证，跨架构（ViT→CNN）和跨模态几乎无研究；(2) teacher 本身不完美时（biased/partially wrong）的蒸馏策略；(3) 蒸馏对 OOD robustness 的影响未知。
