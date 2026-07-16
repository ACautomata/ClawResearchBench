研究主题：tabular imputation 方法迁移到 missing modality imputation。
源域方法：MIWAE（Deep Generative Missingness Model）使用 VAE + importance weighting 在 UCI 数据集上做缺失值补全，关键优势：在 MAR（Missing At Random）和 MNAR（Missing Not At Random）下均有效。
目标域：多模态学习的 missing modality——例如 audio-visual speech recognition 中 video stream 间歇性缺失（camera occlusion），或 medical diagnosis 中某些 lab test 未做。特征：(1) 模态缺失通常是模态级（整个 modality missing）而非特征级（个别特征 missing）；(2) 模态间有 shared semantics——video+audio 共同表达说话内容，可以用可用模态推断缺失模态；(3) 缺失机制通常是 MNAR——lab test 不做是因为医生认为不需要（informative missingness）；(4) 补全的目标不是重建原始模态，而是提取对下游任务有用的特征。
迁移约束：只能用公开多模态数据集（AVSpeech/CMU-MOSEI/MIMIC-IV），不能访问缺失模态的真实值用于验证。
