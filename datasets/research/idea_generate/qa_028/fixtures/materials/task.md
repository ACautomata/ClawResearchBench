研究主题：time series anomaly detection on edge devices。
硬约束：部署在 Raspberry Pi 4（4GB RAM, ARM Cortex-A72），模型必须 <50MB（含权重+推理代码），推理延迟 <100ms per sample，每天最多 1 小时训练时间。
已有 baseline：简单的 moving average + 3-sigma 规则（CPU 5ms/sample，F1=0.62 on NAB benchmark）。
已知问题：深度学习模型（如 LSTM-AE、TranAD）在 NAB 上 F1 可达 0.80+，但模型大小为 200MB+。
用户偏好：Python only、轻量级特征工程可接受、不需要 stream processing。
