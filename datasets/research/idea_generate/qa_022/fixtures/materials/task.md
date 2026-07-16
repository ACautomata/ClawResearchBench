研究主题：self-supervised pretraining 的 representation collapse。
已失败实验：直接增加 SimSiam 的 predictor 深度（2 层→4 层）后，linear probing accuracy 反而下降（CIFAR-100: 62.3% → 58.1%），t-SNE 可视化显示 representations 退化到低维流形——即 model collapse 而非改进。减少 predictor 深度到 1 层则 accuracy 恢复到 63.5%。
论文 insight：predictor 的架构选择对 collapse 非常敏感，stop-gradient 操作不是万能的崩溃防护。
约束：只能改 projector/predictor 架构和损失函数，不能用负样本（保持 SimSiam 的 negative-free 特性）。
