研究谱系：parameter-efficient fine-tuning (PEFT)。
[2019] Adapter — bottleneck 模块，~3% 参数。GLUE 接近 full fine-tuning。
[2021] Prefix Tuning — 输入前加可学习 token，<0.1% 参数。
[2021] LoRA — 低秩分解，<1% 参数，zero inference overhead。
[2022] (IA)^3 — 三组缩放向量，<0.01% 参数。
[2023] QLoRA — LoRA + 4-bit 量化，65B 模型单卡 fine-tune。
[2024] DoRA — magnitude + direction 分解。
当前 uncovered gaps: (1) multi-task/continual PEFT 几乎未探索；(2) LoRA rank 选择缺乏理论基础；(3) 不同 PEFT 方法的组合效果与交互未知。
