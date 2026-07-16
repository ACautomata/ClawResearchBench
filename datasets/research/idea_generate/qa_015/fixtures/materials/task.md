研究主题：causal representation learning for disentanglement。
论文 A 摘要：beta-VAE 通过加大 KL 散度权重实现 disentanglement，但 reconstruction quality 显著下降，且两者的 trade-off 未被定量分析。
论文 B 摘要：将因果图结构注入 latent space 的正则化，在 dSprites 上 disentanglement score 提升 15%，但方法要求预知 causal graph，实际场景不可用。
约束：dSprites/Cars3D/Shapes3D 验证，指标为 MIG（Mutual Information Gap）和 FactorVAE score。
