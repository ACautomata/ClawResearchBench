研究主题：parameter-efficient fine-tuning (PEFT) for large language models。
竞争性解释场景：
方法 A (LoRA)：低秩分解可以有效捕获微调信号——核心假设是'task adaptation lives in a low-rank subspace'。
方法 B (Prefix Tuning)：在输入前加可学习 token 即可——核心假设是'task adaptation is primarily input-conditioning, not weight modification'。
方法 C (IA3)：只缩放激活值——核心假设是'task adaptation requires only rescaling, not re-weighting'。
三种方法在 GLUE 上表现接近（±1%），但在 3 个新 benchmark（LongRangeQA, CodeXGLUE, MMLU-Pro）上排名完全相反：
- LongRangeQA: Prefix > IA3 > LoRA
- CodeXGLUE: LoRA > IA3 > Prefix
- MMLU-Pro: IA3 > LoRA > Prefix
张力：PEFT 方法的有效性与任务类型高度相关，但现有文献各自声称自己的假设'普遍成立'，无人系统比较'什么任务特征决定哪种 PEFT 更合适'。
约束：只能做 inference-only 验证（不能训练新 LLM），指标为 task-type × method 交互效应。
