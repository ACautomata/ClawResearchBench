研究主题：continual learning for image classification。
硬约束：仅 CPU（无 GPU），最多 2 小时训练时间，数据集已按 10 个 sequential tasks 切分好（CIFAR-100 split）。
已有代码：基础 finetuning baseline（PyTorch，串行训练每个 task）。
已知问题：finetuning baseline 在第 5 个 task 后 catastrophic forgetting 严重，task 1 准确率从 70% 降至 25%。
用户偏好：低风险、Python only、容易复现、最好只加轻量正则化或 replay buffer。
