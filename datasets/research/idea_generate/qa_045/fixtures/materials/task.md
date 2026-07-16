研究谱系：diffusion model fast sampling。
[2020] DDPM — 1000 步采样，FID=3.17，推理需数分钟。
[2021] DDIM — 确定性采样，100 步，推理加速 10x。
[2022] DPM-Solver — ODE solver 数值方法，10-20 步达 SOTA。
[2022] Progressive Distillation — teacher(1024 steps)→student(8 steps)。
[2023] Consistency Models — 单步映射，无需迭代。CIFAR-10 单步 FID=6.2。
[2024] LCM-LoRA — consistency distillation 适配 Stable Diffusion，4-step 高质量生成。
当前 uncovered gaps: (1) Consistency Models 单步质量在复杂场景仍落后；(2) 条件生成下的 trade-off 曲线 vs 无条件生成完全不同；(3) 加速方法对 safety/fairness 的影响未知。
