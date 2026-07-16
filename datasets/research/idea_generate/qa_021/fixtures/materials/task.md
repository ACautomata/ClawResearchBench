研究主题：Neural Architecture Search (NAS) 搜索成本。
已失败实验：使用 DARTS 在 NAS-Bench-201 上搜索 cell 结构，search phase 耗费 12 GPU-hours，但最终发现的 architecture 的 test accuracy (94.1%) 与随机采样的 top-5 平均值 (93.8%) 无显著差异（p=0.34，Welch t-test）。zero-cost proxy（如 NASWOT、Synflow）虽然搜索仅需 5 秒，但与真实 accuracy 的 Spearman 相关系数在 NAS-Bench-301 上仅 0.45-0.55。
论文 insight：search space 设计可能比 search algorithm 更重要——如果 search space 中大部分 architecture 性能接近，NAS 的收益有限。
约束：只能用公开 NAS benchmark（NAS-Bench-201/301），不能设计新 search space。
