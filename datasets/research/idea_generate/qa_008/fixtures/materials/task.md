研究主题：model compression for edge deployment。
论文 A 摘要：知识蒸馏用 temperature scaling 将大模型 soft label 迁移到小模型，在 ResNet->MobileNet 上保持 95% 准确率，但模型仍需 50MB。
论文 B 摘要：Lottery Ticket Hypothesis 发现稀疏子网络可匹配原网络性能，非结构化剪枝可达 90% 稀疏度，但需要反复 iterative pruning。
约束：目标为边缘设备部署，模型必须 <10MB，保持 >90% 原准确率。指标为 accuracy retention 和 inference latency。
