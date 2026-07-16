研究谱系：federated learning personalization。
[2017] FedAvg — 联邦学习基础。IID 效果好，non-IID 下降 10-20%。
[2020] FedProx — proximal term 约束本地更新不偏离全局。
[2020] Per-FedAvg — 重新定义为 meta-learning：学习好全局初始化。
[2021] Ditto — 同时训练全局+个性化本地模型，极端 non-IID 下显著优于 FedAvg+fine-tuning。
[2022] FedRep — shared representation + personalized head。representation 全局共享，classifier 本地个性化。
[2023] pFedBayes — Bayesian 框架统一 FL personalization，提供不确定性估计。
当前 uncovered gaps: (1) 真实 FL 的 non-IID 有更复杂结构（temporal shift/concept drift/adversarial clients）；(2) personalization 和 privacy 的联合优化——DP 约束可能与个性化冲突；(3) multi-modal FL（clients 不同 data modality）完全没有被现有方法覆盖。
