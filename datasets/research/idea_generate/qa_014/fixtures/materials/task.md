研究主题：Neural ODE 在 irregular time series 上的应用。
论文 A 摘要：Neural ODE 将时间序列建模为连续动态系统，相比 RNN 能自然处理不规则采样，但在 PhysioNet（48h ICU 数据）上仅比 GRU-D 高 1.2% AUROC。
论文 B 摘要：引入 attention-based time encoding 到 ODE solver，让模型感知采样间隔，在 MIMIC-III 上提升 3.5% 但计算量增加 4x。
约束：公开 benchmark（PhysioNet/MIMIC-III），指标为 AUROC + solver steps（效率）。
