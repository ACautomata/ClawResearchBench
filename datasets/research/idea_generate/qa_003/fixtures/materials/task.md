研究主题：reasoning distillation for small LLMs。
已失败实验：直接蒸馏 long-CoT 数据后，小模型准确率提升有限，输出长度显著增加。
论文 insight：多教师数据有助于覆盖不同 reasoning paths，但低质量 chain 会引入噪声。
约束：只能做数据筛选和训练数据配比，不能改模型结构。
