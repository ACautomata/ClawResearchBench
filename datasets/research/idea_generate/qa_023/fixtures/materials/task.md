研究主题：data augmentation for chest X-ray classification。
已失败实验：将 ImageNet 标准的强 augmentation（RandAugment、CutMix）直接应用到 CheXpert 胸部 X 光片分类上，AUC 反而下降（从 0.842 降到 0.831，p=0.03）。根本原因：CutMix 产生的混合图像（例如将气胸区域粘贴到正常肺上）创建了医学上不可能的特征组合，混淆了模型。
论文 insight：医学图像的 augmentation 必须保持解剖学/病理学合理性，domain-agnostic augmentation 可能引入虚假特征。
约束：只能设计 augmentation 策略，不能用更大模型或更多标注数据。已有 CheXpert/Chest X-ray14 benchmark。
