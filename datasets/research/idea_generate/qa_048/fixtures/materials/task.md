研究谱系：adversarial training for robustness。
[2015] FGSM — 单步攻击+对抗训练，快速但防御有限。
[2018] PGD — 多步迭代攻击，CIFAR-10 robust accuracy 45-50%，但 clean accuracy 95%→87%。核心 insight：robustness-accuracy trade-off。
[2019] TRADES — 公式化 trade-off：clean loss + beta * robust boundary loss。
[2020] AWP — Adversarial Weight Perturbation，寻找更平坦 loss landscape。
[2021] Perceptual Adversarial Training — Lp-bounded attacks 不反映人类感知，语义级攻击 Lp-robust 模型几乎无防御。
[2023] Denoised Smoothing — 扩散去噪+随机平滑认证。ImageNet 首次 L2 radius=1.0 下 certified accuracy>40%。
当前 uncovered gaps: (1) ImageNet-scale 收敛性质完全不同；(2) adversarial training 对 fairness 的影响——不同 subgroup 的 robust accuracy 是否均匀？(3) 针对对抗训练的 meta-attack。
