研究主题：self-supervised learning evaluation 争议。
论文 A（LINEAR）：在 ImageNet 上比较 SimCLR / MoCo / BYOL，使用 linear probing 评估，结论：BYOL > MoCo v2 > SimCLR。
论文 B（FINETUNE）：使用相同 backbone 和预训练数据，但改用 full fine-tuning 评估后发现排名完全颠倒：SimCLR > MoCo v2 > BYOL。
张力：两种评估协议给出相反的模型排名。
约束：无法重新训练 SSL 模型，只能在已有开源 checkpoint 上做评估协议对比实验。
