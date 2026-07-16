研究主题：RLHF reward model overoptimization。
已失败实验：使用 PPO 微调 LLM 时，随着训练步数增加，reward model 打分持续上升（+0.8），但人工评估的 helpfulness 在第 2000 步达到峰值后开始下降（peak 3.8/5，最终 3.1/5）。即 reward model 被 overoptimized——模型学会了利用 reward model 的漏洞而非真正提升质量。
论文 insight：reward model 只在训练分布内准确，OOD response 的 reward 不可靠。
约束：不能重新训练 reward model，只能改 RL 训练策略（早停/正则化/reward shaping/多 reward ensemble）。
